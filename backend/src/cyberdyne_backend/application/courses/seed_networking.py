"""Academy seed content — the Computer Networking track (Beginner → Advanced).

* ``networking-basics``        — layers, IP & subnets, DNS, HTTP, how a packet travels
* ``networking-intermediate``  — TCP/UDP, routing & shortest paths, NAT/DHCP, IPv6
* ``networking-advanced``      — congestion control, BDP, BGP, CDNs, HTTP/2-3, QUIC

Runnable ``code`` lessons use Python builtins + numpy only (the sandbox blocks
socket/ipaddress/struct/etc.), so labs do IP/subnet math, the Internet checksum,
shortest-path routing, and TCP congestion-window simulation by hand.
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
# networking-basics
# ──────────────────────────────────────────────────────────────────────

_NET_BASICS = SeedCourse(
    slug="networking-basics",
    title="Computer Networking — Basics",
    description=(
        "How computers talk: packets and the layered model, IP addresses and "
        "subnets, how a packet actually travels from your laptop to a server, "
        "and the everyday protocols — DNS and HTTP. With a runnable subnet "
        "calculator you build from bit operations."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a network? Packets vs circuits",
            "9 min",
            r"""# What is a network?

A **network** is just devices (**hosts**) connected by **links** so they can
exchange data, joined by **switches** and **routers**. The **Internet** is a
network of networks — billions of hosts reachable through a chain of routers.

## Packet switching

The old telephone network used **circuit switching**: reserve a dedicated path
end-to-end for the whole call. Wasteful — the line sits idle between words.

The Internet uses **packet switching**: data is chopped into small **packets**,
each stamped with a destination address, and each is forwarded independently,
hop by hop, sharing links with everyone else's packets. Benefits:

- **Efficiency** — links are shared statistically; no idle reservations.
- **Resilience** — if a link dies, packets reroute around it.
- **Scale** — no per-conversation state in the core.

The cost is that packets can arrive **out of order, be delayed, or be lost** —
so higher layers must cope (that's what TCP does, next course).

Two numbers describe any link:

- **Bandwidth** — capacity, bits per second (how *wide* the pipe).
- **Latency** — delay for one bit to travel end-to-end (how *long* the pipe).

They're independent: a satellite link can have huge bandwidth but terrible
latency. Keeping packet-switching and these two metrics in mind makes the rest
of networking click.
""",
        ),
        _t(
            "The layered model",
            "10 min",
            r"""# The layered model

Networking is built as **layers**, each solving one problem and offering a clean
service to the layer above. The practical **TCP/IP** model has 4–5 layers
(the academic **OSI** model splits them into 7):

```
Application   HTTP, DNS, SSH        "what the data means"
Transport     TCP, UDP              "end-to-end delivery, ports"
Network       IP                    "addressing & routing between networks"
Link          Ethernet, Wi-Fi       "one hop, MAC addresses"
Physical      cables, radio         "bits on the wire"
```

The magic is **encapsulation**: each layer wraps the layer above in its own
header, like nesting envelopes:

```
[ Ethernet [ IP [ TCP [ HTTP data ] ] ] ]
```

Your browser hands HTTP to TCP, which adds a TCP header (ports, sequence
numbers) and passes it to IP, which adds source/dest IP addresses, which the
link layer wraps with MAC addresses for the next hop. At the receiver, each
layer **strips its header** and passes the payload up.

Why layer at all? **Separation of concerns**: IP doesn't care if you're using
Wi-Fi or fibre; HTTP doesn't care how packets are routed. You can swap Wi-Fi for
Ethernet, or HTTP/1.1 for HTTP/3, without touching the other layers. This is the
single most important idea in networking — everything else hangs off it.
""",
        ),
        _t(
            "IP addresses & subnets",
            "11 min",
            r"""# IP addresses & subnets

Every host on an IP network has an **IP address**. IPv4 is 32 bits, written as
four **octets**: `192.168.1.10`. An address splits into a **network part** and a
**host part**; a **subnet mask** (or **CIDR** prefix) says where the split is.

**CIDR notation** `192.168.1.0/24` means "the first 24 bits are the network".
So:

- **Network address** = host bits all 0 → `192.168.1.0`
- **Broadcast address** = host bits all 1 → `192.168.1.255`
- **Usable hosts** = $2^{(32 - \text{prefix})} - 2$ (minus network & broadcast)

A `/24` gives $2^8 - 2 = 254$ hosts; a `/30` (point-to-point link) gives just 2.

```plot
{"title": "Usable hosts shrink as the prefix grows", "xLabel": "CIDR prefix length", "yLabel": "usable hosts", "xRange": [24, 31], "yRange": [0, 260], "functions": [{"expr": "2^(32 - x) - 2", "label": "2^(32−prefix) − 2", "color": "#2563eb"}]}
```

**Private ranges** (RFC 1918) are reusable inside any network and not routed on
the public Internet: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`. Your home
router hands these out and uses **NAT** (later) to share one public address.

**Subnetting** carves a big block into smaller ones by borrowing host bits for
the network part — how organisations split address space among departments. You
do the bit math by hand next.
""",
        ),
        _code(
            "Build a subnet calculator",
            "13 min",
            r"""# An IPv4 address is just a 32-bit number. With bit operations you can derive
# the network, broadcast, and host count of any CIDR block. Press Run.

def ip_to_int(ip):
    parts = ip.split(".")
    value = 0
    for part in parts:
        value = value * 256 + int(part)   # shift left one octet, add it
    return value

def int_to_ip(value):
    octets = []
    for shift in [24, 16, 8, 0]:
        octets.append(str((value >> shift) & 255))
    return ".".join(octets)

ip = "192.168.1.10"
prefix = 24

addr = ip_to_int(ip)
# Mask = 'prefix' ones followed by (32-prefix) zeros.
mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
network = addr & mask
broadcast = network | (0xFFFFFFFF >> prefix)
host_bits = 32 - prefix
usable = (2 ** host_bits) - 2

print("address:  ", ip, "/", prefix)
print("netmask:  ", int_to_ip(mask))
print("network:  ", int_to_ip(network))
print("broadcast:", int_to_ip(broadcast))
print("first host:", int_to_ip(network + 1))
print("last host: ", int_to_ip(broadcast - 1))
print("usable hosts:", usable)
# Try /30 (a router link -> 2 hosts) or /16 (a big LAN -> 65534 hosts).
""",
        ),
        _t(
            "How a packet travels",
            "10 min",
            r"""# How a packet travels

You type a URL; how do bytes reach the server? Follow one packet.

1. **Name → address.** Your host asks **DNS** to turn `example.com` into an IP
   (next lesson).
2. **Local or remote?** Your host compares the destination IP to its own subnet
   (using the mask). **Same subnet** → deliver directly. **Different subnet** →
   send to the **default gateway** (your router).
3. **IP → MAC (ARP).** To put the packet on the local link, it needs the
   *next hop's* **MAC address** (the link-layer hardware address). **ARP**
   broadcasts "who has 192.168.1.1?" and caches the reply.
4. **Switching (within a LAN).** A **switch** forwards the frame to the right
   port using MAC addresses — it doesn't look at IP.
5. **Routing (between networks).** Each **router** looks at the **destination
   IP**, consults its **routing table**, and forwards toward the next hop —
   repeatedly, hop by hop, until the destination network is reached. The MAC
   addresses change every hop; the **IP addresses stay the same** end-to-end.

So two different address systems work together: **MAC** for "the next hop on
this link" and **IP** for "the ultimate destination across the Internet."
Switches operate on MAC (Layer 2, within a network); routers operate on IP
(Layer 3, between networks). `traceroute` shows you the actual chain of routers
a packet crosses to reach a host.
""",
        ),
        _t(
            "DNS: the Internet's phone book",
            "9 min",
            r"""# DNS: the Internet's phone book

Humans use names (`cyberdynecorp.ai`); routers need IP addresses. The **Domain
Name System (DNS)** translates between them — a massive, distributed, cached
directory.

A lookup walks a **hierarchy** of name servers:

1. Your **resolver** (often your ISP's or a public one like `1.1.1.1`) gets the
   query.
2. It asks a **root** server → which points to the **TLD** server (`.ai`).
3. The TLD points to the domain's **authoritative** server.
4. That returns the answer (e.g. an **A record**: name → IPv4).

Every step is **cached** with a **TTL** (time-to-live), so popular names resolve
instantly without hitting the root each time.

Common **record types**:

- **A / AAAA** — name → IPv4 / IPv6 address.
- **CNAME** — an alias (name → another name).
- **MX** — mail server for the domain.
- **TXT** — arbitrary text (SPF, domain verification).
- **NS** — the authoritative name servers.

DNS is foundational and a frequent culprit ("it's always DNS"): a wrong record
or stale cache breaks everything downstream. It's also security-sensitive —
hijacking it redirects users — which is why **DNSSEC** (signed records) and
encrypted DNS (DoH/DoT) exist.
""",
        ),
        _t(
            "HTTP & the web",
            "10 min",
            r"""# HTTP & the web

**HTTP** (HyperText Transfer Protocol) is the application-layer protocol of the
web — a simple **request/response** conversation over TCP.

A request:

```
GET /courses HTTP/1.1
Host: cyberdynecorp.ai
Accept: application/json
```

A response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{ "courses": [ ... ] }
```

**Methods** (the verb):

- **GET** — read a resource (no side effects).
- **POST** — create / submit.
- **PUT/PATCH** — update. **DELETE** — remove.

**Status codes** (the result class):

- **2xx** success (200 OK, 201 Created)
- **3xx** redirect (301 moved, 304 not modified)
- **4xx** client error (400 bad request, 401 unauthorized, 404 not found)
- **5xx** server error (500, 503)

HTTP is **stateless** — each request stands alone — so apps track sessions with
**cookies** or tokens. **HTTPS** is HTTP over **TLS**: the same protocol,
encrypted and authenticated (your Security course covers the handshake).

This request/response model underpins REST APIs, the courses you're reading now,
and almost every app you use. Newer versions (HTTP/2, HTTP/3) keep these
semantics but change *how* bytes move on the wire — covered in the Advanced
course.
""",
        ),
        quiz_lesson(
            "Quiz: Networking Basics",
            (
                q(
                    "What is the main advantage of packet switching over circuit switching?",
                    (
                        opt(
                            "Links are shared efficiently and packets reroute around failures",
                            correct=True,
                        ),
                        opt("It reserves a dedicated path for each conversation"),
                        opt("It guarantees packets never get lost"),
                        opt("It removes the need for addresses"),
                    ),
                    "Packets are forwarded independently over shared links — efficient and resilient, at the cost of possible loss/reordering.",
                ),
                q(
                    "What does encapsulation mean in the layered model?",
                    (
                        opt("Each layer wraps the layer above with its own header", correct=True),
                        opt("All layers share one big header"),
                        opt("The application layer talks directly to the physical layer"),
                        opt("Packets are encrypted at every layer"),
                    ),
                    "Each layer adds its header (TCP, then IP, then Ethernet…); the receiver strips them back off.",
                ),
                q(
                    "For a /24 network, how many usable host addresses are there?",
                    (
                        opt("254 (2^8 − 2, excluding network and broadcast)", correct=True),
                        opt("256"),
                        opt("255"),
                        opt("24"),
                    ),
                    "A /24 leaves 8 host bits → 2^8 = 256, minus the network and broadcast addresses = 254.",
                ),
                q(
                    "What's the difference between a MAC address and an IP address as a packet travels?",
                    (
                        opt(
                            "MAC identifies the next hop on a link (changes each hop); IP is the end-to-end destination (stays the same)",
                            correct=True,
                        ),
                        opt("They are the same thing"),
                        opt("IP changes every hop; MAC stays the same"),
                        opt("MAC is only used on the Internet backbone"),
                    ),
                    "Switches forward by MAC within a link; routers forward by IP between networks — IP endpoints are constant.",
                ),
                q(
                    "What does DNS do?",
                    (
                        opt(
                            "Translates human-readable names into IP addresses via a cached hierarchy",
                            correct=True,
                        ),
                        opt("Encrypts web traffic"),
                        opt("Assigns MAC addresses"),
                        opt("Routes packets between networks"),
                    ),
                    "DNS resolves names to addresses through root → TLD → authoritative servers, cached by TTL.",
                ),
                q(
                    "An HTTP response with status 404 means…",
                    (
                        opt("Client error — the requested resource was not found", correct=True),
                        opt("Success"),
                        opt("Server crashed (5xx)"),
                        opt("Redirect to another URL"),
                    ),
                    "4xx are client errors; 404 specifically means the resource doesn't exist.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# networking-intermediate
# ──────────────────────────────────────────────────────────────────────

_NET_INTERMEDIATE = SeedCourse(
    slug="networking-intermediate",
    title="Computer Networking — Intermediate",
    description=(
        "The transport and network layers in depth: TCP vs UDP and the "
        "three-way handshake, the Internet checksum, how routers find shortest "
        "paths, NAT and DHCP, and IPv6 — with runnable checksum and routing "
        "(Dijkstra) labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "TCP vs UDP",
            "10 min",
            r"""# TCP vs UDP

The transport layer adds **ports** (so many apps share one IP) and offers two
very different services.

**TCP** — *reliable, ordered, connection-oriented.*

- Establishes a connection (handshake), numbers every byte, **retransmits**
  what's lost, **reorders** what arrives jumbled, and applies **flow** and
  **congestion control**.
- Cost: setup latency and overhead. Use it when **correctness matters**: web,
  email, file transfer, APIs, databases.

**UDP** — *unreliable, unordered, connectionless.*

- Just wraps your data with ports and a checksum and fires it off. No handshake,
  no retransmit, no ordering.
- Benefit: **minimal latency and overhead**. Use it when **speed beats
  perfection** or you build your own reliability: live video/voice, gaming, DNS
  queries, QUIC (which puts reliability *on top* of UDP).

```
TCP: "Did you get packet 5? No? Here it is again." (reliable, slower)
UDP: "Here's the data." ...gone. (fast, best-effort)
```

**Ports** identify the app: a server listens on a well-known port (HTTP 80,
HTTPS 443, DNS 53, SSH 22); the client uses a random high port. A connection is
uniquely identified by the **4-tuple** (source IP+port, dest IP+port), which is
how one server handles thousands of simultaneous clients. Choosing TCP vs UDP is
one of the first design decisions for any networked app.
""",
        ),
        _t(
            "TCP in depth: the handshake & reliability",
            "11 min",
            r"""# TCP in depth

**Opening a connection — the 3-way handshake.** Before data flows, both sides
agree on starting sequence numbers:

```
client → SYN (seq=x)
server → SYN-ACK (seq=y, ack=x+1)
client → ACK (ack=y+1)        ...connection established
```

(Closing uses a similar FIN/ACK exchange.)

**Reliability via sequence & acknowledgement numbers.** Every byte is numbered.
The receiver **ACKs** the next byte it expects. If the sender doesn't get an ACK
within a timeout (or sees **duplicate ACKs**), it **retransmits**. Out-of-order
segments are buffered and reordered. This is how TCP turns the lossy, unordered
IP layer into a clean byte stream.

**Flow control — don't overwhelm the receiver.** Each ACK carries a **receive
window**: "I have room for N more bytes." The sender never has more than a
window's worth of unacknowledged data in flight. A slow receiver shrinks the
window; the sender slows down.

**Sliding window.** Rather than send-one-wait-one (terrible over high latency),
TCP keeps a *window* of bytes in flight, sliding it forward as ACKs arrive — so
throughput depends on **window ÷ round-trip-time**. That ratio, and how the
window grows/shrinks under loss, is the heart of **congestion control** (the
Advanced course). Distinguish the two windows: **flow control** protects the
*receiver*; **congestion control** protects the *network*.
""",
        ),
        _code(
            "The Internet checksum",
            "12 min",
            r"""# Every TCP/UDP/IP header carries a CHECKSUM so the receiver can detect
# corruption. It's a 16-bit one's-complement sum. Build it from bytes.

def internet_checksum(data):
    # Sum the data in 16-bit words.
    total = 0
    for i in range(0, len(data), 2):
        hi = data[i]
        lo = data[i + 1] if i + 1 < len(data) else 0
        word = (hi << 8) + lo
        total = total + word
    # Fold the carry bits back in (one's-complement add).
    while total > 0xFFFF:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF      # one's complement

message = [0x45, 0x00, 0x00, 0x3c, 0x1c, 0x46, 0x40, 0x00]   # bytes of a header
checksum = internet_checksum(message)
print("checksum:", hex(checksum))

# The receiver sums the data AND the checksum; a clean message totals 0xFFFF.
def verify(data, given):
    total = given
    for i in range(0, len(data), 2):
        total = total + ((data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0))
    while total > 0xFFFF:
        total = (total & 0xFFFF) + (total >> 16)
    return total == 0xFFFF

print("verifies clean:", verify(message, checksum))
# Flip one byte and it won't verify — that's how corruption is caught.
flipped = [message[0] ^ 0x01] + message[1:]
print("verifies after a bit flip:", verify(flipped, checksum))
""",
        ),
        _t(
            "Routing: how packets find a path",
            "10 min",
            r"""# Routing: how packets find a path

A **router** decides where to send each packet next, using a **routing table**:
a list of (destination network → next hop). The key rule is **longest-prefix
match** — the most *specific* route wins. Given routes for `10.0.0.0/8` and
`10.1.2.0/24`, a packet to `10.1.2.5` takes the `/24` (more specific).

How tables get filled:

- **Static routing** — a human configures routes. Simple, fine for small/stable
  networks; no automatic failover.
- **Dynamic routing** — routers **talk to each other** and compute paths
  automatically, adapting to failures:
  - **Distance-vector** (RIP) — "tell neighbours your distance to everywhere";
    simple, slow to converge.
  - **Link-state** (OSPF) — every router learns the *whole map* and runs a
    shortest-path algorithm (**Dijkstra**) locally; fast, scalable within an
    organisation.
  - **Path-vector** (BGP) — routing *between* organisations across the Internet
    (Advanced course).

"Shortest" path is by a **cost metric** (hop count, link bandwidth, latency),
not necessarily fewest hops. The classic algorithm link-state protocols use is
**Dijkstra's** — find the lowest-cost path from a source to every other node —
which you'll implement next. Routing is what makes the Internet a *network of
networks*: no router knows the whole Internet, yet packets still find their way.
""",
        ),
        _code(
            "Shortest-path routing (Dijkstra)",
            "14 min",
            r"""# Link-state routing runs Dijkstra to find lowest-cost paths. Here it is on a
# small weighted network (costs = link 'distance'). Pure builtins.

# Graph: node -> list of (neighbour, cost)
graph = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2), ("D", 5)],
    "C": [("A", 4), ("B", 2), ("D", 1)],
    "D": [("B", 5), ("C", 1)],
}

def dijkstra(graph, source):
    INF = float("inf")
    dist = {}
    for node in graph:
        dist[node] = INF
    dist[source] = 0
    visited = {}
    for node in graph:
        visited[node] = False

    for step in range(len(graph)):
        # Pick the unvisited node with the smallest known distance.
        current = None
        best = INF
        for node in graph:
            if not visited[node] and dist[node] < best:
                best = dist[node]
                current = node
        if current is None:
            break
        visited[current] = True
        # Relax each neighbour.
        for neighbour, cost in graph[current]:
            if dist[current] + cost < dist[neighbour]:
                dist[neighbour] = dist[current] + cost
    return dist

distances = dijkstra(graph, "A")
print("shortest cost from A to each node:")
for node in sorted(distances):
    print("  A ->", node, "=", distances[node])
# A->D is 4 (A-B-C-D: 1+2+1), cheaper than A-C-D (4+1) or A-B-D (1+5).
""",
        ),
        _t(
            "NAT, DHCP & getting online",
            "9 min",
            r"""# NAT, DHCP & getting online

Two protocols quietly make every home and office network work.

**DHCP — automatic addressing.** When a device joins, it doesn't know its IP. It
broadcasts a **DHCP** request; the DHCP server (your router) **leases** it an
address plus the subnet mask, default gateway, and DNS servers. That's why you
plug in and "it just works" — no manual config.

**NAT — sharing one public address.** The world ran out of IPv4 addresses, so
your home gets **one** public IP while every device uses a **private** address
(`192.168.x.x`). **Network Address Translation** in your router rewrites
outgoing packets to use the public IP + a unique port, and remembers the mapping
so replies get back to the right device:

```
laptop 192.168.1.5:51000  →  [NAT]  →  203.0.113.7:40001  → server
                          ←  [NAT]  ←  (reply to :40001)   ←
```

Consequences worth knowing:

- **Many devices, one public IP** — NAT is why IPv4 survived as long as it has.
- **Inbound connections are hard** — outside hosts can't reach a device behind
  NAT unless you **port-forward**; this is why hosting a server at home needs
  configuration, and why P2P apps use **STUN/TURN** to "hole-punch".
- NAT is a side effect of address scarcity — **IPv6** (next lesson) has so many
  addresses it removes the need for it.
""",
        ),
        _t(
            "IPv6: why and how",
            "8 min",
            r"""# IPv6: why and how

IPv4's 32 bits give ~4.3 billion addresses — long since exhausted for a planet of
tens of billions of devices. **IPv6** uses **128 bits**: about
$3.4\times10^{38}$ addresses, enough to never worry again.

Format — eight groups of four hex digits, with shorthand:

```
2001:0db8:0000:0000:0000:ff00:0042:8329
2001:db8::ff00:42:8329        # "::" collapses one run of zero groups
```

What changes:

- **No NAT needed** — every device can have a globally unique address, restoring
  true end-to-end connectivity.
- **Simpler headers** — fixed-size, faster for routers to process.
- **Built-in autoconfiguration** (SLAAC) — a host can derive its own address
  from the network prefix.
- **Security & multicast** improvements baked in.

The catch is the **transition**: IPv4 and IPv6 aren't directly compatible, so
the Internet runs **dual-stack** (both at once) with translation/tunnelling
mechanisms during the long migration. Adoption is now past ~40% of traffic and
climbing.

The takeaway: the address-scarcity workarounds you just learned (NAT, private
ranges) are IPv4-era patches; IPv6 is the real fix — abundant addresses and a
cleaner design — gradually becoming the default.
""",
        ),
        quiz_lesson(
            "Quiz: Transport & Routing",
            (
                q(
                    "When should you choose UDP over TCP?",
                    (
                        opt(
                            "When low latency matters more than guaranteed delivery (e.g. live video, gaming, DNS)",
                            correct=True,
                        ),
                        opt("When you need guaranteed, ordered delivery"),
                        opt("When transferring a critical file"),
                        opt("Always — UDP is strictly better"),
                    ),
                    "UDP trades reliability for speed/overhead; TCP is for correctness-critical, ordered data.",
                ),
                q(
                    "What does TCP's 3-way handshake accomplish?",
                    (
                        opt(
                            "Both sides agree on initial sequence numbers and establish the connection (SYN, SYN-ACK, ACK)",
                            correct=True,
                        ),
                        opt("It encrypts the connection"),
                        opt("It assigns IP addresses"),
                        opt("It compresses the data"),
                    ),
                    "SYN/SYN-ACK/ACK synchronises sequence numbers before any data flows.",
                ),
                q(
                    "What does the Internet checksum let the receiver do?",
                    (
                        opt(
                            "Detect corruption — a clean message + checksum sums to all-ones",
                            correct=True,
                        ),
                        opt("Decrypt the payload"),
                        opt("Find the shortest route"),
                        opt("Assign a port number"),
                    ),
                    "The one's-complement sum detects bit errors; a flipped bit makes verification fail.",
                ),
                q(
                    "In a routing table, which route wins for a given destination?",
                    (
                        opt("The longest (most specific) prefix match", correct=True),
                        opt("The shortest prefix"),
                        opt("The first one listed"),
                        opt("A random one"),
                    ),
                    "Longest-prefix match picks the most specific route (e.g. /24 over /8).",
                ),
                q(
                    "What does NAT solve?",
                    (
                        opt(
                            "Letting many private-addressed devices share one public IPv4 address",
                            correct=True,
                        ),
                        opt("Encrypting traffic"),
                        opt("Resolving names to addresses"),
                        opt("Finding shortest paths"),
                    ),
                    "NAT rewrites private addresses to a shared public IP+port, working around IPv4 scarcity.",
                ),
                q(
                    "Why does IPv6 remove the need for NAT?",
                    (
                        opt(
                            "Its 128-bit space gives every device a globally unique address",
                            correct=True,
                        ),
                        opt("It encrypts every packet"),
                        opt("It is faster than IPv4"),
                        opt("It has no addresses at all"),
                    ),
                    "With ~3.4×10^38 addresses, every device can be globally addressable — no sharing needed.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# networking-advanced
# ──────────────────────────────────────────────────────────────────────

_NET_ADVANCED = SeedCourse(
    slug="networking-advanced",
    title="Computer Networking — Advanced",
    description=(
        "Performance and the modern Internet: TCP congestion control and the "
        "bandwidth-delay product, queuing and QoS, BGP and how the Internet "
        "routes between networks, CDNs and load balancing, and HTTP/2, HTTP/3 "
        "(QUIC) — with a runnable congestion-window simulation."
    ),
    level="Advanced",
    lessons=(
        _t(
            "TCP congestion control",
            "11 min",
            r"""# TCP congestion control

Flow control protects the *receiver*; **congestion control** protects the
*network* from collapse when too many senders flood shared links. TCP probes for
available bandwidth and backs off on loss (which it treats as the congestion
signal). The classic algorithm:

- **Slow start.** Begin with a tiny congestion window (**cwnd**) and **double**
  it every round-trip — exponential ramp-up — until a threshold or a loss.
- **Congestion avoidance (AIMD).** Past the threshold, grow **linearly** (+1 per
  RTT) — gentle probing.
- **On loss** (timeout / triple-duplicate-ACK): **multiplicative decrease** —
  cut cwnd (roughly in half), then resume.

This **Additive-Increase / Multiplicative-Decrease (AIMD)** rule produces the
famous **sawtooth**: climb gently, halve on loss, climb again. It's both *stable*
and *fair* — competing flows converge toward an equal share of a link.

The amount of data in flight is **min(cwnd, receive window)**, so throughput is
roughly `window / RTT`. High-latency links need big windows to stay full — which
is exactly the **bandwidth-delay product** (next lesson).

Modern variants change the climb/back-off: **CUBIC** (Linux default, better on
high-speed links) and **BBR** (Google — models bandwidth and RTT directly
instead of treating loss as the only signal). You'll simulate the AIMD sawtooth
next.
""",
        ),
        _code(
            "Simulate the AIMD congestion window",
            "13 min",
            r"""# Simulate TCP's congestion window: slow-start (double), congestion avoidance
# (+1/RTT), and multiplicative decrease on loss. Watch the sawtooth in numbers.

cwnd = 1.0          # congestion window (in segments)
ssthresh = 16.0     # slow-start threshold
loss_rounds = {6, 13, 19}    # rounds where a loss occurs

history = []
for rnd in range(24):
    history.append(round(cwnd, 1))
    if rnd in loss_rounds:
        ssthresh = max(cwnd / 2.0, 1.0)   # multiplicative decrease
        cwnd = ssthresh                    # resume from the new threshold
    elif cwnd < ssthresh:
        cwnd = cwnd * 2.0                  # slow start: exponential
    else:
        cwnd = cwnd + 1.0                  # congestion avoidance: linear (AIMD)

print("cwnd per round (the 'sawtooth'):")
print(history)
peak = max(history)
print("peak window:", peak, "segments")
print("note: exponential ramp early, linear growth after ssthresh, halving on loss")
""",
        ),
        _t(
            "Bandwidth, latency & the BDP",
            "10 min",
            r"""# Bandwidth, latency & the bandwidth-delay product

Three numbers describe network performance, and people constantly conflate them:

- **Bandwidth** — capacity (bits/sec). The *width* of the pipe.
- **Latency (RTT)** — round-trip delay. The *length* of the pipe.
- **Throughput** — the rate you *actually* achieve, ≤ bandwidth.

The non-obvious result: on a reliable, windowed protocol like TCP, throughput is
capped by **window ÷ RTT**, not just bandwidth. To keep a fat, long pipe full you
must have enough data **in flight** — the **bandwidth-delay product (BDP)**:

$$ \text{BDP} = \text{bandwidth} \times \text{RTT}. $$

It's literally how many bits "fit in the pipe" at once. If your TCP window is
smaller than the BDP, you leave capacity idle no matter how fat the link — the
"**long fat network**" problem (satellite, transcontinental links). The fix:
**window scaling** (large windows).

Throughput rises with window size until it saturates the link, then flattens:

```plot
{"title": "Throughput rises with window, then saturates the link", "xLabel": "window size (× segments)", "yLabel": "throughput", "xRange": [0, 16], "yRange": [0, 9], "functions": [{"expr": "if(x < 8, x, 8)", "label": "min(window/RTT, bandwidth)", "color": "#2563eb"}]}
```

Practical upshot: to make a connection faster you might need **lower latency**
(move servers closer — CDNs), a **bigger window**, or **less loss** — not just a
bigger bandwidth number. "More Mbps" doesn't help a window- or latency-bound
transfer.
""",
        ),
        _t(
            "Queuing, QoS & buffer bloat",
            "9 min",
            r"""# Queuing, QoS & buffer bloat

When packets arrive at a router faster than the outbound link can send them,
they **queue**. Queues absorb bursts — but they also add **delay**, and when
full, they **drop** packets (the loss that TCP reacts to).

**Quality of Service (QoS)** prioritises traffic that's delay-sensitive. A voice
call or game needs **low latency** even at the cost of throughput; a file
download is the opposite. QoS mechanisms (priority queues, traffic shaping,
DiffServ marking) let routers serve latency-critical packets first.

**Buffer bloat** is the counterintuitive trap: making router buffers *too big*
hurts. Huge queues mean packets wait a long time instead of being dropped, so
latency balloons (web pages crawl while a download runs) and TCP — which relies
on loss as its congestion signal — gets that signal *late*, overshooting. The
fix is **smarter queue management** that drops/marks early: **AQM** algorithms
like **CoDel** and **FQ-CoDel** keep queues short and latency low.

The key mental shift for advanced networking: **bandwidth is rarely the
bottleneck for interactive apps — latency and queuing are.** A link can have
plenty of capacity yet feel terrible if buffers are bloated or traffic isn't
prioritised. Measuring and controlling *latency under load* matters as much as
raw throughput.
""",
        ),
        _t(
            "BGP & how the Internet routes",
            "10 min",
            r"""# BGP & how the Internet routes

Within one organisation, OSPF/Dijkstra find shortest paths. But the Internet is
~75,000 independent networks — **Autonomous Systems (AS)**, each run by an ISP,
cloud, or enterprise. Routing *between* them is the job of the **Border Gateway
Protocol (BGP)**.

BGP is a **path-vector** protocol: ASes advertise "I can reach this prefix, via
this AS-path." Routers pick routes by **policy** — not just shortest path, but
business relationships (prefer a customer's route over a peer's over a
provider's), because money and contracts, not just hops, decide how traffic
flows. BGP is what stitches the networks into *the* Internet.

Two things make BGP famous:

- **It runs the Internet** — every cross-network packet depends on BGP routes
  converging.
- **It's fragile and trust-based** — historically a network could announce
  prefixes it doesn't own (**route hijacking**) or leak routes, causing global
  outages (a single misconfiguration has taken big sites offline). **RPKI**
  (signed route origins) is the ongoing fix.

You won't configure BGP early in your career, but understanding it explains a
lot: why a fibre cut in one country slows traffic elsewhere, why routing changes
take minutes to propagate globally, and why "the Internet is down" is sometimes
really "BGP convergence is in progress."
""",
        ),
        _t(
            "CDNs, load balancing & anycast",
            "9 min",
            r"""# CDNs, load balancing & anycast

Physics caps latency — data can't beat the speed of light, so a server in
Frankfurt always feels slow from Sydney. The fix is to **move content closer to
users** and **spread load**.

- **CDN (Content Delivery Network)** — cache static content (images, video, JS,
  even API responses) on **edge servers** in hundreds of cities. A user fetches
  from the nearest edge → much lower latency, less origin load, and resilience
  against traffic spikes/DDoS. (This is squarely Cyberdyne's serving domain.)
- **Load balancing** — spread requests across many backend servers so no one is
  overwhelmed. Strategies: round-robin, least-connections, latency-based,
  consistent hashing. Layer 4 (by IP/port) vs Layer 7 (by HTTP path/host) load
  balancers. Adds horizontal scalability **and** redundancy.
- **Anycast** — advertise the *same* IP address from many locations; BGP routes
  each user to the **topologically nearest** instance. It's how DNS resolvers
  (`1.1.1.1`) and CDNs send you to a close edge with a single address, and a key
  DDoS defence (attack traffic is dispersed across sites).

Together these turn a single origin into a globally fast, resilient service. The
guiding principle echoes the BDP lesson: **reduce latency by reducing distance**,
and **survive load by spreading it**.
""",
        ),
        _t(
            "The modern web: HTTP/2, HTTP/3 & QUIC",
            "10 min",
            r"""# The modern web: HTTP/2, HTTP/3 & QUIC

HTTP's *semantics* (methods, status codes) have barely changed — but how it moves
bytes has been overhauled for speed.

**HTTP/1.1** — one request at a time per connection. **Head-of-line blocking**:
a slow response stalls everything behind it. Browsers worked around it by opening
many parallel connections (wasteful).

**HTTP/2** — **multiplexing**: many requests/responses share one TCP connection
as interleaved **streams**, plus header compression (HPACK) and server push. Far
fewer connections, much faster page loads. But one problem remains: it still runs
on **TCP**, so a single lost packet stalls *all* streams (TCP-level
head-of-line blocking).

**HTTP/3 + QUIC** — the big leap: replace TCP with **QUIC**, a new transport
built **on UDP**. QUIC gives each stream **independent** delivery (a lost packet
only stalls *its* stream), folds the **TLS handshake into the connection setup**
(0–1 RTT — faster first byte), and survives network changes (Wi-Fi → cellular)
via **connection IDs** without reconnecting. It moves congestion control into
user space, so it can evolve without OS changes.

Also worth knowing: **WebSockets** (full-duplex persistent connections for
real-time apps) and **gRPC** (HTTP/2-based RPC with protobuf, common between
microservices). The throughline: the web keeps pushing latency down — multiplex
to avoid blocking, fold handshakes to cut round-trips, and get closer to the user
(CDNs). Everything you've learned — TCP, congestion, BDP, TLS — comes together
here.
""",
        ),
        quiz_lesson(
            "Quiz: Performance & the Modern Internet",
            (
                q(
                    "What pattern does TCP's AIMD congestion control produce?",
                    (
                        opt(
                            "A sawtooth — gradual linear increase, then a sharp multiplicative cut on loss",
                            correct=True,
                        ),
                        opt("A flat line"),
                        opt("Constant exponential growth"),
                        opt("Random jumps"),
                    ),
                    "Additive increase + multiplicative decrease climbs gently and halves on loss — the classic sawtooth.",
                ),
                q(
                    "What is the bandwidth-delay product (BDP)?",
                    (
                        opt(
                            "bandwidth × RTT — how much data must be in flight to keep a link full",
                            correct=True,
                        ),
                        opt("bandwidth ÷ RTT"),
                        opt("The number of hops to the destination"),
                        opt("The size of a packet"),
                    ),
                    "BDP is the 'bits in the pipe'; a window smaller than the BDP leaves capacity idle.",
                ),
                q(
                    "Why does buffer bloat hurt performance?",
                    (
                        opt(
                            "Oversized queues add latency and delay TCP's loss signal, so pages crawl under load",
                            correct=True,
                        ),
                        opt("It drops too many packets immediately"),
                        opt("It encrypts the queue"),
                        opt("It reduces bandwidth to zero"),
                    ),
                    "Huge buffers trade drops for delay; AQM (CoDel) keeps queues short to control latency.",
                ),
                q(
                    "What does BGP route between?",
                    (
                        opt(
                            "Autonomous Systems (independent networks) across the Internet, by policy",
                            correct=True,
                        ),
                        opt("Hosts within a single subnet"),
                        opt("Threads within a process"),
                        opt("Files on a disk"),
                    ),
                    "BGP is the path-vector protocol connecting ASes; routes are chosen by policy, not just hop count.",
                ),
                q(
                    "How does anycast reduce latency?",
                    (
                        opt(
                            "The same IP is announced from many sites; BGP routes each user to the nearest one",
                            correct=True,
                        ),
                        opt("It encrypts traffic end-to-end"),
                        opt("It increases the bandwidth of each link"),
                        opt("It assigns every user a unique IP"),
                    ),
                    "One address served from many locations sends users to a topologically close instance (also aids DDoS defence).",
                ),
                q(
                    "What key problem does HTTP/3 (QUIC over UDP) solve versus HTTP/2?",
                    (
                        opt(
                            "TCP-level head-of-line blocking — QUIC gives each stream independent delivery",
                            correct=True,
                        ),
                        opt("It removes the need for encryption"),
                        opt("It eliminates DNS"),
                        opt("It makes HTTP stateful"),
                    ),
                    "On TCP, one lost packet stalls all HTTP/2 streams; QUIC isolates loss per stream and speeds up setup.",
                ),
            ),
        ),
    ),
)


NETWORKING_COURSES = (_NET_BASICS, _NET_INTERMEDIATE, _NET_ADVANCED)
