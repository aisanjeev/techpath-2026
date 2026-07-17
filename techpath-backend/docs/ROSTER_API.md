# Roster API — contract

The external API that TechPath reads batches, students and trainers from. **You build
this; TechPath consumes it.**

TechPath already runs against a faithful mock of this contract
(`app/services/roster/mock_provider.py`, fixtures in `app/services/roster/fixtures/`).
Those fixtures are the executable version of this document — if something here is
ambiguous, the fixtures are the answer. When your API is ready, switching over is a
config change (`ROSTER_PROVIDER=http`), not a code change.

---

## Transport

- **Server-to-server only.** TechPath's backend calls you. Browsers never do, so no CORS
  is required.
- **Auth:** `X-API-Key: <key>` on every request. TechPath stores the key in Azure Key
  Vault, never in source.
- **HTTPS required.** Timestamps are UTC ISO-8601 (`2026-07-16T09:30:00Z`).
- Content type `application/json`.

## Response envelope

Every **list** endpoint returns:

```json
{
  "data": [ ... ],
  "meta": { "page": 1, "page_size": 100, "total": 250, "has_more": true }
}
```

Single-item endpoints may return the object directly or wrapped in `{"data": {...}}` —
TechPath accepts both.

---

## The three guarantees

Without these, the sync is unreliable in ways that are hard to notice and expensive to
debug. Everything else is negotiable; these are not.

### 1. `updated_since` works on every list endpoint

Filter on the record's `updated_at`, returning everything changed **at or after** the
given timestamp. This is how TechPath syncs incrementally instead of pulling your whole
database every few minutes.

Note it must be `>=`, not `>`. TechPath deliberately re-requests a one-minute overlap to
absorb clock skew between your server and ours, and relies on boundary records coming
back.

### 2. IDs are immutable

`id` is the join key. TechPath stores it as `external_id` and hangs attendance and
progress history off it. **If a student's `id` ever changes, that student's history is
orphaned** — they become a new person. IDs must survive edits, re-imports, and
migrations on your side.

### 3. Pagination is consistent and ordering is stable

Order by `id`. A record must never appear on two pages, or fall between them, while
paging. `has_more` must be accurate — TechPath keeps requesting pages until it is
`false`.

---

## Endpoints

```
GET /health
GET /batches?status=&trainer_id=&updated_since=&page=&page_size=
GET /batches/{id}
GET /batches/{id}/students?page=&page_size=
GET /students?updated_since=&page=&page_size=
GET /students/{id}
GET /trainers?updated_since=&page=&page_size=
```

`GET /health` returns 200 when you're up. TechPath surfaces this on the admin sync page.

### Batch

| Field | Type | Notes |
|---|---|---|
| `id` | string | **Required. Immutable.** |
| `name` | string | **Required.** |
| `code` | string | Human-facing label, e.g. `PY-2026-JUL-A` |
| `status` | string | `upcoming` \| `running` \| `completed` \| `cancelled` |
| `mode` | string | `online` \| `offline` \| `hybrid` |
| `start_date` / `end_date` | date | `YYYY-MM-DD` |
| `schedule` | object | `{ days: ["Mon","Wed"], start_time: "09:00", end_time: "11:00", timezone: "Asia/Kolkata" }` |
| `trainer_id` | string | |
| `trainer_name` | string | |
| **`trainer_email`** | string | **The mapping key.** Must equal the trainer's TechPath login email, or they will not see the batch. Case doesn't matter. |
| `course_ref` | string \| null | Your course code. Nullable — offline-only training needn't have one. |
| `student_count` | int | |
| `location` | string \| null | For offline batches |
| `updated_at` | datetime | **Required for `updated_since` to work.** |

### Student

| Field | Type | Notes |
|---|---|---|
| `id` | string | **Required. Immutable.** |
| `name` | string | **Required.** |
| `email` | string | **Identity join key.** Strongly preferred. |
| `roll_no` | string | |
| `phone` | string | |
| `status` | string | `active` \| `dropped` \| `completed` \| `on_hold` |
| `enrolled_on` | date | |
| `photo_url` | string \| null | |
| **`batch_ids`** | string[] | **Array — a student may be in several batches at once.** Authoritative: TechPath makes local membership match this exactly, so removing an id here removes them from that roster. |
| `updated_at` | datetime | **Required.** |

### Trainer

| Field | Type | Notes |
|---|---|---|
| `id` | string | **Required. Immutable.** |
| `name` | string | **Required.** |
| **`email`** | string | **Required. Must match their TechPath login email.** |
| `phone` | string | |
| `status` | string | |
| `expertise` | string[] | |
| `updated_at` | datetime | **Required.** |

---

## Error handling

- `4xx` — TechPath treats this as a permanent fault, surfaces the error, and does **not**
  retry.
- `429` / `5xx` / connection failures — retried up to 3 times with exponential backoff
  and jitter. `Retry-After` is honoured if you send it.
- Unknown fields are preserved verbatim rather than rejected, so you can add fields
  without coordinating a release with us.

---

## Optional extras, in priority order

1. **Change webhook** — `POST` to a TechPath endpoint when a batch or student changes, so
   we can stop polling.
2. **Attendance write-back** — `POST /batches/{id}/attendance` accepting
   `{ date, session_ref, records: [{ student_id, status, minutes_present }] }`. TechPath
   currently owns attendance; the service boundary for pushing it to you already exists
   (`app/services/attendance_service.py`).
3. **Soft deletes** — a `deleted_at` on list responses. Without it, a record you delete
   simply stops appearing and TechPath keeps its last known copy indefinitely.

---

## TechPath configuration

| Setting | Value |
|---|---|
| `ROSTER_PROVIDER` | `mock` (fixtures) or `http` (your API) |
| `ROSTER_API_BASE_URL` | Your base URL |
| `ROSTER_API_KEY` | The API key — **Key Vault only** |
| `ROSTER_SYNC_PAGE_SIZE` | Default `100` |

Sync runs from `scripts/sync_training.py` (cron/systemd timer), or on demand from the
admin UI. `GET /api/v1/training/sync/status` reports the provider, its health, and the
last run per resource.
