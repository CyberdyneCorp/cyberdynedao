from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Data representation and the ISA": (
            q(
                "In two's complement, how do you negate a value?",
                (
                    opt("Add 1 to the top bit"),
                    opt("Flip all bits and add 1", correct=True),
                    opt("Flip only the top bit"),
                    opt("Subtract the value from zero without changing bits"),
                ),
                "Two's complement negation is flip all bits and add 1, which lets one adder serve both signed and unsigned.",
            ),
            q(
                "What does the Instruction Set Architecture (ISA) define?",
                (
                    opt("The exact transistor layout of the chip"),
                    opt(
                        "The visible interface: registers, instructions, encodings, addressing modes, memory model",
                        correct=True,
                    ),
                    opt("The clock frequency and power budget"),
                    opt("The operating system scheduler policy"),
                ),
                "The ISA is the contract between software and hardware; the microarchitecture beneath it can change while the ISA stays stable.",
            ),
            q(
                "Which addressing mode is the workhorse for arrays and structs?",
                (
                    opt("Immediate"),
                    opt("Register"),
                    opt("Base plus offset", correct=True),
                    opt("PC-relative"),
                ),
                "Base plus offset computes mem[reg + const], the natural way to index arrays and struct fields.",
            ),
        ),
        "The datapath and a single-cycle CPU": (
            q(
                "What does the program counter (PC) hold?",
                (
                    opt("The result of the last ALU operation"),
                    opt("The address of the next instruction", correct=True),
                    opt("The current stack pointer"),
                    opt("The opcode being decoded"),
                ),
                "The PC holds the address of the next instruction to fetch.",
            ),
            q(
                "Why must a single-cycle clock period cover the slowest instruction's path?",
                (
                    opt(
                        "Because every instruction must finish within one clock tick", correct=True
                    ),
                    opt("Because the ALU only works at one fixed speed"),
                    opt("Because the register file has a single port"),
                    opt("Because memory cannot be read and written together"),
                ),
                "A single-cycle CPU completes one whole instruction per tick, so the period must cover the longest path (typically a load).",
            ),
            q(
                "Which control signals are set for a load (lw)?",
                (
                    opt("ALUSrc=1, MemRead=1, MemtoReg=1, RegWrite=1", correct=True),
                    opt("ALUSrc=0, MemWrite=1, RegWrite=0"),
                    opt("MemRead=0, MemtoReg=0, RegWrite=0"),
                    opt("Branch=1, MemRead=1, RegWrite=0"),
                ),
                "A load uses the immediate (ALUSrc=1), reads memory (MemRead=1), writes the loaded value (MemtoReg=1), and enables the register write (RegWrite=1).",
            ),
        ),
        "The memory hierarchy and buses": (
            q(
                "Why does a memory hierarchy exist?",
                (
                    opt(
                        "Fast memory is small and expensive while big memory is slow", correct=True
                    ),
                    opt("DRAM is faster than SRAM"),
                    opt("Registers are larger than main memory"),
                    opt("Storage is the fastest layer"),
                ),
                "The hierarchy layers fast-small over slow-large memory because no single technology is both fast and big and cheap.",
            ),
            q(
                "What sets the maximum addressable memory?",
                (
                    opt("The width of the data bus"),
                    opt("The width of the address bus", correct=True),
                    opt("The number of control lines"),
                    opt("The clock frequency"),
                ),
                "Address-bus width of b bits addresses 2^b locations, so it bounds the addressable memory.",
            ),
            q(
                "How do most modern CPUs combine von Neumann and Harvard designs?",
                (
                    opt("Pure Harvard everywhere"),
                    opt("Pure von Neumann everywhere"),
                    opt(
                        "von Neumann at main memory but Harvard at the L1 cache (split I-cache and D-cache)",
                        correct=True,
                    ),
                    opt("Harvard at main memory but von Neumann at L1"),
                ),
                "Most CPUs are von Neumann at main memory yet split the L1 into I-cache and D-cache (Harvard) for the best of both.",
            ),
        ),
        "Assembly programming basics": (
            q(
                "In RISC-V, which register is always zero?",
                (
                    opt("x0", correct=True),
                    opt("x1"),
                    opt("sp"),
                    opt("ra"),
                ),
                "RISC-V has 32 integer registers x0 through x31, and x0 always reads as zero.",
            ),
            q(
                "Under the calling convention, where do arguments and the return value go?",
                (
                    opt("Arguments in a0-a7; return value in a0", correct=True),
                    opt("Arguments in s0-s11; return value in ra"),
                    opt("Arguments in t0-t6; return value in sp"),
                    opt("All arguments on the stack; return value in t0"),
                ),
                "Arguments are passed in a0-a7 and the return value comes back in a0.",
            ),
            q(
                "Which registers must a function preserve (callee-saved)?",
                (
                    opt("t0-t6"),
                    opt("a0-a7"),
                    opt("s0-s11", correct=True),
                    opt("x0 only"),
                ),
                "Callee-saved s0-s11 must be preserved by the function that uses them; t0-t6 are caller-saved and may be clobbered.",
            ),
        ),
        "I/O and buses: polling vs interrupts": (
            q(
                "What is memory-mapped I/O (MMIO)?",
                (
                    opt(
                        "Device registers live at ordinary memory addresses accessed with normal loads and stores",
                        correct=True,
                    ),
                    opt("A separate set of special I/O-only instructions"),
                    opt("Mapping files into the page table"),
                    opt("Using DMA for every device access"),
                ),
                "With MMIO, device registers sit at ordinary addresses, so the same lw/sw read and write them; no special instructions are needed.",
            ),
            q(
                "Why is the volatile keyword essential for MMIO in C?",
                (
                    opt("It makes the access atomic across cores"),
                    opt(
                        "It tells the compiler the value can change outside the program, so it must not cache or reorder the access",
                        correct=True,
                    ),
                    opt("It places the variable in read-only memory"),
                    opt("It forces the value into a CPU register"),
                ),
                "volatile prevents the compiler from caching or reordering the access because the device can change the value independently.",
            ),
            q(
                "When do interrupts win over polling?",
                (
                    opt("For very frequent events where per-interrupt overhead dominates"),
                    opt(
                        "For rare events, since the CPU does real work until something happens",
                        correct=True,
                    ),
                    opt("Never; polling is always more efficient"),
                    opt("Only when no DMA controller is present"),
                ),
                "For rare events interrupts win big; for very frequent events the per-interrupt overhead can dominate and polling or DMA wins.",
            ),
        ),
        "Lab: simulate a tiny CPU datapath": (
            q(
                "What kind of machine does the lab simulator model?",
                (
                    opt("A single-cycle machine where every instruction costs one cycle"),
                    opt("A multi-cycle machine with a per-opcode cycle cost", correct=True),
                    opt("A superscalar out-of-order core"),
                    opt("A pipelined 5-stage machine"),
                ),
                "The lab uses a cost dict per opcode (LOADI=1, ADD=2, SUB=2, OUT=3), modeling a multi-cycle machine rather than single-cycle.",
            ),
            q(
                "What value does the simulated program output?",
                (
                    opt("15"),
                    opt("12", correct=True),
                    opt("10"),
                    opt("3"),
                ),
                "It computes r2 = 10 + 5 = 15, then r2 = 15 - 3 = 12, and outputs 12.",
            ),
            q(
                "How does the lab suggest making the simulator model a single-cycle machine?",
                (
                    opt("Set all entries in the cost dict to 1", correct=True),
                    opt("Remove the OUT instruction"),
                    opt("Add more registers to the machine"),
                    opt("Increase the number of ADD instructions"),
                ),
                "Setting every cost to 1 makes each instruction take one cycle, modeling a single-cycle machine.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about two's complement is correct?",
            (
                opt("The top bit has weight +2^(n-1)"),
                opt(
                    "The top bit has weight -2^(n-1), so an 8-bit byte covers -128 to 127",
                    correct=True,
                ),
                opt("It needs a separate adder for signed and unsigned values"),
                opt("An 8-bit byte covers 0 to 255 only"),
            ),
            "In two's complement the top bit carries weight -2^(n-1); an 8-bit byte spans -128 to 127 and one adder handles both signed and unsigned.",
        ),
        q(
            "What primarily improves a RISC ISA's pipeline-friendliness compared to CISC?",
            (
                opt("Variable-length instructions"),
                opt("Many instructions that touch memory directly"),
                opt(
                    "Fixed-length instructions and a load/store design with simple decode",
                    correct=True,
                ),
                opt("Fewer registers"),
            ),
            "RISC uses fixed-length instructions, only load/store touch memory, and decode is simple, which is pipeline-friendly.",
        ),
        q(
            "Order the memory hierarchy from fastest/smallest to slowest/largest.",
            (
                opt("Registers, L1 cache, main memory (DRAM), storage", correct=True),
                opt("Main memory, registers, storage, L1 cache"),
                opt("Storage, main memory, L1 cache, registers"),
                opt("L1 cache, registers, storage, main memory"),
            ),
            "Latency rises with distance from the core: registers, then L1/L2/L3 SRAM caches, then DRAM, then SSD/disk storage.",
        ),
        q(
            "A function needs to use s2 and call another function. What must it do?",
            (
                opt("Nothing; s2 and ra are automatically preserved by hardware"),
                opt(
                    "Save s2 (callee-saved) and save ra on the stack before the call, then restore them",
                    correct=True,
                ),
                opt("Save only t0-t6 since those survive calls"),
                opt("Pass s2 in a0 to protect it"),
            ),
            "s2 is callee-saved so it must be preserved, and the return address ra must be saved on the stack across a nested call.",
        ),
        q(
            "For bulk transfers like disk or network, what cuts the CPU out of the data-moving loop?",
            (
                opt("Polling a status register faster"),
                opt(
                    "A DMA controller that moves blocks and interrupts only when done", correct=True
                ),
                opt("Adding more interrupt lines"),
                opt("Using port I/O instead of MMIO"),
            ),
            "A DMA controller moves blocks between a device and memory on its own, interrupting the CPU only when the whole transfer completes.",
        ),
    ),
)
