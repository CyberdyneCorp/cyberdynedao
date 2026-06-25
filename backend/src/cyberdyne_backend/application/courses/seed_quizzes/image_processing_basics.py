"""Curated quiz questions for the Image & Video Processing - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Digital images: pixels, sampling & colour": (
            q(
                "What does the quantisation step of digitising an image control?",
                (
                    opt("The number of pixels in the grid"),
                    opt(
                        "The number of discrete brightness levels each sample can take",
                        correct=True,
                    ),
                    opt("The physical size of the lens"),
                    opt("The frame rate of the camera"),
                ),
                "Quantisation rounds each sample's brightness to a fixed set of levels; too few causes banding.",
            ),
            q(
                "Why do codecs subsample the chroma channels but keep luma at full resolution?",
                (
                    opt("Because chroma is cheaper to store than luma in every format"),
                    opt(
                        "Because the eye is far more sensitive to luma (brightness) than to colour",
                        correct=True,
                    ),
                    opt("Because luma cannot be compressed at all"),
                    opt("Because RGB has no luma component to keep"),
                ),
                "The eye is much more sensitive to luma than chroma, so colour channels can be subsampled with little visible loss.",
            ),
            q(
                "How many numbers does a typical RGB colour pixel store?",
                (
                    opt("One intensity value"),
                    opt("Two: hue and saturation"),
                    opt("Three: red, green and blue", correct=True),
                    opt("Four: red, green, blue and luma"),
                ),
                "A greyscale pixel holds one intensity; an RGB colour pixel holds three values (R, G, B).",
            ),
        ),
        "Intensity transforms & gamma": (
            q(
                "An intensity (point) transform maps each pixel based on what?",
                (
                    opt("Its own value alone, independent of its neighbours", correct=True),
                    opt("The average of its 8 neighbours"),
                    opt("The gradient at that location"),
                    opt("The Fourier coefficient at that frequency"),
                ),
                "A point transform s = T(r) maps each pixel through a function of its own value, ignoring neighbours.",
            ),
            q(
                "In the gamma transform s = 255·(r/255)^γ, what does γ < 1 do?",
                (
                    opt("Darkens the mid-tones"),
                    opt("Brightens the mid-tones (lifts shadows)", correct=True),
                    opt("Leaves the image unchanged"),
                    opt("Inverts the image like a negative"),
                ),
                "Gamma below 1 lifts shadows and brightens mid-tones; gamma above 1 darkens them; gamma = 1 is the identity.",
            ),
            q(
                "Why are point operations so fast in practice?",
                (
                    opt("They use the FFT internally"),
                    opt(
                        "They can be precomputed as a 256-entry lookup table, applied per value not per pixel",
                        correct=True,
                    ),
                    opt("They only run on the edges of the image"),
                    opt("They require no arithmetic at all"),
                ),
                "A point transform is a lookup table over the 256 possible values, so it is computed once per distinct value.",
            ),
        ),
        "The histogram & equalisation": (
            q(
                "What does a histogram of an image represent?",
                (
                    opt("The spatial location of each edge"),
                    opt("How many pixels have each intensity value", correct=True),
                    opt("The Fourier spectrum of the image"),
                    opt("The gradient magnitude at each pixel"),
                ),
                "The histogram counts how many pixels take each intensity; its shape reveals contrast and exposure.",
            ),
            q(
                "Which function is used as the transform in histogram equalisation?",
                (
                    opt("The image's cumulative distribution function (CDF)", correct=True),
                    opt("A fixed gamma curve"),
                    opt("The Sobel operator"),
                    opt("A Gaussian kernel"),
                ),
                "Equalisation uses the image's own CDF as the transfer curve, spreading crowded values apart.",
            ),
            q(
                "Why is CLAHE often preferred over plain global equalisation?",
                (
                    opt("It is the only method that works on colour images"),
                    opt(
                        "It equalises locally with a clip limit, avoiding over-amplifying noise",
                        correct=True,
                    ),
                    opt("It runs without computing a histogram"),
                    opt("It always increases the image resolution"),
                ),
                "Global equalisation can over-amplify noise; CLAHE equalises tile-by-tile with a clip limit to control that.",
            ),
        ),
        "Spatial filtering & convolution": (
            q(
                "What is a smoothing/blur kernel an example of?",
                (
                    opt("A high-pass filter"),
                    opt("A low-pass filter", correct=True),
                    opt("A point transform"),
                    opt("An edge detector"),
                ),
                "A smoothing kernel averages neighbours, suppressing detail and noise, which is a low-pass operation.",
            ),
            q(
                "What property of a 2-D Gaussian kernel makes it cheap to apply?",
                (
                    opt("It has only one non-zero weight"),
                    opt(
                        "It is separable: one horizontal pass then one vertical pass",
                        correct=True,
                    ),
                    opt("It requires no border handling"),
                    opt("It is identical to a point transform"),
                ),
                "A Gaussian is separable, so a 2-D blur is done as a 1-D horizontal pass followed by a 1-D vertical pass.",
            ),
            q(
                "How does unsharp masking sharpen an image?",
                (
                    opt("By averaging each pixel with its neighbours"),
                    opt("By subtracting a blurred copy to boost edges", correct=True),
                    opt("By applying a gamma curve"),
                    opt("By equalising the histogram"),
                ),
                "Unsharp masking subtracts a blurred version (a high-pass operation) to emphasise edges and fine detail.",
            ),
        ),
        "Noise & denoising": (
            q(
                "Which filter best removes salt-and-pepper (impulse) noise while keeping edges?",
                (
                    opt("The mean (box) filter"),
                    opt("The median filter", correct=True),
                    opt("The Gaussian filter"),
                    opt("A gamma transform"),
                ),
                "The median filter replaces each pixel with the neighbourhood median, crushing impulse spikes while preserving edges.",
            ),
            q(
                "Why does the median resist outliers better than the mean?",
                (
                    opt("Because it averages more pixels than the mean"),
                    opt(
                        "Because a few extreme values shift the mean but not the middle value",
                        correct=True,
                    ),
                    opt("Because it ignores all dark pixels"),
                    opt("Because it operates in the frequency domain"),
                ),
                "Extreme salt/pepper values drag the mean but leave the median (middle value) essentially unchanged.",
            ),
            q(
                "What advantage do edge-preserving filters (bilateral, non-local means) offer?",
                (
                    opt("They remove noise without ever blurring real edges as much"),
                    opt("They average only over similar nearby pixels", correct=True),
                    opt("They require no parameters at all"),
                    opt("They convert the image to greyscale"),
                ),
                "Edge-preserving filters average only over pixels that are similar, so they denoise without smearing edges.",
            ),
        ),
        "Edge detection: gradients, Sobel & Canny": (
            q(
                "What signals an edge in terms of the image gradient?",
                (
                    opt("A large gradient magnitude", correct=True),
                    opt("A gradient magnitude of exactly zero"),
                    opt("A constant intensity region"),
                    opt("A high pixel value regardless of change"),
                ),
                "An edge is a location of sharp intensity change, which produces a large gradient magnitude.",
            ),
            q(
                "What does the Sobel operator add beyond a plain derivative?",
                (
                    opt("Histogram equalisation"),
                    opt("Smoothing in the perpendicular direction to resist noise", correct=True),
                    opt("Colour-space conversion"),
                    opt("Frequency-domain filtering"),
                ),
                "Sobel combines a derivative in one direction with smoothing in the other, so it finds edges while resisting noise.",
            ),
            q(
                "What does non-maximum suppression do in the Canny pipeline?",
                (
                    opt("Removes all edges below a single threshold"),
                    opt("Thins edges to a single-pixel width", correct=True),
                    opt("Smooths the image with a Gaussian"),
                    opt("Converts gradients to colour"),
                ),
                "Non-maximum suppression keeps only local gradient maxima, thinning edges to one pixel before thresholding.",
            ),
        ),
    },
    final=(
        q(
            "What are the two steps that turn a continuous scene into a digital image?",
            (
                opt("Convolution and thresholding"),
                opt("Sampling (spatial grid) and quantisation (brightness levels)", correct=True),
                opt("Equalisation and gamma correction"),
                opt("Erosion and dilation"),
            ),
            "Sampling places the scene on a grid; quantisation rounds each sample's brightness to discrete levels.",
        ),
        q(
            "Which colour space, separating luma from chroma, is used by JPEG and video?",
            (
                opt("RGB"),
                opt("YCbCr", correct=True),
                opt("CMYK"),
                opt("Grayscale"),
            ),
            "YCbCr separates a luma channel from two chroma channels, which lets codecs subsample colour.",
        ),
        q(
            "Histogram equalisation uses which curve as its transform?",
            (
                opt("A fixed gamma curve"),
                opt("The image's cumulative distribution function", correct=True),
                opt("The Sobel kernel"),
                opt("A box-filter kernel"),
            ),
            "Equalisation maps intensities through the image's CDF to spread crowded values across the range.",
        ),
        q(
            "A blurring kernel is a low-pass filter; what kind of filter sharpens?",
            (
                opt("A high-pass filter", correct=True),
                opt("A low-pass filter"),
                opt("A median filter"),
                opt("A point transform"),
            ),
            "Sharpening boosts high frequencies (edges), so it is a high-pass operation, e.g. unsharp masking or Laplacian.",
        ),
        q(
            "For salt-and-pepper noise, which filter is the right choice?",
            (
                opt("Mean filter"),
                opt("Gaussian filter"),
                opt("Median filter", correct=True),
                opt("Gamma transform"),
            ),
            "The non-linear median filter removes impulse spikes while keeping edges crisp.",
        ),
        q(
            "Which statement about the Canny edge detector is correct?",
            (
                opt(
                    "It uses double thresholding with hysteresis to keep connected edges",
                    correct=True,
                ),
                opt("It equalises the histogram before detecting edges"),
                opt("It detects edges purely from the colour channels"),
                opt("It needs no smoothing because it is noise-free"),
            ),
            "Canny smooths, computes gradients, applies non-maximum suppression, then double thresholding with hysteresis.",
        ),
    ),
)
