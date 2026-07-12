"""Academy seed content - AI and Data Science for Environmental Engineering.

The flagship new-technology course of the Environmental Engineering track:
how machine learning and data science reshape environmental practice.
It covers the end-to-end data science workflow, supervised learning for
regression and classification, time-series forecasting for air quality and
streamflow, anomaly and leak detection, computer vision for satellite change
detection, IoT real-time sensing, digital twins of treatment plants, and
responsible AI (explainability, uncertainty and limits). Every lesson is a
direct explanation with a concrete Python or data example and a mermaid
diagram, followed by a checkpoint quiz; the course closes with a
comprehensive final quiz.
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


_AI_FOR_ENVIRONMENTAL_ENGINEERING = SeedCourse(
    slug="ai-for-environmental-engineering",
    title="AI & Data Science for Environmental Engineering",
    description=(
        "How AI and data science transform environmental engineering: machine "
        "learning for air and water forecasting, satellite change detection, "
        "IoT sensing, digital twins of treatment plants, and responsible AI - "
        "with concrete Python snippets, data pipelines and a diagram in every "
        "lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# AI and Data Science for Environmental Engineering

Environmental engineering has always been data-driven - gauge readings,
lab assays, emissions inventories. What changed is the **scale and the
methods**: continuous IoT sensors, petabytes of free satellite imagery,
and machine learning that can forecast, classify and detect patterns no
hand-tuned model could. This course connects that modern toolkit to the
practice you already know: mass balances, water-quality standards, air
dispersion, and treatment-plant operation.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a short real example - a Python or pandas snippet, a data
pipeline, or a formula - and draws it as a diagram. After each lesson
there is a short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **The environmental data science workflow** - from raw sensor to decision
2. **Machine learning for regression and classification** - the core methods
3. **Time-series forecasting** - air quality and streamflow
4. **Anomaly and leak detection** - finding the abnormal automatically
5. **Computer vision for satellite change detection** - deforestation, floods
6. **IoT and real-time environmental sensing** - the streaming edge
7. **Digital twins of treatment plants** - live models that mirror reality
8. **Responsible AI** - explainability, uncertainty and hard limits

Throughout we stay grounded in real standards and tools - **WHO** and
**EPA** air and water guidelines, **CONAMA** and **ABNT NBR** where they
apply, and open stacks like **scikit-learn**, **pandas**, **Sentinel** and
**Landsat** imagery, **EPANET** and **QUAL2K**. AI does not replace the
engineering; it amplifies it. The judgment about what a number means, and
what to do about it, stays yours.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the central premise of this course?",
                    (
                        opt("AI replaces environmental engineering judgment entirely"),
                        opt(
                            "Modern data science (IoT, satellite imagery, machine "
                            "learning) amplifies established environmental engineering "
                            "practice - the engineering judgment stays with you",
                            correct=True,
                        ),
                        opt("Environmental data is too messy for any model"),
                        opt("Only satellite imagery matters"),
                    ),
                    "AI amplifies the practice; deciding what a result means and what "
                    "to do about it remains an engineering responsibility.",
                ),
                q(
                    "How is each lesson structured?",
                    (
                        opt("Only a video, no examples"),
                        opt(
                            "A direct explanation, a concrete example (Python, a data "
                            "pipeline, or a formula), and a mermaid diagram, followed by "
                            "a short quiz",
                            correct=True,
                        ),
                        opt("Pure theory with no code"),
                        opt("A reading list only"),
                    ),
                    "Explanation plus a concrete example plus a diagram, then a checkpoint quiz.",
                ),
            ),
        ),
        # -- 1. Workflow -----------------------------------------------
        _t(
            "The environmental data science workflow",
            "10 min",
            """# The environmental data science workflow

Before any model, there is a **workflow** - the disciplined path from a
raw measurement to a decision you can defend. Skipping it is the single
most common reason environmental ML projects fail: a clever model on badly
prepared data is worse than useless, because it looks authoritative.

The stages, in order:

- **Frame the question** - what decision does this serve? "Predict
  tomorrow's PM2.5 so we can issue a health advisory" is a usable frame;
  "do some AI on the sensor data" is not.
- **Ingest** - pull from sensors, lab LIMS, satellite archives, public
  APIs (e.g. EPA AQS, national water agencies).
- **Clean** - the bulk of the work. Handle missing values, sensor drift,
  calibration offsets, unit mismatches, and outliers that are faults
  (a negative dissolved-oxygen reading) versus real events (a spill).
- **Explore (EDA)** - plot distributions and correlations; understand the
  data before modeling it.
- **Feature engineering** - derive useful inputs: rolling means, lags,
  hour-of-day, upstream rainfall.
- **Model** - fit, then **validate honestly** (respecting time order).
- **Deploy and monitor** - a model in production drifts as the world
  changes; watch it.

A tiny but realistic cleaning step in **pandas**:

```python
import pandas as pd

df = pd.read_csv("station_pm25.csv", parse_dates=["timestamp"])
df = df.set_index("timestamp").sort_index()

# 1. Physically impossible readings are sensor faults, not data
df.loc[df["pm25"] < 0, "pm25"] = pd.NA

# 2. Flag a stuck sensor: same value repeated for hours
stuck = df["pm25"].eq(df["pm25"].shift()).rolling(6).sum() >= 6
df.loc[stuck, "pm25"] = pd.NA

# 3. Fill short gaps, but never invent long ones
df["pm25"] = df["pm25"].interpolate(limit=3)     # up to 3 hours only
```

The rule that separates real environmental data science from a demo:
**garbage in, garbage out is not a cliche here - it is a public-health
risk**. Most of your time is cleaning and validating, and that is correct.

```mermaid
graph LR
    FRAME["Frame the question"] --> INGEST["Ingest data"]
    INGEST --> CLEAN["Clean and validate"]
    CLEAN --> EDA["Explore the data"]
    EDA --> FEAT["Engineer features"]
    FEAT --> MODEL["Model and validate"]
    MODEL --> DEPLOY["Deploy and monitor"]
    DEPLOY --> FRAME
```

Remember: the workflow is a loop, not a line. A deployed model feeds back
lessons that reframe the next question.
""",
        ),
        quiz_lesson(
            "Quiz: The environmental data science workflow",
            (
                q(
                    "Why is 'frame the question' the first stage of the workflow?",
                    (
                        opt("Because framing is optional paperwork"),
                        opt(
                            "A model must serve a concrete decision; a clear frame like "
                            "'predict tomorrow's PM2.5 to issue an advisory' guides every "
                            "later choice, while 'do some AI' does not",
                            correct=True,
                        ),
                        opt("Because it makes the model train faster"),
                        opt("Because regulators require a written frame"),
                    ),
                    "The decision the model serves determines the data, the metric and "
                    "the acceptable error - so it comes first.",
                ),
                q(
                    "In the cleaning step, why set a negative PM2.5 reading to missing?",
                    (
                        opt("Negative pollution is possible but rare"),
                        opt(
                            "A negative concentration is physically impossible, so it is "
                            "a sensor fault - keeping it would poison the model",
                            correct=True,
                        ),
                        opt("Because pandas cannot store negatives"),
                        opt("To make the average look lower"),
                    ),
                    "Physically impossible values are faults; distinguishing faults from "
                    "real events is the core of cleaning.",
                ),
                q(
                    "Why interpolate only short gaps (e.g. limit=3) and not long ones?",
                    (
                        opt("Long interpolation is slower to compute"),
                        opt(
                            "Filling a long gap invents data that was never measured, "
                            "creating false confidence; short gaps can be bridged safely",
                            correct=True,
                        ),
                        opt("Because the CSV format forbids it"),
                        opt("Interpolation always makes data worse"),
                    ),
                    "Bridging a few missing hours is defensible; fabricating a whole day "
                    "of readings is not.",
                ),
            ),
        ),
        # -- 2. ML regression/classification ---------------------------
        _t(
            "Machine learning for regression and classification",
            "11 min",
            """# Machine learning for regression and classification

Most environmental ML falls into two supervised tasks. **Regression**
predicts a continuous number - a BOD concentration, a PM2.5 level, a
streamflow in cubic metres per second. **Classification** predicts a
category - "is this water potable?", "is this a flood pixel?", "is this
sensor faulty?". The method you reach for depends on which of these you
have framed.

Common workhorses, roughly in order of complexity:

- **Linear and logistic regression** - simple, interpretable baselines.
  Always start here; a fancy model that cannot beat linear regression is
  telling you something.
- **Decision trees** - human-readable if-then splits.
- **Random forests and gradient boosting** (XGBoost, LightGBM) - ensembles
  of trees, the reliable default for tabular environmental data.
- **Neural networks** - powerful for images and sequences, data-hungry and
  harder to interpret.

The non-negotiable discipline is **honest validation**. You split data
into **train** and **test** sets, fit only on train, and judge on the
unseen test set. For regression you report **RMSE** or **MAE**; for
classification, **precision** and **recall** (accuracy alone lies when
classes are imbalanced - and environmental events like spills are rare).

A worked regression example predicting dissolved oxygen from routine
parameters:

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

X = df[["temperature", "bod", "nitrate", "flow"]]
y = df["dissolved_oxygen"]

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
model = RandomForestRegressor(n_estimators=300).fit(X_tr, y_tr)

pred = model.predict(X_te)
print("MAE:", mean_absolute_error(y_te, pred), "mg/L")
```

Two failure modes to internalize. **Overfitting**: the model memorizes the
training data (great on train, poor on test) - use simpler models, more
data, or regularization. **Data leakage**: a feature secretly contains the
answer (predicting a lab result from a field kit that measured the same
thing) - it looks brilliant in testing and fails in production.

```mermaid
graph TD
    DATA["Labeled data"] --> SPLIT["Train test split"]
    SPLIT --> TRAIN["Fit on train only"]
    TRAIN --> EVAL["Evaluate on unseen test"]
    EVAL --> REG["Regression uses RMSE or MAE"]
    EVAL --> CLS["Classification precision and recall"]
    EVAL --> CHECK["Watch for overfitting and leakage"]
```

Remember: start simple, validate on unseen data, and choose the metric
that matches the decision - a missed spill costs far more than a false
alarm, so recall may matter more than accuracy.
""",
        ),
        quiz_lesson(
            "Quiz: Machine learning for regression and classification",
            (
                q(
                    "Predicting tomorrow's streamflow in cubic metres per second is which task?",
                    (
                        opt("Classification"),
                        opt("Regression - the target is a continuous number", correct=True),
                        opt("Clustering"),
                        opt("Neither - it cannot be modeled"),
                    ),
                    "A continuous numeric target is regression; a categorical target "
                    "(flood or not) would be classification.",
                ),
                q(
                    "Why can accuracy be misleading for rare environmental events like spills?",
                    (
                        opt("Accuracy is always the best metric"),
                        opt(
                            "With imbalanced classes, a model that predicts 'no spill' "
                            "every time scores high accuracy while catching zero spills - "
                            "precision and recall reveal the truth",
                            correct=True,
                        ),
                        opt("Accuracy cannot be computed for spills"),
                        opt("Spills are too common to measure"),
                    ),
                    "When positives are rare, always look at precision and recall, not "
                    "accuracy alone.",
                ),
                q(
                    "What is data leakage?",
                    (
                        opt("A pipe bursting in the treatment plant"),
                        opt("Losing data to a disk failure"),
                        opt(
                            "A feature that secretly contains the answer, making the "
                            "model look excellent in testing but fail in production",
                            correct=True,
                        ),
                        opt("Training on too little data"),
                    ),
                    "Leakage inflates test scores dishonestly; guard against features "
                    "that would not be available at prediction time.",
                ),
            ),
        ),
        # -- 3. Time-series forecasting --------------------------------
        _t(
            "Time-series forecasting (air quality, streamflow)",
            "11 min",
            """# Time-series forecasting (air quality, streamflow)

Much environmental data is a **time series** - values ordered in time,
where each point depends on the ones before. Forecasting the next value
(tomorrow's PM2.5, next week's river flow) is its own discipline, and the
first rule breaks a habit from ordinary ML: **you must never shuffle time**.

Because past predicts future, you validate with a **forward chaining**
split - train on earlier data, test on strictly later data. A random
train/test split leaks the future into the past and gives fantasy scores.

The methods span a ladder:

- **Classical statistics** - ARIMA and SARIMA capture trend and
  seasonality; excellent, interpretable baselines for a single series.
- **Machine learning on lag features** - turn the series into a table of
  lagged values and let gradient boosting learn; strong and practical.
- **Deep learning** - LSTM and other recurrent networks, or Transformers,
  for long, complex, multi-variable sequences (weather-driven streamflow).

Environmental series have structure you should exploit as **features**:

```text
Useful engineered features for an air-quality forecast:
  lag_1h, lag_24h        -> yesterday and same-hour-yesterday values
  roll_mean_24h          -> smoothed recent level
  hour, day_of_week      -> daily and weekly traffic cycles
  temp, wind_speed, rain -> meteorology drives dispersion
  is_holiday             -> emissions differ on holidays
```

A minimal forward-chaining setup with scikit-learn:

```python
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import GradientBoostingRegressor

tscv = TimeSeriesSplit(n_splits=5)      # each fold trains on the past only
for train_idx, test_idx in tscv.split(X):
    model = GradientBoostingRegressor().fit(X.iloc[train_idx], y.iloc[train_idx])
    score = model.score(X.iloc[test_idx], y.iloc[test_idx])
```

Always report the forecast with a **horizon** (how far ahead) and an
**uncertainty band** - a single number without "how far and how sure" is
not an actionable forecast for a health advisory or a flood warning.

```mermaid
graph LR
    SERIES["Raw time series"] --> LAGS["Build lag and calendar features"]
    LAGS --> MET["Add meteorology drivers"]
    MET --> SPLIT["Forward chaining split"]
    SPLIT --> FIT["Train on past"]
    FIT --> FCAST["Forecast next horizon"]
    FCAST --> BAND["Report with uncertainty band"]
```

Remember: respect time order, engineer lag and weather features, and always
attach a horizon and an uncertainty band to the forecast.
""",
        ),
        quiz_lesson(
            "Quiz: Time-series forecasting (air quality, streamflow)",
            (
                q(
                    "Why must you not use a random train/test split for time-series forecasting?",
                    (
                        opt("Random splits are too slow"),
                        opt(
                            "Shuffling lets future values train the model that then "
                            "predicts the past - leaking the future and giving unrealistic "
                            "scores; use a forward-chaining split instead",
                            correct=True,
                        ),
                        opt("Random splits use too much memory"),
                        opt("Time series cannot be split at all"),
                    ),
                    "Forward chaining trains on the past and tests on strictly later "
                    "data, matching how forecasting actually works.",
                ),
                q(
                    "Why add meteorology (temperature, wind, rain) as features to an air-quality forecast?",
                    (
                        opt("To make the table look bigger"),
                        opt(
                            "Weather physically drives dispersion and accumulation of "
                            "pollutants, so it carries real predictive signal",
                            correct=True,
                        ),
                        opt("Because ARIMA requires it"),
                        opt("Meteorology is irrelevant to air quality"),
                    ),
                    "Wind disperses, stagnation accumulates, rain scavenges - "
                    "meteorology is a genuine driver.",
                ),
                q(
                    "What two things must accompany a forecast to make it actionable?",
                    (
                        opt("A logo and a timestamp"),
                        opt(
                            "A horizon (how far ahead) and an uncertainty band (how sure)",
                            correct=True,
                        ),
                        opt("The training code and the raw data"),
                        opt("A color and a font"),
                    ),
                    "Without 'how far ahead' and 'how confident', a single number cannot "
                    "support a health advisory or flood warning.",
                ),
            ),
        ),
        # -- 4. Anomaly & leak detection -------------------------------
        _t(
            "Anomaly and leak detection",
            "10 min",
            """# Anomaly and leak detection

Not every problem comes with labeled examples. You rarely have a tidy
dataset of "leaks" and "not leaks" to train on - leaks are rare, varied,
and often unrecorded. **Anomaly detection** solves this: learn what
**normal** looks like, then flag whatever deviates. It is mostly
**unsupervised**, which is exactly why it fits environmental monitoring.

Where it earns its keep:

- **Water distribution leaks** - a District Metered Area shows a rising
  **minimum night flow**; when demand should be near zero but flow is not,
  water is escaping.
- **Sensor faults** - a stuck, drifting, or spiking probe.
- **Illicit discharges** - a sudden conductivity or pH excursion in a sewer
  that fingerprints an industrial dump.
- **Process upsets** - a treatment stage sliding out of its normal band.

Methods, from simple to learned:

- **Statistical thresholds** - control charts, the classic **3-sigma** rule:
  flag a point more than three standard deviations from the rolling mean.
- **Isolation Forest** - isolates outliers because they are "few and
  different"; robust and needs no labels.
- **Autoencoders** - a neural net trained to reconstruct normal data; a
  large **reconstruction error** means "this does not look normal".

The core statistical idea in one formula:

```text
Rolling z-score anomaly flag (control-chart logic):

    z_t = ( x_t - mean_window ) / std_window

    flag if |z_t| > 3      (a "3-sigma" excursion)

Leak-specific signal in a District Metered Area:
    minimum night flow rising over days, with no legitimate demand,
    indicates a background leak growing in the network.
```

And an unsupervised detector in a few lines:

```python
from sklearn.ensemble import IsolationForest

# expected fraction of anomalies; no labels needed
detector = IsolationForest(contamination=0.01, random_state=0)
df["anomaly"] = detector.fit_predict(df[["flow", "pressure", "conductivity"]])
alerts = df[df["anomaly"] == -1]     # -1 marks the outliers
```

The engineering catch is the **threshold trade-off**: too sensitive floods
operators with false alarms until they ignore the system; too lax misses
real leaks. Tune it against the real cost of a missed event versus a false
alarm, and always give a human the context to confirm.

```mermaid
graph TD
    STREAM["Live sensor stream"] --> NORMAL["Learn normal behavior"]
    NORMAL --> SCORE["Score each new point"]
    SCORE --> OK["Within normal band"]
    SCORE --> FLAG["Deviation flagged"]
    FLAG --> TRIAGE["Human triage and confirm"]
    TRIAGE --> ACTION["Dispatch or dismiss"]
```

Remember: model normal, flag the deviation, and tune sensitivity to the
real cost of misses versus false alarms - the alert is a prompt for a human,
not a verdict.
""",
        ),
        quiz_lesson(
            "Quiz: Anomaly and leak detection",
            (
                q(
                    "Why is anomaly detection usually unsupervised in environmental monitoring?",
                    (
                        opt("Because unsupervised methods are always more accurate"),
                        opt(
                            "Leaks and faults are rare, varied and often unlabeled, so "
                            "instead of training on examples you learn normal behavior and "
                            "flag deviations",
                            correct=True,
                        ),
                        opt("Because labels are illegal to use"),
                        opt("Because sensors cannot be labeled"),
                    ),
                    "You seldom have a clean labeled set of leaks, so you model normal "
                    "and flag what departs from it.",
                ),
                q(
                    "In a District Metered Area, what signal suggests a background leak?",
                    (
                        opt("Zero flow at all hours"),
                        opt(
                            "A rising minimum night flow - water moving when legitimate "
                            "demand should be near zero",
                            correct=True,
                        ),
                        opt("High pressure during the day"),
                        opt("A single spike in conductivity"),
                    ),
                    "At night true demand nears zero, so persistent or rising night flow "
                    "points to water escaping the network.",
                ),
                q(
                    "What is the core threshold trade-off in anomaly detection?",
                    (
                        opt("Faster models versus slower models"),
                        opt(
                            "Too sensitive floods operators with false alarms until they "
                            "ignore alerts; too lax misses real events - tune to the real "
                            "cost of each",
                            correct=True,
                        ),
                        opt("More sensors versus fewer sensors"),
                        opt("Cloud storage versus local storage"),
                    ),
                    "Sensitivity must be tuned against the cost of a missed leak versus "
                    "the cost of a false alarm.",
                ),
            ),
        ),
        # -- 5. CV satellite change detection --------------------------
        _t(
            "Computer vision for satellite change detection (deforestation, floods)",
            "12 min",
            """# Computer vision for satellite change detection

Free, frequent satellite imagery - **Landsat** (since the 1970s) and the
EU **Sentinel** program - turned Earth observation into a data science
problem. **Computer vision** lets us detect and map change across whole
regions automatically: deforestation, flood extent, algal blooms, urban
sprawl, burn scars. What once took a field team now runs on an image.

The key insight is that different surfaces reflect light differently across
**spectral bands**, and simple **band-math indices** already reveal a lot
before any deep learning:

```text
NDVI - Normalized Difference Vegetation Index (vegetation health):

    NDVI = (NIR - RED) / (NIR + RED)

    ~ 0.6 to 0.9  dense healthy vegetation
    ~ 0.2 to 0.5  sparse vegetation or shrub
    < 0.1         bare soil, rock, water, built-up

NDWI - Normalized Difference Water Index (open water, floods):

    NDWI = (GREEN - NIR) / (GREEN + NIR)      (positive over water)
```

**Change detection** compares two dates. The simplest method differences an
index: a stretch of forest whose NDVI drops from 0.8 to 0.2 between two
images is very likely **deforestation**; a rise in NDWI over dry land maps
a **flood**. Deep models (a **U-Net** semantic-segmentation network) go
further, labeling every pixel as forest, water, cloud or bare ground - and
learning subtler change than a single index.

A band-math change detector in a few lines:

```python
import numpy as np

def ndvi(nir, red):
    return (nir - red) / (nir + red + 1e-9)     # epsilon avoids divide by zero

ndvi_before = ndvi(img_2020["nir"], img_2020["red"])
ndvi_after  = ndvi(img_2024["nir"], img_2024["red"])

loss = (ndvi_before > 0.6) & (ndvi_after < 0.3)   # was forest, now bare
print("deforested pixels:", int(loss.sum()))
area_ha = loss.sum() * (10 * 10) / 10_000          # Sentinel-2 is 10 m pixels
```

Two practical cautions define real work here. **Clouds** masquerade as
change and must be masked out (or use cloud-penetrating **radar**, Sentinel-1
SAR, for floods). And **registration** matters: the two images must line up
pixel-for-pixel, or you detect motion that is not there. This work
underpins operational systems like Brazil's **PRODES and DETER** Amazon
monitoring and global flood-response mapping.

```mermaid
graph LR
    T1["Image time one"] --> IDX1["Compute index"]
    T2["Image time two"] --> IDX2["Compute index"]
    IDX1 --> DIFF["Difference the indices"]
    IDX2 --> DIFF
    CLOUD["Cloud mask"] --> DIFF
    DIFF --> MAP["Change map"]
    MAP --> AREA["Quantify area changed"]
```

Remember: spectral band math already detects a lot, deep segmentation
detects more, and clouds plus misregistration are the errors that will fool
you if you skip them.
""",
        ),
        quiz_lesson(
            "Quiz: Computer vision for satellite change detection (deforestation, floods)",
            (
                q(
                    "What does a sharp drop in NDVI between two dates over the same area suggest?",
                    (
                        opt("The satellite malfunctioned"),
                        opt(
                            "Loss of vegetation - very likely deforestation or clearing, "
                            "since NDVI tracks vegetation health",
                            correct=True,
                        ),
                        opt("More rainfall"),
                        opt("Nothing can be inferred from NDVI"),
                    ),
                    "NDVI = (NIR - RED)/(NIR + RED); healthy forest is high, bare ground "
                    "is low, so a large drop maps clearing.",
                ),
                q(
                    "Why must clouds be masked in optical change detection?",
                    (
                        opt("Clouds make the image prettier"),
                        opt(
                            "Clouds change between dates and masquerade as real surface "
                            "change; unmasked, they produce false detections - radar can "
                            "see through them for floods",
                            correct=True,
                        ),
                        opt("Clouds speed up the computation"),
                        opt("Clouds only affect radar, not optical"),
                    ),
                    "A cloud present on one date but not the other looks like change; "
                    "mask it or use cloud-penetrating SAR.",
                ),
                q(
                    "Why does image registration matter in change detection?",
                    (
                        opt("It compresses the files"),
                        opt(
                            "The two images must align pixel-for-pixel, or apparent change "
                            "is really just misalignment between dates",
                            correct=True,
                        ),
                        opt("It converts the color palette"),
                        opt("It is only needed for video"),
                    ),
                    "Misregistered images make stationary ground appear to move, "
                    "creating spurious change.",
                ),
            ),
        ),
        # -- 6. IoT sensing --------------------------------------------
        _t(
            "IoT and real-time environmental sensing",
            "11 min",
            """# IoT and real-time environmental sensing

Traditional monitoring meant a technician visiting a station monthly.
**Environmental IoT** replaces that with dense networks of low-cost
sensors reporting continuously - air-quality nodes on lampposts, water
probes in rivers, flow and pressure meters across a distribution network.
The result is orders of magnitude more data, in real time, which is what
makes the forecasting and anomaly detection in this course operational
rather than academic.

A typical architecture has four layers:

- **Edge** - the sensor and a small processor. Low-power radios like
  **LoRaWAN** or NB-IoT send tiny messages over kilometres on a battery.
  Some cleaning and thresholding happen here (**edge computing**) to save
  bandwidth and react instantly.
- **Ingest** - a broker (often **MQTT**, a lightweight publish/subscribe
  protocol built for constrained devices) receives the stream.
- **Store and process** - a time-series database and a stream processor.
- **Serve** - dashboards, alerts, and the ML models above, closing the loop.

The defining engineering problem is **data quality at scale**. Low-cost
sensors **drift** and are affected by temperature and humidity, so they
need periodic **co-location calibration** against a reference-grade
instrument. A dense network of imperfect sensors, well calibrated and
cross-checked, beats one perfect station - but only if you manage the
quality.

A small MQTT edge publisher, with a sanity check before sending:

```python
import json, paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.local", 1883)

def publish(reading):
    # edge validation: drop physically impossible values at the source
    if not (0 <= reading["pm25"] <= 1000):
        return
    payload = json.dumps({"station": "node-17", **reading})
    client.publish("air/pm25", payload, qos=1)   # qos 1 = at least once
```

The payoff is **timeliness**: a flood gauge that reports every minute can
trigger a warning while there is still time to act; a distribution network
streaming pressure can localize a burst in minutes, not after customer
complaints. Real-time data turns monitoring from a record of what happened
into a tool for acting before it gets worse.

```mermaid
graph LR
    SENSOR["Edge sensor"] --> EDGE["Edge validate and calibrate"]
    EDGE --> BROKER["MQTT broker"]
    BROKER --> TSDB["Time series store"]
    TSDB --> ML["Forecast and anomaly models"]
    ML --> DASH["Dashboards and alerts"]
    DASH --> ACT["Act in time"]
```

Remember: dense real-time sensing enables everything else, but low-cost
sensors drift - calibration and quality control are the price of trusting
the stream.
""",
        ),
        quiz_lesson(
            "Quiz: IoT and real-time environmental sensing",
            (
                q(
                    "What is 'edge computing' in an environmental IoT network?",
                    (
                        opt("Storing all data in one central cloud only"),
                        opt(
                            "Doing some processing (validation, thresholding) at or near "
                            "the sensor to save bandwidth and react instantly",
                            correct=True,
                        ),
                        opt("Placing sensors only at the edge of a city"),
                        opt("Using the fastest possible internet"),
                    ),
                    "Edge computing pushes light processing to the device, reducing "
                    "traffic and enabling immediate local reaction.",
                ),
                q(
                    "Why do low-cost IoT sensors need periodic co-location calibration?",
                    (
                        opt("To make them look more expensive"),
                        opt(
                            "They drift and are affected by temperature and humidity, so "
                            "comparing against a reference-grade instrument keeps their "
                            "readings trustworthy",
                            correct=True,
                        ),
                        opt("Calibration is only a legal formality"),
                        opt("They never need calibration"),
                    ),
                    "Low-cost sensors drift; co-locating with a reference instrument "
                    "corrects them so the dense network can be trusted.",
                ),
                q(
                    "What is the core operational payoff of real-time IoT sensing?",
                    (
                        opt("Cheaper sensors only"),
                        opt(
                            "Timeliness - reporting every minute lets you warn or "
                            "localize a burst while there is still time to act, not after "
                            "the fact",
                            correct=True,
                        ),
                        opt("It removes the need for any model"),
                        opt("It guarantees perfect data"),
                    ),
                    "Timeliness turns monitoring from a record of the past into a tool "
                    "for acting before things worsen.",
                ),
            ),
        ),
        # -- 7. Digital twins ------------------------------------------
        _t(
            "Digital twins of treatment plants",
            "11 min",
            """# Digital twins of treatment plants

A **digital twin** is a live, data-connected model of a physical asset - a
water or wastewater treatment plant - that mirrors its current state,
updated continuously from sensors, and can be used to **predict, test and
optimize** without touching the real process. It is the convergence of
everything so far: physics-based process models, IoT streams, and machine
learning, fused into one operational replica.

It is more than a simulation. The distinction is the **live data link**:

- A **model** describes how the plant behaves in principle.
- A **digital twin** is that model continuously **synchronized** with the
  real plant's live sensor data, so it reflects the actual current state,
  not a generic one.

Twins of treatment plants typically combine two kinds of model:

- **Mechanistic** - established process physics and biology, e.g. the
  **Activated Sludge Models (ASM1/ASM2d)** for biological nutrient removal,
  or hydraulic models of the network. These encode known engineering.
- **Data-driven** - ML that learns residuals and patterns the equations
  miss (influent quality patterns, energy use, membrane fouling).

What operators actually do with a twin:

- **What-if simulation** - "if influent ammonia doubles at 6am, will the
  effluent breach the permit? Should we raise aeration now?" Test it on the
  twin first.
- **Soft sensors** - infer an expensive or slow lab measurement (effluent
  BOD, taking days) in real time from cheap online signals.
- **Optimization** - aeration is often the largest energy cost; a twin can
  tune dissolved-oxygen setpoints to meet the permit at minimum energy.
- **Operator training and anomaly rehearsal** - safely.

A minimal soft-sensor / what-if loop in pseudo-Python:

```python
# twin = mechanistic core (ASM) + ML residual correction, kept in sync
state = twin.update(live_sensors)                 # synchronize to reality now

# soft sensor: estimate a slow lab value from fast online signals
effluent_bod = twin.estimate("effluent_bod", state)

# what-if: simulate a shock load before it reaches the works
future = twin.simulate(state, influent_ammonia=state.ammonia * 2, horizon="6h")
if future.effluent_nh3 > PERMIT_LIMIT:
    recommend("increase aeration setpoint now")
```

The honest caveat: a twin is only as good as its **calibration and data**.
It must be validated against real plant behavior and re-calibrated as the
biology, equipment and influent change - a stale twin quietly stops
matching reality and gives confident wrong advice. This ties directly to
the responsible-AI lesson next.

```mermaid
graph TD
    PLANT["Physical plant"] --> SENSE["Live sensor stream"]
    SENSE --> TWIN["Digital twin model"]
    MECH["Mechanistic ASM core"] --> TWIN
    ML["Data driven correction"] --> TWIN
    TWIN --> WHATIF["What if simulation"]
    TWIN --> SOFT["Soft sensor estimates"]
    WHATIF --> OPT["Optimize aeration and setpoints"]
    OPT --> PLANT
```

Remember: a digital twin is a model kept live by sensor data - use it to
predict, test and optimize before acting on the real plant, and keep it
calibrated or it will confidently mislead.
""",
        ),
        quiz_lesson(
            "Quiz: Digital twins of treatment plants",
            (
                q(
                    "What distinguishes a digital twin from an ordinary simulation model?",
                    (
                        opt("A twin runs faster"),
                        opt(
                            "A twin is continuously synchronized with the real plant's "
                            "live sensor data, so it reflects the actual current state, "
                            "not a generic one",
                            correct=True,
                        ),
                        opt("A twin needs no model at all"),
                        opt("A twin is only a 3D picture"),
                    ),
                    "The live data link is the defining feature - the twin mirrors the "
                    "plant's real current state.",
                ),
                q(
                    "What is a 'soft sensor' in this context?",
                    (
                        opt("A physical sensor made of soft plastic"),
                        opt(
                            "An estimate of an expensive or slow measurement (like "
                            "effluent BOD) inferred in real time from cheap online signals",
                            correct=True,
                        ),
                        opt("A sensor that only works in soft water"),
                        opt("A backup sensor kept in storage"),
                    ),
                    "Soft sensors infer a costly or slow lab value from fast, cheap "
                    "online signals via the model.",
                ),
                q(
                    "Why must a digital twin be re-calibrated over time?",
                    (
                        opt("To use a newer software version"),
                        opt(
                            "The biology, equipment and influent change, so a stale twin "
                            "stops matching reality and gives confident wrong advice",
                            correct=True,
                        ),
                        opt("Calibration makes it look more impressive"),
                        opt("Twins never need re-calibration once built"),
                    ),
                    "A twin is only as good as its data and calibration; drift makes it "
                    "quietly mislead.",
                ),
            ),
        ),
        # -- 8. Responsible AI -----------------------------------------
        _t(
            "Responsible AI: explainability, uncertainty and limitations",
            "11 min",
            """# Responsible AI: explainability, uncertainty and limitations

Environmental decisions affect public health, ecosystems and legal
compliance. A model that issues an air-quality advisory, sizes a flood
defence, or certifies effluent quality carries real consequences, so it
must be **trustworthy, not just accurate**. Responsible AI is the
engineering discipline that makes it so, and it rests on three ideas.

**Explainability.** A black box that says "trust me" is unacceptable when a
regulator or a citizen asks *why*. Techniques like **feature importance**
and **SHAP** values open the box - showing that a flood prediction was
driven mostly by upstream rainfall and soil saturation, which an engineer
can sanity-check against physics. If the model relied on something absurd,
you catch it before it does harm.

**Uncertainty.** Every prediction has error, and reporting it honestly is
non-negotiable. "PM2.5 will be 80 plus or minus 15 micrograms per cubic
metre" is an engineering statement; "PM2.5 will be 80" pretends to a
precision that does not exist. Prediction intervals let a decision-maker
weigh risk. A model must also flag when an input is **outside its training
range** (extrapolation) - a flood model never trained on a record storm
should say "I do not know", not guess confidently.

**Limitations and bias.** Models inherit the flaws of their data. A sensor
network sparse in poorer neighbourhoods yields a model blind to their air
quality - an **environmental-justice** failure. Correlation is not
causation: a model may exploit a spurious link that breaks when conditions
shift. And a model trained on the past can fail under **climate change**,
where the future is deliberately unlike the training data.

```text
Responsible reporting of an environmental forecast:

    point estimate      80 ug/m3        (the prediction)
    uncertainty         +/- 15 ug/m3    (how sure)
    top drivers         rainfall, wind  (why - from SHAP)
    in training range?  yes / NO         (can we trust it here)
    known limits        sparse rural data, no wildfire cases
```

The governing principle is **human-in-the-loop**. AI is a decision-support
tool, not the decision-maker. It surfaces patterns, forecasts and alerts;
a qualified engineer, accountable and equipped with explanation and
uncertainty, makes the call - especially for anything safety- or
compliance-critical. Frameworks like **ISO 14001** environmental management
still frame the responsibility; the AI serves it.

```mermaid
graph TD
    MODEL["Model prediction"] --> EXPLAIN["Explain the drivers"]
    MODEL --> UNCERT["Report uncertainty"]
    MODEL --> LIMITS["State limits and bias"]
    EXPLAIN --> HUMAN["Human in the loop"]
    UNCERT --> HUMAN
    LIMITS --> HUMAN
    HUMAN --> DECISION["Accountable decision"]
```

Remember: accuracy is not enough. Explain the why, report the uncertainty,
be honest about limits, and keep an accountable human making the call.
""",
        ),
        quiz_lesson(
            "Quiz: Responsible AI: explainability, uncertainty and limitations",
            (
                q(
                    "Why is explainability (e.g. SHAP, feature importance) important for environmental models?",
                    (
                        opt("It makes the model train faster"),
                        opt(
                            "When a regulator or citizen asks why, you can show the "
                            "drivers and sanity-check them against physics - catching "
                            "absurd reasoning before it causes harm",
                            correct=True,
                        ),
                        opt("It is only needed for images"),
                        opt("It replaces the need for accuracy"),
                    ),
                    "Explainability opens the black box so an engineer can verify the "
                    "prediction rests on sensible drivers.",
                ),
                q(
                    "Which is the responsible way to report a PM2.5 forecast?",
                    (
                        opt("PM2.5 will be exactly 80 - no other detail"),
                        opt(
                            "PM2.5 will be about 80 plus or minus 15, with the main "
                            "drivers and a note if the input is outside the training range",
                            correct=True,
                        ),
                        opt("PM2.5 is impossible to forecast"),
                        opt("Report only the model's accuracy score"),
                    ),
                    "Honest uncertainty and a flag for extrapolation let a decision-maker "
                    "weigh the risk; a bare number feigns false precision.",
                ),
                q(
                    "What is the 'human-in-the-loop' principle for environmental AI?",
                    (
                        opt("A human types the data in by hand"),
                        opt(
                            "AI is decision-support that surfaces patterns and forecasts, "
                            "while an accountable qualified engineer makes the final call, "
                            "especially for safety or compliance",
                            correct=True,
                        ),
                        opt("A human must be physically at every sensor"),
                        opt("The AI makes all decisions autonomously"),
                    ),
                    "The AI informs; a responsible human, equipped with explanation and "
                    "uncertainty, decides.",
                ),
                q(
                    "How can a sparse sensor network create an environmental-justice problem?",
                    (
                        opt("It cannot - sensors are neutral"),
                        opt(
                            "If sensors are sparse in poorer neighbourhoods, the model is "
                            "blind to their air quality, inheriting and amplifying the "
                            "coverage bias",
                            correct=True,
                        ),
                        opt("Sparse networks are always more accurate"),
                        opt("It only affects wealthy areas"),
                    ),
                    "Models inherit their data's gaps; unequal sensor coverage yields "
                    "unequal protection.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Where does most of the effort go in a real environmental data science project?",
                    (
                        opt("Choosing the fanciest neural network"),
                        opt(
                            "Cleaning and validating data - distinguishing sensor faults "
                            "from real events - because garbage in is a public-health risk",
                            correct=True,
                        ),
                        opt("Designing the dashboard colors"),
                        opt("Buying the most sensors"),
                    ),
                    "Cleaning and validation dominate; a clever model on bad data looks "
                    "authoritative and misleads.",
                ),
                q(
                    "Predicting whether a water sample is potable is which kind of task?",
                    (
                        opt("Regression"),
                        opt("Classification - the target is a category", correct=True),
                        opt("Forecasting"),
                        opt("Clustering"),
                    ),
                    "A categorical target (potable or not) is classification; a "
                    "continuous target would be regression.",
                ),
                q(
                    "Why must time-series forecasts use a forward-chaining (not random) split?",
                    (
                        opt("Random splits are slower"),
                        opt(
                            "A random split leaks future values into training, giving "
                            "fantasy scores; forward chaining trains on the past and tests "
                            "on later data",
                            correct=True,
                        ),
                        opt("Time series cannot be validated"),
                        opt("Forward chaining uses less memory"),
                    ),
                    "Respect time order so validation matches how forecasting really works.",
                ),
                q(
                    "Why is anomaly detection well suited to finding leaks and faults?",
                    (
                        opt("Because leaks are always labeled in advance"),
                        opt(
                            "Leaks are rare and unlabeled, so instead of training on "
                            "examples you model normal behavior and flag deviations",
                            correct=True,
                        ),
                        opt("Because it needs no data"),
                        opt("Because it eliminates false alarms entirely"),
                    ),
                    "Unsupervised anomaly detection learns normal and flags departures - "
                    "ideal when labeled failures are scarce.",
                ),
                q(
                    "What does NDVI = (NIR - RED)/(NIR + RED) measure in satellite imagery?",
                    (
                        opt("Water depth"),
                        opt(
                            "Vegetation health - high over dense forest, low over bare ground",
                            correct=True,
                        ),
                        opt("Air temperature"),
                        opt("Cloud thickness"),
                    ),
                    "NDVI tracks vegetation; a sharp drop between dates maps clearing or "
                    "deforestation.",
                ),
                q(
                    "Why mask clouds before optical satellite change detection?",
                    (
                        opt("Clouds improve image resolution"),
                        opt(
                            "Clouds differ between dates and masquerade as real surface "
                            "change, producing false detections",
                            correct=True,
                        ),
                        opt("Clouds only matter for night images"),
                        opt("Masking speeds up the download"),
                    ),
                    "Unmasked clouds create spurious change; radar (SAR) can see through "
                    "them for flood mapping.",
                ),
                q(
                    "What is the main data-quality challenge of low-cost IoT sensor networks?",
                    (
                        opt("They produce too little data"),
                        opt(
                            "Sensors drift and are affected by temperature and humidity, "
                            "so they need periodic co-location calibration against a "
                            "reference instrument",
                            correct=True,
                        ),
                        opt("They are always perfectly accurate"),
                        opt("They cannot connect to a network"),
                    ),
                    "Drift is the price of low cost; calibration and quality control make "
                    "the dense network trustworthy.",
                ),
                q(
                    "What makes a digital twin different from a plain process model?",
                    (
                        opt("It uses a different programming language"),
                        opt(
                            "It is continuously synchronized with the plant's live sensor "
                            "data, mirroring the real current state",
                            correct=True,
                        ),
                        opt("It cannot simulate anything"),
                        opt("It needs no calibration"),
                    ),
                    "The live data link lets the twin reflect the actual plant now and "
                    "run realistic what-if simulations.",
                ),
                q(
                    "What is the responsible way to communicate a model's prediction?",
                    (
                        opt("A single number with maximum confidence"),
                        opt(
                            "A point estimate with its uncertainty, the main drivers, and "
                            "a flag if the input is outside the training range",
                            correct=True,
                        ),
                        opt("Only the model's accuracy percentage"),
                        opt("Nothing - keep the model secret"),
                    ),
                    "Uncertainty, explanation, and an extrapolation flag let an "
                    "accountable human weigh the risk honestly.",
                ),
                q(
                    "What is the overarching principle of responsible environmental AI?",
                    (
                        opt("The AI should make all decisions autonomously"),
                        opt(
                            "Human-in-the-loop - AI is decision-support that surfaces "
                            "forecasts and alerts, while an accountable engineer makes the "
                            "safety- and compliance-critical call",
                            correct=True,
                        ),
                        opt("Accuracy is the only thing that matters"),
                        opt("Explainability can be skipped if accuracy is high"),
                    ),
                    "AI informs; a qualified, accountable human decides - accuracy alone "
                    "is never sufficient for public-health decisions.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

AI_FOR_ENVIRONMENTAL_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (
    _AI_FOR_ENVIRONMENTAL_ENGINEERING,
)
