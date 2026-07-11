# websearch Specification

## Purpose

Read-only open-web search as a tool for the chat agents (and any
authenticated client): given a query, return organic search results and,
when the engine surfaces one, a concise direct answer. Backed by SERPAPI
(Google engine). The context stores nothing and owns no persistence.

## Requirements

### Requirement: Web search

The system SHALL expose `GET /api/v1/search?q=<query>&num=<n>` returning
the query, an optional direct `answer`, and an ordered `results` array of
`{position, title, url, snippet, source}`. `num` is bounded to 1..20
(default 10) and out-of-range values SHALL yield `422`. Authentication
SHALL be required (the endpoint must not be an anonymous search proxy).
An empty query SHALL yield `422`. When no SERPAPI key is configured the
capability is off and the endpoint SHALL yield `503`. A search-engine
failure (unreachable, invalid key, quota exhausted) SHALL yield `503`.

#### Scenario: Results returned for a query

- GIVEN an authenticated caller and a configured SERPAPI key
- WHEN they request `/api/v1/search?q=cyberdyne`
- THEN the response is `200` with `query`, an optional `answer`, and a
  `results` array of organic results in engine order

#### Scenario: Capability disabled

- GIVEN no SERPAPI key configured
- WHEN a search is requested
- THEN the response is `503`

#### Scenario: Anonymous caller rejected

- GIVEN no bearer token
- WHEN a search is requested
- THEN the response is `401`
