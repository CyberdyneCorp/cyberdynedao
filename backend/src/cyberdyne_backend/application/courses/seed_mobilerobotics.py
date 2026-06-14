"""Academy seed content — the Mobile Robotics & Autonomy track (Beginner → Advanced).

* ``mobile-robotics-basics``        — robot types, unicycle & differential-drive kinematics, odometry & drift, sensors
* ``mobile-robotics-intermediate``  — the localization problem, Bayes filter, histogram/Markov & EKF localization, occupancy grids, particle filters
* ``mobile-robotics-advanced``      — SLAM, path planning (Dijkstra/A*/RRT/PRM), motion planning & obstacle avoidance, path tracking (pure pursuit/Stanley/MPC)

Runnable ``code`` lessons use Python (validated inline) to integrate
differential-drive odometry, drive a unicycle with (v, ω), run a 1-D histogram
Bayes filter, step a particle filter with low-variance resampling, search a grid
with A*, and steer with pure pursuit. The **equivalent MATLAB** appears as
read-only blocks. Interactive plots include a slider-driven belief/heuristic
curve. Part of the Robotics & Autonomy curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, θ, ω, Δ, ±, ², ×, °, π) in diagrams.
# ruff: noqa: RUF001, RUF003

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


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# mobile-robotics-basics
# ──────────────────────────────────────────────────────────────────────

_MR_BASICS = SeedCourse(
    slug="mobile-robotics-basics",
    title="Mobile Robotics & Autonomy — Basics",
    description=(
        "How wheeled robots move and sense: differential-drive, Ackermann, omni, "
        "tracked and legged platforms; unicycle and differential-drive kinematics "
        "(forward and inverse); odometry, dead-reckoning and why it drifts; and the "
        "sensor suite (encoders, IMU, LiDAR, cameras, GPS). With runnable Python "
        "labs, MATLAB equivalents, and an interactive trajectory plot."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Types of mobile robots",
            "10 min",
            r"""# Types of mobile robots

A **mobile robot** moves through its environment, unlike a fixed factory arm. The
**drive geometry** — how the wheels (or legs) are arranged and actuated — decides
*how* it can move, and therefore shapes every controller and planner that follows.
A handful of archetypes cover almost everything you'll meet:

- **Differential drive** — two independently driven wheels on a common axle, plus
  passive caster(s) for balance. Drive both forward → go straight; spin them
  opposite → **rotate in place**. Cheap, simple, and the workhorse of indoor robots
  (Roomba, TurtleBot, warehouse AMRs). This is our reference platform.
- **Ackermann / car-like** — front wheels **steer**, rear wheels drive (like a car).
  It **cannot turn in place** — there is a minimum turning radius — which makes
  parking and tight maneuvers hard. The model for self-driving cars and any
  fast outdoor vehicle.
- **Omnidirectional** — special wheels (**mecanum** or **omni**) let the robot
  translate in **any** direction *and* rotate **independently** — it can slide
  sideways. Wonderful maneuverability (used in some warehouse and competition
  robots) at the cost of mechanical complexity and slip.
- **Tracked** — two continuous tracks (like a tank). Skid-steer kinematics, similar
  in spirit to differential drive but with heavy slip. Excellent on rough or soft
  terrain (search-and-rescue, agriculture, planetary rovers).
- **Legged** — 2, 4, or 6 legs. Can traverse stairs, rubble and gaps no wheel can,
  but the kinematics and balance control are far harder (Spot, humanoids).

```
 differential        Ackermann (car)       omni (mecanum)
   ◯───◯              ╱◯     ◯╲              ◯ ◯
   │   │   ← drive    (steer) (drive)        ↕ ↔   ← move any direction
   ◯───◯               ◯     ◯               ◯ ◯
 turn in place      min turn radius        translate + rotate freely
```

**Holonomic vs non-holonomic** is the deep distinction. A robot is **holonomic** if
its controllable degrees of freedom equal its total degrees of freedom in the plane
(x, y, θ) — an omni robot is holonomic: it can move instantly in any direction.
Differential-drive, Ackermann and tracked robots are **non-holonomic**: they
*cannot* move sideways. A diff-drive robot can eventually reach any (x, y, θ), but
only by combining forward motion and turning — never by sliding sideways. This
constraint is what makes parallel parking hard and what every path planner for
wheeled robots must respect.

The platform you pick fixes the **kinematic model** — the equations relating wheel
or steering commands to motion — and that model is the contract between your control
software and the physical robot. We start with the two simplest and most useful
models: the **unicycle** and the **differential drive**.
""",
        ),
        _t(
            "Unicycle & differential-drive kinematics",
            "12 min",
            r"""# Unicycle & differential-drive kinematics

To control a robot we need **math that maps commands to motion**. For wheeled
ground robots the **unicycle model** is the elegant abstraction, and the
**differential-drive model** is the concrete machine that realizes it.

**The unicycle model.** Treat the robot as a point with a **heading θ**, commanded
by a **forward (linear) speed v** and a **turning (angular) rate ω**. Its pose
$(x, y, \theta)$ evolves as:

$$ \dot{x} = v\cos\theta, \qquad \dot{y} = v\sin\theta, \qquad \dot{\theta} = \omega $$

Read it directly: you always move **along your current heading** at speed v, while
your heading turns at rate ω. The non-holonomic constraint is built in — there is
**no sideways term** ($\dot{x}\sin\theta - \dot{y}\cos\theta = 0$). Almost every
planner and controller for ground robots is written in terms of (v, ω).

**The differential-drive model** is how a real two-wheel robot produces (v, ω).
Let the left/right wheels have radius $r$ and linear speeds $v_L$, $v_R$ (= $r$
times their angular speeds), separated by wheel base / track width $L$. Then:

$$ v = \frac{v_R + v_L}{2}, \qquad \omega = \frac{v_R - v_L}{L} $$

- Both wheels equal ($v_R = v_L$) → ω = 0 → **straight line**.
- Equal and opposite ($v_R = -v_L$) → v = 0 → **spin in place**.
- One wheel faster → curve, with **instantaneous radius** $R = \tfrac{L}{2}\cdot
  \tfrac{v_R + v_L}{v_R - v_L}$.

```
        v_R (right wheel)
   ┌──────●──────┐
   │      │      │   v = (v_R + v_L)/2     (how fast the body moves)
   │   <- L ->   │   ω = (v_R - v_L)/L     (how fast it turns)
   └──────●──────┘
        v_L (left wheel)         turns about a point on the wheel axis (the ICC)
```

**Forward kinematics** answers "given the wheel speeds, how does the pose move?" —
compute (v, ω), then integrate the unicycle equations. **Inverse kinematics**
answers "to achieve a desired (v, ω), what wheel speeds do I command?":

$$ v_R = v + \tfrac{\omega L}{2}, \qquad v_L = v - \tfrac{\omega L}{2} $$

That pair of formulas is what your motor controller runs every cycle: the planner
asks for (v, ω); inverse kinematics turns it into left/right wheel commands.

A subtlety: the equations assume **no wheel slip** and instantaneous speeds. Over
one small time step Δt we integrate them to update the pose — the basis of
**odometry**, next. If v and ω are constant over the step, the robot traces a
circular arc; for small Δt the simple Euler update $x \mathrel{+}= v\cos\theta\,
\Delta t$ (etc.) is accurate enough and is what most odometry code uses.

A constant (v, ω) traces a circle of **turning radius $R = v/\omega$**. Drag the
forward speed v and watch the radius scale — at fixed ω, going faster sweeps a wider
arc (and ω → 0 straightens it out, $R \to \infty$):

```plot
{"title": "Turning radius R = v/ω — drag the forward speed v", "xLabel": "turn rate ω (rad/s)", "yLabel": "turning radius R (m)", "xRange": [0.1, 2.0], "yRange": [0, 8], "controls": [{"name": "v", "label": "forward speed v (m/s)", "range": [1, 6], "step": 1, "value": 2}], "functions": [{"expr": "v / x", "label": "R = v/ω", "color": "#2563eb"}]}
```

Master these two models and you can command, simulate, and reason about any
diff-drive or unicycle robot. You'll integrate them into a trajectory next.
""",
        ),
        _code(
            "Differential-drive odometry",
            "13 min",
            r"""# ODOMETRY: integrate left/right wheel speeds into an (x, y, theta) trajectory.
# We command a sequence of wheel speeds and dead-reckon the pose with the unicycle
# update x += v*cos(theta)*dt, y += v*sin(theta)*dt, theta += omega*dt. numpy.

import numpy as np

r = 0.05          # wheel radius (m)
half_l = 0.10     # half the track width L/2 (m); L = 0.20 m
dt = 0.1          # time step (s)

# Wheel angular speeds (rad/s) over 60 steps: drive straight, then curve left.
steps = 60
wl = np.where(np.arange(steps) < 30, 10.0, 8.0)   # left wheel
wr = np.where(np.arange(steps) < 30, 10.0, 12.0)  # right wheel

# Convert to wheel linear speeds, then body (v, omega) per step.
vl = r * wl
vr = r * wr
v = (vr + vl) * 0.5                 # forward speed each step
omega = (vr - vl) / (2.0 * half_l)  # turn rate each step

# Dead-reckon the pose (straight-line numpy at module level: globals stay visible).
x = 0.0
y = 0.0
theta = 0.0
xs = [0.0]
ys = [0.0]
for i in range(steps):
    x = x + float(v[i]) * float(np.cos(theta)) * dt
    y = y + float(v[i]) * float(np.sin(theta)) * dt
    theta = theta + float(omega[i]) * dt
    xs.append(x)
    ys.append(y)

print("differential-drive odometry over %d steps:" % steps)
print("  start pose (0.000, 0.000, 0.0 deg)")
print("  final pose (%.3f, %.3f, %.1f deg)" % (x, y, float(np.degrees(theta))))
print("  path length ~ %.3f m" % float(np.sum(np.abs(v) * dt)))
print("the robot drove straight then curved left -- pose comes purely from wheels.")
""",
        ),
        _code(
            "Unicycle model driven by (v, ω)",
            "12 min",
            r"""# THE UNICYCLE MODEL: command a forward speed v and turn rate omega directly.
# Drive a constant (v, omega) -> the robot traces a perfect circle of radius v/omega.
# Then verify the radius matches the closed form. numpy.

import numpy as np

dt = 0.05
steps = 314        # ~ one full circle: heading change = steps*omega*dt ~ 2*pi

v_cmd = 0.5        # forward speed (m/s)
omega_cmd = 0.4    # turn rate (rad/s) -> circle of radius v/omega = 1.25 m

# Integrate the unicycle equations at module level.
x = 0.0
y = 0.0
theta = 0.0
xs = [0.0]
ys = [0.0]
for i in range(steps):
    x = x + v_cmd * float(np.cos(theta)) * dt
    y = y + v_cmd * float(np.sin(theta)) * dt
    theta = theta + omega_cmd * dt
    xs.append(x)
    ys.append(y)

xa = np.array(xs)
ya = np.array(ys)

# A constant (v, omega) gives a circle; recover its radius from the trajectory.
radius_theory = v_cmd / omega_cmd
cx = float(np.mean(xa))
cy = float(np.mean(ya))
radius_measured = float(np.mean(np.sqrt((xa - cx) ** 2 + (ya - cy) ** 2)))

print("unicycle driven by constant (v=%.2f m/s, omega=%.2f rad/s):" % (v_cmd, omega_cmd))
print("  theoretical circle radius v/omega = %.3f m" % radius_theory)
print("  measured radius from trajectory   = %.3f m" % radius_measured)
print("  total heading change = %.1f deg over %.1f s" % (float(np.degrees(theta)), steps * dt))
print("constant (v, omega) -> a circle; that is the unicycle model in one picture.")
""",
        ),
        _t(
            "Odometry, dead-reckoning & drift",
            "11 min",
            r"""# Odometry, dead-reckoning & drift

**Odometry** is estimating where the robot is by **integrating its own motion** —
counting wheel rotations (and/or IMU readings) and summing them up. It's the most
basic form of **dead-reckoning**: "I started here, I went this far at this heading,
so I must be there." It needs no external infrastructure, runs at high rate, and is
the backbone of every robot's short-term pose estimate.

From the encoders you measure how far each wheel turned in the last step (Δs per
wheel), form the body displacement and rotation, and update the pose:

$$ \Delta s = \frac{\Delta s_R + \Delta s_L}{2}, \quad \Delta\theta = \frac{\Delta s_R - \Delta s_L}{L} $$
$$ x \mathrel{+}= \Delta s\cos\theta, \quad y \mathrel{+}= \Delta s\sin\theta, \quad \theta \mathrel{+}= \Delta\theta $$

This is exactly the integration from the last labs, fed by **measured** wheel motion
instead of commanded speeds.

**Why it drifts.** Odometry **accumulates error**. Every step's estimate is built on
the previous one, so small errors never wash out — they **compound and grow without
bound**. The error sources:

- **Systematic errors** — wrong wheel radius, unequal wheels, wrong track width L.
  These bias *every* step the same way, so the path slowly bends. They can be
  **calibrated out** (e.g. the UMBmark figure-eight test).
- **Non-systematic errors** — **wheel slip** (the killer), bumps, uneven floors,
  picking the robot up. Random and unpredictable; calibration can't fix them.

```
   truth  ●────────────────────────────●  (where the robot really is)
                          ╱
 odometry  ●─────────────╱   (estimate drifts away — error grows with distance)
                        ↑ heading error rotates ALL future motion
```

**Heading error is the worst.** A small error in θ rotates **every subsequent
displacement**, so a tiny angular bias becomes a large position error far down the
path — position error from a heading bias grows roughly **linearly with distance
travelled**. This is why a robot that "knows" it drove in a straight line can end up
metres off after a long run.

**The fundamental limitation:** dead-reckoning is an **open-loop** estimate with no
reference to the outside world, so its uncertainty only ever **grows**. It's
excellent over **short** distances and **high rate**, terrible over **long** runs.
The cure is to **fuse** it with sensors that observe the environment (LiDAR, camera,
GPS) to *correct* the drift — which is exactly **localization** (next course). The
mental model for the whole field: **odometry predicts, sensing corrects**. Knowing
*why and how fast* odometry drifts tells you how often you must correct it.

The same dead-reckoning update in **MATLAB** (for the MATLAB REPL):

```matlab
L = 0.20; dsR = 0.011; dsL = 0.010;   % per-step wheel arc lengths (m)
pose = [0; 0; 0];                       % x, y, theta
for k = 1:50
    ds = (dsR + dsL)/2;
    dth = (dsR - dsL)/L;
    pose(1) = pose(1) + ds*cos(pose(3));
    pose(2) = pose(2) + ds*sin(pose(3));
    pose(3) = pose(3) + dth;
end
disp('final pose (x y theta):'); disp(pose')
```

You'll see drift bend a path next, when we add real sensors to fight it.
""",
        ),
        _t(
            "Sensors for mobile robots",
            "11 min",
            r"""# Sensors for mobile robots

A robot that only dead-reckons drifts forever; to correct itself it must **sense the
world**. Each sensor has a characteristic strength and weakness, and good autonomy
comes from **fusing** complementary ones (next course). The core suite:

- **Wheel encoders** — measure wheel rotation → the raw input to **odometry**. High
  rate, cheap, accurate per step, but **drift** (slip, calibration). Proprioceptive
  (they sense the robot, not the world).
- **IMU (gyroscope + accelerometer)** — measures **angular rate** and **linear
  acceleration**. The gyro gives excellent **short-term heading** (far better than
  wheel-derived θ), but **integrating drift** (especially the accelerometer →
  position) makes it unusable alone over time. Fused with encoders it sharpens
  heading.
- **LiDAR** — fires laser pulses and times the return to build a precise **range
  scan** (2-D) or **point cloud** (3-D) of surrounding geometry. The gold standard
  for **mapping and localization** (great accuracy, works in the dark), but
  expensive and degraded by rain/dust/glass.
- **Cameras** — rich, cheap, dense data; enable **visual odometry**, **VSLAM**,
  object/lane detection and recognition. Passive and information-rich, but sensitive
  to **lighting**, textureless scenes, and they need heavy computation; a single
  camera gives no absolute scale (stereo or motion does).
- **GPS / GNSS** — gives an **absolute** global position (no drift!), the perfect
  complement to odometry's drift. But it's **coarse** (metres; cm with RTK),
  **slow**, and **fails indoors / in urban canyons / under foliage**. Outdoor only.
- **Sonar / ultrasonic, bump & cliff sensors** — cheap, short-range proximity and
  contact detection for obstacle avoidance and safety.

```
 SENSOR        gives            strength            weakness
 encoders      wheel motion     fast, cheap         drifts (odometry)
 IMU           rate, accel      great short-term θ  drifts when integrated
 LiDAR         range / cloud    precise geometry    cost; rain/glass
 camera        images           rich, cheap         lighting; compute; no scale
 GPS           global position  no drift, absolute  coarse, slow, no indoors
```

**The complementary-fusion idea** is the heart of robotic perception. **No single
sensor is enough.** Encoders + IMU give a smooth, high-rate but drifting pose
(*relative*); LiDAR/camera/GPS give slower, noisier but **drift-free** fixes
(*absolute*). Combine them — **odometry predicts between fixes, exteroceptive
sensors correct the drift** — and you get an estimate that is *both* smooth and
bounded. The mathematical machinery that does this fusing optimally (the Bayes
filter, Kalman/particle filters) is the entire **localization** course that follows.

Two more practical truths: every sensor reading is **noisy** (so we reason with
**probability**, not certainty — the next course's whole premise), and sensors must
be **time-synchronized and calibrated** (extrinsics: where each sensor sits on the
robot) before fusion makes sense. Pick sensors that **fail differently** so that
where one is weak, another is strong — that redundancy is what makes autonomy
robust. Next: turning these noisy readings into a confident estimate of *where the
robot is*.
""",
        ),
        quiz_lesson(
            "Quiz: Robot Models, Odometry & Sensors",
            (
                q(
                    "What makes a differential-drive robot non-holonomic?",
                    (
                        opt(
                            "It cannot move sideways — only forward/back and turn — so it reaches arbitrary (x,y,θ) only by combining motions",
                            correct=True,
                        ),
                        opt("It has fewer than three wheels"),
                        opt("It can slide in any direction instantly"),
                        opt("It cannot rotate in place"),
                    ),
                    "Non-holonomic = controllable DOF < total DOF: no sideways term in the kinematics. An omni (holonomic) robot can translate any direction; diff-drive cannot.",
                ),
                q(
                    "In the differential-drive model, how are body speed v and turn rate ω formed from wheel speeds?",
                    (
                        opt(
                            "v = (v_R + v_L)/2 and ω = (v_R − v_L)/L",
                            correct=True,
                        ),
                        opt("v = v_R − v_L and ω = v_R + v_L"),
                        opt("v = v_R · v_L and ω = v_R / v_L"),
                        opt("v = L·(v_R + v_L) and ω = (v_R + v_L)/2"),
                    ),
                    "The average of the wheel speeds is forward speed; their difference over the track width L is the turn rate. Equal speeds → straight; opposite → spin in place.",
                ),
                q(
                    "In the unicycle model, what path results from a constant (v, ω) with ω ≠ 0?",
                    (
                        opt(
                            "A circle of radius v/ω",
                            correct=True,
                        ),
                        opt("A straight line"),
                        opt("A figure-eight"),
                        opt("It stays in place"),
                    ),
                    "ẋ=v cosθ, ẏ=v sinθ, θ̇=ω: constant v and ω turn the heading uniformly while moving at speed v → a circular arc of radius v/ω.",
                ),
                q(
                    "Why does wheel odometry drift, and which error is worst?",
                    (
                        opt(
                            "It integrates motion open-loop, so errors accumulate; a heading (θ) error is worst because it rotates all future displacement, growing position error with distance",
                            correct=True,
                        ),
                        opt("It drifts only because of GPS interference"),
                        opt("Position errors are worse than heading errors"),
                        opt("It does not drift if wheels are calibrated"),
                    ),
                    "Dead-reckoning has no external reference, so uncertainty only grows. A small θ bias rotates every later step, so heading error dominates over distance.",
                ),
                q(
                    "Why fuse encoders/IMU with LiDAR/camera/GPS instead of using one sensor?",
                    (
                        opt(
                            "Encoders/IMU are smooth and fast but drift (relative); LiDAR/camera/GPS are slower/noisier but drift-free (absolute) — fusing gives smooth AND bounded estimates",
                            correct=True,
                        ),
                        opt("Because more sensors always means less computation"),
                        opt("GPS works perfectly everywhere, so the others are backups"),
                        opt("A single camera already gives absolute, drift-free pose with scale"),
                    ),
                    "Complementary fusion: odometry predicts between fixes; exteroceptive sensors correct the drift. Pick sensors that fail differently for robustness.",
                ),
                q(
                    "Which platform CAN translate sideways without first rotating?",
                    (
                        opt(
                            "An omnidirectional (mecanum/omni-wheel) robot — it is holonomic",
                            correct=True,
                        ),
                        opt("An Ackermann (car-like) robot"),
                        opt("A differential-drive robot"),
                        opt("A tracked (skid-steer) robot"),
                    ),
                    "Only omnidirectional drives are holonomic in the plane; Ackermann, differential and tracked robots are all non-holonomic and cannot move directly sideways.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# mobile-robotics-intermediate
# ──────────────────────────────────────────────────────────────────────

_MR_INTERMEDIATE = SeedCourse(
    slug="mobile-robotics-intermediate",
    title="Mobile Robotics & Autonomy — Intermediate",
    description=(
        "Knowing where you are despite noise and drift: the localization problem, "
        "belief and the recursive Bayes filter, histogram/Markov localization, the "
        "EKF, occupancy-grid mapping, and the particle filter (Monte-Carlo "
        "localization) with low-variance resampling. With runnable Bayes-filter and "
        "particle-filter labs and an interactive belief plot."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The localization problem & belief",
            "10 min",
            r"""# The localization problem & belief

**Localization** is the question that defines mobile robotics: *given a map, noisy
sensors, and noisy motion, where am I?* Odometry alone drifts without bound (last
course); localization fights that drift by **fusing motion with observations of the
world** — and it does so in the language of **probability**, because every
measurement and every move is uncertain.

**The key shift in mindset: track a *belief*, not a point.** Instead of claiming
"the robot is at exactly x", we maintain a **probability distribution over all
possible poses** — the **belief** $bel(x)$. A sharp, peaked belief means "I'm
confident"; a flat, spread-out belief means "I'm lost." This is honest: the robot
*knows what it doesn't know*, and acts accordingly.

```
  lost (flat belief)             confident (peaked belief)
  prob │▁▁▂▂▂▂▂▂▁▁              prob │      ▁██▁
       └───────────  pose            └──────────────  pose
   could be anywhere                  almost certainly here
```

Three flavours of the problem, in increasing difficulty:

- **Position tracking** — you know roughly where you start; just keep the (single,
  peaked) belief updated as you move. The easy, common case.
- **Global localization** — you have **no idea** where you start (the
  *wake-up / kidnapped robot* problem); the belief starts flat over the whole map
  and must **converge** to the truth from scratch. Much harder — needs a
  representation that can hold *many* hypotheses at once.
- **Failure recovery** — detect that you've become lost (belief went wrong) and
  re-localize. Robustness matters in the real world.

**Two streams of information** drive the belief, and they push it in opposite
directions:

- **Motion (control u)** — the robot moves; this **shifts** the belief and, because
  motion is noisy, **spreads it out** (uncertainty grows). The *prediction*.
- **Measurements (observation z)** — the robot senses; this **sharpens** the belief
  toward poses consistent with what it saw (uncertainty shrinks). The *correction*.

Localization is the perpetual tug-of-war between these two: **moving blurs the
belief, sensing focuses it.** The whole course is about doing this fusion
*recursively* and *optimally*. The mathematical engine that combines motion and
measurement to update a belief is the **Bayes filter** — the foundation of every
method that follows (histogram, Kalman/EKF, particle filter). Next.
""",
        ),
        _t(
            "The Bayes filter",
            "12 min",
            r"""# The Bayes filter

The **Bayes filter** is the single recursive algorithm underneath *every*
localization method — histogram, Kalman, EKF, particle filter are all just
different ways of representing and computing the same two steps. Master it once and
the rest are implementations.

It maintains the **belief** $bel(x_t)$ — the probability distribution over the pose
at time t — and updates it **recursively** as new control $u_t$ and measurement
$z_t$ arrive. Each cycle has **two steps**:

**1. Prediction (motion update).** Apply the motion model to push the belief forward,
accounting for where each possible previous pose would have moved:

$$ \overline{bel}(x_t) = \int p(x_t \mid u_t, x_{t-1})\, bel(x_{t-1})\; dx_{t-1} $$

This is a **convolution** of the old belief with the motion's noise. It **spreads
out** (uncertainty grows) because motion is noisy. The bar $\overline{bel}$ marks
the *predicted* (pre-measurement) belief.

**2. Correction (measurement update).** Apply Bayes' rule: reweight the predicted
belief by how likely the actual measurement is at each pose:

$$ bel(x_t) = \eta\; p(z_t \mid x_t)\; \overline{bel}(x_t) $$

where $p(z_t \mid x_t)$ is the **measurement model** (sensor likelihood) and $\eta$
**normalizes** so the belief sums to 1. This **sharpens** the belief toward poses
consistent with the observation.

```
   bel(x_{t-1})  --PREDICT (move, blur)-->  bel-bar(x_t)
                                                │
                          measurement z_t  ──> CORRECT (sense, sharpen, normalize)
                                                │
                                                v
                                           bel(x_t)   --> next cycle
```

**Two assumptions make this tractable** (the **Markov assumption**):

- The **next state depends only on the current state and control** (not the full
  history) — so we carry only $bel(x_t)$, not every past pose.
- Measurements depend only on the **current state**.

These let the filter run in **constant memory and time per step**, recursively,
forever — it never stores the past, only the current belief.

**The recipe in words:** *predict* with the motion model (move and blur the
belief), then *correct* with the measurement model (reweight by sensor likelihood
and renormalize) — repeat. Predict, correct, predict, correct.

Why so many algorithms for one filter? Because the integral and the product are
**intractable in general** — the methods differ in how they **represent** the
belief:

- **Histogram / grid** — belief = probabilities over a **discrete grid** (exact but
  scales badly with dimensions). *Next lab.*
- **Kalman / EKF** — belief = a **Gaussian** (mean + covariance); elegant and fast
  for unimodal, near-linear problems. *Next lesson.*
- **Particle filter** — belief = a **set of samples**; flexible, multi-modal,
  handles global localization. *Later lab.*

Every one is the Bayes filter; they just trade exactness, speed, and the kinds of
belief shapes they can represent. You'll implement the discrete (histogram) Bayes
filter next.
""",
        ),
        _t(
            "Histogram & Markov localization",
            "11 min",
            r"""# Histogram & Markov localization

**Histogram localization** (a.k.a. **Markov localization** in its grid form) is the
Bayes filter made **concrete and discrete**: chop the space of poses into a grid of
cells, store a probability for each cell, and run predict/correct directly on that
array. It's the clearest way to *see* a belief move and sharpen, and it's the
foundation for understanding everything fancier.

**Representation.** The belief is just a list (or grid) of numbers — $p_i$ = the
probability the robot is in cell $i$ — that always **sum to 1**. For a robot on a
1-D corridor with N cells, that's an N-element array.

**The two steps on a grid:**

- **Prediction (move).** Shift the belief by the motion, blurred by motion noise.
  In 1-D, moving "one cell to the right" with some slip becomes a **convolution**:
  $\overline{p}_i = \sum_k p_{i-k}\, q_k$ where $q_k$ is the probability the motion
  actually moved k cells. This **spreads** the belief.
- **Correction (sense).** Multiply each cell's probability by the **measurement
  likelihood** there, then renormalize: $p_i = \eta\, L_i\, \overline{p}_i$. If the
  robot senses "a door" and only some cells are near doors, those cells get boosted.
  This **sharpens** the belief.

```
 corridor cells:   0   1   2   3   4   5   6   7
 belief (flat):   .12 .12 .12 .12 .12 .12 .12 .12   <- lost
   sense 'door' at cells 2 and 5 (likelier there):
 after correct:   .03 .03 .35 .06 .06 .35 .06 .06   <- two hypotheses!
   move right, sense again, repeat -> converges to one peak
```

**The headline strength: it handles multi-modality and global localization
natively.** Because every cell holds its own probability, the belief can have
**several peaks at once** — exactly what you need when the robot is lost and several
places look alike (two identical doors). Over a few sense/move cycles the ambiguity
resolves and the belief **collapses to a single peak**. A Gaussian/Kalman filter
*cannot* do this (it's stuck with one peak); the histogram filter can.

**The cost: it scales badly.** A grid over $(x, y, \theta)$ explodes:
**fine resolution × 3 dimensions = millions of cells** to update every step. The
**curse of dimensionality** makes pure grid localization impractical beyond small or
low-dimensional problems. That motivates the two efficient successors:

- **Kalman/EKF** — represent the (single) peak as a **Gaussian** → tiny, fast, but
  unimodal. *Next.*
- **Particle filter** — put probability only **where it matters** via samples →
  multi-modal *and* scalable. *Later.*

The shape of the corrected belief depends on **sensor confidence**. Drag the
confidence k below: a confident sensor (high k) produces a **sharp** belief peak
(low uncertainty), a vague sensor a **broad** one — the same effect the correction
step has on a real grid:

```plot
{"title": "Belief over cells after a measurement — drag the sensor confidence k", "xLabel": "cell position", "yLabel": "belief (normalised)", "xRange": [0, 10], "yRange": [0, 1.05], "controls": [{"name": "k", "label": "sensor confidence k", "range": [1, 8], "step": 1, "value": 3}], "functions": [{"expr": "exp(-0.5 * pow(k * (x - 5) / 3, 2))", "label": "belief peak at cell 5", "color": "#2563eb"}]}
```

The histogram filter is the **conceptual** workhorse: it shows the Bayes filter
working on a real array of numbers, demonstrates global localization and
multi-modal belief, and exposes exactly why we need smarter representations.

The discrete sense/move update in **MATLAB** (for the MATLAB REPL):

```matlab
world = [0 1 0 0 1 0 1 0 0 0];   % 1 = door
belief = ones(1, 10) / 10;        % flat: lost
z = 1;                            % sensed a door
like = world*0.9 + (1 - world)*0.1;   % P(hit)=0.9 where door matches
if z == 0, like = 1 - like; end
belief = like .* belief;
belief = belief / sum(belief);    % CORRECT: normalise
belief = 0.8*circshift(belief, 1) + 0.2*belief;   % PREDICT: move +1, slip
disp('belief after one sense/move:'); disp(belief)
```

You'll build the full filter next — and watch a flat belief converge to a confident
peak.
""",
        ),
        _code(
            "1-D histogram Bayes localization",
            "14 min",
            r"""# HISTOGRAM (MARKOV) LOCALIZATION on a 1-D ring of cells. The world has 'doors'
# at known cells; the robot senses door/no-door (noisily) and moves right one cell
# each step. Start LOST (flat belief) -> watch it converge to a single peak. numpy.

import numpy as np

# A cyclic corridor of 10 cells; 1 = door, 0 = wall, at known locations.
world = np.array([0, 1, 0, 0, 1, 0, 1, 0, 0, 0], dtype=float)
n = 10

# Sensor model: P(measure correctly) = 0.9, P(error) = 0.1.
p_hit = 0.9
p_miss = 0.1

# Motion model: commanded +1 cell, but noisy: 0.8 lands right, 0.1 under, 0.1 over.
p_exact = 0.8
p_under = 0.1
p_over = 0.1

# Belief starts FLAT -> the robot is globally lost.
belief = np.ones(n) / n

# The true robot starts at cell 0; it SENSES then MOVES +1 each step. The readings
# below are taken at true cells 0,1,2,3,4 (doors at 1,4,6) -> [0, 1, 0, 0, 1].
measurements = [0, 1, 0, 0, 1]   # what the (noisy) sensor reports each step
true_cell = 0

print("histogram localization on %d cells, doors at %s" % (n, list(np.flatnonzero(world))))
print("start: flat belief, max prob = %.3f at cell %d" % (belief.max(), int(belief.argmax())))

for z in measurements:
    # CORRECT (sense): boost cells whose door-state matches the reading.
    like = np.where(world == z, p_hit, p_miss)
    belief = like * belief
    belief = belief / belief.sum()

    # PREDICT (move +1 cell, with slip): circular convolution of the 3-tap kernel.
    belief = (
        p_exact * np.roll(belief, 1)
        + p_under * np.roll(belief, 0)
        + p_over * np.roll(belief, 2)
    )
    true_cell = (true_cell + 1) % n

best = int(belief.argmax())
print("after %d sense/move cycles:" % len(measurements))
print("  belief peak = %.3f at cell %d (true cell %d)" % (belief.max(), best, true_cell))
print("  belief: %s" % np.round(belief, 3).tolist())
print("a flat (lost) belief converged toward the true cell -- Bayes filter at work.")
""",
        ),
        _t(
            "EKF localization & occupancy grids",
            "12 min",
            r"""# EKF localization & occupancy grids

Two practical engines power most real systems: the **Extended Kalman Filter** for
*tracking* a pose efficiently, and the **occupancy grid** for *building the map* the
robot localizes against.

**The Kalman filter (KF)** is the Bayes filter when the belief is a **Gaussian**
(mean $\mu$ + covariance $\Sigma$) and the models are **linear** with Gaussian
noise. Then the two Bayes steps have a beautiful **closed form** — no integrals,
just matrix algebra — and the KF is **provably optimal**:

- **Predict:** $\mu^- = A\mu + Bu$, $\;\Sigma^- = A\Sigma A^\top + Q$. (Move the
  mean; **grow** the covariance by process noise Q.)
- **Update:** compute the **Kalman gain** $K = \Sigma^- H^\top (H\Sigma^- H^\top +
  R)^{-1}$, then $\mu = \mu^- + K(z - H\mu^-)$, $\;\Sigma = (I - KH)\Sigma^-$.
  (Correct toward the measurement; **shrink** the covariance.) The gain K balances
  trust between the prediction and the sensor (noise R).

**Why the EXTENDED KF?** Robot motion ($\dot\theta = \omega$, sines and cosines) and
sensor models (range, bearing) are **nonlinear** — a plain KF doesn't apply. The
**EKF** handles this by **linearizing** the models each step with their **Jacobians**
(first-order Taylor expansion) around the current estimate, then applying the KF
equations. It's the workhorse of robot localization and **EKF-SLAM** (next course).

```
   GAUSSIAN belief:  N(mu, Sigma)
   predict ─► mu moves, Sigma GROWS  (motion adds uncertainty)
   update  ─► mu pulled toward z, Sigma SHRINKS  (measurement removes it)
   K (Kalman gain): how much to trust the sensor vs the prediction
```

**Strengths and limits.** The EKF is **fast and compact** (just a mean and a
covariance) — ideal for **position tracking**. But the Gaussian is **unimodal**: it
holds **one** hypothesis, so it **can't do global localization** or recover from a
big "kidnap" the way a histogram or particle filter can. And linearization errors
can make it **diverge** if the nonlinearity is strong or the initial guess is poor.

**Occupancy-grid mapping.** Where does the *map* come from? An **occupancy grid**
divides the environment into cells, each holding the **probability that the cell is
occupied** (obstacle) vs free. As the robot drives and scans (LiDAR/sonar), it
updates each cell from the ranges — typically in **log-odds**, which turns Bayesian
updates into simple **addition**:

$$ \ell_i \mathrel{+}= \text{inverse-sensor-model}(z, \text{cell } i) $$

- A beam that **passes through** a cell → that cell is likely **free** (subtract).
- A beam that **stops at** a cell → that cell is likely **occupied** (add).

Cells are assumed **independent**, so the whole map is just an array of log-odds,
updated cheaply scan by scan. The result is the **2-D map** (free / occupied /
unknown) that path planners (next course) search over and that localization matches
scans against.

```
  occupancy grid (■ occupied, · free, ? unknown):
   ■ ■ ■ ■ ■ ■
   ■ · · · · ■      built by ray-casting each LiDAR scan into cells:
   ■ · ? · · ■        through  -> free,  endpoint -> occupied
   ■ · · · R ■      R = robot
   ■ ■ ■ ■ ■ ■
```

Together these are the backbone of practical autonomy: the **EKF tracks the pose**
(efficiently, when you start localized), and the **occupancy grid is the map** it
moves and plans in. Their limitation — the single-hypothesis Gaussian — is exactly
what the **particle filter** overcomes next.
""",
        ),
        _t(
            "Particle filters & Monte-Carlo localization",
            "12 min",
            r"""# Particle filters & Monte-Carlo localization

The **particle filter** (a.k.a. **Monte-Carlo Localization, MCL**) is the Bayes
filter with the most flexible representation of all: the belief is a **cloud of
samples** ("particles"), each a candidate pose, with a weight. It's **multi-modal**
(solves global localization), handles **arbitrary nonlinear** motion/sensor models,
and is wonderfully intuitive — the modern default for robot localization.

**Each particle is a guess** $x^{[m]}$ at the pose; the **density of particles**
*is* the belief — many particles where the robot probably is, few where it probably
isn't. With M particles you approximate any distribution shape you like (no Gaussian
assumption). The cycle has **three steps**:

- **1. Predict (sample motion).** Move **every** particle through the motion model,
  adding random noise — each particle takes a slightly different noisy step. This
  spreads the cloud (uncertainty grows). *Replaces the Bayes prediction integral with
  sampling.*
- **2. Weight (measure).** For each particle, compute how well its pose **explains
  the actual measurement**: $w^{[m]} = p(z \mid x^{[m]})$. Particles consistent with
  the sensor get **high weight**; inconsistent ones get low weight. *This is the
  measurement update.*
- **3. Resample.** Draw a new set of M particles **with replacement**, in proportion
  to the weights. High-weight particles get **copied** (often several times);
  low-weight ones **die out**. The cloud **concentrates** where the evidence points,
  then the weights reset to uniform. *This focuses computation where it matters.*

```
 PREDICT          WEIGHT              RESAMPLE
  · ·  ·          · ·  ·             survivors cluster:
 ·  ·· ·   move  ·  ◉◉ ·   measure    ◉◉◉
 · ·  ··  noise  · ◉◉◉ ·  -> weights  ◉◉◉◉   (low-weight particles culled,
  ·· ·            ·· ·                 ◉◉      high-weight copied)
```

**Why resampling — and why "low-variance"?** Without resampling, after a few steps
nearly all weight lands on one particle and the rest are wasted (**degeneracy**).
Resampling fixes that, but **naive** resampling (M independent draws) adds variance
and can randomly kill good particles. **Low-variance (systematic) resampling** is the
standard fix: pick **one** random start $r \in [0, 1/M)$ and step through the
cumulative weights at even intervals $r, r+1/M, r+2/M, \dots$ — picking one particle
per slice. It's **O(M)**, uses a **single** random number, samples evenly, and is far
less noisy than independent draws. (Implemented in the next lab.)

**Strengths vs the EKF:**

```
 EKF             single Gaussian   fast, compact   unimodal; can't re-localize
 particle filter sample cloud      multi-modal,    cost ~ M particles;
                                   global, nonlinear   needs enough particles
```

**Practical knobs:** **more particles** → better accuracy but more compute (a real
trade-off); **adaptive** schemes (KLD-sampling) vary M with uncertainty — many
particles when lost, few when confident. A dash of **random particles** each step
guards against the **kidnapped-robot** problem and **particle deprivation**
(running out of particles near the truth). Garbage motion/sensor models break it, as
with any Bayes filter.

The particle filter is where the whole course lands: the Bayes filter, represented
by samples, with prediction = sampling, correction = weighting, and resampling to
stay efficient — giving robust **global** localization on real, nonlinear robots.
You'll implement one step, including low-variance resampling, next.
""",
        ),
        _code(
            "Particle filter with low-variance resampling",
            "15 min",
            r"""# A PARTICLE FILTER step on a 1-D line: M particles guess the robot's position.
# PREDICT (noisy move) -> WEIGHT by a range measurement -> LOW-VARIANCE RESAMPLE.
# Randomness comes from a module-level LCG (no 'random' module). numpy.

import numpy as np

m = 200          # number of particles
steps = 8        # filter iterations
true_x = 2.0     # the robot's true starting position (unknown to the filter)
move = 1.0       # commanded move per step (+1.0 m)
move_noise = 0.20
sensor_noise = 0.5

# LCG: pre-generate enough uniforms. Init uses m (initial spread); each step uses
# 2*m (motion jitter) + 1 (resample start). Buffer = m + steps*(2*m + 1) + margin.
needed = m + steps * (2 * m + 1) + 100
state = 12345
rnd = []
for i in range(needed):
    state = (1103515245 * state + 12345) % 2147483648
    rnd.append(state / 2147483648.0)

# Particles spread uniformly over [0, 10) -> globally uncertain at the start.
particles = np.array([rnd[i] * 10.0 for i in range(m)])  # reuse first m uniforms
pos = m

print("particle filter: %d particles, true start x=%.1f" % (m, true_x))
for t in range(steps):
    # PREDICT: move every particle by 'move' plus Gaussian-ish noise.
    # Box-Muller from two LCG uniforms -> a normal-ish jitter, straight-line numpy.
    u1 = np.array([rnd[pos + 2 * j] for j in range(m)])
    u2 = np.array([rnd[pos + 2 * j + 1] for j in range(m)])
    pos = pos + 2 * m
    jitter = np.sqrt(-2.0 * np.log(u1 + 1e-12)) * np.cos(2.0 * np.pi * u2)
    particles = particles + move + move_noise * jitter
    true_x = true_x + move

    # WEIGHT: a range sensor measures true_x (noisy); weight by Gaussian likelihood.
    z = true_x  # use the clean reading for a deterministic, readable lab
    weights = np.exp(-0.5 * ((particles - z) / sensor_noise) ** 2)
    weights = weights / weights.sum()

    # LOW-VARIANCE (systematic) RESAMPLE: one random start, even strides.
    cumsum = np.cumsum(weights)
    r0 = rnd[pos] / m
    pos = pos + 1
    new_particles = []
    idx = 0
    for k in range(m):
        thresh = r0 + k * (1.0 / m)
        while thresh > cumsum[idx]:
            idx = idx + 1
        new_particles.append(particles[idx])
    particles = np.array(new_particles)

estimate = float(np.mean(particles))
spread = float(np.std(particles))
print("after %d steps: estimate x=%.3f, true x=%.3f, spread=%.3f"
      % (steps, estimate, true_x, spread))
print("the cloud tracked the robot and tightened -- low-variance resampling at work.")
""",
        ),
        quiz_lesson(
            "Quiz: Localization, Bayes & Particle Filters",
            (
                q(
                    "What are the two steps of the Bayes filter?",
                    (
                        opt(
                            "Prediction (motion model: shift and blur the belief) and Correction (measurement model: reweight by sensor likelihood and normalize)",
                            correct=True,
                        ),
                        opt("Integration and differentiation"),
                        opt("Encoding and decoding"),
                        opt("Sampling and rejecting"),
                    ),
                    "Predict moves/blurs the belief (uncertainty grows); correct sharpens it toward poses consistent with z. Every localizer is this loop.",
                ),
                q(
                    "Why represent the robot's position as a belief (distribution) rather than a single point?",
                    (
                        opt(
                            "Motion and sensors are noisy; a distribution honestly captures uncertainty and can hold multiple hypotheses (key for global localization)",
                            correct=True,
                        ),
                        opt("To use more memory on purpose"),
                        opt("Because robots cannot measure position at all"),
                        opt("Points are illegal in probability"),
                    ),
                    "A peaked belief = confident, flat = lost; multi-modal beliefs hold several hypotheses when the robot is globally lost among look-alike places.",
                ),
                q(
                    "What can a histogram/particle filter do that a Kalman/EKF cannot?",
                    (
                        opt(
                            "Represent a multi-modal belief (several hypotheses) and perform global localization / kidnapped-robot recovery",
                            correct=True,
                        ),
                        opt("Run faster with less memory"),
                        opt("Guarantee optimality for linear-Gaussian systems"),
                        opt("Avoid any need for a motion model"),
                    ),
                    "The EKF's Gaussian is unimodal — one hypothesis. Grid/particle representations hold many peaks, enabling global localization the EKF can't.",
                ),
                q(
                    "Why does the EKF linearize the motion and measurement models?",
                    (
                        opt(
                            "Robot motion and sensors are nonlinear, so the EKF uses Jacobians (first-order Taylor) each step to apply the linear Kalman equations",
                            correct=True,
                        ),
                        opt("To make the belief multi-modal"),
                        opt("Because linear models are always exact"),
                        opt("To avoid computing a Kalman gain"),
                    ),
                    "The plain KF needs linear models; the EKF linearizes nonlinear ones around the current estimate. Strong nonlinearity or a bad init can make it diverge.",
                ),
                q(
                    "In a particle filter, what does resampling accomplish?",
                    (
                        opt(
                            "Draw a new particle set in proportion to weights — copying high-weight particles and culling low-weight ones — to fight degeneracy and focus computation",
                            correct=True,
                        ),
                        opt("It adds a fixed amount to every particle's weight"),
                        opt("It deletes the measurement"),
                        opt("It converts particles to a single Gaussian"),
                    ),
                    "Without resampling, weight collapses onto one particle (degeneracy). Resampling concentrates particles where evidence points; weights then reset uniform.",
                ),
                q(
                    "Why prefer low-variance (systematic) resampling over naive independent draws?",
                    (
                        opt(
                            "It uses a single random start with even strides — O(M), lower variance, and is less likely to randomly kill good particles",
                            correct=True,
                        ),
                        opt("It needs M independent random numbers per step"),
                        opt("It increases the spread of the particle cloud"),
                        opt("It only works for Gaussian beliefs"),
                    ),
                    "Systematic resampling steps through the cumulative weights at fixed intervals from one random offset r∈[0,1/M): even coverage, O(M), far less sampling noise.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# mobile-robotics-advanced
# ──────────────────────────────────────────────────────────────────────

_MR_ADVANCED = SeedCourse(
    slug="mobile-robotics-advanced",
    title="Mobile Robotics & Autonomy — Advanced",
    description=(
        "Mapping, planning, and driving the path: SLAM (EKF-SLAM, pose-graph, loop "
        "closure); path planning (Dijkstra, A*, RRT/RRT*, PRM); motion planning and "
        "obstacle avoidance (potential fields, dynamic window); and path tracking "
        "(pure pursuit, Stanley, MPC). With a runnable A* grid search and "
        "pure-pursuit steering lab plus an interactive heuristic/cost plot."
    ),
    level="Advanced",
    lessons=(
        _t(
            "SLAM: mapping while localizing",
            "12 min",
            r"""# SLAM: mapping while localizing

So far the robot localized **against a known map**. But what if there is **no map**?
**SLAM — Simultaneous Localization And Mapping** — is the robot building a map *and*
localizing within it **at the same time**, from scratch. It's the cornerstone of
autonomous robots, AR headsets, and self-driving cars exploring new places.

**The chicken-and-egg problem:** to build a map you need to know where you are; to
know where you are you need a map. SLAM solves both **jointly** — and the magic is
that the **errors are correlated**: a landmark's position error and the robot's pose
error are coupled, so observing landmarks **constrains** the pose and vice-versa.
The estimate of the map and the path co-improve.

**Two dominant formulations:**

- **EKF-SLAM (filtering).** Extend the EKF (last course): the **state vector holds
  the robot pose *and* every landmark's position**, with one big joint covariance.
  Each observation updates the whole state, capturing the robot↔landmark
  correlations. Elegant, but the covariance is **N×N for N landmarks** → **O(N²)**
  per update, so it doesn't scale to large maps, and linearization errors
  accumulate.
- **Graph-based / pose-graph SLAM (smoothing).** Build a **graph**: **nodes** are
  robot poses (and/or landmarks), **edges** are constraints from odometry and
  measurements ("pose B is ≈ this transform from pose A"). Then **optimize** all
  poses at once to best satisfy the constraints (a sparse nonlinear least-squares
  problem: g2o, GTSAM, Ceres). This is the **modern standard** — sparse, scalable,
  and accurate.

```
  pose-graph SLAM:
   (x0)──odom──(x1)──odom──(x2)──odom──(x3)
     ╲                                  ╱
      ╲────────── loop closure ────────╱   "I've been here before!"
   nodes = poses, edges = constraints; optimize to minimize total error
```

**Loop closure — the make-or-break step.** As the robot drives, pose errors **drift**
(odometry again). When it **recognizes a previously visited place** (via scan/visual
matching — "place recognition"), it adds a **loop-closure constraint** linking the
current pose to the old one. Optimizing the graph then **redistributes the
accumulated error** around the whole loop, snapping the map into consistency — a
dramatic correction. Loop closure is what turns a drifting trajectory into a
**globally consistent** map. (False loop closures are catastrophic, so robust
matching matters.)

**The front-end / back-end split** organizes real systems:

- **Front-end** — process sensor data: extract features, match scans/images, detect
  loop closures, form constraints (the perception-heavy part).
- **Back-end** — optimize the graph / run the filter to produce the best poses + map
  (the estimation-heavy part).

**Variants by sensor:** **visual SLAM** (cameras — ORB-SLAM), **LiDAR SLAM** (point
clouds — scan matching / ICP), **visual-inertial** (camera + IMU — robust, used in
AR/drones). Whatever the sensor, the structure is the same: **drift, recognize,
constrain, optimize**.

SLAM is the grand synthesis of the whole track — motion models, sensors,
probabilistic estimation, the EKF/graph — combined so a robot can enter an unknown
world and come out with a map and a consistent trajectory. With a map in hand, the
next questions are **planning** a path through it and **driving** that path.
""",
        ),
        _t(
            "Path planning: Dijkstra, A*, RRT, PRM",
            "12 min",
            r"""# Path planning: Dijkstra, A*, RRT, PRM

With a map, the robot must **find a path** from start to goal — ideally short, and
**collision-free**. Path planners split into two great families: **graph search**
(great for grids / discrete maps) and **sampling-based** (great for
high-dimensional / continuous spaces).

**Graph search** treats the map as a graph (e.g. occupancy-grid cells = nodes,
adjacency = edges):

- **Dijkstra's algorithm** — expands outward from the start in order of **cost-so-far
  $g(n)$**, guaranteeing the **shortest** path. Correct but **uninformed**: it
  explores in all directions equally, so it's slow on large maps.
- **A\*** — Dijkstra **+ a heuristic**. It orders the search by

  $$ f(n) = g(n) + h(n) $$

  where $g(n)$ is cost-so-far and $h(n)$ is an **estimate of the cost-to-go** to the
  goal (e.g. straight-line/Euclidean or Manhattan distance). The heuristic
  **guides** the search toward the goal, exploring far fewer nodes. If $h$ is
  **admissible** (never overestimates the true cost), A\* is **optimal**; the closer
  $h$ is to the truth, the faster it runs (h = 0 reduces A\* to Dijkstra). The
  default grid planner.

```
   Dijkstra: explores a circle      A*: heuristic pulls toward goal
       · · · · ·                        · ·
     · · S · · ·                      S · · ·
     · · · · · G   (wasteful)           · · · G   (focused)
       · · · · ·                          ·
```

**Sampling-based planners** avoid building a full grid — essential when the space is
**high-dimensional** (a robot arm, or (x, y, θ) with kinematic constraints) where a
grid would be astronomically large:

- **RRT (Rapidly-exploring Random Tree)** — grow a tree from the start: repeatedly
  **sample a random point**, find the **nearest** tree node, and **extend** a small
  step toward the sample (if collision-free). The tree rapidly fans into free space
  and finds *a* path fast. **Probabilistically complete** (finds a solution if one
  exists, given time) but the path is **not optimal** (jagged).
- **RRT\*** — the optimal variant: it **rewires** the tree as it grows, so the path
  **converges to the optimal** as samples increase. The standard for high-DOF
  planning.
- **PRM (Probabilistic Roadmap)** — sample many random free configurations, connect
  nearby ones into a **roadmap graph** once, then answer **many** start→goal queries
  by graph search. Great for **multi-query** planning in a static map.

**How to choose:**

```
  low-dim grid / known map, want optimal   -> A* (or Dijkstra)
  high-dim / kinodynamic, want fast feasible-> RRT
  high-dim, want optimal                    -> RRT*
  static map, many queries                  -> PRM
```

A\*'s priority is $f(n) = g(n) + h(n)$. Walking *toward* the goal, cost-so-far $g$
**rises** while the heuristic estimate-to-go $h$ **falls** — their sum $f$ stays near
the (constant) true path cost for nodes on the optimal path, which is exactly why A\*
barely strays from it. Drag the total path length D to see how the two terms trade
off along the route:

```plot
{"title": "A* priority f = g + h along the optimal path — drag total length D", "xLabel": "distance travelled from start", "yLabel": "cost", "xRange": [0, 10], "yRange": [0, 12], "controls": [{"name": "D", "label": "total path length D", "range": [4, 10], "step": 1, "value": 8}], "functions": [{"expr": "x", "label": "g (cost-so-far)", "color": "#16a34a"}, {"expr": "D - x", "label": "h (estimate-to-go)", "color": "#dc2626"}, {"expr": "D", "label": "f = g + h (≈ const)", "color": "#2563eb"}]}
```

Two cross-cutting truths: planners search a **configuration space** where obstacles
are **inflated by the robot's radius** (so a point-robot search stays collision-free),
and the output is a **geometric path** — a sequence of waypoints — that still has to
be **driven** by a controller that respects the robot's kinematics. Next we make A\*
concrete, then add reactive obstacle avoidance and path tracking.
""",
        ),
        _code(
            "A* search on an occupancy grid",
            "15 min",
            r"""# A* PATHFINDING on a small 2-D occupancy grid (0 = free, 1 = obstacle). We use a
# binary-heap open set, the Manhattan-distance heuristic, and reconstruct the path
# by walking parents back from the goal. Pure builtins -- NO numpy here.

# Grid: 6 rows x 7 cols; 1 = obstacle. Start top-left, goal bottom-right.
grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0],
]
rows = 6
cols = 7
start = (0, 0)
goal = (5, 6)


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])   # Manhattan distance (admissible)


# A* with a list-based binary min-heap of (f, g, cell).
def heap_push(heap, item):
    heap.append(item)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent][0] <= heap[i][0]:
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def heap_pop(heap):
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i = 0
        size = len(heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            small = i
            if left < size and heap[left][0] < heap[small][0]:
                small = left
            if right < size and heap[right][0] < heap[small][0]:
                small = right
            if small == i:
                break
            heap[i], heap[small] = heap[small], heap[i]
            i = small
    return top


open_heap = []
heap_push(open_heap, (heuristic(start, goal), 0, start))
came_from = {}
g_score = {start: 0}
visited = set()
expanded = 0

while open_heap:
    f, g, current = heap_pop(open_heap)
    if current in visited:
        continue
    visited.add(current)
    expanded = expanded + 1
    if current == goal:
        break
    cr, cc = current
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = cr + dr
        nc = cc + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        if grid[nr][nc] == 1:
            continue
        neighbor = (nr, nc)
        tentative = g + 1
        if neighbor not in g_score or tentative < g_score[neighbor]:
            g_score[neighbor] = tentative
            came_from[neighbor] = current
            heap_push(open_heap, (tentative + heuristic(neighbor, goal), tentative, neighbor))

# Reconstruct the path by walking parents back from the goal.
path = [goal]
node = goal
while node != start:
    node = came_from[node]
    path.append(node)
path.reverse()

print("A* on a %dx%d grid, start %s -> goal %s" % (rows, cols, start, goal))
print("  nodes expanded = %d" % expanded)
print("  path length    = %d steps" % (len(path) - 1))
print("  path: %s" % path)
print("the heuristic steered A* around obstacles to the shortest free path.")
""",
        ),
        _t(
            "Motion planning & obstacle avoidance",
            "11 min",
            r"""# Motion planning & obstacle avoidance

A planned path assumes a **static, known** world. Reality has **moving people, doors,
unexpected obstacles**, and a robot that **can't turn on a dime**. **Motion planning
and obstacle avoidance** bridge the gap: they turn a geometric path into safe,
**executable** motion, reacting to what the planner didn't know.

The split is **deliberative vs reactive**:

- **Deliberative (global) planning** — the A\*/RRT path over the known map: optimal-ish
  and far-sighted, but **slow** and blind to new obstacles.
- **Reactive (local) avoidance** — fast, sensor-driven steering that **dodges**
  obstacles in real time but is **myopic** (can get stuck). Real systems run a
  **two-layer** architecture: a global planner sets the route; a local planner
  follows it while reacting to immediate obstacles.

**Potential fields** — an elegant reactive idea: treat the goal as an **attractive**
force pulling the robot in, and obstacles as **repulsive** forces pushing it away.
The robot moves down the **gradient** of the summed potential:

$$ U(x) = U_{\text{att}}(x) + U_{\text{rep}}(x), \qquad F = -\nabla U $$

Simple, smooth, and runs in real time. Its famous flaw: **local minima** — the robot
can get **trapped** in a spot where attraction and repulsion cancel (e.g. in a
U-shaped obstacle) and stall, never reaching the goal. Fixes add random escapes,
navigation functions, or fall back to a global planner.

```
  potential field:    goal pulls (↓ low potential)
      obstacle (high potential, repels)
        ╲   ╱
   robot →●→→→→ goal        but a U-shaped trap can create a
        ╱   ╲                   LOCAL MINIMUM where the robot stalls
```

A 1-D slice shows the idea: a **quadratic well** at the goal (here x = 8) plus a
**repulsive spike** at an obstacle (x = 4). Drag the repulsion strength — too weak
and the robot clips the obstacle; too strong and the spike can carve a **local
minimum** the robot stalls in:

```plot
{"title": "Potential field U(x): goal well + obstacle spike — drag repulsion", "xLabel": "position x", "yLabel": "potential U", "xRange": [0, 10], "yRange": [0, 12], "controls": [{"name": "krep", "label": "repulsion strength", "range": [1, 8], "step": 1, "value": 4}], "functions": [{"expr": "0.1 * pow(x - 8, 2) + krep / (pow(x - 4, 2) + 0.3)", "label": "U(x) = U_att + U_rep", "color": "#2563eb"}]}
```

The potential and its gradient (the steering force) in **MATLAB** (for the REPL):

```matlab
x = linspace(0, 10, 200);
katt = 0.1; krep = 4; xgoal = 8; xobs = 4;
U = katt*(x - xgoal).^2 + krep ./ ((x - xobs).^2 + 0.3);
F = -gradient(U, x(2) - x(1));      % force = -dU/dx steers the robot
disp('min potential near x ='); disp(x(U == min(U)))
disp('max repulsive force near the obstacle ='); disp(max(abs(F)))
```

**Dynamic Window Approach (DWA)** — the practical local planner for wheeled robots,
because it respects the robot's **dynamics**. It searches over **achievable (v, ω)
commands** (the "dynamic window" of velocities reachable in the next instant given
acceleration limits), simulates the short arc each would produce, and **scores** each
by an objective that balances:

- **progress toward the goal** (or the global path),
- **clearance from obstacles** (reject any arc that would collide),
- **speed** (prefer faster, smoother motion).

It then executes the best (v, ω) for one step and repeats. DWA naturally produces
**smooth, dynamically feasible** motion and is a staple of ROS navigation. The
**Velocity Obstacle / RVO** family extends reactive avoidance to **moving** obstacles
and **multi-robot** settings (each robot picks velocities that avoid collision cones).

**The key architecture and trade-off:** global planners are **complete and
far-sighted but slow**; local methods are **fast and reactive but myopic** (and can
get stuck in local minima). Layering them — **plan globally, avoid locally** — gives
both safety and goal-reaching, and is how virtually every real autonomous robot
navigates. Whatever the avoidance method, its output is still a **(v, ω) command**,
which a **path-tracking controller** must execute on the real, non-holonomic robot —
next.
""",
        ),
        _t(
            "Path tracking: pure pursuit, Stanley & MPC",
            "11 min",
            r"""# Path tracking: pure pursuit, Stanley & MPC

The planner gives a **geometric path** (waypoints); the robot must actually **drive**
it, correcting for drift, disturbances and its own kinematics. **Path tracking**
(a.k.a. trajectory following) is the **controller** that turns a path into wheel/steer
commands — the last link from plan to motion.

The job: minimize the **cross-track error** (lateral distance from the path) and the
**heading error** (misalignment with the path direction), smoothly, while respecting
the robot's non-holonomic limits.

**Pure pursuit** — the simplest and most popular tracker. Pick a point on the path a
**lookahead distance $L_d$** ahead of the robot, and command a **steering / turn**
that drives the robot along the **circular arc** to that point. For a car-like robot
the steering angle is

$$ \delta = \arctan\!\left(\frac{2 \ell \sin\alpha}{L_d}\right) $$

(ℓ = wheelbase, α = angle to the lookahead point); for a unicycle/diff-drive you
command a curvature $\kappa = \tfrac{2\sin\alpha}{L_d}$, i.e. $\omega = \kappa v$. The
**lookahead $L_d$ is the key knob**:

- **Short $L_d$** → tight, aggressive tracking, but **oscillation** / instability.
- **Long $L_d$** → smooth and stable, but **cuts corners** (large tracking error).

Often $L_d$ scales with speed (look farther when going faster). It's geometric,
intuitive, and robust — the default for many robots and the lab next.

```
   pure pursuit:                path ····●···· lookahead point (L_d ahead)
                                    ╱α            steer along the arc to it
        robot ──►(arc)────────────●
                 chosen turn brings the robot onto the path
```

**Stanley controller** (of DARPA Grand Challenge fame) — steers using **both** the
heading error **and** a term proportional to the cross-track error
($\delta = \theta_e + \arctan(k\, e / v)$). It corrects cross-track error more
directly than pure pursuit and has nice stability properties; a strong choice for
car-like vehicles.

**Model Predictive Control (MPC)** — the heavyweight, optimal approach. At each step
it uses the robot's **dynamics model** to **predict** the trajectory over a short
**horizon** for candidate command sequences, **optimizes** the commands to minimize a
cost (tracking error + control effort) **subject to constraints** (speed, steering,
acceleration, obstacle limits), executes the **first** command, then **re-plans** next
step (**receding horizon**). MPC handles constraints and dynamics **explicitly** and
gives the smoothest, most capable tracking — at a real **computational cost**, which
is why it's now common in self-driving cars and high-performance robots.

```
  pure pursuit   geometric, 1 knob (L_d)     simple, robust; tunes by feel
  Stanley        heading + cross-track term  direct error correction (cars)
  MPC            predict + optimize horizon  optimal, handles constraints; costly
```

**The trade-off:** **simplicity vs capability.** Pure pursuit/Stanley are cheap,
robust, and everywhere; MPC is powerful and constraint-aware but heavy. All three
close the loop from **path → command**, completing the autonomy stack: **SLAM** (map
+ localize) → **planning** (find a path) → **avoidance** (stay safe) → **tracking**
(drive it). That full pipeline — perception, estimation, planning, control, woven
together — is what makes a robot **autonomous**. You'll implement pure-pursuit
steering next.
""",
        ),
        _code(
            "Pure-pursuit path tracking",
            "14 min",
            r"""# PURE PURSUIT: steer a unicycle robot to follow a path of waypoints. Each step we
# find the lookahead point (first waypoint at least L_d ahead), compute the curvature
# of the arc to it, set omega = curvature * v, and integrate the pose. numpy.

import numpy as np

# The reference path is a straight line along y = 0 (densely sampled waypoints).
path_x = np.linspace(0.0, 12.0, 121)
path_y = np.zeros(121)

v = 0.6          # constant forward speed (m/s)
ld = 1.0         # lookahead distance (m)
dt = 0.1
steps = 180

# Robot starts 0.6 m off the path (to the side) -> watch it converge onto y = 0.
x = 0.0
y = 0.6
theta = 0.0
xs = [x]
ys = [y]
cross_track = [abs(y)]

for i in range(steps):
    # Find the lookahead point: first waypoint AHEAD (x >= robot x) at distance >= ld.
    dx = path_x - x
    dy = path_y - y
    dist = np.sqrt(dx * dx + dy * dy)
    far_enough = (dist >= ld) & (path_x >= x)
    ahead = np.flatnonzero(far_enough)
    if ahead.size > 0:
        tgt = int(ahead[0])
    else:
        tgt = int(path_x.size - 1)   # near the end: aim at the final waypoint

    # Angle to the lookahead point in the robot frame (wrapped to [-pi, pi]).
    alpha = float(np.arctan2(path_y[tgt] - y, path_x[tgt] - x)) - theta
    alpha = float(np.arctan2(np.sin(alpha), np.cos(alpha)))

    # Pure-pursuit curvature kappa = 2 sin(alpha)/L_d, then omega = kappa*v; integrate.
    curvature = 2.0 * float(np.sin(alpha)) / ld
    omega = curvature * v
    x = x + v * float(np.cos(theta)) * dt
    y = y + v * float(np.sin(theta)) * dt
    theta = theta + omega * dt
    xs.append(x)
    ys.append(y)
    cross_track.append(abs(y))   # distance to the y = 0 reference path

print("pure pursuit: v=%.1f m/s, lookahead L_d=%.1f m, started 0.6 m off the path" % (v, ld))
print("  final pose (%.2f, %.2f, %.0f deg)" % (x, y, float(np.degrees(theta))))
print("  initial cross-track error = %.3f m, final = %.3f m"
      % (cross_track[0], cross_track[-1]))
print("the robot converged onto the path and held it -- pure pursuit works.")
""",
        ),
        quiz_lesson(
            "Quiz: SLAM, Planning & Path Tracking",
            (
                q(
                    "What does SLAM solve, and why is it hard?",
                    (
                        opt(
                            "Building a map and localizing in it simultaneously — hard because mapping needs a known pose and localization needs a map (chicken-and-egg), solved jointly via correlated errors",
                            correct=True,
                        ),
                        opt("Only localization, against a pre-built map"),
                        opt("Only mapping, with a perfectly known trajectory"),
                        opt("Planning the shortest path through a known map"),
                    ),
                    "SLAM estimates pose and map jointly; robot↔landmark errors are correlated, so observations constrain both. Loop closure corrects accumulated drift.",
                ),
                q(
                    "How does A* improve on Dijkstra's algorithm?",
                    (
                        opt(
                            "It adds an admissible heuristic h(n): order by f = g + h so the search is guided toward the goal, expanding far fewer nodes while staying optimal",
                            correct=True,
                        ),
                        opt("It ignores edge costs entirely"),
                        opt("It searches randomly instead of by cost"),
                        opt("It always finds a longer path faster"),
                    ),
                    "Dijkstra is uninformed (expands a circle); A* uses h(n) (e.g. Manhattan/Euclidean) to focus toward the goal. Admissible h ⇒ optimal; h=0 ⇒ Dijkstra.",
                ),
                q(
                    "When are sampling-based planners (RRT/RRT*/PRM) preferred over grid search (A*)?",
                    (
                        opt(
                            "In high-dimensional or continuous/kinodynamic spaces where a grid would be astronomically large",
                            correct=True,
                        ),
                        opt("Only for tiny 2-D grids"),
                        opt("Whenever an admissible heuristic exists"),
                        opt("Never — A* always wins"),
                    ),
                    "RRT explores high-DOF spaces fast (probabilistically complete); RRT* converges to optimal; PRM amortizes a roadmap over many queries. A* shines on low-dim grids.",
                ),
                q(
                    "What is the classic failure mode of potential-field obstacle avoidance?",
                    (
                        opt(
                            "Local minima — attractive and repulsive forces can cancel (e.g. in a U-shaped obstacle), trapping the robot short of the goal",
                            correct=True,
                        ),
                        opt("It always finds the global optimum"),
                        opt("It cannot run in real time"),
                        opt("It requires a full pre-built grid"),
                    ),
                    "Goal attracts, obstacles repel, robot follows −∇U; but forces can balance in a trap (local minimum). DWA respects dynamics and avoids this pitfall.",
                ),
                q(
                    "In pure-pursuit path tracking, what does the lookahead distance L_d trade off?",
                    (
                        opt(
                            "Short L_d → tight but oscillatory tracking; long L_d → smooth but cuts corners (more tracking error)",
                            correct=True,
                        ),
                        opt("It sets the robot's maximum speed only"),
                        opt("It has no effect on tracking behaviour"),
                        opt("Longer L_d always means tighter tracking"),
                    ),
                    "Pure pursuit steers along the arc to a point L_d ahead. Small L_d = aggressive/oscillating; large L_d = smooth but corner-cutting; often L_d scales with speed.",
                ),
                q(
                    "What distinguishes MPC from pure pursuit and Stanley?",
                    (
                        opt(
                            "MPC predicts over a horizon using the dynamics model and optimizes commands subject to constraints (receding horizon) — optimal and constraint-aware, but computationally heavy",
                            correct=True,
                        ),
                        opt("MPC ignores the robot's dynamics"),
                        opt("MPC is the simplest, cheapest controller"),
                        opt("MPC cannot handle constraints"),
                    ),
                    "MPC optimizes a command sequence over a prediction horizon with explicit constraints, executes the first command, then re-plans. Pure pursuit/Stanley are cheaper, geometric trackers.",
                ),
            ),
        ),
    ),
)


MOBILE_ROBOTICS_COURSES = (_MR_BASICS, _MR_INTERMEDIATE, _MR_ADVANCED)
