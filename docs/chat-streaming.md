# AI Tutor chat streaming contract (SSE)

> Status: 2026-06-17 · Authoritative description of the streaming reply
> format for `POST /api/v1/chat/sessions/{session_id}/messages/stream`.
> Resolves issue #167. The non-streaming twin
> `POST /api/v1/chat/sessions/{session_id}/messages` is unchanged and
> returns a single `ChatMessageResponse` JSON body.

## Transport

- **Method/path:** `POST /api/v1/chat/sessions/{session_id}/messages/stream`
- **Request body:** identical to the non-streaming endpoint —
  `SendMessageRequest`:
  ```jsonc
  {
    "content": "string (1..4000, required)",
    "interpreterSessionId": "string | null (optional)",
    "attachments": ["filename", "..."]   // optional, max 20
  }
  ```
- **Response content type:** `text/event-stream` (Server-Sent Events).
- **Response headers:** `Cache-Control: no-cache`, `X-Accel-Buffering: no`
  (disables proxy buffering so events flush promptly).
- **HTTP status:** always `200` once the stream opens. Failures that occur
  after the stream has begun are delivered **in-band** as `error` events,
  not as a non-200 status (see *Errors* below).

## Framing

Each SSE event is a single `data:` line containing one **JSON object**,
terminated by a blank line:

```
data: <json>\n\n
```

There is **no** `event:` field and **no** `id:` field — only `data:`
lines. There is **no `[DONE]` sentinel**; the terminal event is the one
with `type: "done"`.

## Event chunk schemas

Every chunk is a JSON object with a discriminating `type` field.

| `type`   | Shape | Meaning |
|----------|-------|---------|
| `status` | `{ "type": "status", "tool": "<tool name>" }` | The agent is about to run a tool round (e.g. `list_projects`). Zero or more before the answer. |
| `delta`  | `{ "type": "delta", "text": "<chunk>" }` | An incremental chunk of the assistant's answer. Concatenate `text` across all `delta` events to reconstruct the reply. |
| `done`   | `{ "type": "done", "message": <ChatMessageResponse> }` | **Terminal** event. Carries the full persisted assistant message (camelCase), including final `content`, `toolCalls`, token counts and `model`. |
| `error`  | `{ "type": "error", "detail": "<message>" }` | An error, delivered in-band. The stream ends after this. |

### `done.message` (`ChatMessageResponse`)

```jsonc
{
  "id": "uuid",
  "sessionId": "uuid",
  "role": "assistant",
  "content": "the full reply text",
  "toolCalls": [ { "id": "c1", "name": "list_projects", "argumentsJson": "{}" } ],
  "toolCallId": null,
  "tokensIn": 0,
  "tokensOut": 0,
  "model": "string | null",
  "createdAt": "2026-06-17T12:00:00Z"
}
```

`toolCalls` reflects the tool calls the assistant made on its final turn
(usually empty by the time the user-visible answer is produced). The
intermediate tool rounds are surfaced live via `status` events; the
per-round tool *result* messages are persisted server-side and available
afterward via `GET /api/v1/chat/sessions/{session_id}`.

## Ordering guarantees

1. Zero or more `status` events (one per tool round, in order).
2. Zero or more `delta` events carrying the answer text in order.
3. Exactly one terminal event: either `done` **or** `error`.

A turn that needs no tools emits only `delta`s then `done`. A turn that
fails before producing an answer may emit only an `error`.

## Reference transcripts

**Simple reply (no tools):**

```
data: {"type": "delta", "text": "Hello "}

data: {"type": "delta", "text": "world"}

data: {"type": "done", "message": {"id": "4f1c...", "sessionId": "9ab2...", "role": "assistant", "content": "Hello world", "toolCalls": [], "toolCallId": null, "tokensIn": 0, "tokensOut": 0, "model": "gpt-x", "createdAt": "2026-06-17T12:00:00Z"}}

```

**Reply that runs a tool first:**

```
data: {"type": "status", "tool": "list_projects"}

data: {"type": "delta", "text": "We build "}

data: {"type": "delta", "text": "CyberSTAC."}

data: {"type": "done", "message": {"id": "7d22...", "sessionId": "9ab2...", "role": "assistant", "content": "We build CyberSTAC.", "toolCalls": [], "toolCallId": null, "tokensIn": 0, "tokensOut": 0, "model": "gpt-x", "createdAt": "2026-06-17T12:00:00Z"}}

```

**Error mid-stream:**

```
data: {"type": "error", "detail": "chat provider unavailable"}

```

## Client guidance

- Parse line-by-line; for each `data:` line, JSON-parse the remainder and
  switch on `type`. Ignore unknown `type` values (forward-compatible).
- Treat `done` as success and `error` as failure; both are terminal. Do
  **not** wait for a `[DONE]` sentinel — it is never sent.
- The assistant text is the concatenation of `delta.text`, but the
  authoritative final text is `done.message.content` (use it to reconcile).
