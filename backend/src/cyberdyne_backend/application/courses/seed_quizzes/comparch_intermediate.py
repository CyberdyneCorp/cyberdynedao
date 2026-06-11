from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pipelining: the 5-stage pipeline": (
            q(
                "What does pipelining improve, and what does it leave unchanged?",
                (
                    opt("It lowers the latency of a single instruction"),
                    opt(
                        "It improves throughput while a single instruction's latency stays the same",
                        correct=True,
                    ),
                    opt("It improves both latency and throughput equally"),
                    opt("It reduces the number of stages an instruction passes through"),
                ),
                "Once the pipe is full one instruction completes per cycle (throughput), but a single instruction still takes all 5 stages (latency).",
            ),
            q(
                "What are the five classic RISC pipeline stages in order?",
                (
                    opt("Fetch, Execute, Decode, Memory, Write-back"),
                    opt("Decode, Fetch, Execute, Write-back, Memory"),
                    opt("Fetch, Decode, Execute, Memory, Write-back", correct=True),
                    opt("Fetch, Decode, Memory, Execute, Write-back"),
                ),
                "The order is IF (fetch), ID (decode), EX (execute), MEM (memory), WB (write-back).",
            ),
            q(
                "With N instructions and k stages, how many cycles does the pipeline take and what is the speedup limit?",
                (
                    opt("N times k cycles, with speedup approaching 1"),
                    opt("N + k - 1 cycles, with speedup approaching k for large N", correct=True),
                    opt("N + k cycles, with speedup approaching N"),
                    opt("N - k + 1 cycles, with speedup approaching k squared"),
                ),
                "Time is N + k - 1 cycles instead of N times k, and the speedup approaches the stage count k as N grows.",
            ),
        ),
        "Hazards: structural, data, and control": (
            q(
                "What causes a structural hazard, and what is a typical fix?",
                (
                    opt("A branch resolving late; fixed by prediction"),
                    opt(
                        "Two instructions needing the same hardware resource in one cycle; fixed by duplicating the resource (split I-cache and D-cache)",
                        correct=True,
                    ),
                    opt("A dependent value not yet written back; fixed by forwarding"),
                    opt("A page not in RAM; fixed by trapping to the OS"),
                ),
                "A structural hazard is contention for the same hardware; splitting the I-cache and D-cache removes the shared memory-port conflict.",
            ),
            q(
                "Why does a load-use hazard still cost one bubble even with forwarding?",
                (
                    opt("Because the ALU result is never available for forwarding"),
                    opt(
                        "Because a lw result is not ready until after MEM, so forwarding cannot fully hide it",
                        correct=True,
                    ),
                    opt("Because loads always require two stall cycles"),
                    opt("Because forwarding only works for branches"),
                ),
                "Forwarding eliminates most data hazards, but a load's result isn't ready until after MEM, so the load-use case still costs one bubble.",
            ),
            q(
                "If a fraction f of instructions stall for p penalty cycles, what is the effective CPI?",
                (
                    opt("CPI = f times p"),
                    opt("CPI = 1 + f times p", correct=True),
                    opt("CPI = 1 - f times p"),
                    opt("CPI = f + p"),
                ),
                "Stalls inflate cycles-per-instruction as CPI = 1 + f * p; e.g. f=0.20, p=2 gives 1.4.",
            ),
        ),
        "Caches, locality, and AMAT": (
            q(
                "What is the difference between temporal and spatial locality?",
                (
                    opt("Temporal means nearby addresses; spatial means the same address again"),
                    opt(
                        "Temporal means reusing the same address soon; spatial means using neighbouring addresses soon",
                        correct=True,
                    ),
                    opt("Both refer to reusing the exact same address"),
                    opt("Temporal applies only to writes; spatial applies only to reads"),
                ),
                "Temporal locality is reusing an address (loop counters); spatial locality is using neighbours (arrays), which is why caches fetch a whole block.",
            ),
            q(
                "What is the main drawback of a direct-mapped cache?",
                (
                    opt("It is the most expensive mapping to build"),
                    opt(
                        "Two hot blocks mapping to the same slot keep evicting each other, causing conflict misses",
                        correct=True,
                    ),
                    opt("A block can go anywhere, making lookup slow"),
                    opt("It cannot exploit spatial locality at all"),
                ),
                "Direct-mapped gives each block exactly one slot, so two hot blocks that map to the same slot repeatedly evict each other (conflict misses).",
            ),
            q(
                "What is the AMAT formula?",
                (
                    opt("AMAT = t_hit times miss rate times miss penalty"),
                    opt("AMAT = t_hit + miss rate"),
                    opt(
                        "AMAT = t_hit + miss rate times miss penalty",
                        correct=True,
                    ),
                    opt("AMAT = miss rate + miss penalty"),
                ),
                "Average Memory Access Time = t_hit + miss rate * miss penalty; because the penalty is large, even a small miss rate dominates.",
            ),
        ),
        "Virtual memory, paging, and the TLB": (
            q(
                "What does virtual memory provide to each process?",
                (
                    opt("Direct shared access to all physical RAM"),
                    opt(
                        "The illusion of a large, private, contiguous address space with isolation and relocation",
                        correct=True,
                    ),
                    opt("Faster instruction fetch by skipping the cache"),
                    opt("Guaranteed placement of every page in physical RAM"),
                ),
                "Virtual memory gives each process a private, contiguous address space, providing isolation, relocation, and the ability to exceed physical RAM.",
            ),
            q(
                "What is the role of the TLB?",
                (
                    opt("It stores recently used data blocks from main memory"),
                    opt(
                        "It is a small fast cache of recent virtual-to-physical address translations",
                        correct=True,
                    ),
                    opt("It holds the entire page table in fast SRAM"),
                    opt("It predicts which branch a program will take"),
                ),
                "The Translation Lookaside Buffer caches recent virtual-to-physical translations; a hit translates in about 1 cycle, avoiding a page-table walk.",
            ),
            q(
                "For 4 KB pages, how is a virtual address split into a page number and offset?",
                (
                    opt("vpn = vaddr & 0xFFF; offset = vaddr >> 12"),
                    opt("vpn = vaddr >> 12; offset = vaddr & 0xFFF", correct=True),
                    opt("vpn = vaddr >> 4; offset = vaddr & 0xF"),
                    opt("vpn = vaddr times 4096; offset = vaddr mod 4096"),
                ),
                "With a 12-bit offset for 4 KB pages, the page number is vaddr >> 12 and the offset is the low 12 bits, vaddr & 0xFFF.",
            ),
        ),
        "Performance evaluation: CPI and Amdahl's law": (
            q(
                "What three factors make up the iron law of performance?",
                (
                    opt("Clock speed alone"),
                    opt(
                        "Instruction count times CPI times clock period (seconds per cycle)",
                        correct=True,
                    ),
                    opt("Cache size times miss rate times penalty"),
                    opt("Instruction count divided by IPC times miss rate"),
                ),
                "Execution time = instruction count * CPI * clock period; IPC is 1/CPI.",
            ),
            q(
                "According to Amdahl's law, if a fraction p is sped up, what is the speedup ceiling as s approaches infinity?",
                (
                    opt("p"),
                    opt("1/(1-p)", correct=True),
                    opt("1/p"),
                    opt("s times p"),
                ),
                "Overall speedup is 1/((1-p) + p/s), capped at 1/(1-p) even with infinite s.",
            ),
            q(
                "Which mean should you report for normalized performance ratios?",
                (
                    opt("The arithmetic mean of the speedups"),
                    opt("The geometric mean", correct=True),
                    opt("The harmonic mean of clock speeds"),
                    opt("The maximum observed speedup"),
                ),
                "Use the geometric mean for normalized ratios; the arithmetic mean of speedups is misleading.",
            ),
        ),
        "Lab: cache hit-rate and pipeline speedup": (
            q(
                "In the cache simulator, how is the set index computed for an address?",
                (
                    opt("tag = addr // BLOCK // N_SETS"),
                    opt("s = (addr // BLOCK) % N_SETS", correct=True),
                    opt("s = addr * N_SETS"),
                    opt("s = addr % BLOCK"),
                ),
                "The set index is s = (addr // BLOCK) % N_SETS, while the tag is addr // BLOCK // N_SETS.",
            ),
            q(
                "How does the lab model LRU within a set?",
                (
                    opt("It evicts the most recently used tag at the end of the list"),
                    opt(
                        "On a hit it moves the tag to the end (most-recent); on a miss when full it pops index 0 (LRU)",
                        correct=True,
                    ),
                    opt("It randomly evicts any tag when the set is full"),
                    opt("It never evicts; the set grows without bound"),
                ),
                "Most-recent tags sit at the end of the list; a hit moves the tag to the end, and a full-set miss pops the front (the least-recently-used victim).",
            ),
            q(
                "What does the lab expect to happen as associativity increases for this access stream?",
                (
                    opt("The miss rate rises sharply"),
                    opt(
                        "The miss rate falls (direct-mapped is worst, 16-way is lowest), with diminishing returns",
                        correct=True,
                    ),
                    opt("The miss rate stays exactly constant"),
                    opt("Pipeline speedup drops below 1"),
                ),
                "Higher associativity cuts conflict misses with diminishing returns, so the direct-mapped (1-way) miss rate is highest and 16-way is lowest.",
            ),
        ),
    },
    final=(
        q(
            "Why does pipelining raise throughput without lowering single-instruction latency?",
            (
                opt("It removes pipeline registers between stages"),
                opt(
                    "Stages overlap so one instruction completes per cycle once full, but each instruction still traverses all stages",
                    correct=True,
                ),
                opt("It executes every instruction in a single stage"),
                opt("It shortens each instruction to fewer stages"),
            ),
            "Overlapping stages lets one instruction complete per cycle (throughput), yet a single instruction's latency remains the full stage count.",
        ),
        q(
            "Which technique eliminates most data hazards without a stall, and which hazard still forces one bubble?",
            (
                opt("Branch prediction; the structural hazard"),
                opt(
                    "Forwarding (bypassing) eliminates most data hazards; the load-use hazard still costs one bubble",
                    correct=True,
                ),
                opt("Stalling; the control hazard"),
                opt("Register renaming; the conflict miss"),
            ),
            "Forwarding routes the ALU result directly to the next EX input, but a load's value isn't ready until after MEM, so load-use still costs a bubble.",
        ),
        q(
            "Given t_hit = 1, miss rate = 0.05, and miss penalty = 100, what is AMAT?",
            (
                opt("1.05 cycles"),
                opt("5.0 cycles"),
                opt("6.0 cycles", correct=True),
                opt("100 cycles"),
            ),
            "AMAT = t_hit + miss rate * miss penalty = 1 + 0.05 * 100 = 6.0 cycles.",
        ),
        q(
            "A workload is 80% optimizable (p=0.8). With an essentially infinite speedup of that part, what is the overall speedup ceiling?",
            (
                opt("8x"),
                opt("5x", correct=True),
                opt("80x"),
                opt("1.25x"),
            ),
            "Amdahl's ceiling is 1/(1-p) = 1/(1-0.8) = 5x, regardless of how fast the optimized part becomes.",
        ),
        q(
            "What does the TLB cache, and why is it performance-critical?",
            (
                opt("Recently used data blocks, to avoid main-memory fetches"),
                opt(
                    "Recent virtual-to-physical translations, avoiding a costly page-table walk on every access",
                    correct=True,
                ),
                opt("Branch targets, to start the next fetch immediately"),
                opt("Dirty cache lines awaiting write-back"),
            ),
            "The TLB caches recent address translations; without it, each instruction would need an extra page-table memory access, which would be ruinous.",
        ),
    ),
)
