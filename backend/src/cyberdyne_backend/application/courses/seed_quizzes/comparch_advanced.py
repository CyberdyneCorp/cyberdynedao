from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Instruction-level parallelism and out-of-order execution": (
            q(
                "What does a superscalar core add over a simple in-order pipeline?",
                (
                    opt("It runs the clock at a higher frequency"),
                    opt(
                        "Multiple execution units so it can issue several instructions per cycle",
                        correct=True,
                    ),
                    opt("A larger cache hierarchy only"),
                    opt("Out-of-order retirement but single issue"),
                ),
                "A superscalar core has multiple execution units and can issue 2-8 instructions per cycle, pushing IPC above 1.",
            ),
            q(
                "What problem does register renaming solve?",
                (
                    opt("Real (true) data dependencies between instructions"),
                    opt("Cache coherence across cores"),
                    opt(
                        "False dependencies (WAR/WAW) from reusing the same architectural register",
                        correct=True,
                    ),
                    opt("Branch mispredictions"),
                ),
                "Register renaming maps architectural registers to a larger physical pool, removing WAR/WAW false dependencies so independent uses run in parallel.",
            ),
            q(
                "Why did the industry pivot from ever-wider superscalar issue to multicore?",
                (
                    opt(
                        "Wider issue gives diminishing returns because available ILP is finite",
                        correct=True,
                    ),
                    opt("Wider issue is impossible to build"),
                    opt("Multicore needs no software changes"),
                    opt("ILP is unlimited but caches are not"),
                ),
                "Dependency chains and branches cap available ILP, so wider issue yields diminishing returns, a key reason for the multicore pivot.",
            ),
        ),
        "Branch prediction": (
            q(
                "How many times per loop does a 1-bit predictor typically mispredict?",
                (
                    opt("Once, only on exit"),
                    opt("Twice, on entry and exit", correct=True),
                    opt("Never for loops"),
                    opt("Once per iteration"),
                ),
                "A 1-bit predictor remembers only the last outcome, so it mispredicts twice per loop, at entry and at exit.",
            ),
            q(
                "What does the Branch Target Buffer (BTB) cache?",
                (
                    opt("The taken/not-taken direction"),
                    opt("The 2-bit saturating counters"),
                    opt(
                        "The branch target address so the next fetch can start immediately",
                        correct=True,
                    ),
                    opt("The reorder buffer entries"),
                ),
                "The BTB caches the target address so the next fetch starts before decode even knows it was a branch; the BHT/PHT predicts direction.",
            ),
            q(
                "The added CPI penalty from branches is proportional to which product?",
                (
                    opt(
                        "Branch frequency times miss rate times misprediction penalty", correct=True
                    ),
                    opt("Cache miss rate times memory latency"),
                    opt("Issue width times pipeline depth"),
                    opt("Clock frequency times voltage squared"),
                ),
                "The effective CPI penalty equals branch frequency times miss rate times the misprediction penalty (pipeline depth in cycles).",
            ),
        ),
        "Multicore and memory consistency": (
            q(
                "In MESI, which state means this cache holds the only, dirty copy?",
                (
                    opt("Exclusive"),
                    opt("Shared"),
                    opt("Modified", correct=True),
                    opt("Invalid"),
                ),
                "Modified means this cache has the only copy and it is dirty (does not match memory); Exclusive is the only copy but clean.",
            ),
            q(
                "What is false sharing?",
                (
                    opt("Two cores reading the same variable safely"),
                    opt(
                        "Two cores writing different variables that happen to share one cache line",
                        correct=True,
                    ),
                    opt("A cache line stuck in the Invalid state forever"),
                    opt("A predictor sharing history across branches"),
                ),
                "False sharing happens when different variables land on the same cache line, so writes ping-pong the line via invalidations; padding/aligning fixes it.",
            ),
            q(
                "Which primitive is the building block of lock-free synchronization?",
                (
                    opt("A spin delay loop"),
                    opt("Atomic compare-and-swap (or LL/SC)", correct=True),
                    opt("A static branch hint"),
                    opt("A larger reorder buffer"),
                ),
                "Atomic read-modify-write instructions like compare-and-swap and LL/SC, plus barriers and locks, enforce ordering on a relaxed memory model.",
            ),
        ),
        "Accelerators, data parallelism, and the roofline model": (
            q(
                "What does SIMD mean?",
                (
                    opt("Single Instruction, Multiple Data", correct=True),
                    opt("Single Issue, Multiple Dispatch"),
                    opt("Shared Instruction Memory Decode"),
                    opt("Synchronous Inter-core Memory Daemon"),
                ),
                "SIMD lanes apply one operation to a vector of elements at once, as in SSE/AVX on x86 and NEON/SVE on ARM.",
            ),
            q(
                "Which hardware structure is built for matrix multiply in neural networks?",
                (
                    opt("Branch target buffer"),
                    opt("Reorder buffer"),
                    opt("Systolic array of multiply-accumulate cells", correct=True),
                    opt("Snooping MESI controller"),
                ),
                "A systolic array pumps data through a grid of multiply-accumulate cells, ideal for matrix multiply; TPUs and tensor cores use this idea.",
            ),
            q(
                "A low arithmetic-intensity kernel like SAXPY sits where on the roofline?",
                (
                    opt("On the flat compute roof (compute-bound)"),
                    opt("On the sloped roof (memory-bound)", correct=True),
                    opt("Exactly at the ridge point always"),
                    opt("Above the peak compute roof"),
                ),
                "Attainable performance is min(peak compute, intensity times bandwidth); low intensity kernels are memory-bound on the sloped roof.",
            ),
        ),
        "SoC and modern systems": (
            q(
                "What does the memory controller do on an SoC?",
                (
                    opt("Predicts branch directions"),
                    opt(
                        "Turns load/store requests into DRAM command sequences and schedules them for bandwidth",
                        correct=True,
                    ),
                    opt("Renames architectural registers"),
                    opt("Routes packets between every block"),
                ),
                "The memory controller issues precise DRAM commands (activate, read/write, precharge), schedules for bandwidth, and handles refresh.",
            ),
            q(
                "Why use a network-on-chip instead of a single shared bus?",
                (
                    opt("It removes the need for caches"),
                    opt(
                        "A shared bus cannot keep up with dozens of blocks; a NoC routes packets for scalable bandwidth",
                        correct=True,
                    ),
                    opt("It eliminates the memory controller"),
                    opt("It makes the chip run at a higher voltage"),
                ),
                "With dozens of blocks on a die, a single bus saturates; a NoC routes packets over a mesh or ring for scalable, locality-aware bandwidth.",
            ),
            q(
                "What distinguishes a microcontroller (MCU) from an application SoC?",
                (
                    opt("The MCU has a full MMU, OS, and gigabytes of DRAM"),
                    opt(
                        "The MCU is a simple core with on-chip flash/SRAM, often no MMU, running bare-metal or an RTOS",
                        correct=True,
                    ),
                    opt("The application SoC has no GPU or NPU"),
                    opt("They are identical except for clock speed"),
                ),
                "An MCU packs a simple core, on-chip flash/SRAM and peripherals, often Harvard with no MMU; an application SoC has OoO CPUs, GPU/NPU, MMU and an OS.",
            ),
        ),
        "Applications, use cases, and the throughline": (
            q(
                "Which vulnerabilities exploited speculative execution?",
                (
                    opt("Heartbleed and Shellshock"),
                    opt("Spectre and Meltdown", correct=True),
                    opt("Rowhammer and Dirty COW"),
                    opt("SQL injection and XSS"),
                ),
                "Spectre and Meltdown exploited speculative execution, putting microarchitecture squarely in the security spotlight.",
            ),
            q(
                "For a high-frequency trading engine, which techniques matter most?",
                (
                    opt(
                        "Keep the hot path in L1/L2, avoid unpredictable branches, pin threads to avoid false sharing",
                        correct=True,
                    ),
                    opt("Maximize DRAM capacity and ignore branch behavior"),
                    opt("Run everything on a single GPU"),
                    opt("Rely on the OS scheduler to migrate threads freely"),
                ),
                "Latency-critical trading keeps data in L1/L2 (locality), uses branchless code, pins threads to avoid coherence traffic and false sharing, and bypasses the kernel.",
            ),
            q(
                "Which two laws are named as bounding everything in the throughline?",
                (
                    opt("Moore's law and Dennard scaling"),
                    opt("The memory wall and Amdahl's law", correct=True),
                    opt("Little's law and Gustafson's law"),
                    opt("Ohm's law and Kirchhoff's law"),
                ),
                "The memory wall (compute outran memory, so locality rules) and Amdahl's law (the serial part bounds parallel speedup) bound everything.",
            ),
        ),
        "Lab: branch-prediction accuracy and a roofline plot": (
            q(
                "On the loop-heavy part of the stream, why does the 2-bit predictor win?",
                (
                    opt("It mispredicts once per loop instead of twice", correct=True),
                    opt("It ignores the loop entirely"),
                    opt("It uses a branch target buffer"),
                    opt("It predicts forward branches not taken"),
                ),
                "The 2-bit saturating counter needs two wrong guesses to flip, so a loop mispredicts only once (on exit) versus twice for the 1-bit predictor.",
            ),
            q(
                "In the roofline experiment, how is the ridge point computed?",
                (
                    opt("peak_flops divided by bw", correct=True),
                    opt("bw multiplied by peak_flops"),
                    opt("intensity multiplied by bw"),
                    opt("peak_flops minus bw"),
                ),
                "The ridge-point intensity is peak_flops / bw; in the lab that is 1000/100 = 10 FLOP/byte where the sloped and flat roofs meet.",
            ),
            q(
                "The lab suggests doubling the bandwidth to bw=200. What happens?",
                (
                    opt("The ridge point moves right and fewer kernels are compute-bound"),
                    opt(
                        "The ridge point moves left and more kernels become compute-bound",
                        correct=True,
                    ),
                    opt("The peak compute roof rises"),
                    opt("Branch predictor accuracy improves"),
                ),
                "Raising bandwidth tilts the sloped roof up, moving the ridge point left so more kernels reach the flat compute roof (become compute-bound).",
            ),
        ),
    },
    final=(
        q(
            "Which technique is the key enabler of out-of-order execution by removing false dependencies?",
            (
                opt("Branch prediction"),
                opt("Register renaming", correct=True),
                opt("Cache blocking"),
                opt("Memory barriers"),
            ),
            "Register renaming maps architectural registers to a larger physical pool, eliminating WAR/WAW false dependencies that would otherwise serialize OoO execution.",
        ),
        q(
            "A core writes a cache line that is Shared in MESI. What must happen first?",
            (
                opt("Other copies must be invalidated, costing cross-core traffic", correct=True),
                opt("The line moves directly to Exclusive with no traffic"),
                opt("The reorder buffer flushes"),
                opt("The branch predictor is retrained"),
            ),
            "A write must invalidate other cached copies before transitioning to Modified, which costs cross-core invalidation traffic.",
        ),
        q(
            "According to the roofline model, a memory-bound kernel gets faster mainly by what?",
            (
                opt("Adding a faster ALU"),
                opt(
                    "Raising arithmetic intensity (tiling, fusing, reuse) or buying more bandwidth",
                    correct=True,
                ),
                opt("Increasing branch prediction accuracy"),
                opt("Widening the superscalar issue"),
            ),
            "Memory-bound kernels sit on the sloped roof; a beefier ALU does not help, so raise arithmetic intensity or add bandwidth.",
        ),
        q(
            "Why can two cores at half clock beat one core at full clock on power?",
            (
                opt("Because IPC doubles automatically"),
                opt("Because dynamic power rises roughly with the cube of frequency", correct=True),
                opt("Because caches get larger"),
                opt("Because branch mispredictions disappear"),
            ),
            "Dynamic power scales as C times V squared times f, and voltage tracks frequency, so power grows about cubically; lower clocks save large amounts of power.",
        ),
        q(
            "Which pair of laws does the track name as bounding all performance?",
            (
                opt("The memory wall and Amdahl's law", correct=True),
                opt("Moore's law and Little's law"),
                opt("Dennard scaling and Gustafson's law"),
                opt("Ohm's law and Amdahl's law"),
            ),
            "The throughline names the memory wall (locality rules because compute outran memory) and Amdahl's law (serial part bounds parallel speedup).",
        ),
    ),
)
