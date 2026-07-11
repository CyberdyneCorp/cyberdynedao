"""Academy seed content - Process Dynamics, Instrumentation and Control.

Keeping chemical processes stable and on-spec. This course covers process
dynamics and transfer functions, first- and second-order response,
measurement and instrumentation, the feedback control loop, PID control
and tuning, cascade/ratio/feedforward schemes, advanced control (model
predictive control), and modern distributed control systems and Industry
4.0. Every lesson is a direct explanation with a worked equation or
calculation snippet and a mermaid diagram, followed by a checkpoint quiz;
the course closes with a comprehensive final quiz.
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


_PROCESS_DYNAMICS_CONTROL = SeedCourse(
    slug="process-dynamics-control",
    title="Process Dynamics, Instrumentation & Control",
    description=(
        "Keeping chemical processes stable and on-spec: process dynamics and "
        "transfer functions, measurement and instrumentation, feedback and PID "
        "control, cascade/ratio/feedforward schemes, advanced control (MPC), and "
        "modern distributed control systems and Industry 4.0 - with worked "
        "equations, tuning calculations and a diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Process Dynamics, Instrumentation and Control

A chemical plant is never truly at rest. Feed compositions drift, ambient
temperature swings, pumps wear, and operators change setpoints. **Process
control** is the discipline of keeping temperatures, pressures, flows,
levels and compositions where they need to be - safely, continuously, and
close to the economic optimum - despite all that disturbance.

This course builds the ideas in order, from how a process *responds* to a
change, through how we *measure* it, to how we *control* it - ending with
the model-based and digital systems that run modern plants.

The approach is **concrete**: every lesson explains one idea directly,
shows it with a worked equation or a short calculation, and draws it as a
diagram. After each lesson there is a short quiz; a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **Process dynamics and transfer functions** - how outputs lag inputs
2. **First- and second-order response** - the shapes processes make
3. **Measurement and instrumentation** - flow, temperature, pressure, level
4. **Feedback control and the control loop** - closing the loop
5. **PID controllers and tuning** - the workhorse algorithm
6. **Cascade, ratio and feedforward control** - beyond single-loop
7. **Advanced control** - model predictive control (MPC)
8. **Distributed control systems and Industry 4.0** - the modern plant

Grounded in real practice - ISA standards, PID loops you will meet in any
DCS, and tools like Aspen Dynamics and MATLAB/Simulink - but kept
teachable. Let us start with why a process does not respond instantly.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the core goal of process control?",
                    (
                        opt("To design the chemical reaction itself"),
                        opt(
                            "To keep process variables (temperature, pressure, flow, "
                            "level, composition) at target despite disturbances",
                            correct=True,
                        ),
                        opt("To replace all human operators"),
                        opt("To reduce the number of pipes in a plant"),
                    ),
                    "Control holds the process on-spec and safe in the face of "
                    "ever-present disturbances.",
                ),
                q(
                    "In what order does this course build the material?",
                    (
                        opt("Control first, then how the process responds"),
                        opt(
                            "Dynamics (how a process responds), then measurement, then "
                            "control, then advanced and digital systems",
                            correct=True,
                        ),
                        opt("Only steady-state design, no dynamics"),
                        opt("Purely economics with no equations"),
                    ),
                    "You cannot control what you do not understand or measure - so "
                    "dynamics and instrumentation come first.",
                ),
            ),
        ),
        # -- 1. Process dynamics and transfer functions ----------------
        _t(
            "Process dynamics and transfer functions",
            "10 min",
            """# Process dynamics and transfer functions

**Process dynamics** is the study of how a process output changes over
*time* when an input changes - not just where it ends up, but how it gets
there. A steam-heated tank does not jump to a new temperature the instant
you open the valve; it warms gradually. That lag is what control must
work with.

The standard tool for describing dynamics is the **transfer function**. We
take a linear (or linearized) model, apply the **Laplace transform**, and
get an algebraic ratio of output to input in the frequency domain `s`:

```text
        Y(s)      output (deviation from steady state)
G(s) = ------  =  ------------------------------------
        U(s)      input  (deviation from steady state)
```

Everything is written in **deviation variables** - the difference from the
steady-state operating point - so the initial condition is zero and the
algebra stays clean.

Two features dominate almost every chemical process:

- **Time constant (tau)** - how *fast* the process responds. A large tau
  (a big well-mixed tank) is sluggish; a small tau is quick.
- **Dead time (theta)** - a pure *delay* before any response begins,
  caused by transport (fluid travelling down a pipe) or measurement lag.
  Dead time is the enemy of control: it delays the feedback.

A very common model is the **first-order plus dead time (FOPDT)** form,
the single most useful approximation in practice:

```text
              K * exp(-theta * s)
G(s)  =  ---------------------------
                tau * s  +  1

K     = process gain     (how much output moves per unit input)
tau   = time constant    (speed of response)
theta = dead time        (delay before response)
```

```mermaid
graph LR
    U["Input change U of s"] --> DT["Dead time delay theta"]
    DT --> LAG["First order lag tau"]
    LAG --> K["Gain K scales output"]
    K --> Y["Output response Y of s"]
```

Remember: a transfer function packs a process into three numbers - **gain,
time constant, dead time** - and those three numbers are what we tune the
controller against.
""",
        ),
        quiz_lesson(
            "Quiz: Process dynamics and transfer functions",
            (
                q(
                    "What does a transfer function G(s) represent?",
                    (
                        opt("The steady-state cost of running a process"),
                        opt(
                            "The ratio of output to input in the Laplace domain, "
                            "describing how the output responds dynamically to the input",
                            correct=True,
                        ),
                        opt("The number of pipes between two units"),
                        opt("The chemical formula of the product"),
                    ),
                    "G(s) = Y(s)/U(s) captures the dynamic input-output relationship "
                    "in deviation variables.",
                ),
                q(
                    "Why is dead time (theta) especially troublesome for control?",
                    (
                        opt("It increases the process gain"),
                        opt(
                            "It delays the response, so feedback about a disturbance "
                            "arrives late and the controller reacts behind the process",
                            correct=True,
                        ),
                        opt("It has no effect on control"),
                        opt("It makes the sensor cheaper"),
                    ),
                    "Pure delay means the controller is always acting on stale "
                    "information - large theta forces slower, more cautious tuning.",
                ),
                q(
                    "What three parameters define a first-order plus dead time (FOPDT) model?",
                    (
                        opt("Voltage, current, resistance"),
                        opt(
                            "Process gain K, time constant tau, and dead time theta",
                            correct=True,
                        ),
                        opt("Pressure, temperature, flow"),
                        opt("Proportional, integral, derivative"),
                    ),
                    "FOPDT is the workhorse identification model: K, tau, theta.",
                ),
            ),
        ),
        # -- 2. First- and second-order response -----------------------
        _t(
            "First- and second-order process response",
            "11 min",
            """# First- and second-order process response

When you make a **step change** in an input, the shape of the output tells
you the order of the process.

## First-order response

A single capacity - one well-mixed tank, one lag - gives a smooth
exponential approach to the new value. For a step of size `M` in the input
of a first-order process with gain `K` and time constant `tau`:

```text
y(t)  =  K * M * (1 - exp(-t / tau))

At t = tau     -> 63.2 percent of the final change is complete
At t = 3*tau   -> about 95 percent complete
At t = 5*tau   -> about 99 percent (practically settled)
```

So `tau` is read straight off a step test: the time to reach 63.2 percent
of the final value. No overshoot ever - a first-order process only *lags*.

## Second-order response

Put two capacities in series, or add inertia (a valve actuator, a
recycle), and you get a **second-order** system, characterised by a
**natural period** and a **damping ratio (zeta)**:

```text
                    K
G(s) = --------------------------------
        tau^2 * s^2 + 2*zeta*tau*s + 1

zeta > 1   overdamped   -> slow, no overshoot (two real lags)
zeta = 1   critically damped -> fastest with no overshoot
zeta < 1   underdamped  -> oscillates and overshoots before settling
```

Underdamped responses **overshoot** and ring - important, because an
aggressively tuned control loop turns an otherwise sluggish process into
an oscillating second-order-like one.

```mermaid
graph TD
    STEP["Step input change"] --> ORDER["Process order"]
    ORDER --> FIRST["First order smooth exponential"]
    ORDER --> SECOND["Second order"]
    FIRST --> TAU["Reaches 63 percent at one tau"]
    SECOND --> OVER["Underdamped overshoots and rings"]
    SECOND --> CRIT["Critically damped fast no overshoot"]
```

Remember: first-order lags but never overshoots; second-order *can*
overshoot and oscillate, and the damping ratio zeta decides which.
""",
        ),
        quiz_lesson(
            "Quiz: First- and second-order process response",
            (
                q(
                    "After a step change, how long until a first-order process reaches "
                    "63.2 percent of its final value?",
                    (
                        opt("One time constant, tau", correct=True),
                        opt("One dead time, theta"),
                        opt("Five time constants"),
                        opt("It reaches it instantly"),
                    ),
                    "y(tau) = K*M*(1 - e^-1) = 0.632*K*M - reading tau off a step test.",
                ),
                q(
                    "Which statement about a first-order step response is true?",
                    (
                        opt("It always overshoots the final value"),
                        opt(
                            "It approaches the final value smoothly and never overshoots",
                            correct=True,
                        ),
                        opt("It oscillates forever"),
                        opt("It responds instantly with no lag"),
                    ),
                    "A single capacity only lags; overshoot needs second (or higher) "
                    "order dynamics.",
                ),
                q(
                    "What does a damping ratio zeta less than 1 produce?",
                    (
                        opt("An overdamped, sluggish response"),
                        opt(
                            "An underdamped response that overshoots and oscillates "
                            "before settling",
                            correct=True,
                        ),
                        opt("No response at all"),
                        opt("A perfectly linear ramp"),
                    ),
                    "zeta < 1 is underdamped (rings); zeta = 1 critical; zeta > 1 overdamped.",
                ),
            ),
        ),
        # -- 3. Measurement and instrumentation ------------------------
        _t(
            "Measurement and instrumentation (flow, temperature, pressure, level)",
            "11 min",
            """# Measurement and instrumentation

You cannot control what you cannot measure. A control loop is only as good
as its **sensor** (the measuring element) and **transmitter** (which
converts the measurement into a standard signal - historically **4-20 mA**,
increasingly digital fieldbus/HART). Sensor tag names follow the **ISA-5.1**
convention: `FT` flow transmitter, `TT` temperature, `PT` pressure, `LT`
level.

The four workhorse measurements:

- **Flow** - **orifice plate** with a differential-pressure transmitter is
  the classic; flow relates to the square root of the pressure drop.
  **Coriolis** meters measure true mass flow directly and very accurately;
  **magnetic** meters suit conductive liquids; **vortex** and **turbine**
  are also common.
- **Temperature** - **thermocouples** (rugged, wide range, based on the
  Seebeck effect) and **RTDs** such as the Pt100 (more accurate and stable,
  resistance rises with temperature). The sensor sits in a **thermowell**
  so it can be replaced without opening the process.
- **Pressure** - **capacitance** or **piezoresistive** transmitters;
  **differential-pressure (DP)** cells are the swiss-army knife, used for
  flow, level and filter monitoring too.
- **Level** - **DP** across the liquid head, **radar** and **guided-wave
  radar**, **ultrasonic**, and **capacitance** probes.

Two properties decide whether a measurement is fit for control: **accuracy**
(closeness to the true value) and **repeatability** (same reading for the
same condition). For control, repeatability often matters more than
absolute accuracy - a repeatable measurement can be trimmed.

The orifice-plate flow relationship shows why sensors need care:

```text
Q  =  Cd * A * sqrt( 2 * dP / rho )

Q   = volumetric flow rate
Cd  = discharge coefficient (orifice specific)
A   = orifice area
dP  = differential pressure across the plate
rho = fluid density

Because Q varies with sqrt(dP), halving the flow quarters the dP -
so a DP flow measurement loses resolution badly at low flow (turndown).
```

```mermaid
graph LR
    PROC["Process fluid"] --> SENSE["Sensor primary element"]
    SENSE --> TX["Transmitter 4 to 20 mA or digital"]
    TX --> CTRL["Controller in the DCS"]
    CTRL --> DISP["Display and historian"]
```

Remember: the transmitter turns a physical quantity into a standard signal
the controller can read - and the whole loop inherits that measurement's
accuracy, repeatability and lag.
""",
        ),
        quiz_lesson(
            "Quiz: Measurement and instrumentation (flow, temperature, pressure, level)",
            (
                q(
                    "In an orifice-plate flow meter, how does volumetric flow Q relate "
                    "to the differential pressure dP?",
                    (
                        opt("Q is proportional to dP"),
                        opt(
                            "Q is proportional to the square root of dP",
                            correct=True,
                        ),
                        opt("Q is inversely proportional to dP"),
                        opt("Q does not depend on dP"),
                    ),
                    "Q = Cd*A*sqrt(2*dP/rho); the square-root law is why DP flow loses "
                    "resolution at low flow.",
                ),
                q(
                    "Which pair are common temperature-measuring elements?",
                    (
                        opt("Orifice plate and Coriolis meter"),
                        opt("Thermocouple and RTD (Pt100)", correct=True),
                        opt("Radar and ultrasonic"),
                        opt("Capacitance and piezoresistive cells"),
                    ),
                    "Thermocouples (Seebeck effect) and RTDs (resistance vs temperature) "
                    "are the two workhorses; the others measure flow, level or pressure.",
                ),
                q(
                    "For closed-loop control, why can repeatability matter more than "
                    "absolute accuracy?",
                    (
                        opt("Accuracy is never important"),
                        opt(
                            "A consistently repeatable measurement can be trimmed or "
                            "calibrated out, and control acts on changes, so consistency "
                            "keeps the loop stable",
                            correct=True,
                        ),
                        opt("Repeatability makes the sensor cheaper to buy"),
                        opt("Because transmitters cannot be accurate"),
                    ),
                    "The loop responds to deviations; a repeatable bias can be corrected, "
                    "but a wandering (non-repeatable) reading destabilises control.",
                ),
            ),
        ),
        # -- 4. Feedback control and the control loop ------------------
        _t(
            "Feedback control and the control loop",
            "10 min",
            """# Feedback control and the control loop

**Feedback control** is the central idea: measure the controlled variable,
compare it to the **setpoint (SP)**, and adjust an input to drive the
difference toward zero. That difference is the **error**:

```text
error  e(t)  =  SP  -  PV        (setpoint minus process variable)
```

The pieces of every single loop:

- **Process variable (PV)** - what you are controlling (a tank temperature).
- **Setpoint (SP)** - the target value.
- **Controller** - computes an output from the error.
- **Final control element** - usually a **control valve** that moves the
  **manipulated variable (MV)** (say, steam flow).
- **Disturbance** - anything else that pushes the PV around (feed temp).

The signal travels around a **closed loop**: sensor to controller to valve
to process and back to sensor. Because the controller output eventually
affects its own input, the loop can either settle nicely or, if pushed too
hard, **oscillate** or go unstable.

Two big choices define the loop's character:

- **Direct vs reverse acting** - which way the controller moves its output
  as PV rises. Get this wrong and feedback becomes *positive* feedback,
  driving the loop away from setpoint. It must match the process and valve
  action (e.g. air-to-open vs air-to-close, fail-safe).
- **Feedback vs feedforward** - feedback reacts to error *after* it appears
  (robust, but always a step behind); feedforward acts on a measured
  disturbance *before* it reaches the PV (fast, but needs a model). More on
  feedforward in a later lesson.

```mermaid
graph LR
    SP["Setpoint SP"] --> CMP["Compare error equals SP minus PV"]
    PV["Measured PV"] --> CMP
    CMP --> CTRL["Controller"]
    CTRL --> VAL["Control valve MV"]
    VAL --> PROC["Process"]
    DIST["Disturbance"] --> PROC
    PROC --> SENSE["Sensor"]
    SENSE --> PV
```

Remember: feedback closes the loop - measure, subtract from setpoint, act -
and the direction of controller action must be set so that acting *reduces*
the error, not amplifies it.
""",
        ),
        quiz_lesson(
            "Quiz: Feedback control and the control loop",
            (
                q(
                    "How is the control error defined?",
                    (
                        opt("Error equals process variable times setpoint"),
                        opt("Error equals setpoint minus process variable", correct=True),
                        opt("Error equals valve position minus flow"),
                        opt("Error equals the disturbance magnitude"),
                    ),
                    "e(t) = SP - PV; the controller drives this error toward zero.",
                ),
                q(
                    "What is the manipulated variable (MV) in a typical loop?",
                    (
                        opt("The setpoint the operator enters"),
                        opt(
                            "The input the controller adjusts (via the final control "
                            "element, usually a valve) to influence the PV",
                            correct=True,
                        ),
                        opt("The disturbance entering the process"),
                        opt("The historian record of past values"),
                    ),
                    "The controller moves the MV (e.g. steam flow through a valve) to "
                    "correct the PV.",
                ),
                q(
                    "Why must controller action (direct vs reverse acting) be set correctly?",
                    (
                        opt("To choose the color of the faceplate"),
                        opt(
                            "So that the controller's response reduces the error; the "
                            "wrong action turns feedback into positive feedback and "
                            "drives the loop unstable",
                            correct=True,
                        ),
                        opt("It only affects the units displayed"),
                        opt("It has no effect on stability"),
                    ),
                    "Action must match process and valve (fail-safe) so acting corrects, "
                    "not worsens, the error.",
                ),
            ),
        ),
        # -- 5. PID controllers and tuning -----------------------------
        _t(
            "PID controllers and tuning",
            "12 min",
            """# PID controllers and tuning

The **PID controller** is the workhorse of process control - the large
majority of industrial loops are PID or a subset (PI, P). It combines three
actions on the error `e(t) = SP - PV`:

```text
                          1    /                de(t)
u(t) = Kc * [ e(t)  +  ------ | e(t) dt  +  Td ------- ]
                          Ti   /                  dt

Kc = controller gain        (proportional - reacts to present error)
Ti = integral time          (removes steady-state offset - the past)
Td = derivative time        (anticipates - reacts to the rate, the future)
```

What each term does:

- **Proportional (P)** - output proportional to current error. Strong and
  immediate, but pure P leaves a permanent **offset** (steady-state error).
- **Integral (I)** - accumulates past error and keeps adjusting until the
  error is *zero*. It eliminates offset but adds lag and can **wind up** if
  the valve saturates (use anti-windup).
- **Derivative (D)** - responds to how fast the error is changing, adding
  damping and anticipation. Sensitive to noise, so it is often filtered or
  omitted; many loops run as **PI**.

**Tuning** means choosing Kc, Ti, Td for a good balance of speed and
stability. A classic starting point is **Ziegler-Nichols**, using the FOPDT
model (K, tau, theta) from a step test:

```python
# Ziegler-Nichols (open-loop, FOPDT) PI tuning from a step test
def zn_pi(K, tau, theta):
    Kc = 0.9 * tau / (K * theta)   # controller gain
    Ti = 3.33 * theta              # integral time
    return Kc, Ti

# Example: K = 2.0, tau = 30 s, theta = 5 s
Kc, Ti = zn_pi(2.0, 30.0, 5.0)
print(round(Kc, 2), round(Ti, 2))   # -> 2.7  16.65
```

Ziegler-Nichols is aggressive (quarter-amplitude decay); methods like
**IMC / lambda tuning** trade a little speed for robustness and are widely
preferred in practice. Notice the tuning depends directly on the **theta/tau
ratio** - more dead time forces a gentler controller.

```mermaid
graph LR
    E["Error e equals SP minus PV"] --> P["Proportional Kc times e"]
    E --> I["Integral removes offset"]
    E --> D["Derivative adds damping"]
    P --> SUM["Sum to controller output"]
    I --> SUM
    D --> SUM
    SUM --> VALVE["Control valve"]
```

Remember: P reacts to the present, I to the past (kills offset), D to the
future (adds damping); tune Kc, Ti, Td from the process model, and more dead
time means back off the gain.
""",
        ),
        quiz_lesson(
            "Quiz: PID controllers and tuning",
            (
                q(
                    "Which PID term eliminates steady-state offset?",
                    (
                        opt("Proportional"),
                        opt("Integral", correct=True),
                        opt("Derivative"),
                        opt("None - offset cannot be removed"),
                    ),
                    "Integral action keeps accumulating error until PV equals SP, "
                    "removing the offset that pure P leaves.",
                ),
                q(
                    "What is the main drawback of a pure proportional (P-only) controller?",
                    (
                        opt("It always makes the loop unstable"),
                        opt(
                            "It leaves a permanent steady-state offset from setpoint",
                            correct=True,
                        ),
                        opt("It cannot respond to any error"),
                        opt("It amplifies noise excessively"),
                    ),
                    "P alone balances at a nonzero error; integral action is needed to "
                    "drive offset to zero.",
                ),
                q(
                    "Why is derivative action often filtered or omitted in practice?",
                    (
                        opt("It removes offset too aggressively"),
                        opt(
                            "It responds to the rate of change and is very sensitive to "
                            "measurement noise, which it amplifies",
                            correct=True,
                        ),
                        opt("It is illegal under ISA standards"),
                        opt("It only works on flow loops"),
                    ),
                    "D amplifies noise; many loops run as PI, or filter the derivative.",
                ),
                q(
                    "How does a larger dead-time-to-time-constant (theta/tau) ratio affect tuning?",
                    (
                        opt("It allows a much higher controller gain"),
                        opt(
                            "It forces a gentler, lower-gain controller because feedback "
                            "arrives more delayed",
                            correct=True,
                        ),
                        opt("It has no effect on tuning"),
                        opt("It removes the need for integral action"),
                    ),
                    "More dead time relative to tau means slower, more cautious tuning "
                    "to keep the loop stable.",
                ),
            ),
        ),
        # -- 6. Cascade, ratio and feedforward control -----------------
        _t(
            "Cascade, ratio and feedforward control",
            "11 min",
            """# Cascade, ratio and feedforward control

A single feedback loop is often not enough. Three classic multi-loop
structures handle disturbances a lone PID handles poorly.

## Cascade control

Put one loop **inside** another. The **outer (primary/master)** controller
sets the **setpoint** of an **inner (secondary/slave)** controller, which
acts on the valve. The inner loop must be **faster** than the outer.

Example: a reactor temperature (slow, primary) sets the setpoint for a
jacket-flow or jacket-temperature loop (fast, secondary). If cooling-water
pressure dips, the fast inner loop corrects the jacket flow *before* the
reactor temperature even notices - the disturbance is caught early.

```text
Rule of thumb: the inner (secondary) loop should be roughly
3 to 5 times faster than the outer (primary) loop, or cascade
gives little benefit.
```

## Ratio control

Hold two flows in a fixed **ratio** - essential for blending and combustion.
The controller sets one flow (the *manipulated* stream) as a multiple of a
measured *wild* stream:

```text
SP_B  =  R * F_A

F_A = measured wild flow (e.g. air)
R   = desired ratio (e.g. fuel-to-air)
SP_B = setpoint for the controlled flow (e.g. fuel)
```

## Feedforward control

**Measure the disturbance and act before it reaches the PV.** Feedback is
always a step behind because it waits for an error; feedforward uses a
model of the disturbance's effect to cancel it in advance. It is powerful
but imperfect (models are never exact), so it is almost always paired
**with** feedback, which mops up the residual error.

```mermaid
graph LR
    FA["Wild flow F A measured"] --> RATIO["Multiply by ratio R"]
    RATIO --> SPB["Setpoint for controlled flow"]
    DIST["Measured disturbance"] --> FF["Feedforward model"]
    FF --> SUM["Combine with feedback"]
    OUTER["Primary controller"] --> INNER["Secondary setpoint cascade"]
    INNER --> SUM
    SUM --> VALVE["Control valve"]
```

Remember: cascade nests a fast inner loop to catch disturbances early;
ratio ties one flow to another; feedforward acts on a measured disturbance
before it hits - and all three are usually combined with plain feedback.
""",
        ),
        quiz_lesson(
            "Quiz: Cascade, ratio and feedforward control",
            (
                q(
                    "In cascade control, what does the outer (primary) controller output?",
                    (
                        opt("The valve position directly"),
                        opt(
                            "The setpoint for the inner (secondary) controller",
                            correct=True,
                        ),
                        opt("The measured disturbance"),
                        opt("The historian setpoint only"),
                    ),
                    "The primary sets the secondary's setpoint; the fast secondary loop "
                    "moves the valve.",
                ),
                q(
                    "What is a key requirement for cascade control to help?",
                    (
                        opt("The inner loop must be much slower than the outer loop"),
                        opt(
                            "The inner (secondary) loop must be significantly faster than "
                            "the outer (primary) loop",
                            correct=True,
                        ),
                        opt("Both loops must run at exactly the same speed"),
                        opt("There must be no disturbances at all"),
                    ),
                    "A faster inner loop (roughly 3-5x) catches disturbances before they "
                    "reach the primary variable.",
                ),
                q(
                    "How does feedforward control differ from feedback?",
                    (
                        opt("Feedforward waits for an error to appear before acting"),
                        opt(
                            "Feedforward measures the disturbance and acts before it "
                            "affects the PV, whereas feedback reacts after an error "
                            "appears",
                            correct=True,
                        ),
                        opt("Feedforward ignores disturbances entirely"),
                        opt("They are identical in behaviour"),
                    ),
                    "Feedforward is proactive (needs a model); feedback is reactive but "
                    "robust - so they are combined.",
                ),
            ),
        ),
        # -- 7. Advanced control (MPC) ---------------------------------
        _t(
            "Advanced control (model predictive control)",
            "12 min",
            """# Advanced control (model predictive control)

PID controls one loop at a time. But real units are **multivariable** -
moving one valve shifts several variables at once (a distillation column's
reflux affects both top and bottom composition), and there are **constraints**
(valve limits, purity specs, safety limits). **Model Predictive Control
(MPC)** is the standard **advanced process control (APC)** answer, deployed
on thousands of refinery and chemical units.

MPC uses an explicit **dynamic model** of the process to **predict** the
future response over a **prediction horizon**, then solves an **optimization**
at every control step to choose the moves that best track the targets while
**respecting constraints**:

```text
At each step, MPC solves (conceptually):

  minimize   sum over future k of  ( y_predicted(k) - setpoint )^2
             +  weight * ( change in u(k) )^2

  subject to:   u_min   <=  u(k)  <=  u_max     (valve limits)
                y_min   <=  y(k)  <=  y_max     (quality/safety limits)

Apply only the FIRST computed move, then measure and re-solve
next step - this is the "receding horizon" idea.
```

The **receding horizon**: compute an optimal sequence of moves, apply only
the first, then measure and re-optimise - so MPC constantly corrects for
model error and new disturbances, like feedback wrapped around prediction.

Why plants pay for MPC:

- **Handles interaction** - one controller coordinates many inputs and
  outputs together instead of fighting single loops.
- **Respects constraints explicitly** - it can push the process *right up
  against* a limit safely, which is where the money is (operate closer to
  the maximum-throughput or minimum-energy constraint).
- **Anticipates** - because it predicts, it starts acting before a modelled
  disturbance fully arrives.

The cost is a **good dynamic model** (identified from **step tests** or
plant data) and ongoing maintenance - models drift as equipment ages.

```mermaid
graph TD
    MODEL["Dynamic process model"] --> PRED["Predict future outputs"]
    MEAS["Current measurements"] --> PRED
    PRED --> OPT["Optimize moves over horizon"]
    CONS["Constraints valve and quality limits"] --> OPT
    OPT --> MOVE["Apply first move only"]
    MOVE --> MEAS
```

Remember: MPC predicts with a model, optimizes the moves over a horizon
subject to constraints, applies the first move, and re-solves each step -
letting a plant run closer to its limits than single-loop PID safely can.
""",
        ),
        quiz_lesson(
            "Quiz: Advanced control (model predictive control)",
            (
                q(
                    "What core capability defines model predictive control?",
                    (
                        opt("It uses no process model at all"),
                        opt(
                            "It uses a dynamic model to predict future behaviour and "
                            "optimizes control moves over a horizon subject to constraints",
                            correct=True,
                        ),
                        opt("It only tunes a single PID gain"),
                        opt("It replaces all sensors with cameras"),
                    ),
                    "MPC = model + prediction + constrained optimization each step.",
                ),
                q(
                    "What is the 'receding horizon' principle in MPC?",
                    (
                        opt("Apply the entire computed move sequence and never re-solve"),
                        opt(
                            "Compute an optimal sequence, apply only the first move, then "
                            "measure and re-optimize at the next step",
                            correct=True,
                        ),
                        opt("Ignore measurements once the horizon is set"),
                        opt("Extend the horizon to infinity permanently"),
                    ),
                    "Applying only the first move and re-solving lets MPC correct for "
                    "model error and new disturbances - feedback around prediction.",
                ),
                q(
                    "Why is MPC especially valuable for multivariable, constrained units?",
                    (
                        opt("Because it needs no model or measurements"),
                        opt(
                            "It coordinates many interacting inputs and outputs and can "
                            "safely push the process against constraints, capturing the "
                            "economic benefit near the limits",
                            correct=True,
                        ),
                        opt("Because it is simpler to tune than a single PID"),
                        opt("Because it eliminates the need for any feedback"),
                    ),
                    "Handling interaction and honoring constraints lets plants operate "
                    "closer to optimal limits than independent PID loops.",
                ),
            ),
        ),
        # -- 8. Distributed control systems and Industry 4.0 -----------
        _t(
            "Distributed control systems and Industry 4.0",
            "11 min",
            """# Distributed control systems and Industry 4.0

Modern plants do not run on one computer. A **Distributed Control System
(DCS)** spreads control across many networked controllers, each handling a
section of the plant, tied together by a common network, engineering tools,
operator **HMI** screens, and a **historian** database. Distributing the
control means no single failure stops the whole plant - and the workload
scales.

A useful mental model is the **automation pyramid**:

```text
Level 4  Enterprise / ERP        (planning, scheduling, business systems)
Level 3  MES / historian         (production management, data collection)
Level 2  SCADA / DCS supervisory (HMI, operators, alarms, APC/MPC)
Level 1  Controllers / PLC       (the PID loops, interlocks, logic)
Level 0  Field devices           (sensors, transmitters, valves)
```

Related terms: **PLC** (programmable logic controller - discrete/sequential
logic, fast interlocks), **SCADA** (supervisory control and data acquisition
- often over wide areas), and the critically important **Safety Instrumented
System (SIS)**, an *independent* layer (per IEC 61511) that trips the
process to a safe state - kept separate from the control DCS on purpose.

**Industry 4.0** is the current shift: connect all that data and add
intelligence on top.

- **Industrial IoT (IIoT)** - cheap networked sensors everywhere feeding a
  data lake.
- **Digital twin** - a live simulation of the unit, fed by real data, used
  to test changes, predict behaviour and train operators.
- **Machine learning for optimization** - models learn from historian data
  to predict quality (**soft sensors** - inferring a hard-to-measure
  composition from easy measurements), forecast equipment failure
  (**predictive maintenance**), and squeeze energy or yield beyond what a
  fixed model captures.
- **Cybersecurity** - once operational technology (OT) is networked, it must
  be defended; standards like **IEC 62443** and network segmentation matter
  as much as any control loop.

```mermaid
graph TD
    FIELD["Field sensors and valves"] --> CTRL["DCS and PLC controllers"]
    CTRL --> SUP["Supervisory HMI and historian"]
    SUP --> CLOUD["Analytics and machine learning"]
    CLOUD --> TWIN["Digital twin and soft sensors"]
    TWIN --> OPT["Optimization and predictive maintenance"]
    OPT --> CTRL
    SIS["Independent safety system SIS"] --> FIELD
```

Remember: a DCS distributes control across the plant and layers it from
field devices up to the enterprise, an independent safety system guards it,
and Industry 4.0 adds IIoT data, digital twins and machine learning on top -
while demanding serious OT cybersecurity.
""",
        ),
        quiz_lesson(
            "Quiz: Distributed control systems and Industry 4.0",
            (
                q(
                    "What is a Distributed Control System (DCS)?",
                    (
                        opt("A single PID controller on one valve"),
                        opt(
                            "Control spread across many networked controllers, each "
                            "handling a plant section, unified by a common network, HMI "
                            "and historian",
                            correct=True,
                        ),
                        opt("A spreadsheet of setpoints"),
                        opt("The chemical reactor itself"),
                    ),
                    "Distributing control avoids a single point of failure and scales "
                    "across the whole plant.",
                ),
                q(
                    "Why is a Safety Instrumented System (SIS) kept independent of the "
                    "control DCS?",
                    (
                        opt("To save money on wiring"),
                        opt(
                            "So an independent layer can trip the process to a safe state "
                            "even if the control system fails - a separation required by "
                            "safety standards like IEC 61511",
                            correct=True,
                        ),
                        opt("Because the DCS cannot read sensors"),
                        opt("Independence has no safety benefit"),
                    ),
                    "The SIS is a separate protection layer; sharing hardware with the "
                    "DCS would defeat its purpose.",
                ),
                q(
                    "What is a 'soft sensor' in an Industry 4.0 context?",
                    (
                        opt("A physical sensor made of soft plastic"),
                        opt(
                            "A model that infers a hard-to-measure variable (like "
                            "composition) from easy-to-measure ones using data or "
                            "machine learning",
                            correct=True,
                        ),
                        opt("A backup thermocouple"),
                        opt("A valve with a rubber seat"),
                    ),
                    "Soft sensors predict a quantity that is expensive or slow to "
                    "measure directly, from readily available measurements.",
                ),
                q(
                    "What new risk does networking operational technology (OT) for "
                    "Industry 4.0 introduce?",
                    (
                        opt("Higher measurement accuracy"),
                        opt(
                            "Cybersecurity exposure - connected OT must be defended with "
                            "segmentation and standards like IEC 62443",
                            correct=True,
                        ),
                        opt("Slower PID loops by law"),
                        opt("The need to remove all sensors"),
                    ),
                    "Connectivity brings data value but also attack surface; OT "
                    "cybersecurity becomes essential.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What do the three parameters of an FOPDT transfer function represent?",
                    (
                        opt("Proportional, integral, derivative gains"),
                        opt(
                            "Process gain K, time constant tau, and dead time theta",
                            correct=True,
                        ),
                        opt("Setpoint, process variable, error"),
                        opt("Flow, temperature, pressure"),
                    ),
                    "FOPDT: K (how much), tau (how fast), theta (delay before response).",
                ),
                q(
                    "A first-order process reaches what fraction of its final value "
                    "after one time constant?",
                    (
                        opt("About 63.2 percent", correct=True),
                        opt("100 percent"),
                        opt("About 5 percent"),
                        opt("It overshoots to 120 percent"),
                    ),
                    "y(tau) = 0.632 of the total change; ~95 percent at 3*tau.",
                ),
                q(
                    "What does a damping ratio zeta below 1 cause in a second-order response?",
                    (
                        opt("A sluggish overdamped approach"),
                        opt("Overshoot and oscillation before settling", correct=True),
                        opt("No response at all"),
                        opt("A permanent steady offset"),
                    ),
                    "zeta < 1 is underdamped - it rings; aggressive tuning can make a "
                    "loop behave this way.",
                ),
                q(
                    "In an orifice-plate flow meter, flow is proportional to what?",
                    (
                        opt("The differential pressure dP"),
                        opt("The square root of the differential pressure dP", correct=True),
                        opt("The square of the flow area"),
                        opt("The fluid temperature only"),
                    ),
                    "Q = Cd*A*sqrt(2*dP/rho); the square-root law limits turndown at low flow.",
                ),
                q(
                    "How is control error defined and what drives it to zero?",
                    (
                        opt("Error = PV + SP; the disturbance drives it to zero"),
                        opt(
                            "Error = SP - PV; the controller adjusts the manipulated "
                            "variable to drive it toward zero",
                            correct=True,
                        ),
                        opt("Error = valve position; the sensor drives it to zero"),
                        opt("Error is always zero by design"),
                    ),
                    "e = SP - PV; feedback moves the MV to reduce the error.",
                ),
                q(
                    "Which PID term removes steady-state offset, and which adds damping?",
                    (
                        opt("Proportional removes offset; integral adds damping"),
                        opt(
                            "Integral removes offset; derivative adds damping",
                            correct=True,
                        ),
                        opt("Derivative removes offset; proportional adds damping"),
                        opt("None of the terms affect offset or damping"),
                    ),
                    "I eliminates offset (the past), D adds anticipation/damping (the "
                    "future), P acts on the present.",
                ),
                q(
                    "What is the defining feature of cascade control?",
                    (
                        opt("Two independent valves controlled by one setpoint"),
                        opt(
                            "A slow outer loop sets the setpoint of a faster inner loop, "
                            "which acts on the valve",
                            correct=True,
                        ),
                        opt("Holding two flows in a fixed ratio"),
                        opt("Acting on a disturbance before it reaches the PV"),
                    ),
                    "Cascade nests a fast secondary loop inside a slow primary to catch "
                    "disturbances early (ratio and feedforward are different schemes).",
                ),
                q(
                    "How does feedforward control improve on feedback alone?",
                    (
                        opt("It removes the need to measure the process variable"),
                        opt(
                            "It measures a disturbance and acts before it affects the PV, "
                            "rather than waiting for an error - usually combined with "
                            "feedback",
                            correct=True,
                        ),
                        opt("It makes the process respond instantly with no dynamics"),
                        opt("It eliminates the need for any controller"),
                    ),
                    "Feedforward is proactive but model-dependent; feedback mops up the "
                    "residual, so they pair well.",
                ),
                q(
                    "What does model predictive control (MPC) do that single-loop PID cannot?",
                    (
                        opt("Run without any measurements"),
                        opt(
                            "Use a dynamic model to predict and optimize moves for many "
                            "interacting variables while explicitly respecting constraints",
                            correct=True,
                        ),
                        opt("Eliminate the need for sensors and valves"),
                        opt("Guarantee zero dead time in the process"),
                    ),
                    "MPC coordinates multivariable, constrained problems with a receding "
                    "horizon - letting plants run near their limits.",
                ),
                q(
                    "Which statement about a modern DCS and Industry 4.0 is correct?",
                    (
                        opt(
                            "A DCS is a single controller, and Industry 4.0 means "
                            "removing all networking"
                        ),
                        opt(
                            "A DCS distributes control across networked controllers, an "
                            "independent SIS provides safety, and Industry 4.0 adds IIoT "
                            "data, digital twins and machine learning (with new OT "
                            "cybersecurity needs)",
                            correct=True,
                        ),
                        opt("Industry 4.0 replaces all control loops with spreadsheets"),
                        opt("A DCS and an SIS must always share the same hardware"),
                    ),
                    "Distributed control plus an independent safety layer, with IIoT, "
                    "digital twins and ML on top - and OT security as a real concern.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PROCESS_DYNAMICS_CONTROL_COURSES: tuple[SeedCourse, ...] = (_PROCESS_DYNAMICS_CONTROL,)
