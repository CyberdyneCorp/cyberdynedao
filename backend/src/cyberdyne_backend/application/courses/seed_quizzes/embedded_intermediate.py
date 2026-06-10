from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Interrupts in depth: NVIC, priorities & latency": (
            q(
                "On Cortex-M, what does the priority number of an interrupt mean?",
                (
                    opt("Higher number means higher priority"),
                    opt("Lower number means higher priority", correct=True),
                    opt("The number is only a label with no ordering"),
                    opt("Priority is fixed and cannot be changed"),
                ),
                "On Cortex-M a lower priority number means higher priority, so it preempts ISRs with higher numbers.",
            ),
            q(
                "Why must variables shared between an ISR and the main loop be declared volatile?",
                (
                    opt("To make the compiler optimize them into registers"),
                    opt(
                        "To prevent the compiler from caching a stale value and missing the ISR update",
                        correct=True,
                    ),
                    opt("Because volatile speeds up the interrupt entry"),
                    opt("Because the NVIC requires it for vectoring"),
                ),
                "volatile tells the compiler the value can change outside normal flow, so it always re-reads it rather than caching a stale copy.",
            ),
            q(
                "According to the golden rule for ISRs, what should an ISR do?",
                (
                    opt("Run the heavy work directly so the main loop stays free"),
                    opt("Call printf to log the event for debugging"),
                    opt(
                        "Signal the main loop and return quickly while the main loop does the work",
                        correct=True,
                    ),
                    opt("Disable the NVIC until the next event arrives"),
                ),
                "The golden rule is ISRs signal, the main loop works: do the urgent minimum, set a flag or queue an event, and return.",
            ),
        ),
        "Serial buses: UART, SPI & I2C": (
            q(
                "What does UART rely on instead of a shared clock?",
                (
                    opt("A chip-select line per device"),
                    opt("Both ends agreeing on a baud rate", correct=True),
                    opt("Open-drain pull-up resistors"),
                    opt("A 7-bit device address"),
                ),
                "UART is asynchronous: there is no shared clock, so both ends must agree on a baud rate such as 115200 bit/s.",
            ),
            q(
                "Which bus is full duplex, uses a shared clock plus MOSI and MISO, and needs one chip-select per peripheral?",
                (
                    opt("UART"),
                    opt("I2C"),
                    opt("SPI", correct=True),
                    opt("CAN"),
                ),
                "SPI uses a shared SCLK plus MOSI and MISO and one CS per peripheral, giving fast full-duplex transfers.",
            ),
            q(
                "What classic first-day bug does the lesson warn about with I2C?",
                (
                    opt("Forgetting the pull-up resistors on SDA and SCL", correct=True),
                    opt("Using too high a baud rate"),
                    opt("Wiring MISO and MOSI backwards"),
                    opt("Leaving the chip-select line floating"),
                ),
                "I2C lines are open-drain and need pull-ups; forgetting the I2C pull-up resistors is the classic first-day bug.",
            ),
        ),
        "Advanced timers: input capture, output compare & watchdog": (
            q(
                "What does a timer in input capture mode do when a pin edge arrives?",
                (
                    opt("It resets the counter to zero"),
                    opt("It latches the counter value at the instant of the edge", correct=True),
                    opt("It toggles an output pin"),
                    opt("It kicks the watchdog"),
                ),
                "Input capture latches the counter value the instant an edge arrives, so two captures give a precise interval.",
            ),
            q(
                "What does a watchdog timer do if the firmware fails to kick it before it reaches zero?",
                (
                    opt("It raises an interrupt that the ISR must clear"),
                    opt("It resets the MCU", correct=True),
                    opt("It switches the MCU to a sleep mode"),
                    opt("It doubles the timer clock frequency"),
                ),
                "A watchdog counts down and resets the MCU if it reaches zero, recovering from a hung program that stops kicking it.",
            ),
            q(
                "What is the practical advice for setting and kicking the watchdog?",
                (
                    opt("Set it shorter than the loop and kick from many places"),
                    opt(
                        "Set it longer than the worst-case loop and kick from one well-understood place",
                        correct=True,
                    ),
                    opt("Disable it during normal operation and enable it only on errors"),
                    opt("Kick it from inside every ISR to be safe"),
                ),
                "Set the watchdog longer than your worst-case loop and kick it from one place, or a half-hung program keeps petting it and defeats the point.",
            ),
        ),
        "Power management & sleep modes": (
            q(
                "According to the dynamic power formula P = C V^2 f, how does dynamic power scale?",
                (
                    opt("Linearly with voltage and with the square of frequency"),
                    opt("With the square of voltage and linearly with frequency", correct=True),
                    opt("Only with the static leakage current"),
                    opt("Inversely with frequency"),
                ),
                "Dynamic power scales with the square of voltage and linearly with frequency, so halving the clock roughly halves dynamic power.",
            ),
            q(
                "Which sleep mode keeps clocks off but retains RAM and wakes in a few microseconds?",
                (
                    opt("Run"),
                    opt("Sleep"),
                    opt("Stop", correct=True),
                    opt("Standby"),
                ),
                "Stop mode turns clocks off while keeping RAM, drawing about microamps and waking fast in a few microseconds.",
            ),
            q(
                "What primarily sets the battery life of a low-power device?",
                (
                    opt("The peak current during a burst of work"),
                    opt(
                        "The average current, dominated by how often and how long you are awake",
                        correct=True,
                    ),
                    opt("The number of peripherals physically connected"),
                    opt("The deepest sleep mode supported by the MCU"),
                ),
                "Average current sets battery life and is dominated by how often and how long you are awake, so wake, work fast, and sleep.",
            ),
        ),
        "Event-driven firmware & state machines": (
            q(
                "Which firmware structure is described as the sweet spot for most event-driven products like a vending machine or microwave?",
                (
                    opt("Super-loop"),
                    opt("FSM (finite state machine)", correct=True),
                    opt("RTOS"),
                    opt("Bare interrupt-only design"),
                ),
                "The FSM is the sweet spot for an enormous range of event-driven products such as a vending machine, microwave, or charger.",
            ),
            q(
                "How do you define a finite state machine in this lesson?",
                (
                    opt("By scattering mode booleans and nested ifs across the super-loop"),
                    opt(
                        "By the states, the events, and the transition for each (state, event) pair",
                        correct=True,
                    ),
                    opt("By giving each task its own scheduler"),
                    opt("By polling every peripheral on each loop pass"),
                ),
                "An FSM is defined by its states, its events, and the transition for each (state, event) pair, kept in one readable table.",
            ),
            q(
                "What does combining an FSM with sleep achieve?",
                (
                    opt("Continuous CPU activity for faster response"),
                    opt(
                        "CPU activity becomes short bursts around events, staying asleep until an event arrives",
                        correct=True,
                    ),
                    opt("Elimination of the need for interrupts"),
                    opt("Higher dynamic power from constant clocking"),
                ),
                "Staying asleep until an event arrives and processing the transition makes CPU activity short spikes around events instead of a busy loop.",
            ),
        ),
        "Lab: UART frame decode + FSM byte parser": (
            q(
                "In the lab frame format [STX] [LEN] [payload...] [CHK], what is CHK?",
                (
                    opt("The sum of all payload bytes"),
                    opt("The XOR of the payload bytes", correct=True),
                    opt("The length of the payload"),
                    opt("A copy of the STX byte"),
                ),
                "CHK is the XOR of the payload bytes; the parser accumulates acc_chk by XORing each payload byte and compares it to CHK.",
            ),
            q(
                "What are the four states the FSM parser walks through in order?",
                (
                    opt("READ_LEN -> WAIT_STX -> READ_CHK -> READ_PAYLOAD"),
                    opt("WAIT_STX -> READ_LEN -> READ_PAYLOAD -> READ_CHK", correct=True),
                    opt("IDLE -> SYNC -> DATA -> DONE"),
                    opt("WAIT_STX -> READ_CHK -> READ_LEN -> READ_PAYLOAD"),
                ),
                "The parser progresses WAIT_STX -> READ_LEN -> READ_PAYLOAD -> READ_CHK, then returns to WAIT_STX after checking the frame.",
            ),
            q(
                "What happens to the middle frame in the simulated stream and why?",
                (
                    opt("It is accepted because its checksum still matches"),
                    opt(
                        "It is rejected because it was built with corrupt=True, breaking its checksum",
                        correct=True,
                    ),
                    opt("It causes the FSM to crash and stop parsing"),
                    opt("It is skipped because it has zero length"),
                ),
                "The middle frame is built with corrupt=True which XORs the checksum with 0xFF, so it fails the CHK comparison and is rejected.",
            ),
        ),
    },
    final=(
        q(
            "On Cortex-M, why does keeping interrupts masked for long critical sections matter?",
            (
                opt("It speeds up the hardware entry below 12 cycles"),
                opt("It inflates worst-case interrupt latency", correct=True),
                opt("It permanently disables the NVIC"),
                opt("It lowers the dynamic power consumption"),
            ),
            "Worst-case latency is inflated by time spent with IRQs masked plus the fixed hardware entry, so long critical sections hurt the worst case.",
        ),
        q(
            "You need many small slow sensors sharing only two wires. Which bus fits best?",
            (
                opt("SPI because it is full duplex"),
                opt("UART because it needs no clock"),
                opt("I2C because two wires carry many addressed devices", correct=True),
                opt("A dedicated chip-select per sensor"),
            ),
            "I2C uses two wires and 7-bit addressing to put many slow sensors on one bus, ideal when pins are scarce.",
        ),
        q(
            "Which timer mode lets you flip a pin at an exact counter value with zero software jitter?",
            (
                opt("Input capture"),
                opt("Output compare", correct=True),
                opt("Watchdog"),
                opt("Clock gating"),
            ),
            "Output compare flips a pin or fires an interrupt when the counter reaches a programmed value, with timing done in hardware.",
        ),
        q(
            "What is the recommended low-power pattern that ties together sleep and event-driven design?",
            (
                opt("Poll all peripherals continuously in a super-loop"),
                opt("Run the CPU at full clock and disable the watchdog"),
                opt("Do a quick burst of work then sleep until the next interrupt", correct=True),
                opt("Use Standby mode for every short idle period"),
            ),
            "The classic pattern is to do a quick burst of work then sleep until the next interrupt, so the FSM stays idle until an event wakes it.",
        ),
        q(
            "In the lab parser, what does the FSM do if the stream is truncated mid-frame?",
            (
                opt("It crashes with an index error"),
                opt("It safely waits in READ_PAYLOAD", correct=True),
                opt("It accepts the partial frame as good"),
                opt("It resets the MCU like a watchdog"),
            ),
            "If the stream is truncated mid-frame the FSM safely waits in READ_PAYLOAD without producing a frame or crashing.",
        ),
    ),
)
