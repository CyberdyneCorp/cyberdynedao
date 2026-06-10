from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "RTOS fundamentals: tasks, scheduler & context switch": (
            q(
                "In an RTOS, what is a task?",
                (
                    opt("A single global super-loop shared by all jobs"),
                    opt(
                        "A function with its own stack that runs as if it owns the CPU",
                        correct=True,
                    ),
                    opt("An interrupt service routine that never blocks"),
                    opt("A fixed block of flash memory reserved by the linker"),
                ),
                "A task is an independent function with its own stack; the scheduler shares the one CPU among tasks.",
            ),
            q(
                "On a Cortex-M, where does a preemptive RTOS perform the context switch?",
                (
                    opt("In the PendSV handler", correct=True),
                    opt("In the main super-loop"),
                    opt("Inside the DMA controller"),
                    opt("In the reset vector"),
                ),
                "On Cortex-M the kernel saves and restores CPU registers in the PendSV handler at a fixed, small cycle cost.",
            ),
            q(
                "What is the main drawback of a cooperative scheduler compared to a preemptive one?",
                (
                    opt("It requires expensive priority-inheritance hardware"),
                    opt("It causes data races that preemptive schedulers avoid"),
                    opt("One greedy task that never yields can hog the CPU", correct=True),
                    opt("It cannot run more than one task at a time ever"),
                ),
                "Cooperative tasks run until they voluntarily yield or block, so a greedy task that never yields starves the others.",
            ),
        ),
        "RTOS synchronization: semaphores, mutexes & queues": (
            q(
                "Which primitive is meant to protect a shared resource so only one owner uses it at a time?",
                (
                    opt("A counting semaphore"),
                    opt("A mutex", correct=True),
                    opt("A queue"),
                    opt("A binary semaphore"),
                ),
                "A mutex enforces mutual exclusion: only the task holding it runs the critical section while others block.",
            ),
            q(
                "What famous spacecraft incident was caused by priority inversion in 1997?",
                (
                    opt("The Mars Pathfinder mission stalling", correct=True),
                    opt("The Apollo 11 guidance computer overload"),
                    opt("The Ariane 5 maiden flight failure"),
                    opt("The Hubble mirror misfocus"),
                ),
                "Priority inversion, where a low task holds a mutex a high task needs while a medium task preempts, stalled NASA's Mars Pathfinder in 1997.",
            ),
            q(
                "What is the recommended fix for priority inversion described in the lesson?",
                (
                    opt("Disabling all interrupts globally"),
                    opt(
                        "Priority inheritance, where the low task temporarily inherits the high task's priority",
                        correct=True,
                    ),
                    opt("Giving every task the same priority"),
                    opt("Removing the mutex and sharing the variable directly"),
                ),
                "Priority inheritance lets the low task temporarily run at the high task's priority so it finishes the critical section fast.",
            ),
        ),
        "DMA & high-throughput peripherals": (
            q(
                "What does a DMA engine fundamentally do for high-throughput peripherals?",
                (
                    opt("Moves data between peripheral and memory without the CPU", correct=True),
                    opt("Increases the CPU clock frequency during transfers"),
                    opt("Compresses data before storing it in flash"),
                    opt("Generates interrupts for every single byte transferred"),
                ),
                "DMA is a dedicated engine that shuttles data peripheral-to-memory (or memory-to-memory) on its own, freeing the CPU.",
            ),
            q(
                "In ping-pong (double) buffering, what happens while DMA fills buffer A?",
                (
                    opt("The CPU also writes into buffer A to speed it up"),
                    opt("The CPU processes the just-filled buffer B", correct=True),
                    opt("Both buffers are paused until the IRQ fires"),
                    opt("The DMA engine is disabled to avoid a race"),
                ),
                "With two buffers, DMA fills one while the CPU processes the other, swapping on each completion interrupt so the CPU never races the DMA.",
            ),
            q(
                "Which hazard does the lesson warn about when using DMA on bigger parts like the Cortex-M7?",
                (
                    opt("Priority inversion between DMA channels"),
                    opt(
                        "Cache coherency, where cached CPU data disagrees with DMA-written memory",
                        correct=True,
                    ),
                    opt("Stack overflow inside the DMA controller"),
                    opt("Jitter in the rate-monotonic schedule"),
                ),
                "On parts with cache, a buffer the CPU cached and the DMA wrote can disagree, so you flush/invalidate cache or use non-cached memory.",
            ),
        ),
        "Debugging & testing embedded systems": (
            q(
                "What capability do SWD and JTAG give a firmware developer?",
                (
                    opt("They compress logs sent over UART"),
                    opt(
                        "Direct CPU control: breakpoints, single-step, and read/write of memory and registers",
                        correct=True,
                    ),
                    opt("They move bulk data without the CPU"),
                    opt("They guarantee tasks meet their deadlines"),
                ),
                "SWD (2 pins) and JTAG, through a probe like ST-Link or J-Link, give breakpoints, single-stepping, and memory/register access.",
            ),
            q(
                "Why can printf debugging over UART backfire inside a tight ISR?",
                (
                    opt("It permanently corrupts the flash memory"),
                    opt(
                        "It changes timing and can break the very bug you are chasing", correct=True
                    ),
                    opt("It disables the DMA engine"),
                    opt("It requires a logic analyzer to read"),
                ),
                "printf is cheap but changes timing; a print inside a tight ISR can mask or alter the timing-dependent bug being investigated.",
            ),
            q(
                "What is the key trick that makes embedded firmware testable on a PC?",
                (
                    opt("Running the full RTOS scheduler on the host"),
                    opt(
                        "Separating logic from hardware so business logic is plain C you can unit-test on a PC",
                        correct=True,
                    ),
                    opt("Replacing all interrupts with polling loops"),
                    opt("Using only assembly so timing is exact"),
                ),
                "Pushing register pokes behind a thin driver layer leaves parsers, control laws, and state machines as plain C testable on the host.",
            ),
        ),
        "Real-time scheduling & constraints": (
            q(
                "What does real-time actually mean according to the lesson?",
                (
                    opt("Running at the highest possible clock speed"),
                    opt("On time, every time, so missing a deadline is a failure", correct=True),
                    opt("Using as little power as possible"),
                    opt("Processing data only when the CPU is idle"),
                ),
                "Real-time means on time every time; a system is real-time if missing a deadline is a failure.",
            ),
            q(
                "Under rate-monotonic scheduling, how are fixed priorities assigned?",
                (
                    opt("The most frequent task gets the highest priority", correct=True),
                    opt("The task with the longest period gets the highest priority"),
                    opt("All tasks share one equal priority"),
                    opt("Priority is assigned randomly at boot"),
                ),
                "RMS assigns fixed priorities by rate: the most frequent (shortest-period) task gets the highest priority.",
            ),
            q(
                "What is WCET in real-time scheduling?",
                (
                    opt("The average time a task takes to run"),
                    opt(
                        "The Worst-Case Execution Time, the longest a piece of code can take",
                        correct=True,
                    ),
                    opt("The wake-up cost of exiting a sleep mode"),
                    opt("The number of context switches per second"),
                ),
                "WCET is the worst-case execution time; schedulability uses the worst case, not the average, because caches and interrupts make it hard to bound.",
            ),
        ),
        "Lab: preemptive task scheduler & timing": (
            q(
                "In the lab, how are task priorities assigned to the three periodic tasks?",
                (
                    opt("Rate-monotonic: shorter period means higher priority", correct=True),
                    opt("By alphabetical order of the task name"),
                    opt("By longest compute time first"),
                    opt("Round-robin with equal priority"),
                ),
                "The lab uses rate-monotonic priorities: shorter period implies higher priority, with index 0 (A_fast) highest.",
            ),
            q(
                "How does the lab detect that a task missed its deadline?",
                (
                    opt("When the timeline array stays at -1 for too long"),
                    opt(
                        "When a new job is released while the previous job's remaining work is still greater than zero",
                        correct=True,
                    ),
                    opt("When utilization U drops below the RM bound"),
                    opt("When two tasks have the same period"),
                ),
                "At each period boundary, if remaining[i] is still greater than 0 the previous job did not finish, which is recorded as a deadline miss.",
            ),
            q(
                "According to the lab's 'Try it yourself', what happens if you swap priorities so C_slow is highest?",
                (
                    opt("The fast task starves and misses its deadline", correct=True),
                    opt("All tasks finish with extra slack"),
                    opt("The simulation refuses to start"),
                    opt("DMA takes over the scheduling"),
                ),
                "Giving C_slow the highest priority starves the fast task so it misses deadlines, illustrating why rate-monotonic ordering matters.",
            ),
        ),
        "Applications & the throughline": (
            q(
                "In the worked fitness-wearable example, what dominates battery life?",
                (
                    opt("The duty cycle of being awake", correct=True),
                    opt("The size of the DMA buffer"),
                    opt("The number of I2C sensors attached"),
                    opt("The BLE radio's transmit frequency band"),
                ),
                "Battery life is dominated by the duty cycle of being awake, the single number a wearable's firmware fights for.",
            ),
            q(
                "Which domain is associated with hard real-time, CAN bus, and safety in the applications table?",
                (
                    opt("Consumer appliances and toys"),
                    opt("Automotive", correct=True),
                    opt("IoT wearables"),
                    opt("Industrial PLCs only"),
                ),
                "The table maps Automotive to engine/brake/airbag control over CAN bus, leaning on hard real-time, watchdog, RTOS, and safety.",
            ),
            q(
                "What is Edge AI / TinyML as listed in the trends to watch?",
                (
                    opt("Streaming all sensor data to the cloud for inference"),
                    opt(
                        "Running small neural nets on the MCU itself, like keyword spotting",
                        correct=True,
                    ),
                    opt("A new secure-boot signing standard"),
                    opt("A DMA cache-coherency protocol"),
                ),
                "Edge AI / TinyML runs small neural nets on the MCU itself (keyword spotting, anomaly detection) without the cloud.",
            ),
        ),
    },
    final=(
        q(
            "Which kernel mechanism lets a preemptive RTOS stop a running task to run a higher-priority one?",
            (
                opt("A context switch (e.g. via PendSV on Cortex-M)", correct=True),
                opt("A DMA completion interrupt"),
                opt("A rate-monotonic utilization test"),
                opt("A logic analyzer capture"),
            ),
            "A preemptive scheduler performs a context switch, saving and restoring registers, to run a higher-priority ready task.",
        ),
        q(
            "What is the cleanest synchronization pattern the course recommends to avoid most races?",
            (
                opt("Sharing global variables guarded by disabling interrupts"),
                opt("Passing messages through a queue instead of sharing memory", correct=True),
                opt("Busy-waiting in a tight spin loop"),
                opt("Giving every task the same priority"),
            ),
            "The lesson prefers queues over shared variables plus mutexes because passing messages sidesteps most concurrency races.",
        ),
        q(
            "Why is DMA the single biggest lever for throughput on an MCU?",
            (
                opt("It raises the CPU clock during transfers"),
                opt(
                    "It moves bulk data without the CPU, dropping per-sample CPU cost to nearly zero",
                    correct=True,
                ),
                opt("It compresses the data stream before storage"),
                opt("It guarantees deadlines under fixed priorities"),
            ),
            "DMA moves data without the CPU, so per-sample CPU cost falls to roughly one interrupt per buffer instead of per byte.",
        ),
        q(
            "As the number of tasks grows, the rate-monotonic utilization bound approaches which value?",
            (
                opt("100%"),
                opt("About 69% (ln 2)", correct=True),
                opt("About 50%"),
                opt("About 25%"),
            ),
            "The RMS bound n(2^(1/n)-1) starts at 100% for one task and decreases toward ln 2, about 69%, as n grows.",
        ),
        q(
            "What practice do the fastest embedded teams follow for testing, per the course?",
            (
                opt("Test only on target hardware with a HIL rig"),
                opt(
                    "Keep firmware logic hardware-independent and unit-test it on the host in CI",
                    correct=True,
                ),
                opt("Rely solely on printf logging in production"),
                opt("Skip unit tests and use only an oscilloscope"),
            ),
            "Fast teams keep logic hardware-independent and unit-test it on the host in CI, reserving the probe, analyzer, and HIL for hardware-coupled bugs.",
        ),
    ),
)
