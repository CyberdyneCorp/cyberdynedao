from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is an embedded system & MCU anatomy": (
            q(
                "What distinguishes a microcontroller (MCU) from the microprocessor in a laptop?",
                (
                    opt("It always runs a full operating system"),
                    opt(
                        "It puts flash, RAM, and peripherals on the same die and runs without an OS",
                        correct=True,
                    ),
                    opt("It is measured in gigabytes and watts"),
                    opt("It cannot execute any instructions from flash"),
                ),
                "An MCU integrates CPU, flash, RAM, and peripherals on one die, runs without an OS, and is sized in kilobytes and milliwatts.",
            ),
            q(
                "In a Harvard-style architecture, why can the CPU fetch an instruction and a datum at the same time?",
                (
                    opt("Because instructions and data share a single bus"),
                    opt("Because there is no flash on the chip"),
                    opt(
                        "Because program and data have separate paths",
                        correct=True,
                    ),
                    opt("Because the CPU runs an operating system"),
                ),
                "Harvard architecture uses separate program and data paths, so code can run from flash while variables live in RAM concurrently.",
            ),
            q(
                "Which 2004 CPU family was designed for embedded use and now sits inside STM32 and the RP2040?",
                (
                    opt("Intel 4004"),
                    opt("Intel 8051"),
                    opt("ARM Cortex-M", correct=True),
                    opt("Intel 8048"),
                ),
                "ARM Cortex-M (2004) is the deterministic, low-power embedded family used in STM32, the Raspberry Pi Pico (RP2040), Nordic radios, and more.",
            ),
        ),
        "GPIO & memory-mapped registers": (
            q(
                "How does an MCU drive output pins if there is no special output instruction?",
                (
                    opt("By calling an OS system call"),
                    opt(
                        "By writing words to peripheral registers at fixed memory addresses",
                        correct=True,
                    ),
                    opt("By reading the IDR register"),
                    opt("By recompiling the firmware at runtime"),
                ),
                "Peripherals are memory-mapped: writing a word to a fixed register address (such as the ODR) sets the output pins.",
            ),
            q(
                "Which C idiom clears bit n of a register while leaving the other bits alone?",
                (
                    opt("REG |= (1u << n);"),
                    opt("REG ^= (1u << n);"),
                    opt("REG &= ~(1u << n);", correct=True),
                    opt("REG = (1u << n);"),
                ),
                "ANDing with the inverted mask ~(1u << n) clears only bit n; OR sets, XOR toggles.",
            ),
            q(
                "Why is the volatile keyword critical when accessing a hardware register in C?",
                (
                    opt("It makes the access faster by caching the value"),
                    opt("It marks the register as read-only"),
                    opt(
                        "It tells the compiler the value can change outside the program so it must really read and write memory each time",
                        correct=True,
                    ),
                    opt("It atomically sets and resets bits"),
                ),
                "volatile prevents the compiler from optimising the access away, since hardware can change the value outside the program flow.",
            ),
        ),
        "The bare-metal program: startup, vector table & super-loop": (
            q(
                "On reset, what are the first two 32-bit words a Cortex-M reads from the start of flash?",
                (
                    opt("The clock frequency and the linker script address"),
                    opt(
                        "The initial stack pointer and the reset vector (address of Reset_Handler)",
                        correct=True,
                    ),
                    opt("The .data section and the .bss section"),
                    opt("The first two GPIO register values"),
                ),
                "The first word is the initial stack pointer and the second is the reset vector pointing at Reset_Handler.",
            ),
            q(
                "What must the startup code do before main() can run?",
                (
                    opt("Return from main() immediately"),
                    opt("Load an operating system into RAM"),
                    opt(
                        "Copy .data into RAM, zero .bss, and set up the clock",
                        correct=True,
                    ),
                    opt("Poll every peripheral once"),
                ),
                "Startup copies initialised variables (.data) from flash to RAM, zeroes uninitialised globals (.bss), sets up the clock, then calls main().",
            ),
            q(
                "What is the trade-off between polling and interrupts for getting peripheral information?",
                (
                    opt(
                        "Polling is simple but wastes CPU and may miss fast events, while interrupts are responsive but harder to reason about",
                        correct=True,
                    ),
                    opt("Interrupts are always simpler and faster to reason about"),
                    opt("Polling never misses events and uses no CPU"),
                    opt("Interrupts require the super-loop to return"),
                ),
                "Polling repeatedly asks a peripheral (simple, wasteful, can miss events); interrupts let the peripheral preempt the loop (responsive but harder to reason about).",
            ),
        ),
        "Timers & PWM": (
            q(
                "What does a prescaler (PSC) do in a timer/counter peripheral?",
                (
                    opt("It sets the duty cycle of a PWM output"),
                    opt(
                        "It divides the peripheral clock first so slow rates are reachable without a huge counter",
                        correct=True,
                    ),
                    opt("It converts an analog voltage into a code"),
                    opt("It debounces a noisy button input"),
                ),
                "The prescaler divides the clock before the counter, with overflow frequency f_clk / ((PSC+1)(ARR+1)).",
            ),
            q(
                "For a PWM signal, how does the average output voltage relate to the duty cycle D?",
                (
                    opt("V_avg = V_cc / D"),
                    opt("V_avg = D * V_cc", correct=True),
                    opt("V_avg = D + V_cc"),
                    opt("V_avg is independent of D"),
                ),
                "PWM drives the pin high for fraction D of each period, so a slow load sees an average voltage of D times V_cc.",
            ),
            q(
                "An RC hobby servo interprets its control signal as what?",
                (
                    opt("A duty cycle from 0 to 100 percent"),
                    opt("An ADC code"),
                    opt(
                        "A pulse width, e.g. a 1.0 to 2.0 ms high pulse mapping to 0 to 180 degrees",
                        correct=True,
                    ),
                    opt("A prescaler value"),
                ),
                "A servo reads pulse width, not duty cycle: a 20 ms frame with a 1.0 to 2.0 ms high pulse maps linearly to 0 to 180 degrees.",
            ),
        ),
        "Reading the world: ADC & buttons": (
            q(
                "What does an ADC produce and how many steps does an N-bit ADC have over the range 0 to Vref?",
                (
                    opt("A voltage; N steps"),
                    opt(
                        "An integer code; 2 to the power N steps",
                        correct=True,
                    ),
                    opt("A duty cycle; N steps"),
                    opt("A pulse width; 2N steps"),
                ),
                "An ADC reports an integer code measured against Vref, splitting the range into 2^N steps; resolution is Vref / 2^N.",
            ),
            q(
                "Why does a mechanical button need debouncing?",
                (
                    opt("Because the ADC code drifts over time"),
                    opt("Because the pin is read-only"),
                    opt(
                        "Because its contacts physically bounce for a few milliseconds, producing fake transitions",
                        correct=True,
                    ),
                    opt("Because volatile is not used on the register"),
                ),
                "A switch does not close cleanly; its contacts bounce for a few ms, so a raw read registers one press as many.",
            ),
            q(
                "What is the standard firmware approach to debouncing a button?",
                (
                    opt("Add long delays in the main loop after each read"),
                    opt(
                        "Accept a new state only after it reads the same value for several consecutive samples",
                        correct=True,
                    ),
                    opt("Sample faster than twice the Nyquist rate"),
                    opt("Increase the ADC bit depth"),
                ),
                "Debounce in the time domain: require the pin to be stable for several samples (around 10 to 30 ms) before accepting a new state.",
            ),
        ),
        "Lab: button debounce + PWM duty waveform": (
            q(
                "In the lab, what does the STABLE constant (set to 15) control?",
                (
                    opt("The PWM carrier frequency in Hz"),
                    opt("The number of real presses in the simulation"),
                    opt(
                        "How many consecutive matching samples are required before accepting a new debounced state",
                        correct=True,
                    ),
                    opt("The duty cycle increment per press"),
                ),
                "STABLE = 15 requires 15 ms of stability (at the 1 kHz tick) before the debounced state updates.",
            ),
            q(
                "What happens to the PWM duty cycle on each clean rising edge detected?",
                (
                    opt("It resets to zero"),
                    opt("It bumps up by 25 percent, capped at 1.0", correct=True),
                    opt("It doubles"),
                    opt("It drops by 25 percent"),
                ),
                "Each clean rising edge increments the duty by 0.25 using min(1.0, d + 0.25), so it steps up and saturates at full scale.",
            ),
            q(
                "The lab comment says that lowering STABLE to 3 will cause what?",
                (
                    opt("The PWM carrier to disappear"),
                    opt("The simulation to run forever"),
                    opt(
                        "Bounce to leak through so the code over-counts presses",
                        correct=True,
                    ),
                    opt("The duty cycle to never change"),
                ),
                "With too small a stability window, bounce chatter is accepted as real edges and the press count is inflated.",
            ),
        ),
    },
    final=(
        q(
            "Which statement best describes a microcontroller used in embedded systems?",
            (
                opt("A CPU-only chip that needs external flash, RAM, and an OS"),
                opt(
                    "A whole computer on one chip with CPU, flash, RAM, and peripherals, running bare metal",
                    correct=True,
                ),
                opt("A device measured in gigabytes and watts"),
                opt("A peripheral that only converts analog signals to digital"),
            ),
            "An MCU is a complete computer on a single die that typically runs firmware bare metal without an operating system.",
        ),
        q(
            "How are GPIO and other peripherals accessed on a Cortex-M MCU?",
            (
                opt("Through operating-system device drivers"),
                opt("Through a dedicated input/output instruction set"),
                opt(
                    "As memory-mapped registers at fixed addresses, manipulated with bit operations",
                    correct=True,
                ),
                opt("Only through interrupts, never directly"),
            ),
            "Peripherals are memory-mapped; firmware sets, clears, and toggles specific bits in registers like MODER, ODR, and BSRR.",
        ),
        q(
            "On power-up, what sequence brings a bare-metal Cortex-M to main()?",
            (
                opt("The OS bootloader loads main() into RAM and jumps to it"),
                opt(
                    "Load the initial stack pointer, jump to Reset_Handler, copy .data and zero .bss, then call main()",
                    correct=True,
                ),
                opt("Poll all peripherals, then start an interrupt that calls main()"),
                opt("Read the ADC, set up PWM, then enter the vector table"),
            ),
            "Reset loads the stack pointer and reset vector, startup copies .data to RAM and zeroes .bss and sets the clock, then main() runs its super-loop.",
        ),
        q(
            "Using f_tick = f_clk / ((PSC+1)(ARR+1)), how do you reach a slow blink rate from a fast clock?",
            (
                opt("Increase Vref so each step is larger"),
                opt("Set the duty cycle to 100 percent"),
                opt(
                    "Choose prescaler and auto-reload values whose product divides the clock down to the target rate",
                    correct=True,
                ),
                opt("Add more tasks to the super-loop"),
            ),
            "The prescaler and ARR together divide the clock; picking their product (e.g. 48 million for 1 Hz from 48 MHz) sets the overflow rate.",
        ),
        q(
            "Why must a button be debounced while an ADC reading instead concerns sampling rate?",
            (
                opt("Both need the volatile keyword to work"),
                opt(
                    "A button's contacts bounce and must be confirmed stable over time, while an ADC must sample above twice the signal's highest frequency to avoid aliasing",
                    correct=True,
                ),
                opt("A button is analog and an ADC is digital, so neither needs care"),
                opt("Debouncing lowers the ADC resolution"),
            ),
            "Buttons need time-domain stability to reject bounce; ADCs need the Nyquist rate (sample above twice the highest frequency) to avoid aliasing.",
        ),
    ),
)
