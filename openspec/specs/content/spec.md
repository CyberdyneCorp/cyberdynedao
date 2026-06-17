# content Specification

## Purpose

Serve the public marketing/site pages (team, projects, services, contact,
about, resource groups) from seeded data. Read-only in v1; admin authoring
is a future phase. (src: adapters/inbound/api/content/router.py)

## Requirements

### Requirement: Public site page reads

The system SHALL expose unauthenticated GET endpoints for the site's
content pages: `/api/v1/content/team`, `/cyberdyne`, `/projects`,
`/services`, `/contact`, `/resources`. A page that has not been seeded
SHALL return `404`.

#### Scenario: Fetch a seeded page

- GIVEN the team roster has been seeded
- WHEN a client GETs `/api/v1/content/team`
- THEN the system SHALL respond `200` with the list of team members

#### Scenario: Unseeded singleton page

- GIVEN the contact page has not been seeded
- WHEN a client GETs `/api/v1/content/contact`
- THEN the system SHALL respond `404`
