"""Image & Video Processing track: Basics -> Intermediate -> Advanced.

From pixels, sampling and colour spaces to histograms, spatial filtering,
edges, the 2-D Fourier transform, restoration, morphology, segmentation and
feature detection, then on to compression (DCT/JPEG, wavelets), video coding
(motion estimation, I/P/B frames, H.264/HEVC) and learning-based vision.
Lessons are `text` with LaTeX, interactive ```plot blocks and ```mermaid block
diagrams of the imaging and codec pipelines.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Image & Video Processing — Basics ────────────────────────────────────────

_IP_BASICS = SeedCourse(
    slug="image-processing-basics",
    title="Image & Video Processing — Basics",
    description=(
        "What a digital image really is: pixels, sampling, quantisation and "
        "colour spaces. Then the core toolbox — intensity transforms and gamma, "
        "histogram equalisation, spatial filtering and convolution, denoising and "
        "edge detection — with interactive transfer-curve and kernel plots and a "
        "diagram of the imaging pipeline."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Digital images: pixels, sampling & colour",
            "10 min",
            """\
# Digital images: pixels, sampling & colour

A **digital image** is a 2-D grid of **pixels**, each holding a number (or a
small tuple of numbers). Producing one from the continuous world takes two steps:

- **Sampling** — chop the scene into a grid of locations. More samples → higher
  **spatial resolution** (sharper detail). Too few → blocky pixels and aliasing.
- **Quantisation** — round each sample's brightness to a fixed set of levels.
  8 bits gives $2^8 = 256$ grey levels; too few levels causes visible **banding**.

A greyscale pixel is one intensity $I \\in [0, 255]$; a colour pixel is usually
three — **R, G, B**. But RGB mixes brightness and colour, so we often convert to
spaces that separate them: **YCbCr** (luma $Y$ + two chroma channels, used by
JPEG and video), **HSV** (hue/saturation/value), or device-independent **CIELAB**.

```mermaid
flowchart LR
  SCENE["Continuous scene"] --> LENS["Lens + sensor"]
  LENS --> SAMP["Sampling (grid)"]
  SAMP --> QUANT["Quantisation (bit depth)"]
  QUANT --> IMG["Digital image f(x,y)"]
  IMG --> COLOR["Colour-space convert (RGB to YCbCr)"]
```

The eye is far more sensitive to **luma** than to **chroma**, which is why almost
every codec keeps full-resolution $Y$ but **subsamples** the colour channels.

**Next:** reshaping brightness with intensity transforms.
""",
        ),
        _t(
            "Intensity transforms & gamma",
            "10 min",
            """\
# Intensity transforms & gamma

An **intensity (point) transform** maps each pixel's value through a function
$s = T(r)$ — independent of its neighbours. A few essentials:

- **Negative** $s = 255 - r$ — invert (useful for film/medical images).
- **Contrast stretch** — spread a narrow range of values over the full $[0,255]$.
- **Gamma / power law** $s = 255\\,(r/255)^{\\gamma}$ — brighten ($\\gamma<1$) or
  darken ($\\gamma>1$) the mid-tones. Displays apply gamma to match the eye's
  roughly logarithmic response to light.

Slide $\\gamma$ and watch the transfer curve bend. $\\gamma = 1$ is the identity
(straight line); $\\gamma < 1$ lifts shadows, $\\gamma > 1$ deepens them:

```plot
{"title": "Gamma transfer curve s = (r/255)^γ × 255", "xLabel": "input r", "yLabel": "output s", "xRange": [0, 255], "yRange": [0, 255], "controls": [{"name": "g", "range": [0.3, 3], "value": 0.5, "label": "gamma γ"}], "functions": [{"expr": "255*(x/255)^g", "label": "s = T(r)", "color": "#2563eb"}, {"expr": "x", "label": "identity (γ=1)", "color": "#94a3b8"}]}
```

Because the transform is just a **lookup table** over 256 entries, point
operations are extremely fast — they run once per distinct value, not per pixel.

**Next:** reading and reshaping the histogram.
""",
        ),
        _t(
            "The histogram & equalisation",
            "11 min",
            """\
# The histogram & equalisation

The **histogram** counts how many pixels have each intensity. Its shape tells you
a lot: a dark image piles up near 0, a washed-out one near 255, a low-contrast one
crowds into a narrow band.

**Histogram equalisation** spreads those values out to use the full range. The
trick: use the image's own **cumulative distribution function** (CDF) as the
transform, $s = T(r) = (L-1)\\,\\text{CDF}(r)$. Wherever pixels are crowded, the CDF
is steep, so it pushes them apart — flattening the histogram and boosting contrast.

Below is a CDF used as an equalisation transfer curve: its steep middle (where
most pixels live) stretches the mid-tones across the output range:

```plot
{"title": "Equalisation: the CDF becomes the transfer curve", "xLabel": "input intensity r", "yLabel": "output s = (L-1)·CDF(r)", "xRange": [0, 255], "yRange": [0, 255], "functions": [{"expr": "255/(1+exp(-(x-128)/28))", "label": "CDF transfer curve", "color": "#2563eb"}, {"expr": "x", "label": "no change", "color": "#94a3b8"}]}
```

Global equalisation can over-amplify noise, so practitioners use **CLAHE**
(contrast-limited, adaptive, tile-by-tile) to equalise locally with a clip limit.

**Next:** operating on neighbourhoods with spatial filters.
""",
        ),
        _t(
            "Spatial filtering & convolution",
            "11 min",
            """\
# Spatial filtering & convolution

Point transforms ignore neighbours; **spatial filtering** slides a small **kernel**
(mask) over the image and replaces each pixel with a weighted sum of the pixels
under it. That operation is **convolution**:

$$g(x,y) = \\sum_{i}\\sum_{j} h(i,j)\\, f(x-i,\\, y-j).$$

The kernel $h$ decides the effect:

- **Smoothing / blur** — a box or **Gaussian** kernel (all-positive weights summing
  to 1) averages neighbours, suppressing detail and noise (a **low-pass** filter).
- **Sharpening** — subtract a blurred copy (unsharp masking) or apply a Laplacian;
  these boost edges (a **high-pass** filter) and can have negative weights.

Below is a 1-D slice of a Gaussian smoothing kernel — widen it ($\\sigma$) and the
filter averages over more neighbours, blurring more aggressively:

```plot
{"title": "1-D Gaussian smoothing kernel (wider σ = more blur)", "xLabel": "offset from centre (pixels)", "yLabel": "weight", "xRange": [-6, 6], "yRange": [0, 0.6], "controls": [{"name": "s", "range": [0.6, 3], "value": 1, "label": "sigma σ"}], "functions": [{"expr": "exp(-x^2/(2*s^2))/(s*sqrt(2*pi))", "label": "h(x)", "color": "#2563eb"}]}
```

Watch the **borders** (pad by zero, replicate or reflect) and note that a 2-D
Gaussian is **separable** — one horizontal pass then one vertical pass — which is
far cheaper than a full 2-D convolution.

**Next:** noise and how to remove it.
""",
        ),
        _t(
            "Noise & denoising",
            "10 min",
            """\
# Noise & denoising

Real images carry **noise** from the sensor, light and electronics:

- **Gaussian noise** — small additive fluctuations, bell-shaped.
- **Salt-and-pepper (impulse) noise** — scattered pure-black and pure-white pixels.

Different noise wants different filters:

- **Mean (box) filter** — averages a neighbourhood. Cheap, but blurs edges and
  barely helps with salt-and-pepper outliers.
- **Gaussian filter** — a weighted average; good for Gaussian noise, still blurs.
- **Median filter** — replaces each pixel with the **median** of its neighbourhood.
  Non-linear, it crushes salt-and-pepper spikes while keeping edges crisp.

There is always a trade-off: stronger denoising removes more noise but also more
real detail. **Edge-preserving** filters (bilateral, non-local means) win the
balance by averaging only over *similar* nearby pixels. The histogram below shows
why the median beats the mean on outliers — a few extreme values drag the mean but
leave the middle value untouched:

```plot
{"title": "Noise: outliers shift the mean but not the median", "xLabel": "pixel value", "yLabel": "count", "xRange": [0, 255], "yRange": [0, 1.1], "functions": [{"expr": "exp(-(x-120)^2/(2*18^2))", "label": "clean neighbourhood values", "color": "#2563eb"}], "points": [{"x": 5, "y": 0.25, "label": "pepper outlier", "color": "#dc2626", "size": 6}, {"x": 250, "y": 0.25, "label": "salt outlier", "color": "#dc2626", "size": 6}]}
```

**Next:** finding the boundaries — edge detection.
""",
        ),
        _t(
            "Edge detection: gradients, Sobel & Canny",
            "11 min",
            """\
# Edge detection: gradients, Sobel & Canny

An **edge** is where intensity changes sharply — a boundary between regions. The
maths of "sharp change" is the **gradient**:

$$\\nabla f = \\left(\\frac{\\partial f}{\\partial x},\\, \\frac{\\partial f}{\\partial y}\\right),
\\qquad |\\nabla f| = \\sqrt{f_x^2 + f_y^2}.$$

A large gradient magnitude = a likely edge; its direction is perpendicular to the
edge. We estimate $f_x, f_y$ with small derivative kernels — the **Sobel** operator
combines a derivative in one direction with smoothing in the other, so it finds
edges while resisting noise.

The 1-D profile below is a smoothed step (an edge); its derivative spikes exactly
at the transition — that spike is what an edge detector flags:

```plot
{"title": "An edge is a peak in the gradient (derivative of intensity)", "xLabel": "position x", "yLabel": "value", "xRange": [-6, 6], "yRange": [-0.2, 1.1], "functions": [{"expr": "1/(1+exp(-1.5*x))", "label": "intensity profile (a step edge)", "color": "#2563eb"}, {"expr": "exp(-(1.5*x)^2/4)", "label": "gradient magnitude", "color": "#dc2626"}]}
```

The **Canny** detector is the classic pipeline: Gaussian-smooth, compute
gradients, **non-maximum suppression** to thin edges to one pixel, then **double
thresholding + hysteresis** to keep strong edges and only the weak ones connected
to them. The result is clean, connected, single-pixel contours.

```mermaid
flowchart LR
  IMG["Input image"] --> SM["Gaussian smoothing"]
  SM --> GR["Gradient (Sobel): magnitude + direction"]
  GR --> NMS["Non-maximum suppression (thin to 1 px)"]
  NMS --> HYS["Double threshold + hysteresis"]
  HYS --> EDGE["Clean edge map"]
```

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Image & Video Processing — Intermediate ──────────────────────────────────

_IP_INTERMEDIATE = SeedCourse(
    slug="image-processing-intermediate",
    title="Image & Video Processing — Intermediate",
    description=(
        "The frequency domain and beyond: the 2-D Fourier transform and "
        "frequency-domain filtering, image restoration and the Wiener filter, "
        "morphological operations, segmentation (thresholding, region growing, "
        "watershed), feature detection (corners, blobs, SIFT) and geometric "
        "transforms with interpolation — with interactive frequency-response plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The 2-D Fourier transform & frequency-domain filtering",
            "12 min",
            """\
# The 2-D Fourier transform & frequency-domain filtering

Any image can be written as a sum of 2-D sinusoids. The **2-D Discrete Fourier
Transform (DFT)** gives, for each spatial frequency $(u,v)$, how much of that
ripple the image contains:

$$F(u,v) = \\sum_{x}\\sum_{y} f(x,y)\\, e^{-j2\\pi(ux/M + vy/N)}.$$

In the **spectrum**: the centre is the DC term (average brightness), **low
frequencies** near the centre carry smooth regions, and **high frequencies** at the
edges carry fine detail and sharp edges. Filtering becomes simple — *multiply* the
spectrum by a mask $H(u,v)$ instead of convolving:

- **Low-pass** keeps the centre → blurs (removes detail/noise).
- **High-pass** removes the centre → sharpens (keeps edges).

Below are the frequency responses of an ideal low-pass and a smoother **Butterworth**
low-pass. The ideal one's hard cutoff causes **ringing**; the gradual one avoids it:

```plot
{"title": "Low-pass frequency responses (cutoff D₀)", "xLabel": "frequency distance D from centre", "yLabel": "gain H", "xRange": [0, 100], "yRange": [0, 1.1], "controls": [{"name": "d0", "range": [10, 80], "value": 35, "label": "cutoff D₀"}], "functions": [{"expr": "1/sqrt(1+(x/d0)^4)", "label": "Butterworth (n=2)", "color": "#2563eb"}, {"expr": "1/sqrt(1+(x/d0)^16)", "label": "near-ideal (sharp)", "color": "#dc2626"}]}
```

The **convolution theorem** ties it together: convolution in space = multiplication
in frequency, so large filters are often faster via the **FFT**.

**Next:** undoing degradation — image restoration.
""",
        ),
        _t(
            "Image restoration & the Wiener filter",
            "11 min",
            """\
# Image restoration & the Wiener filter

**Restoration** tries to *recover* the original from a known degradation, unlike
enhancement which just makes images *look* better. The standard model is

$$g = h * f + n,$$

a true image $f$ blurred by a known point-spread function $h$ (motion, defocus)
plus additive **noise** $n$.

Naively dividing the spectra ($\\hat F = G/H$, **inverse filtering**) explodes
wherever $H$ is near zero — it amplifies noise catastrophically. The **Wiener
filter** balances deblurring against noise using the signal-to-noise ratio:

$$\\hat F(u,v) = \\frac{H^*(u,v)}{|H(u,v)|^2 + K}\\, G(u,v),$$

where $K$ approximates the noise-to-signal power ratio. The plot shows the Wiener
gain vs the unstable inverse: where the blur kills a frequency ($H$ small), the
inverse blows up while Wiener gently rolls off instead:

```plot
{"title": "Wiener gain stays bounded where the inverse filter explodes", "xLabel": "blur response H at this frequency", "yLabel": "restoration gain", "xRange": [0.02, 1], "yRange": [0, 12], "controls": [{"name": "K", "range": [0.001, 0.2], "value": 0.02, "label": "noise/signal K"}], "functions": [{"expr": "1/x", "label": "inverse filter 1/H", "color": "#dc2626"}, {"expr": "x/(x^2+K)", "label": "Wiener gain", "color": "#2563eb"}]}
```

Restoration powers astronomy, microscopy and forensics; modern methods replace the
hand-built prior with learned ones, but the degradation model is the same.

**Next:** shape-based processing — morphology.
""",
        ),
        _t(
            "Morphological operations",
            "10 min",
            """\
# Morphological operations

**Morphology** processes **shape**, usually on binary (black/white) images, by
probing them with a small **structuring element** (a disk, square or cross). The
two primitives:

- **Erosion** — a pixel stays on only if the structuring element fits **entirely**
  inside the foreground. Shrinks objects, removes thin protrusions and small specks.
- **Dilation** — turns on a pixel if the element **touches** any foreground. Grows
  objects, fills small holes and gaps.

Composing them gives the workhorses:

- **Opening** = erosion then dilation → removes small bright specks, keeps overall
  size. Great for cleaning salt noise.
- **Closing** = dilation then erosion → fills small dark holes and joins nearby
  blobs.

Other recipes follow: the **morphological gradient** (dilation − erosion) outlines
boundaries; **top-hat / black-hat** isolate features smaller than the element;
**thinning** reduces shapes to skeletons. Morphology is the cheap, reliable
clean-up stage after thresholding — used everywhere from OCR to defect inspection.

**Next:** carving the image into regions — segmentation.
""",
        ),
        _t(
            "Segmentation: thresholding, region growing & watershed",
            "11 min",
            """\
# Segmentation: thresholding, region growing & watershed

**Segmentation** partitions an image into meaningful regions (object vs background,
or several objects). Three workhorse families:

- **Thresholding** — pick a value $T$ and label pixels above/below it. **Otsu's
  method** chooses $T$ automatically by finding the split that **minimises the
  within-class variance** of the two groups (equivalently, maximises the
  between-class variance) — it works beautifully when the histogram is bimodal.
- **Region growing** — start from seed pixels and absorb neighbours that are
  similar (in intensity or colour) until a threshold stops the growth. Region
  splitting/merging is the top-down cousin.
- **Watershed** — treat intensity as terrain; "flood" from minima and build dams
  where basins meet. Powerful for touching objects, but prone to **over-segmentation**
  unless guided by markers.

Otsu sits at the **valley between the two peaks** of a bimodal histogram — the
threshold that best separates dark background from a bright object:

```plot
{"title": "Otsu threshold sits in the valley of a bimodal histogram", "xLabel": "intensity", "yLabel": "count", "xRange": [0, 255], "yRange": [0, 1.1], "functions": [{"expr": "exp(-(x-70)^2/(2*22^2)) + 0.9*exp(-(x-185)^2/(2*20^2))", "label": "histogram (two classes)", "color": "#2563eb"}], "points": [{"x": 128, "y": 0, "label": "Otsu threshold T", "color": "#dc2626", "size": 7}]}
```

Modern pipelines fold these ideas into learned segmentation (U-Net, Mask R-CNN),
but classical methods remain fast, label-free baselines.

**Next:** finding distinctive points — feature detection.
""",
        ),
        _t(
            "Feature detection: corners, blobs & SIFT",
            "11 min",
            """\
# Feature detection: corners, blobs & SIFT

To match, stitch or track images we need **features** — distinctive points that are
easy to find again under translation, rotation, scale and lighting changes.

- **Corners** — points where intensity changes in **two** directions (unlike an
  edge, which changes in one). The **Harris detector** examines the local
  structure tensor: if both of its eigenvalues are large, you have a corner; one
  large = edge; both small = flat. Corners are well-localised and repeatable.
- **Blobs** — compact regions that differ from their surroundings, found with the
  **Laplacian-of-Gaussian** (or its fast difference-of-Gaussians approximation)
  across multiple scales; the peak response also reveals the blob's **size**.
- **SIFT** — Scale-Invariant Feature Transform: detect blobs across a scale-space
  pyramid, assign each a dominant orientation, then describe its neighbourhood with
  a histogram of gradient orientations. The result is a **descriptor** that's robust
  to scale, rotation and modest lighting/viewpoint change, so the same point matches
  across very different photos. SURF, ORB and BRIEF are faster cousins.

These hand-crafted descriptors underpin **panorama stitching, structure-from-motion,
object recognition and visual SLAM** — and they motivate the learned features of
modern CNNs (covered in the Advanced track).

**Next:** moving and resampling pixels — geometric transforms.
""",
        ),
        _t(
            "Geometric transforms & interpolation",
            "10 min",
            """\
# Geometric transforms & interpolation

**Geometric transforms** move pixels to new locations: translate, rotate, scale,
shear (together the **affine** family) or the more general **projective**
(homography) used for perspective correction. In homogeneous coordinates an affine
map is a single matrix multiply:

$$\\begin{bmatrix} x' \\\\ y' \\\\ 1 \\end{bmatrix} =
\\begin{bmatrix} a & b & t_x \\\\ c & d & t_y \\\\ 0 & 0 & 1 \\end{bmatrix}
\\begin{bmatrix} x \\\\ y \\\\ 1 \\end{bmatrix}.$$

The catch: output pixel centres rarely map back to exact input pixel centres, so we
must **interpolate**. We use **inverse mapping** (for each output pixel, find where
it came from) to avoid holes, then interpolate the value:

- **Nearest-neighbour** — copy the closest pixel. Fast, but blocky/jagged.
- **Bilinear** — weighted average of the 4 surrounding pixels. Smooth, cheap.
- **Bicubic / Lanczos** — use 16+ neighbours for sharper, higher-quality resampling.

Downscaling needs **pre-filtering** (blur first) to avoid aliasing; upscaling trades
smoothness against ringing. These resampling rules are exactly the ones video codecs
use for **sub-pixel motion compensation** in the Advanced track.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Image & Video Processing — Advanced ──────────────────────────────────────

_IP_ADVANCED = SeedCourse(
    slug="image-processing-advanced",
    title="Image & Video Processing — Advanced",
    description=(
        "Compression and video: the DCT and the full JPEG pipeline, wavelets and "
        "JPEG2000, video fundamentals and temporal redundancy, motion estimation "
        "and compensation, modern video coding (MPEG/H.264/HEVC with I/P/B frames) "
        "and an intro to learning-based vision. Includes DCT-basis and rate-distortion "
        "plots plus JPEG and motion-estimation block diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Image compression & the DCT (JPEG)",
            "12 min",
            """\
# Image compression & the DCT (JPEG)

Compression exploits **redundancy**: neighbouring pixels are correlated, and the eye
tolerates losing high-frequency detail. **JPEG** is the canonical lossy pipeline.

```mermaid
flowchart LR
  RGB["RGB image"] --> YCC["Colour transform RGB to YCbCr + chroma subsample"]
  YCC --> BLK["Split into 8x8 blocks"]
  BLK --> DCT["2-D DCT per block"]
  DCT --> Q["Quantise (quality-controlled table)"]
  Q --> ZZ["Zig-zag scan"]
  ZZ --> ENT["Run-length + Huffman entropy coding"]
  ENT --> JPG["JPEG bitstream"]
```

The heart is the **Discrete Cosine Transform**. Each 8×8 block is rewritten as a sum
of cosine **basis patterns** of increasing frequency; natural images concentrate
energy in the low-frequency basis functions (top-left), leaving most high-frequency
coefficients near zero. **Quantisation** then divides by a table — coarser for
high frequencies (the eye won't miss them) — zeroing most of them. That is where the
loss, and the compression, happens.

Here are the first few 1-D DCT basis cosines $\\cos\\!\\big(\\tfrac{\\pi(2x+1)u}{16}\\big)$;
higher $u$ = finer ripples, the ones quantisation discards first:

```plot
{"title": "1-D DCT basis functions (low u kept, high u quantised away)", "xLabel": "pixel position x in block", "yLabel": "amplitude", "xRange": [0, 7], "yRange": [-1.2, 1.2], "functions": [{"expr": "cos(pi*(2*x+1)*1/16)", "label": "u = 1", "color": "#2563eb"}, {"expr": "cos(pi*(2*x+1)*2/16)", "label": "u = 2", "color": "#16a34a"}, {"expr": "cos(pi*(2*x+1)*4/16)", "label": "u = 4", "color": "#dc2626"}]}
```

The **quality** knob just scales the quantisation table — lower quality = bigger
divisors = more zeros = smaller file but visible **blocking** at the 8×8 edges.

**Next:** a different basis — wavelets and JPEG2000.
""",
        ),
        _t(
            "Wavelets & JPEG2000",
            "11 min",
            """\
# Wavelets & JPEG2000

The DCT is **global per block**: each coefficient mixes the whole 8×8 patch, so it
can't say *where* a feature is — and block boundaries cause **blocking artifacts**.
The **wavelet transform** fixes both by being **localised in space and frequency**.

A wavelet decomposition splits the image into an **approximation** (low-pass, a
shrunken blurry version) and three **detail** sub-bands (horizontal, vertical,
diagonal high-frequencies). Recurse on the approximation and you get a multi-
resolution **pyramid** — coarse structure plus progressively finer detail.

**JPEG2000** builds on this:

- One whole-image wavelet transform → no 8×8 blocks, so artifacts are gentle
  blur/ringing rather than ugly blocking.
- **Embedded** coding: bits are ordered most-significant-first, so you can truncate
  the stream anywhere for a lower bitrate — **scalable** quality and resolution from
  a single file.
- Built-in **region-of-interest** coding and a lossless mode (reversible transform).

It compresses better at low bitrates and is favoured in medical, cinema (Digital
Cinema Package) and archival imaging — though plain JPEG still dominates the web.

**Next:** from stills to video.
""",
        ),
        _t(
            "Video basics & temporal redundancy",
            "10 min",
            """\
# Video basics & temporal redundancy

A **video** is a sequence of images (**frames**) shown fast enough to look
continuous — typically 24–60 **fps**. That brings two new properties to exploit:

- **Temporal redundancy** — consecutive frames are nearly identical; mostly small
  regions move. Sending each frame whole (like a folder of JPEGs, "Motion JPEG")
  wastes enormous bandwidth.
- **Spatial redundancy** — still present within each frame (handled by DCT/transform
  coding, as in JPEG).

The big idea of video coding is to **predict** a frame from already-decoded ones and
transmit only the small **residual** (the difference). Frame types:

- **I-frame (Intra)** — coded on its own like a JPEG; a random-access entry point.
- **P-frame (Predicted)** — predicted from a **past** frame; send motion + residual.
- **B-frame (Bidirectional)** — predicted from **past and future** frames; smallest,
  but needs frame reordering at the encoder.

Because most frames are P/B and carry only residuals, video compresses **10–100×**
better than sending independent frames — temporal prediction is where the win lives.

**Next:** the engine of prediction — motion estimation.
""",
        ),
        _t(
            "Motion estimation & compensation",
            "12 min",
            """\
# Motion estimation & compensation

To predict a frame from another, the encoder must figure out **what moved where**.
That is **motion estimation**, and using the result to build the prediction is
**motion compensation**.

```mermaid
flowchart LR
  CUR["Current block"] --> ME["Motion estimation: search reference frame"]
  REF["Reference frame"] --> ME
  ME --> MV["Motion vector (dx, dy)"]
  MV --> MC["Motion compensation: shift reference block"]
  MC --> RES["Residual = current − prediction"]
  RES --> TQ["Transform + quantise residual"]
  MV --> BIT["Bitstream"]
  TQ --> BIT
```

**Block matching** is the standard: divide the frame into blocks (e.g. 16×16
macroblocks), and for each, search a window in the **reference** frame for the best
match — minimising a cost like **SAD** (sum of absolute differences). The offset to
the best match is the **motion vector**; the leftover error is the **residual**,
which is transform-coded like a small image.

Two refinements matter a lot:

- **Sub-pixel motion** — objects rarely move whole pixels, so codecs interpolate the
  reference to half/quarter-pixel positions (using the resampling from the
  Intermediate track) for much better matches.
- **Fast search** — exhaustive search is costly, so encoders use diamond/three-step
  searches and predict each vector from its neighbours.

Decoding is cheap and exact: shift the reference block by the motion vector, add the
decoded residual. **The encoder is hard, the decoder is easy** — by design.

**Next:** putting it together in real codecs.
""",
        ),
        _t(
            "Video coding: MPEG, H.264 & HEVC",
            "11 min",
            """\
# Video coding: MPEG, H.264 & HEVC

Real codecs wrap intra + inter prediction, transform, quantisation and entropy
coding into a standardised **bitstream**. Frames are grouped into a **GOP** (Group
of Pictures) like `I B B P B B P …`: an I-frame anchors random access, P/B frames
ride on prediction.

The lineage:

- **MPEG-1/2** — gave us I/P/B frames, 8×8 DCT and half-pixel motion; MPEG-2 still
  powers DVD and broadcast TV.
- **H.264 / AVC** — variable block sizes (down to 4×4), quarter-pixel motion,
  multiple reference frames, in-loop **deblocking**, and efficient **CABAC**
  arithmetic coding. Roughly **2×** the efficiency of MPEG-2; ubiquitous on the web.
- **H.265 / HEVC** — quad-tree **coding tree units** up to 64×64, 35 intra directions,
  better motion-vector prediction; ~**2× over H.264** at 4K/HDR. Successors **VP9**,
  **AV1** and **VVC (H.266)** push further (AV1/VVC ~30–50% past HEVC).

Every gain trades **bitrate vs distortion**, formalised as **rate-distortion**: the
encoder minimises $J = D + \\lambda R$ (distortion plus $\\lambda$ × bits) when choosing
modes. Better codecs push this curve down — same quality for fewer bits:

```plot
{"title": "Rate-distortion: newer codecs shift the curve down-left", "xLabel": "bitrate R (Mbps)", "yLabel": "distortion D (lower = better)", "xRange": [0.5, 10], "yRange": [0, 12], "functions": [{"expr": "10/x", "label": "older codec (MPEG-2)", "color": "#94a3b8"}, {"expr": "6/x", "label": "H.264", "color": "#2563eb"}, {"expr": "3.5/x", "label": "HEVC / AV1", "color": "#16a34a"}]}
```

**Next:** when the features are learned, not designed.
""",
        ),
        _t(
            "Learning-based vision & applications",
            "11 min",
            """\
# Learning-based vision & applications

For decades, vision used **hand-crafted** features (Sobel, SIFT, HOG) feeding a
classifier. **Convolutional neural networks (CNNs)** flipped this: they **learn** the
filters directly from data.

A CNN stacks:

- **Convolution layers** — banks of small learnable kernels, exactly the convolution
  from the Basics track, but the weights are trained, not fixed. Early layers learn
  edge/colour/blob detectors strikingly similar to Gabor filters and SIFT; deeper
  layers compose them into textures, parts and whole objects — a learned feature
  **hierarchy**.
- **Non-linearities** (ReLU) and **pooling/striding** that shrink spatial size while
  growing the channel (feature) depth.
- A **head** (fully-connected or another conv) for the task.

This powers the modern toolbox: **classification** (ResNet), **detection** (YOLO,
Faster R-CNN), **semantic/instance segmentation** (U-Net, Mask R-CNN), **super-
resolution** and **denoising** (often beating Wiener), **generative** models
(GANs, diffusion) and **vision transformers** that replace convolution with
attention. Learned methods are even entering **codecs** (learned in-loop filters,
end-to-end neural compression).

The throughline of this whole track: **convolution, frequency analysis, prediction
and transform coding** are the foundation — deep learning automates the *choice* of
filters, but the signal-processing ideas underneath are the same ones you have been
building since pixels and sampling.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


IMAGE_PROCESSING_COURSES: tuple[SeedCourse, ...] = (_IP_BASICS, _IP_INTERMEDIATE, _IP_ADVANCED)

__all__ = ["IMAGE_PROCESSING_COURSES"]
