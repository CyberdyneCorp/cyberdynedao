"""Academy seed content — the Operating Systems track (Beginner → Advanced).

* ``os-basics``        — what an OS does, processes, scheduling, memory, files
* ``os-intermediate``  — scheduling algorithms, concurrency, deadlock, paging
* ``os-advanced``      — virtual memory internals, FS internals, kernels, RTOS

Runnable ``code`` lessons *simulate* OS algorithms (schedulers, banker's
algorithm, page replacement) in pure Python builtins + numpy — no real syscalls
(the sandbox blocks os/threading), which is exactly how OS courses teach them.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ²) in diagrams and labels.
# ruff: noqa: RUF001

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
# os-basics
# ──────────────────────────────────────────────────────────────────────

_OS_BASICS = SeedCourse(
    slug="os-basics",
    title="Operating Systems — Basics",
    description=(
        "What an operating system actually does: managing processes, the CPU, "
        "memory, and files; kernel vs user space and system calls. With a "
        "runnable round-robin scheduler so you see time-sharing happen."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What an operating system does",
            "9 min",
            r"""# What an operating system does

An **operating system (OS)** is the software layer between your programs and the
hardware. It's a **resource manager** and an **abstraction provider**:

- **Manages resources** — shares the CPU, memory, disk, and devices among many
  programs fairly and safely.
- **Provides abstractions** — your program says "open this file" or "allocate
  memory", not "move the disk head to cylinder 9" or "set these RAM chips". The
  OS turns clean abstractions (processes, files, sockets) into messy hardware
  operations.
- **Isolates and protects** — one buggy or malicious program can't crash the
  others or read their memory.

## Kernel vs user space

The OS runs in two privilege levels enforced by the CPU:

- **Kernel space** — the core OS, full hardware access (scheduling, memory
  management, device drivers). A crash here takes down the machine.
- **User space** — your applications, sandboxed. They can't touch hardware
  directly; they must **ask** the kernel.

That "ask" is a **system call** — a controlled doorway into the kernel (`read`,
`write`, `fork`, `mmap`). The CPU traps into kernel mode, the kernel does the
privileged work, and returns. This boundary is what makes a multi-user,
multi-program machine both possible and safe.
""",
        ),
        _t(
            "Processes & their lifecycle",
            "10 min",
            r"""# Processes & their lifecycle

A **process** is a program *in execution* — not the file on disk, but a running
instance with its own:

- **Address space** — its private memory (code, data, heap, stack).
- **Registers & program counter** — where it is in execution.
- **Resources** — open files, sockets — tracked by the OS in a **Process
  Control Block (PCB)**.

Isolation is the point: each process thinks it has the machine to itself; the OS
keeps them apart.

## The state machine

A process moves between states as it runs and waits:

```
  new → ready ⇄ running → terminated
              ↑     │
              └─ waiting (blocked on I/O)
```

- **Ready** — could run, waiting for a CPU.
- **Running** — currently on a CPU.
- **Waiting/blocked** — paused for something (disk, network, a lock).
- The **scheduler** moves processes between *ready* and *running*; a **context
  switch** saves one process's registers and loads another's.

Processes are created by **forking** (a parent spawns a child) and cleaned up on
exit. With more processes than CPUs, the OS rapidly switches between them — fast
enough to create the *illusion* that everything runs at once. How it chooses who
runs next is **scheduling**, up next.
""",
        ),
        _code(
            "A round-robin scheduler",
            "12 min",
            r"""# Round-robin: give each ready process a fixed time slice (quantum), then
# rotate. It's how time-sharing creates the illusion of concurrency. Press Run.

# Processes: name -> CPU time still needed (burst).
burst = {"P1": 5, "P2": 3, "P3": 4}
quantum = 2

queue = list(burst.keys())     # ready queue (round-robin order)
remaining = dict(burst)
clock = 0
timeline = []

while queue:
    proc = queue.pop(0)        # take the front of the queue
    run = min(quantum, remaining[proc])
    timeline.append((proc, clock, clock + run))
    clock = clock + run
    remaining[proc] = remaining[proc] - run   # (subscript += is blocked in the sandbox)
    if remaining[proc] > 0:
        queue.append(proc)     # not done -> back of the queue
    # (a real OS would also insert newly-arrived processes here)

print("execution timeline (proc: start-end):")
for proc, start, end in timeline:
    print(f"  {proc}: {start}-{end}")
print("total time:", clock)
print("context switches:", len(timeline) - 1)
# Try: a smaller quantum -> more switches (overhead) but snappier response.
""",
        ),
        _t(
            "Threads vs processes",
            "9 min",
            r"""# Threads vs processes

A **thread** is a unit of execution *within* a process. A process can have many
threads that **share its memory** (code, heap, globals) but each has its **own
stack and registers**.

| | Process | Thread |
|---|---|---|
| Memory | isolated, private | shared with siblings |
| Creation cost | heavy | light |
| Communication | IPC (pipes, sockets) | shared variables |
| A crash… | contained | can take down the whole process |

**Why threads?** Concurrency within one program — keep a UI responsive while
work runs, or use multiple CPU cores in parallel. The cost: shared memory means
**race conditions** if threads touch the same data without coordination (the
Intermediate course tackles this).

A **context switch** between threads is cheaper than between processes (no need
to swap the address space), but it isn't free — saving/restoring state and
cache effects add up. More threads is not always faster:

```plot
{"title": "Throughput rises, then thrashes (too many threads)", "xLabel": "number of threads", "yLabel": "useful work / sec", "xRange": [1, 16], "yRange": [0, 1.1], "functions": [{"expr": "x/4 * exp(-x/6)*2.7", "label": "throughput", "color": "#2563eb"}]}
```

Beyond the core count (plus some for I/O overlap), extra threads mostly add
switching and contention overhead. Match concurrency to the work and the
hardware.
""",
        ),
        _t(
            "Memory: stack, heap & virtual memory",
            "10 min",
            r"""# Memory: stack, heap & virtual memory

Each process sees a clean, private **address space**, laid out roughly:

```
high │  stack    ↓   (function calls, locals — grows down)
     │   ...
     │  heap     ↑   (malloc/new — grows up)
     │  data         (globals, static)
low  │  code         (the program instructions)
```

- **Stack** — fast, automatic: a frame is pushed on each function call (its
  locals, return address) and popped on return. Fixed-ish size — deep recursion
  blows it (**stack overflow**).
- **Heap** — dynamic memory you request and (in C/C++) must free. Flexible but
  slower, and the source of leaks and use-after-free bugs.

## The big illusion: virtual memory

Programs don't use physical RAM addresses. The OS + CPU's **MMU** give each
process a private **virtual** address space and translate virtual → physical
addresses on the fly, in fixed-size **pages**. This buys you:

- **Isolation** — a process literally cannot name another's memory.
- **More memory than you have** — inactive pages spill to disk (**swap**).
- **Simplicity** — every program is compiled as if it owns all of memory.

The page-table machinery (paging, the TLB, page faults) is the heart of the
Intermediate and Advanced courses — but the takeaway now: the addresses your
program sees are a convenient fiction the OS maintains.
""",
        ),
        _t(
            "Files & filesystems",
            "8 min",
            r"""# Files & filesystems

A **file** is the OS's abstraction for persistent, named bytes — whether on an
SSD, spinning disk, or network. A **filesystem** organises files into a
hierarchy of **directories** and tracks where each file's data physically lives.

What the OS hides for you:

- **Naming & hierarchy** — human paths (`/home/leo/report.txt`) instead of disk
  block numbers.
- **Metadata** — size, owner, permissions, timestamps (in Unix, an **inode**
  holds this plus pointers to the data blocks; the directory just maps a name to
  an inode).
- **Permissions** — who may read/write/execute (Unix `rwx` for user/group/other).
- **Open files** — a process gets a **file descriptor** (a small integer) from
  `open()`, then `read`/`write`/`seek`/`close` through it.

Everything-is-a-file is a Unix superpower: devices (`/dev/...`), pipes, and
sockets present the same `read`/`write` interface, so the same tools compose
over all of them.

Reliability matters because crashes happen mid-write. Modern filesystems use
**journaling** — record the intended change in a log first, so an interrupted
operation can be replayed or rolled back cleanly (more in Advanced).
""",
        ),
        _t(
            "System calls & the shell",
            "8 min",
            r"""# System calls & the shell

A program can't touch hardware directly — it requests OS services through
**system calls**, the API of the kernel. The essentials (Unix):

- **Processes** — `fork` (clone the current process), `exec` (replace its image
  with a new program), `wait`, `exit`.
- **Files** — `open`, `read`, `write`, `close`, `lseek`.
- **Communication** — `pipe`, `socket`, `mmap`.

A system call **traps** into kernel mode, the kernel validates and performs the
privileged operation, then returns to your program — the controlled, checked
boundary that keeps the system safe.

The **shell** (bash, zsh) is just a user program that reads commands and orchestrates
these calls. When you run `ls | grep txt`:

```bash
ls | grep txt        # the shell: fork two processes, connect them with a pipe()
```

the shell `fork`s, sets up a `pipe` so `ls`'s output becomes `grep`'s input, and
`exec`s each command. **fork + exec** is how every program you launch comes to
life. Understanding this demystifies the shell: pipes, redirection (`>`, `<`),
and background jobs (`&`) are all thin sugar over a handful of system calls.

```bash
strace ls            # (read-only) watch the actual system calls a program makes
```
""",
        ),
        quiz_lesson(
            "Quiz: OS Basics",
            (
                q(
                    "What are the two core jobs of an operating system?",
                    (
                        opt(
                            "Manage hardware resources and provide abstractions to programs",
                            correct=True,
                        ),
                        opt("Compile code and render graphics"),
                        opt("Encrypt files and serve web pages"),
                        opt("Replace the BIOS"),
                    ),
                    "The OS shares resources (CPU/memory/devices) and abstracts hardware (processes/files).",
                ),
                q(
                    "What is a system call?",
                    (
                        opt(
                            "A controlled request from user space into the kernel for a privileged operation",
                            correct=True,
                        ),
                        opt("A function call within your own program"),
                        opt("A network request to another machine"),
                        opt("A compiler directive"),
                    ),
                    "User code traps into kernel mode via syscalls (read, write, fork) to use hardware safely.",
                ),
                q(
                    "How do threads differ from processes?",
                    (
                        opt(
                            "Threads share their process's memory; processes are isolated",
                            correct=True,
                        ),
                        opt("Threads have separate address spaces; processes share memory"),
                        opt("Threads can't run in parallel"),
                        opt("Processes are always faster to create"),
                    ),
                    "Shared memory makes threads light and fast to communicate — but prone to race conditions.",
                ),
                q(
                    "In round-robin scheduling, what does a smaller time quantum cause?",
                    (
                        opt(
                            "More context switches (overhead) but snappier responsiveness",
                            correct=True,
                        ),
                        opt("Fewer context switches and slower response"),
                        opt("Processes never finish"),
                        opt("Memory leaks"),
                    ),
                    "A small quantum rotates faster (responsive) but spends more time switching.",
                ),
                q(
                    "What does virtual memory give each process?",
                    (
                        opt(
                            "A private virtual address space, isolating it and allowing more memory than physical RAM",
                            correct=True,
                        ),
                        opt("Direct access to physical RAM addresses"),
                        opt("A copy of the kernel"),
                        opt("Faster CPUs"),
                    ),
                    "The MMU translates per-process virtual addresses to physical pages, isolating processes and enabling swap.",
                ),
                q(
                    "How does the shell run `ls | grep txt`?",
                    (
                        opt(
                            "fork two processes and connect them with a pipe (stdout → stdin)",
                            correct=True,
                        ),
                        opt("Run both commands in the kernel"),
                        opt("Merge them into one program"),
                        opt("Send them to a remote server"),
                    ),
                    "The shell forks/execs each command and wires a pipe between them — fork+exec is the core pattern.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# os-intermediate
# ──────────────────────────────────────────────────────────────────────

_OS_INTERMEDIATE = SeedCourse(
    slug="os-intermediate",
    title="Operating Systems — Intermediate",
    description=(
        "The classic algorithms: CPU scheduling (FCFS/SJF/RR/priority), "
        "concurrency and synchronization, deadlock and the banker's algorithm, "
        "and demand paging with page-replacement policies — several runnable as "
        "simulations you compare yourself."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "CPU scheduling algorithms",
            "11 min",
            r"""# CPU scheduling algorithms

With more ready processes than CPUs, the **scheduler** picks who runs next. The
classics, with their trade-offs:

- **FCFS (First-Come-First-Served)** — a simple queue. Fair-ish, but a long job
  at the front delays everyone (the **convoy effect**).
- **SJF (Shortest Job First)** — run the shortest burst next. *Optimal* average
  waiting time, but you must know/estimate burst lengths, and long jobs can
  **starve**.
- **Round-Robin (RR)** — time slices in rotation. Great **responsiveness** for
  interactive systems; quantum size is the key knob.
- **Priority** — highest priority first. Flexible, but low-priority jobs can
  starve → fix with **aging** (raise priority the longer you wait).

Key metrics to compare them by:

- **Waiting time** — time spent ready but not running.
- **Turnaround** — total time from arrival to completion.
- **Response time** — arrival to *first* run (what interactive users feel).

**Preemptive** schedulers (RR, preemptive SJF) can interrupt a running process;
**non-preemptive** ones (FCFS, plain SJF) run a job to its next block/exit. Real
OSes use **multi-level feedback queues** — multiple priority queues with
different quanta, automatically demoting CPU-hogs and favouring interactive jobs.
You'll measure these next.
""",
        ),
        _code(
            "Compare schedulers by average wait",
            "13 min",
            r"""# Compute average WAITING TIME for FCFS vs SJF on the same jobs.
# SJF minimises it — see by how much. (All jobs arrive at time 0.)

jobs = {"P1": 7, "P2": 3, "P3": 1, "P4": 5}   # name -> burst time

def avg_wait(order, burst):
    # Waiting time of each job = sum of bursts of everyone before it.
    clock = 0
    total = 0
    for name in order:
        total = total + clock   # this job waited 'clock' units before starting
        clock = clock + burst[name]
    return total / len(order)

fcfs_order = list(jobs.keys())                       # arrival order
# shortest burst first — sort (burst, name) pairs (no lambda over a global):
pairs = []
for name in jobs:
    pairs.append((jobs[name], name))
pairs.sort()
sjf_order = [name for burst_value, name in pairs]

print("bursts:", jobs)
print("FCFS order:", fcfs_order, "-> avg wait", round(avg_wait(fcfs_order, jobs), 2))
print("SJF  order:", sjf_order, "-> avg wait", round(avg_wait(sjf_order, jobs), 2))
print("\\nSJF is provably optimal for average waiting time —")
print("running short jobs first lets everyone behind them wait less.")
""",
        ),
        _t(
            "Concurrency: races, mutexes & semaphores",
            "11 min",
            r"""# Concurrency: races, mutexes & semaphores

When threads share data, trouble starts. A **race condition**: the result
depends on the *timing* of interleavings. The classic — two threads both run
`balance = balance + 100`:

```
read balance (100) ─┐                 ┌─ read balance (100)
add 100 -> 200      │  interleaved →  │  add 100 -> 200
write 200 ──────────┘                 └─ write 200   # one +100 LOST!
```

The fix is to make the dangerous section **atomic** — a **critical section**
only one thread enters at a time. Primitives:

- **Mutex (lock)** — `acquire()` before the critical section, `release()` after.
  Only the holder proceeds; others block.
- **Semaphore** — a counter; allows up to *N* threads (a mutex is a binary
  semaphore). Used for pools and signalling.
- **Condition variables** — wait until some condition holds (e.g.
  producer–consumer: consumers wait until the buffer is non-empty).

The rules that keep you sane:

- **Hold locks briefly**, around the smallest critical section.
- **Always acquire multiple locks in the same global order** (prevents
  deadlock — next lesson).
- Prefer higher-level constructs (thread-safe queues, immutable data,
  message-passing) over hand-rolled locking when you can — they're far easier to
  get right.
""",
        ),
        _t(
            "Deadlock",
            "10 min",
            r"""# Deadlock

A **deadlock** is a standstill where processes each hold a resource and wait for
one another forever. The textbook case: P1 holds lock A and wants B; P2 holds B
and wants A. Neither yields.

Deadlock needs **all four Coffman conditions** at once — break any one and you're
safe:

1. **Mutual exclusion** — resources can't be shared.
2. **Hold and wait** — hold one resource while waiting for another.
3. **No preemption** — resources can't be forcibly taken.
4. **Circular wait** — a cycle of "waiting-for".

Strategies:

- **Prevention** — design out a condition. The easiest in practice: impose a
  **global lock ordering** so a circular wait is impossible.
- **Avoidance** — grant a request only if the system stays in a *safe* state
  (the **banker's algorithm**, next lesson).
- **Detection & recovery** — let deadlocks happen, detect cycles in the
  wait-for graph, then kill/restart a victim.
- **Ostrich algorithm** — ignore it and reboot if rare (yes, really — common for
  unlikely cases).

Most application code avoids deadlock simply by **acquiring locks in a
consistent order** and **not holding a lock while calling out** to code that
might grab another. The banker's algorithm shows the formal "is this safe?"
check you'll implement next.
""",
        ),
        _code(
            "Banker's algorithm: is this state safe?",
            "14 min",
            r"""# The banker's algorithm: only grant resources if the system can still finish
# every process. It searches for a 'safe sequence'. Uses numpy for the matrices.
import numpy as np

total = np.array([10, 5, 7])              # total units of resources A, B, C

# Per-process: what it has now (allocation) and the most it may still need.
allocation = np.array([[0, 1, 0],
                       [2, 0, 0],
                       [3, 0, 2],
                       [2, 1, 1],
                       [0, 0, 2]])
maximum = np.array([[7, 5, 3],
                    [3, 2, 2],
                    [9, 0, 2],
                    [2, 2, 2],
                    [4, 3, 3]])
need = maximum - allocation
available = total - allocation.sum(axis=0)

n = allocation.shape[0]
finished = [False] * n
work = available.copy()
sequence = []

made_progress = True
while made_progress:
    made_progress = False
    for i in range(n):
        if not finished[i] and bool(np.all(need[i] <= work)):
            work = work + allocation[i]    # process i finishes, frees its resources
            finished[i] = True
            sequence.append("P" + str(i))
            made_progress = True

if all(finished):
    print("SAFE — a safe sequence exists:", " -> ".join(sequence))
else:
    print("UNSAFE — no sequence lets every process finish (deadlock risk)")
print("available at start:", list(available))
""",
        ),
        _t(
            "Paging, page faults & the TLB",
            "10 min",
            r"""# Paging, page faults & the TLB

Virtual memory works in fixed-size **pages** (e.g. 4 KB). A **page table** maps
each virtual page to a physical **frame**. When a program accesses an address:

1. The CPU splits it into (page number, offset).
2. It looks up the frame in the page table.
3. If the page is in RAM → translate and go. If not → a **page fault**: the OS
   fetches it from disk into a frame (evicting another if memory is full), then
   retries.

Page faults are expensive (disk is ~100,000× slower than RAM), so we minimise
them. Two accelerators:

- **TLB (Translation Lookaside Buffer)** — a small cache of recent page→frame
  translations, so most lookups skip the page table entirely.
- **Locality** — programs reuse the same pages (loops, nearby data), so caching
  works.

More frames generally means fewer faults, with diminishing returns:

```plot
{"title": "Page-fault rate falls as you give a process more frames", "xLabel": "frames allocated", "yLabel": "page-fault rate", "xRange": [1, 12], "yRange": [0, 1.05], "functions": [{"expr": "exp(-0.45*x) + 0.03", "label": "fault rate", "color": "#dc2626"}]}
```

But *which* page to evict matters enormously — a good **replacement policy**
gets far fewer faults for the same memory. You'll compare two next. (Curiously,
for the naive FIFO policy, more frames can sometimes cause *more* faults —
**Bélády's anomaly**.)
""",
        ),
        _code(
            "Page replacement: FIFO vs LRU",
            "13 min",
            r"""# Given a page-reference string and a fixed number of frames, count page
# faults under FIFO (evict oldest loaded) vs LRU (evict least-recently-used).

refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
frames = 3

def fifo_faults(refs, capacity):
    mem = []          # acts as a queue; front = oldest
    faults = 0
    for page in refs:
        if page not in mem:
            faults += 1
            if len(mem) >= capacity:
                mem.pop(0)          # evict the oldest
            mem.append(page)
    return faults

def lru_faults(refs, capacity):
    mem = []          # end = most recently used
    faults = 0
    for page in refs:
        if page in mem:
            mem.remove(page)        # refresh recency
            mem.append(page)
        else:
            faults += 1
            if len(mem) >= capacity:
                mem.pop(0)          # evict least recently used (front)
            mem.append(page)
    return faults

print("reference string length:", len(refs), " frames:", frames)
print("FIFO faults:", fifo_faults(refs, frames))
print("LRU  faults:", lru_faults(refs, frames))
print("\\nLRU exploits locality (recent = likely-soon-again), usually winning.")
""",
        ),
        quiz_lesson(
            "Quiz: Scheduling, Concurrency & Memory",
            (
                q(
                    "Which scheduling algorithm gives the optimal average waiting time?",
                    (
                        opt("Shortest Job First (SJF)", correct=True),
                        opt("First-Come-First-Served (FCFS)"),
                        opt("Round-robin with a large quantum"),
                        opt("Random"),
                    ),
                    "Running shortest bursts first provably minimises average waiting time (but needs burst estimates).",
                ),
                q(
                    "What is a race condition?",
                    (
                        opt(
                            "A bug where the result depends on the timing/interleaving of concurrent accesses",
                            correct=True,
                        ),
                        opt("Two CPUs running at different speeds"),
                        opt("A process that runs too fast"),
                        opt("A deadlock between threads"),
                    ),
                    "Unsynchronised shared-data access yields timing-dependent, incorrect results.",
                ),
                q(
                    "Which is a reliable, practical way to prevent deadlock?",
                    (
                        opt(
                            "Always acquire multiple locks in the same global order (no circular wait)",
                            correct=True,
                        ),
                        opt("Use more threads"),
                        opt("Never release any lock"),
                        opt("Give every process maximum priority"),
                    ),
                    "Consistent lock ordering breaks the circular-wait Coffman condition.",
                ),
                q(
                    "What does the banker's algorithm check before granting resources?",
                    (
                        opt(
                            "That the system stays in a safe state — a sequence exists where all processes can finish",
                            correct=True,
                        ),
                        opt("That the process has the highest priority"),
                        opt("That memory is encrypted"),
                        opt("That no other process is running"),
                    ),
                    "It only grants a request if a safe completion sequence still exists, avoiding deadlock.",
                ),
                q(
                    "Why is the TLB important for paging performance?",
                    (
                        opt(
                            "It caches recent virtual→physical translations so most lookups skip the page table",
                            correct=True,
                        ),
                        opt("It stores files on disk"),
                        opt("It schedules processes"),
                        opt("It encrypts page tables"),
                    ),
                    "The TLB makes address translation fast by caching hot mappings.",
                ),
                q(
                    "Why does LRU usually beat FIFO for page replacement?",
                    (
                        opt(
                            "It exploits locality — recently used pages are likely to be used again soon",
                            correct=True,
                        ),
                        opt("It uses less memory"),
                        opt("It never has page faults"),
                        opt("It evicts random pages"),
                    ),
                    "LRU keeps recently-touched pages; FIFO can evict a hot page just because it loaded early.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# os-advanced
# ──────────────────────────────────────────────────────────────────────

_OS_ADVANCED = SeedCourse(
    slug="os-advanced",
    title="Operating Systems — Advanced",
    description=(
        "Deeper systems: demand paging and thrashing, disk/I-O scheduling, "
        "filesystem internals and journaling, classic synchronization problems, "
        "kernel architectures (monolithic/microkernel, VMs vs containers), and "
        "real-time/embedded OSes."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Demand paging, working sets & thrashing",
            "11 min",
            r"""# Demand paging, working sets & thrashing

**Demand paging** loads a page only when it's first touched, not up front — so a
program starts fast and uses RAM only for what it actually accesses.

The **working set** is the set of pages a process is using *right now* (within a
recent time window). If its working set fits in its allocated frames, it runs
smoothly with few faults. If it doesn't, every access risks evicting a page it's
about to need again.

That failure mode is **thrashing**: the system spends more time paging in/out
than computing. As you pack more processes in, CPU utilisation climbs — until
collective working sets exceed RAM, faults explode, and throughput **collapses**:

```plot
{"title": "Thrashing: utilisation collapses past a point", "xLabel": "degree of multiprogramming", "yLabel": "CPU utilisation", "xRange": [0, 12], "yRange": [0, 1.05], "functions": [{"expr": "if(x < 7, x/8, 1 - (x-7)*0.28)", "label": "CPU utilisation", "color": "#2563eb"}]}
```

Cures: the OS tracks each process's working set and only admits more processes
if their working sets fit (**working-set model**), or watches the global
**page-fault frequency** and suspends processes when it spikes. The practical
sysadmin signal: high disk I/O + low CPU = thrashing; add RAM or reduce load.
""",
        ),
        _t(
            "Disk & I/O scheduling",
            "9 min",
            r"""# Disk & I/O scheduling

On a spinning disk, **seek time** (moving the head) dominates, so the order you
service requests hugely affects throughput. Disk-scheduling algorithms reorder
the queue of cylinder requests:

- **FCFS** — service in arrival order. Fair, but the head zig-zags wildly.
- **SSTF (Shortest Seek Time First)** — nearest request next. Efficient but can
  **starve** far-away requests.
- **SCAN ("elevator")** — sweep the head in one direction servicing everything,
  then reverse. Like a lift: no starvation, smooth.
- **C-SCAN** — sweep one way, then jump back to the start (more uniform wait
  times than SCAN).

**SSDs change the calculus** — no moving head, so seek time ≈ 0 and ordering
matters far less; modern schedulers (or "none"/NVMe multi-queue) focus instead
on fairness, merging adjacent requests, and write amplification.

Either way the OS also **buffers and caches** aggressively: a **page cache**
holds recently read data in RAM, and writes are often **buffered** and flushed
in batches (which is why pulling power can lose un-flushed writes — and why
`fsync` and journaling exist). I/O is slow; the OS works hard to hide it behind
caching, reordering, and overlap with computation.
""",
        ),
        _t(
            "Filesystem internals & journaling",
            "10 min",
            r"""# Filesystem internals & journaling

How does a filesystem turn `/home/leo/report.txt` into bytes on a disk?

- **Inodes** — each file has an inode storing metadata (size, owner,
  permissions, timestamps) and **pointers to its data blocks**. Crucially, the
  inode has **no name**; a **directory** is just a table mapping names → inode
  numbers. That's why a single file can have multiple names (**hard links**) —
  they point to the same inode.
- **Data blocks** — the file's contents, in fixed-size blocks. Big files use
  indirect blocks (pointers to pointers) or **extents** (ranges) to scale.
- **Free-space management** — bitmaps/lists track which blocks are free.

**The crash problem:** creating a file touches several structures (inode, data
block, directory, free map). A crash between updates leaves the filesystem
**inconsistent** (e.g. a block marked used but unreferenced).

**Journaling** fixes this: write the intended changes to a **journal (log)**
first; only after they're safely logged are they applied to their real
locations. After a crash, the OS **replays** the journal — completed
transactions are finished, incomplete ones discarded — so the filesystem is
always consistent without a slow full scan (`fsck`). **Copy-on-write**
filesystems (ZFS, Btrfs) go further: never overwrite in place, so the old state
is always intact until the new one is committed — enabling cheap snapshots.
""",
        ),
        _t(
            "Classic synchronization problems",
            "10 min",
            r"""# Classic synchronization problems

Three textbook problems capture the hard parts of concurrency; recognising them
helps you spot the pattern in real systems.

**Producer–Consumer (bounded buffer).** Producers add items, consumers remove
them, sharing a fixed-size buffer. Needs coordination so producers block when
**full** and consumers block when **empty** — solved with two **semaphores**
(empty slots, full slots) plus a mutex. This is every work queue, pipeline, and
message broker.

**Readers–Writers.** Many threads read shared data; writers need exclusive
access. Maximise concurrent reads while keeping writes safe — and avoid starving
writers (or readers). This is the design behind read-write locks and database
concurrency.

**Dining Philosophers.** Five philosophers, five forks, each needs both
neighbours' forks to eat. The naive "grab left, then right" **deadlocks** if all
grab left at once. Classic fixes: impose a **global fork ordering** (break
circular wait), let only N-1 sit at once, or have one philosopher grab right
first. It's the canonical illustration of deadlock and the value of consistent
resource ordering.

The meta-lesson: concurrency bugs are about **coordination under
non-determinism**. Reach for proven patterns (bounded queues, RW locks) and
established primitives rather than improvising — and test under contention,
because these bugs hide until the worst possible moment.
""",
        ),
        _t(
            "Kernel architectures; VMs vs containers",
            "10 min",
            r"""# Kernel architectures; VMs vs containers

**How much lives in the kernel?**

- **Monolithic kernel** (Linux) — drivers, filesystems, networking all run in
  kernel space. Fast (no boundary crossings) but large; a driver bug can crash
  the system. Linux mitigates this with **loadable modules**.
- **Microkernel** (QNX, seL4) — only the bare minimum (scheduling, IPC, memory)
  in the kernel; drivers and filesystems run as **user-space services**. More
  robust and secure (a crashed driver doesn't take down the kernel) but pays for
  extra message-passing. Favoured in high-reliability/embedded systems.
- **Hybrid** (Windows NT, macOS XNU) — pragmatic blends.

**Isolating whole environments:**

- **Virtual machines** — a **hypervisor** runs multiple guest OSes, each with its
  own kernel, on virtual hardware. Strong isolation; heavyweight (full OS per VM).
- **Containers** (Docker) — processes sharing the **host kernel**, isolated by
  kernel features (**namespaces** for what they see, **cgroups** for how much
  they use). Near-native speed, seconds to start, tiny images — but weaker
  isolation than VMs since they share a kernel.

The rule of thumb: **containers** for packaging and scaling app workloads
(your DevOps courses); **VMs** when you need different/again-isolated kernels or
stronger security boundaries. Both rest on the same OS primitives this track
has covered.
""",
        ),
        _t(
            "Real-time & embedded operating systems",
            "9 min",
            r"""# Real-time & embedded operating systems

A general-purpose OS optimises **average** throughput and fairness. A
**real-time OS (RTOS)** optimises something different: **predictability** —
meeting **deadlines**, every time.

- **Hard real-time** — missing a deadline is a failure (an airbag controller, a
  motor control loop, a pacemaker). Timing is part of correctness.
- **Soft real-time** — occasional misses degrade quality but aren't catastrophic
  (video playback, audio).

What an RTOS does differently:

- **Deterministic scheduling** — typically fixed-priority **preemptive** with
  bounded latency; analysed with **Rate-Monotonic** or **Earliest-Deadline-First
  (EDF)** so you can *prove* deadlines are met.
- **Bounded everything** — predictable interrupt latency; avoid or bound
  features whose timing varies (paging, garbage collection, dynamic allocation).
- **Priority inheritance** — when a high-priority task waits on a lock held by a
  low-priority one, temporarily boost the holder to avoid **priority inversion**
  (the bug that froze the Mars Pathfinder).

Examples: FreeRTOS, Zephyr, QNX, VxWorks — running on microcontrollers and
safety-critical hardware. This ties straight back to the **Embedded** and
**Control** courses: firmware engineers live in RTOS land, where "fast on
average" loses to "always on time".
""",
        ),
        quiz_lesson(
            "Quiz: Advanced OS",
            (
                q(
                    "What is thrashing?",
                    (
                        opt(
                            "Spending more time paging in/out than computing, collapsing throughput",
                            correct=True,
                        ),
                        opt("Running too many threads on one core"),
                        opt("A deadlock between two processes"),
                        opt("Fragmentation of the disk"),
                    ),
                    "When working sets exceed RAM, page faults dominate and useful work plummets.",
                ),
                q(
                    "What problem does the SCAN ('elevator') disk algorithm solve vs SSTF?",
                    (
                        opt(
                            "It avoids starving far-away requests by sweeping in one direction",
                            correct=True,
                        ),
                        opt("It encrypts disk data"),
                        opt("It eliminates seek time entirely"),
                        opt("It only works on SSDs"),
                    ),
                    "SCAN services everything along a sweep, preventing the starvation SSTF can cause.",
                ),
                q(
                    "What does filesystem journaling guarantee?",
                    (
                        opt(
                            "Consistency after a crash by logging intended changes before applying them",
                            correct=True,
                        ),
                        opt("Faster reads via compression"),
                        opt("That files are encrypted"),
                        opt("Infinite storage"),
                    ),
                    "The journal is replayed on recovery, so interrupted operations leave a consistent FS.",
                ),
                q(
                    "In a Unix filesystem, where do filenames live?",
                    (
                        opt(
                            "In directories, which map names to inode numbers (inodes themselves have no name)",
                            correct=True,
                        ),
                        opt("Inside the inode"),
                        opt("In the data blocks"),
                        opt("In the page table"),
                    ),
                    "Inodes hold metadata + block pointers; directories map names→inodes, enabling hard links.",
                ),
                q(
                    "How do containers differ from virtual machines?",
                    (
                        opt(
                            "Containers share the host kernel (namespaces/cgroups); VMs run separate guest kernels via a hypervisor",
                            correct=True,
                        ),
                        opt("Containers are slower and larger than VMs"),
                        opt("VMs share the host kernel"),
                        opt("They are the same thing"),
                    ),
                    "Containers are lightweight kernel-shared isolation; VMs are heavier with full per-guest kernels.",
                ),
                q(
                    "What does a real-time OS prioritise over a general-purpose OS?",
                    (
                        opt("Predictability — meeting deadlines deterministically", correct=True),
                        opt("Maximum average throughput"),
                        opt("The largest possible page cache"),
                        opt("Running the most processes"),
                    ),
                    "An RTOS guarantees bounded latency and deadline adherence, not just good average performance.",
                ),
            ),
        ),
    ),
)


OS_COURSES = (_OS_BASICS, _OS_INTERMEDIATE, _OS_ADVANCED)
