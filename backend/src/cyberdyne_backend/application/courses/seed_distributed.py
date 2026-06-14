"""Academy seed content — the Distributed Systems track (Beginner → Advanced).

* ``distributed-basics``        — why distribute, partial failure, time & ordering, consensus intro
* ``distributed-intermediate``  — vector clocks, quorums, leader election, gossip
* ``distributed-advanced``      — Raft/Paxos, 2PC/saga, CRDTs, consistency in practice

Runnable ``code`` lessons use Python builtins + numpy only, so the labs simulate
Lamport and vector clocks, quorum reads/writes, Raft-style leader election,
epidemic gossip, two-phase commit, and a G-Counter CRDT by hand. Builds on the
System Design track (replication, CAP, quorums) and Networking.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ², ×, ‖) in diagrams and labels.
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
# distributed-basics
# ──────────────────────────────────────────────────────────────────────

_DIST_BASICS = SeedCourse(
    slug="distributed-basics",
    title="Distributed Systems — Basics",
    description=(
        "Why distributed systems are hard and how to reason about them: the "
        "fallacies, partial failure, why clocks can't be trusted, logical time "
        "and the happens-before relation, replication, and the consensus "
        "problem. With a runnable Lamport-clock simulation."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a distributed system?",
            "10 min",
            r"""# What is a distributed system?

A **distributed system** is a set of independent computers that, to a user, looks
like a single coherent system. They cooperate by passing **messages** over a
network because they share no memory and no clock. Almost everything at scale is
distributed: web backends, databases, file stores, blockchains, even your phone
talking to the cloud.

**Why distribute at all?**

- **Scale** — handle more load/data than one machine can.
- **Availability** — survive the failure of any single machine.
- **Latency** — put data and compute close to users (geo-distribution).
- **Some problems are inherently distributed** — multiple parties, multiple
  locations.

But distribution buys those benefits at the price of **enormous new difficulty**.
The reasons were captured as the **8 fallacies of distributed computing** —
false assumptions that wreck naïve designs:

1. The network is reliable.
2. Latency is zero.
3. Bandwidth is infinite.
4. The network is secure.
5. Topology doesn't change.
6. There is one administrator.
7. Transport cost is zero.
8. The network is homogeneous.

Every one of these is **false**, and every distributed bug can be traced to
trusting one of them. Messages get **lost, delayed, duplicated, or reordered**;
nodes **crash** or — worse — go slow; and parts of the system can't tell the
difference between "the other node is down" and "the network between us is
broken."

The mental shift for this whole track: **stop thinking of remote calls as
function calls.** A local call always returns; a remote call may never return,
may return late, or may have executed *without you ever hearing back*. Designing
for that uncertainty is what distributed systems is about.
""",
        ),
        _t(
            "Failure is the norm",
            "10 min",
            r"""# Failure is the norm

On one machine, failure is all-or-nothing: the program runs or it crashes. In a
distributed system you get the hardest case — **partial failure**: some
components work while others don't, and *you often can't tell which*.

**Why it's unavoidable at scale.** If a single server has 99% uptime, the chance
that **all** of N servers are simultaneously healthy is `0.99^N` — which collapses
as N grows. With hundreds of machines, **something is always broken**. You can't
engineer failure away; you must engineer *around* it.

```plot
{"title": "P(all N nodes healthy) collapses with cluster size (per-node 99%)", "xLabel": "number of nodes", "yLabel": "probability all healthy", "xRange": [1, 200], "yRange": [0, 1], "functions": [{"expr": "0.99^x", "label": "0.99^N", "color": "#dc2626"}]}
```

**The core difficulty: the timeout dilemma.** You send a request and hear
nothing. Is the other node *dead*, or just *slow*, or did your *request* arrive
and only the *reply* got lost? You cannot distinguish these. So you set a
**timeout** — but:

- Too short → you give up on healthy-but-slow nodes (and may retry an operation
  that already succeeded → duplicates).
- Too long → you hang, holding resources, while a truly-dead node wastes your
  time.

There's no perfect timeout; this ambiguity is fundamental.

**The Two Generals Problem** proves a humbling limit: two parties communicating
over an unreliable channel can **never be certain** they've reached agreement —
each acknowledgement itself needs acknowledging, forever. Perfect coordination
over a lossy network is *impossible*; we settle for *high probability* and clever
protocols.

The practical consequences shape everything ahead: design for **retries** (so
make operations **idempotent**), **redundancy** (so one failure isn't fatal),
**failure detection** (timeouts + heartbeats), and **graceful degradation** (do
something useful when a dependency is down). In distributed systems, **failure
isn't an exception path — it's the main path.**
""",
        ),
        _t(
            "Time & ordering: why clocks lie",
            "11 min",
            r"""# Time & ordering: why clocks lie

A single program has one clock and one obvious order of events. A distributed
system has **neither** — and this breaks intuitions hard.

**Physical clocks disagree.** Every machine has its own quartz clock, and they
**drift** apart (and get corrected by NTP in jumps). So two servers' wall-clock
readings can differ by **milliseconds to seconds**. That means you **cannot**
order events across machines by comparing timestamps — "event A has an earlier
timestamp than B" does **not** prove A happened first. Using wall-clock time to
decide "who wrote last" silently corrupts data.

**What we actually need is *ordering*, not time.** Often you don't care what time
it was — you care whether **A could have caused B**. Leslie Lamport's insight:
define a logical **happens-before** relation (written `→`):

- If A and B are in the **same process** and A comes first, then `A → B`.
- If A is a **send** and B is the matching **receive**, then `A → B`.
- It's **transitive**: if `A → B` and `B → C`, then `A → C`.

If neither `A → B` nor `B → A`, the events are **concurrent** (`A ‖ B`) — they
could have happened in either order and **neither could have influenced the
other**. Concurrency isn't a bug; it's the normal state of independent events.

**Logical clocks** capture this relation *without* synchronised time. A **Lamport
clock** is a simple integer counter per process:

1. Before each event, increment your counter.
2. When you **send** a message, attach your counter.
3. When you **receive**, set your counter to `max(local, received) + 1`.

This guarantees: if `A → B` then `timestamp(A) < timestamp(B)`. (The converse
isn't true — a smaller timestamp doesn't prove happens-before; vector clocks fix
that, next course.) You'll implement Lamport clocks next — the foundation for
reasoning about order in a world with no shared clock.
""",
        ),
        _code(
            "Lamport logical clocks",
            "13 min",
            r"""# Lamport clocks assign each event an integer so that if A happens-before B,
# then timestamp(A) < timestamp(B) — without any synchronised wall clock.
# Rule: increment on every event; on receive, clock = max(local, msg) + 1.

clock = {"P1": 0, "P2": 0, "P3": 0}
mailbox = {}     # message name -> Lamport timestamp stamped at send time

# A fixed schedule of events across three processes.
# (process, kind, message)   kind in {"local","send","recv"}
schedule = [
    ("P1", "local", None),
    ("P1", "send", "m1"),     # P1 sends m1 to P2
    ("P2", "local", None),
    ("P2", "recv", "m1"),     # P2 receives m1
    ("P2", "send", "m2"),     # P2 sends m2 to P3
    ("P3", "recv", "m2"),
    ("P3", "send", "m3"),     # P3 sends m3 back to P1
    ("P1", "recv", "m3"),
    ("P1", "local", None),
]

print("event-by-event Lamport timestamps:")
for proc, kind, msg in schedule:
    if kind == "local":
        clock[proc] = clock[proc] + 1
    elif kind == "send":
        clock[proc] = clock[proc] + 1
        mailbox[msg] = clock[proc]                       # piggyback the timestamp
    else:  # recv
        clock[proc] = max(clock[proc], mailbox[msg]) + 1
    label = msg if msg is not None else "-"
    print("  ", proc, kind, label, "  ->  clock(", proc, ") =", clock[proc])

print("final clocks:", clock)
# Notice the send of m1 has a smaller timestamp than its receive, and the chain
# m1 -> m2 -> m3 has strictly increasing timestamps: causality is preserved.
""",
        ),
        _t(
            "Replication & consistency models",
            "11 min",
            r"""# Replication & consistency models

To survive failure and serve reads at scale, distributed systems keep **multiple
copies** (replicas) of data. The hard question is the one from the System Design
track, now central: **how in-sync must the copies be?** That's the **consistency
model** — a contract about what a read can return.

From strongest (most intuitive, most expensive) to weakest (cheapest, most
available):

- **Linearizable (strong)** — the system behaves as if there's a **single copy**:
  every read sees the most recent write, and operations appear to take effect
  instantaneously in a single global order. Easiest to reason about; costs
  latency and availability (you may have to wait or refuse during partitions).
- **Sequential / causal** — weaker but useful: **causal** consistency guarantees
  that operations related by happens-before are seen in order by everyone (a
  reply never appears before the message it answers), while concurrent operations
  may be seen in different orders. Often the sweet spot.
- **Eventual** — replicas **converge** if writes stop, but a read may return
  **stale** data in the meantime. Cheapest and most available; fine for view
  counts, dangerous for bank balances.

The deep trade-off is the **CAP theorem** (System Design course): during a
network **partition** you must choose **consistency or availability**, never both.
Since partitions are unavoidable, real systems are **CP** (stay correct, may
reject requests) or **AP** (stay up, may serve stale data). And **PACELC** adds
the everyday tail: even with no partition, stronger consistency costs **latency**
(coordination round-trips).

The takeaway: **consistency is a dial, not a switch.** Strong consistency is a
convenience you *pay for* in latency and availability. A huge part of distributed
design is choosing the **weakest model your application can tolerate** — and the
logical-clock machinery you just learned is exactly how systems track causality
to offer models like causal consistency.
""",
        ),
        _t(
            "Communication: RPC & delivery semantics",
            "10 min",
            r"""# Communication: RPC & delivery semantics

Nodes cooperate by **passing messages**. The most common pattern is **RPC**
(Remote Procedure Call): make a remote service look like a local function —
`user = userService.get(id)`. Convenient, but the abstraction **leaks**, because
(as we saw) a remote call can fail in ways a local one never does.

**Delivery semantics** — the guarantee about how many times a message/operation is
processed — is the key design choice:

- **At-most-once** — send and don't retry. The operation runs **0 or 1** times.
  Never duplicates, but may be **lost**. Fine for "best-effort" data (a metric
  sample).
- **At-least-once** — retry until acknowledged. The operation runs **1 or more**
  times. Never lost, but may **duplicate** (you retried, but the first attempt had
  actually succeeded — you just didn't hear the ack). The common default.
- **Exactly-once** — runs **precisely once**. The ideal, but **impossible to
  guarantee** at the messaging layer in general. It's *approximated* by combining
  **at-least-once delivery** with **idempotent** processing or **deduplication**.

**Idempotency** is the workhorse that makes retries safe: an operation is
idempotent if doing it twice has the same effect as doing it once. `SET balance =
100` is idempotent; `ADD 50 to balance` is not. The standard trick is an
**idempotency key** (a unique request ID): the receiver records processed IDs and
ignores repeats. This is how payment APIs let you safely retry a charge.

Also know the shape of communication: **synchronous** (caller blocks for the
reply — simple, but couples availability and latency) vs **asynchronous** (fire a
message onto a queue/log and continue — decoupled and resilient, at the cost of
eventual consistency, as in the message-queue lesson). Picking semantics and
sync/async per interaction — and making handlers idempotent — is the daily craft
of building reliable distributed services.
""",
        ),
        _t(
            "The consensus problem",
            "10 min",
            r"""# The consensus problem

Again and again, distributed systems need a set of nodes to **agree on a single
value** despite failures and message loss: *who is the leader? what's the next
entry in the log? did this transaction commit?* This is **consensus**, and it is
*the* central problem of the field.

Formally, a consensus protocol must guarantee:

- **Agreement** — all non-faulty nodes decide the **same** value.
- **Validity** — the value decided was actually **proposed** by some node (no
  values invented from thin air).
- **Termination** — all non-faulty nodes **eventually decide** (it doesn't hang
  forever).

Sounds simple; it is brutally hard, because of a foundational result — the **FLP
impossibility theorem**: in a fully **asynchronous** system (no bound on message
delay) where even **one** node may crash, **no** consensus protocol can guarantee
*all three* properties. You can't have safety *and* guaranteed termination when
you can't tell a slow node from a dead one.

So real protocols make a pragmatic escape: they keep **safety always** (never
decide two different values) and achieve **termination "eventually," assuming
partial synchrony** (the network behaves *most* of the time) — typically using
**timeouts** to make progress and a **majority quorum** to stay correct.

The famous practical protocols:

- **Paxos** — the original, correct, and notoriously hard to understand.
- **Raft** — designed for **understandability**: a single elected **leader**
  replicates an append-only **log** to followers; a **majority** must acknowledge
  before an entry is committed. Now the default in real systems (etcd, Consul,
  CockroachDB…).

The reliance on a **majority (quorum)** is the thread tying this together: any two
majorities of N nodes **overlap**, so they can't independently decide conflicting
things — which is why a 5-node cluster survives 2 failures but a partition with
only 2 reachable nodes **can't elect a leader** (no majority). The next course
turns these ideas — quorums, leader election, vector clocks, gossip — into running
simulations.
""",
        ),
        quiz_lesson(
            "Quiz: Distributed Systems Basics",
            (
                q(
                    "Which is one of the 8 fallacies of distributed computing?",
                    (
                        opt("The network is reliable", correct=True),
                        opt("Computers have CPUs"),
                        opt("Code must be compiled"),
                        opt("Databases store data"),
                    ),
                    "The fallacies are false assumptions (network reliable, latency zero, bandwidth infinite…) that break naïve distributed designs.",
                ),
                q(
                    "Why is partial failure the defining difficulty of distributed systems?",
                    (
                        opt(
                            "Some components fail while others work, and you often can't tell which — a slow node looks like a dead one",
                            correct=True,
                        ),
                        opt("All nodes always fail together"),
                        opt("Failures never happen at scale"),
                        opt("Only the network can fail, never nodes"),
                    ),
                    "You can't distinguish 'dead' from 'slow' from 'reply lost', which is why timeouts are imperfect and retries must be safe.",
                ),
                q(
                    "Why can't you order events across machines using wall-clock timestamps?",
                    (
                        opt(
                            "Physical clocks drift and disagree, so an earlier timestamp doesn't prove an event happened first",
                            correct=True,
                        ),
                        opt("Timestamps are always identical"),
                        opt("Machines have no clocks at all"),
                        opt("Wall clocks are perfectly synchronised"),
                    ),
                    "Clock skew means timestamps are unreliable for ordering; logical clocks capture happens-before instead.",
                ),
                q(
                    "What does a Lamport clock guarantee?",
                    (
                        opt(
                            "If A happens-before B, then timestamp(A) < timestamp(B)", correct=True
                        ),
                        opt("If timestamp(A) < timestamp(B) then A definitely happened before B"),
                        opt("All events get the same timestamp"),
                        opt("It synchronises physical clocks"),
                    ),
                    "Lamport clocks preserve causality one way: happens-before implies smaller timestamp (the converse needs vector clocks).",
                ),
                q(
                    "What does 'at-least-once' delivery require of the receiver?",
                    (
                        opt(
                            "Idempotent processing, because messages may be delivered more than once",
                            correct=True,
                        ),
                        opt("Nothing — duplicates are impossible"),
                        opt("That messages are never retried"),
                        opt("That the network is reliable"),
                    ),
                    "At-least-once means retries cause duplicates; idempotent handlers (or dedup keys) make reprocessing safe.",
                ),
                q(
                    "What does the FLP impossibility result tell us about consensus?",
                    (
                        opt(
                            "In a fully asynchronous system with even one possible crash, no protocol can guarantee agreement, validity, and termination together",
                            correct=True,
                        ),
                        opt("Consensus is trivial and always terminates"),
                        opt("Consensus needs no quorum"),
                        opt("Physical clocks solve consensus"),
                    ),
                    "FLP forces real protocols to keep safety always and achieve termination only under partial synchrony (timeouts + majority quorums).",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# distributed-intermediate
# ──────────────────────────────────────────────────────────────────────

_DIST_INTERMEDIATE = SeedCourse(
    slug="distributed-intermediate",
    title="Distributed Systems — Intermediate",
    description=(
        "The working machinery: vector clocks that detect causality vs "
        "concurrency, quorum reads and writes, leader election by majority, and "
        "gossip/epidemic protocols — with runnable vector-clock, quorum, "
        "leader-election, and gossip simulations."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Vector clocks & causality",
            "10 min",
            r"""# Vector clocks & causality

Lamport clocks have a gap: `A → B` implies `ts(A) < ts(B)`, but the **converse
fails** — a smaller Lamport timestamp does **not** prove happens-before. So with
Lamport clocks alone you **can't tell** whether two events are causally related or
genuinely **concurrent**. Detecting concurrency matters enormously: concurrent
writes are exactly the **conflicts** a replicated system must reconcile.

**Vector clocks** fix this. Instead of one integer, each process keeps a **vector**
of counters — one entry per process — capturing "what I know about everyone's
progress":

1. Each process `i` keeps `V[i]`, initially all zeros.
2. Before an event, process `i` increments **its own** entry: `V[i][i] += 1`.
3. On **send**, attach the whole vector.
4. On **receive**, take the **element-wise max** of local and received vectors,
   then increment your own entry.

Now you can **compare** two vector timestamps `V(A)` and `V(B)` exactly:

- `V(A) ≤ V(B)` element-wise (and not equal) ⟹ **`A → B`** (A happened-before B).
- `V(B) ≤ V(A)` ⟹ **`B → A`**.
- **Neither** ≤ the other ⟹ **`A ‖ B`** — **concurrent** (a real conflict).

That last case is the payoff: vector clocks **detect concurrency**, which Lamport
clocks cannot. This is how Dynamo-style stores (and Git, conceptually) recognise
that two updates happened independently and need merging — surfacing **siblings**
to the application or auto-resolving with a CRDT (Advanced course).

The cost is **size**: a vector grows with the number of participating nodes, so
large or churning clusters use variants (dotted version vectors, bounded vectors).
But the idea is foundational — you'll implement vector clocks and a concurrency
test next.
""",
        ),
        _code(
            "Vector clocks: detecting concurrency",
            "14 min",
            r"""# Vector clocks let you tell causality from concurrency exactly. Each process
# keeps a vector; on receive, take element-wise max then bump your own entry.

order = ["P1", "P2", "P3"]
idx = {"P1": 0, "P2": 1, "P3": 2}
clock = {"P1": [0, 0, 0], "P2": [0, 0, 0], "P3": [0, 0, 0]}
mailbox = {}          # message -> vector stamped at send
snapshots = {}        # event label -> vector, so we can compare later

schedule = [
    ("P1", "local", None, "a"),
    ("P1", "send", "m1", "b"),     # b: P1 sends m1
    ("P2", "local", None, "c"),    # c: concurrent with b (independent)
    ("P2", "recv", "m1", "d"),     # d: P2 receives m1  (b -> d)
    ("P3", "local", None, "e"),    # e: concurrent with everything so far
]

for proc, kind, msg, label in schedule:
    if kind == "recv":
        incoming = mailbox[msg]
        merged = []
        for i in range(3):
            merged.append(max(clock[proc][i], incoming[i]))
        merged[idx[proc]] = merged[idx[proc]] + 1
        clock[proc] = merged
    else:
        clock[proc][idx[proc]] = clock[proc][idx[proc]] + 1
        if kind == "send":
            mailbox[msg] = list(clock[proc])
    snapshots[label] = list(clock[proc])
    print("event", label, "on", proc, "->", clock[proc])

def relate(a, b):
    le = True
    ge = True
    for i in range(len(a)):
        if a[i] > b[i]:
            le = False
        if a[i] < b[i]:
            ge = False
    if le and ge:
        return "equal"
    if le:
        return "a -> b (causal)"
    if ge:
        return "b -> a (causal)"
    return "a || b  (CONCURRENT)"

print()
print("b vs d:", relate(snapshots["b"], snapshots["d"]))   # send before its receive
print("b vs c:", relate(snapshots["b"], snapshots["c"]))   # independent -> concurrent
print("c vs e:", relate(snapshots["c"], snapshots["e"]))   # independent -> concurrent
""",
        ),
        _t(
            "Quorums: the overlap trick",
            "9 min",
            r"""# Quorums: the overlap trick

A **quorum** is the minimum number of nodes that must participate in an operation
for it to count. Quorums are how leaderless and replicated systems stay correct
**without** every node agreeing — and the magic is a single property: **any two
quorums overlap.**

With **N** replicas, a write goes to **W** of them and a read consults **R** of
them. If

$$ W + R > N $$

then the read set and the write set are **guaranteed to share at least one
replica** (pigeonhole) — so a read always sees at least one copy of the latest
write. Tag each value with a **version** and the reader picks the highest version
→ **strong reads**, no leader required.

Tuning W and R trades off the three things you care about:

- **Large W** (e.g. W = N) → durable, slow/fragile writes (every replica must be
  up).
- **Large R** → consistent but slow/fragile reads.
- **Small W and R with W + R ≤ N** → fast and highly available, but reads can be
  **stale** (the sets may not overlap).
- **W = R = ⌊N/2⌋ + 1** (majority) → the balanced sweet spot: strong, and
  tolerates ⌊N/2⌋ failures.

This is the same **majority** idea that powers leader election and Raft commits:
two majorities of N always intersect, so the system can never make two
conflicting decisions. Quorums also explain failure tolerance precisely — a write
quorum survives `N − W` down nodes; a read quorum survives `N − R`.

Real systems add wrinkles — **sloppy quorums** and **hinted handoff** (Dynamo)
keep accepting writes on substitute nodes during partitions, trading strict
overlap for availability and reconciling later. You'll simulate how W + R > N
makes reads fresh — and how W + R ≤ N lets them go stale — next.
""",
        ),
        _code(
            "Quorum reads & writes",
            "13 min",
            r"""# Why W + R > N guarantees fresh reads: any read quorum must overlap any write
# quorum. We test the WORST case — writer touches the first W replicas, reader
# the last R — so they overlap only when W + R > N.

def reader_sees(n, w, r):
    # All replicas start at version 0. A new write (version 1) lands on the
    # first W replicas (worst-case placement). The reader queries the LAST R
    # replicas and returns the highest version it finds.
    versions = []
    for i in range(n):
        versions.append(0)
    for i in range(w):           # write v1 to replicas 0 .. w-1
        versions[i] = 1
    best = 0
    for i in range(n - r, n):    # read replicas n-r .. n-1
        if versions[i] > best:
            best = versions[i]
    return best

n = 5
print("N =", n, " (latest write is version 1)")
print(" W  R  W+R   reader sees   verdict")
for w, r in [(1, 1), (2, 2), (3, 3), (2, 4), (1, 5), (5, 1)]:
    seen = reader_sees(n, w, r)
    overlap = w + r > n
    verdict = "FRESH" if seen == 1 else "STALE"
    print(" ", w, " ", r, "  ", w + r, "    version", seen, "   ", verdict, "(overlap)" if overlap else "(no overlap)")

print()
print("Reads are FRESH exactly when W + R > N — the quorums are forced to overlap.")
""",
        ),
        _t(
            "Leader election",
            "10 min",
            r"""# Leader election

Many designs are far simpler with a **single leader** that sequences all writes
(it sidesteps write conflicts and gives a natural place to order operations). But
the leader can crash — so the cluster must **elect a new one automatically**.
That's **leader election**, and getting it right is what prevents the nightmare of
**split brain** (two nodes both believing they're leader, corrupting data).

**The classic approaches:**

- **Bully algorithm** — when a node notices the leader is gone, it starts an
  election; the **highest-ID** reachable node wins. Simple, lots of messages.
- **Raft-style election** (the modern default) — time is divided into **terms**.
  A follower that hears no **heartbeat** from the leader becomes a **candidate**,
  increments the term, votes for itself, and asks others for votes. A node grants
  **one vote per term**. Win a **majority** → become leader and start sending
  heartbeats.

**Why a majority?** Because any two majorities **overlap**, at most one candidate
can collect a majority in a given term — so you can **never** have two leaders in
the same term. This is the same quorum overlap that makes reads consistent, reused
to make leadership unique.

**Handling ties.** Two candidates can split the vote so neither gets a majority;
the election **times out** and a new term begins. To stop this repeating forever,
Raft uses **randomised election timeouts** so one node almost always wakes first
and wins the next term.

**The crucial safety property:** a leader needs a **majority** to be elected, so a
node on the **minority** side of a network partition **cannot** become leader —
it'll keep trying and failing. This is why a 5-node cluster keeps working when 2
nodes are cut off (the 3-node side elects/keeps a leader) but **halts** if split
3–2 from the minority's view, or 2–2–1 with no majority anywhere. Availability is
deliberately sacrificed to **guarantee a single leader** (a CP choice). You'll
simulate majority-based election next.
""",
        ),
        _code(
            "Raft-style leader election",
            "12 min",
            r"""# A leader needs a MAJORITY of votes, which is why two majorities can't both
# form (they'd overlap) — no split brain. Here we tally votes under different
# partition scenarios. Pure builtins.

def run_election(nodes, reachable):
    # A candidate can collect a vote from each node it can reach (one vote each,
    # fresh term). It wins if it gathers a strict majority of the FULL cluster.
    majority = len(nodes) // 2 + 1
    votes = 0
    for node in nodes:
        if node in reachable:
            votes = votes + 1
    won = votes >= majority
    return votes, majority, won

nodes = ["n1", "n2", "n3", "n4", "n5"]

scenarios = [
    ("all reachable", ["n1", "n2", "n3", "n4", "n5"]),
    ("2 nodes partitioned away (3 reachable)", ["n1", "n2", "n3"]),
    ("only 2 reachable (minority)", ["n1", "n2"]),
    ("only the candidate reachable", ["n1"]),
]

print("cluster of", len(nodes), "nodes")
for name, reachable in scenarios:
    votes, majority, won = run_election(nodes, reachable)
    outcome = "LEADER elected" if won else "NO leader (quorum lost) -> retry next term"
    print(" ", name, ": got", votes, "of", majority, "needed ->", outcome)

print()
print("A minority partition can never reach a majority, so it cannot elect a")
print("leader -> no split brain. Availability is traded for single-leader safety.")
""",
        ),
        _t(
            "Gossip & anti-entropy",
            "10 min",
            r"""# Gossip & anti-entropy

How do you spread information — membership, config, updates — across thousands of
nodes **without** a central coordinator (a single point of failure and a
bottleneck)? You copy nature: **gossip** (a.k.a. **epidemic**) protocols. Each
node periodically picks a few **random peers** and exchanges state, exactly like a
rumour — or a virus — spreading through a crowd.

**Why it's beautiful:**

- **Fast.** Because every newly-infected node *also* starts spreading, the number
  of informed nodes **roughly doubles each round**, so a rumour reaches all N
  nodes in about **log₂(N)** rounds — ~17 rounds for 100,000 nodes.

```plot
{"title": "Gossip: informed nodes double each round (cluster of 100)", "xLabel": "round", "yLabel": "nodes informed", "xRange": [0, 8], "yRange": [0, 110], "functions": [{"expr": "min(2^x, 100)", "label": "min(2^round, N)", "color": "#16a34a"}]}
```

- **Robust.** No coordinator, no fixed structure; nodes can join, leave, or die
  and the protocol just keeps flowing around the gaps. There's massive redundancy
  (you hear things multiple ways).
- **Scalable & decentralised.** Each node talks to only a few peers per round, so
  per-node load stays constant as the cluster grows.

The cost is **eventual** consistency (it takes a few rounds to converge) and some
**redundant** messages (you'll be told things you already know).

**Anti-entropy** is the reconciliation side of the same coin: peers periodically
compare their data and exchange whatever's missing to **repair divergence** —
often using **Merkle trees** to find the differences cheaply (compare root
hashes, descend only where they differ — the same content-addressing idea from
Git). Dynamo/Cassandra use anti-entropy repair to heal replicas after failures.

Gossip powers real systems: **failure detection** and membership (Cassandra,
Consul's **SWIM**), config/secret propagation, and CRDT dissemination. It's the
go-to when you need **decentralised, failure-tolerant, eventually-consistent**
information spread. You'll simulate the log-N spread next.
""",
        ),
        _code(
            "Epidemic gossip spread",
            "11 min",
            r"""# Gossip spreads a rumour like an infection: each informed node tells others,
# so the informed set roughly DOUBLES per round -> ~log2(N) rounds to reach all.

n_nodes = 100
informed = 1            # patient zero
rounds = 0
history = [informed]

# Each round, every informed node successfully informs (about) one new node,
# so the informed count doubles until everyone knows.
while informed < n_nodes:
    informed = min(n_nodes, informed * 2)
    rounds = rounds + 1
    history.append(informed)

print("nodes in cluster:", n_nodes)
print("informed after each round:", history)
print("rounds to full dissemination:", rounds)

# Compare with log2(N): the theoretical lower bound on rounds.
import numpy as np
print("log2(N) =", round(float(np.log2(n_nodes)), 2), "-> gossip matches the ~log N bound")
print("Doubling each round is why gossip scales to huge clusters in a few rounds.")
""",
        ),
        quiz_lesson(
            "Quiz: Clocks, Quorums & Gossip",
            (
                q(
                    "What can vector clocks detect that Lamport clocks cannot?",
                    (
                        opt(
                            "Whether two events are concurrent (causally independent) vs causally ordered",
                            correct=True,
                        ),
                        opt("The exact wall-clock time"),
                        opt("The CPU temperature"),
                        opt("Which node has the most memory"),
                    ),
                    "Comparing vector timestamps reveals concurrency (neither ≤ the other) — the conflicts a replicated system must reconcile.",
                ),
                q(
                    "Why does W + R > N guarantee a read sees the latest write?",
                    (
                        opt(
                            "The read quorum and write quorum are forced to overlap in at least one replica",
                            correct=True,
                        ),
                        opt("It makes writes faster"),
                        opt("It encrypts the data"),
                        opt("It removes the need for versions"),
                    ),
                    "Overlapping quorums (pigeonhole) mean the reader always queries at least one replica holding the newest version.",
                ),
                q(
                    "Why must a leader be elected by a majority?",
                    (
                        opt(
                            "Two majorities always overlap, so at most one candidate can win a term — preventing split brain",
                            correct=True,
                        ),
                        opt("Majorities are faster to count"),
                        opt("It uses less memory"),
                        opt("Minorities are always offline"),
                    ),
                    "Majority overlap guarantees a unique leader per term; a minority partition can't elect one, avoiding two leaders.",
                ),
                q(
                    "Roughly how many rounds does gossip need to reach all N nodes?",
                    (
                        opt(
                            "About log₂(N), because the informed set doubles each round",
                            correct=True,
                        ),
                        opt("About N rounds"),
                        opt("Exactly 1 round"),
                        opt("About N² rounds"),
                    ),
                    "Each informed node also spreads, so informed count doubles per round → ~log₂(N) rounds; ~17 for 100k nodes.",
                ),
                q(
                    "What is anti-entropy in a gossip-based system?",
                    (
                        opt(
                            "Periodically comparing replicas and exchanging missing data to repair divergence (often via Merkle trees)",
                            correct=True,
                        ),
                        opt("Encrypting all messages"),
                        opt("Electing a leader"),
                        opt("Deleting old data"),
                    ),
                    "Anti-entropy reconciles replicas after failures; Merkle trees let peers find the differences cheaply.",
                ),
                q(
                    "What is the main cost of gossip protocols?",
                    (
                        opt(
                            "Eventual (not immediate) consistency and some redundant messages",
                            correct=True,
                        ),
                        opt("They need a central coordinator"),
                        opt("They cannot tolerate node failure"),
                        opt("Per-node load grows linearly with cluster size"),
                    ),
                    "Gossip is decentralised and robust but converges over several rounds and re-delivers known info; per-node load stays constant.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# distributed-advanced
# ──────────────────────────────────────────────────────────────────────

_DIST_ADVANCED = SeedCourse(
    slug="distributed-advanced",
    title="Distributed Systems — Advanced",
    description=(
        "Consensus and conflict resolution in depth: Raft log replication, "
        "Paxos, distributed transactions (2PC and sagas), CRDTs for "
        "conflict-free replication, real-world consistency (Spanner, Dynamo), "
        "and failure handling — with runnable 2PC and G-Counter CRDT labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Raft: consensus you can understand",
            "12 min",
            r"""# Raft: consensus you can understand

**Raft** is the consensus algorithm most systems reach for today, designed
explicitly to be *understandable* (unlike Paxos). It keeps a cluster's
**replicated log** identical across nodes so they behave like one reliable
machine. It decomposes consensus into three parts:

**1. Leader election** (last course). Time is split into **terms**; a node that
misses heartbeats becomes a candidate and needs a **majority** to win. At most one
leader per term.

**2. Log replication.** All client writes go to the **leader**, which appends the
command to its log and sends it to followers (**AppendEntries**). Once a
**majority** have stored the entry, the leader marks it **committed**, applies it
to its state machine, and tells followers to do the same. So every committed entry
lives on a majority — and since majorities overlap, a newly elected leader is
guaranteed to **already have** every committed entry.

**3. Safety.** Raft adds rules so the log can never diverge:

- **Election restriction** — a candidate can only win if its log is **at least as
  up-to-date** as the voter's, so a node missing committed entries can't become
  leader.
- **Log matching** — if two logs agree at some index/term, they agree on
  **everything before** it; followers reject AppendEntries that don't line up,
  and the leader **backfills** them into agreement.

The result is **linearizable** writes that tolerate up to ⌊N/2⌋ failures
(N = 5 survives 2). The price is that every commit needs a **majority round-trip**
(latency) and the cluster **halts** rather than split-brain when it can't reach a
majority — the deliberate **CP** trade-off. Raft underpins **etcd** (Kubernetes'
brain), **Consul**, **CockroachDB**, **TiKV**, and more — when you need a
strongly-consistent, fault-tolerant source of truth, this is the workhorse.
""",
        ),
        _t(
            "Paxos & the consensus landscape",
            "9 min",
            r"""# Paxos & the consensus landscape

**Paxos** (Leslie Lamport, 1998) was the first proven-correct consensus
algorithm, and for two decades it *was* distributed consensus. It's famous for two
opposite reasons: it's foundational, and it's **notoriously hard to understand**
and to implement correctly.

The essence (single-decree Paxos) is a two-phase protocol among **proposers**,
**acceptors**, and **learners**, using **ballot numbers** and **majority quorums**:

1. **Prepare** — a proposer picks a ballot number `n` and asks a majority of
   acceptors to **promise** not to accept anything older than `n` (and to report
   any value they've already accepted).
2. **Accept** — if a majority promise, the proposer asks them to **accept** value
   `v` at ballot `n` — but if any acceptor already had a value, the proposer
   **must reuse that value**. This subtle rule is what preserves **safety**: once
   a value could have been chosen, every later ballot proposes the same value.

Majority overlap again does the heavy lifting: any two majorities share an
acceptor, so two different values can't both be chosen.

**The landscape:**

- **Multi-Paxos** — run Paxos repeatedly for a *log* of values with a stable
  leader (so you skip Phase 1 most of the time). Essentially what Raft also
  achieves, more legibly.
- **Raft** — same guarantees, optimised for understandability; the modern default.
- **ZAB** — ZooKeeper's protocol, similar in spirit.
- **Byzantine fault tolerance (PBFT, Tendermint)** — a *harder* model where nodes
  may be **malicious/lying**, not just crashed. Needs **3f + 1** nodes to tolerate
  *f* traitors and powers blockchains; crash-tolerant Paxos/Raft only need
  **2f + 1**.

You rarely implement these yourself — you use etcd/ZooKeeper/Consul. The value is
recognising **when you need consensus** (leader election, config, metadata,
locks) versus when **weaker, cheaper** coordination (quorums, CRDTs, gossip) will
do — usually the smartest architectural move is to need consensus **as rarely as
possible**.
""",
        ),
        _t(
            "Distributed transactions: 2PC & sagas",
            "10 min",
            r"""# Distributed transactions: 2PC & sagas

A local database gives you **ACID** transactions for free. Across multiple
services or shards, atomicity ("all of these updates happen, or none do") becomes
a hard distributed problem.

**Two-Phase Commit (2PC)** is the classic answer, coordinated by a
**transaction coordinator**:

- **Phase 1 — Prepare.** The coordinator asks every participant: *can you commit?*
  Each does the work tentatively, locks resources, and replies **yes** (vote to
  commit) or **no**.
- **Phase 2 — Commit/Abort.** If **all** voted yes, the coordinator tells everyone
  to **commit**; if **any** said no (or timed out), everyone **aborts**.

It gives atomicity, but it's **blocking and fragile**: participants hold **locks**
between the phases, and if the **coordinator crashes** after participants voted
yes, they're stuck **uncertain** — holding locks, unable to decide — until it
recovers. That latency and unavailability make 2PC a poor fit for high-scale
microservices.

**Sagas** are the scalable alternative. Model a long business transaction as a
**sequence of local transactions**, each in its own service, each with a
**compensating action** that semantically undoes it:

```
Order saga:  create order → reserve stock → charge card → ship
Compensate:  cancel order ← release stock ← refund card ← (n/a)
```

If a step fails, run the **compensations** for the completed steps in reverse.
No global locks, no coordinator holding everyone hostage — but the trade-offs are
real: only **eventual** atomicity, **no isolation** (intermediate states are
visible — an order briefly exists before payment), and **you** must design correct
compensations. Sagas are usually **event/queue-driven** (orchestrated by a central
workflow, or choreographed via events).

The pragmatic guidance from the System Design track holds: **avoid distributed
transactions when you can** — keep data that changes together on one
service/shard, lean on **idempotency** so retries are safe, and when you truly
need a cross-service workflow, prefer a **saga** over 2PC. You'll simulate the 2PC
all-or-nothing decision next.
""",
        ),
        _code(
            "Two-phase commit",
            "12 min",
            r"""# Two-phase commit: the coordinator commits ONLY if every participant votes
# yes in the prepare phase; a single 'no' (or a timeout treated as no) aborts
# the whole transaction. Pure builtins.

def coordinator_decision(votes):
    # Phase 1 already happened; 'votes' are the prepare-phase replies.
    # Phase 2: commit iff the vote was unanimous 'yes'.
    decision = "COMMIT"
    for v in votes:
        if v != "yes":
            decision = "ABORT"
    return decision

scenarios = [
    ("all participants ready", ["yes", "yes", "yes"]),
    ("one cannot commit", ["yes", "no", "yes"]),
    ("a participant times out (treated as no)", ["yes", "yes", "timeout"]),
    ("all but one ready", ["yes", "yes", "yes", "no"]),
]

print("two-phase commit decisions:")
for name, votes in scenarios:
    decision = coordinator_decision(votes)
    print(" ", name)
    print("      prepare votes:", votes, "-> coordinator:", decision)

print()
print("Atomicity = all-or-nothing: any single 'no' aborts the whole transaction.")
print("Risk: between phases participants hold locks; a coordinator crash leaves")
print("them blocked and uncertain — which is why high-scale systems prefer sagas.")
""",
        ),
        _t(
            "CRDTs: conflict-free replication",
            "11 min",
            r"""# CRDTs: conflict-free replication

Consensus (Raft/Paxos) gives strong consistency but costs a **coordination
round-trip** on every write and **halts** during partitions. For many features —
collaborative editing, shopping carts, counters, presence — that's too strict. We
want **AP**: every replica accepts writes locally (instant, always available) and
they **merge automatically** later, with **no conflicts and no coordination**.

**CRDTs (Conflict-free Replicated Data Types)** make this provably safe. A CRDT's
**merge** function is mathematically a **join semilattice** — it is:

- **Commutative** — `merge(a, b) = merge(b, a)` (order of merging doesn't matter).
- **Associative** — grouping doesn't matter.
- **Idempotent** — `merge(a, a) = a` (re-receiving the same state is harmless).

Because of these three properties, replicas that exchange state via **gossip**
(in any order, with duplicates and re-deliveries) are **guaranteed to converge**
to the **same** value — **strong eventual consistency**, with zero coordination.

**Two flavours:** **state-based (CvRDT)** ship the whole merged state; **op-based
(CmRDT)** ship operations (which must be commutative). Common CRDTs:

- **G-Counter** — grow-only counter: a vector of per-replica counts; merge =
  element-wise max; value = sum. (PN-Counter adds a second vector for decrements.)
- **G-Set / OR-Set** — sets with add (and, for OR-Set, remove via unique tags so
  concurrent add/remove resolve deterministically).
- **LWW-Register** — last-writer-wins by timestamp.
- **Sequence CRDTs** (RGA, Logoot) — power real-time collaborative text editors.

The trade-off: CRDTs guarantee **convergence**, but the *merge policy* may not
match business intent (e.g. LWW silently drops a concurrent update; a counter
can't enforce "never below zero"). They shine for **high availability, offline-
first, and collaboration** (used in Redis, Riak, Automerge, Figma-style editors).
You'll build a G-Counter and watch it converge regardless of merge order next.
""",
        ),
        _code(
            "A G-Counter CRDT",
            "13 min",
            r"""# A G-Counter: each replica counts its OWN increments in its slot of a vector.
# merge = element-wise max; value = sum. Because merge is commutative,
# associative, and idempotent, replicas converge no matter the gossip order.

def value(vec):
    total = 0
    for x in vec:
        total = total + x
    return total

def merge(a, b):
    out = []
    for i in range(len(a)):
        out.append(max(a[i], b[i]))
    return out

# Three replicas (slots A=0, B=1, C=2) take increments independently, offline.
ra = [3, 0, 0]      # A incremented 3 times
rb = [0, 2, 0]      # B incremented 2 times
rc = [0, 0, 5]      # C incremented 5 times
print("replica states ->  A:", ra, " B:", rb, " C:", rc)

# Gossip happens in arbitrary orders; every order must reach the same state.
order1 = merge(merge(ra, rb), rc)
order2 = merge(rc, merge(rb, ra))
order3 = merge(merge(rb, rc), ra)
print("merge order 1:", order1, " value =", value(order1))
print("merge order 2:", order2, " value =", value(order2))
print("merge order 3:", order3, " value =", value(order3))

# Idempotent: re-merging an already-seen state changes nothing.
again = merge(order1, rc)
print("re-merging C again (idempotent):", again, " value =", value(again))

converged = order1 == order2 and order2 == order3 and order1 == again
print("all orders converged to the same state:", converged, "-> total count =", value(order1))
""",
        ),
        _t(
            "Consistency in the real world",
            "10 min",
            r"""# Consistency in the real world

Theory meets engineering in how famous systems pick their spot on the
consistency/availability spectrum. A few landmark designs tie this track together:

- **Google Spanner — strong consistency, globally.** Spanner offers
  **externally consistent** (linearizable) transactions across continents. Its
  trick is **TrueTime**: GPS and atomic clocks give every datacentre a clock with
  a *bounded uncertainty* `ε`. To commit, Spanner **waits out the uncertainty**
  (a few ms) so timestamp order matches real order. It essentially **buys tighter
  clocks** to make global strong consistency practical — a **CP** system that
  pays latency for correctness.

- **Amazon Dynamo — availability first.** Dynamo (and Cassandra, Riak) chose
  **AP**: always accept writes, use **leaderless quorums** (tunable N/W/R),
  **vector clocks** to detect concurrent versions, **gossip** for membership, and
  **anti-entropy/Merkle** repair. Conflicts surface as **siblings** for the app
  (or a CRDT) to resolve. Built for "the shopping cart must *always* accept an
  add," even during failures.

- **Calvin / deterministic databases** — agree on a **global order of
  transactions first**, then execute deterministically, avoiding distributed
  locks.

Two principles worth carrying:

- **CALM theorem** — a program can be **consistent without coordination** *if and
  only if* it is **monotonic** (it only ever *adds* knowledge, never retracts).
  This is the theoretical "why" behind CRDTs and gossip: monotonic logic
  (grow-only sets/counters) needs no consensus; non-monotonic logic (uniqueness
  constraints, "is this the last seat?") does.
- **Coordination is the cost.** Strong consistency = coordination = latency +
  reduced availability. So the master skill is **needing coordination as rarely
  as possible**: push work to monotonic/CRDT-friendly designs, reserve
  consensus for the few things that truly require one global truth (leadership,
  uniqueness, money).

There's no universally "correct" consistency — only the **right trade-off for each
piece** of your system, made with eyes open.
""",
        ),
        _t(
            "Failure handling & resilience patterns",
            "10 min",
            r"""# Failure handling & resilience patterns

Knowing failure is the norm, mature distributed systems bake in **patterns** that
turn inevitable faults into non-events. The toolkit:

- **Failure detection** — **heartbeats** and **timeouts** to suspect dead nodes;
  **phi-accrual** detectors output a *suspicion level* instead of a binary
  up/down, adapting to network conditions. Remember: detection is **suspicion**,
  never certainty (you can't tell dead from slow).

- **Retries with backoff + jitter** — retry transient failures, but **exponential
  backoff** (wait 1s, 2s, 4s…) avoids hammering a struggling service, and **random
  jitter** prevents the **thundering herd** where all clients retry in lockstep
  and synchronise into repeating spikes. Pair retries with **idempotency** so they
  don't double-apply.

- **Circuit breakers** — after too many failures to a dependency, **trip** the
  breaker and fail fast (don't pile requests onto a dying service); periodically
  send a trial request and **close** the breaker when it recovers. Prevents
  **cascading failure**, where one slow service exhausts everyone's threads/
  connections and takes the whole system down.

- **Bulkheads** — isolate resources (separate thread/connection pools per
  dependency) so one overloaded component can't sink the rest — like watertight
  compartments in a ship.

- **Timeouts everywhere & load shedding** — never wait forever; under overload,
  **shed** or **degrade** (serve cached/partial results) rather than collapse.

- **Idempotency & dedup** — the safety net under *all* retry-based patterns.

- **Observability** — distributed **tracing** (follow one request across
  services), **metrics**, and structured **logs**, because in a distributed system
  you can't attach a debugger to "the program." You can only operate what you can
  **see**.

The throughline of the whole track: you **cannot prevent** partial failure, lost
messages, or clock skew — so you **design for** them. Replicate for redundancy,
use **quorums/consensus** where you need one truth, **CRDTs/gossip** where you can
stay coordination-free, make everything **idempotent**, detect failures with
timeouts, and contain blast radius with breakers and bulkheads. That mindset —
**embrace failure, engineer around it** — is what separates systems that survive
the real world from those that don't.
""",
        ),
        quiz_lesson(
            "Quiz: Consensus, Transactions & CRDTs",
            (
                q(
                    "In Raft, when is a log entry considered committed?",
                    (
                        opt(
                            "Once a majority of nodes have stored it — guaranteeing a new leader already has it",
                            correct=True,
                        ),
                        opt("As soon as the leader writes it locally"),
                        opt("After every single node acknowledges it"),
                        opt("When a timeout expires"),
                    ),
                    "Majority storage + overlap means any future leader holds all committed entries; the cluster tolerates ⌊N/2⌋ failures.",
                ),
                q(
                    "Why is Two-Phase Commit considered fragile?",
                    (
                        opt(
                            "Participants hold locks between phases, and a coordinator crash can leave them blocked and uncertain",
                            correct=True,
                        ),
                        opt("It never achieves atomicity"),
                        opt("It requires no coordinator"),
                        opt("It cannot abort transactions"),
                    ),
                    "2PC blocks while holding locks; coordinator failure after 'yes' votes strands participants — hence sagas at high scale.",
                ),
                q(
                    "What three properties must a CRDT's merge function have to guarantee convergence?",
                    (
                        opt("Commutative, associative, and idempotent", correct=True),
                        opt("Fast, small, and encrypted"),
                        opt("Ordered, timed, and locked"),
                        opt("Linear, sorted, and unique"),
                    ),
                    "Those three make merge a join semilattice, so replicas converge regardless of message order or duplication — no coordination needed.",
                ),
                q(
                    "How does Google Spanner provide global strong consistency?",
                    (
                        opt(
                            "TrueTime gives clocks bounded uncertainty, and commits wait out that uncertainty so timestamp order matches real order",
                            correct=True,
                        ),
                        opt("It uses a single server worldwide"),
                        opt("It abandons consistency entirely"),
                        opt("It never replicates data"),
                    ),
                    "Spanner buys tight clocks (GPS/atomic) and waits the uncertainty window ε to make externally-consistent global transactions practical.",
                ),
                q(
                    "What does the CALM theorem state?",
                    (
                        opt(
                            "A program can be consistent without coordination if and only if it is monotonic (only adds knowledge)",
                            correct=True,
                        ),
                        opt("All programs need consensus"),
                        opt("Coordination is always free"),
                        opt("Monotonic programs are impossible"),
                    ),
                    "Monotonic logic (grow-only sets/counters) needs no coordination; non-monotonic logic (uniqueness, 'last seat') does — the basis for CRDTs/gossip.",
                ),
                q(
                    "Why add random jitter to exponential backoff on retries?",
                    (
                        opt(
                            "To prevent a thundering herd where all clients retry in lockstep and create synchronised spikes",
                            correct=True,
                        ),
                        opt("To make retries slower for no reason"),
                        opt("To encrypt the retries"),
                        opt("To guarantee exactly-once delivery"),
                    ),
                    "Jitter spreads retries out so clients don't synchronise and repeatedly overwhelm a recovering service.",
                ),
            ),
        ),
    ),
)


DISTRIBUTED_COURSES = (_DIST_BASICS, _DIST_INTERMEDIATE, _DIST_ADVANCED)
