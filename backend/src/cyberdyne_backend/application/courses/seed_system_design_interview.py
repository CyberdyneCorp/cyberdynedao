"""Academy seed content - System Design Interview Prep.

A concept-by-concept course for the system design interview: how to reason
about scalability (vertical vs horizontal), reliability and availability, load
balancing, caching and CDNs, databases (SQL/NoSQL, replication, sharding), the
CAP theorem and consistency, and APIs and message queues - then how to design a
system end to end. Every content lesson pairs a direct explanation with a real
example and a mermaid diagram, followed by a checkpoint quiz, and the course
closes with a full freeCodeCamp crash-course video (with a written summary,
main ideas and a mindmap) and a comprehensive final quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
    video_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_SYSTEM_DESIGN_INTERVIEW = SeedCourse(
    slug="system-design-interview",
    title="System Design Interview Prep",
    description=(
        "Master the system design interview: scalability, reliability and "
        "availability, load balancing, caching and CDNs, SQL vs NoSQL with "
        "replication and sharding, the CAP theorem, and APIs and message "
        "queues - then design a system end to end. Concept-by-concept with "
        "real examples, diagrams, and a full crash-course video."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Welcome - how this course works",
            "6 min",
            '# System Design Interview Prep\n\nThe system design interview is not about writing code - it is about showing how\nyou **glue an entire system together**: how it scales, stays available, stores\nand moves data, and holds up under load. This course gives you the core\nconcepts and a repeatable way to reason about them.\n\nThe approach is **concept by concept**, each explained directly with a real\nexample and a diagram, then a short quiz. You will build up scalability,\nreliability, load balancing, caching, databases, the CAP theorem, and\ncommunication - then put them together to design a system end to end.\n\nThe course closes with a **full crash-course video** from freeCodeCamp that\nwalks the same concepts in one sitting, with a written summary, the main ideas,\nand a mindmap below the player.\n\nBy the end you will be able to take a prompt like "design a URL shortener" or\n"design a news feed" and talk through requirements, high-level architecture,\ndata storage, scaling, and trade-offs with confidence.\n',
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How is this course structured?",
                    (
                        opt(
                            "Concept by concept with examples and diagrams, then a crash-course video",
                            correct=True,
                        ),
                        opt("One long video only"),
                        opt("Only quizzes"),
                    ),
                ),
                q(
                    "What will you be able to do by the end?",
                    (
                        opt("Reason through a system design prompt end to end", correct=True),
                        opt("Only write SQL"),
                        opt("Nothing practical"),
                    ),
                ),
            ),
        ),
        _t(
            "What system design is and how the interview works",
            "9 min",
            '# What system design is and how the interview works\n\n**System design** is the process of defining the architecture, components, and\ndata flow of a software system so it meets its requirements at scale. The\n**system design interview** checks whether you can take a vague, open-ended\nprompt and drive it to a sensible, justified architecture.\n\nThere is no single right answer - interviewers watch **how you reason** and\n**which trade-offs** you make. A reliable structure:\n\n1. **Clarify requirements** - functional (what it does) and non-functional (scale, latency, availability).\n2. **Estimate** - users, requests per second, storage, bandwidth (back-of-the-envelope).\n3. **Define the API** - the operations clients call.\n4. **Sketch the high-level design** - clients, load balancer, services, databases, cache.\n5. **Deep-dive** - pick the hard part and detail it.\n6. **Discuss trade-offs** - bottlenecks, failure modes, scaling.\n\n```mermaid\ngraph LR\n    A["Clarify requirements"] --> B["Estimate scale"]\n    B --> C["Define the API"]\n    C --> D["High-level design"]\n    D --> E["Deep dive"]\n    E --> F["Trade-offs"]\n```\n\nThe rest of this course is the vocabulary and building blocks you draw on at\nstep 4 and defend at step 6.\n',
        ),
        quiz_lesson(
            "Quiz: What system design is and how the interview works",
            (
                q(
                    "What is the system design interview mainly evaluating?",
                    (
                        opt("How you reason about architecture and trade-offs", correct=True),
                        opt("Whether you can write bug-free code fast"),
                        opt("How many algorithms you have memorized"),
                    ),
                    "It is about gluing a system together and justifying decisions, not coding.",
                ),
                q(
                    "Which comes FIRST in a good interview structure?",
                    (
                        opt("Clarifying functional and non-functional requirements", correct=True),
                        opt("Choosing the database vendor"),
                        opt("Drawing the final diagram"),
                    ),
                ),
                q(
                    "A 'non-functional' requirement is, for example:",
                    (
                        opt(
                            "The system must handle 10,000 requests per second at low latency",
                            correct=True,
                        ),
                        opt("Users can post a comment"),
                        opt("The button is blue"),
                    ),
                ),
            ),
        ),
        _t(
            "Scalability: vertical vs horizontal scaling",
            "10 min",
            '# Scalability: vertical vs horizontal scaling\n\n**Scalability** is a system\'s ability to handle growing load. There are two\nways to add capacity:\n\n- **Vertical scaling (scale up)** - give one machine more CPU, RAM, or disk. Simple, but there is a hard ceiling and a single point of failure.\n- **Horizontal scaling (scale out)** - add more machines and spread the load. Nearly unlimited, and it survives a node dying, but it needs a load balancer and stateless services.\n\nMost large systems scale **horizontally** because commodity machines are cheap\nand the design tolerates failure. The catch: your services should be\n**stateless** (keep session and data in a shared store) so any machine can\nhandle any request.\n\n```text\nVertical:   1 server  -> bigger server (32 GB -> 256 GB RAM)\nHorizontal: 1 server  -> 10 servers behind a load balancer\n\nRough capacity: if one node serves 1,000 req/s,\n  10 nodes serve ~10,000 req/s (minus coordination overhead).\n```\n\n```mermaid\ngraph TD\n    LB["Load balancer"] --> S1["Server 1"]\n    LB --> S2["Server 2"]\n    LB --> S3["Server 3"]\n    S1 --> DB["Shared data store"]\n    S2 --> DB\n    S3 --> DB\n```\n\nInterview tip: when asked to scale, say **horizontal + stateless + shared\nstore**, then justify where state lives.\n',
        ),
        quiz_lesson(
            "Quiz: Scalability: vertical vs horizontal scaling",
            (
                q(
                    "What is horizontal scaling?",
                    (
                        opt("Adding more machines and spreading load across them", correct=True),
                        opt("Adding more RAM and CPU to a single machine"),
                        opt("Deleting old data to free space"),
                    ),
                    "Scale out = more nodes; scale up = a bigger node.",
                ),
                q(
                    "Why must services be stateless to scale horizontally well?",
                    (
                        opt(
                            "So any machine can handle any request; state lives in a shared store",
                            correct=True,
                        ),
                        opt("So they can run without electricity"),
                        opt("So they never need a database"),
                    ),
                ),
                q(
                    "A key downside of vertical scaling is:",
                    (
                        opt("A hard capacity ceiling and a single point of failure", correct=True),
                        opt("It requires a load balancer"),
                        opt("It cannot use more RAM"),
                    ),
                ),
            ),
        ),
        _t(
            "Reliability, availability and fault tolerance",
            "10 min",
            '# Reliability, availability and fault tolerance\n\nThree related but distinct goals:\n\n- **Reliability** - the system does the right thing consistently over time (correct results, no data loss).\n- **Availability** - the system is up and answering requests, usually stated as a percentage of uptime.\n- **Fault tolerance** - the system keeps working when a component fails.\n\nAvailability is measured in **nines**. Each nine cuts allowed downtime by 10x:\n\n```text\nAvailability   Downtime per year\n99%    (two 9s)   ~3.65 days\n99.9%  (three 9s) ~8.77 hours\n99.99% (four 9s)  ~52.6 minutes\n99.999%(five 9s)  ~5.26 minutes\n```\n\nYou buy availability with **redundancy**: no single point of failure.\nReplicate servers, replicate data, and use health checks with automatic\nfailover so a dead node is replaced without a human.\n\n```mermaid\ngraph TD\n    Q{"Node healthy"} -->|"yes"| A["Serve traffic"]\n    Q -->|"no"| B["Health check fails"]\n    B --> C["Failover to replica"]\n    C --> A\n```\n\nInterview tip: tie an availability target to a concrete number (for example\n"99.99 percent means under an hour of downtime a year") and back it with\nredundancy and failover.\n',
        ),
        quiz_lesson(
            "Quiz: Reliability, availability and fault tolerance",
            (
                q(
                    "What does 'availability' measure?",
                    (
                        opt(
                            "The share of time the system is up and answering requests",
                            correct=True,
                        ),
                        opt("How fast a single request runs"),
                        opt("How much data the system stores"),
                    ),
                ),
                q(
                    "How do you primarily achieve high availability?",
                    (
                        opt("Redundancy: no single point of failure, with failover", correct=True),
                        opt("Buying one very expensive server"),
                        opt("Turning off health checks"),
                    ),
                ),
                q(
                    "Going from 99.9 to 99.99 percent availability roughly:",
                    (
                        opt("Cuts allowed downtime by about 10x", correct=True),
                        opt("Doubles allowed downtime"),
                        opt("Has no effect on downtime"),
                    ),
                ),
            ),
        ),
        _t(
            "Load balancing",
            "9 min",
            '# Load balancing\n\nA **load balancer** sits in front of your servers and spreads incoming\nrequests across them. It is what makes horizontal scaling work: clients hit one\naddress, and the balancer picks a healthy backend.\n\nCommon **algorithms**:\n\n- **Round robin** - each server in turn. Simple and even when servers are similar.\n- **Least connections** - send to the server with the fewest active requests. Good for uneven request costs.\n- **Hashing** - route by a key (for example user id) so a client sticks to one server.\n\nThe balancer also runs **health checks** and stops sending traffic to a node\nthat fails them - this is where availability comes from. At large scale you run\n**multiple load balancers** too, so the balancer itself is not a single point\nof failure.\n\n```mermaid\ngraph TD\n    C["Clients"] --> LB["Load balancer"]\n    LB -->|"round robin"| S1["Server 1"]\n    LB --> S2["Server 2"]\n    LB --> S3["Server 3"]\n    LB --> H["Health checks"]\n```\n\nInterview tip: name the algorithm and say the balancer does health checks and\nenables both scaling and availability.\n',
        ),
        quiz_lesson(
            "Quiz: Load balancing",
            (
                q(
                    "What does a load balancer do?",
                    (
                        opt(
                            "Spreads incoming requests across multiple backend servers",
                            correct=True,
                        ),
                        opt("Stores the primary copy of the database"),
                        opt("Encrypts the hard disk"),
                    ),
                ),
                q(
                    "Which load-balancing algorithm sends a request to the server with the fewest active requests?",
                    (
                        opt("Least connections", correct=True),
                        opt("Round robin"),
                        opt("Random-only"),
                    ),
                ),
                q(
                    "Besides distributing load, a load balancer improves availability by:",
                    (
                        opt("Running health checks and skipping unhealthy nodes", correct=True),
                        opt("Deleting slow requests"),
                        opt("Turning servers off at night"),
                    ),
                ),
            ),
        ),
        _t(
            "Caching and CDNs",
            "10 min",
            '# Caching and CDNs\n\nA **cache** stores the results of expensive work close to where it is needed so\nrepeated requests are fast. It trades a little staleness for a lot of speed and\ntakes load off your database.\n\nWhere caches live:\n\n- **Client / browser** - avoids a network trip entirely.\n- **Application / in-memory** - a store like **Redis** or Memcached in front of the database.\n- **CDN (Content Delivery Network)** - caches static assets (images, video, JS) at edge locations near users worldwide.\n\nThe hard part is **invalidation** - keeping cached data from going stale.\nCommon policies: **TTL** (expire after a time), **write-through** (update cache\nand DB together), and **eviction** like **LRU** (drop least-recently-used when full).\n\n```text\nRead path with cache:\n  1. check cache\n  2. HIT  -> return cached value (fast)\n  3. MISS -> read DB, store in cache, return\n\nCache hit ratio = hits / (hits + misses)\n  90 percent hit ratio => only 1 in 10 reads touches the DB.\n```\n\n```mermaid\ngraph LR\n    A["Request"] --> B{"In cache"}\n    B -->|"hit"| C["Return cached"]\n    B -->|"miss"| D["Read database"]\n    D --> E["Store in cache"]\n    E --> C\n```\n\nInterview tip: add a cache to cut read latency and DB load, then immediately\naddress invalidation (TTL or write-through) so nobody asks "what about stale\ndata".\n',
        ),
        quiz_lesson(
            "Quiz: Caching and CDNs",
            (
                q(
                    "What is the main purpose of a cache?",
                    (
                        opt(
                            "Store expensive results close by so repeat requests are fast and the DB is offloaded",
                            correct=True,
                        ),
                        opt("Permanently store the only copy of data"),
                        opt("Encrypt network traffic"),
                    ),
                ),
                q(
                    "A CDN specifically caches:",
                    (
                        opt("Static assets at edge locations near users", correct=True),
                        opt("The primary write-ahead log"),
                        opt("Nothing; it only routes DNS"),
                    ),
                ),
                q(
                    "The classic hard problem with caching is:",
                    (
                        opt("Invalidation - keeping cached data from going stale", correct=True),
                        opt("Running out of CPU cores"),
                        opt("Choosing a font"),
                    ),
                ),
            ),
        ),
        _t(
            "Databases: SQL, NoSQL, replication and sharding",
            "12 min",
            '# Databases: SQL, NoSQL, replication and sharding\n\nThe data store is usually the hardest part to scale. Two broad families:\n\n- **SQL (relational)** - tables with a fixed schema, strong consistency, and joins. Great when data is structured and you need transactions (ACID). Examples: PostgreSQL, MySQL.\n- **NoSQL** - flexible schema, built to scale horizontally. Types include key-value, document, wide-column, and graph. Great for huge scale and simple access patterns. Examples: DynamoDB, MongoDB, Cassandra.\n\nTwo techniques scale a database:\n\n- **Replication** - copy data to multiple nodes. A **primary** takes writes; **replicas** serve reads. Improves read throughput and availability.\n- **Sharding (partitioning)** - split the data across nodes by a **shard key** (for example user id) so each node holds a slice. Improves write throughput and storage, but cross-shard queries get harder.\n\n```text\nReplication:  writes -> primary -> replicated to replica1, replica2 (reads)\nSharding:     users A-M -> shard 1 ; users N-Z -> shard 2\n  Pick a shard key with even distribution to avoid a "hot" shard.\n```\n\n```mermaid\ngraph TD\n    W["Writes"] --> P["Primary"]\n    P --> R1["Replica 1 reads"]\n    P --> R2["Replica 2 reads"]\n    APP["App"] --> SK{"Shard key"}\n    SK --> S1["Shard 1"]\n    SK --> S2["Shard 2"]\n```\n\nInterview tip: choose SQL vs NoSQL from the access pattern and consistency\nneeds, then scale reads with replication and writes with sharding.\n',
        ),
        quiz_lesson(
            "Quiz: Databases: SQL, NoSQL, replication and sharding",
            (
                q(
                    "When is a relational (SQL) database the natural choice?",
                    (
                        opt(
                            "Structured data needing transactions and joins with strong consistency",
                            correct=True,
                        ),
                        opt("Whenever you want the most nodes possible"),
                        opt("Only for images and video"),
                    ),
                ),
                q(
                    "What does replication improve most directly?",
                    (
                        opt("Read throughput and availability", correct=True),
                        opt("Write throughput via splitting data"),
                        opt("Font rendering"),
                    ),
                    "Replicas serve reads; sharding splits writes/storage.",
                ),
                q(
                    "Sharding splits data across nodes by a:",
                    (
                        opt("Shard key chosen for even distribution", correct=True),
                        opt("Random cache eviction policy"),
                        opt("Load balancer health check"),
                    ),
                ),
            ),
        ),
        _t(
            "Consistency and the CAP theorem",
            "10 min",
            '# Consistency and the CAP theorem\n\nWhen data lives on many nodes, they can disagree. The **CAP theorem** says that\nduring a **network partition** (P) a distributed system must choose between:\n\n- **Consistency (C)** - every read sees the latest write (or an error).\n- **Availability (A)** - every request gets a non-error response, even if possibly stale.\n\nSince partitions **will** happen, the real choice is **CP** (refuse or block to\nstay correct) vs **AP** (stay up, allow temporary staleness).\n\nRelated idea: **strong** vs **eventual** consistency.\n\n- **Strong** - after a write, all reads see it immediately. Needed for balances, inventory, bookings.\n- **Eventual** - replicas converge "soon". Fine for likes, view counts, feeds - and it is what lets systems stay highly available.\n\n```text\nBank balance      -> strong consistency (CP-leaning): never show wrong money\nSocial feed likes -> eventual consistency (AP-leaning): a stale count is fine\n```\n\n```mermaid\ngraph TD\n    P{"Network partition"} -->|"choose C"| CP["Consistent, may reject requests"]\n    P -->|"choose A"| AP["Available, may be stale"]\n```\n\nInterview tip: state which of consistency or availability the feature needs,\nthen justify CP vs AP - this is one of the most common follow-up questions.\n',
        ),
        quiz_lesson(
            "Quiz: Consistency and the CAP theorem",
            (
                q(
                    "During a network partition, CAP says you must trade off between:",
                    (
                        opt("Consistency and availability", correct=True),
                        opt("Latency and font size"),
                        opt("CPU and RAM"),
                    ),
                ),
                q(
                    "Which feature most needs STRONG consistency?",
                    (
                        opt("An account balance or inventory count", correct=True),
                        opt("A social media like counter"),
                        opt("A 'trending' list"),
                    ),
                ),
                q(
                    "Eventual consistency means:",
                    (
                        opt(
                            "Replicas converge to the same value soon, tolerating brief staleness",
                            correct=True,
                        ),
                        opt("Data is never consistent"),
                        opt("Every read always blocks until all nodes agree"),
                    ),
                ),
            ),
        ),
        _t(
            "APIs, message queues and designing a system end to end",
            "12 min",
            '# APIs, message queues and designing a system end to end\n\nServices talk to each other and to clients through **APIs** and, when work\nshould happen asynchronously, through **message queues**.\n\n- **Synchronous API (REST / gRPC)** - the client calls and waits for a response. Simple, direct, good for reads and quick actions.\n- **Asynchronous messaging (queues)** - the producer drops a message on a queue (for example Kafka, RabbitMQ, SQS) and a consumer processes it later. Decouples services, absorbs spikes, and smooths load.\n\nUse a queue when work is slow, spiky, or can be retried: sending emails,\nencoding video, processing uploads.\n\n**Putting it together - a worked example: a URL shortener.**\n\n```text\nPOST /shorten {url}   -> return short code\nGET  /{code}          -> 301 redirect to long url\n\nFlow:\n  client -> load balancer -> app servers (stateless)\n  write:  app -> generate code -> store {code, url} in DB\n  read:   app -> check cache -> DB on miss -> redirect\n  scale:  cache hot codes; shard the DB by code; replicate for reads\n```\n\n```mermaid\ngraph LR\n    C["Client"] --> LB["Load balancer"]\n    LB --> APP["App servers"]\n    APP --> CA["Cache"]\n    APP --> DB["Database"]\n    APP --> MQ["Message queue"]\n    MQ --> WK["Workers"]\n```\n\nInterview tip: end every design by walking the read path and the write path,\nthen say where you would add a cache, a queue, replication, and sharding.\n',
        ),
        quiz_lesson(
            "Quiz: APIs, message queues and designing a system end to end",
            (
                q(
                    "When is an asynchronous message queue the right tool?",
                    (
                        opt(
                            "For slow, spiky, or retryable work that can happen later", correct=True
                        ),
                        opt("For every read that needs an instant answer"),
                        opt("To replace the database entirely"),
                    ),
                ),
                q(
                    "A message queue helps a system by:",
                    (
                        opt("Decoupling services and absorbing traffic spikes", correct=True),
                        opt("Guaranteeing strong consistency for free"),
                        opt("Removing the need for any servers"),
                    ),
                ),
                q(
                    "A good way to CLOSE a system design answer is to:",
                    (
                        opt(
                            "Walk the read path and write path and point out cache, queue, replication, sharding",
                            correct=True,
                        ),
                        opt("List every programming language you know"),
                        opt("Refuse to discuss trade-offs"),
                    ),
                ),
            ),
        ),
        video_lesson(
            "Video: System design crash course and interview prep",
            "https://www.youtube.com/watch?v=F2FmTdLtb_4",
            duration="54 min",
            body="## Summary\n\nThis crash course walks through the system design concepts you need for a system design interview, where the goal is not to write code but to explain how you glue an entire system together. It opens with the high level architecture of a single computer, explaining how data is measured in bits and bytes and how it flows through layers of increasing speed: nonvolatile disk storage (HDD or SSD) holds the OS and files, volatile RAM holds data currently in use, the even faster L1, L2, and L3 caches sit closest to the CPU, and the CPU fetches, decodes, and executes machine code that a compiler produced from high level languages. It then sketches a production app: a CI/CD pipeline, load balancers and reverse proxies distributing traffic, external storage and services, plus logging, monitoring, alerting, and a staging-first debugging workflow.\n\nThe video defines what makes a good design, centering on scalability, maintainability, and efficiency while planning for failure. It frames system design around three activities: moving data, storing data, and transforming data. It introduces the CAP theorem (Brewer's theorem), which says a distributed system can only guarantee two of consistency, availability, and partition tolerance at once, so every decision is a tradeoff for a specific use case. It quantifies reliability through availability percentages (the golden five nines), SLOs and SLAs, fault tolerance, redundancy, and the speed metrics throughput (requests, queries, or bytes per unit time) and latency.\n\nNetworking basics follow: IPv4 versus IPv6 addressing, packets with IP headers, the reliable connection-oriented TCP versus the faster connectionless UDP, DNS translating domain names into IP addresses, ports, firewalls, and public versus private and static versus dynamic addresses. The course then surveys application layer protocols including HTTP with its status code series and methods, WebSockets for two-way real time updates, SMTP, IMAP, POP3, FTP, SSH, WebRTC, MQTT, AMQP, and RPC. API design covers CRUD over REST, GraphQL, and gRPC, plus idempotency, versioning for backward compatibility, rate limiting, and CORS.\n\nTo cut latency for distant users, the video explains caching at the browser, server, and database levels, cache hits and misses, cache control headers, write-around, write-through, and write-back strategies, and eviction policies like LRU and FIFO. Content delivery networks distribute static content geographically using pull-based or push-based approaches. Proxy servers are covered, distinguishing forward proxies (hiding the client) from reverse proxies (hiding the servers), and load balancing algorithms such as round robin, least connections, least response time, IP hashing, weighted variants, geographical, and consistent hashing, along with health checks and redundant failover.\n\nFinally it dives into databases: relational SQL databases that are ACID compliant (atomicity, consistency, isolation, durability) versus schema-less NoSQL databases that relax consistency, plus in-memory stores like Redis. Scaling options are vertical (a bigger single machine, which has a hard limit) and horizontal (more machines via sharding or replication). It closes on performance techniques (caching, indexing, query optimization) and reminds you that the CAP theorem still governs which two properties to prioritize based on the interview requirements.\n\n## Main ideas\n\n- **Memory hierarchy**: Data moves from slow nonvolatile disk to volatile RAM to faster caches to the CPU, trading capacity for speed.\n- **Three activities**: System design boils down to moving data, storing data, and transforming data.\n- **CAP theorem**: A distributed system can guarantee only two of consistency, availability, and partition tolerance at once.\n- **Availability**: Measured in nines, where 99.999 percent allows about 5 minutes of downtime per year and 99.9 percent allows about 8.76 hours.\n- **Throughput vs latency**: Throughput is how much work per unit time; latency is how long one request takes, and optimizing one can hurt the other.\n- **TCP vs UDP**: TCP is reliable and connection-oriented with a three-way handshake; UDP is faster and connectionless, good for video calls and streaming.\n- **Caching and CDNs**: Caches at browser, server, and database levels plus geographically distributed CDNs reduce latency and server load.\n- **Load balancing**: Algorithms like round robin, least connections, IP hashing, and consistent hashing spread traffic, backed by health checks and failover.\n- **SQL vs NoSQL**: SQL databases are ACID compliant and structured; NoSQL databases are schema-less, flexible, and relax the consistency property.\n\n## Mindmap\n\n```mermaid\nmindmap\n  root((System Design Concepts))\n    Computer Architecture\n      Disk RAM cache CPU\n      Compiler to machine code\n    Scalability\n      Vertical scaling up\n      Horizontal scaling out\n    Reliability\n      Availability five nines\n      Fault tolerance redundancy\n    Networking\n      IP TCP UDP DNS\n      HTTP and WebSockets\n    Caching and CDN\n      Browser server database caches\n      Content delivery networks\n    Load Balancing\n      Round robin\n      Least connections hashing\n    Databases\n      SQL and NoSQL\n      Sharding and replication\n    CAP Theorem\n      Consistency and availability\n      Partition tolerance\n```",
        ),
        quiz_lesson(
            "Quiz: Video: System design crash course and interview prep",
            (
                q(
                    "According to the CAP theorem as explained in the video, how many of its three properties can a distributed system guarantee at the same time?",
                    (
                        opt("Only two of the three", correct=True),
                        opt("All three simultaneously"),
                        opt("Only one at a time"),
                        opt("None can be guaranteed"),
                    ),
                    "The video states that under the CAP (Brewer's) theorem, a distributed system can only achieve two of consistency, availability, and partition tolerance at once, so you must prioritize two based on the use case.",
                ),
                q(
                    "The video contrasts TCP and UDP at the transport layer. Which statement matches its explanation of UDP?",
                    (
                        opt(
                            "It is faster but less reliable and does not establish a connection first",
                            correct=True,
                        ),
                        opt("It guarantees delivery and ordering using sequence numbers"),
                        opt("It uses a three-way handshake before sending data"),
                        opt("It is preferred when no data loss is acceptable"),
                    ),
                    "The video describes UDP as faster but less reliable than TCP because it does not establish a connection or guarantee delivery or order, making it suitable for time sensitive uses like video calls and live streaming.",
                ),
                q(
                    "How does the video distinguish relational SQL databases from NoSQL databases regarding the ACID properties?",
                    (
                        opt(
                            "SQL databases are ACID compliant while NoSQL databases drop the consistency property",
                            correct=True,
                        ),
                        opt("NoSQL databases are fully ACID compliant while SQL databases are not"),
                        opt("Both are schema-less and drop durability"),
                        opt("SQL databases drop atomicity to gain speed"),
                    ),
                    "The video explains that relational SQL databases are ACID compliant (atomicity, consistency, isolation, durability), whereas NoSQL databases are schema-less and drop the consistency property from ACID.",
                ),
            ),
        ),
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "The system design interview primarily tests:",
                    (
                        opt("How you reason about architecture and trade-offs", correct=True),
                        opt("Typing speed"),
                        opt("Memorized algorithms"),
                    ),
                ),
                q(
                    "Horizontal scaling means:",
                    (
                        opt("Adding more machines behind a load balancer", correct=True),
                        opt("Adding RAM to one machine"),
                        opt("Deleting data"),
                    ),
                ),
                q(
                    "99.99 percent availability is roughly how much downtime per year?",
                    (
                        opt("About 52 minutes", correct=True),
                        opt("About 3.65 days"),
                        opt("Zero, guaranteed"),
                    ),
                ),
                q(
                    "Least-connections load balancing routes to:",
                    (
                        opt("The server with the fewest active requests", correct=True),
                        opt("A random server always"),
                        opt("The primary database"),
                    ),
                ),
                q(
                    "A CDN caches:",
                    (
                        opt("Static assets at edge locations near users", correct=True),
                        opt("The write-ahead log"),
                        opt("Nothing"),
                    ),
                ),
                q(
                    "Replication mainly improves:",
                    (
                        opt("Read throughput and availability", correct=True),
                        opt("Write throughput by splitting data"),
                        opt("Cache invalidation"),
                    ),
                ),
                q(
                    "Sharding splits data by a:",
                    (
                        opt("Shard key with even distribution", correct=True),
                        opt("Cache TTL"),
                        opt("Health check"),
                    ),
                ),
                q(
                    "During a partition, an AP system chooses:",
                    (
                        opt("Availability, tolerating temporary staleness", correct=True),
                        opt("Consistency, rejecting requests"),
                        opt("Neither"),
                    ),
                ),
                q(
                    "An account balance needs:",
                    (
                        opt("Strong consistency", correct=True),
                        opt("Eventual consistency"),
                        opt("No database"),
                    ),
                ),
                q(
                    "A message queue is best for:",
                    (
                        opt("Slow, spiky, retryable async work", correct=True),
                        opt("Every instant read"),
                        opt("Replacing the load balancer"),
                    ),
                ),
            ),
        ),
    ),
)

SYSTEM_DESIGN_INTERVIEW_COURSES: tuple[SeedCourse, ...] = (_SYSTEM_DESIGN_INTERVIEW,)
