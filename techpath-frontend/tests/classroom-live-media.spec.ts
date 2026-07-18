import { test, expect, type Page, type Route } from '@playwright/test';

/**
 * Exercises the student-side live video wiring (ClassroomVideoTile, rendered inside
 * ClassroomApp's LiveScreen) end-to-end through the real /classroom page, with the
 * backend and the media server both mocked at the network layer — no live backend or
 * MediaMTX instance required to run this locally or in CI.
 *
 * This intentionally does not attempt to prove real audio/video renders (that needs a
 * live MediaMTX target and a human watching a screen — see quickstart.md Scenario 1 and
 * research.md Decision 5). What it does prove: joining a live session with a
 * `media.whep_url` drives the viewer through getUserMedia-free WHEP signaling and the
 * video tile leaves its "waiting for trainer" placeholder once signaling completes.
 *
 * The trainer side (PresenterVideoTile) lives in techpath-admin, a separate Next.js app
 * on a different port with its own Firebase-authenticated routes — out of scope for this
 * project's Playwright config; it is covered by `tsc --noEmit` plus the manual
 * quickstart.md walkthrough instead.
 */

const JOIN_CODE = '123456';
const SESSION_ID = 42;
const MOCK_WHEP_URL = 'https://mock-media.test/class-42-abcdef/whep';
const MOCK_HLS_URL = 'https://mock-media.test/class-42-abcdef/index.m3u8';

// A syntactically valid SDP answer with matching m-lines for the offer this component
// creates (one recvonly video transceiver, one recvonly audio transceiver). Real ICE/DTLS
// never completes against this fake fingerprint, but setRemoteDescription only validates
// syntax — it never blocks on peer reachability — so signaling completes and the UI
// leaves its "connecting" state.
const MOCK_SDP_ANSWER = [
  'v=0',
  'o=- 0 0 IN IP4 127.0.0.1',
  's=-',
  't=0 0',
  'a=group:BUNDLE 0 1',
  'a=msid-semantic: WMS',
  'm=video 9 UDP/TLS/RTP/SAVPF 96',
  'c=IN IP4 0.0.0.0',
  'a=rtcp:9 IN IP4 0.0.0.0',
  'a=ice-ufrag:mockufrag',
  'a=ice-pwd:mockpwdmockpwdmockpwdmock',
  'a=ice-options:trickle',
  'a=fingerprint:sha-256 00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF',
  'a=setup:active',
  'a=mid:0',
  'a=sendonly',
  'a=rtcp-mux',
  'a=rtpmap:96 VP8/90000',
  'm=audio 9 UDP/TLS/RTP/SAVPF 111',
  'c=IN IP4 0.0.0.0',
  'a=rtcp:9 IN IP4 0.0.0.0',
  'a=ice-ufrag:mockufrag',
  'a=ice-pwd:mockpwdmockpwdmockpwdmock',
  'a=ice-options:trickle',
  'a=fingerprint:sha-256 00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF',
  'a=setup:active',
  'a=mid:1',
  'a=sendonly',
  'a=rtcp-mux',
  'a=rtpmap:111 opus/48000/2',
  '',
].join('\r\n');

async function mockClassroomApi(route: Route, media: unknown) {
  const url = route.request().url();

  if (url.endsWith('/api/v1/classroom/join')) {
    return route.fulfill({
      json: {
        success: true,
        data: {
          session_id: SESSION_ID,
          batch_name: 'Test Batch',
          session_title: 'Live Media Test',
          module_title: null,
          status: 'live',
        },
      },
    });
  }

  if (url.endsWith('/api/v1/classroom/identify')) {
    return route.fulfill({
      json: {
        success: true,
        data: { matched: false, token: 'mock-classroom-token', display_name: 'Guest' },
      },
    });
  }

  if (url.includes(`/api/v1/classroom/${SESSION_ID}/state`)) {
    return route.fulfill({
      json: {
        success: true,
        data: {
          session_id: SESSION_ID,
          title: 'Live Media Test',
          status: 'live',
          batch_name: 'Test Batch',
          module_title: null,
          current_asset: null,
          open_poll: null,
          code: null,
          my_confusion: false,
          presence: { online: 1 },
          timer: null,
          media,
        },
      },
    });
  }

  return route.continue();
}

/** ClassroomCodeInput renders six unlabeled single-digit boxes (no placeholder/name —
 *  see ClassroomCodeInput.jsx) and auto-submits on the 6th keystroke. */
async function enterJoinCode(page: Page, code: string) {
  const boxes = page.locator('input[maxlength="1"]');
  await expect(boxes).toHaveCount(6);
  for (let i = 0; i < code.length; i++) {
    await boxes.nth(i).fill(code[i]);
  }
}

test.describe('Classroom live video tile', () => {
  test('renders no video area for a session that has no live media', async ({ page }) => {
    // media: null means a chat/poll-only class (the backend only populates media for a
    // live video session). The redesigned LiveScreen shows single-column content in that
    // case rather than a dead, empty video box — confirm no <video> is rendered but the
    // student did reach the live screen (the "waiting for your trainer" content shows,
    // since current_asset is null in the mock).
    await page.route('**/api/v1/classroom/**', (route) => mockClassroomApi(route, null));

    await page.goto('/classroom');
    await enterJoinCode(page, JOIN_CODE);
    await page.getByRole('button', { name: /continue as a guest/i }).click();
    await page.getByRole('button', { name: /join classroom/i }).click();

    await expect(page.getByText(/content will appear here as soon as they start/i)).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.locator('video')).toHaveCount(0);
  });

  test('connects the WHEP viewer once media.whep_url is present', async ({ page }) => {
    const media = { whep_url: MOCK_WHEP_URL, hls_url: null, mic_muted: false, camera_off: false, screen_sharing: false };
    await page.route('**/api/v1/classroom/**', (route) => mockClassroomApi(route, media));
    await page.route(MOCK_WHEP_URL, (route) =>
      route.fulfill({ status: 201, contentType: 'application/sdp', body: MOCK_SDP_ANSWER })
    );

    await page.goto('/classroom');
    await enterJoinCode(page, JOIN_CODE);
    await page.getByRole('button', { name: /continue as a guest/i }).click();
    await page.getByRole('button', { name: /join classroom/i }).click();

    // Placeholder must be gone — the tile has moved past "no media yet" into the
    // player, which is what proves the component picked up media.whep_url at all.
    await expect(page.getByText(/waiting for your trainer's camera/i)).not.toBeVisible({
      timeout: 15_000,
    });
    await expect(page.locator('video').first()).toBeVisible();
  });

  test('falls back to HLS on a genuine network failure reaching WHEP', async ({ page }) => {
    // route.abort() simulates the WHEP POST never reaching the server at all (DNS/
    // connection failure) — a real connectivity signal, distinct from a 404 (see the
    // next test). ClassroomVideoTile.jsx counts this the same way as an ICE failure:
    // after ICE_FAILURES_BEFORE_HLS (2) consecutive occurrences, it switches to HLS.
    const media = {
      whep_url: MOCK_WHEP_URL,
      hls_url: MOCK_HLS_URL,
      mic_muted: false,
      camera_off: false,
      screen_sharing: false,
    };
    await page.route('**/api/v1/classroom/**', (route) => mockClassroomApi(route, media));
    await page.route(MOCK_WHEP_URL, (route) => route.abort('connectionrefused'));

    let hlsPlaylistRequested = false;
    await page.route(MOCK_HLS_URL, (route) => {
      hlsPlaylistRequested = true;
      // hls.js only needs a well-formed manifest to fire MANIFEST_PARSED — it doesn't
      // need real segments to prove the fallback wiring picked up media.hls_url.
      return route.fulfill({
        status: 200,
        contentType: 'application/vnd.apple.mpegurl',
        body: '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-ENDLIST\n',
      });
    });

    await page.goto('/classroom');
    await enterJoinCode(page, JOIN_CODE);
    await page.getByRole('button', { name: /continue as a guest/i }).click();
    await page.getByRole('button', { name: /join classroom/i }).click();

    await expect.poll(() => hlsPlaylistRequested, { timeout: 15_000 }).toBe(true);
  });

  test('a 404 from WHEP ("no stream yet") never falls back to HLS — keeps retrying WHEP', async ({
    page,
  }) => {
    // Regression test for the real production bug: the backend hands out whep_url the
    // instant a session goes live, which is *before* the trainer's browser finishes its
    // own publish handshake. A clean 404 here means "no stream at this path yet", not a
    // blocked network — HLS would 404 for the exact same reason, so it must never be
    // attempted for this failure type; the component should just keep retrying WHEP.
    const media = {
      whep_url: MOCK_WHEP_URL,
      hls_url: MOCK_HLS_URL,
      mic_muted: false,
      camera_off: false,
      screen_sharing: false,
    };
    await page.route('**/api/v1/classroom/**', (route) => mockClassroomApi(route, media));

    let whepAttempts = 0;
    let hlsRequested = false;
    await page.route(MOCK_WHEP_URL, (route) => {
      whepAttempts += 1;
      return route.fulfill({
        status: 404,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'error', error: 'no stream is available' }),
      });
    });
    await page.route(MOCK_HLS_URL, (route) => {
      hlsRequested = true;
      return route.fulfill({ status: 404, body: 'not found' });
    });

    await page.goto('/classroom');
    await enterJoinCode(page, JOIN_CODE);
    await page.getByRole('button', { name: /continue as a guest/i }).click();
    await page.getByRole('button', { name: /join classroom/i }).click();

    // Wait long enough to observe several retry cycles (retry delay is 3s).
    await expect.poll(() => whepAttempts, { timeout: 12_000 }).toBeGreaterThanOrEqual(3);
    expect(hlsRequested).toBe(false);
    // Still showing a waiting/connecting state, not the terminal error copy.
    await expect(page.getByText(/couldn't connect to the live video/i)).not.toBeVisible();
  });
});
