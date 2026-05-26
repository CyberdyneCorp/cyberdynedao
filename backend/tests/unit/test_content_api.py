"""Wire-format tests for the content endpoints.

Verifies the response schemas serialize as camelCase (so the existing
SvelteKit components can consume them unchanged) and accept either
naming on input (so the Alembic seed migration's snake_case payload
still validates).
"""

from __future__ import annotations

from cyberdyne_backend.adapters.inbound.api.content.schemas import (
    BeliefResponse,
    CyberdynePageResponse,
    DomainResponse,
    RoadmapItemResponse,
    RoadmapPhaseResponse,
    TeamMemberResponse,
)


def test_team_member_response_serializes_to_camel_case() -> None:
    response = TeamMemberResponse(
        id="alice",
        name="Alice",
        title="Engineer",
        image_url="/x.webp",
        bio="builds stuff",
        tags=["python", "rust"],
        palette="blue",
    )
    data = response.model_dump(by_alias=True)
    assert "imageUrl" in data
    assert "image_url" not in data
    assert data["imageUrl"] == "/x.webp"
    # Other fields that are already single-word stay unchanged
    assert data["palette"] == "blue"
    assert data["tags"] == ["python", "rust"]


def test_team_member_response_accepts_snake_case_input() -> None:
    # The Alembic seed payload + the SQLAlchemy model both use
    # snake_case keys. populate_by_name=True keeps them valid.
    response = TeamMemberResponse.model_validate(
        {
            "id": "alice",
            "name": "Alice",
            "title": "Engineer",
            "image_url": "/x.webp",
            "bio": "b",
            "tags": [],
            "palette": "blue",
        }
    )
    assert response.image_url == "/x.webp"


def test_team_member_response_also_accepts_camel_case_input() -> None:
    response = TeamMemberResponse.model_validate(
        {
            "id": "alice",
            "name": "Alice",
            "title": "Engineer",
            "imageUrl": "/x.webp",
            "bio": "b",
            "tags": [],
            "palette": "blue",
        }
    )
    assert response.image_url == "/x.webp"


def test_cyberdyne_page_response_serializes_all_keys_to_camel_case() -> None:
    response = CyberdynePageResponse(
        hero_tagline="ht",
        intro_lead="il",
        intro_bullets=["b1"],
        domains=[
            DomainResponse(
                id="d1",
                name="D1",
                icon="🌍",
                palette="green",
                tagline="tag",
                projects=["P"],
                status="shipping",
            )
        ],
        beliefs=[BeliefResponse(title="t", description="d")],
        target_users=[],
        tokenomics_rows=[],
        token_utility_points=[],
        example_economics=[],
        roadmap_phases=[
            RoadmapPhaseResponse(
                id="p1",
                title="Phase 1",
                subtitle="s",
                status="shipped",
                color="green",
                items=[RoadmapItemResponse(icon="✓", text="done")],
            )
        ],
        closing_headline="ch",
        closing_body="cb",
    )
    data = response.model_dump(by_alias=True)
    expected_camel = {
        "heroTagline",
        "introLead",
        "introBullets",
        "domains",
        "beliefs",
        "targetUsers",
        "tokenomicsRows",
        "tokenUtilityPoints",
        "exampleEconomics",
        "roadmapPhases",
        "closingHeadline",
        "closingBody",
    }
    assert expected_camel.issubset(data.keys())
    # snake_case should be absent
    forbidden_snake = {
        "hero_tagline",
        "intro_lead",
        "intro_bullets",
        "target_users",
        "tokenomics_rows",
        "token_utility_points",
        "example_economics",
        "roadmap_phases",
        "closing_headline",
        "closing_body",
    }
    assert forbidden_snake.isdisjoint(data.keys())


def test_cyberdyne_page_response_accepts_snake_case_payload() -> None:
    # This is the exact shape stored in the content_pages.payload JSON
    # column by the baseline migration.
    payload = {
        "hero_tagline": "ht",
        "intro_lead": "il",
        "intro_bullets": ["b1"],
        "domains": [],
        "beliefs": [],
        "target_users": [],
        "tokenomics_rows": [],
        "token_utility_points": [],
        "example_economics": [],
        "roadmap_phases": [],
        "closing_headline": "ch",
        "closing_body": "cb",
    }
    response = CyberdynePageResponse.model_validate(payload)
    assert response.hero_tagline == "ht"
    assert response.closing_body == "cb"
