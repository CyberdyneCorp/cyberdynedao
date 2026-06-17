# blog Specification

## Purpose

Editorial blog: editor-authored posts with one-way publish, public reads of
published posts, and an RSS feed. (src: adapters/inbound/api/blog/router.py,
domain/blog, application/blog)

## Requirements

### Requirement: Public post reads

The system SHALL expose unauthenticated `GET /api/v1/blog/posts` (paginated,
filterable by `category`/`tag`) and `GET /api/v1/blog/posts/{slug}`. Only
published posts SHALL be visible to anonymous callers; a draft or missing
slug SHALL return `404`. Published posts SHALL be ordered newest-first.
Pagination SHALL default to 20 and clamp to a maximum of 100.

#### Scenario: List hides drafts from the public

- GIVEN one draft post and one published post
- WHEN an anonymous client GETs `/api/v1/blog/posts`
- THEN only the published post is returned (total = 1)

#### Scenario: Editor sees drafts

- GIVEN the same two posts
- WHEN an editor lists posts with drafts included
- THEN both posts are returned

### Requirement: Editor authoring and one-way publish

The system SHALL allow an `editor` to create a post (`POST /api/v1/admin/blog/posts`,
created as draft, slug auto-derived from the title when omitted) and to
publish it (`POST /api/v1/admin/blog/posts/{slug}/publish`). Publishing a
draft SHALL set `published_at`. Publishing an already-published post SHALL
return `409`. A duplicate slug SHALL return `409`.

#### Scenario: Publish a draft

- GIVEN a draft post
- WHEN an editor publishes it
- THEN its status becomes published and `published_at` is set

#### Scenario: Re-publish is rejected

- GIVEN an already-published post
- WHEN an editor publishes it again
- THEN the system SHALL respond `409`

### Requirement: RSS feed

The system SHALL expose `GET /api/v1/blog/rss.xml` returning well-formed
`application/rss+xml` for published posts (newest-first, capped), with
HTML-escaped title/link/description. An empty catalogue SHALL yield a valid
feed with no `<item>` entries.

#### Scenario: Feed of published posts

- GIVEN published posts exist
- WHEN a client GETs `/api/v1/blog/rss.xml`
- THEN the response is valid RSS XML listing those posts newest-first
