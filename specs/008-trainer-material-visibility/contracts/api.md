# API Contracts: Trainer Material Visibility

## Fetch Module Assets for a Session

To retrieve the materials published for a module, the frontend can query the existing module assets. If an endpoint does not exist to fetch assets for a given module ID (or session ID), one will be exposed or reused.

### Potential Endpoint

`GET /api/v1/modules/{module_id}/assets`

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "asset_id": 42,
      "display_order": 0,
      "is_required": true,
      "asset": {
        "id": 42,
        "title": "Introduction Deck",
        "asset_type": "presentation",
        "external_url": "https://example.com/deck1",
        "status": "published"
      }
    }
  ],
  "timestamp": "2026-07-18T10:00:00Z",
  "message": "Assets retrieved successfully"
}
```

The admin frontend (`techpath-admin`) will use this response to display the list of materials to the trainer.
