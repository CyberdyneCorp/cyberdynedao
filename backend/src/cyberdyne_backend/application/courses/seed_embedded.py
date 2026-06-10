"""Curated Embedded Systems & Microcontrollers track: Basics, Intermediate, Advanced.

A complete embedded curriculum: MCU anatomy and bare-metal firmware (GPIO,
memory-mapped registers, the super-loop, timers/PWM, ADC/buttons), the
intermediate firmware toolkit (interrupts/NVIC, UART/SPI/I2C buses, advanced
timers, power management, event-driven state machines), and the advanced layer
(RTOS tasks and synchronization, DMA, debugging/testing, real-time scheduling,
and real-world applications). MCU firmware is shown in C; the runnable labs are
Python (numpy + matplotlib). Interactive ```plot blocks, Mermaid diagrams, LaTeX
formulas, and concrete real-world use cases throughout.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Embedded Systems & Microcontrollers -- Basics -----------------------------

_EMBEDDED_BASICS = SeedCourse(
    slug="embedded-basics",
    title="Embedded Systems & Microcontrollers -- Basics",
    description=(
        "Bare-metal firmware from the ground up: what an embedded system is and "
        "MCU anatomy, GPIO and memory-mapped registers, the startup/vector-table/"
        "super-loop program, timers and PWM, and reading the world with ADCs and "
        "buttons - with side-by-side C firmware and Python, interactive plots, and "
        "a runnable button-debounce + PWM lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is an embedded system & MCU anatomy",
            "11 min",
            """\
# What is an embedded system & MCU anatomy

An **embedded system** is a computer hidden inside a product to do one job: a
washing machine controller, a car's engine ECU, a pacemaker, a drone flight
controller, a smart thermostat. You never "boot it up" - it just runs. At its
heart is a **microcontroller (MCU)**: a whole computer on one chip.

## What is on the chip

| Block | Role | Typical Cortex-M part |
|-------|------|-----------------------|
| **CPU core** | runs instructions | ARM Cortex-M0/M3/M4 |
| **Flash** | non-volatile **program** storage | 16 KB - 2 MB |
| **RAM (SRAM)** | volatile **data** (variables, stack) | 2 KB - 512 KB |
| **Peripherals** | GPIO, timers, ADC, UART, SPI, I2C, DMA | dozens |
| **Clock + power** | oscillators, PLL, regulators | on-chip |

A microcontroller differs from the microprocessor in your laptop: the MCU has
flash, RAM, and peripherals **on the same die**, runs without an operating
system, and is measured in kilobytes and milliwatts, not gigabytes and watts.

## Harvard vs von Neumann

- **von Neumann** - one bus for instructions and data (your PC).
- **Harvard** - separate program and data paths, so the CPU can fetch an
  instruction and a datum at the same time. Most MCUs are Harvard-ish, which is
  why code runs from flash while variables live in RAM.

```mermaid
flowchart LR
  CPU["Cortex-M CPU"] --- FLASH["flash (program)"]
  CPU --- RAM["SRAM (data)"]
  CPU --- PERIPH["peripherals: GPIO / timers / ADC / UART"]
  CLK["clock + power"] --- CPU
```

## A bit of history

- **1971 - Intel 4004**, the first single-chip CPU, built for a calculator.
- **1976 - Intel 8048**, an early true microcontroller (CPU + RAM + I/O on one
  chip); the **8051** (1980) became the most-cloned MCU ever.
- **2004 - ARM Cortex-M**, a family designed for embedded: deterministic, low
  power, easy interrupts. Today it dominates - it is the CPU inside STM32, the
  Raspberry Pi Pico (RP2040), Nordic radios, and countless others.

## The throughline of this course

A modern car has 50-100 MCUs; a phone has dozens. They all share the same
skeleton: a CPU executes firmware from flash, reads sensors and drives outputs
through peripherals, and reacts to the world in real time. Memory sizes scale
with the job - watch how RAM grows with the task:

```plot
{"title": "MCU RAM needed grows roughly with task complexity", "xLabel": "task complexity (relative)", "yLabel": "RAM needed (KB)", "xRange": [1, 10], "yRange": [0, 260], "grid": true, "controls": [{"name": "k", "range": [1, 4], "value": 2, "label": "data per feature (KB)"}], "functions": [{"expr": "k*x*x", "label": "RAM ~ k * complexity^2"}]}
```

**Next:** talking to peripherals through memory-mapped registers.
""",
        ),
        _t(
            "GPIO & memory-mapped registers",
            "12 min",
            """\
# GPIO & memory-mapped registers

The simplest peripheral is **GPIO** (General-Purpose Input/Output): a pin you
can drive high/low or read. It is how an MCU blinks an LED, reads a button,
toggles a relay, or bit-bangs a protocol.

## Memory-mapped I/O

There is no special "output" instruction. Peripherals appear as **registers at
fixed memory addresses** - writing a 32-bit word to address `0x48000014` sets
output pins. The **datasheet** (and "reference manual") gives you the map: a base
address per peripheral plus an offset and bit layout per register.

| Register | Job |
|----------|-----|
| **MODER** | direction: input / output / alternate / analog |
| **ODR** | output data: the level each pin drives |
| **IDR** | input data: the level read on each pin (read-only) |
| **BSRR** | atomic set/reset of individual bits |

## Bit manipulation: the heartbeat of firmware

You rarely write a whole register - you change **specific bits** while leaving
the rest alone. The three idioms, with `(1 << n)` selecting bit $n$:

```c
REG |=  (1u << n);   // set bit n      (turn on)
REG &= ~(1u << n);   // clear bit n    (turn off)
REG ^=  (1u << n);   // toggle bit n   (flip)
if (REG & (1u << n)) { /* bit n is high */ }
```

```python
reg |=  (1 << n)     # set bit n
reg &= ~(1 << n)     # clear bit n
reg ^=  (1 << n)     # toggle bit n
is_high = bool(reg & (1 << n))   # test bit n
```

## Blinking an LED (the embedded "hello world")

In C against the registers (conceptually, an STM32-style port):

```c
#define GPIOA_MODER (*(volatile unsigned*)0x48000000)
#define GPIOA_ODR   (*(volatile unsigned*)0x48000014)

GPIOA_MODER |=  (1u << (5 * 2));   // PA5 = output (01 in its 2-bit field)
GPIOA_ODR   |=  (1u << 5);         // LED on
GPIOA_ODR   &= ~(1u << 5);         // LED off
```

The `volatile` keyword is critical: it tells the compiler the value can change
outside the program (hardware), so it must **really** read/write memory every
time and not optimise the access away.

## Why bit math, visually

A single 8-bit register holds eight independent on/off lines. Slide which bit you
flip and see only that pin's value change:

```plot
{"title": "Setting bit n of a register lights only pin n (8-bit port)", "xLabel": "pin index", "yLabel": "pin level (after set bit n)", "xRange": [0, 7], "yRange": [-0.2, 1.4], "grid": true, "controls": [{"name": "n", "range": [0, 7], "value": 3, "label": "bit to set"}], "functions": [{"expr": "(round(x)==round(n))*1", "label": "pin = (index == n)"}]}
```

> **Practical insight:** use **BSRR** (a dedicated set/reset register) instead of
> read-modify-write on ODR when an interrupt might touch the same port - it is
> atomic and avoids a race.

**Next:** how the program actually starts running - bare metal.
""",
        ),
        _t(
            "The bare-metal program: startup, vector table & super-loop",
            "12 min",
            """\
# The bare-metal program: startup, vector table & super-loop

On a PC an operating system loads and starts your program. On a bare-metal MCU,
**there is no OS** - your firmware is everything, and you must understand exactly
how the CPU comes alive.

## Reset and the vector table

When power is applied (or reset is pressed), a Cortex-M does something very
specific: it reads two 32-bit words from the start of flash.

1. The **first word** is the initial **stack pointer**.
2. The **second word** is the **reset vector** - the address of `Reset_Handler`.

Those words live in the **vector table**: an array of handler addresses, one per
exception and interrupt, that the hardware indexes into automatically.

```mermaid
flowchart TB
  RST["power-on / reset"] --> SP["load initial stack pointer (word 0)"]
  SP --> RH["jump to Reset_Handler (word 1)"]
  RH --> INIT["copy .data to RAM, zero .bss"]
  INIT --> MAIN["call main()"]
```

## Startup code

Before `main()` can run, the **startup code** (often `startup.s` plus a tiny C
routine) must: copy initialised variables from flash into RAM (the `.data`
section), zero out uninitialised globals (`.bss`), set up the clock, and only
then call `main()`. The **linker script** decides what goes in flash vs RAM.

## The super-loop

A `main()` in embedded almost never returns - it loops forever:

```c
int main(void) {
    clock_init();
    gpio_init();
    while (1) {            // the super-loop: runs until power is removed
        read_sensors();
        update_outputs();
    }
}
```

```python
# The same shape, simulated (one frame of the loop per iteration):
clock_init = lambda: None
while True:
    sensors = read_sensors()
    update_outputs(sensors)
    break   # a real MCU never breaks; it runs forever
```

## Polling vs interrupts

Inside that loop you get information two ways:

- **Polling** - repeatedly *ask* a peripheral ("is the button pressed yet?").
  Simple, but wastes CPU and may miss fast events.
- **Interrupts** - the peripheral *tells* the CPU by triggering an **ISR**
  (Interrupt Service Routine), which preempts the loop, handles the event, and
  returns. Responsive and power-efficient, but harder to reason about.

A polling loop's response time depends on how long one loop iteration takes -
add work and your worst-case latency grows linearly:

```plot
{"title": "Polling latency grows with super-loop work per pass", "xLabel": "tasks in the loop", "yLabel": "worst-case response (ms)", "xRange": [1, 20], "yRange": [0, 22], "grid": true, "controls": [{"name": "ms", "range": [0.2, 2], "value": 1, "label": "time per task (ms)"}], "functions": [{"expr": "ms*x", "label": "latency = tasks * time-per-task"}]}
```

> **Practical insight:** start with a clean super-loop; move only the
> **time-critical or rare** events to interrupts. A loop that does too much grows
> sluggish; an interrupt that does too much starves the loop.

**Next:** counting time precisely with timers and PWM.
""",
        ),
        _t(
            "Timers & PWM",
            "12 min",
            """\
# Timers & PWM

A **timer/counter** is a peripheral that counts clock ticks in hardware,
independent of the CPU. It is how an MCU measures time, generates periodic
interrupts, and produces **PWM** - the workhorse for dimming LEDs, driving
servos, and controlling motor speed.

## Counters and prescalers

A timer increments a counter at the peripheral clock rate. A **prescaler**
divides that clock first, so you can hit slow rates without a huge counter. With
clock $f_{clk}$, prescaler $PSC$, and auto-reload $ARR$, the timer overflows at:

$$f_{tick} = \\frac{f_{clk}}{(PSC + 1)(ARR + 1)}.$$

To blink an LED at 1 Hz from a 48 MHz clock you pick $PSC$ and $ARR$ whose
product is 48 million. Slide the prescaler and watch the output frequency drop:

```plot
{"title": "Timer overflow frequency vs prescaler (ARR=999, 48 MHz)", "xLabel": "prescaler PSC", "yLabel": "overflow frequency (Hz)", "xRange": [0, 100], "yRange": [0, 50], "grid": true, "controls": [{"name": "arr", "range": [199, 1999], "value": 999, "label": "auto-reload ARR"}], "functions": [{"expr": "48000000/((x+1)*(arr+1))", "label": "f_overflow"}]}
```

## PWM: pretending to be analog

**Pulse-Width Modulation** drives a pin high for a fraction of each period - the
**duty cycle** $D$ - and low for the rest. The *average* voltage is $D \\cdot
V_{cc}$, so a slow load (an LED's brightness, a motor's torque, an RC-filtered
output) behaves as if you fed it an analog value:

$$V_{avg} = D \\cdot V_{cc}, \\qquad D = \\frac{t_{on}}{t_{on} + t_{off}}.$$

Slide the duty cycle and watch the PWM waveform's average rise (the dashed
intuition is the average level):

```plot
{"title": "PWM waveform: average tracks the duty cycle (slide D)", "xLabel": "time (one period)", "yLabel": "pin level", "xRange": [0, 4], "yRange": [-0.2, 1.3], "grid": true, "controls": [{"name": "D", "range": [0.05, 0.95], "value": 0.4, "label": "duty cycle D"}], "functions": [{"expr": "((x - floor(x)) < D)*1", "label": "PWM out"}, {"expr": "D", "label": "average level"}]}
```

## Hobby servo: PWM as position

An RC servo reads a **pulse width**, not a duty cycle: a 20 ms frame with a
1.0-2.0 ms high pulse maps to 0-180 degrees. The angle is linear in pulse width:

```plot
{"title": "Servo angle vs pulse width (1.0-2.0 ms -> 0-180 deg)", "xLabel": "pulse width (ms)", "yLabel": "servo angle (deg)", "xRange": [1, 2], "yRange": [0, 180], "grid": true, "functions": [{"expr": "180*(x - 1)", "label": "angle = 180*(pw - 1ms)"}]}
```

```c
// STM32-style: set PWM duty to 40% on a timer with ARR = 999
TIM3->ARR = 999;          // period
TIM3->CCR1 = 400;         // compare value -> 400/1000 = 40% duty
```

```python
arr = 999
duty = 0.40
ccr1 = round(duty * (arr + 1))   # compare value the timer reloads against
```

> **Practical insight:** higher PWM frequency = smoother averaging and quieter
> motors, but more switching loss. LEDs need >~100 Hz to look steady; motor
> drives often run 16-20 kHz to push the whine above hearing.

**Next:** reading analog signals and noisy buttons.
""",
        ),
        _t(
            "Reading the world: ADC & buttons",
            "11 min",
            """\
# Reading the world: ADC & buttons

The world is analog - temperatures, light, voltages, audio. An **ADC**
(Analog-to-Digital Converter) turns a voltage into a number the CPU can use, and
buttons (deceptively simple) need **debouncing** to read reliably.

## The ADC: sampling and quantising

An ADC measures an input voltage against a reference $V_{ref}$ and reports an
integer code. With $N$ bits the range $0..V_{ref}$ splits into $2^N$ steps:

$$\\text{code} = \\left\\lfloor \\frac{V_{in}}{V_{ref}}\\,(2^N - 1) \\right\\rfloor,
\\qquad \\text{resolution} = \\frac{V_{ref}}{2^N}.$$

A 12-bit ADC (common on Cortex-M) gives 4096 steps; on a 3.3 V reference that is
~0.8 mV per step. More bits = finer steps - the staircase that maps voltage to
code gets taller as you add resolution:

```plot
{"title": "ADC transfer: more bits = more steps (slide bit depth)", "xLabel": "input fraction of Vref", "yLabel": "ADC code / max", "xRange": [0, 1], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "levels", "range": [4, 32], "value": 8, "label": "quantisation levels"}], "functions": [{"expr": "floor(x*levels)/levels", "label": "quantised code (normalised)"}]}
```

You also must respect the **sampling rate**: to capture a signal you must sample
at more than twice its highest frequency (the Nyquist rate), or you get
**aliasing** (a fast signal masquerading as a slow one).

## Buttons bounce

A mechanical switch does not close cleanly - its contacts physically **bounce**
for a few milliseconds, producing a burst of fake transitions. Read it raw and
one press registers as many. The noisy contact signal looks like this:

```plot
{"title": "A bouncing contact: many fast edges around one real press", "xLabel": "time (ms)", "yLabel": "raw pin level", "xRange": [0, 12], "yRange": [-0.2, 1.3], "grid": true, "functions": [{"expr": "(x>2)*( ((x<5)*( (sin(18*x)>0)*1 )) + (x>=5)*1 )", "label": "raw bouncing input"}]}
```

## Debouncing: trust a level only if it is stable

The standard fix: sample the pin periodically and only accept a new state after
it has read the same value for a few consecutive samples (e.g. 20 ms of
stability). Hardware (an RC + Schmitt trigger) can help, but firmware debouncing
is cheap and flexible.

```c
// Accept a change only after it is stable for STABLE samples (polled in a tick)
if (raw == last_raw) { stable_count++; }
else { stable_count = 0; last_raw = raw; }
if (stable_count >= STABLE) { button_state = raw; }
```

```python
if raw == last_raw:
    stable_count += 1
else:
    stable_count = 0
    last_raw = raw
if stable_count >= STABLE:
    button_state = raw
```

> **Practical insight:** debounce in the **time domain** (require stability),
> not by adding delays in the main loop. Around 10-30 ms is the usual window -
> long enough to outlast bounce, short enough to feel instant.

**Next:** put debouncing and PWM together in a runnable lab.
""",
        ),
        _code(
            "Lab: button debounce + PWM duty waveform",
            "13 min",
            """\
# Simulate a noisy button being debounced, and a PWM output whose duty cycle
# steps up each clean press. Watch the raw chatter get rejected and the PWM
# average climb. Pure numpy + matplotlib, no hardware needed.
import numpy as np
import matplotlib.pyplot as plt

fs = 1000                       # 1 kHz sampling tick (1 ms per sample)
T = 0.6                         # 600 ms of simulation
t = np.arange(0, T, 1/fs)
n = len(t)

# --- 1. Build a noisy (bouncing) raw button signal: three real presses,
#        each surrounded by a few ms of chatter. ---
rng = np.random.default_rng(7)
raw = np.zeros(n, dtype=int)
press_windows = [(0.10, 0.25), (0.30, 0.42), (0.48, 0.58)]
for (a, b) in press_windows:
    idx = (t >= a) & (t < b)
    raw[idx] = 1
# inject bounce: random flips only in the 8 ms right after each edge
for (a, b) in press_windows:
    edge = (t >= a) & (t < a + 0.008)
    raw[edge] = rng.integers(0, 2, size=int(edge.sum()))

# --- 2. Debounce: accept a new level only after STABLE consecutive samples. ---
STABLE = 15                     # 15 ms of stability required
debounced = np.zeros(n, dtype=int)
state = 0
last = raw[0]
count = 0
for k in range(n):
    if raw[k] == last:
        count += 1
    else:
        count = 0
        last = raw[k]
    if count >= STABLE:
        state = raw[k]
    debounced[k] = state

# --- 3. Count clean rising edges; each press bumps PWM duty by 25%. ---
rising = (debounced[1:] == 1) & (debounced[:-1] == 0)
duty = np.zeros(n)
d = 0.0
for k in range(1, n):
    if rising[k - 1]:
        d = min(1.0, d + 0.25)
    duty[k] = d

# --- 4. Synthesize a 50 Hz PWM carrier modulated by the duty schedule. ---
carrier_phase = (t * 50.0) % 1.0
pwm = (carrier_phase < duty).astype(float)
presses = int(rising.sum())

fig, ax = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
ax[0].plot(t * 1000, raw, color="#94a3b8")
ax[0].set_ylabel("raw"); ax[0].set_title(f"Raw bouncing input ({presses} clean presses detected)")
ax[1].plot(t * 1000, debounced, color="#2563eb", lw=2)
ax[1].set_ylabel("debounced")
ax[2].plot(t * 1000, pwm, color="#dc2626", lw=1)
ax[2].plot(t * 1000, duty, color="#16a34a", lw=2, label="duty (average)")
ax[2].set_ylabel("PWM"); ax[2].set_xlabel("time (ms)"); ax[2].legend(loc="upper left")
for a in ax:
    a.grid(True); a.set_ylim(-0.2, 1.3)
plt.tight_layout(); plt.show()

print(f"clean presses detected: {presses}  (expected 3)")
print(f"final PWM duty cycle: {duty[-1] * 100:.0f}%")

# Try it yourself:
#   1. Lower STABLE to 3: bounce leaks through and you over-count presses.
#   2. Change the +0.25 step to +0.10 for a finer brightness ramp.
""",
        ),
    ),
)


# -- Embedded Systems & Microcontrollers -- Intermediate -----------------------

_EMBEDDED_INTERMEDIATE = SeedCourse(
    slug="embedded-intermediate",
    title="Embedded Systems & Microcontrollers -- Intermediate",
    description=(
        "The working firmware toolkit: interrupts and the NVIC in depth, the "
        "UART/SPI/I2C serial buses, advanced timer modes (input capture, output "
        "compare, watchdog), power management and sleep modes, and event-driven "
        "state machines - with side-by-side C and Python, interactive plots, and a "
        "runnable UART-frame / FSM lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Interrupts in depth: NVIC, priorities & latency",
            "12 min",
            """\
# Interrupts in depth: NVIC, priorities & latency

An **interrupt** lets hardware grab the CPU the instant something happens - a
byte arrives, a timer overflows, a pin changes - instead of the CPU polling for
it. On Cortex-M the traffic controller is the **NVIC** (Nested Vectored
Interrupt Controller).

## How an interrupt fires

```mermaid
flowchart TB
  EVT["peripheral event (e.g. UART byte)"] --> PEND["NVIC marks IRQ pending"]
  PEND --> CMP{"priority > current?"}
  CMP -->|yes| PUSH["CPU pushes context, vectors to ISR"]
  PUSH --> ISR["run ISR_Handler"]
  ISR --> POP["restore context, resume program"]
  CMP -->|no| WAIT["stays pending until allowed"]
```

The NVIC is **vectored** (each IRQ has its own handler address in the vector
table - no scanning needed) and **nested** (a higher-priority interrupt can
preempt one already running).

## Priorities and preemption

Each interrupt has a **priority number** - and on Cortex-M, **lower number =
higher priority**. A higher-priority IRQ preempts a running lower-priority ISR;
equal priorities wait their turn. You split the priority bits into
**preemption** (can interrupt others) and **sub-priority** (tie-break order)
groups.

## Latency

**Interrupt latency** is the delay from the event to the first instruction of
your ISR. On Cortex-M the hardware entry is a fixed ~12 cycles, but the *total*
latency you actually see is inflated by any higher- or equal-priority ISR
already running, and by code that disables interrupts. The more time spent with
interrupts masked, the worse the worst case:

```plot
{"title": "Worst-case interrupt latency vs time spent with IRQs masked", "xLabel": "longest critical section (us)", "yLabel": "worst-case latency (us)", "xRange": [0, 20], "yRange": [0, 25], "grid": true, "controls": [{"name": "entry", "range": [0.1, 3], "value": 0.5, "label": "hardware entry (us)"}], "functions": [{"expr": "x + entry", "label": "latency = mask time + entry"}]}
```

## ISR best practices

- **Keep ISRs short.** Do the urgent minimum (grab the byte, clear the flag, set
  a flag/queue an event) and let the main loop do the heavy work.
- **Clear the interrupt flag**, or it re-fires forever.
- **Share data carefully.** Variables touched by both an ISR and the main code
  must be `volatile`, and multi-byte updates need a brief critical section.

```c
volatile uint8_t rx_byte;
volatile uint8_t rx_ready;

void USART2_IRQHandler(void) {     // short and sharp
    rx_byte  = USART2->RDR;        // read clears the RXNE flag
    rx_ready = 1;                  // signal the main loop
}
```

```python
rx_byte = 0
rx_ready = False

def on_uart_irq(received):   # conceptual ISR: do the minimum, signal, return
    global rx_byte, rx_ready
    rx_byte = received
    rx_ready = True
```

> **Practical insight:** never call slow or blocking code (printf, a long delay,
> a flash write) inside an ISR. The golden rule is "ISRs signal, the main loop
> works."

**Next:** the three serial buses every embedded engineer must know.
""",
        ),
        _t(
            "Serial buses: UART, SPI & I2C",
            "13 min",
            """\
# Serial buses: UART, SPI & I2C

Chips talk to each other (and to your PC) over a handful of **serial buses**.
Three dominate embedded; knowing when to use which is core skill.

## UART - asynchronous, point to point

**UART** sends bytes over a single wire each way (TX, RX) with **no shared
clock** - both ends just agree on a **baud rate** (e.g. 115200 bit/s). Each byte
is framed: a start bit, 8 data bits, optional parity, and a stop bit.

$$t_{byte} \\approx \\frac{10}{\\text{baud}} \\;\\text{seconds (8N1: 1 start + 8 data + 1 stop)}.$$

Higher baud = shorter byte time, so throughput rises with baud rate:

```plot
{"title": "UART byte time vs baud rate (8N1 = 10 bits/byte)", "xLabel": "baud rate (kbit/s)", "yLabel": "time per byte (us)", "xRange": [9.6, 460.8], "yRange": [0, 1100], "grid": true, "functions": [{"expr": "10000/x", "label": "t_byte = 10 / baud"}]}
```

It is great for debug consoles, GPS modules, and chip-to-PC links - but only two
devices, and a baud-rate mismatch garbles everything.

## SPI - fast, synchronous, full duplex

**SPI** uses a shared **clock (SCLK)** from one controller plus **MOSI**, **MISO**,
and one **chip-select (CS)** per peripheral. Data shifts in and out on clock
edges - so it is **full duplex** and **fast** (tens of MHz). Cost: a wire per
peripheral for CS, and no built-in acknowledgement.

```mermaid
flowchart LR
  C["controller"] -->|SCLK| P1["sensor"]
  C -->|MOSI| P1
  P1 -->|MISO| C
  C -->|CS1| P1
```

Use it for SD cards, displays, fast ADCs/DACs, and radios - anything
high-throughput.

## I2C - two wires, many devices, addressed

**I2C** needs only **two wires** (SDA data, SCL clock, both open-drain with
pull-ups) and puts many devices on the same bus, each with a **7-bit address**.
A transaction is: start, address + R/W, then bytes each **acknowledged** by the
receiver, then stop.

| Bus | Wires | Clock | Speed | Best for |
|-----|-------|-------|-------|----------|
| **UART** | 2 (+gnd) | none (async) | low-med | PC/debug, GPS, modems |
| **SPI** | 3 + 1 CS each | shared | very high | displays, SD, ADC, radio |
| **I2C** | 2 | shared | low-med | many small sensors on one bus |

```c
// I2C read of 1 byte from register reg of a 7-bit-address device (HAL-style)
uint8_t value;
HAL_I2C_Mem_Read(&hi2c1, dev_addr << 1, reg, 1, &value, 1, 100);
```

```python
# Same idea on a Linux/MicroPython-style I2C object:
value = i2c.readfrom_mem(dev_addr, reg, 1)   # read 1 byte from register `reg`
```

> **Practical insight:** pick by need - **I2C** when pins are scarce and many
> slow sensors share a bus, **SPI** when you need speed, **UART** for a simple
> two-party or PC link. Forgetting I2C pull-up resistors is the classic
> first-day bug.

**Next:** the timer's advanced tricks - capture, compare, and the watchdog.
""",
        ),
        _t(
            "Advanced timers: input capture, output compare & watchdog",
            "12 min",
            """\
# Advanced timers: input capture, output compare & watchdog

The Basics course used a timer to count and make PWM. The same peripheral has
powerful modes that measure and react to events with hardware precision.

## Input capture - timestamp an edge

In **input capture** the timer **latches its counter value** the instant a pin
edge arrives. Capture two edges and the difference is a precise time interval -
no CPU polling, no jitter. Uses: measuring a pulse width, decoding an RC
receiver, or computing **frequency** from the period between rising edges.

$$f_{signal} = \\frac{f_{timer}}{\\Delta\\text{count}}.$$

A shorter captured period means a higher measured frequency (inverse relation):

```plot
{"title": "Measured frequency from captured period (1 MHz timer)", "xLabel": "captured period (timer counts)", "yLabel": "measured frequency (kHz)", "xRange": [10, 1000], "yRange": [0, 100], "grid": true, "functions": [{"expr": "1000/x", "label": "f = f_timer / delta-count"}]}
```

## Output compare - act at an exact time

**Output compare** flips a pin (or fires an interrupt) the moment the counter
reaches a programmed value - PWM is a special case. It lets you generate precise
edges, one-shot pulses, or periodic events with zero software jitter, because the
**hardware** does the timing.

## The watchdog - the firmware safety net

A **watchdog timer** counts down and **resets the MCU** if it ever reaches zero.
Your firmware must "kick" (reload) it periodically; if the code hangs - stuck in
a loop, crashed in an ISR - the kicks stop and the watchdog reboots the system.
It is mandatory in cars, medical, and industrial gear.

```mermaid
flowchart LR
  RUN["firmware running"] -->|periodic kick| WDT["watchdog counter"]
  WDT -->|reaches 0| RESET["MCU reset"]
  RESET --> RUN
```

```c
// Configure input capture on TIM2 CH1, then read captured period each event
IC_init(TIM2);                       // rising-edge capture into CCR1
uint32_t t1 = capture_wait(TIM2);    // first edge timestamp
uint32_t t2 = capture_wait(TIM2);    // second edge timestamp
uint32_t period = t2 - t1;           // counts between edges
IWDG_kick();                         // pet the watchdog so it does not reset us
```

```python
# Measure frequency from two captured edge timestamps (timer counts)
f_timer = 1_000_000
t1, t2 = 1500, 2500
period = t2 - t1
f_signal = f_timer / period          # 1 kHz
```

> **Practical insight:** always set the watchdog *longer* than your worst-case
> loop, and kick it from **one** well-understood place (not scattered everywhere,
> or a half-hung program keeps petting it and defeats the point).

**Next:** doing more with less - power management and sleep.
""",
        ),
        _t(
            "Power management & sleep modes",
            "11 min",
            """\
# Power management & sleep modes

A coin-cell sensor or a wearable must run for months on a tiny battery. The CPU
is idle most of the time, so the art is **sleeping aggressively** and waking only
when needed.

## Where the power goes

MCU current has two parts: **dynamic** power, proportional to clock frequency and
to capacitance switching each cycle, and **static** (leakage) power that flows
even when idle. Dynamic power scales with the square of voltage and linearly with
frequency:

$$P_{dynamic} = C\\,V^2 f.$$

So halving the clock roughly halves dynamic power - clock down when you can:

```plot
{"title": "Dynamic power scales with clock frequency (slide voltage)", "xLabel": "clock frequency (MHz)", "yLabel": "dynamic power (relative)", "xRange": [1, 48], "yRange": [0, 12], "grid": true, "controls": [{"name": "V", "range": [1, 3.3], "value": 3.3, "label": "core voltage (V)"}], "functions": [{"expr": "0.02*V*V*x", "label": "P = C V^2 f"}]}
```

## Clock gating and the sleep ladder

Two big levers:

- **Clock gating** - turn off the clock to peripherals you are not using. No
  clock means almost no dynamic power in that block.
- **Sleep modes** - a ladder from light to deep, trading wake-up speed for
  current:

| Mode | What is on | Wake-up | Typical current |
|------|------------|---------|-----------------|
| **Run** | everything | -- | mA |
| **Sleep** | CPU clock off, peripherals on | instant (any IRQ) | ~hundreds uA |
| **Stop** | clocks off, RAM kept | fast (a few us) | ~uA |
| **Standby** | almost all off, RAM lost | slow (reset-like) | ~nA-uA |

The deeper you sleep, the lower the average current but the longer the wake-up.
The classic pattern: do a quick burst of work, then **sleep until the next
interrupt** (a timer tick or a pin edge).

```c
// Burst-then-sleep: handle the event, then halt the CPU until the next IRQ
handle_event();
__WFI();              // Wait For Interrupt: CPU sleeps; an IRQ wakes it
```

```python
# Average current = duty * active + (1 - duty) * sleep
active_mA, sleep_mA = 10.0, 0.005
duty = 0.02                                  # awake 2% of the time
avg_mA = duty * active_mA + (1 - duty) * sleep_mA
months = (220.0 / avg_mA) / 24 / 30          # 220 mAh coin cell
```

> **Practical insight:** the **average** current sets battery life, and it is
> dominated by how often and how long you are awake. Wake, work fast, sleep -
> and gate every peripheral you are not actively using.

**Next:** structuring firmware as events and states.
""",
        ),
        _t(
            "Event-driven firmware & state machines",
            "12 min",
            """\
# Event-driven firmware & state machines

As firmware grows, a flat super-loop full of flags becomes a tangle. The cure is
to think in **events** and **states**: the system sits in a well-defined state
and **transitions** when an event arrives.

## Three ways to structure firmware

| Approach | Idea | Good for |
|----------|------|----------|
| **Super-loop** | poll everything every pass | tiny, simple devices |
| **FSM** (finite state machine) | explicit states + transitions | most event-driven firmware |
| **RTOS** | independent tasks + a scheduler | complex, multi-rate systems (Advanced) |

The FSM is the sweet spot for an enormous range of products: a vending machine,
a microwave, a BLE connection, a charger's charge cycle.

## A finite state machine

Define the **states**, the **events**, and the **transition** for each (state,
event) pair. Example: a door lock.

```mermaid
stateDiagram-v2
  [*] --> Locked
  Locked --> Unlocked: correct_code
  Locked --> Alarm: too_many_tries
  Unlocked --> Locked: timeout
  Alarm --> Locked: reset
```

The whole behaviour lives in one readable table, not scattered flags. Adding a
state or event is a local change, and it is easy to prove every case is handled.

```c
typedef enum { LOCKED, UNLOCKED, ALARM } State;
State next_state(State s, Event e) {
    switch (s) {
        case LOCKED:
            if (e == CORRECT_CODE)    return UNLOCKED;
            if (e == TOO_MANY_TRIES)  return ALARM;
            return LOCKED;
        case UNLOCKED:
            return (e == TIMEOUT) ? LOCKED : UNLOCKED;
        case ALARM:
            return (e == RESET) ? LOCKED : ALARM;
    }
    return s;
}
```

```python
TRANSITIONS = {
    ("LOCKED", "correct_code"): "UNLOCKED",
    ("LOCKED", "too_many_tries"): "ALARM",
    ("UNLOCKED", "timeout"): "LOCKED",
    ("ALARM", "reset"): "LOCKED",
}
state = "LOCKED"
event = "correct_code"
state = TRANSITIONS.get((state, event), state)   # -> "UNLOCKED"
```

## Event-driven plus sleep = efficient

Combine the FSM with the power lesson: stay asleep until an **event** (an
interrupt-posted message) arrives, process the transition, then sleep again. CPU
activity becomes a series of short spikes around events instead of a busy loop:

```plot
{"title": "Event-driven CPU activity: short bursts, mostly idle", "xLabel": "time", "yLabel": "CPU active", "xRange": [0, 12], "yRange": [-0.2, 1.3], "grid": true, "functions": [{"expr": "(abs(x-2)<0.3) + (abs(x-5)<0.3) + (abs(x-9)<0.3)", "label": "active during events only"}]}
```

> **Practical insight:** if you find yourself adding "mode" booleans and nested
> ifs to a super-loop, you have an implicit state machine - make it explicit. A
> transition table is easier to test, document, and hand to the next engineer.

**Next:** decode a serial frame and drive an FSM in a runnable lab.
""",
        ),
        _code(
            "Lab: UART frame decode + FSM byte parser",
            "13 min",
            """\
# Decode a UART byte stream with a finite state machine. The device sends framed
# packets:  [STX] [LEN] [payload...] [CHK]  where CHK is the XOR of the payload.
# We simulate the wire (with one corrupted frame) and run an FSM byte-by-byte,
# the way real firmware parses an interrupt-fed RX buffer. numpy + matplotlib.
import numpy as np
import matplotlib.pyplot as plt

STX = 0x02

# --- Build a byte stream of three frames; the middle one is corrupted. ---
def make_frame(payload, corrupt=False):
    chk = 0
    for b in payload:
        chk ^= b
    if corrupt:
        chk ^= 0xFF                      # break the checksum
    return [STX, len(payload)] + list(payload) + [chk]

stream = []
stream += [0x00, 0x00]                    # idle garbage before sync
stream += make_frame([0x41, 0x42, 0x43])  # "ABC"  -> good
stream += make_frame([0x10, 0x20], corrupt=True)  # bad checksum
stream += make_frame([0x55])              # good
stream = np.array(stream, dtype=int)

# --- FSM parser: WAIT_STX -> READ_LEN -> READ_PAYLOAD -> READ_CHK. ---
state = "WAIT_STX"
length = 0
payload = []
acc_chk = 0
state_trace = []
states = {"WAIT_STX": 0, "READ_LEN": 1, "READ_PAYLOAD": 2, "READ_CHK": 3}
good_frames = []
bad_frames = 0

for b in stream:
    state_trace.append(states[state])
    if state == "WAIT_STX":
        if b == STX:
            state = "READ_LEN"
    elif state == "READ_LEN":
        length = b
        payload = []
        acc_chk = 0
        state = "READ_PAYLOAD" if length > 0 else "READ_CHK"
    elif state == "READ_PAYLOAD":
        payload.append(b)
        acc_chk ^= b
        if len(payload) == length:
            state = "READ_CHK"
    elif state == "READ_CHK":
        if b == acc_chk:
            good_frames.append(bytes(payload))
        else:
            bad_frames += 1
        state = "WAIT_STX"

print("good frames:", [p.decode("ascii", "replace") for p in good_frames])
print("rejected (bad checksum):", bad_frames)

plt.figure(figsize=(9, 3.5))
plt.step(np.arange(len(stream)), state_trace, where="post", color="#2563eb")
plt.yticks(list(states.values()), list(states.keys()))
plt.xlabel("byte index in stream"); plt.title("UART frame parser FSM walking the byte stream")
plt.grid(True, axis="x"); plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Flip corrupt=False on the middle frame: rejected count drops to 0.
#   2. Truncate the stream mid-frame: the FSM safely waits in READ_PAYLOAD.
""",
        ),
    ),
)


# -- Embedded Systems & Microcontrollers -- Advanced ---------------------------

_EMBEDDED_ADVANCED = SeedCourse(
    slug="embedded-advanced",
    title="Embedded Systems & Microcontrollers -- Advanced",
    description=(
        "The advanced firmware layer: RTOS fundamentals (tasks, scheduler, "
        "preemption, context switch), synchronization (semaphores, mutexes, "
        "queues, priority inversion), DMA and high-throughput peripherals, "
        "debugging and testing (SWD/JTAG, logic analyzers, HIL), real-time "
        "scheduling theory, and real-world applications - with side-by-side C and "
        "Python, interactive plots, and a runnable preemptive-scheduler lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "RTOS fundamentals: tasks, scheduler & context switch",
            "13 min",
            """\
# RTOS fundamentals: tasks, scheduler & context switch

When a system has many jobs running at different rates - read a sensor at 100 Hz,
update a display at 10 Hz, service a radio whenever it interrupts - a single
super-loop gets brittle. A **Real-Time Operating System (RTOS)** lets you write
each job as an independent **task** and have a **scheduler** share the one CPU
between them.

## Tasks and the scheduler

A **task** is a function with its own **stack** that looks like it has the CPU to
itself. The **scheduler** decides which ready task runs now. Each task is in one
of a few states:

```mermaid
stateDiagram-v2
  [*] --> Ready
  Ready --> Running: scheduler picks it
  Running --> Ready: preempted / yields
  Running --> Blocked: waits (delay, queue, semaphore)
  Blocked --> Ready: event arrives
```

## Preemption and context switching

A **preemptive** scheduler (like FreeRTOS by default) can stop a running task to
run a higher-priority one that just became ready. To switch, the kernel performs
a **context switch**: save the current task's CPU registers onto its stack, load
the next task's saved registers, and resume it. On Cortex-M this is done in the
**PendSV** handler and costs a fixed, small number of cycles.

That cost is pure overhead, so switching too often wastes CPU. The fraction lost
to switching grows as the **tick rate** (how often the scheduler runs) rises:

```plot
{"title": "RTOS overhead vs scheduler tick rate (slide switch cost)", "xLabel": "tick frequency (kHz)", "yLabel": "CPU lost to context switch (%)", "xRange": [0.1, 10], "yRange": [0, 12], "grid": true, "controls": [{"name": "cyc", "range": [50, 500], "value": 200, "label": "cycles per switch"}], "functions": [{"expr": "100*cyc*x/48000", "label": "overhead % (48 MHz core)"}]}
```

## Cooperative vs preemptive

- **Cooperative** - tasks run until they voluntarily `yield`/block. Simple, no
  data races, but one greedy task hogs the CPU.
- **Preemptive** - the kernel can switch at any tick or on a higher-priority
  wake. Responsive, but you must protect shared data (next lesson).

```c
// FreeRTOS: two tasks at different priorities; the kernel time-slices them
void blink_task(void *p)  { for (;;) { led_toggle(); vTaskDelay(500); } }
void sense_task(void *p)  { for (;;) { read_adc();   vTaskDelay(10);  } }

xTaskCreate(blink_task, "blink", 128, NULL, 1, NULL);   // low priority
xTaskCreate(sense_task, "sense", 128, NULL, 3, NULL);   // higher priority
vTaskStartScheduler();
```

```python
# A cooperative model in Python: each "task" is a generator that yields control
def blink():
    while True:
        yield "led toggled"
def sense():
    while True:
        yield "adc read"
tasks = [blink(), sense()]
round_robin = [next(t) for t in tasks]    # one slice each
```

> **Practical insight:** reach for an RTOS when you have multiple, independent,
> multi-rate jobs or need clean blocking I/O. For a single tight control loop, a
> bare-metal super-loop is often simpler and more deterministic.

**Next:** the hardest part of an RTOS - sharing data safely.
""",
        ),
        _t(
            "RTOS synchronization: semaphores, mutexes & queues",
            "13 min",
            """\
# RTOS synchronization: semaphores, mutexes & queues

The moment two tasks share data, you have a **concurrency problem**: a context
switch can happen mid-update, leaving data half-written. RTOS primitives solve
this.

## The toolkit

| Primitive | Use | Analogy |
|-----------|-----|---------|
| **Mutex** | protect a shared resource (one owner at a time) | a key to a room |
| **Semaphore (counting)** | manage N identical resources / signal events | a tray of tickets |
| **Binary semaphore** | signal from ISR to task ("event happened") | a flag |
| **Queue** | pass data between tasks/ISR safely | a conveyor belt |

## Mutex: mutual exclusion

A **critical section** is code that must not be interrupted mid-way (e.g.
updating a shared struct). A **mutex** ensures only the task holding it runs that
section; others **block** until it is released.

```c
xSemaphoreTake(mutex, portMAX_DELAY);   // lock
shared.x = a; shared.y = b;             // critical section (atomic to others)
xSemaphoreGive(mutex);                  // unlock
```

```python
# threading.Lock is the same idea in Python
import threading
mutex = threading.Lock()
with mutex:                 # take ... give, even on exceptions
    shared_x, shared_y = a, b
```

## Queues: communicate, do not share

The cleanest pattern is to **not share memory at all** - instead pass messages
through a **queue**. An ISR or producer task posts an item; a consumer task
blocks until one arrives. This is how you get data out of a short ISR safely.

```mermaid
flowchart LR
  ISR["UART ISR (producer)"] -->|post byte| Q["queue"]
  Q -->|receive| TASK["parser task (consumer)"]
```

## Priority inversion - the famous trap

A subtle failure: a **low**-priority task holds a mutex that a **high**-priority
task needs, so the high task blocks. Then a **medium**-priority task preempts the
low one - so the medium task effectively runs ahead of the high one. This
**priority inversion** stalled NASA's Mars Pathfinder in 1997. The fix is
**priority inheritance**: the low task temporarily inherits the high task's
priority so it finishes the critical section fast.

The high task's blocked time balloons with how long the low task is preempted:

```plot
{"title": "Priority inversion: high task blocked time vs medium-task run length", "xLabel": "medium task hogging the CPU (ms)", "yLabel": "high task blocked (ms)", "xRange": [0, 20], "yRange": [0, 25], "grid": true, "controls": [{"name": "crit", "range": [0.5, 5], "value": 2, "label": "critical section length (ms)"}], "functions": [{"expr": "x + crit", "label": "without inheritance"}, {"expr": "crit", "label": "with priority inheritance", "color": "#16a34a"}]}
```

> **Practical insight:** prefer **queues** over shared variables + mutexes - they
> sidestep most races. When you must use a mutex across priorities, enable
> **priority inheritance**, and never block inside an ISR (use a queue/semaphore
> *give* from the ISR instead).

**Next:** moving data without the CPU - DMA.
""",
        ),
        _t(
            "DMA & high-throughput peripherals",
            "12 min",
            """\
# DMA & high-throughput peripherals

If the CPU has to copy every byte from a peripheral to memory, fast data streams
(audio, ADC sweeps, displays, high-speed UART) eat all its time. **DMA** (Direct
Memory Access) is a dedicated engine that moves data **without the CPU**.

## How DMA works

You configure a **DMA channel** with a source, a destination, a count, and a
trigger (e.g. "every time the ADC finishes a conversion"). The DMA controller
then shuttles data peripheral-to-memory (or memory-to-memory) on its own,
interrupting the CPU only when the whole transfer is done.

```mermaid
flowchart LR
  ADC["ADC"] -->|each sample| DMA["DMA engine"]
  DMA -->|writes| BUF["RAM buffer"]
  DMA -->|"IRQ when full"| CPU["CPU (free until then)"]
```

## Why it matters: CPU load

Without DMA, CPU load from servicing a stream is proportional to the data rate -
at high rates the CPU does nothing but copy. With DMA, per-sample CPU cost drops
to nearly zero (just one interrupt per buffer):

```plot
{"title": "CPU load moving a data stream: polled/IRQ vs DMA (slide rate)", "xLabel": "samples per second (thousands)", "yLabel": "CPU load (%)", "xRange": [1, 100], "yRange": [0, 110], "grid": true, "controls": [{"name": "cyc", "range": [20, 200], "value": 80, "label": "cycles per sample (no DMA)"}], "functions": [{"expr": "min(100, cyc*x*1000/480000)", "label": "no DMA (per-sample CPU)"}, {"expr": "2", "label": "with DMA (one IRQ per buffer)", "color": "#16a34a"}]}
```

## Ping-pong (double) buffering

For continuous streams, use **two buffers**: DMA fills buffer A while the CPU
processes the just-filled buffer B, then they swap on each completion interrupt.
This way the CPU always has a full, stable buffer to work on and never races the
DMA engine. It is how audio codecs, camera sensors, and SDR front-ends run
gap-free.

```c
// Circular DMA from ADC into a buffer; half/full IRQs trigger processing
HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buf, BUF_LEN);   // runs forever
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef *h) { process(&adc_buf[0]); }
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *h)     { process(&adc_buf[BUF_LEN/2]); }
```

```python
# Ping-pong model: process one half while the other "fills"
buffers = [[0]*256, [0]*256]
fill, proc = 0, 1
for _ in range(4):
    # DMA fills buffers[fill]; CPU processes buffers[proc]; then swap
    fill, proc = proc, fill
```

> **Practical insight:** DMA is the single biggest lever for throughput on an
> MCU - but beware **cache coherency** on bigger parts (Cortex-M7): a buffer the
> CPU cached and the DMA wrote can disagree, so flush/invalidate cache around DMA
> regions or place them in non-cached memory.

**Next:** finding and proving bugs - debugging and testing.
""",
        ),
        _t(
            "Debugging & testing embedded systems",
            "12 min",
            """\
# Debugging & testing embedded systems

Embedded bugs hide where you cannot see: a race in an ISR, a stack overflow, a
glitch on a bus. A toolbox of techniques makes the invisible visible.

## On-chip debugging: SWD / JTAG

**SWD** (Serial Wire Debug, 2 pins) and the older **JTAG** give a debugger
(through a probe like ST-Link or J-Link) direct control of the CPU: set
**breakpoints**, single-step, read/write memory and registers, and inspect the
live system. It is the closest thing to a desktop debugger for firmware.

## printf and logging

The humble **`printf` over UART** (or SWO/ITM trace, or RTT) is still the most-
used tool: sprinkle prints, watch the flow. Cheap, but it changes timing - a
print inside a tight ISR can break the very bug you are chasing.

## The logic analyzer and oscilloscope

A **logic analyzer** captures many digital lines over time - indispensable for
decoding SPI/I2C/UART traffic and catching glitches. An **oscilloscope** shows
analog detail (ringing, noise, rise times). They show you what the chip *really*
did, not what you think it did.

## Testing: from unit tests to HIL

| Level | What | Where it runs |
|-------|------|---------------|
| **Unit tests** | pure logic (parsers, FSMs, math) | on your PC (host) |
| **Integration** | driver + peripheral on the chip | on target |
| **HIL** (hardware-in-the-loop) | firmware vs a simulated plant/world | target + simulator |

The trick that makes embedded testable: **separate logic from hardware**. Push
register pokes behind a thin driver layer so the business logic (a protocol
parser, a control law, a state machine) is plain C you can unit-test on a PC -
exactly like the labs in this course.

```c
// Host unit test (e.g. Unity/Ceedling): logic with no hardware dependency
void test_parser_rejects_bad_checksum(void) {
    Frame f;
    TEST_ASSERT_FALSE(parse_frame(bad_bytes, sizeof bad_bytes, &f));
}
```

```python
# Same logic, tested in pytest on the host - no MCU required
def test_parser_rejects_bad_checksum():
    assert parse_frame(bad_bytes) is None
```

Test coverage of the testable (host) logic climbs fast with a handful of cases,
while pure on-target bugs need the probe and analyzer - so push as much logic to
the host as you can:

```plot
{"title": "Bugs caught vs host unit tests written (diminishing returns)", "xLabel": "host unit tests", "yLabel": "logic bugs caught (%)", "xRange": [0, 40], "yRange": [0, 100], "grid": true, "controls": [{"name": "rate", "range": [0.05, 0.3], "value": 0.12, "label": "catch rate per test"}], "functions": [{"expr": "100*(1 - exp(-rate*x))", "label": "cumulative bugs caught"}]}
```

> **Practical insight:** the fastest embedded teams keep firmware logic
> hardware-independent and unit-test it on the host in CI, reserving the
> debugger, analyzer, and HIL rig for the genuinely hardware-coupled bugs.

**Next:** the theory that guarantees deadlines - real-time scheduling.
""",
        ),
        _t(
            "Real-time scheduling & constraints",
            "12 min",
            """\
# Real-time scheduling & constraints

"Real-time" does not mean *fast* - it means **on time, every time**. A system is
real-time if missing a **deadline** is a failure: an airbag, a motor commutation,
an audio buffer. The theory tells you whether your task set will *always* meet
its deadlines.

## Hard vs soft real-time

- **Hard** - a missed deadline is a catastrophe (airbag, engine timing).
- **Soft** - a missed deadline degrades quality but is survivable (a dropped
  video frame, a laggy UI).

## Rate-monotonic scheduling (RMS)

A classic result: if you assign **fixed priorities by rate** (the most frequent
task gets the highest priority), the set is schedulable as long as total CPU
**utilization** stays under a bound. With $n$ tasks of execution time $C_i$ and
period $T_i$:

$$U = \\sum_{i=1}^{n} \\frac{C_i}{T_i} \\le n\\left(2^{1/n} - 1\\right).$$

That bound starts at 100% for one task and decreases toward $\\ln 2 \\approx
69\\%$ as $n$ grows - the price of guaranteeing deadlines under fixed priorities:

```plot
{"title": "Rate-monotonic utilization bound vs number of tasks", "xLabel": "number of tasks n", "yLabel": "schedulable utilization bound (%)", "xRange": [1, 12], "yRange": [60, 105], "grid": true, "functions": [{"expr": "100*x*(2^(1/x) - 1)", "label": "RMS bound n(2^(1/n)-1)"}, {"expr": "69.3", "label": "asymptote ln 2", "color": "#dc2626"}]}
```

## Jitter and WCET

Two enemies of determinism:

- **Jitter** - variation in *when* a periodic task actually runs. A control loop
  expects an exact period; jitter degrades it.
- **WCET** (Worst-Case Execution Time) - the longest a piece of code can take.
  Caches, branches, and interrupts make this hard to bound, but you must, because
  schedulability uses the **worst** case, not the average.

Press Play to watch a task that should fire on an exact grid drift because of
jitter (the marker wobbles off the ideal tick):

```plot
{"title": "Jitter: a periodic task's actual fire time wobbles off the ideal grid", "xLabel": "time", "yLabel": "task index", "xRange": [0, 10], "yRange": [-0.5, 5.5], "grid": true, "animate": {"param": "t", "range": [0, 10], "label": "time"}, "functions": [{"expr": "floor(x)", "label": "ideal periodic schedule"}], "points": [{"xExpr": "t + 0.25*sin(9*t)", "yExpr": "floor(t)", "label": "actual (jittered)", "color": "#dc2626", "size": 7, "trail": true}]}
```

> **Practical insight:** keep ISRs short and bounded, avoid unbounded loops in
> real-time paths, and measure WCET on the real hardware (toggle a GPIO and scope
> it). Utilization headroom is not waste - it is your margin against jitter and
> overruns.

**Next:** build a preemptive scheduler and watch timing in code.
""",
        ),
        _code(
            "Lab: preemptive task scheduler & timing",
            "14 min",
            """\
# Simulate a fixed-priority preemptive scheduler (rate-monotonic) running three
# periodic tasks on one CPU. We step a virtual clock in 1 ms ticks, always run
# the highest-priority READY task, and record what executes each tick. Then we
# check whether any task missed its deadline. numpy + matplotlib, no hardware.
import numpy as np
import matplotlib.pyplot as plt

# Each task: (name, period_ms, compute_ms). Rate-monotonic: shorter period =>
# higher priority. Index 0 is highest priority.
tasks = [
    ("A_fast", 10, 3),     # highest priority (most frequent)
    ("B_med", 20, 5),
    ("C_slow", 40, 7),
]
SIM_MS = 80
n_tasks = len(tasks)

# Utilization and the rate-monotonic bound (from the lesson).
U = sum(c / p for (_, p, c) in tasks)
rm_bound = n_tasks * (2 ** (1 / n_tasks) - 1)
print(f"total utilization U = {U:.3f}   RM bound = {rm_bound:.3f}")
print("schedulable by RM test:" , U <= rm_bound)

remaining = [0.0] * n_tasks          # ms of work left for current job
released = [0] * n_tasks             # tick the current job was released
missed = []                          # (task, time) deadline misses
timeline = np.full(SIM_MS, -1)       # which task ran each ms (-1 = idle)

for t in range(SIM_MS):
    # Release new jobs at the start of each period.
    for i, (_, period, comp) in enumerate(tasks):
        if t % period == 0:
            if remaining[i] > 0:     # previous job not finished -> deadline miss
                missed.append((tasks[i][0], t))
            remaining[i] = comp
            released[i] = t
    # Pick the highest-priority task with work remaining.
    runnable = [i for i in range(n_tasks) if remaining[i] > 0]
    if runnable:
        run = runnable[0]            # list is already in priority order
        remaining[run] -= 1.0
        timeline[t] = run

# Plot the execution timeline (Gantt-style) per task row.
plt.figure(figsize=(9, 3.8))
colors = ["#dc2626", "#2563eb", "#16a34a"]
for t in range(SIM_MS):
    r = timeline[t]
    if r >= 0:
        plt.barh(r, 1, left=t, color=colors[r], edgecolor="none")
for i, (name, period, _) in enumerate(tasks):
    for rel in range(0, SIM_MS, period):
        plt.axvline(rel, ymin=0, ymax=1, color="#cbd5e1", lw=0.5)
plt.yticks(range(n_tasks), [n for (n, _, _) in tasks])
plt.xlabel("time (ms)"); plt.title("Rate-monotonic preemptive schedule (highest priority on top)")
plt.gca().invert_yaxis(); plt.grid(True, axis="x"); plt.tight_layout(); plt.show()

idle = int((timeline < 0).sum())
print(f"idle ticks: {idle} / {SIM_MS}  ({100 * idle / SIM_MS:.0f}% slack)")
print("deadline misses:", missed if missed else "none")

# Try it yourself:
#   1. Raise C_slow compute to 15 ms: utilization exceeds 1.0 -> deadline misses.
#   2. Swap priorities (give C_slow highest): the fast task starves and misses.
""",
        ),
        _t(
            "Applications & the throughline",
            "11 min",
            """\
# Applications & the throughline

Everything in this track converges on real products. Embedded systems are the
quiet majority of all computers made - billions of MCUs ship every year, almost
none of them ever seen by a user.

## Where this knowledge ships

| Domain | What the MCU does | Skills it leans on |
|--------|-------------------|--------------------|
| **IoT / wearables** | read sensors, sleep, send data over radio | ADC, I2C/SPI, sleep modes, power budget |
| **Automotive** | engine/brake/airbag control, CAN bus | hard real-time, watchdog, RTOS, safety |
| **Robotics / drones** | motor control, IMU fusion, fast loops | PWM, timers, interrupts, DMA, scheduling |
| **Medical** | pacemakers, infusion pumps, monitors | reliability, watchdog, testing/HIL |
| **Industrial** | PLCs, motor drives, instrumentation | buses, real-time, FSMs |
| **Consumer** | appliances, toys, power tools | super-loop, FSM, PWM, cost focus |

## A worked example: a fitness wearable

It ties the whole course together:

- An **ADC** + I2C sensors read heart rate and motion.
- Most of the time the MCU is in a deep **sleep mode**, waking on a **timer**
  interrupt to sample - that is what makes a tiny battery last days (the
  power-budget math from the Intermediate course).
- A **DMA**-fed buffer collects accelerometer samples while the CPU sleeps.
- An **RTOS** (or a tidy FSM) juggles sampling, a step-counting algorithm, the
  display, and a **BLE** radio stack.
- A **watchdog** guarantees it reboots rather than freezing on your wrist.

Battery life is dominated by the **duty cycle** of being awake - the single
number a wearable's firmware fights for:

```plot
{"title": "Wearable battery life vs awake duty cycle (220 mAh, slide active draw)", "xLabel": "awake duty cycle (%)", "yLabel": "battery life (days)", "xRange": [0.2, 10], "yRange": [0, 60], "grid": true, "controls": [{"name": "act", "range": [3, 20], "value": 8, "label": "active current (mA)"}], "functions": [{"expr": "(220/((x/100)*act + (1 - x/100)*0.01))/24", "label": "life (days)"}]}
```

## Trends to watch

- **Security** - connected devices need secure boot, signed firmware, and crypto
  accelerators; an unpatched IoT device is a liability.
- **Edge AI / TinyML** - running small neural nets on the MCU itself (keyword
  spotting, anomaly detection) without the cloud.
- **Functional safety** - standards (ISO 26262 automotive, IEC 62304 medical)
  formalize the watchdog, testing, and redundancy practices above.

## The throughline

A CPU runs firmware from flash, reads the world through peripherals (GPIO, ADC,
buses), reacts in real time via interrupts and timers, organizes itself with
state machines or an RTOS, moves bulk data with DMA, sips power by sleeping, and
proves itself with debugging and tests. From a 1 KB sensor node to a safety-
critical ECU, the skeleton is the same - only the scale changes. That is the
discipline of embedded systems.

**Next:** the final check.
""",
        ),
    ),
)


EMBEDDED_COURSES: tuple[SeedCourse, ...] = (
    _EMBEDDED_BASICS,
    _EMBEDDED_INTERMEDIATE,
    _EMBEDDED_ADVANCED,
)

__all__ = ["EMBEDDED_COURSES"]
