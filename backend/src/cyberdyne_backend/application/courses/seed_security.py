"""Academy seed content — the Cybersecurity track (Beginner → Advanced).

* ``security-basics``        — CIA triad, authn/authz, classical ciphers, web vulns
* ``security-intermediate``  — modern crypto, OWASP Top 10, auth protocols
* ``security-advanced``      — threat modeling, secure SDLC, TLS 1.3, defense ops

Runnable ``code`` lessons use only Python builtins + numpy (the sandbox blocks
hashlib/secrets/random/etc.), so hands-on labs are classical ciphers, modular
arithmetic, and simulated attacks; real hashing/crypto libraries appear as
read-only ```python blocks.
"""
# Lesson content uses math/security Unicode (⊕, →, ², ·) in strings and labels.
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
# security-basics
# ──────────────────────────────────────────────────────────────────────

_SEC_BASICS = SeedCourse(
    slug="security-basics",
    title="Cybersecurity — Basics",
    description=(
        "How to think about security: the CIA triad and threat models, the "
        "difference between encoding, encryption and hashing, the classic web "
        "vulnerabilities, and hands-on classical ciphers you'll build — and "
        "break — in code."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What security means: the CIA triad",
            "9 min",
            r"""# What security means

Security isn't one thing — it's three goals, the **CIA triad**:

- **Confidentiality** — only authorised parties can read the data (encryption,
  access control).
- **Integrity** — data can't be altered undetected (hashes, signatures).
- **Availability** — the system is there when you need it (redundancy,
  DoS protection).

Every control you'll meet maps to one or more of these. A ransomware attack
breaks confidentiality *and* availability; a tampered software update breaks
integrity.

## Think like an attacker: threat modeling

You can't secure everything equally, so you reason about **what** you're
protecting, **from whom**, and **how** they'd attack:

- **Assets** — what's valuable (user data, money, uptime, reputation)?
- **Adversaries** — script kiddies, criminals, insiders, nation states — each
  with different skill and motivation.
- **Attack surface** — every input, endpoint, dependency, and human is a way in.
- **Trust boundaries** — where data crosses from less- to more-trusted (the
  network edge, a process boundary). Most bugs live there.

The mindset that matters: **never trust input**, assume breach, and **defense
in depth** — layers, so one failure isn't game over.
""",
        ),
        _t(
            "Authentication vs authorization",
            "8 min",
            r"""# Authentication vs authorization

Two words people constantly confuse:

- **Authentication (authn)** — *who are you?* Proving identity.
- **Authorization (authz)** — *what may you do?* Granting permissions.

You authenticate **once**; you're authorized on **every** action.

## Factors of authentication

- **Something you know** — password, PIN.
- **Something you have** — phone, hardware key (TOTP, FIDO2).
- **Something you are** — fingerprint, face.

Combining two of different kinds is **multi-factor authentication (MFA)** — the
single highest-leverage control against account takeover, because a stolen
password alone is no longer enough.

## Authorization models

- **RBAC** (role-based) — permissions attached to roles (admin, editor, viewer).
- **ABAC** (attribute-based) — decisions from attributes (department, time,
  resource owner).

The cardinal rule is **least privilege**: every user, service, and token gets
the *minimum* access it needs, for the *shortest* time. Over-broad permissions
turn a small breach into a catastrophic one.
""",
        ),
        _code(
            "Build a Caesar & XOR cipher",
            "12 min",
            r"""# Two classical ciphers, from scratch. Press Run, then change the message/key.
# (Educational only — these are trivially breakable; never use them for real.)

# --- Caesar cipher: shift each letter by k positions ---
def caesar(text, k):
    out = ""
    for ch in text:
        if "a" <= ch <= "z":
            out += chr((ord(ch) - ord("a") + k) % 26 + ord("a"))
        elif "A" <= ch <= "Z":
            out += chr((ord(ch) - ord("A") + k) % 26 + ord("A"))
        else:
            out += ch
    return out

msg = "Attack at dawn"
enc = caesar(msg, 3)
print("Caesar  plain :", msg)
print("Caesar  cipher:", enc)
print("Caesar  back  :", caesar(enc, -3))   # decrypt = shift the other way

# --- XOR cipher: combine each byte with a repeating key (⊕ = exclusive or) ---
def xor_cipher(text, key):
    out = []
    for i in range(len(text)):
        out.append(ord(text[i]) ^ ord(key[i % len(key)]))
    return out

secret = xor_cipher("hello", "k")          # list of XORed codepoints
back = "".join(chr(c ^ ord("k")) for c in secret)
print("XOR     cipher:", secret)
print("XOR     back  :", back)
# Key insight: XOR is its own inverse — applying the same key twice restores the text.
""",
        ),
        _t(
            "Encoding vs encryption vs hashing",
            "10 min",
            r"""# Encoding vs encryption vs hashing

Three things that look similar and are constantly mixed up:

| | Reversible? | Needs a key? | Purpose |
|---|---|---|---|
| **Encoding** (Base64, URL) | yes, by anyone | no | safe transport of bytes |
| **Encryption** | yes, *with the key* | yes | confidentiality |
| **Hashing** (SHA-256) | **no** | no | integrity, fingerprints |

**Base64 is not security** — it's just bytes-to-text. Anyone can decode it.

**Hashing** is one-way: easy to compute, infeasible to invert, and a tiny input
change flips ~half the output bits (the *avalanche* effect). It's how we store
passwords (as salted hashes, never plaintext) and verify file integrity.

Why brute force fails against a good key: the **keyspace** doubles with every
bit. At $2^{128}$ keys, even a billion-guesses-per-second machine would take far
longer than the age of the universe:

```plot
{"title": "Keyspace = 2^bits grows exponentially", "xLabel": "key length (bits)", "yLabel": "possible keys", "xRange": [0, 20], "yRange": [0, 1100000], "functions": [{"expr": "2^x", "label": "2^bits", "color": "#dc2626"}]}
```

That's why "long random key" beats "clever secret algorithm" — security rests on
the **key**, not on hiding the method (Kerckhoffs's principle).
""",
        ),
        _t(
            "The web's classic vulnerabilities",
            "11 min",
            r"""# The web's classic vulnerabilities

Almost all of them share one root cause: **untrusted input treated as trusted
code or commands.**

- **Injection (SQL, command, LDAP)** — user input is concatenated into a query
  or shell command and changes its meaning. `'; DROP TABLE users;--` is the
  cliché. Fix: **parameterised queries** — data never becomes code.
- **Cross-Site Scripting (XSS)** — attacker input is rendered as HTML/JS in
  another user's browser, stealing sessions or defacing pages. Fix: **escape
  output** by context; use a strict Content-Security-Policy.
- **Cross-Site Request Forgery (CSRF)** — a malicious site makes the victim's
  browser send an authenticated request to yours. Fix: **anti-CSRF tokens**,
  SameSite cookies.
- **Broken authentication / session management** — weak passwords, leaked
  tokens, sessions that never expire.
- **Insecure direct object references** — `/invoice?id=124` lets you read
  `id=125`. Fix: **authorize every access**, don't trust the id.

The unifying defenses: **validate input, escape output, parameterise queries,
authorize every action, and never trust the client.** You'll simulate an
injection in the Intermediate course.
""",
        ),
        _code(
            "Break a Caesar cipher (frequency analysis)",
            "12 min",
            r"""# Crack a Caesar cipher WITHOUT the key — by counting letters.
# English text is ~12.7% 'e' and has lots of spaces; the right shift reveals them.

def caesar(text, k):
    out = ""
    for ch in text:
        if "a" <= ch <= "z":
            out += chr((ord(ch) - ord("a") + k) % 26 + ord("a"))
        elif "A" <= ch <= "Z":
            out += chr((ord(ch) - ord("A") + k) % 26 + ord("A"))
        else:
            out += ch
    return out

intercepted = caesar("the quick brown fox jumps over the lazy dog", 7)
print("intercepted:", intercepted)

# Try all 26 shifts; score each by how many letters land on common English
# letters (e, t, a, o, ...). The real shift scores highest.
best_k, best_score, best_text = 0, -1, ""
for k in range(26):
    candidate = caesar(intercepted, -k)
    score = 0
    for ch in candidate:
        if ch in "etaoinshr":
            score = score + 1
    if score > best_score:
        best_k, best_score, best_text = k, score, candidate

print("recovered shift:", best_k)
print("recovered text :", best_text)
# Lesson: short keys + known language statistics = no security at all.
""",
        ),
        _t(
            "Securing data in transit: TLS & certificates",
            "9 min",
            r"""# Securing data in transit: TLS

When your browser shows the padlock, **TLS** (Transport Layer Security, the "S"
in HTTPS) is doing three jobs at once:

1. **Confidentiality** — the connection is encrypted, so eavesdroppers see
   gibberish.
2. **Integrity** — tampering in flight is detected.
3. **Authentication** — you're really talking to the site you think you are.

That third job relies on **certificates**. A site presents a certificate signed
by a **Certificate Authority (CA)** your device trusts. The cert binds the
domain name to a **public key**; your browser verifies the signature chain up to
a trusted root. If it doesn't check out (expired, wrong domain, untrusted
issuer), you get the scary warning.

The handshake then uses **asymmetric crypto** to agree on a fresh **symmetric**
session key (fast for bulk data) — you'll see the why in the next course.

Practical takeaways: serve **everything** over HTTPS, redirect HTTP→HTTPS, use
**HSTS**, keep certificates auto-renewed (Let's Encrypt), and never ship an app
that ignores certificate errors.
""",
        ),
        _t(
            "Everyday secure practices",
            "8 min",
            r"""# Everyday secure practices

Most breaches don't need exotic exploits — they walk through unlocked doors.
The habits that prevent the majority of incidents:

- **Patch.** Most exploited vulnerabilities have a fix available; attackers scan
  for the unpatched. Automate updates.
- **Manage secrets properly.** Never hard-code API keys or passwords; never
  commit them to git. Use a secrets manager and **rotate** them.
- **Least privilege everywhere.** Scope tokens, database users, and cloud IAM
  roles to exactly what's needed.
- **MFA on everything** that supports it — especially email, which is the reset
  path for everything else.
- **Encrypt at rest and in transit.** Disk encryption + TLS.
- **Log and monitor.** You can't respond to what you can't see; keep audit
  trails of auth and admin actions.
- **Back up — and test restores.** A backup you've never restored isn't a backup.
- **Assume breach.** Segment networks and design so one compromised component
  can't reach everything.

Security is a process, not a product: small consistent hygiene beats a single
expensive tool.
""",
        ),
        quiz_lesson(
            "Quiz: Security Basics",
            (
                q(
                    "What are the three goals of the CIA triad?",
                    (
                        opt("Confidentiality, Integrity, Availability", correct=True),
                        opt("Cryptography, Identity, Access"),
                        opt("Control, Inspection, Auditing"),
                        opt("Confidentiality, Isolation, Authentication"),
                    ),
                    "CIA = Confidentiality, Integrity, Availability — the goals every control maps to.",
                ),
                q(
                    "What is the difference between authentication and authorization?",
                    (
                        opt(
                            "Authn proves who you are; authz decides what you may do", correct=True
                        ),
                        opt("They are two words for the same thing"),
                        opt("Authn is for admins, authz is for users"),
                        opt("Authz happens first, then authn"),
                    ),
                    "You authenticate once (identity) and are authorized per action (permissions).",
                ),
                q(
                    "Why is Base64 not a form of security?",
                    (
                        opt(
                            "It's reversible encoding anyone can decode — no key involved",
                            correct=True,
                        ),
                        opt("It's a strong but slow cipher"),
                        opt("It hashes data one-way"),
                        opt("It requires a certificate"),
                    ),
                    "Encoding just changes representation; encryption needs a key, hashing is one-way.",
                ),
                q(
                    "The XOR cipher restores plaintext when you apply the key twice because…",
                    (
                        opt("XOR is its own inverse: a ⊕ k ⊕ k = a", correct=True),
                        opt("XOR sorts the bytes"),
                        opt("XOR is a one-way hash"),
                        opt("XOR doubles the key length"),
                    ),
                    "XORing with the same key twice cancels out, recovering the original bytes.",
                ),
                q(
                    "What is the root cause shared by SQL injection, XSS, and command injection?",
                    (
                        opt("Untrusted input is treated as trusted code/commands", correct=True),
                        opt("Weak encryption keys"),
                        opt("Expired TLS certificates"),
                        opt("Too much logging"),
                    ),
                    "All are injection: data crosses into a code/command context. Parameterise and escape.",
                ),
                q(
                    "What does a TLS certificate let your browser verify?",
                    (
                        opt(
                            "That the site's public key is bound to its domain by a trusted CA",
                            correct=True,
                        ),
                        opt("That the site has no bugs"),
                        opt("That the password is strong"),
                        opt("That the server is fast"),
                    ),
                    "The CA-signed cert authenticates the server's identity; the browser checks the chain to a trusted root.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# security-intermediate
# ──────────────────────────────────────────────────────────────────────

_SEC_INTERMEDIATE = SeedCourse(
    slug="security-intermediate",
    title="Cybersecurity — Intermediate",
    description=(
        "Modern cryptography you can reason about: symmetric vs asymmetric, key "
        "exchange, signatures and PKI; password storage done right; the OWASP "
        "Top 10 in depth; and the auth protocols (OAuth2, JWT) behind real apps."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Symmetric vs asymmetric cryptography",
            "11 min",
            r"""# Symmetric vs asymmetric cryptography

Two families, used together in practice.

**Symmetric** — one shared secret key encrypts and decrypts (AES is the
standard). Fast, great for bulk data. The hard part is **getting the key to the
other party** without anyone intercepting it.

**Asymmetric (public-key)** — a **key pair**: a *public* key anyone can have, and
a *private* key you guard. What one encrypts, only the other decrypts (RSA,
elliptic-curve). Slow, but it solves key distribution: publish your public key
freely.

**The hybrid everyone uses** (e.g. TLS): asymmetric crypto to agree on a fresh
symmetric **session key**, then fast symmetric crypto for the actual data. Best
of both.

Security scales with **key length**, exponentially — adding bits multiplies the
attacker's work:

```plot
{"title": "Attacker effort doubles per key bit", "xLabel": "extra key bits", "yLabel": "relative work", "xRange": [0, 16], "yRange": [0, 70000], "functions": [{"expr": "2^x", "label": "work = 2^bits", "color": "#dc2626"}]}
```

Symmetric and asymmetric key sizes aren't comparable bit-for-bit: AES-128 is
roughly as strong as RSA-3072, because attacks on each scale differently.
""",
        ),
        _t(
            "Hashing, salts & password storage",
            "10 min",
            r"""# Hashing, salts & password storage

**Never store passwords** — store a one-way hash, and even that needs care.

A plain `sha256(password)` is **not enough**: attackers precompute hashes of
common passwords (**rainbow tables**) and look yours up. Two fixes:

- **Salt** — a unique random value stored alongside each hash. Now identical
  passwords get different hashes, and a single rainbow table can't cover everyone.
- **Slow, memory-hard hashing** — use **bcrypt**, **scrypt**, or **Argon2**, not
  raw SHA. They're deliberately expensive (tunable work factor) so brute-forcing
  billions of guesses becomes infeasible even with GPUs.

```python
# Read-only (hashlib/bcrypt aren't in the sandbox) — the real pattern:
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# verify later:
bcrypt.checkpw(attempt.encode(), hashed)   # constant-time compare inside
```

**HMAC** (`HMAC(key, message)`) is the keyed cousin of hashing — it proves a
message came from someone who holds the key and wasn't tampered with (message
authentication). It's what signs JWTs and API requests.

Rule of thumb: **hash + unique salt + a slow KDF (Argon2/bcrypt)**, and compare
in constant time. Never invent your own.
""",
        ),
        _code(
            "Diffie–Hellman key exchange (toy)",
            "13 min",
            r"""# How two people agree on a shared secret over a public channel —
# without ever sending the secret. Uses modular exponentiation: pow(base, exp, mod).
# (Tiny numbers for clarity; real DH uses 2048+ bit primes.)

p = 23      # public prime modulus
g = 5       # public generator

# Private keys (never shared):
a_private = 6      # Alice
b_private = 15     # Bob

# Public keys (shared openly) = g^private mod p
a_public = pow(g, a_private, p)
b_public = pow(g, b_private, p)
print("Alice sends:", a_public)
print("Bob sends  :", b_public)

# Each raises the OTHER's public key to their own private key:
alice_shared = pow(b_public, a_private, p)
bob_shared = pow(a_public, b_private, p)
print("Alice computes secret:", alice_shared)
print("Bob   computes secret:", bob_shared)
print("secrets match:", alice_shared == bob_shared)

# An eavesdropper sees p, g, a_public, b_public — but recovering the secret
# requires the discrete log (find 'a' from g^a mod p), which is hard for big p.
print("eavesdropper would need to solve g^a mod p =", a_public, "for a")
""",
        ),
        _t(
            "Digital signatures & PKI",
            "9 min",
            r"""# Digital signatures & PKI

Encryption hides *content*; **signatures** prove *origin and integrity*.

To sign, you hash the message and encrypt the hash with your **private** key.
Anyone with your **public** key can decrypt it and check it matches the
message's hash. If it does, the message (a) came from you and (b) wasn't
altered. This gives **authenticity**, **integrity**, and **non-repudiation**
(you can't deny signing).

But how do you trust that a public key really belongs to who it claims? That's
**Public Key Infrastructure (PKI)**:

- A **Certificate Authority (CA)** signs certificates binding a public key to an
  identity (a domain, a person).
- Your device ships with a set of **trusted root CAs**.
- A certificate chains from the server up to a trusted root; each link is a
  signature you can verify.

This is the backbone of HTTPS, code signing, signed software updates, and
secure email. Its weak point is **trust**: a compromised or coerced CA can mint
fraudulent certificates — which is why **certificate transparency** logs and
pinning exist.
""",
        ),
        _t(
            "The OWASP Top 10",
            "11 min",
            r"""# The OWASP Top 10

The industry's consensus list of the most critical web risks. Know these by
name — interviewers and auditors expect it:

1. **Broken Access Control** — users act outside their permissions (the #1 risk).
   Enforce authz server-side, deny by default.
2. **Cryptographic Failures** — weak/missing encryption, secrets in transit or
   at rest. Use strong, current algorithms; protect keys.
3. **Injection** — SQL/NoSQL/command/LDAP. Parameterise; validate.
4. **Insecure Design** — flaws baked in before a line of code. Threat-model early.
5. **Security Misconfiguration** — default creds, verbose errors, open buckets.
6. **Vulnerable & Outdated Components** — that unpatched dependency. Scan and
   update (SCA tools).
7. **Identification & Authentication Failures** — weak passwords, broken
   sessions, no MFA.
8. **Software & Data Integrity Failures** — unsigned updates, insecure CI/CD,
   untrusted deserialization.
9. **Security Logging & Monitoring Failures** — you can't detect or investigate
   what you don't log.
10. **Server-Side Request Forgery (SSRF)** — the server is tricked into making
    requests to internal systems.

Notice how many are **design and configuration**, not exotic exploits — secure
defaults and reviews prevent most of them.
""",
        ),
        _code(
            "SQL injection: why parameterisation matters",
            "11 min",
            r"""# Simulate how string-concatenated queries get hijacked — and how
# parameterised queries stop it. (No real DB; we just build the query string.)

def vulnerable_query(username):
    # DANGER: user input concatenated straight into SQL.
    return "SELECT * FROM users WHERE name = '" + username + "'"

def safe_query(username):
    # The query template is fixed; the value is bound separately (shown as ?).
    template = "SELECT * FROM users WHERE name = ?"
    return template, (username,)

# A normal user:
print("normal  :", vulnerable_query("alice"))

# An attacker's input ends the string and appends 'OR 1=1' (always true) +
# a comment (--) to swallow the rest:
attack = "x' OR '1'='1"
print("attacked:", vulnerable_query(attack))
print("  -> the WHERE clause is now always true: the attacker dumps every row!")

# Parameterised: the input can NEVER change the query's structure.
tmpl, params = safe_query(attack)
print("safe    :", tmpl, "with bound params", params)
print("  -> the malicious text is treated as a literal name, matching nothing.")
""",
        ),
        _t(
            "Auth protocols: sessions, OAuth2 & JWT",
            "10 min",
            r"""# Auth protocols: sessions, OAuth2 & JWT

**Sessions (stateful).** After login the server creates a session, stores it,
and hands the browser a random **session id** cookie. Every request sends the
cookie; the server looks it up. Simple, easy to revoke (delete the session).

**JWT (stateless).** A **JSON Web Token** is a signed token the client carries —
`header.payload.signature`. The server verifies the signature (HMAC or public
key) without a lookup, reading claims (user id, expiry, scopes) straight from
the payload. Scales horizontally, but **hard to revoke** before expiry, so keep
lifetimes short and pair with refresh tokens. The payload is only **Base64, not
encrypted** — never put secrets in it.

**OAuth2 / OpenID Connect.** *Delegated* authorization — "Log in with Google."
Your app never sees the user's Google password; instead Google issues a scoped
**access token** after the user consents. OIDC adds an **id token** (a JWT) for
authentication on top.

Pitfalls: store tokens safely (HttpOnly/SameSite cookies beat localStorage for
web), validate **every** token's signature, issuer, audience and expiry, and
always use **short-lived** access tokens with refresh.
""",
        ),
        quiz_lesson(
            "Quiz: Applied Cryptography & Web Security",
            (
                q(
                    "Why does TLS use both asymmetric and symmetric crypto?",
                    (
                        opt(
                            "Asymmetric to exchange a key safely, then fast symmetric crypto for the data",
                            correct=True,
                        ),
                        opt("Asymmetric is used for everything because it's faster"),
                        opt("Symmetric authenticates the server"),
                        opt("To avoid needing certificates"),
                    ),
                    "The hybrid scheme solves key distribution (asymmetric) then encrypts bulk data quickly (symmetric).",
                ),
                q(
                    "What does a salt protect against?",
                    (
                        opt(
                            "Precomputed rainbow-table lookups and identical-password collisions",
                            correct=True,
                        ),
                        opt("Network eavesdropping"),
                        opt("Expired certificates"),
                        opt("Cross-site scripting"),
                    ),
                    "A unique per-password salt makes precomputed tables useless and de-duplicates equal passwords.",
                ),
                q(
                    "In Diffie–Hellman, what does an eavesdropper who sees g, p and both public keys still lack?",
                    (
                        opt(
                            "The shared secret — recovering it requires the hard discrete-log problem",
                            correct=True,
                        ),
                        opt("The prime modulus p"),
                        opt("The generator g"),
                        opt("The public keys"),
                    ),
                    "The public values are safe to share; deriving a private exponent (discrete log) is computationally hard.",
                ),
                q(
                    "How does a digital signature prove a message wasn't altered?",
                    (
                        opt(
                            "The signer encrypts the message hash with their private key; verifiers check it against the message",
                            correct=True,
                        ),
                        opt("It encrypts the whole message with a shared key"),
                        opt("It Base64-encodes the message"),
                        opt("It stores the message in a database"),
                    ),
                    "Verifying the signature against the recomputed hash confirms origin and integrity.",
                ),
                q(
                    "Why does a parameterised query stop SQL injection?",
                    (
                        opt(
                            "Input is bound as a value and can never change the query's structure",
                            correct=True,
                        ),
                        opt("It encrypts the user input"),
                        opt("It hashes the database"),
                        opt("It runs the query twice"),
                    ),
                    "With bound parameters, malicious text is treated as data, not executable SQL.",
                ),
                q(
                    "What's a key caveat of a JWT's payload?",
                    (
                        opt(
                            "It's only Base64-encoded (signed, not encrypted) — never put secrets in it",
                            correct=True,
                        ),
                        opt("It is fully encrypted and safe for secrets"),
                        opt("It can never expire"),
                        opt("It must be stored server-side"),
                    ),
                    "JWT claims are readable by anyone; the signature guarantees integrity, not confidentiality.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# security-advanced
# ──────────────────────────────────────────────────────────────────────

_SEC_ADVANCED = SeedCourse(
    slug="security-advanced",
    title="Cybersecurity — Advanced",
    description=(
        "Building and defending secure systems: STRIDE threat modeling, memory "
        "safety and side channels, TLS 1.3 and forward secrecy, the secure SDLC "
        "(SAST/DAST/SCA), and detection & response — SIEM, zero trust, cloud and "
        "container security."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Threat modeling with STRIDE",
            "10 min",
            r"""# Threat modeling with STRIDE

Threat modeling is structured paranoia done **at design time**, when fixes are
cheap. **STRIDE** is a checklist of six threat categories — walk each component
and trust boundary and ask "how could this be attacked?":

- **S**poofing — pretending to be someone/something else → *authentication*.
- **T**ampering — altering data or code → *integrity (hashes, signatures)*.
- **R**epudiation — denying an action → *audit logs, signatures*.
- **I**nformation disclosure — leaking data → *encryption, access control*.
- **D**enial of service — exhausting resources → *rate limits, quotas*.
- **E**levation of privilege — gaining unauthorised rights → *least privilege,
  isolation*.

The process: draw a **data-flow diagram**, mark **trust boundaries**, enumerate
threats per element with STRIDE, then decide to **mitigate, eliminate,
transfer, or accept** each. Prioritise by likelihood × impact.

Done early, a one-hour threat model catches design flaws that no amount of later
testing would find — because you can't test your way out of a fundamentally
insecure design.
""",
        ),
        _t(
            "Memory safety & exploitation",
            "10 min",
            r"""# Memory safety & exploitation

A whole class of severe vulnerabilities comes from **unsafe memory handling** in
languages like C/C++:

- **Buffer overflow** — writing past the end of an array overwrites adjacent
  memory, including return addresses — letting an attacker redirect execution
  to their own code.
- **Use-after-free / double-free** — using memory after it's released, leading
  to corruption or control-flow hijacking.
- **Integer overflow** — a size calculation wraps around, under-allocating a
  buffer.

Decades of defenses raised the bar: **stack canaries** (detect overwrites),
**ASLR** (randomise addresses), **DEP/NX** (non-executable data), and modern
exploit mitigations. But the most effective fix is **memory-safe languages**
(Rust, Go, Java, Python) that make whole bug classes impossible — which is why
governments now push memory safety for critical software.

The lesson for builders: prefer memory-safe languages; when you must use C/C++,
use sanitizers (ASan/UBSan), fuzzing, and bounds-checked APIs. Validate every
length and index.
""",
        ),
        _code(
            "Constant-time comparison (avoid timing leaks)",
            "11 min",
            r"""# A naive equality check leaks information through TIMING: it returns early
# on the first mismatch, so an attacker measuring response time learns how many
# leading bytes were correct — and can recover a secret byte-by-byte.

def naive_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False        # early return — timing depends on the data!
    return True

def constant_time_equal(a, b):
    # Always scan the whole input; accumulate differences with XOR.
    if len(a) != len(b):
        return False
    diff = 0
    for i in range(len(a)):
        diff = diff | (ord(a[i]) ^ ord(b[i]))   # 0 only if every byte matched
    return diff == 0

secret = "s3cr3t-token"
print("naive,    correct:", naive_equal(secret, "s3cr3t-token"))
print("naive,    wrong  :", naive_equal(secret, "x3cr3t-token"))
print("const-time correct:", constant_time_equal(secret, "s3cr3t-token"))
print("const-time wrong  :", constant_time_equal(secret, "xxxxxx-xxxxx"))
# Both give the right answer; only the constant-time version takes the SAME time
# regardless of WHERE the mismatch is. Use it for tokens, MACs, and passwords.
""",
        ),
        _t(
            "TLS 1.3 & forward secrecy",
            "9 min",
            r"""# TLS 1.3 & forward secrecy

TLS 1.3 (2018) streamlined and hardened the protocol:

- **Faster handshake** — 1 round-trip (or 0-RTT for resumption) vs 2 before, so
  HTTPS connections set up quicker.
- **Removed legacy cruft** — no more RSA key transport, RC4, MD5, SHA-1,
  static keys; only modern AEAD ciphers (AES-GCM, ChaCha20-Poly1305).
- **Forward secrecy by default** — every session uses an **ephemeral**
  Diffie–Hellman key exchange (ECDHE). The session keys are derived from
  short-lived values and then thrown away.

**Why forward secrecy matters:** even if an attacker records your encrypted
traffic today and *later* steals the server's long-term private key, they
**still can't decrypt past sessions** — the ephemeral keys are gone. Without it,
one key compromise retroactively exposes everything ever recorded ("harvest now,
decrypt later").

Operationally: keep TLS libraries current, disable old versions (TLS ≤1.1),
prefer 1.3, use strong cipher suites, and automate certificate rotation. This is
also why **post-quantum** key exchange is being layered into TLS now — to keep
forward secrecy against future quantum attacks.
""",
        ),
        _t(
            "The secure software development lifecycle",
            "11 min",
            r"""# The secure SDLC

Security isn't a phase at the end — it's woven through development. Each stage
has its tooling:

- **Design** — threat modeling (STRIDE), security requirements, secure
  defaults.
- **Code** — secure-coding standards, peer review with a security lens,
  pre-commit secret scanning.
- **Build/CI** — automated gates:
  - **SAST** (static analysis) — scans source for vulnerable patterns.
  - **SCA** (software composition analysis) — flags vulnerable/outdated
    dependencies (your biggest real-world risk surface).
  - **Secret scanning** — blocks committed keys.
- **Test** — **DAST** (dynamic analysis) hits the running app; **fuzzing**
  throws malformed input; penetration testing for depth.
- **Deploy** — signed artefacts, hardened configs, least-privilege IAM,
  infrastructure-as-code scanning.
- **Operate** — monitoring, patching, incident response.

The principle is **shift left**: catch issues as early (and cheaply) as possible.
A vulnerability found in design costs almost nothing; the same flaw found in
production after a breach can cost a company its reputation. Supply-chain
security (signing, SBOMs, pinned dependencies) is now a first-class concern after
high-profile attacks.
""",
        ),
        _t(
            "Detection, response & defensive operations",
            "10 min",
            r"""# Detection, response & defensive operations

Prevention fails eventually — mature security assumes breach and invests in
**detecting and responding** fast.

- **Logging & SIEM** — centralise logs (auth, network, app) into a **Security
  Information and Event Management** system that correlates events and alerts on
  suspicious patterns. You can't investigate what you didn't record.
- **Detection** — IDS/IPS, EDR on endpoints, anomaly detection. Tune to cut
  alert fatigue.
- **Incident response** — a rehearsed plan: **Prepare → Identify → Contain →
  Eradicate → Recover → Learn.** The post-incident review (blameless) is where
  you actually get safer.
- **Zero trust** — drop the idea of a trusted internal network. **Never trust,
  always verify**: authenticate and authorize every request, every device, every
  time; micro-segment so a foothold can't spread.
- **Cloud & container security** — lock down IAM (least privilege), scan images,
  don't run as root, keep secrets out of images, isolate workloads, watch for
  misconfigured storage (a top cause of leaks).

The defender's edge is **practice**: tabletop exercises, red-team/blue-team
drills, and treating every near-miss as a lesson. Security is a continuous loop,
not a finish line.
""",
        ),
        quiz_lesson(
            "Quiz: Securing & Defending Systems",
            (
                q(
                    "What does the 'E' in STRIDE stand for?",
                    (
                        opt("Elevation of privilege", correct=True),
                        opt("Encryption"),
                        opt("Exfiltration"),
                        opt("Endpoint"),
                    ),
                    "STRIDE = Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.",
                ),
                q(
                    "Why is a constant-time comparison used for secrets/tokens?",
                    (
                        opt(
                            "It takes the same time regardless of where a mismatch is, leaking no timing info",
                            correct=True,
                        ),
                        opt("It is faster than a normal comparison"),
                        opt("It encrypts the values before comparing"),
                        opt("It hashes both inputs first"),
                    ),
                    "Early-return comparisons leak how many leading bytes matched; constant-time always scans fully.",
                ),
                q(
                    "What does forward secrecy guarantee?",
                    (
                        opt(
                            "Past recorded sessions stay safe even if the long-term private key is later stolen",
                            correct=True,
                        ),
                        opt("Future sessions can't be decrypted"),
                        opt("Certificates never expire"),
                        opt("Passwords are stored hashed"),
                    ),
                    "Ephemeral per-session keys (ECDHE) are discarded, so a later key theft can't decrypt old traffic.",
                ),
                q(
                    "What does SCA (software composition analysis) protect against?",
                    (
                        opt("Vulnerable or outdated third-party dependencies", correct=True),
                        opt("SQL injection in your own code"),
                        opt("Expired TLS certificates"),
                        opt("Weak passwords"),
                    ),
                    "SCA inventories and flags known-vulnerable components — a leading real-world risk.",
                ),
                q(
                    "What is the core principle of zero trust?",
                    (
                        opt(
                            "Never trust, always verify — authenticate/authorize every request regardless of network location",
                            correct=True,
                        ),
                        opt("Trust everything inside the corporate network"),
                        opt("Encrypt only external traffic"),
                        opt("Give admins unrestricted access"),
                    ),
                    "Zero trust drops the trusted-internal-network assumption and verifies every access.",
                ),
                q(
                    "What does 'shift left' mean in the secure SDLC?",
                    (
                        opt(
                            "Address security as early as possible (design/code), where fixes are cheapest",
                            correct=True,
                        ),
                        opt("Move servers to a different data center"),
                        opt("Delay security testing until production"),
                        opt("Use left-handed encryption keys"),
                    ),
                    "Catching issues early (threat modeling, SAST/SCA in CI) is far cheaper than fixing post-breach.",
                ),
            ),
        ),
    ),
)


SECURITY_COURSES = (_SEC_BASICS, _SEC_INTERMEDIATE, _SEC_ADVANCED)
