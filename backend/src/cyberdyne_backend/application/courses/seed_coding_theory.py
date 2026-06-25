"""Information Theory & Coding track: Basics -> Intermediate -> Advanced.

A channel-coding / error-correcting-codes companion to the entropy/math
courses. From bits, entropy and channel capacity through linear block codes,
Hamming/CRC/Reed-Solomon, and on to convolutional/turbo/LDPC/polar codes and
coding in modern systems (5G, Wi-Fi, storage). Lessons are `text` with LaTeX,
interactive ```plot blocks and ```mermaid encoder/decoder & Tanner-graph
diagrams.
"""

# Lesson prose uses typographic characters (×, →, ≈, ⊕, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Information Theory & Coding — Basics ──────────────────────────────────────

_CT_BASICS = SeedCourse(
    slug="coding-theory-basics",
    title="Information Theory & Coding — Basics",
    description=(
        "The foundations of communicating reliably over noisy channels: bits and "
        "entropy, mutual information, Shannon's channel-capacity theorem, source "
        "coding (Huffman / prefix codes), and the first ideas of error control — "
        "detection vs correction and Hamming distance. Interactive entropy and "
        "capacity plots plus encoder/decoder diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Information, entropy & the bit",
            "11 min",
            """\
# Information, entropy & the bit

Information theory measures **surprise**. A certain event carries no information;
a rare one carries a lot. The information of an outcome with probability $p$ is

$$I = \\log_2 \\frac1p \\quad\\text{bits}.$$

Average it over all outcomes and you get the **entropy** $H$ — the average number
of bits needed to describe a source:

$$H(X) = -\\sum_i p_i \\log_2 p_i.$$

For a single biased bit (probability $p$ of a $1$) this is the **binary entropy
function** $H(p) = -p\\log_2 p - (1-p)\\log_2(1-p)$. It is $0$ at $p=0$ or $p=1$
(no surprise) and peaks at exactly **1 bit** when $p = 0.5$ (maximum uncertainty):

```plot
{"title": "Binary entropy function H(p)", "xLabel": "p (probability of a 1)", "yLabel": "H(p) in bits", "xRange": [0, 1], "yRange": [0, 1.1], "functions": [{"expr": "-(x*log2(x) + (1-x)*log2(1-x))", "label": "H(p)", "color": "#2563eb"}], "points": [{"x": 0.5, "y": 1, "label": "max = 1 bit at p = 0.5", "color": "#dc2626", "size": 7}]}
```

Entropy is the **floor** on lossless compression and the budget every code must
respect. The whole subject is one tension: pack information tightly (compression)
yet survive noise (error correction).

**Next:** what a noisy channel does to information.
""",
        ),
        _t(
            "Mutual information & the noisy channel",
            "11 min",
            """\
# Mutual information & the noisy channel

Send $X$, receive $Y$ through a noisy channel. How much does $Y$ tell you about
$X$? That is the **mutual information**

$$I(X;Y) = H(X) - H(X\\mid Y),$$

the entropy of the input minus what *remains* uncertain after seeing the output.
No noise → $I = H(X)$ (the output pins down the input); pure noise → $I = 0$.

The textbook model is the **binary symmetric channel (BSC)**: each bit is flipped
independently with probability $p$.

```mermaid
flowchart LR
  X0["sent 0"] -->|"1 − p"| Y0["received 0"]
  X0 -->|"p (flip)"| Y1["received 1"]
  X1["sent 1"] -->|"p (flip)"| Y0
  X1 -->|"1 − p"| Y1
```

The noise the channel injects is exactly the binary entropy of the flip
probability, $H(p)$. At $p = 0.5$ the bit is destroyed ($I = 0$); near $p = 0$ or
$p = 1$ almost all information survives:

```plot
{"title": "Information lost to a BSC equals H(p)", "xLabel": "flip probability p", "yLabel": "bits of noise H(p)", "xRange": [0, 1], "yRange": [0, 1.1], "functions": [{"expr": "-(x*log2(x) + (1-x)*log2(1-x))", "label": "noise H(p)", "color": "#dc2626"}], "points": [{"x": 0.5, "y": 1, "label": "channel useless (p = 0.5)", "color": "#94a3b8", "size": 7}]}
```

Mutual information is the raw material of capacity: maximise it over the input and
you get the most a channel can carry.

**Next:** that maximum — channel capacity.
""",
        ),
        _t(
            "Channel capacity & Shannon's theorem",
            "12 min",
            """\
# Channel capacity & Shannon's theorem

**Capacity** $C$ is the largest mutual information any input distribution can wring
out of a channel — the absolute ceiling on reliable bits per use:

$$C = \\max_{p(x)} I(X;Y).$$

**Shannon's noisy-channel coding theorem** (1948) is the stunning result: for *any*
rate $R < C$ there exist codes with arbitrarily small error probability, and for
$R > C$ reliable communication is impossible. Capacity is a hard wall — but below
it, perfection is achievable in principle.

For the band-limited Gaussian channel, the **Shannon–Hartley** law gives capacity
from bandwidth $B$ and signal-to-noise ratio:

$$C = B\\,\\log_2\\!\\left(1 + \\mathrm{SNR}\\right).$$

Capacity grows only **logarithmically** with SNR — diminishing returns from raw
power, which is why coding (not just more watts) matters:

```plot
{"title": "Capacity per Hz vs SNR (Shannon–Hartley)", "xLabel": "SNR (linear)", "yLabel": "C/B = log2(1 + SNR) (bits/s/Hz)", "xRange": [0, 30], "yRange": [0, 5.5], "functions": [{"expr": "log2(1 + x)", "label": "log2(1 + SNR)", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "label": "SNR = 1 → 1 bit/s/Hz", "color": "#dc2626", "size": 6}]}
```

Shannon's theorem launched the search for codes that approach $C$ — a search this
track follows all the way to the capacity-approaching codes of the Advanced course.

**Next:** squeezing redundancy out — source coding.
""",
        ),
        _t(
            "Source coding & data compression",
            "11 min",
            """\
# Source coding & data compression

Before fighting noise, remove **waste**. Source coding (compression) represents a
source in as few bits as possible — ideally close to its entropy $H$, the
information-theoretic floor (Shannon's *source coding theorem*).

The trick: give **short codewords to frequent symbols, long ones to rare symbols**.
A **prefix code** (no codeword is the start of another) can be decoded instantly,
with no separators. **Huffman coding** builds the optimal prefix code by repeatedly
merging the two least-likely symbols into a binary tree:

```mermaid
flowchart TB
  ROOT(( )) -->|"0"| A["A  (p = 0.5)"]
  ROOT -->|"1"| N1(( ))
  N1 -->|"0"| B["B  (p = 0.25)"]
  N1 -->|"1"| N2(( ))
  N2 -->|"0"| C["C  (p = 0.125)"]
  N2 -->|"1"| D["D  (p = 0.125)"]
```

Reading root-to-leaf gives `A=0`, `B=10`, `C=110`, `D=111`. Frequent `A` costs one
bit; rare `C`/`D` cost three. The average length here, $1.75$ bits, equals the
source entropy exactly — Huffman is optimal among symbol codes.

This is the *opposite* of error coding: compression **strips** redundancy, error
correction **adds it back** in a controlled, useful form. Real systems do both,
in that order.

**Next:** why we need to add redundancy back.
""",
        ),
        _t(
            "The need for error control",
            "10 min",
            """\
# The need for error control

A real channel flips bits. With no protection, a single flip silently corrupts
your data. **Error control** adds structured redundancy so the receiver can either
*notice* or *fix* the damage. Two regimes:

- **Error detection** — enough redundancy to *spot* that something is wrong (e.g. a
  parity bit, a checksum, a CRC). Cheap. Response: ask for a retransmission (ARQ).
- **Error correction** — enough redundancy to *reconstruct* the original without
  asking again (forward error correction, FEC). More overhead, but essential when
  there is no back-channel (deep space, storage, broadcast).

```mermaid
flowchart LR
  SRC["message k bits"] --> ENC["encoder: add redundancy"]
  ENC --> TX["codeword n bits"]
  TX --> CH["noisy channel"]
  CH --> RX["received word"]
  RX --> DEC["decoder: detect / correct"]
  DEC --> OUT["recovered message"]
```

A **single parity bit** detects any one bit-flip (the parity no longer matches) but
cannot say *which* bit or fix it, and misses an even number of flips. To **correct**,
you need a code where each valid message maps to a codeword that stays
recognisable even after a few flips. The **code rate** $R = k/n$ measures the price:
$k$ message bits carried in $n$ transmitted bits.

**Next:** the geometry that makes correction possible — Hamming distance.
""",
        ),
        _t(
            "Hamming distance & block codes",
            "11 min",
            """\
# Hamming distance & block codes

The **Hamming distance** between two binary words is the number of positions where
they differ — e.g. $d(\\texttt{10110}, \\texttt{10011}) = 2$. A code is a chosen set
of valid codewords scattered in this space; noise nudges a codeword to a nearby
word, and the decoder snaps it back to the **closest** valid codeword.

The power of a code is its **minimum distance** $d_{\\min}$, the smallest distance
between any two codewords. From it everything follows:

- **Detect** up to $d_{\\min} - 1$ errors.
- **Correct** up to $\\left\\lfloor \\frac{d_{\\min} - 1}{2} \\right\\rfloor$ errors.

So a code with $d_{\\min} = 3$ corrects **1** error (and detects 2). The simplest
example is the **3× repetition code**: send each bit three times and take a
majority vote. It has $d_{\\min} = 3$, so it corrects one flip — at a brutal rate of
$R = 1/3$. Its error probability after voting drops sharply as the channel improves:

```plot
{"title": "Repetition-3 majority vote: error vs raw bit error p", "xLabel": "raw bit error p", "yLabel": "post-decode error", "xRange": [0, 0.5], "yRange": [0, 0.5], "functions": [{"expr": "3*x^2 - 2*x^3", "label": "P(error) = 3p² − 2p³", "color": "#dc2626"}, {"expr": "x", "label": "uncoded (= p)", "color": "#94a3b8"}], "points": [{"x": 0.1, "y": 0.028, "label": "p = 0.1 → ≈ 0.028", "color": "#16a34a", "size": 6}]}
```

Below $p = 0.5$ the coded curve sits under the uncoded line — coding helps. The
art is achieving large $d_{\\min}$ at a **good rate**, which is exactly what linear
block codes deliver next.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Information Theory & Coding — Intermediate ────────────────────────────────

_CT_INTERMEDIATE = SeedCourse(
    slug="coding-theory-intermediate",
    title="Information Theory & Coding — Intermediate",
    description=(
        "The workhorses of error correction: linear block codes via generator and "
        "parity-check matrices, syndrome decoding, Hamming codes and SECDED, cyclic "
        "codes and CRC, Reed–Solomon symbol codes for bursts, and interleaving. The "
        "algebra and engineering behind reliable storage and links, with BER plots "
        "and encoder/decoder diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Linear block codes: G and H",
            "13 min",
            """\
# Linear block codes: G and H

A **linear block code** maps $k$ message bits to $n$ codeword bits so that any sum
(XOR) of codewords is again a codeword. That linearity makes everything computable
with two matrices over $\\mathbb{F}_2$ (arithmetic mod 2):

- The **generator matrix** $G$ ($k \\times n$) encodes: $\\mathbf{c} = \\mathbf{m}\\,G$.
- The **parity-check matrix** $H$ ($(n-k) \\times n$) validates: $\\mathbf{c}$ is a
  valid codeword **iff** $H\\mathbf{c}^{\\top} = \\mathbf{0}$.

In **systematic** form $G = [\\,I_k \\mid P\\,]$, so the first $k$ codeword bits are
the message verbatim and the rest are parity. Then $H = [\\,P^{\\top} \\mid I_{n-k}\\,]$.

```mermaid
flowchart LR
  M["message m (k bits)"] --> G["× G  (encode)"]
  G --> C["codeword c (n bits)"]
  C --> CH["channel"]
  CH --> R["received r = c ⊕ e"]
  R --> H["× Hᵀ  (check)"]
  H --> S["syndrome s"]
```

The minimum distance equals the **smallest number of columns of $H$ that sum to
zero**. Notation $(n, k, d_{\\min})$ summarises a code — e.g. a $(7,4,3)$ code carries
4 bits in 7 and corrects one error.

**Next:** using the syndrome to actually locate the error.
""",
        ),
        _t(
            "Syndrome decoding",
            "12 min",
            """\
# Syndrome decoding

The receiver gets $\\mathbf{r} = \\mathbf{c} \\oplus \\mathbf{e}$, where $\\mathbf{e}$ is
the (unknown) error pattern. Multiply by $H$:

$$\\mathbf{s} = H\\mathbf{r}^{\\top} = H(\\mathbf{c}\\oplus\\mathbf{e})^{\\top}
= \\underbrace{H\\mathbf{c}^{\\top}}_{=\\,0} \\oplus\\, H\\mathbf{e}^{\\top}
= H\\mathbf{e}^{\\top}.$$

The **syndrome** $\\mathbf{s}$ depends only on the *error*, not the message — a huge
simplification. If $\\mathbf{s} = \\mathbf{0}$, no (detectable) error. Otherwise the
syndrome points at the most likely error pattern:

```mermaid
flowchart LR
  R["received r"] --> CALC["s = H rᵀ"]
  CALC --> Z{"s = 0 ?"}
  Z -->|"yes"| OK["accept r"]
  Z -->|"no"| LUT["syndrome → error e"]
  LUT --> FIX["correct: ĉ = r ⊕ e"]
```

For a single-error-correcting code, each single-bit error gives a **distinct**
syndrome equal to the corresponding **column of $H$** — so the syndrome literally
*is* the address of the flipped bit. A small lookup table (standard array) maps
syndrome → most-likely error, the decoder XORs it out, and the codeword is
restored. This is **maximum-likelihood decoding** done cheaply.

**Next:** the most famous instance — Hamming codes.
""",
        ),
        _t(
            "Hamming codes & SECDED",
            "12 min",
            """\
# Hamming codes & SECDED

The **Hamming codes** are the classic single-error-correcting linear codes. The
$(7,4)$ Hamming code carries 4 data bits in 7, with $d_{\\min} = 3$. Its genius:
arrange the columns of $H$ to be the binary numbers $1$ through $7$. Then the
syndrome read as a binary number **is the position of the flipped bit** — flip it
back and you are done.

```mermaid
flowchart LR
  D["4 data bits"] --> ENC["add 3 parity bits<br/>(positions 1,2,4)"]
  ENC --> C7["7-bit codeword"]
  C7 --> CH["channel (≤1 flip)"]
  CH --> SYN["syndrome = bit position"]
  SYN --> CORR["flip that bit → corrected"]
```

Hamming codes are **perfect**: every 7-bit word is either a codeword or exactly one
flip from a unique codeword — no waste. Their rate is high ($4/7 \\approx 0.57$),
which is why they beat repetition for the same protection.

Add **one more overall parity bit** to get the $(8,4)$ **SECDED** code with
$d_{\\min} = 4$: it **S**ingle-**E**rror **C**orrects *and* **D**ouble-**E**rror
**D**etects. This is the workhorse of ECC memory — every DRAM error-correcting
DIMM uses a SECDED (often extended Hamming) code to silently fix the single-bit
flips that cosmic rays cause.

**Next:** codes built from polynomials — cyclic codes and CRC.
""",
        ),
        _t(
            "Cyclic codes & CRC",
            "12 min",
            """\
# Cyclic codes & CRC

A **cyclic code** is a linear code where any cyclic shift of a codeword is again a
codeword. This extra structure lets us treat bit strings as **polynomials** over
$\\mathbb{F}_2$ and reduces encoding/decoding to polynomial division — implementable
with a tiny **shift register with XOR taps**, which is why it is everywhere in
hardware.

A codeword polynomial is a multiple of a fixed **generator polynomial** $g(x)$.
Encoding the message $m(x)$:

$$c(x) = m(x)\\,x^{r} \\;\\oplus\\; \\big[\\,m(x)\\,x^{r} \\bmod g(x)\\,\\big],$$

appending the remainder as check bits. The **CRC (cyclic redundancy check)** is
exactly this used for *detection*: transmit data + remainder; the receiver divides
by $g(x)$ and expects remainder zero.

```mermaid
flowchart LR
  MSG["message bits"] --> SR["LFSR: divide by g(x)"]
  SR --> REM["remainder = CRC bits"]
  REM --> FRAME["message ‖ CRC on the wire"]
  FRAME --> RXDIV["receiver divides by g(x)"]
  RXDIV --> CHK{"remainder = 0 ?"}
  CHK -->|"yes"| ACCEPT["accept"]
  CHK -->|"no"| DROP["error → reject / resend"]
```

A well-chosen $g(x)$ catches all single and double-bit errors, all odd numbers of
errors, and any burst shorter than the CRC length. CRC-32 guards Ethernet frames,
ZIP files and PNG chunks; it **detects** corruption (then you retransmit) rather
than correcting it.

**Next:** correcting whole symbols and bursts — Reed–Solomon.
""",
        ),
        _t(
            "Reed–Solomon codes",
            "12 min",
            """\
# Reed–Solomon codes

**Reed–Solomon (RS)** codes work on **symbols** (groups of bits, typically bytes)
rather than single bits, using arithmetic over a **Galois field** $\\mathrm{GF}(2^m)$.
An $\\mathrm{RS}(n,k)$ code adds $n-k$ parity symbols and can **correct up to
$t = \\frac{n-k}{2}$ symbol errors** anywhere in the block.

The key idea: treat the $k$ data symbols as a polynomial and evaluate it at $n$
points (or, equivalently, oversample). Because $n - k$ extra evaluations are
redundant, any $k$ correct symbols are enough to recover the polynomial — RS is a
**maximum-distance-separable (MDS)** code, the best possible $d_{\\min} = n - k + 1$.

Crucially, a *burst* of bit errors usually corrupts only a **few symbols**, so
RS shrugs off bursts that would defeat a bit-level code. RS(255, 223) — 32 parity
bytes correcting 16 byte-errors — protected the Voyager deep-space link; RS codes
also armour CDs, DVDs, QR codes and (historically) hard drives.

```mermaid
flowchart LR
  DATA["k data symbols"] --> RSENC["RS encoder<br/>(+ n−k parity symbols)"]
  RSENC --> BLK["n-symbol block"]
  BLK --> CH["channel<br/>(bursts → few bad symbols)"]
  CH --> RSDEC["RS decoder<br/>locate + correct ≤ t symbols"]
  RSDEC --> OUT["recovered data"]
```

As the number of corrupted symbols approaches the limit $t$, decoding still
succeeds; beyond it, the decoder either fails loudly or (rarely) miscorrects:

```plot
{"title": "RS block-failure vs symbol-error rate (qualitative)", "xLabel": "symbol error rate", "yLabel": "block failure probability", "xRange": [0, 0.2], "yRange": [0, 1.05], "functions": [{"expr": "1/(1 + exp(-90*(x - 0.063)))", "label": "RS(255,223), t = 16", "color": "#2563eb"}], "points": [{"x": 0.063, "y": 0.5, "label": "≈ t/n threshold", "color": "#dc2626", "size": 6}]}
```

**Next:** spreading errors out so codes can cope — interleaving.
""",
        ),
        _t(
            "Interleaving & burst errors",
            "11 min",
            """\
# Interleaving & burst errors

Many real channels fail in **bursts** — a scratch on a CD, a fade in a wireless
link, a defect on a disk — clobbering many *consecutive* bits at once. That is the
worst case for a code designed for scattered errors: a single burst can exceed any
one codeword's correction limit.

**Interleaving** defeats bursts by **shuffling** the transmitted order. Write the
codewords into a matrix **by rows**, transmit **by columns**. A burst on the wire
then hits one symbol from *each* codeword instead of many from one — turning a
concentrated burst into the sparse, scattered errors codes handle well. The
receiver de-interleaves before decoding.

```mermaid
flowchart LR
  CW["coded symbols<br/>(row order)"] --> INT["interleaver<br/>(read by columns)"]
  INT --> CH["bursty channel"]
  CH --> DEINT["de-interleaver<br/>(restore row order)"]
  DEINT --> DEC["per-codeword decoder"]
  DEC --> OUT["recovered data"]
```

The cost is **latency and memory** (you must buffer the whole interleaver block),
and a burst longer than the interleaver depth still breaks through — so depth is a
design knob. CDs combine RS + interleaving (CIRC) so a 2.5 mm scratch — thousands
of consecutive bad bits — is fully recoverable. The pairing of a strong symbol
code with an interleaver is a recurring pattern, and it sets up the powerful
**concatenated** and iterative codes of the Advanced track.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Information Theory & Coding — Advanced ────────────────────────────────────

_CT_ADVANCED = SeedCourse(
    slug="coding-theory-advanced",
    title="Information Theory & Coding — Advanced",
    description=(
        "The capacity-approaching frontier: convolutional codes and the trellis, "
        "Viterbi decoding, turbo codes and iterative decoding, LDPC codes with "
        "belief propagation on the Tanner graph, polar codes, and how all of it "
        "lands in 5G, Wi-Fi and storage (soft vs hard decision). Trellis and "
        "Tanner-graph diagrams plus BER and capacity-gap plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Convolutional codes & the trellis",
            "13 min",
            """\
# Convolutional codes & the trellis

Unlike block codes, a **convolutional code** has **memory**: each output depends on
the current input *and* the last few inputs, held in a shift register. The encoder
slides over the stream, emitting more bits than it ingests (rate $k/n$, e.g. one
bit in → two bits out for a rate-$1/2$ code). The **constraint length** $K$ is how
many input bits influence each output.

Because the encoder is a small finite-state machine, its behaviour draws out as a
**trellis**: states down the side, time across, with edges for each input bit
labelled by the output bits. Every possible codeword is a **path** through the
trellis.

```mermaid
flowchart LR
  subgraph t0["time t"]
    A0["00"]
    B0["01"]
    C0["10"]
    D0["11"]
  end
  subgraph t1["time t+1"]
    A1["00"]
    B1["01"]
    C1["10"]
    D1["11"]
  end
  A0 -->|"0 / 00"| A1
  A0 -->|"1 / 11"| C1
  C0 -->|"0 / 10"| B1
  C0 -->|"1 / 01"| D1
  B0 -->|"0 / 11"| A1
  B0 -->|"1 / 00"| C1
  D0 -->|"0 / 01"| B1
  D0 -->|"1 / 10"| D1
```

Decoding becomes a **shortest-path** problem on this trellis: find the path whose
output best matches what was received. That is exactly what the Viterbi algorithm
does next.

**Next:** optimal trellis decoding — Viterbi.
""",
        ),
        _t(
            "Viterbi decoding",
            "12 min",
            """\
# Viterbi decoding

The **Viterbi algorithm** finds the single most likely path through the trellis —
i.e. the maximum-likelihood codeword — without enumerating the exponentially many
paths. It is dynamic programming on the trellis.

At each time step, for **every** state, it keeps only the **best surviving path**
reaching that state (the one with smallest accumulated *branch metric* — Hamming
distance for hard decisions, Euclidean for soft). Paths that arrive at the same
state with worse cost are discarded immediately, so the work per step is constant
in the message length.

```mermaid
flowchart LR
  R["received symbols"] --> BM["branch metrics<br/>(distance to each edge)"]
  BM --> ACS["add–compare–select<br/>(keep best survivor per state)"]
  ACS --> TB["traceback<br/>(follow survivors back)"]
  TB --> OUT["most-likely message"]
```

**Soft-decision** Viterbi — feeding the decoder the analog confidence of each bit
rather than a hard 0/1 — buys roughly **2 dB** of coding gain over hard decision,
a recurring theme: never throw away the channel's confidence too early. Viterbi
decoders shipped in modems, GSM, Wi-Fi and deep-space links for decades and remain
the reference for short-memory convolutional codes.

**Next:** combining codes to approach capacity — turbo codes.
""",
        ),
        _t(
            "Turbo codes & iterative decoding",
            "12 min",
            """\
# Turbo codes & iterative decoding

In 1993 **turbo codes** stunned the field by getting within a fraction of a dB of
the Shannon limit — a gap that had stood for 45 years. The recipe: two simple
convolutional encoders working on the data in **two different orders** (one direct,
one through an **interleaver**), producing two independent streams of parity.

The magic is in the **iterative decoder**. Two soft-input/soft-output decoders take
turns: each produces a *soft* belief about every bit (a log-likelihood ratio),
passes that **extrinsic** information to the other as a refined prior, and they
ping-pong until they agree. Each round, confidence improves — like two experts
swapping notes.

```mermaid
flowchart LR
  RX["soft received bits"] --> D1["decoder 1<br/>(SISO)"]
  D1 -->|"extrinsic LLR"| INT["interleave"]
  INT --> D2["decoder 2<br/>(SISO)"]
  D2 -->|"extrinsic LLR"| DEINT["de-interleave"]
  DEINT -->|"feed back as prior"| D1
  D2 --> DEC["hard decision after N iterations"]
```

The BER plummets dramatically near a threshold SNR — the famous **turbo cliff** —
then enters a gentler **error floor**:

```plot
{"title": "Turbo code BER vs SNR — the 'turbo cliff' (qualitative)", "xLabel": "Eb/N0 (dB)", "yLabel": "BER (log-like axis)", "xRange": [0, 4], "yRange": [0, 0.55], "functions": [{"expr": "0.5/(1 + exp(8*(x - 1.2)))", "label": "turbo, several iterations", "color": "#2563eb"}, {"expr": "0.5/(1 + exp(2.2*(x - 1.2)))", "label": "uncoded-ish reference", "color": "#94a3b8"}], "points": [{"x": 1.2, "y": 0.25, "label": "cliff ≈ near capacity", "color": "#dc2626", "size": 6}]}
```

Turbo codes powered 3G/4G data channels and deep-space probes, and proved iterative
**message passing** could approach capacity in practice — the same idea LDPC codes
push further.

**Next:** LDPC codes and belief propagation.
""",
        ),
        _t(
            "LDPC codes & belief propagation",
            "13 min",
            """\
# LDPC codes & belief propagation

**Low-density parity-check (LDPC)** codes are linear block codes whose parity-check
matrix $H$ is **sparse** — only a few 1s per row. Invented by Gallager in 1962,
ignored for 30 years, then rediscovered as another route to capacity. The sparsity
is what makes iterative decoding both possible and cheap.

An LDPC code is best pictured as a **Tanner graph**: a bipartite graph with one
**variable node** per code bit and one **check node** per parity equation, with an
edge wherever $H$ has a 1.

```mermaid
graph TB
  v1(("v1")) --- c1{{"c1"}}
  v2(("v2")) --- c1
  v2 --- c2{{"c2"}}
  v3(("v3")) --- c1
  v3 --- c2
  v4(("v4")) --- c2
  v4 --- c3{{"c3"}}
  v5(("v5")) --- c1
  v5 --- c3
  v6(("v6")) --- c3
```

Decoding is **belief propagation** (the sum–product algorithm): variable and check
nodes exchange soft *messages* (probabilities/LLRs) along the edges. Variable nodes
combine what the channel and their checks suggest; check nodes enforce the
parity constraints; iterate. Because the graph is sparse with few short cycles,
these local updates converge to the right answer with near-optimal performance.

LDPC codes match or beat turbo codes, decode with massive parallelism, and now
protect Wi-Fi (802.11n/ac/ax), 10G Ethernet, DVB-S2 satellite, SSDs and the 5G
data channel.

**Next:** the provably capacity-achieving newcomer — polar codes.
""",
        ),
        _t(
            "Polar codes & the capacity frontier",
            "12 min",
            """\
# Polar codes & the capacity frontier

**Polar codes** (Arıkan, 2009) are the first codes **proven** to *achieve* channel
capacity with low-complexity encoding and decoding — a landmark that won them a
place in the 5G standard barely a decade after their invention.

The idea is **channel polarisation**. Combine $N$ copies of a channel through a
recursive transform; as $N$ grows, the synthesised sub-channels split into two
extremes: some become **almost perfect** (capacity → 1) and the rest become
**almost useless** (capacity → 0). The encoder then puts **data on the good
sub-channels** and fixes the bad ones to known "frozen" bits.

```mermaid
flowchart LR
  U["N input slots"] --> POL["polarising transform<br/>(recursive XOR butterfly)"]
  POL --> SPLIT{"sub-channels polarise"}
  SPLIT -->|"good (≈ noiseless)"| DATA["carry data bits"]
  SPLIT -->|"bad (≈ useless)"| FROZEN["frozen bits (known 0)"]
  DATA --> SC["successive-cancellation decoder"]
  FROZEN --> SC
  SC --> OUT["decoded message"]
```

The fraction of *good* sub-channels converges to exactly the channel capacity $C$ —
so a long polar code transmits at any rate below $C$ reliably. Decoding by
**successive cancellation** (especially the list variant, SCL, with a CRC aid) is
practical and, at the short block lengths of control signalling, competitive with
LDPC. 5G uses polar codes for control channels and LDPC for data — different tools
for different jobs.

**Next:** how all of this is used in practice.
""",
        ),
        _t(
            "Coding in practice",
            "12 min",
            """\
# Coding in practice

Real systems don't pick one code — they **stack** them and tune for the channel.

- **Concatenation.** An *inner* code (often convolutional/Viterbi or LDPC) cleans
  up the raw channel; an *outer* code (often Reed–Solomon) mops up the residual
  errors the inner decoder lets through. CDs, deep-space links and DVB all do this.
- **Soft vs hard decision.** Hard decision quantises each received symbol to 0/1
  before decoding; **soft decision** keeps the analog confidence (an LLR) and feeds
  it to the decoder. Soft decoding is worth roughly **2 dB** — the difference
  between a working and a failing link — so modern decoders (Viterbi, turbo, LDPC)
  are all soft-input.
- **Rate adaptation.** Systems carry a family of code rates and pick one to match
  the current SNR (more coding when the channel is bad, less when it is good),
  often via **puncturing** a low-rate mother code.

```mermaid
flowchart LR
  SRC["data"] --> RS["outer code (RS)"]
  RS --> ILV["interleaver"]
  ILV --> INNER["inner code (LDPC / conv.)"]
  INNER --> MOD["modulator → channel"]
  MOD --> IDEC["soft inner decoder"]
  IDEC --> DILV["de-interleaver"]
  DILV --> RSDEC["outer RS decoder"]
  RSDEC --> OUT["clean data"]
```

Where the codes live today: **5G NR** uses LDPC for data and polar for control;
**Wi-Fi** (802.11n and later) offers LDPC; **storage** uses LDPC in SSDs/flash and
RS in optical media and QR codes; **deep space** still leans on RS + convolutional/
turbo. Every working code sits a measurable gap from the Shannon limit — and the
last 60 years of this subject is the story of closing that gap:

```plot
{"title": "Closing the gap to capacity over the decades (schematic)", "xLabel": "year", "yLabel": "gap to Shannon limit (dB)", "xRange": [1948, 2020], "yRange": [0, 9], "functions": [{"expr": "8.5 - 0.105*(x - 1948)", "label": "frontier codes (trend)", "color": "#2563eb"}], "points": [{"x": 1960, "y": 6.4, "label": "Hamming / RS era", "color": "#94a3b8", "size": 6}, {"x": 1993, "y": 1.9, "label": "turbo", "color": "#dc2626", "size": 6}, {"x": 2009, "y": 0.6, "label": "LDPC / polar", "color": "#16a34a", "size": 6}]}
```

You now have the full arc: from entropy and capacity to the codes that chase it.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


CODING_THEORY_COURSES: tuple[SeedCourse, ...] = (_CT_BASICS, _CT_INTERMEDIATE, _CT_ADVANCED)

__all__ = ["CODING_THEORY_COURSES"]
