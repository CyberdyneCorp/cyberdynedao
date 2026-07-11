"""Academy seed content - Digital Twins, AI and Computer Vision in Construction.

How data and AI are reshaping civil engineering: moving from static BIM
models to living digital twins fed by IoT sensors, building the data
pipelines that carry field data, using machine learning to predict cost,
demand and deterioration, applying computer vision to progress and defect
detection, exploring generative design and predictive maintenance, and
closing with the responsibility that using AI on safety-critical
infrastructure demands. Every lesson is a direct explanation with a
concrete example - an ML or computer-vision snippet, a data pipeline, or
a formula - and a mermaid diagram, followed by a checkpoint quiz; the
course closes with a comprehensive final quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_DIGITAL_TWINS_AI_CONSTRUCTION = SeedCourse(
    slug="digital-twins-ai-construction",
    title="Digital Twins, AI and Computer Vision in Construction",
    description=(
        "A modern tour of how AI is reshaping civil engineering: digital "
        "twins that mirror real assets, IoT structural health monitoring, "
        "data pipelines for infrastructure, machine learning for cost, "
        "demand and deterioration prediction, computer vision on site, "
        "generative design and predictive maintenance - and the "
        "responsibility of using AI on safety-critical work. Every lesson "
        "has a concrete example and a diagram."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Digital Twins, AI and Computer Vision in Construction

Civil engineering is being reshaped by data. The drawings and BIM models
that describe a bridge or a building are becoming **living digital
twins** - kept in sync with the real asset by sensors, updated as it
ages, and paired with machine learning that predicts what will happen
next. This course is the modern, practical map of that shift.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a short real example (a machine-learning snippet, a
computer-vision routine, a data pipeline, or a formula), and draws the
idea as a diagram. After each lesson there is a short quiz; at the end, a
final quiz covers the whole course.

What you will build understanding for, in order:

1. **From BIM to digital twins** - a model that mirrors a real asset
2. **IoT sensors and structural health monitoring** - the nervous system
3. **Data pipelines and platforms** - moving field data to where it is used
4. **Machine learning for prediction** - cost, demand, deterioration
5. **Computer vision on site** - progress tracking and defect detection
6. **Generative design and structural optimization** - the computer proposes
7. **Predictive maintenance and asset management** - fix before it fails
8. **Responsible AI in engineering** - verification, hallucinations, accountability

This is a tools-and-judgement course. AI does not replace the engineer's
responsibility - it gives the engineer better information, faster. Where
we mention standards (ABNT NBR, ACI, Eurocode, AASHTO, ISO 19650, ISO
23247) it is to ground the ideas in real practice, not to memorize codes.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the central shift this course is about?",
                    (
                        opt("Replacing engineers with automated software"),
                        opt(
                            "Moving from static drawings and models toward data-driven, "
                            "living digital twins paired with machine learning",
                            correct=True,
                        ),
                        opt("Abandoning BIM in favour of hand calculations"),
                        opt("Using AI only for marketing renders"),
                    ),
                    "The theme is data and AI augmenting civil engineering - not "
                    "removing the engineer's responsibility.",
                ),
                q(
                    "How is each content lesson structured?",
                    (
                        opt("A long theoretical essay with no examples"),
                        opt(
                            "A direct explanation, a concrete example (code, pipeline or "
                            "formula), a diagram, and a checkpoint quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A video with no text"),
                    ),
                    "Explain, show a concrete example, diagram it, then quiz - the same "
                    "shape every lesson.",
                ),
            ),
        ),
        # -- 1. From BIM to digital twins ------------------------------
        _t(
            "From BIM to digital twins",
            "10 min",
            """# From BIM to digital twins

**BIM (Building Information Modeling)** is a rich 3D model where every
element - a beam, a wall, a valve - carries data: material, dimensions,
cost, install date. It is the coordinated source of truth for *design and
construction*, exchanged through the open **IFC** format and governed by
**ISO 19650**.

A **digital twin** goes one step further. It is a BIM (or other) model
**connected to the real asset by a live data feed**, so the model
reflects the asset's actual current state, not just its designed state.
The formal definition (ISO 23247) has three parts you should keep
straight:

- **Physical asset** - the real bridge, building, or plant.
- **Virtual model** - the digital representation of it.
- **The connection** - a two-way data link. Sensor data flows *up* into
  the model; analysis and control can flow *down* to the asset.

The connection is what separates a twin from a plain 3D model. A common
way to describe maturity is a **ladder**:

- **Descriptive** - the twin shows what the asset *is* now (geometry plus
  live readings).
- **Diagnostic** - it helps explain *why* something is happening.
- **Predictive** - it forecasts what *will* happen (later lessons).
- **Prescriptive** - it recommends what to *do*.

```mermaid
graph LR
    BIM["BIM model IFC and ISO 19650"] --> TWIN["Digital twin"]
    PHYS["Physical asset"] -->|"sensor data up"| TWIN
    TWIN -->|"control and insight down"| PHYS
    TWIN --> DESC["Descriptive state now"]
    DESC --> DIAG["Diagnostic why"]
    DIAG --> PRED["Predictive what next"]
    PRED --> PRESC["Prescriptive what to do"]
```

A minimal state-sync record - the kind of message that keeps a twin in
step with its asset - looks like this:

```python
# One reading updating an element in the twin
reading = {
    "element_id": "BRG-PIER-03",     # matches the IFC GUID in the model
    "metric": "tilt_deg",
    "value": 0.42,
    "timestamp": "2026-07-11T09:15:00Z",
    "sensor_id": "INCL-114",
}
# The twin stores this against the element and flags if it drifts
# past a design threshold (here 0.5 deg of pier tilt).
alert = reading["value"] > 0.5
```

Remember: BIM describes the *designed* asset; a digital twin stays
synchronized with the *real* one through a live connection - and that
connection is the whole point.
""",
        ),
        quiz_lesson(
            "Quiz: From BIM to digital twins",
            (
                q(
                    "What distinguishes a digital twin from a plain BIM model?",
                    (
                        opt("The twin has more colours in the render"),
                        opt(
                            "A live two-way data connection keeps the twin synchronized "
                            "with the real asset's current state",
                            correct=True,
                        ),
                        opt("The twin is drawn in 2D instead of 3D"),
                        opt("Nothing - the terms are identical"),
                    ),
                    "BIM is the designed model; the twin adds the live connection to the "
                    "physical asset (ISO 23247).",
                ),
                q(
                    "Which open format is used to exchange BIM data between tools?",
                    (
                        opt("PDF"),
                        opt("IFC", correct=True),
                        opt("JPEG"),
                        opt("CSV only"),
                    ),
                    "IFC is the open BIM exchange format; ISO 19650 governs the "
                    "information management process.",
                ),
                q(
                    "On the digital-twin maturity ladder, what does the 'predictive' "
                    "level add over 'descriptive'?",
                    (
                        opt("It shows the asset's geometry in higher resolution"),
                        opt(
                            "It forecasts what will happen next, rather than only showing "
                            "the current state",
                            correct=True,
                        ),
                        opt("It removes all sensors"),
                        opt("It converts the model back to paper drawings"),
                    ),
                    "Descriptive = what is; diagnostic = why; predictive = what next; "
                    "prescriptive = what to do.",
                ),
            ),
        ),
        # -- 2. IoT sensors and SHM ------------------------------------
        _t(
            "IoT sensors and structural health monitoring",
            "11 min",
            """# IoT sensors and structural health monitoring

If a digital twin is the brain, **IoT sensors** are the nervous system.
**Structural Health Monitoring (SHM)** instruments a real structure so
its behaviour can be observed continuously, instead of relying only on
periodic manual inspection.

Common sensor types in civil SHM:

- **Strain gauges** - measure local strain in a member; convert to stress
  through the material modulus.
- **Accelerometers** - capture vibration; the structure's **natural
  frequencies** shift when stiffness changes (damage, loosening).
- **Inclinometers and tiltmeters** - measure rotation of piers, walls,
  slopes.
- **Displacement and crack sensors (LVDTs, crackmeters)** - track movement
  and crack width over time.
- **Temperature and corrosion sensors** - environment and reinforcement
  condition, both major drivers of deterioration.

Sensors are typically low-power devices reporting over a wireless network
(LoRaWAN, NB-IoT) to a gateway, which forwards to the platform. The
**edge** near the sensor often does first-pass filtering and threshold
checks so the network is not flooded with raw data.

```mermaid
graph LR
    S1["Strain gauge"] --> GW["Edge gateway"]
    S2["Accelerometer"] --> GW
    S3["Inclinometer"] --> GW
    GW -->|"filtered readings"| PLAT["Monitoring platform"]
    PLAT --> TWIN["Digital twin"]
    PLAT --> ALERT["Threshold alert"]
```

A worked strain-to-stress conversion - the everyday calculation behind a
gauge reading, using Hooke's law in the elastic range:

```text
Hooke's law:  sigma = E * epsilon

Given:
  epsilon = 150 microstrain = 150e-6   (strain gauge reading)
  E       = 200 GPa = 200e9 Pa         (structural steel)

sigma = 200e9 * 150e-6 = 30e6 Pa = 30 MPa

Compare against the allowable stress for the member. A steadily
rising epsilon under the same load points to a stiffness problem.
```

A key SHM idea is the **baseline**: you record how the healthy structure
behaves (its natural frequencies, its strain under known loads), then
watch for **deviation** from that baseline. Damage rarely announces
itself as a single dramatic reading - it shows up as a slow drift or a
frequency shift against the baseline.

Remember: SHM turns "inspect every two years and hope" into "observe
continuously and act on deviation from a known-good baseline."
""",
        ),
        quiz_lesson(
            "Quiz: IoT sensors and structural health monitoring",
            (
                q(
                    "Which quantity does a strain gauge measure, and how is it turned into stress?",
                    (
                        opt("It measures temperature; multiply by mass"),
                        opt(
                            "It measures strain; multiply by the elastic modulus E "
                            "(sigma = E times epsilon) in the elastic range",
                            correct=True,
                        ),
                        opt("It measures colour; divide by area"),
                        opt("It measures wind speed directly"),
                    ),
                    "Hooke's law sigma = E * epsilon converts a gauge's strain reading "
                    "to stress in the elastic range.",
                ),
                q(
                    "Why do accelerometers help detect structural damage?",
                    (
                        opt("They photograph cracks"),
                        opt(
                            "A loss of stiffness shifts the structure's natural "
                            "frequencies, which vibration data reveals",
                            correct=True,
                        ),
                        opt("They measure the price of steel"),
                        opt("They only work after collapse"),
                    ),
                    "Damage lowers stiffness, which changes natural frequencies - a "
                    "core SHM signal.",
                ),
                q(
                    "What is the role of a 'baseline' in structural health monitoring?",
                    (
                        opt("It is the concrete foundation of the sensor"),
                        opt(
                            "A record of the healthy structure's behaviour, against which "
                            "later readings are compared for deviation",
                            correct=True,
                        ),
                        opt("It is the lowest sensor on the structure"),
                        opt("It is the wireless network name"),
                    ),
                    "Damage usually shows as drift from a known-good baseline, not a "
                    "single dramatic value.",
                ),
            ),
        ),
        # -- 3. Data pipelines and platforms ---------------------------
        _t(
            "Data pipelines and platforms for infrastructure",
            "11 min",
            """# Data pipelines and platforms for infrastructure

Sensors produce a flood of readings; models and dashboards need them
clean, joined, and reliable. Between the two sits a **data pipeline** -
the plumbing that ingests, stores, transforms, and serves infrastructure
data. Without it, a digital twin is just a pretty model with no fuel.

A typical pipeline has clear stages:

- **Ingest** - collect from sensors, drones, inspection apps, and BIM. A
  message broker or streaming layer (MQTT, Kafka) buffers high-rate feeds.
- **Store** - a **time-series database** for sensor streams (readings
  indexed by time), object storage for images and point clouds, and a
  metadata store linking data to the BIM element GUIDs.
- **Transform** - clean, validate, resample, and join. Raw sensor data is
  noisy: drop out-of-range values, align timestamps, fill small gaps.
- **Serve** - feed dashboards, the digital twin, and ML models.

```mermaid
graph LR
    SRC["Sensors drones inspections BIM"] --> ING["Ingest stream buffer"]
    ING --> STORE["Time series and object store"]
    STORE --> XFORM["Clean validate resample join"]
    XFORM --> SERVE["Serve twin dashboards models"]
    SERVE --> ML["ML predictions"]
    ML --> STORE
```

A tiny but realistic transform step - resampling noisy per-second strain
data to clean per-minute averages and dropping impossible spikes:

```python
import pandas as pd

# raw: irregular, noisy strain readings with a bad spike
df = pd.read_parquet("strain_BRG_PIER_03.parquet")   # columns: ts, microstrain

df["ts"] = pd.to_datetime(df["ts"])
df = df.set_index("ts").sort_index()

# 1) drop physically impossible readings (sensor glitch)
df = df[df["microstrain"].between(-2000, 2000)]

# 2) resample to 1-minute means so downstream models see clean signal
clean = df["microstrain"].resample("1min").mean().interpolate(limit=3)

clean.to_parquet("strain_BRG_PIER_03_clean.parquet")
```

Two principles keep infrastructure data trustworthy:

- **Data quality is a first-class job.** Validate on ingest; a model
  trained on garbage predicts garbage ("garbage in, garbage out").
- **Lineage and provenance.** Record where each value came from and how it
  was transformed, so a decision affecting public safety can be traced
  back to raw evidence and an audit can reproduce it.

Remember: the pipeline is unglamorous but decisive - reliable, traceable
data is what makes every later AI step believable.
""",
        ),
        quiz_lesson(
            "Quiz: Data pipelines and platforms for infrastructure",
            (
                q(
                    "Which storage type is best suited to high-rate sensor readings "
                    "indexed by time?",
                    (
                        opt("A plain spreadsheet"),
                        opt("A time-series database", correct=True),
                        opt("A PDF archive"),
                        opt("The BIM render cache"),
                    ),
                    "Sensor streams are time-indexed; a time-series database is built "
                    "for exactly that access pattern.",
                ),
                q(
                    "Why is the 'transform' stage (cleaning, validating, resampling) "
                    "important before feeding ML models?",
                    (
                        opt("It makes the dashboard colours brighter"),
                        opt(
                            "Raw sensor data is noisy and gappy; models trained on "
                            "unclean data give unreliable predictions (garbage in, "
                            "garbage out)",
                            correct=True,
                        ),
                        opt("It deletes all the data to save space"),
                        opt("It is only needed for images, never sensors"),
                    ),
                    "Clean, validated, aligned data is the precondition for trustworthy "
                    "predictions.",
                ),
                q(
                    "Why does infrastructure data need lineage and provenance?",
                    (
                        opt("To make the files larger"),
                        opt(
                            "So a safety-relevant decision can be traced back to raw "
                            "evidence and independently reproduced or audited",
                            correct=True,
                        ),
                        opt("Because regulators dislike time-series databases"),
                        opt("It has no real purpose"),
                    ),
                    "On safety-critical assets, being able to trace a value from "
                    "decision back to raw sensor is essential.",
                ),
            ),
        ),
        # -- 4. Machine learning for prediction ------------------------
        _t(
            "Machine learning for prediction",
            "12 min",
            """# Machine learning for prediction

With clean data flowing, **machine learning (ML)** lets us predict
outcomes from patterns in history instead of from a fixed formula alone.
Three prediction problems dominate civil practice:

- **Cost and duration** - estimate a project's final cost or schedule from
  features of similar past projects (type, span, location, soil, complexity).
- **Demand** - forecast traffic on a road, ridership on a line, or water
  demand for a network, to size and operate infrastructure.
- **Deterioration** - predict how a pavement, deck, or pipe condition will
  decline over time, to plan intervention.

Most of these are **supervised learning**: you have historical examples
with known answers (**labels**), the model learns the mapping from
**features** to label, and you then predict on new cases. The iron rule
is to **evaluate on data the model never saw** (a held-out test set), or
you will fool yourself.

```mermaid
graph LR
    HIST["Historical labelled projects"] --> FEAT["Feature engineering"]
    FEAT --> SPLIT["Train and test split"]
    SPLIT --> TRAIN["Train model"]
    TRAIN --> EVAL["Evaluate on unseen test set"]
    EVAL --> PRED["Predict new project"]
    EVAL -->|"poor score"| FEAT
```

A compact, realistic cost-prediction example with scikit-learn:

```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# X: features per past project (area_m2, floors, soil_class, region_index...)
# y: final cost in currency units
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = GradientBoostingRegressor()
model.fit(X_train, y_train)

pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)   # average error in currency units
print("Mean absolute error:", mae)
```

Two cautions that matter more in engineering than in most fields:

- **Correlation is not a load path.** An ML model finds patterns; it does
  not understand physics. Use it to *estimate and prioritize*, then check
  against engineering judgement and code requirements.
- **Distribution shift.** A model trained on past projects can be wrong on
  a genuinely novel design, material, or climate. Track its error over
  time and retrain; do not trust it blindly outside its training range.

Remember: ML predicts from patterns in history - powerful for cost,
demand and deterioration - but it estimates, it does not certify. The
engineer still owns the decision.
""",
        ),
        quiz_lesson(
            "Quiz: Machine learning for prediction",
            (
                q(
                    "In supervised learning, what are 'labels'?",
                    (
                        opt("The names printed on the sensors"),
                        opt(
                            "The known correct answers in historical data that the model "
                            "learns to predict from the features",
                            correct=True,
                        ),
                        opt("The colours used in the chart"),
                        opt("The file names of the datasets"),
                    ),
                    "Supervised learning maps features to known labels, then predicts "
                    "labels for new cases.",
                ),
                q(
                    "Why must a model be evaluated on a held-out test set it never saw?",
                    (
                        opt("To make training run faster"),
                        opt(
                            "Otherwise you measure memorization, not real predictive "
                            "performance, and fool yourself about accuracy",
                            correct=True,
                        ),
                        opt("Because scikit-learn refuses to run otherwise"),
                        opt("Test sets are only for images"),
                    ),
                    "Scoring on unseen data is the only honest measure of how the model "
                    "will perform on new projects.",
                ),
                q(
                    "What is 'distribution shift', and why does it matter in engineering?",
                    (
                        opt("The model file moving to another server"),
                        opt(
                            "New cases differ from the training data (novel design, "
                            "material, climate), so the model may be wrong outside its "
                            "training range",
                            correct=True,
                        ),
                        opt("A change in the chart's colour palette"),
                        opt("Splitting data into train and test"),
                    ),
                    "ML learns patterns from history; on genuinely novel conditions it "
                    "can fail, so monitor error and retrain.",
                ),
            ),
        ),
        # -- 5. Computer vision on site --------------------------------
        _t(
            "Computer vision for progress tracking and defect detection",
            "12 min",
            """# Computer vision for progress tracking and defect detection

**Computer vision (CV)** lets software interpret images and video - from
site cameras, phones, and drones - automatically. Two high-value uses on
construction and infrastructure:

- **Progress tracking** - compare what is built against the schedule and
  BIM. Drone photogrammetry produces a **point cloud** of the site; a
  **scan-vs-BIM** comparison shows which elements are in place, so
  progress and earned value are measured from reality, not a status
  meeting.
- **Defect and safety detection** - detect cracks, spalling, corrosion,
  and rebar exposure on structures, or missing hard hats and unsafe zones
  on site. A trained model flags candidates for an engineer to confirm.

The workhorse is a **convolutional neural network (CNN)**. Two task types
matter:

- **Classification** - "is there a crack in this image?" (yes or no).
- **Object detection or segmentation** - "where is the crack, outlined?" -
  which lets you measure it.

```mermaid
graph LR
    CAM["Site cameras drones phones"] --> IMG["Images and point clouds"]
    IMG --> CV["CV model CNN"]
    CV --> PROG["Scan vs BIM progress"]
    CV --> DEF["Crack and defect detection"]
    CV --> SAFE["PPE and safety checks"]
    DEF --> ENG["Engineer confirms and measures"]
```

A concrete crack-detection inference step, using a pretrained detector:

```python
import cv2
from ultralytics import YOLO

model = YOLO("crack_detector.pt")     # a model fine-tuned on labelled cracks
img = cv2.imread("deck_span_7.jpg")

results = model(img)[0]
for box in results.boxes:
    conf = float(box.conf)            # detector confidence 0..1
    if conf > 0.5:                    # keep confident detections
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imwrite("deck_span_7_flagged.jpg", img)   # for engineer review
```

Two realities of CV in the field:

- **It flags, humans decide.** A confidence score is not a diagnosis. The
  model triages thousands of images down to the few an engineer must look
  at; it does not sign off on structural condition.
- **Data and conditions matter.** Lighting, dust, rust stains and shadows
  fool models trained on clean images. Represent real site conditions in
  the training data, and measure false negatives (missed defects) - the
  costly error - carefully.

Remember: computer vision multiplies an inspector's reach - measuring
progress from reality and surfacing defects across huge image sets - but
the engineer confirms and measures what it flags.
""",
        ),
        quiz_lesson(
            "Quiz: Computer vision for progress tracking and defect detection",
            (
                q(
                    "How does computer vision measure construction progress objectively?",
                    (
                        opt("By asking the foreman for a percentage"),
                        opt(
                            "By comparing a point cloud or images of the real site "
                            "against the BIM model (scan-vs-BIM) to see which elements "
                            "are in place",
                            correct=True,
                        ),
                        opt("By counting the number of workers on site"),
                        opt("By reading the project's PDF schedule"),
                    ),
                    "Scan-vs-BIM measures progress from reality captured by drones or "
                    "cameras, not from a status meeting.",
                ),
                q(
                    "What kind of neural network is the workhorse for interpreting site images?",
                    (
                        opt("A spreadsheet macro"),
                        opt("A convolutional neural network (CNN)", correct=True),
                        opt("A time-series database"),
                        opt("A message broker"),
                    ),
                    "CNNs are the standard architecture for image classification, "
                    "detection and segmentation.",
                ),
                q(
                    "In defect detection, why is a missed defect (false negative) "
                    "treated as the costly error, and how is CV used responsibly?",
                    (
                        opt("It is not costly; any error is fine"),
                        opt(
                            "A missed defect can compromise safety, so CV is used to "
                            "flag candidates for an engineer to confirm and measure, not "
                            "to sign off condition automatically",
                            correct=True,
                        ),
                        opt("False negatives make the images blurry"),
                        opt("The model should replace inspection entirely"),
                    ),
                    "CV triages and flags; the engineer confirms. Missing a real defect "
                    "is the dangerous error to minimize.",
                ),
            ),
        ),
        # -- 6. Generative design --------------------------------------
        _t(
            "Generative design and structural optimization",
            "11 min",
            """# Generative design and structural optimization

In traditional design the engineer proposes a form and then analyzes it.
**Generative design** flips this: you state the **goals and
constraints**, and the computer generates and evaluates many candidate
designs, searching for ones that satisfy the rules while optimizing an
objective.

The ingredients:

- **Objective** - what to minimize or maximize (material mass, cost,
  embodied carbon, deflection).
- **Constraints** - what must hold (stress below allowable, deflection
  limits, clearances, buildability, code requirements from Eurocode / ACI
  / NBR).
- **Variables** - what the algorithm may change (member sizes, geometry,
  topology, layout).
- **Search** - an optimization method (gradient-based, genetic algorithms)
  or **topology optimization**, which removes material from lightly
  stressed regions to find an efficient load path.

```mermaid
graph LR
    GOAL["Objectives and constraints"] --> GEN["Generate candidate designs"]
    GEN --> SIM["Simulate FEA stress and deflection"]
    SIM --> SCORE["Score against objective"]
    SCORE --> SEL["Select and vary best"]
    SEL --> GEN
    SCORE --> OUT["Optimized design set"]
    OUT --> ENG["Engineer chooses and verifies"]
```

A minimal optimization statement makes the idea concrete - sizing a
member to minimize mass while respecting a stress limit:

```text
minimize    mass(A) = rho * L * A
subject to  sigma(A) = P / A  <=  sigma_allow
            A >= A_min

Given P = 500 kN, sigma_allow = 165 MPa:
  A_required = P / sigma_allow
             = 500e3 N / 165e6 Pa
             = 3.03e-3 m^2  = 3030 mm^2

The optimizer drives A toward this active constraint - the smallest
section that still passes - instead of an over-conservative guess.
```

Two things to hold onto:

- **The computer proposes; the engineer disposes.** Generative design
  explores far more options than a human could, but a candidate is only a
  proposal. It must be verified against the full code, constructability,
  and context before it is real.
- **Garbage constraints, garbage designs.** The optimizer will happily
  exploit a missing constraint (an unbuildable shape, an ignored load
  case). Getting the constraints and load cases right is the engineering.

Remember: generative design turns the engineer into the author of the
*problem* - objectives and constraints - and lets the machine search the
solution space, which the engineer then verifies.
""",
        ),
        quiz_lesson(
            "Quiz: Generative design and structural optimization",
            (
                q(
                    "How does generative design differ from traditional design?",
                    (
                        opt("It skips analysis entirely"),
                        opt(
                            "The engineer states objectives and constraints, and the "
                            "computer generates and evaluates many candidate designs",
                            correct=True,
                        ),
                        opt("It only changes the render colours"),
                        opt("It removes the need for any constraints"),
                    ),
                    "You author the problem (objectives + constraints); the machine "
                    "searches the solution space.",
                ),
                q(
                    "What does topology optimization do?",
                    (
                        opt("Renames the model elements"),
                        opt(
                            "Removes material from lightly stressed regions to find an "
                            "efficient load path for the objective",
                            correct=True,
                        ),
                        opt("Adds material everywhere to be safe"),
                        opt("Converts the model to 2D"),
                    ),
                    "Topology optimization sculpts material toward where the load "
                    "actually flows, cutting mass.",
                ),
                q(
                    "Why is getting the constraints and load cases right the essential "
                    "engineering task in generative design?",
                    (
                        opt("Because the optimizer needs pretty inputs"),
                        opt(
                            "The optimizer will exploit any missing constraint, producing "
                            "an unbuildable or unsafe design that still scores well",
                            correct=True,
                        ),
                        opt("Constraints only affect the render speed"),
                        opt("Load cases are irrelevant to optimization"),
                    ),
                    "A missing constraint or load case yields a 'valid' but wrong "
                    "design - the engineer owns the problem statement.",
                ),
            ),
        ),
        # -- 7. Predictive maintenance ---------------------------------
        _t(
            "Predictive maintenance and asset management",
            "11 min",
            """# Predictive maintenance and asset management

Infrastructure is expensive to maintain and dangerous to neglect. The
question is *when* to intervene. Three strategies, in increasing
sophistication:

- **Reactive** - fix it after it fails. Cheapest to plan, most expensive
  and dangerous when the asset is a bridge or a water main.
- **Preventive** - maintain on a fixed schedule (every N years). Safer,
  but wasteful: you service healthy assets and can still miss early failures.
- **Predictive** - use condition data and models to intervene **just
  before** a problem, on the evidence of the specific asset.

Predictive maintenance leans on the digital twin, SHM data, and ML
deterioration models from earlier lessons. A widely used framing is
**remaining useful life (RUL)**: from the current condition and its trend,
estimate how much service life is left, and schedule work inside that
window.

```mermaid
graph LR
    SHM["SHM and inspection data"] --> COND["Condition assessment"]
    COND --> TREND["Deterioration trend model"]
    TREND --> RUL["Remaining useful life estimate"]
    RUL --> PLAN["Schedule intervention in window"]
    PLAN --> PRIOR["Prioritize across the portfolio"]
    PRIOR --> WORK["Maintenance work order"]
```

At **portfolio** scale (a network of bridges, a pipe grid), you cannot
fix everything at once, so you rank. A simple, transparent **risk score**
drives prioritization:

```text
Risk = Probability_of_failure  x  Consequence_of_failure

Bridge A: P = 0.30 (poor deck, rising crack trend),  C = 9 (major route)
          Risk_A = 0.30 * 9 = 2.7
Bridge B: P = 0.60 (corrosion),  C = 3 (low-traffic rural)
          Risk_B = 0.60 * 3 = 1.8

Bridge A ranks above B despite a lower failure probability, because
its consequence is far higher. Spend the maintenance budget by risk,
not by age alone.
```

Two points to remember:

- **Condition-based beats calendar-based.** Acting on the evidence of a
  specific asset avoids both premature work and dangerous surprises.
- **Risk, not just probability.** For public infrastructure, consequence
  matters as much as likelihood - a low-probability failure on a critical
  crossing can outrank a likely failure on a minor one.

Remember: predictive maintenance uses condition data and models to fix
things *just in time*, and risk-based prioritization spends limited
budget where it protects the most.
""",
        ),
        quiz_lesson(
            "Quiz: Predictive maintenance and asset management",
            (
                q(
                    "How does predictive maintenance differ from preventive "
                    "(scheduled) maintenance?",
                    (
                        opt("It waits until the asset fails, then repairs"),
                        opt(
                            "It uses condition data and models to intervene just before "
                            "a problem on the specific asset, rather than on a fixed "
                            "calendar",
                            correct=True,
                        ),
                        opt("It never performs any maintenance"),
                        opt("It only repaints the structure"),
                    ),
                    "Preventive = fixed schedule; predictive = act on the evidence of "
                    "the specific asset's condition and trend.",
                ),
                q(
                    "What does 'remaining useful life (RUL)' estimate?",
                    (
                        opt("The cost of the original construction"),
                        opt(
                            "How much service life is left, from current condition and "
                            "its deterioration trend, so work can be scheduled in that "
                            "window",
                            correct=True,
                        ),
                        opt("The number of sensors installed"),
                        opt("The colour of the asset"),
                    ),
                    "RUL turns condition and trend into a time window for intervention.",
                ),
                q(
                    "In risk-based prioritization, why can a bridge with a lower failure "
                    "probability rank above one with a higher probability?",
                    (
                        opt("Because older bridges always rank first"),
                        opt(
                            "Risk multiplies probability by consequence, so a high "
                            "consequence (a critical route) can outweigh a lower "
                            "probability",
                            correct=True,
                        ),
                        opt("Because it has more sensors"),
                        opt("Probability is the only thing that matters"),
                    ),
                    "Risk = probability x consequence; for public assets, consequence "
                    "weighs heavily.",
                ),
            ),
        ),
        # -- 8. Responsible AI -----------------------------------------
        _t(
            "Responsible AI in engineering",
            "11 min",
            """# Responsible AI in engineering

Everything in this course puts AI close to decisions that affect public
safety. That raises the stakes: a wrong prediction here is not a bad movie
recommendation, it can be a collapsed structure. Using AI responsibly in
engineering is itself an engineering discipline.

The core risks to manage:

- **Hallucination and overconfidence.** Generative and large-language
  models can produce fluent, confident output that is simply wrong - an
  invented code clause, a mis-stated formula. A confident answer is not a
  correct one.
- **Automation bias.** People tend to trust a computer's output and stop
  checking. The more capable the tool, the stronger the pull - and the
  more important deliberate verification becomes.
- **Opacity.** Many models are hard to interrogate ("black box"). For a
  safety decision you need to be able to explain *why*.
- **Bias and distribution shift.** A model reflects its training data and
  may be wrong on novel or under-represented cases.

The response is a **human-in-the-loop** discipline: AI assists, a
qualified engineer verifies and remains **accountable**.

```mermaid
graph LR
    AI["AI output prediction or design"] --> VERIFY["Engineer verifies"]
    VERIFY --> CHECK["Check against physics and code"]
    CHECK --> TRACE["Trace data and assumptions"]
    TRACE --> DECIDE["Engineer decides and signs"]
    DECIDE --> ACCOUNT["Named accountability"]
    VERIFY -->|"cannot verify"| REJECT["Reject or escalate"]
```

A practical verification checklist before acting on any AI output:

```text
[ ] Source: what data and model produced this, and is it in range?
[ ] Physics: does the result obey equilibrium, units, and load paths?
[ ] Code: does it satisfy the governing standard (NBR, ACI, Eurocode)?
[ ] Uncertainty: what is the error or confidence, and the failure mode?
[ ] Independent check: does a second method or engineer agree?
[ ] Accountability: who is the named responsible engineer signing off?

If any box cannot be honestly ticked, do not act on the output.
```

Two principles to carry out of this course:

- **The tool assists; the engineer is accountable.** AI does not hold a
  professional licence and cannot be responsible for a failure. The named
  engineer of record remains accountable, exactly as before.
- **Verify, then trust - never the reverse.** Use AI to work faster and
  see more, but keep physics, codes, and independent checks as the final
  authority. Treat AI output as a well-informed draft, not a verdict.

Remember: the point of AI in civil engineering is better information,
faster - never abdicated judgement. The engineer's signature still means
"I have verified this and I am responsible."
""",
        ),
        quiz_lesson(
            "Quiz: Responsible AI in engineering",
            (
                q(
                    "What is an AI 'hallucination' in this context?",
                    (
                        opt("A rendering glitch in the 3D model"),
                        opt(
                            "Fluent, confident output that is actually wrong - such as an "
                            "invented code clause or a mis-stated formula",
                            correct=True,
                        ),
                        opt("A sensor overheating"),
                        opt("A correct but slow answer"),
                    ),
                    "Confidence is not correctness; models can state wrong things "
                    "fluently, so they must be verified.",
                ),
                q(
                    "What is 'automation bias' and why is it dangerous in engineering?",
                    (
                        opt("A preference for manual tools"),
                        opt(
                            "The tendency to over-trust a computer's output and stop "
                            "checking - risky when the decision affects public safety",
                            correct=True,
                        ),
                        opt("A bias in the camera lens"),
                        opt("A scheduling conflict in the pipeline"),
                    ),
                    "The more capable the tool, the stronger the pull to stop verifying "
                    "- which is exactly when verification matters most.",
                ),
                q(
                    "Who is accountable for a decision made with the help of an AI tool?",
                    (
                        opt("The AI model itself"),
                        opt("Nobody, once AI is involved"),
                        opt(
                            "The qualified, named engineer of record who verifies the "
                            "output and signs off - the tool assists but is not "
                            "responsible",
                            correct=True,
                        ),
                        opt("The software vendor automatically"),
                    ),
                    "AI holds no licence and cannot be responsible; human-in-the-loop "
                    "means a named engineer verifies and remains accountable.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What separates a digital twin from a plain BIM model?",
                    (
                        opt("A larger file size"),
                        opt(
                            "A live two-way data connection keeping the twin synchronized "
                            "with the real asset's current state",
                            correct=True,
                        ),
                        opt("It is rendered in black and white"),
                        opt("It uses no standards"),
                    ),
                    "BIM is the designed model; the connection to the physical asset "
                    "makes it a twin (ISO 23247).",
                ),
                q(
                    "A strain gauge on a steel member reads 150 microstrain. Using "
                    "E = 200 GPa, the stress is about:",
                    (
                        opt("3 MPa"),
                        opt("30 MPa", correct=True),
                        opt("300 MPa"),
                        opt("3 GPa"),
                    ),
                    "sigma = E * epsilon = 200e9 * 150e-6 = 30e6 Pa = 30 MPa.",
                ),
                q(
                    "In structural health monitoring, damage is usually detected as:",
                    (
                        opt("A single dramatic reading that is obvious"),
                        opt(
                            "A drift or frequency shift away from a known-good baseline",
                            correct=True,
                        ),
                        opt("A change in the sensor's colour"),
                        opt("The network going offline"),
                    ),
                    "You compare against a baseline; damage shows as deviation, such as "
                    "shifted natural frequencies.",
                ),
                q(
                    "Why is the data pipeline's 'transform' stage essential before ML?",
                    (
                        opt("It compresses the images only"),
                        opt(
                            "Raw sensor data is noisy and gappy; unclean data yields "
                            "unreliable predictions (garbage in, garbage out)",
                            correct=True,
                        ),
                        opt("It renames the BIM elements"),
                        opt("It is never actually needed"),
                    ),
                    "Cleaning, validating and resampling produce the trustworthy input "
                    "models require.",
                ),
                q(
                    "Why must an ML model be scored on a held-out test set?",
                    (
                        opt("To make training faster"),
                        opt(
                            "To measure real predictive performance on unseen data rather "
                            "than memorization",
                            correct=True,
                        ),
                        opt("Because the library requires four datasets"),
                        opt("Only images need test sets"),
                    ),
                    "Evaluating on data the model never saw is the only honest accuracy measure.",
                ),
                q(
                    "How is computer vision used responsibly for defect detection?",
                    (
                        opt("It signs off structural condition automatically"),
                        opt(
                            "It flags candidate defects with a confidence score for an "
                            "engineer to confirm and measure",
                            correct=True,
                        ),
                        opt("It replaces all inspection permanently"),
                        opt("It only works on perfectly clean images"),
                    ),
                    "CV triages huge image sets and flags; the engineer confirms - "
                    "missed defects (false negatives) are the costly error.",
                ),
                q(
                    "In generative design, what is the engineer's primary responsibility?",
                    (
                        opt("To draw every candidate by hand"),
                        opt(
                            "To author correct objectives, constraints and load cases, "
                            "and to verify the chosen design against code",
                            correct=True,
                        ),
                        opt("To let the optimizer deploy the design directly"),
                        opt("To remove all constraints so the search is free"),
                    ),
                    "The optimizer exploits any missing constraint; the engineer owns "
                    "the problem statement and verifies the result.",
                ),
                q(
                    "Two bridges: A has failure probability 0.30 on a major route "
                    "(consequence 9); B has 0.60 on a rural road (consequence 3). Which "
                    "ranks higher by risk?",
                    (
                        opt("Bridge B, because its probability is higher"),
                        opt(
                            "Bridge A, because risk = probability x consequence gives "
                            "2.7 versus 1.8",
                            correct=True,
                        ),
                        opt("They are exactly equal"),
                        opt("Neither - risk ignores consequence"),
                    ),
                    "Risk = 0.30 x 9 = 2.7 for A versus 0.60 x 3 = 1.8 for B; "
                    "consequence tips it to A.",
                ),
                q(
                    "What does 'remaining useful life' let an asset manager do?",
                    (
                        opt("Repaint on a fixed calendar regardless of condition"),
                        opt(
                            "Estimate how much service life is left and schedule "
                            "intervention just in time",
                            correct=True,
                        ),
                        opt("Ignore the asset until it fails"),
                        opt("Count the number of workers"),
                    ),
                    "RUL turns condition and trend into an intervention window - the "
                    "heart of predictive maintenance.",
                ),
                q(
                    "What is the guiding principle for using AI responsibly in engineering?",
                    (
                        opt("Trust the model output and skip verification"),
                        opt(
                            "AI assists and gives better information faster, but a named "
                            "engineer verifies against physics and code and remains "
                            "accountable",
                            correct=True,
                        ),
                        opt("The AI holds the professional responsibility"),
                        opt("Verification is optional if confidence is high"),
                    ),
                    "Verify then trust; the engineer's signature still means 'I have "
                    "verified this and I am responsible.'",
                ),
            ),
            duration="10 min",
        ),
    ),
)

DIGITAL_TWINS_AI_CONSTRUCTION_COURSES: tuple[SeedCourse, ...] = (_DIGITAL_TWINS_AI_CONSTRUCTION,)
