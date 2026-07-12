"""Create the "Environmental Engineering" learning path + its modules via the
admin API (companion to ``create_computer_engineering_path``).

An operational, run-once helper, NOT app seed data. The courses are seeded by
the academy seed (reused chemistry/biology/geoscience/water/geospatial/AI
courses plus the 16 new environmental-specific courses); this curates them
into 14 modules and a path from scientific foundations through water, waste,
air, remediation, geospatial monitoring, management and climate to an AI and
resilience stage. Idempotent and extend-safe:
  * each module is POSTed (409 -> already exists, skipped);
  * the path is POSTed, OR - if it already exists - its ``moduleSlugs`` are
    PATCHed to include any new modules;
  * module + path translations (pt-BR/es/fr) are PUT (idempotent).

    python -m cyberdyne_backend.cli.create_environmental_engineering_path

Configuration via environment variables:
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_AUTH_BASE  default https://auth.backend.coolify.cyberdynecorp.ai
  ACADEMY_TOKEN      a bearer token (skips login), OR
  ACADEMY_EMAIL / ACADEMY_PASSWORD   to log in
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_API_BASE = "https://dao.backend.coolify.cyberdynecorp.ai"
DEFAULT_AUTH_BASE = "https://auth.backend.coolify.cyberdynecorp.ai"

MODULES: tuple[dict[str, Any], ...] = (
    {
        "slug": "env-foundations",
        "title": "Scientific Foundations",
        "category": "Environmental Engineering",
        "level": "Beginner",
        "duration": "38 hr",
        "icon": "\U0001f4d0",
        "description": "The mathematics, physics and statistics every environmental engineer builds on.",
        "topics": ["Calculus", "Physics", "Statistics"],
        "courseSlugs": [
            "math-basics",
            "math-intermediate",
            "physics-basics",
            "physics-intermediate",
            "math-probability",
        ],
    },
    {
        "slug": "env-computing",
        "title": "Computing and Data Science",
        "category": "Environmental Engineering",
        "level": "Beginner",
        "duration": "34 hr",
        "icon": "\U0001f4bb",
        "description": "Python, R, SQL, version control and numerical methods for environmental data.",
        "topics": ["Python", "R", "SQL", "Numerical methods"],
        "courseSlugs": [
            "python-course",
            "r-data-analysis-basics",
            "sql-basics",
            "git-basics",
            "math-numerical",
            "prob-stats-python-basics",
        ],
    },
    {
        "slug": "env-chemistry",
        "title": "Environmental Chemistry",
        "category": "Environmental Engineering",
        "level": "Intermediate",
        "duration": "36 hr",
        "icon": "\U0001f9ea",
        "description": "General, organic and analytical chemistry and the chemistry of the environment.",
        "topics": [
            "General chemistry",
            "Organic chemistry",
            "Analytical chemistry",
            "Environmental chemistry",
        ],
        "courseSlugs": [
            "general-chemistry-basics",
            "general-chemistry-intermediate",
            "organic-chemistry-basics",
            "analytical-chemistry-basics",
            "environmental-chemistry",
        ],
    },
    {
        "slug": "env-bio-ecology",
        "title": "Biology, Ecology and Microbiology",
        "category": "Environmental Engineering",
        "level": "Intermediate",
        "duration": "28 hr",
        "icon": "\U0001f9ec",
        "description": "Cell biology, ecology and environmental microbiology - the life science of the environment.",
        "topics": ["Cell biology", "Ecology", "Microbiology"],
        "courseSlugs": [
            "cell-biology-basics",
            "evolution-ecology-basics",
            "microbiology-basics",
            "microbiology-intermediate",
        ],
    },
    {
        "slug": "env-intro",
        "title": "Introduction and Representation",
        "category": "Environmental Engineering",
        "level": "Beginner",
        "duration": "14 hr",
        "icon": "\U0001f331",
        "description": "The profession and the language of technical drawings.",
        "topics": ["Environmental engineering", "Technical drawing", "CAD"],
        "courseSlugs": ["intro-environmental-engineering", "engineering-graphics-cad-basics"],
    },
    {
        "slug": "env-transport",
        "title": "Fluid Mechanics and Transport Phenomena",
        "category": "Environmental Engineering",
        "level": "Intermediate",
        "duration": "32 hr",
        "icon": "\U0001f30a",
        "description": "Fluid mechanics and the transport of heat and mass in environmental systems.",
        "topics": ["Fluid mechanics", "Heat transfer", "Mass transfer"],
        "courseSlugs": [
            "fluid-mechanics-basics",
            "fluid-mechanics-intermediate",
            "heat-transfer-basics",
            "mass-transfer-separations",
        ],
    },
    {
        "slug": "env-geo",
        "title": "Geosciences, Soil and Hydrology",
        "category": "Environmental Engineering",
        "level": "Intermediate",
        "duration": "24 hr",
        "icon": "\U0001faa8",
        "description": "Engineering geology, soil mechanics and hydrology - the physical setting of environmental work.",
        "topics": ["Geology", "Soil", "Hydrology"],
        "courseSlugs": ["engineering-geology", "soil-mechanics", "hydrology-water-resources"],
    },
    {
        "slug": "env-water-sanitation",
        "title": "Water Supply, Treatment and Sanitation",
        "category": "Environmental Engineering",
        "level": "Advanced",
        "duration": "40 hr",
        "icon": "\U0001f6b0",
        "description": "Water quality monitoring, drinking-water and wastewater treatment, and urban sanitation.",
        "topics": ["Water quality", "Water treatment", "Wastewater", "Sanitation"],
        "courseSlugs": [
            "water-quality-monitoring",
            "water-treatment",
            "wastewater-treatment",
            "sanitation-drainage",
        ],
    },
    {
        "slug": "env-waste-air",
        "title": "Waste and Air Pollution",
        "category": "Environmental Engineering",
        "level": "Advanced",
        "duration": "30 hr",
        "icon": "\U0001f5d1",
        "description": "Solid waste management, air pollution control, and industrial environmental processes.",
        "topics": ["Solid waste", "Air pollution", "Industrial processes"],
        "courseSlugs": [
            "solid-waste-management",
            "air-pollution-control",
            "environmental-process-engineering",
        ],
    },
    {
        "slug": "env-remediation",
        "title": "Hydrogeology, Contamination and Modeling",
        "category": "Environmental Engineering",
        "level": "Advanced",
        "duration": "28 hr",
        "icon": "\U0001f9ea",
        "description": "Groundwater, contaminant transport and remediation, and environmental modeling.",
        "topics": ["Hydrogeology", "Remediation", "Modeling"],
        "courseSlugs": [
            "hydrogeology-remediation",
            "environmental-modeling",
            "computational-fluid-dynamics-basics",
        ],
    },
    {
        "slug": "env-geospatial",
        "title": "Geospatial and Remote Sensing",
        "category": "Environmental Engineering",
        "level": "Intermediate",
        "duration": "34 hr",
        "icon": "\U0001f6f0",
        "description": "GIS, remote sensing and geospatial modeling for environmental monitoring.",
        "topics": ["GIS", "Remote sensing", "Geospatial modeling"],
        "courseSlugs": [
            "gis-fundamentals",
            "remote-sensing-fundamentals",
            "remote-sensing-analysis",
            "environmental-geospatial-modeling",
            "spatial-databases-postgis",
        ],
    },
    {
        "slug": "env-management-law",
        "title": "Impact, Management and Risk",
        "category": "Environmental Engineering",
        "level": "Advanced",
        "duration": "30 hr",
        "icon": "\U0001f4cb",
        "description": "Environmental impact assessment, management systems and auditing, risk, and economics.",
        "topics": ["Impact assessment", "ISO 14001", "Risk", "Economics"],
        "courseSlugs": [
            "environmental-impact-assessment",
            "environmental-management-auditing",
            "environmental-risk-assessment",
            "process-economics-management",
        ],
    },
    {
        "slug": "env-climate-sustainability",
        "title": "Climate, Energy and Restoration",
        "category": "Environmental Engineering",
        "level": "Advanced",
        "duration": "30 hr",
        "icon": "\U0001f30d",
        "description": "Climate change and carbon, sustainable processes, renewable energy, and ecological restoration.",
        "topics": ["Climate change", "Carbon", "Renewable energy", "Restoration"],
        "courseSlugs": [
            "climate-change-carbon",
            "sustainable-processes",
            "renewable-ev-basics",
            "ecological-restoration",
        ],
    },
    {
        "slug": "env-ai-resilience",
        "title": "AI, Data and Resilience",
        "category": "Environmental Engineering",
        "level": "Advanced",
        "duration": "30 hr",
        "icon": "\U0001f9e0",
        "description": "AI and data science for the environment, geospatial deep learning, and disaster resilience.",
        "topics": ["Machine learning", "GeoAI", "Digital twins", "Resilience"],
        "courseSlugs": [
            "ai-for-environmental-engineering",
            "disaster-risk-resilience",
            "ml-for-engineering-basics",
            "geoai-deep-learning",
        ],
    },
)

PATH: dict[str, Any] = {
    "slug": "environmental-engineering",
    "title": "Environmental Engineering",
    "description": (
        "A full environmental-engineering curriculum, from scientific, chemistry and "
        "biology foundations through water supply and treatment, wastewater, solid "
        "waste, air pollution, hydrogeology and remediation, geospatial monitoring, "
        "impact assessment and management, and climate and sustainability - closing "
        "with AI, data science and disaster resilience for the environment."
    ),
    "moduleSlugs": [m["slug"] for m in MODULES],
    "estimatedTime": "56-68 weeks",
    "icon": "\U0001f331",
}

MODULE_TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    "env-foundations": {
        "pt-BR": {
            "title": "Fundamentos Cientificos",
            "description": "A matematica, fisica e estatistica que todo engenheiro ambiental usa.",
        },
        "es": {
            "title": "Fundamentos Cientificos",
            "description": "Las matematicas, la fisica y la estadistica que todo ingeniero ambiental usa.",
        },
        "fr": {
            "title": "Fondements Scientifiques",
            "description": "Les mathematiques, la physique et les statistiques de base de l'ingenieur en environnement.",
        },
    },
    "env-computing": {
        "pt-BR": {
            "title": "Computacao e Ciencia de Dados",
            "description": "Python, R, SQL, controle de versao e metodos numericos para dados ambientais.",
        },
        "es": {
            "title": "Computacion y Ciencia de Datos",
            "description": "Python, R, SQL, control de versiones y metodos numericos para datos ambientales.",
        },
        "fr": {
            "title": "Informatique et Science des Donnees",
            "description": "Python, R, SQL, gestion de versions et methodes numeriques pour les donnees environnementales.",
        },
    },
    "env-chemistry": {
        "pt-BR": {
            "title": "Quimica Ambiental",
            "description": "Quimica geral, organica e analitica e a quimica do meio ambiente.",
        },
        "es": {
            "title": "Quimica Ambiental",
            "description": "Quimica general, organica y analitica y la quimica del medio ambiente.",
        },
        "fr": {
            "title": "Chimie de l'Environnement",
            "description": "Chimie generale, organique et analytique et la chimie de l'environnement.",
        },
    },
    "env-bio-ecology": {
        "pt-BR": {
            "title": "Biologia, Ecologia e Microbiologia",
            "description": "Biologia celular, ecologia e microbiologia ambiental.",
        },
        "es": {
            "title": "Biologia, Ecologia y Microbiologia",
            "description": "Biologia celular, ecologia y microbiologia ambiental.",
        },
        "fr": {
            "title": "Biologie, Ecologie et Microbiologie",
            "description": "Biologie cellulaire, ecologie et microbiologie environnementale.",
        },
    },
    "env-intro": {
        "pt-BR": {
            "title": "Introducao e Representacao",
            "description": "A profissao e a linguagem dos desenhos tecnicos.",
        },
        "es": {
            "title": "Introduccion y Representacion",
            "description": "La profesion y el lenguaje de los dibujos tecnicos.",
        },
        "fr": {
            "title": "Introduction et Representation",
            "description": "La profession et le langage des dessins techniques.",
        },
    },
    "env-transport": {
        "pt-BR": {
            "title": "Mecanica dos Fluidos e Fenomenos de Transporte",
            "description": "Mecanica dos fluidos e transporte de calor e massa em sistemas ambientais.",
        },
        "es": {
            "title": "Mecanica de Fluidos y Fenomenos de Transporte",
            "description": "Mecanica de fluidos y transporte de calor y masa en sistemas ambientales.",
        },
        "fr": {
            "title": "Mecanique des Fluides et Phenomenes de Transport",
            "description": "Mecanique des fluides et transfert de chaleur et de matiere dans les systemes environnementaux.",
        },
    },
    "env-geo": {
        "pt-BR": {
            "title": "Geociencias, Solo e Hidrologia",
            "description": "Geologia de engenharia, mecanica dos solos e hidrologia.",
        },
        "es": {
            "title": "Geociencias, Suelo e Hidrologia",
            "description": "Geologia de ingenieria, mecanica de suelos e hidrologia.",
        },
        "fr": {
            "title": "Geosciences, Sol et Hydrologie",
            "description": "Geologie de l'ingenieur, mecanique des sols et hydrologie.",
        },
    },
    "env-water-sanitation": {
        "pt-BR": {
            "title": "Agua, Tratamento e Saneamento",
            "description": "Monitoramento da qualidade da agua, tratamento de agua e esgoto e saneamento urbano.",
        },
        "es": {
            "title": "Agua, Tratamiento y Saneamiento",
            "description": "Monitoreo de calidad del agua, tratamiento de agua y aguas residuales y saneamiento urbano.",
        },
        "fr": {
            "title": "Eau, Traitement et Assainissement",
            "description": "Surveillance de la qualite de l'eau, traitement de l'eau et des eaux usees et assainissement urbain.",
        },
    },
    "env-waste-air": {
        "pt-BR": {
            "title": "Residuos e Poluicao do Ar",
            "description": "Gestao de residuos solidos, controle da poluicao atmosferica e processos industriais.",
        },
        "es": {
            "title": "Residuos y Contaminacion del Aire",
            "description": "Gestion de residuos solidos, control de la contaminacion atmosferica y procesos industriales.",
        },
        "fr": {
            "title": "Dechets et Pollution de l'Air",
            "description": "Gestion des dechets solides, controle de la pollution atmospherique et procedes industriels.",
        },
    },
    "env-remediation": {
        "pt-BR": {
            "title": "Hidrogeologia, Contaminacao e Modelagem",
            "description": "Agua subterranea, transporte de contaminantes e remediacao, e modelagem ambiental.",
        },
        "es": {
            "title": "Hidrogeologia, Contaminacion y Modelado",
            "description": "Agua subterranea, transporte de contaminantes y remediacion, y modelado ambiental.",
        },
        "fr": {
            "title": "Hydrogeologie, Contamination et Modelisation",
            "description": "Eaux souterraines, transport de contaminants et remediation, et modelisation environnementale.",
        },
    },
    "env-geospatial": {
        "pt-BR": {
            "title": "Geoespacial e Sensoriamento Remoto",
            "description": "SIG, sensoriamento remoto e modelagem geoespacial para monitoramento ambiental.",
        },
        "es": {
            "title": "Geoespacial y Teledeteccion",
            "description": "SIG, teledeteccion y modelado geoespacial para monitoreo ambiental.",
        },
        "fr": {
            "title": "Geospatial et Teledetection",
            "description": "SIG, teledetection et modelisation geospatiale pour la surveillance environnementale.",
        },
    },
    "env-management-law": {
        "pt-BR": {
            "title": "Impacto, Gestao e Risco",
            "description": "Avaliacao de impacto ambiental, sistemas de gestao e auditoria, risco e economia.",
        },
        "es": {
            "title": "Impacto, Gestion y Riesgo",
            "description": "Evaluacion de impacto ambiental, sistemas de gestion y auditoria, riesgo y economia.",
        },
        "fr": {
            "title": "Impact, Gestion et Risque",
            "description": "Evaluation des impacts environnementaux, systemes de gestion et audit, risque et economie.",
        },
    },
    "env-climate-sustainability": {
        "pt-BR": {
            "title": "Clima, Energia e Restauracao",
            "description": "Mudancas climaticas e carbono, processos sustentaveis, energia renovavel e restauracao ecologica.",
        },
        "es": {
            "title": "Clima, Energia y Restauracion",
            "description": "Cambio climatico y carbono, procesos sostenibles, energia renovable y restauracion ecologica.",
        },
        "fr": {
            "title": "Climat, Energie et Restauration",
            "description": "Changement climatique et carbone, procedes durables, energie renouvelable et restauration ecologique.",
        },
    },
    "env-ai-resilience": {
        "pt-BR": {
            "title": "IA, Dados e Resiliencia",
            "description": "IA e ciencia de dados para o meio ambiente, aprendizado profundo geoespacial e resiliencia a desastres.",
        },
        "es": {
            "title": "IA, Datos y Resiliencia",
            "description": "IA y ciencia de datos para el medio ambiente, aprendizaje profundo geoespacial y resiliencia ante desastres.",
        },
        "fr": {
            "title": "IA, Donnees et Resilience",
            "description": "IA et science des donnees pour l'environnement, apprentissage profond geospatial et resilience aux catastrophes.",
        },
    },
}

PATH_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "Engenharia Ambiental",
        "description": (
            "Um curriculo completo de engenharia ambiental, dos fundamentos cientificos, de quimica e "
            "biologia ao abastecimento e tratamento de agua, esgoto, residuos solidos, poluicao do ar, "
            "hidrogeologia e remediacao, monitoramento geoespacial, avaliacao de impacto e gestao, e "
            "clima e sustentabilidade - encerrando com IA, ciencia de dados e resiliencia a desastres."
        ),
    },
    "es": {
        "title": "Ingenieria Ambiental",
        "description": (
            "Un curriculo completo de ingenieria ambiental, desde los fundamentos cientificos, de quimica y "
            "biologia hasta el abastecimiento y tratamiento de agua, aguas residuales, residuos solidos, "
            "contaminacion del aire, hidrogeologia y remediacion, monitoreo geoespacial, evaluacion de "
            "impacto y gestion, y clima y sostenibilidad - cerrando con IA, ciencia de datos y resiliencia."
        ),
    },
    "fr": {
        "title": "Ingenierie de l'Environnement",
        "description": (
            "Un cursus complet d'ingenierie de l'environnement, des fondements scientifiques, chimiques et "
            "biologiques a l'alimentation et au traitement de l'eau, aux eaux usees, aux dechets solides, a "
            "la pollution de l'air, a l'hydrogeologie et a la remediation, a la surveillance geospatiale, a "
            "l'evaluation d'impact et a la gestion, et au climat et a la durabilite - en terminant par l'IA, "
            "la science des donnees et la resilience aux catastrophes."
        ),
    },
}


def build_payloads() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return (module payloads, path payload). Pure - unit-tested."""
    module_slugs = {m["slug"] for m in MODULES}
    missing = [s for s in PATH["moduleSlugs"] if s not in module_slugs]
    if missing:  # pragma: no cover - edit guard
        raise ValueError(f"path references modules not in MODULES: {missing}")
    return list(MODULES), dict(PATH)


def merged_module_slugs(existing: list[str], wanted: list[str]) -> list[str]:
    """Existing order preserved; any wanted slug not present is appended."""
    return existing + [s for s in wanted if s not in existing]


def _ctx() -> ssl.SSLContext | None:
    if os.environ.get("ACADEMY_INSECURE_TLS") == "1":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None


def _call(method: str, url: str, token: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, context=_ctx()) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def _token() -> str:
    token = os.environ.get("ACADEMY_TOKEN")
    if token:
        return token
    auth = os.environ.get("ACADEMY_AUTH_BASE", DEFAULT_AUTH_BASE)
    email, password = os.environ.get("ACADEMY_EMAIL"), os.environ.get("ACADEMY_PASSWORD")
    if not (email and password):
        raise SystemExit("set ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD")
    req = urllib.request.Request(
        f"{auth}/api/v1/auth/login",
        data=json.dumps({"email": email, "password": password}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=_ctx()) as r:
        return str(json.loads(r.read().decode())["access_token"])


def _upsert_translations(api: str, token: str, kind: str, slug: str, trs: dict[str, Any]) -> None:
    for language, tr in trs.items():
        st, _ = _call(
            "PUT",
            f"{api}/api/v1/admin/learning/{kind}/{slug}/translations/{language}",
            token,
            tr,
        )
        print(f"    {kind[:-1]} {slug} {language}: {'ok' if st == 200 else f'FAILED {st}'}")


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()
    modules, path = build_payloads()

    for module in modules:
        st, _ = _call("POST", f"{api}/api/v1/admin/learning/modules", token, module)
        verb = "created" if st in (200, 201) else ("exists" if st == 409 else f"FAILED {st}")
        print(f"  module {module['slug']}: {verb}")
        if module["slug"] in MODULE_TRANSLATIONS:
            _upsert_translations(
                api, token, "modules", module["slug"], MODULE_TRANSLATIONS[module["slug"]]
            )

    st, body = _call("POST", f"{api}/api/v1/admin/learning/paths", token, path)
    if st in (200, 201):
        print(f"  path {path['slug']}: created")
    elif st == 409:
        _, existing = _call("GET", f"{api}/api/v1/admin/learning/paths", token)
        current: list[str] = next(
            (p["moduleSlugs"] for p in existing if p["slug"] == path["slug"]), []
        )
        merged = merged_module_slugs(list(current), path["moduleSlugs"])
        if merged == current:
            print(f"  path {path['slug']}: exists (all modules already present)")
        else:
            st, body = _call(
                "PATCH",
                f"{api}/api/v1/admin/learning/paths/{path['slug']}",
                token,
                {"moduleSlugs": merged},
            )
            if st != 200:
                print(f"  path {path['slug']}: PATCH FAILED {st} {body}")
                return 1
            print(f"  path {path['slug']}: extended to {len(merged)} modules")
    else:
        print(f"  path {path['slug']}: FAILED {st} {body}")
        return 1
    _upsert_translations(api, token, "paths", path["slug"], PATH_TRANSLATIONS)

    print(f"Done - '{path['title']}' path is live and enrollable.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
