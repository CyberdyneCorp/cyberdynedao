# youtube Specification

## Purpose

Read-only access to public YouTube content as source material for the
chat agents (and any authenticated client): a video's transcript as
plain text, and a playlist's ordered video listing. The context stores
nothing and owns no persistence; it wraps YouTube over HTTP.

## Requirements

### Requirement: Video transcript retrieval

The system SHALL expose `GET /api/v1/youtube/transcript?video=<ref>&lang=<code>`
returning the video's transcript as plain text with the video id, its
canonical URL, and the language actually fetched. `video` accepts a
watch/short/embed/`youtu.be` URL or a bare 11-character id; `lang`
defaults to `en`, and the system MAY fall back to English when the
requested language has no transcript. Authentication SHALL be required
(the endpoint must not be an anonymous YouTube proxy). An unrecognizable
reference SHALL yield `422`; a missing video or a video without captions
SHALL yield `404`; YouTube being unreachable or throttling SHALL yield
`503`.

#### Scenario: Transcript fetched from a URL reference

- GIVEN an authenticated caller
- WHEN they request `/api/v1/youtube/transcript?video=https://youtu.be/<id>`
- THEN the response is `200` with `videoId`, `url`, `language`, and the
  transcript `text` as plain text

#### Scenario: Captions disabled

- GIVEN a video whose owner disabled captions
- WHEN its transcript is requested
- THEN the response is `404` with a detail explaining no transcript is
  available

#### Scenario: Anonymous caller rejected

- GIVEN no bearer token
- WHEN a transcript is requested
- THEN the response is `401`

### Requirement: Playlist listing

The system SHALL expose `GET /api/v1/youtube/playlist?playlist=<ref>`
returning the playlist's title, channel, and ordered video entries, each
with the video id, canonical watch URL, title, and duration in seconds
when known. `playlist` accepts any URL carrying `list=` or a bare
playlist id. Authentication SHALL be required. An unrecognizable
reference SHALL yield `422`; a missing or private playlist SHALL yield
`404`; YouTube being unreachable SHALL yield `503`.

#### Scenario: Playlist listed from a URL reference

- GIVEN an authenticated caller
- WHEN they request `/api/v1/youtube/playlist?playlist=https://www.youtube.com/playlist?list=<id>`
- THEN the response is `200` with `playlistId`, `url`, `title`,
  `channel`, and a `videos` array of `{videoId, url, title, durationS}`
  in playlist order
