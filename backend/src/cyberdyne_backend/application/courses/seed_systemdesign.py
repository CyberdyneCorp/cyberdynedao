"""Academy seed content — the System Design track (Beginner → Advanced).

* ``system-design-basics``        — requirements, estimation, latency, scaling, LB, caching
* ``system-design-intermediate``  — eviction, sharding, consistent hashing, replication, CAP, queues, rate limiting
* ``system-design-advanced``      — scale playbook, DB scaling, consistency/transactions, quorum, bloom filters, SLOs, a case study

Runnable ``code`` lessons use Python builtins + numpy only (the sandbox blocks
hashlib/random/re/etc.), so the hashing labs hand-roll an FNV-1a hash, and the
LRU/rate-limiter/quorum labs are pure arithmetic. Builds directly on the
Networking track (load balancing, CDNs, anycast).
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ², ×) in diagrams and labels.
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
# system-design-basics
# ──────────────────────────────────────────────────────────────────────

_SD_BASICS = SeedCourse(
    slug="system-design-basics",
    title="System Design — Basics",
    description=(
        "How to design systems that scale: turning fuzzy requirements into "
        "concrete numbers, the latency figures every engineer should know, "
        "vertical vs horizontal scaling, load balancing, and caching. With a "
        "runnable capacity estimator and load-balancer simulation."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is system design?",
            "9 min",
            r"""# What is system design?

**System design** is deciding how the pieces of a software system — servers,
databases, caches, queues, networks — fit together to meet a goal **at scale**,
**reliably**, and **within budget**. Coding solves "does it work?"; system design
solves "does it still work with a million users, when a server dies, on a
budget?"

Every design starts by pinning down two kinds of requirements:

- **Functional** — *what* the system does. "Users can post a photo." "A short
  URL redirects to the original." These become your API.
- **Non-functional** — *how well* it must do it. **Scale** (how many users/QPS?),
  **latency** (how fast?), **availability** (how much downtime is acceptable?),
  **consistency** (must everyone see the same data instantly?), **durability**
  (can we ever lose data?), and **cost**.

The non-functional requirements drive every interesting decision. "100 users"
and "100 million users" are completely different systems even if the feature
list is identical.

Two ideas to internalise up front:

- **There are no right answers, only trade-offs.** Faster usually costs more;
  stronger consistency usually costs latency or availability. Your job is to make
  the trade-offs *deliberately* and justify them against the requirements.
- **Design top-down, then drill in.** Sketch the boxes (client → load balancer →
  app servers → cache → database), agree on the API and data model, *then*
  zoom into the hard parts (the database that won't fit on one machine, the
  endpoint that's 100× hotter than the rest).

The rest of this track gives you the building blocks and the numbers to reason
about them.
""",
        ),
        _t(
            "Back-of-the-envelope estimation",
            "11 min",
            r"""# Back-of-the-envelope estimation

Good design decisions rest on **rough numbers**, computed in your head in
seconds. You don't need precision — you need the **order of magnitude**: is this
1 server or 1,000? Megabytes or petabytes?

**Powers of two & ten** (memorise these):

```
2^10 ≈ 10^3   = thousand  (KB)
2^20 ≈ 10^6   = million   (MB)
2^30 ≈ 10^9   = billion   (GB)
2^40 ≈ 10^12  = trillion  (TB)
```

**Time:** there are **86,400 seconds/day** ≈ **~10^5**. So a handy shortcut:
*requests/day ÷ 100,000 ≈ requests/second (QPS)*. 1 million/day ≈ ~12 QPS;
1 billion/day ≈ ~12,000 QPS.

**The estimation recipe:**

1. **Users → QPS.** daily-active-users × actions/user ÷ 86,400 = average QPS.
   Multiply by a **peak factor** (≈2–5×) for the busy hour.
2. **Read/write ratio.** Most systems are read-heavy (often 100:1). Size reads
   and writes separately — they hit different components.
3. **Storage.** writes/day × bytes/write × retention (days/years). Don't forget
   replication (×3 is common) and indexes/overhead.
4. **Bandwidth.** QPS × payload size.

The point isn't the exact figure — it's catching the **infeasible** early. "That's
50 TB/day, so one disk won't do — we must shard" is the kind of conclusion a
30-second estimate gives you, before you've drawn a single box wrong. You'll run
the numbers in code next.
""",
        ),
        _code(
            "A capacity estimator",
            "12 min",
            r"""# Turn requirements into numbers: QPS, storage, and bandwidth for a
# photo-sharing service. Change the inputs and re-run. Pure arithmetic.

dau = 100_000_000          # daily active users
posts_per_user = 2         # writes per user per day
read_write_ratio = 100     # reads are 100x writes (read-heavy)
avg_post_bytes = 300_000   # 300 KB per photo
peak_factor = 3            # busy-hour multiplier
replication = 3            # copies kept for durability
seconds_per_day = 86_400

writes_per_day = dau * posts_per_user
write_qps = writes_per_day / seconds_per_day
read_qps = write_qps * read_write_ratio

print("writes/day:   ", writes_per_day)
print("avg write QPS:", round(write_qps))
print("peak write QPS:", round(write_qps * peak_factor))
print("avg read QPS: ", round(read_qps))
print("peak read QPS:", round(read_qps * peak_factor))

storage_per_day = writes_per_day * avg_post_bytes * replication
storage_5yr = storage_per_day * 365 * 5

print("storage/day:  ", round(storage_per_day / 1e12, 2), "TB (with 3x replication)")
print("storage/5yr:  ", round(storage_5yr / 1e15, 2), "PB")

read_bandwidth = read_qps * avg_post_bytes
print("read bandwidth:", round(read_bandwidth / 1e9, 1), "GB/s (avg)")
# Conclusion: petabytes of storage + GB/s egress => you MUST shard storage and
# put a CDN in front. The estimate told you that before any code was written.
""",
        ),
        _t(
            "Latency, throughput & tail latency",
            "11 min",
            r"""# Latency, throughput & tail latency

Three words people confuse:

- **Latency** — time for *one* request (e.g. 20 ms).
- **Throughput** — requests served *per second* (QPS). They're related but not
  the same — batching can raise throughput while *hurting* latency.
- **Tail latency** — the *slow* requests. You care about **p99** (the 99th
  percentile), not the average, because at scale the tail dominates user
  experience: if one page makes 100 backend calls, it's as slow as the *slowest*
  of those 100 — so a "rare" p99 hits almost every page.

**Latency numbers every engineer should know** (orders of magnitude):

```
L1 cache reference            ~1 ns
Main memory (RAM) reference   ~100 ns
SSD random read               ~16 µs
Read 1 MB sequentially (RAM)  ~3 µs
Read 1 MB from SSD            ~50 µs
Round trip within a datacenter ~0.5 ms
Disk (HDD) seek               ~10 ms
Round trip across continents  ~150 ms
```

The lesson: **memory is ~100,000× faster than a cross-continent round trip.**
This single fact justifies caching, CDNs, and keeping hot data in RAM.

**Latency rises sharply as a server fills up.** Queueing theory: as utilisation ρ
(arrival rate ÷ service rate) approaches 1, waiting time blows up like
`1 / (1 − ρ)` — a server at 90% load has ~10× the response time of one at 0%,
even though it's "only" 90% busy. This is why you **never run servers near 100%**
and why adding a little headroom dramatically improves tail latency.

```plot
{"title": "Response time explodes as utilisation approaches 100%", "xLabel": "utilisation ρ", "yLabel": "relative response time", "xRange": [0, 0.95], "yRange": [0, 20], "functions": [{"expr": "1 / (1 - x)", "label": "1 / (1 − ρ)", "color": "#dc2626"}]}
```

Design implication: to improve the experience you usually attack **p99 and
utilisation**, not the average — shed load, add headroom, cache, and parallelise.
""",
        ),
        _t(
            "Scaling: vertical vs horizontal",
            "10 min",
            r"""# Scaling: vertical vs horizontal

When one server isn't enough, you have two moves:

- **Vertical scaling (scale up)** — a *bigger* machine: more CPU, RAM, faster
  disk. Simple — no code changes — but it hits a **ceiling** (the biggest box
  money can buy), gets expensive non-linearly, and is a **single point of
  failure**.
- **Horizontal scaling (scale out)** — *more* machines behind a load balancer.
  Effectively unlimited and fault-tolerant (one dies, others carry on) — but it
  forces hard questions: how do requests find a server, and where does **state**
  live?

The key enabler of horizontal scaling is **statelessness**. If each app server
keeps no per-user state in local memory (sessions, uploaded files), then *any*
server can handle *any* request, and you can add/remove servers freely. So you
push state **out** to shared stores:

- **Sessions / cache** → Redis or a distributed cache.
- **Files** → object storage (S3) or a CDN.
- **Data** → the database tier (itself scaled separately).

This **stateless app tier + shared state tier** split is the backbone of almost
every scalable web system.

**Amdahl's law** tempers the optimism: if a fraction *p* of work is
parallelisable, the best speedup on *n* machines is `1 / ((1−p) + p/n)`. Even at
*p* = 0.95, you cap out at 20× no matter how many machines — the **serial part
dominates** at scale. So horizontal scaling isn't free magic; you must minimise
coordination and shared bottlenecks (locks, a single hot database row).

```plot
{"title": "Amdahl's law: the serial part caps speedup (p = 0.95)", "xLabel": "number of machines", "yLabel": "speedup", "xRange": [1, 64], "yRange": [0, 24], "functions": [{"expr": "1 / (0.05 + 0.95 / x)", "label": "1 / ((1−p) + p/n)", "color": "#2563eb"}]}
```

Rule of thumb: **scale up first** (simplest), **scale out when you must** — and
design stateless from day one so scaling out is an option.
""",
        ),
        _t(
            "Load balancing",
            "10 min",
            r"""# Load balancing

A **load balancer (LB)** sits in front of your app servers and spreads incoming
requests across them. It's what makes horizontal scaling usable: clients hit one
address, the LB picks a healthy backend. (You met LBs in the Networking track —
here's the design view.)

**What it buys you:**

- **Scalability** — add servers behind the LB transparently.
- **Availability** — **health checks** route around dead/slow backends.
- **Flexibility** — rolling deploys, A/B routing, draining a node for
  maintenance.

**Where it operates:**

- **Layer 4** (transport) — balances by IP/port, blind to content. Fast, cheap.
- **Layer 7** (application) — reads HTTP, so it can route by **path/host/header**
  (`/api` → API servers, `/img` → image servers), terminate TLS, and do
  sticky sessions. More work, more power.

**How it chooses a backend:**

- **Round-robin** — next server in rotation. Simple; ignores load.
- **Least-connections** — the server with the fewest active requests. Better when
  requests vary in cost.
- **Weighted** — bigger servers get more traffic.
- **Hashing** (by client IP or key) — the *same* client/key always lands on the
  *same* server — essential for cache locality and sticky sessions (and the seed
  of **consistent hashing**, next course).

The LB itself must not become the single point of failure — production setups run
**redundant LBs** (active/passive or via DNS/anycast, as you saw with CDNs). You'll
simulate the routing strategies next.
""",
        ),
        _code(
            "Load-balancer strategies",
            "12 min",
            r"""# Simulate two classic load-balancing strategies over the same request
# stream and watch how they distribute work. Pure builtins.

servers = ["s1", "s2", "s3"]

# 1) Round-robin: hand each request to the next server in rotation.
print("Round-robin:")
cursor = 0
for req in range(6):
    chosen = servers[cursor % len(servers)]
    cursor = cursor + 1
    print("  request", req, "->", chosen)

# 2) Least-connections: send each request to the server holding the fewest
#    active connections. 'cost' is how many in-flight units each request adds.
print("Least-connections (requests have different costs):")
active = {}
for s in servers:
    active[s] = 0
costs = [3, 1, 1, 2, 1, 3]      # request 0 is heavy, etc.
for req in range(6):
    best = servers[0]
    for s in servers:
        if active[s] < active[best]:
            best = s
    active[best] = active[best] + costs[req]
    print("  request", req, "(cost", costs[req], ") ->", best, " load now", dict(active))

print("final load:", dict(active))
# Round-robin ignores cost, so a run of heavy requests can pile onto one server;
# least-connections adapts to real load. Try changing 'costs'.
""",
        ),
        _t(
            "Caching",
            "11 min",
            r"""# Caching

A **cache** is a small, fast store of *frequently used* data placed in front of a
slow source (a database, a disk, a remote service). Because memory is ~100,000×
faster than a cross-continent round trip, a cache hit can turn a 150 ms request
into a sub-millisecond one — and it offloads the database so it survives traffic
spikes. Caching is the single highest-leverage performance tool in system design.

**Where caches live** (often several at once):

- **Client / browser** — avoid the request entirely.
- **CDN** — cache static content at the edge, near users (Networking track).
- **Application cache** — Redis/Memcached holding hot query results, sessions.
- **Database cache** — the DB's own buffer pool.

**Read patterns:**

- **Cache-aside (lazy)** — app checks cache; on a **miss**, reads the DB and
  populates the cache. Most common; only caches what's actually requested.
- **Read-through** — the cache itself fetches from the DB on a miss (app only
  talks to the cache).

**Write patterns:**

- **Write-through** — write cache *and* DB together: consistent, slightly slower
  writes.
- **Write-back** — write cache now, DB later (async): fast, but risks data loss
  on crash.

**The hard parts** — caching's famous trade-off is **staleness vs freshness**:

- **TTL (expiry)** — entries auto-expire; bounds staleness.
- **Invalidation** — on a write, evict/update the cached copy. *"There are only
  two hard things in CS: cache invalidation and naming things."*
- **Eviction** — the cache is finite; when full, which entry goes? **LRU** (least
  recently used) is the default; **LFU** and **FIFO** are alternatives. (You'll
  build an LRU cache in the next course.)

A good cache strategy can cut load by 90%+; a bad one serves stale data or
stampedes the DB when many keys expire at once. Cache **hot, read-heavy,
tolerant-of-slight-staleness** data first.
""",
        ),
        quiz_lesson(
            "Quiz: System Design Basics",
            (
                q(
                    "Why do non-functional requirements (scale, latency, availability) drive system design?",
                    (
                        opt(
                            "They determine the interesting trade-offs; the same feature at 100 vs 100M users is a different system",
                            correct=True,
                        ),
                        opt("They are optional and rarely matter"),
                        opt("They only affect the UI"),
                        opt("They are the same as functional requirements"),
                    ),
                    "Functional requirements define what; non-functional (scale/latency/availability/consistency/cost) define how well — and dictate the architecture.",
                ),
                q(
                    "Roughly how do you convert requests/day to average QPS?",
                    (
                        opt("Divide by ~100,000 (there are ~86,400 seconds per day)", correct=True),
                        opt("Multiply by 86,400"),
                        opt("Divide by 60"),
                        opt("Multiply by 1000"),
                    ),
                    "~86,400 s/day ≈ 10^5, so requests/day ÷ 100,000 ≈ QPS. 1M/day ≈ 12 QPS.",
                ),
                q(
                    "Why does tail latency (p99) matter more than the average?",
                    (
                        opt(
                            "At scale a request fans out to many backends and is as slow as the slowest, so the 'rare' tail hits most requests",
                            correct=True,
                        ),
                        opt("The average is impossible to measure"),
                        opt("p99 is always equal to the average"),
                        opt("Tail latency only affects writes"),
                    ),
                    "If one page makes 100 calls, its latency is the max of 100 — so a 1% tail shows up on nearly every page.",
                ),
                q(
                    "What makes horizontal scaling possible?",
                    (
                        opt(
                            "Stateless app servers, with shared state pushed to caches/object-storage/databases",
                            correct=True,
                        ),
                        opt("Keeping all session state in each server's local memory"),
                        opt("Using a single bigger machine"),
                        opt("Disabling the load balancer"),
                    ),
                    "If servers hold no local state, any server can serve any request, so you can add/remove them freely.",
                ),
                q(
                    "According to Amdahl's law, why doesn't adding machines scale forever?",
                    (
                        opt(
                            "The serial (non-parallelisable) fraction caps the maximum speedup",
                            correct=True,
                        ),
                        opt("Machines get slower in parallel"),
                        opt("Networks have infinite bandwidth"),
                        opt("Caches stop working past 10 servers"),
                    ),
                    "Speedup = 1/((1−p) + p/n); even p=0.95 caps at 20× — the serial part dominates at scale.",
                ),
                q(
                    "In a cache-aside (lazy) read pattern, what happens on a cache miss?",
                    (
                        opt(
                            "The app reads the database, then populates the cache for next time",
                            correct=True,
                        ),
                        opt("The request fails"),
                        opt("The cache is wiped"),
                        opt("The database is bypassed permanently"),
                    ),
                    "Cache-aside: check cache → on miss read DB and backfill the cache; only requested data is cached.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# system-design-intermediate
# ──────────────────────────────────────────────────────────────────────

_SD_INTERMEDIATE = SeedCourse(
    slug="system-design-intermediate",
    title="System Design — Intermediate",
    description=(
        "Distributing data and load: cache eviction (LRU), partitioning and "
        "consistent hashing, replication and the strong-vs-eventual consistency "
        "choice, the CAP theorem, message queues, and rate limiting — with "
        "runnable LRU-cache, consistent-hashing, and token-bucket labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Cache eviction policies",
            "9 min",
            r"""# Cache eviction policies

A cache is finite, so when it fills up, adding an entry means **evicting** one.
Which one you drop is the **eviction policy**, and it decides your **hit rate** —
the single number that determines whether the cache is helping.

- **LRU (Least Recently Used)** — evict whatever hasn't been touched for the
  longest time. Bets that *recently used = soon used again* (temporal locality).
  The sensible default for most workloads.
- **LFU (Least Frequently Used)** — evict the entry with the fewest accesses.
  Better when popularity is stable, but slow to forget once-hot items.
- **FIFO (First In, First Out)** — evict the oldest inserted, ignoring use. Simple
  but usually worse than LRU (it'll evict a hot entry just because it's old).
- **Random** — evict any entry. Surprisingly competitive and trivially cheap;
  used when tracking order is too expensive.

**Implementing LRU efficiently** needs O(1) lookup *and* O(1) recency update. The
classic trick is a **hash map + doubly-linked list**: the map gives O(1) lookup;
the list orders entries by recency, and on each access you move the node to the
front. Eviction pops the tail. (Many languages provide this directly — Python's
`OrderedDict`, Java's `LinkedHashMap`.)

Beware **cache stampede**: if many popular keys expire at the same instant, all
the misses hammer the database at once. Mitigations: **jittered TTLs**, serving
slightly-stale data while one request refreshes, or a lock so only one caller
recomputes. You'll build an LRU cache by hand next.
""",
        ),
        _code(
            "Build an LRU cache",
            "13 min",
            r"""# An LRU cache: O(1) get/put with a fixed capacity that evicts the
# least-recently-used key when full. Here a dict holds values and a list
# tracks recency (most-recent at the end). Pure builtins.

capacity = 3
cache = {}        # key -> value
recency = []      # keys, least-recent first

def lru_get(cache, recency, key):
    if key in cache:
        recency.remove(key)
        recency.append(key)          # touch: move to most-recent
        return cache[key]
    return None

def lru_put(cache, recency, capacity, key, value):
    evicted = None
    if key in cache:
        recency.remove(key)
    elif len(cache) >= capacity:
        evicted = recency[0]          # least-recently used
        recency.remove(evicted)
        cache.pop(evicted)
    cache[key] = value
    recency.append(key)
    return evicted                    # the caller reports it (no print inside)

# Drive it through a sequence of operations.
ops = [
    ("put", "a", 1), ("put", "b", 2), ("put", "c", 3),
    ("get", "a", None),                 # 'a' becomes most-recent
    ("put", "d", 4),                    # cache full -> evict LRU (b)
    ("get", "b", None),                 # miss: b was evicted
    ("get", "c", None),
]
for kind, key, value in ops:
    if kind == "put":
        evicted = lru_put(cache, recency, capacity, key, value)
        if evicted is not None:
            print("put", key, "=", value, " (evicted", evicted, ") | order:", recency)
        else:
            print("put", key, "=", value, " | order:", recency)
    else:
        got = lru_get(cache, recency, key)
        print("get", key, "->", got, " | order:", recency)
""",
        ),
        _t(
            "Partitioning & sharding",
            "10 min",
            r"""# Partitioning & sharding

When data outgrows one machine (the petabytes your estimator predicted), you
**partition** (a.k.a. **shard**) it: split the dataset across many nodes, each
holding a slice. Done well, capacity and throughput scale *horizontally* with the
number of shards.

**How to choose the shard for a row** — by a **shard key**:

- **Range partitioning** — by key ranges (A–F on shard 1, G–M on shard 2…).
  Great for range scans ("all orders in March"), but prone to **hot spots** if
  traffic clusters (everyone's writing today's date → one shard melts).
- **Hash partitioning** — `shard = hash(key) % N`. Spreads load **evenly** and
  avoids hot spots, but kills range scans (adjacent keys scatter everywhere).
- **Directory / lookup** — a service maps key → shard explicitly. Flexible
  (you can move individual keys) at the cost of a lookup hop and a thing to keep
  available.

**Pick the shard key carefully** — it's the most consequential decision. A bad
key creates **hot shards** (a celebrity user, a single popular product) that
bottleneck the whole system regardless of how many shards you have.

The naive `hash(key) % N` has a fatal flaw: **change N (add/remove a node) and
almost every key remaps**, triggering a massive data reshuffle and cache
invalidation storm. The fix — **consistent hashing** — is next, and you'll build
it.

Sharding also complicates things you took for granted: **joins** across shards
are expensive, **transactions** spanning shards are hard, and **re-sharding** a
live system is a major operation. So shard only when you must, and choose the key
to keep related data together and load spread apart.
""",
        ),
        _code(
            "Consistent hashing",
            "14 min",
            r"""# Consistent hashing places nodes and keys on a hash 'ring'; each key goes
# to the next node clockwise. Adding/removing a node remaps only a small slice
# of keys, not (almost) all of them. We hand-roll an FNV-1a hash (no hashlib).

def fnv1a(text, seed):
    # 32-bit FNV-1a: deterministic, well-spread hash from a string.
    h = (2166136261 ^ seed) & 0xFFFFFFFF
    for ch in text:
        h = (h ^ ord(ch)) & 0xFFFFFFFF
        h = (h * 16777619) & 0xFFFFFFFF
    return h

keys = [
    "user1", "user2", "photo.jpg", "session-xyz", "cart42", "order99", "img-7",
    "doc-3", "invoice-2024", "avatar.png", "video-clip", "profile", "token-abc",
    "blob-xyz", "cache-key-7", "report.pdf", "thumbnail", "feed-item-3",
    "msg-4471", "upload-99",
]
vnodes = 80    # virtual nodes per server, for an even spread around the ring

# Build the ring for nodes A, B, C. Each node gets 'vnodes' points on the ring.
ring = []
for node in ["A", "B", "C"]:
    for v in range(vnodes):
        ring.append((fnv1a(node + "#" + str(v), 0), node))
ring.sort()

# Assign each key to the first node clockwise from its hash.
placement = {}
counts = {}
for pos, node in ring:
    counts[node] = 0
for key in keys:
    h = fnv1a(key, 0)
    chosen = ring[0][1]            # wrap-around default
    for pos, node in ring:
        if h <= pos:
            chosen = node
            break
    placement[key] = chosen
    counts[chosen] = counts[chosen] + 1
print("with nodes A,B,C ->", counts)

# Add node D and rebuild: only keys that now fall to D should move.
ring2 = []
for node in ["A", "B", "C", "D"]:
    for v in range(vnodes):
        ring2.append((fnv1a(node + "#" + str(v), 0), node))
ring2.sort()

placement2 = {}
counts2 = {}
for pos, node in ring2:
    counts2[node] = 0
for key in keys:
    h = fnv1a(key, 0)
    chosen = ring2[0][1]
    for pos, node in ring2:
        if h <= pos:
            chosen = node
            break
    placement2[key] = chosen
    counts2[chosen] = counts2[chosen] + 1
print("after adding D   ->", counts2)

moved = 0
for key in keys:
    if placement[key] != placement2[key]:
        moved = moved + 1
print("keys that moved when adding D:", moved, "of", len(keys))
print("(naive hash % N would have moved almost all of them)")
""",
        ),
        _t(
            "Replication & consistency",
            "11 min",
            r"""# Replication & consistency

**Replication** keeps copies of data on multiple nodes. It buys **durability**
(lose a node, keep the data), **availability** (serve from a surviving replica),
and **read scalability** (spread reads across copies). It's how systems survive
hardware failure — and it introduces the central headache of distributed data:
**keeping the copies in agreement**.

**Topologies:**

- **Leader–follower (primary–replica)** — all writes go to one **leader**, which
  streams changes to **followers** that serve reads. Simple and common.
- **Multi-leader** — several nodes accept writes (e.g. one per region). Lower
  write latency, but **write conflicts** must be resolved.
- **Leaderless (quorum)** — clients write to several replicas directly (Dynamo
  style). Robust, with quorum rules to stay consistent (Advanced course).

**Sync vs async replication** is the key knob:

- **Synchronous** — the leader waits for follower(s) to confirm before
  acknowledging the write. **No data loss** on leader failure, but **slower** and
  stalls if a follower is down.
- **Asynchronous** — leader acks immediately, replicates in the background.
  **Fast**, but a leader crash can **lose** the last unreplicated writes, and
  followers serve slightly **stale** reads (**replication lag**).

This gives the **strong vs eventual consistency** choice:

- **Strong** — every read sees the latest write. Intuitive, but costs latency
  and availability (you may have to wait or refuse during partitions).
- **Eventual** — replicas converge *eventually*; reads may be briefly stale. Far
  more available and scalable — fine for likes/feeds, dangerous for bank
  balances.

Choosing per-feature ("strong for payments, eventual for view counts") is normal.
**The CAP theorem** (next) formalises *why* you can't simply have it all.
""",
        ),
        _t(
            "The CAP theorem",
            "9 min",
            r"""# The CAP theorem

The **CAP theorem** is the most quoted (and most misquoted) result in distributed
systems. Three properties:

- **C — Consistency** — every read sees the most recent write (one up-to-date view
  of the data).
- **A — Availability** — every request gets a (non-error) response, even if some
  nodes are down.
- **P — Partition tolerance** — the system keeps working when the network **drops
  messages between nodes** (a *partition*).

The theorem: **during a network partition, you can have C or A, but not both.**
The nodes can't talk, so either you **refuse/stall** requests to avoid serving
stale data (choose **C**, sacrifice **A**) or you **answer anyway** from each side
and reconcile later (choose **A**, sacrifice **C**).

The crucial nuance: **partitions are not optional.** On a real network they
*will* happen, so **P is mandatory** — which means the real choice is **CP vs
AP**:

- **CP** (e.g. a strongly-consistent store, ZooKeeper, etcd) — stays consistent,
  may reject requests during a partition. Pick when correctness is non-negotiable
  (locks, leader election, money).
- **AP** (e.g. Cassandra, DynamoDB default) — stays available, may serve stale
  data during a partition, converging afterward. Pick when uptime beats
  perfect freshness (feeds, carts, telemetry).

**When there's no partition** (the normal case) you get both C and A — CAP only
forces the trade *during* a partition. The richer model **PACELC** adds the
everyday tail: *else* (no partition), you still trade **latency vs consistency**.
That "L vs C" is the daily reality — strong consistency costs round-trips even
when the network is healthy.
""",
        ),
        _t(
            "Message queues & async processing",
            "10 min",
            r"""# Message queues & async processing

Not everything should happen *during* the request. Sending email, encoding video,
generating thumbnails, updating search indexes — make the user wait for those and
your latency and reliability both suffer. The fix is **asynchronous processing**
via a **message queue**.

A **producer** drops a **message** ("resize photo 123") onto a **queue/broker**
(RabbitMQ, SQS, Kafka); **consumers** (workers) pull and process them on their own
schedule. The request returns immediately; the slow work happens in the
background.

**What queues give you:**

- **Decoupling** — producers and consumers don't know about each other; you can
  change/scale either side independently.
- **Load levelling (buffering)** — a traffic spike fills the queue instead of
  crashing the workers; they drain it at a steady rate. **Backpressure** prevents
  overload.
- **Resilience** — if a worker dies mid-job, the message is redelivered (it isn't
  lost).
- **Elastic scaling** — queue getting long? Add more consumers.

**Two messaging shapes:**

- **Work queue** — each message processed by **one** consumer (task distribution).
- **Pub/Sub** — each message broadcast to **many** subscribers (event fan-out).
  Logs like **Kafka** retain an ordered, replayable event stream — the backbone
  of event-driven architectures.

**The catch — delivery semantics.** Most systems are **at-least-once**: a message
may be delivered **more than once** (e.g. a worker processes it but crashes before
acking). So consumers must be **idempotent** — processing the same message twice
has the same effect as once (use a dedup key / "have I already handled this ID?").
Exactly-once is hard and often faked with idempotency. Designing for *replays and
duplicates* is the price of going async.
""",
        ),
        _code(
            "A token-bucket rate limiter",
            "12 min",
            r"""# Rate limiting protects a service from overload and abuse. The token-bucket
# algorithm refills tokens at a steady rate up to a capacity; each request
# spends a token, and is denied when the bucket is empty. Pure arithmetic.

capacity = 5.0          # bucket holds at most 5 tokens (burst size)
refill_rate = 2.0       # tokens added per second (steady allowed rate)

tokens = capacity       # start full
last_t = 0.0

# Simulated request arrival times (seconds). A burst at the start, then a gap.
arrivals = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 2.5, 2.6, 5.0]

allowed = 0
denied = 0
for t in arrivals:
    # Refill for the time elapsed since the last request (capped at capacity).
    elapsed = t - last_t
    tokens = min(capacity, tokens + elapsed * refill_rate)
    last_t = t
    if tokens >= 1.0:
        tokens = tokens - 1.0
        allowed = allowed + 1
        print("t=", t, "s  ALLOW  (tokens left", round(tokens, 2), ")")
    else:
        denied = denied + 1
        print("t=", t, "s  DENY   (tokens left", round(tokens, 2), ")")

print("allowed:", allowed, " denied:", denied)
# The initial burst drains the bucket (allowed up to capacity), then requests
# are throttled to ~refill_rate until tokens build back up during the idle gap.
""",
        ),
        quiz_lesson(
            "Quiz: Distributing Data & Load",
            (
                q(
                    "What does the LRU eviction policy do when the cache is full?",
                    (
                        opt(
                            "Evicts the entry that hasn't been accessed for the longest time",
                            correct=True,
                        ),
                        opt("Evicts the most recently used entry"),
                        opt("Evicts the most frequently used entry"),
                        opt("Never evicts anything"),
                    ),
                    "LRU bets on temporal locality: recently used data is likely to be used again, so it drops the least-recently-used entry.",
                ),
                q(
                    "Why is consistent hashing preferred over hash(key) % N for sharding?",
                    (
                        opt(
                            "Adding/removing a node remaps only a small slice of keys, not nearly all of them",
                            correct=True,
                        ),
                        opt("It is faster to compute"),
                        opt("It guarantees strong consistency"),
                        opt("It removes the need for replication"),
                    ),
                    "With modulo, changing N reshuffles almost every key; consistent hashing moves only the keys near the changed node.",
                ),
                q(
                    "What is the trade-off between synchronous and asynchronous replication?",
                    (
                        opt(
                            "Sync avoids data loss but is slower; async is fast but can lose recent writes and serve stale reads",
                            correct=True,
                        ),
                        opt("They are identical"),
                        opt("Async never loses data"),
                        opt("Sync is always faster"),
                    ),
                    "Sync waits for replicas (durable, slow); async acks immediately (fast) but risks loss on leader failure and replication lag.",
                ),
                q(
                    "What does the CAP theorem force you to choose during a network partition?",
                    (
                        opt(
                            "Consistency or Availability — you can't keep both while nodes can't communicate (P is mandatory)",
                            correct=True,
                        ),
                        opt("Speed or cost"),
                        opt("CPU or memory"),
                        opt("Read or write, but never both"),
                    ),
                    "Partitions are unavoidable, so the real choice is CP (stay consistent, may reject) vs AP (stay available, may be stale).",
                ),
                q(
                    "Why must consumers of an at-least-once message queue be idempotent?",
                    (
                        opt(
                            "Messages can be delivered more than once, so processing a duplicate must have the same effect as processing it once",
                            correct=True,
                        ),
                        opt("Because messages are encrypted"),
                        opt("Because queues guarantee exactly-once delivery"),
                        opt("To make processing slower"),
                    ),
                    "At-least-once delivery means duplicates happen (e.g. crash before ack); idempotent handlers make replays safe.",
                ),
                q(
                    "In a token-bucket rate limiter, what does the bucket capacity control?",
                    (
                        opt(
                            "The maximum burst size — how many requests can be allowed back-to-back before throttling",
                            correct=True,
                        ),
                        opt("The total number of requests ever allowed"),
                        opt("The network bandwidth"),
                        opt("The number of servers"),
                    ),
                    "Capacity is the burst allowance; the refill rate sets the sustained rate once the initial tokens are spent.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# system-design-advanced
# ──────────────────────────────────────────────────────────────────────

_SD_ADVANCED = SeedCourse(
    slug="system-design-advanced",
    title="System Design — Advanced",
    description=(
        "Designing real systems end to end: the scaling playbook, database "
        "scaling and CQRS, consistency models and distributed transactions, "
        "quorum reads/writes, Bloom filters, SLOs and the math of reliability, "
        "and a full case study — with runnable quorum and Bloom-filter labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The scaling playbook",
            "11 min",
            r"""# The scaling playbook

Most large web systems converge on the **same layered shape**. Knowing it lets
you start any design from a sensible default and then justify deviations.

```
Clients
   │
[ DNS / Anycast ]          → send users to the nearest region
   │
[ CDN ]                    → serve static & cacheable content at the edge
   │
[ Load Balancer ]          → spread requests across app servers (health-checked)
   │
[ Stateless App Servers ]  → scale horizontally; hold no local state
   │            │
[ Cache ]   [ Message Queue ] → hot data in RAM; slow work done async by workers
   │
[ Database tier ]          → replicated + sharded; read replicas for reads
   │
[ Object storage ]         → files/blobs (S3), often fronted by the CDN
```

**The order you reach for these as load grows:**

1. **One server** → split the app and database onto separate machines.
2. **Add a cache** → kill repeated reads; biggest win for least effort.
3. **Add read replicas** → scale reads; route writes to the leader.
4. **Add a CDN** → offload static/edge content, cut latency globally.
5. **Add a load balancer + more app servers** → scale the stateless tier.
6. **Shard the database** → when one DB can't hold the data or write load.
7. **Add queues + workers** → push slow/spiky work off the request path.

**Cross-cutting concerns** apply at every layer: **monitoring/metrics**,
**redundancy** (no single point of failure — N+1 everything), **graceful
degradation** (shed non-essential features under load rather than fall over), and
**autoscaling**. The art is applying each step *only when the numbers demand it* —
premature sharding or microservices add complexity you'll pay for daily.
""",
        ),
        _t(
            "Database scaling & CQRS",
            "10 min",
            r"""# Database scaling & CQRS

The database is usually the **first hard bottleneck** — it's stateful, so you
can't just add stateless copies. The escalation ladder:

1. **Indexing & query tuning** — the cheapest win. A missing index turns a fast
   lookup into a full-table scan. Fix the queries before changing the
   architecture.
2. **Connection pooling & caching** — reuse connections; put a cache in front to
   absorb reads.
3. **Read replicas** — replicate the data; send **reads** to replicas, **writes**
   to the leader. Scales read-heavy workloads (most of them). Watch for
   **replication lag** — a read right after a write may be stale ("read-your-own-
   writes" needs care).
4. **Vertical partitioning** — split *tables/columns* across databases by domain
   (users DB, orders DB). Often pairs with breaking a monolith into services.
5. **Horizontal sharding** — split *rows* across nodes by shard key (last
   course). The big gun; complicates joins and transactions.

**SQL vs NoSQL** in one breath: **SQL** gives you joins, **ACID** transactions,
and strong consistency — pick it when relationships and correctness matter (most
apps). **NoSQL** (document/key-value/wide-column) trades those for **horizontal
scale**, flexible schemas, and high write throughput — pick it for huge scale,
simple access patterns, or semi-structured data. Many systems use **both** (SQL
for orders, a key-value store for sessions).

**CQRS (Command Query Responsibility Segregation)** splits the **write** model
from the **read** model: writes go to a normalised store optimised for
correctness; reads come from **denormalised**, pre-computed views (often built by
consuming a change/event stream) optimised for fast queries. It powers feeds and
dashboards — at the cost of eventual consistency between the two sides and more
moving parts. **Denormalisation** in general — storing redundant, pre-joined data
— is a core scaling tactic: trade storage and write complexity for fast reads.
""",
        ),
        _t(
            "Consistency models & transactions",
            "11 min",
            r"""# Consistency models & distributed transactions

Beyond "strong vs eventual" there's a **spectrum** of guarantees, and naming the
one you need prevents both bugs and over-engineering:

- **Strong / linearizable** — reads always see the latest write, as if there were
  one copy. Strongest, costliest.
- **Read-your-writes** — *you* always see *your own* updates (others may lag).
  Often the practical minimum for good UX.
- **Monotonic reads** — you never see time go backwards (no reading newer then
  older).
- **Causal** — operations that are cause-and-effect are seen in order by everyone
  (a reply never appears before the message it answers).
- **Eventual** — replicas converge if writes stop; cheapest, most available.

**Distributed transactions** — updating data across multiple shards/services
atomically — are the hard case:

- **Two-Phase Commit (2PC)** — a coordinator asks all participants to *prepare*,
  then *commit* only if all said yes. Gives atomicity but is **blocking**: if the
  coordinator dies mid-commit, participants are stuck holding locks. Slow and
  fragile at scale.
- **Saga** — model a long transaction as a **sequence of local transactions**,
  each with a **compensating action** to undo it. If step 4 fails, run the
  compensations for 3,2,1 (refund, release inventory, cancel order). No global
  locks; **eventual** consistency; you must design the undo logic. The default for
  microservices.

The pragmatic stance: **avoid distributed transactions when you can** — keep data
that changes together on the **same shard/service**, and lean on **idempotency
keys** so retries are safe. When you truly need cross-service atomicity, reach for
a **saga**, not 2PC. The next lab makes one quorum-consistency knob concrete.
""",
        ),
        _code(
            "Quorum consistency (W + R > N)",
            "12 min",
            r"""# In a leaderless (Dynamo-style) store, each write goes to W replicas and each
# read queries R of N replicas. If W + R > N, the read set and write set must
# OVERLAP, so a read is guaranteed to see the latest write. Explore the knob.

N = 5     # total replicas per key

def classify(N, W, R):
    strong = (W + R > N)
    # Writes succeed while at most (N - W) replicas are down; reads while (N - R) down.
    write_fault_tolerance = N - W
    read_fault_tolerance = N - R
    return strong, write_fault_tolerance, read_fault_tolerance

configs = [
    (1, 1),   # fast, highly available, but stale reads possible
    (5, 1),   # durable + fast reads, slow/fragile writes
    (1, 5),   # fast writes, slow/fragile reads
    (3, 3),   # balanced quorum (majority)
    (2, 4),
    (4, 2),
]

print("N =", N, "replicas per key")
print("W  R   overlap?   tolerates (write/read failures)")
for W, R in configs:
    strong, wft, rft = classify(N, W, R)
    label = "STRONG " if strong else "stale  "
    print(" ", W, " ", R, "  ", label, "  W tolerates", wft, "down,  R tolerates", rft, "down")

print()
print("W + R > N  => the read quorum overlaps the write quorum => strong reads.")
print("W=R=3 (majority) is the common balanced choice: strong, tolerates 2 failures.")
""",
        ),
        _t(
            "Bloom filters & probabilistic structures",
            "10 min",
            r"""# Bloom filters & probabilistic data structures

At scale, exact answers can be too expensive in memory. **Probabilistic data
structures** trade a controlled amount of error for *huge* space savings — a
recurring system-design superpower.

The **Bloom filter** answers one question — *"have I seen this item?"* — using a
tiny bit array and *k* hash functions:

- **Insert** — hash the item with *k* functions; set those *k* bits to 1.
- **Query** — hash again; if **any** of those *k* bits is 0, the item is
  **definitely not** present. If **all** are 1, it's **probably** present.

The asymmetry is the whole point: **no false negatives**, but **false positives**
are possible (other items' bits can collide to set all *k*). You tune the
false-positive rate with the bit-array size *m* and hash count *k*; more bits per
element → fewer collisions → lower error.

**Why it's everywhere:** a Bloom filter for "is this key in the database?" lets a
system **skip an expensive disk/network lookup** for the vast majority of *absent*
keys — used in databases (LSM-trees like Cassandra/RocksDB skip SSTables), CDNs
(cache admission), web crawlers (seen-URL sets), and spam/duplicate detection. It
might use **~10 bits per element** for a 1% false-positive rate — versus storing
the full keys.

Cousins worth knowing: **Counting Bloom filter** (supports deletion),
**HyperLogLog** (estimates *cardinality* — "how many unique visitors?" — in
kilobytes instead of gigabytes), and **Count-Min Sketch** (estimates frequencies
of a stream). All follow the same bargain: **accept bounded error, save enormous
space.** You'll build a Bloom filter next.
""",
        ),
        _code(
            "Build a Bloom filter",
            "14 min",
            r"""# A Bloom filter: a bit array + k hashes. No false negatives, tunable false
# positives. We hand-roll k FNV-1a hashes (varying the seed) over a numpy
# bit array, then measure the false-positive rate empirically.

import numpy as np

def fnv1a(text, seed):
    h = (2166136261 ^ seed) & 0xFFFFFFFF
    for ch in text:
        h = (h ^ ord(ch)) & 0xFFFFFFFF
        h = (h * 16777619) & 0xFFFFFFFF
    return h

m = 200        # number of bits
k = 4          # number of hash functions
bits = np.zeros(m, dtype=int)

# Insert a set of members.
members = []
for i in range(30):
    members.append("member-" + str(i))
for word in members:
    for s in range(k):
        idx = fnv1a(word, s * 7919 + 1) % m
        bits[idx] = 1

print("bits set:", int(bits.sum()), "of", m)

# Query 30 known members (must ALL report present -> no false negatives) ...
present_hits = 0
for word in members:
    all_set = True
    for s in range(k):
        if bits[fnv1a(word, s * 7919 + 1) % m] == 0:
            all_set = False
            break
    if all_set:
        present_hits = present_hits + 1
print("known members reported present:", present_hits, "of", len(members), "(expect all)")

# ... and 1000 non-members; any 'present' is a FALSE POSITIVE.
false_pos = 0
trials = 1000
for i in range(trials):
    word = "stranger-" + str(i)
    all_set = True
    for s in range(k):
        if bits[fnv1a(word, s * 7919 + 1) % m] == 0:
            all_set = False
            break
    if all_set:
        false_pos = false_pos + 1
print("false positives:", false_pos, "of", trials, "=", round(100.0 * false_pos / trials, 1), "%")
print("no false negatives is GUARANTEED; the false-positive rate falls as m grows.")
""",
        ),
        _t(
            "Reliability, SLOs & the math of nines",
            "10 min",
            r"""# Reliability, SLOs & the math of nines

You can't improve what you don't measure, and you can't promise what you don't
quantify. The vocabulary:

- **SLI (Indicator)** — a measured number: % of requests under 200 ms, error
  rate, uptime.
- **SLO (Objective)** — your *target* for an SLI: "99.9% of requests succeed each
  month."
- **SLA (Agreement)** — a *contractual* promise to customers, usually looser than
  the internal SLO, with penalties if breached.

**Availability "nines"** — what the targets actually cost in downtime:

```
99%      ("two nines")   → ~3.65 days/year   down
99.9%    ("three nines") → ~8.8  hours/year
99.99%   ("four nines")  → ~52   minutes/year
99.999%  ("five nines")  → ~5.3  minutes/year
```

Each extra nine is **~10× harder and costlier** — it demands more redundancy,
automation, and operational rigour. Don't chase nines you don't need; pick the SLO
the business actually requires.

**Composing availability:** services in a **dependency chain** *multiply* — if a
request needs three components each at 99.9%, the whole is `0.999³ ≈ 99.7%`
(worse than any part). More dependencies → lower combined availability. The cure
is **redundancy in parallel**: two independent 99% replicas give
`1 − 0.01² = 99.99%` (far better than one). So: **minimise serial dependencies,
add parallel redundancy.**

**Error budgets** make SLOs actionable: a 99.9% SLO permits ~0.1% failures — that
*budget* is spent on risk. Plenty left? Ship features faster. Budget exhausted?
Freeze risky changes and focus on stability. It turns reliability from a vague
aspiration into a number that guides decisions — and balances velocity against
stability without endless debate.
""",
        ),
        _t(
            "Case study: design a URL shortener",
            "12 min",
            r"""# Case study: design a URL shortener

Let's assemble everything into one design — a TinyURL-style service. This is the
canonical interview/warm-up because it touches estimation, APIs, data modelling,
caching, and scale.

**1. Requirements.** *Functional:* create a short code for a long URL; redirect a
short code to the long URL; (optional) custom aliases, expiry, click analytics.
*Non-functional:* very **read-heavy** (redirects ≫ creations), **low-latency**
redirects, **high availability** (a dead shortener breaks every link), links
**durable** for years.

**2. Estimate.** Say 100M new URLs/month ≈ ~40 writes/s; at 100:1 reads that's
~4,000 redirects/s (peak higher). Over 5 years ≈ 6B URLs. 6B fits in **7
characters** of base62 (62⁷ ≈ 3.5 trillion), so short codes are tiny — storage is
modest (a few TB), but **read QPS and latency** dominate the design.

**3. API.** `POST /urls {long_url}` → `{short_code}`; `GET /{short_code}` → `301`
redirect to the long URL.

**4. Data model.** A key-value mapping `short_code → long_url` (+ created_at,
expiry, owner). Key-value access, no joins → a **NoSQL/KV store** shards cleanly
by `short_code`.

**5. Generating the code.** Either a **counter → base62 encode** (needs a
distributed unique counter — a range-allocator service hands each app server a
block of IDs to avoid coordination per request), or **hash the URL and take 7
chars** (handle the rare collision by retrying). The ID-block approach avoids
hot-counter contention.

**6. Make redirects fast.** Redirects are the hot path → **cache aggressively**:
the `code → url` map is immutable, so a cache (Redis) with a high hit-rate serves
most redirects from RAM, and a **CDN/edge** can cache the 301 itself. The database
is the source of truth behind the cache.

**7. Scale & resilience.** Stateless app servers behind a **load balancer**;
**sharded** KV store (by code) with **replication** for durability/availability;
**multi-region + anycast** so redirects are fast worldwide; analytics done
**asynchronously** via a **queue** (don't slow the redirect to count a click).

Notice every building block from this track appears — estimation sized it,
caching and the CDN made it fast, sharding and replication made it scale and
survive, and a queue kept the hot path lean. That's system design: **the right
boxes, connected for the requirements.**
""",
        ),
        quiz_lesson(
            "Quiz: Designing Real Systems",
            (
                q(
                    "In the standard scaling playbook, which is usually the highest-leverage early step?",
                    (
                        opt("Adding a cache to eliminate repeated reads", correct=True),
                        opt("Sharding the database immediately"),
                        opt("Rewriting everything as microservices"),
                        opt("Removing the load balancer"),
                    ),
                    "A cache gives the biggest win for the least effort; premature sharding/microservices add complexity before it's needed.",
                ),
                q(
                    "What does CQRS separate?",
                    (
                        opt(
                            "The write model (normalised, correct) from the read model (denormalised, fast)",
                            correct=True,
                        ),
                        opt("The frontend from the backend"),
                        opt("Encryption from compression"),
                        opt("Users from administrators"),
                    ),
                    "CQRS splits commands (writes) from queries (reads), letting each side be optimised separately — at the cost of eventual consistency between them.",
                ),
                q(
                    "Why prefer a Saga over Two-Phase Commit for cross-service transactions?",
                    (
                        opt(
                            "Sagas use local transactions with compensating actions, avoiding 2PC's global locks and blocking on coordinator failure",
                            correct=True,
                        ),
                        opt("Sagas guarantee linearizable consistency"),
                        opt("2PC is impossible to implement"),
                        opt("Sagas require no error handling"),
                    ),
                    "2PC blocks and holds locks if the coordinator fails; a saga runs local steps with compensations, trading global atomicity for availability.",
                ),
                q(
                    "In quorum replication, what does W + R > N guarantee?",
                    (
                        opt(
                            "The read and write quorums overlap, so a read sees the latest write (strong reads)",
                            correct=True,
                        ),
                        opt("Writes are always faster"),
                        opt("No replicas can ever fail"),
                        opt("The data is encrypted"),
                    ),
                    "Overlapping quorums mean at least one replica in any read set has the newest write — the basis of tunable consistency.",
                ),
                q(
                    "What is the defining property of a Bloom filter?",
                    (
                        opt(
                            "No false negatives, but possible false positives — 'definitely not present' or 'probably present'",
                            correct=True,
                        ),
                        opt("It stores the full items exactly"),
                        opt("It has false negatives but no false positives"),
                        opt("It can delete items for free"),
                    ),
                    "If any of the k bits is 0 the item is definitely absent; all-1 means probably present (collisions cause false positives).",
                ),
                q(
                    "Three services each at 99.9% availability are called in sequence for one request. The combined availability is…",
                    (
                        opt("Lower — ~99.7% (0.999³); serial dependencies multiply", correct=True),
                        opt("Higher — 99.99%"),
                        opt("Exactly 99.9%"),
                        opt("100%"),
                    ),
                    "Serial dependencies multiply (0.999³ ≈ 0.997); reduce serial deps and add parallel redundancy to raise availability.",
                ),
            ),
        ),
    ),
)


SYSTEM_DESIGN_COURSES = (_SD_BASICS, _SD_INTERMEDIATE, _SD_ADVANCED)
