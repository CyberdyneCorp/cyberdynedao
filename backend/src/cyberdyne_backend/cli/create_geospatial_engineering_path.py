"""Create the "Geospatial Engineering" learning path + its modules via the
admin API (companion to ``create_computer_engineering_path``).

An operational, run-once helper, NOT app seed data. The courses are seeded
by the academy seed (reused math/CS/ML/remote-sensing courses plus the 18
new geospatial-specific courses); this curates them into 13 modules and a
path from scientific foundations through geodesy, GIS, remote sensing,
photogrammetry, satellites and GeoAI to full geospatial platforms.
Idempotent and extend-safe:
  * each module is POSTed (409 -> already exists, skipped);
  * the path is POSTed, OR - if it already exists - its ``moduleSlugs`` are
    PATCHed to include any new modules;
  * module + path translations (pt-BR/es/fr) are PUT (idempotent).

    python -m cyberdyne_backend.cli.create_geospatial_engineering_path

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
        "slug": "geo-foundations",
        "title": "Scientific Foundations",
        "category": "Geospatial Engineering",
        "level": "Beginner",
        "duration": "40 hr",
        "icon": "\U0001f4d0",
        "description": "The mathematics and physics every geospatial engineer builds on.",
        "topics": ["Calculus", "Linear algebra", "Vector calculus", "Physics"],
        "courseSlugs": [
            "math-basics",
            "math-intermediate",
            "math-matrices",
            "vectorcalc-basics",
            "physics-basics",
        ],
    },
    {
        "slug": "geo-computing",
        "title": "Computing and Programming",
        "category": "Geospatial Engineering",
        "level": "Beginner",
        "duration": "34 hr",
        "icon": "\U0001f4bb",
        "description": "Python, C++, algorithms, version control and SQL for geospatial software.",
        "topics": ["Python", "C++", "Algorithms", "SQL"],
        "courseSlugs": [
            "python-course",
            "cpp-basics",
            "algorithms-basics",
            "git-basics",
            "sql-basics",
        ],
    },
    {
        "slug": "geo-stats-numerical",
        "title": "Statistics and Numerical Methods",
        "category": "Geospatial Engineering",
        "level": "Intermediate",
        "duration": "26 hr",
        "icon": "\U0001f4ca",
        "description": "Probability, statistics, numerical methods and optimization for spatial data.",
        "topics": ["Probability", "Statistics", "Numerical methods", "Optimization"],
        "courseSlugs": [
            "math-probability",
            "prob-stats-python-basics",
            "math-numerical",
            "math-optimization",
        ],
    },
    {
        "slug": "geo-intro-cartography",
        "title": "Introduction and Cartography",
        "category": "Geospatial Engineering",
        "level": "Beginner",
        "duration": "14 hr",
        "icon": "\U0001f5fa",
        "description": "The discipline, and how the round Earth becomes a flat map.",
        "topics": ["Geospatial engineering", "Projections", "Coordinate systems"],
        "courseSlugs": ["intro-geospatial-engineering", "cartography-projections"],
    },
    {
        "slug": "geo-geodesy-survey",
        "title": "Geodesy, Surveying and Positioning",
        "category": "Geospatial Engineering",
        "level": "Intermediate",
        "duration": "30 hr",
        "icon": "\U0001f30d",
        "description": "Measuring the Earth and positioning on it - geodesy, surveying and GNSS.",
        "topics": ["Geodesy", "Surveying", "GNSS", "RTK and PPP"],
        "courseSlugs": ["geodesy", "surveying-geoprocessing", "gnss-navigation"],
    },
    {
        "slug": "geo-gis",
        "title": "GIS and Spatial Data",
        "category": "Geospatial Engineering",
        "level": "Intermediate",
        "duration": "26 hr",
        "icon": "\U0001f9ed",
        "description": "Geographic Information Systems, geoprocessing and spatial databases.",
        "topics": ["GIS", "Geoprocessing", "PostGIS", "Spatial SQL"],
        "courseSlugs": ["gis-fundamentals", "spatial-databases-postgis", "postgresql"],
    },
    {
        "slug": "geo-remote-sensing",
        "title": "Remote Sensing",
        "category": "Geospatial Engineering",
        "level": "Intermediate",
        "duration": "34 hr",
        "icon": "\U0001f6f0",
        "description": "Seeing the Earth from above - the physics, spectral analysis and radar of remote sensing.",
        "topics": ["Radiation physics", "Spectral indices", "Image analysis", "Radar"],
        "courseSlugs": [
            "remote-sensing-fundamentals",
            "remote-sensing-analysis",
            "image-processing-basics",
            "radar-basics",
        ],
    },
    {
        "slug": "geo-photogrammetry-lidar",
        "title": "Photogrammetry, LiDAR and SAR",
        "category": "Geospatial Engineering",
        "level": "Advanced",
        "duration": "26 hr",
        "icon": "\U0001f6e9",
        "description": "3D reconstruction from images, laser scanning and radar interferometry.",
        "topics": ["Photogrammetry", "Drone mapping", "LiDAR", "InSAR"],
        "courseSlugs": ["photogrammetry-drone-mapping", "lidar-point-clouds", "sar-insar"],
    },
    {
        "slug": "geo-satellite",
        "title": "Satellites and Earth Observation",
        "category": "Geospatial Engineering",
        "level": "Advanced",
        "duration": "18 hr",
        "icon": "\U0001f6f0",
        "description": "The space segment: observation missions, orbits and Earth-observation data catalogues.",
        "topics": ["Earth observation", "Orbits", "Constellations", "STAC"],
        "courseSlugs": ["satellite-earth-observation", "satellite-orbits-missions"],
    },
    {
        "slug": "geo-geoai",
        "title": "GeoAI and Machine Learning",
        "category": "Geospatial Engineering",
        "level": "Advanced",
        "duration": "34 hr",
        "icon": "\U0001f9e0",
        "description": "Deep learning for Earth observation - segmentation, detection and geospatial foundation models.",
        "topics": ["Deep learning", "Segmentation", "Change detection", "Foundation models"],
        "courseSlugs": [
            "geoai-deep-learning",
            "ml-basics",
            "ml-intermediate",
            "image-processing-intermediate",
        ],
    },
    {
        "slug": "geo-visualization-web",
        "title": "Web and 3D Visualization",
        "category": "Geospatial Engineering",
        "level": "Intermediate",
        "duration": "24 hr",
        "icon": "\U0001f5fa",
        "description": "Interactive web maps and 3D digital globes with Leaflet, MapLibre and Cesium.",
        "topics": ["Web GIS", "Vector tiles", "Cesium", "3D Tiles"],
        "courseSlugs": ["web-gis-development", "3d-geospatial-visualization", "webdev-basics"],
    },
    {
        "slug": "geo-platform-cloud",
        "title": "Geospatial Platforms and Cloud",
        "category": "Geospatial Engineering",
        "level": "Advanced",
        "duration": "36 hr",
        "icon": "☁️",
        "description": "Building scalable geospatial platforms - cloud-native data, distributed processing and containers.",
        "topics": ["Data engineering", "STAC and OGC APIs", "Distributed processing", "Kubernetes"],
        "courseSlugs": [
            "geospatial-data-engineering",
            "distributed-basics",
            "docker-basics",
            "kubernetes-basics",
            "gpu-programming-cuda-opencl",
        ],
    },
    {
        "slug": "geo-environmental",
        "title": "Environmental and Physical Modeling",
        "category": "Geospatial Engineering",
        "level": "Advanced",
        "duration": "22 hr",
        "icon": "\U0001f30a",
        "description": "Modeling Earth systems from geospatial data - terrain, hydrology, climate and hazards.",
        "topics": ["Terrain analysis", "Hydrology", "Climate", "Hazards"],
        "courseSlugs": [
            "environmental-geospatial-modeling",
            "hydrology-water-resources",
            "computational-fluid-dynamics-basics",
        ],
    },
)

PATH: dict[str, Any] = {
    "slug": "geospatial-engineering",
    "title": "Geospatial Engineering",
    "description": (
        "A full geospatial-engineering curriculum, from scientific and computing "
        "foundations through cartography, geodesy, GIS, remote sensing, photogrammetry, "
        "LiDAR, SAR and satellites, to GeoAI, 3D visualization and building scalable "
        "geospatial platforms - the skills to create systems like Google Earth, ArcGIS, "
        "Cesium and modern Earth-observation clouds."
    ),
    "moduleSlugs": [m["slug"] for m in MODULES],
    "estimatedTime": "56-68 weeks",
    "icon": "\U0001f30d",
}

MODULE_TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    "geo-foundations": {
        "pt-BR": {
            "title": "Fundamentos Cientificos",
            "description": "A matematica e a fisica que todo engenheiro geoespacial usa.",
        },
        "es": {
            "title": "Fundamentos Cientificos",
            "description": "Las matematicas y la fisica que todo ingeniero geoespacial usa.",
        },
        "fr": {
            "title": "Fondements Scientifiques",
            "description": "Les mathematiques et la physique de base de l'ingenieur geospatial.",
        },
    },
    "geo-computing": {
        "pt-BR": {
            "title": "Computacao e Programacao",
            "description": "Python, C++, algoritmos, controle de versao e SQL para software geoespacial.",
        },
        "es": {
            "title": "Computacion y Programacion",
            "description": "Python, C++, algoritmos, control de versiones y SQL para software geoespacial.",
        },
        "fr": {
            "title": "Informatique et Programmation",
            "description": "Python, C++, algorithmes, gestion de versions et SQL pour le logiciel geospatial.",
        },
    },
    "geo-stats-numerical": {
        "pt-BR": {
            "title": "Estatistica e Metodos Numericos",
            "description": "Probabilidade, estatistica, metodos numericos e otimizacao para dados espaciais.",
        },
        "es": {
            "title": "Estadistica y Metodos Numericos",
            "description": "Probabilidad, estadistica, metodos numericos y optimizacion para datos espaciales.",
        },
        "fr": {
            "title": "Statistiques et Methodes Numeriques",
            "description": "Probabilite, statistiques, methodes numeriques et optimisation pour les donnees spatiales.",
        },
    },
    "geo-intro-cartography": {
        "pt-BR": {
            "title": "Introducao e Cartografia",
            "description": "A disciplina e como a Terra redonda vira um mapa plano.",
        },
        "es": {
            "title": "Introduccion y Cartografia",
            "description": "La disciplina y como la Tierra redonda se convierte en un mapa plano.",
        },
        "fr": {
            "title": "Introduction et Cartographie",
            "description": "La discipline et comment la Terre ronde devient une carte plane.",
        },
    },
    "geo-geodesy-survey": {
        "pt-BR": {
            "title": "Geodesia, Topografia e Posicionamento",
            "description": "Medir a Terra e se posicionar nela - geodesia, topografia e GNSS.",
        },
        "es": {
            "title": "Geodesia, Topografia y Posicionamiento",
            "description": "Medir la Tierra y posicionarse en ella - geodesia, topografia y GNSS.",
        },
        "fr": {
            "title": "Geodesie, Topographie et Positionnement",
            "description": "Mesurer la Terre et s'y positionner - geodesie, topographie et GNSS.",
        },
    },
    "geo-gis": {
        "pt-BR": {
            "title": "SIG e Dados Espaciais",
            "description": "Sistemas de Informacao Geografica, geoprocessamento e bancos de dados espaciais.",
        },
        "es": {
            "title": "SIG y Datos Espaciales",
            "description": "Sistemas de Informacion Geografica, geoprocesamiento y bases de datos espaciales.",
        },
        "fr": {
            "title": "SIG et Donnees Spatiales",
            "description": "Systemes d'information geographique, geotraitement et bases de donnees spatiales.",
        },
    },
    "geo-remote-sensing": {
        "pt-BR": {
            "title": "Sensoriamento Remoto",
            "description": "Ver a Terra do alto - a fisica, a analise espectral e o radar do sensoriamento remoto.",
        },
        "es": {
            "title": "Teledeteccion",
            "description": "Ver la Tierra desde arriba - la fisica, el analisis espectral y el radar de la teledeteccion.",
        },
        "fr": {
            "title": "Teledetection",
            "description": "Voir la Terre d'en haut - la physique, l'analyse spectrale et le radar de la teledetection.",
        },
    },
    "geo-photogrammetry-lidar": {
        "pt-BR": {
            "title": "Fotogrametria, LiDAR e SAR",
            "description": "Reconstrucao 3D a partir de imagens, varredura a laser e interferometria de radar.",
        },
        "es": {
            "title": "Fotogrametria, LiDAR y SAR",
            "description": "Reconstruccion 3D a partir de imagenes, escaneo laser e interferometria de radar.",
        },
        "fr": {
            "title": "Photogrammetrie, LiDAR et SAR",
            "description": "Reconstruction 3D a partir d'images, balayage laser et interferometrie radar.",
        },
    },
    "geo-satellite": {
        "pt-BR": {
            "title": "Satelites e Observacao da Terra",
            "description": "O segmento espacial: missoes de observacao, orbitas e catalogos de dados.",
        },
        "es": {
            "title": "Satelites y Observacion de la Tierra",
            "description": "El segmento espacial: misiones de observacion, orbitas y catalogos de datos.",
        },
        "fr": {
            "title": "Satellites et Observation de la Terre",
            "description": "Le segment spatial : missions d'observation, orbites et catalogues de donnees.",
        },
    },
    "geo-geoai": {
        "pt-BR": {
            "title": "GeoIA e Aprendizado de Maquina",
            "description": "Aprendizado profundo para observacao da Terra - segmentacao, deteccao e modelos de fundacao.",
        },
        "es": {
            "title": "GeoIA y Aprendizaje Automatico",
            "description": "Aprendizaje profundo para observacion de la Tierra - segmentacion, deteccion y modelos fundacionales.",
        },
        "fr": {
            "title": "GeoIA et Apprentissage Automatique",
            "description": "Apprentissage profond pour l'observation de la Terre - segmentation, detection et modeles de fondation.",
        },
    },
    "geo-visualization-web": {
        "pt-BR": {
            "title": "Visualizacao Web e 3D",
            "description": "Mapas web interativos e globos digitais 3D com Leaflet, MapLibre e Cesium.",
        },
        "es": {
            "title": "Visualizacion Web y 3D",
            "description": "Mapas web interactivos y globos digitales 3D con Leaflet, MapLibre y Cesium.",
        },
        "fr": {
            "title": "Visualisation Web et 3D",
            "description": "Cartes web interactives et globes numeriques 3D avec Leaflet, MapLibre et Cesium.",
        },
    },
    "geo-platform-cloud": {
        "pt-BR": {
            "title": "Plataformas Geoespaciais e Nuvem",
            "description": "Construir plataformas geoespaciais escalaveis - dados nativos de nuvem, processamento distribuido e conteineres.",
        },
        "es": {
            "title": "Plataformas Geoespaciales y Nube",
            "description": "Construir plataformas geoespaciales escalables - datos nativos de nube, procesamiento distribuido y contenedores.",
        },
        "fr": {
            "title": "Plateformes Geospatiales et Cloud",
            "description": "Construire des plateformes geospatiales evolutives - donnees cloud-natives, traitement distribue et conteneurs.",
        },
    },
    "geo-environmental": {
        "pt-BR": {
            "title": "Modelagem Ambiental e Fisica",
            "description": "Modelar sistemas terrestres a partir de dados geoespaciais - terreno, hidrologia, clima e riscos.",
        },
        "es": {
            "title": "Modelado Ambiental y Fisico",
            "description": "Modelar sistemas terrestres a partir de datos geoespaciales - terreno, hidrologia, clima y riesgos.",
        },
        "fr": {
            "title": "Modelisation Environnementale et Physique",
            "description": "Modeliser les systemes terrestres a partir de donnees geospatiales - terrain, hydrologie, climat et risques.",
        },
    },
}

PATH_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "Engenharia Geoespacial",
        "description": (
            "Um curriculo completo de engenharia geoespacial, dos fundamentos cientificos e de "
            "computacao a cartografia, geodesia, SIG, sensoriamento remoto, fotogrametria, LiDAR, "
            "SAR e satelites, ate GeoIA, visualizacao 3D e a construcao de plataformas geoespaciais "
            "escalaveis - as habilidades para criar sistemas como Google Earth, ArcGIS, Cesium e as "
            "nuvens modernas de observacao da Terra."
        ),
    },
    "es": {
        "title": "Ingenieria Geoespacial",
        "description": (
            "Un curriculo completo de ingenieria geoespacial, desde los fundamentos cientificos y de "
            "computacion hasta la cartografia, geodesia, SIG, teledeteccion, fotogrametria, LiDAR, SAR y "
            "satelites, hasta GeoIA, visualizacion 3D y la construccion de plataformas geoespaciales "
            "escalables - las habilidades para crear sistemas como Google Earth, ArcGIS, Cesium y las "
            "nubes modernas de observacion de la Tierra."
        ),
    },
    "fr": {
        "title": "Ingenierie Geospatiale",
        "description": (
            "Un cursus complet d'ingenierie geospatiale, des fondements scientifiques et informatiques a la "
            "cartographie, la geodesie, les SIG, la teledetection, la photogrammetrie, le LiDAR, le SAR et "
            "les satellites, jusqu'a la GeoIA, la visualisation 3D et la construction de plateformes "
            "geospatiales evolutives - les competences pour creer des systemes comme Google Earth, ArcGIS, "
            "Cesium et les clouds modernes d'observation de la Terre."
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
