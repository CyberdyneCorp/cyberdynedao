"""Curated quiz questions for the Image & Video Processing - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The 2-D Fourier transform & frequency-domain filtering": (
            q(
                "In a centred 2-D Fourier spectrum, what lives near the centre?",
                (
                    opt("High frequencies and fine edge detail"),
                    opt("Low frequencies and smooth regions (with DC at the centre)", correct=True),
                    opt("Only the noise"),
                    opt("The colour channels"),
                ),
                "The centre holds the DC term and low frequencies (smooth areas); high frequencies (detail) sit toward the edges.",
            ),
            q(
                "What does the convolution theorem let you do?",
                (
                    opt(
                        "Replace convolution in space with multiplication in the frequency domain",
                        correct=True,
                    ),
                    opt("Replace the histogram with its CDF"),
                    opt("Convert RGB to YCbCr instantly"),
                    opt("Avoid quantisation in JPEG"),
                ),
                "Convolution in space equals multiplication in frequency, so large filters can be applied efficiently via the FFT.",
            ),
            q(
                "Why does an ideal (sharp-cutoff) low-pass filter cause ringing?",
                (
                    opt("Because it adds noise to the centre"),
                    opt(
                        "Because its abrupt cutoff corresponds to oscillations in the spatial domain",
                        correct=True,
                    ),
                    opt("Because it removes the DC term"),
                    opt("Because it operates only on the colour channels"),
                ),
                "A hard frequency cutoff yields a sinc-like spatial kernel that oscillates, producing ringing; Butterworth rolls off gradually.",
            ),
        ),
        "Image restoration & the Wiener filter": (
            q(
                "How does restoration differ from enhancement?",
                (
                    opt("Restoration only changes colour, enhancement changes brightness"),
                    opt(
                        "Restoration recovers the original using a known degradation model, enhancement just makes images look better",
                        correct=True,
                    ),
                    opt("They are identical operations"),
                    opt("Restoration always discards high frequencies"),
                ),
                "Restoration inverts a known degradation (blur + noise) to recover the original; enhancement only improves appearance.",
            ),
            q(
                "Why does naive inverse filtering fail in the presence of noise?",
                (
                    opt("It blurs the image too much"),
                    opt(
                        "Dividing by H explodes where H is near zero, amplifying noise catastrophically",
                        correct=True,
                    ),
                    opt("It removes the DC term"),
                    opt("It only works on binary images"),
                ),
                "Inverse filtering divides spectra by H; where H is near zero the gain blows up and noise is amplified.",
            ),
            q(
                "What does the Wiener filter balance via its term K?",
                (
                    opt("Brightness against contrast"),
                    opt(
                        "Deblurring against noise amplification (using the noise/signal ratio)",
                        correct=True,
                    ),
                    opt("Spatial resolution against frame rate"),
                    opt("Hue against saturation"),
                ),
                "The Wiener filter uses K (noise-to-signal ratio) so its gain stays bounded where the inverse would explode.",
            ),
        ),
        "Morphological operations": (
            q(
                "What does erosion do to foreground objects in a binary image?",
                (
                    opt("Grows them and fills holes"),
                    opt("Shrinks them and removes thin protrusions and small specks", correct=True),
                    opt("Detects their edges in colour"),
                    opt("Equalises their histogram"),
                ),
                "Erosion keeps a pixel only if the structuring element fits entirely inside the foreground, shrinking objects.",
            ),
            q(
                "Opening is defined as which sequence of operations?",
                (
                    opt("Dilation then erosion"),
                    opt("Erosion then dilation", correct=True),
                    opt("Two erosions"),
                    opt("A gradient then a threshold"),
                ),
                "Opening is erosion followed by dilation; it removes small bright specks while keeping overall object size.",
            ),
            q(
                "Which operation fills small dark holes and joins nearby blobs?",
                (
                    opt("Opening"),
                    opt("Closing", correct=True),
                    opt("Erosion"),
                    opt("Thresholding"),
                ),
                "Closing (dilation then erosion) fills small holes and bridges small gaps between nearby foreground regions.",
            ),
        ),
        "Segmentation: thresholding, region growing & watershed": (
            q(
                "What does Otsu's method choose automatically?",
                (
                    opt("A kernel size for blurring"),
                    opt(
                        "A threshold that minimises within-class variance (separates the two histogram peaks)",
                        correct=True,
                    ),
                    opt("The number of segments via clustering"),
                    opt("The gamma value for display"),
                ),
                "Otsu picks the threshold that minimises within-class variance (equivalently maximises between-class variance).",
            ),
            q(
                "How does region growing form a segment?",
                (
                    opt("By thresholding the whole image at once"),
                    opt(
                        "By starting from seed pixels and absorbing similar neighbours until a criterion stops it",
                        correct=True,
                    ),
                    opt("By computing the Fourier transform"),
                    opt("By eroding the foreground repeatedly"),
                ),
                "Region growing starts at seeds and adds neighbouring pixels that are similar enough until growth stops.",
            ),
            q(
                "What is a common drawback of the watershed transform?",
                (
                    opt("It cannot handle greyscale images"),
                    opt("It tends to over-segment unless guided by markers", correct=True),
                    opt("It only works on binary images"),
                    opt("It requires a bimodal histogram"),
                ),
                "Watershed floods from every minimum and is prone to over-segmentation unless seeded with markers.",
            ),
        ),
        "Feature detection: corners, blobs & SIFT": (
            q(
                "How does a corner differ from an edge in terms of intensity change?",
                (
                    opt("A corner changes in two directions; an edge changes in one", correct=True),
                    opt("A corner has no intensity change at all"),
                    opt("An edge changes in two directions; a corner in one"),
                    opt("They change identically"),
                ),
                "A corner shows strong intensity variation in two directions (both structure-tensor eigenvalues large); an edge in one.",
            ),
            q(
                "What makes a SIFT descriptor robust across very different photos?",
                (
                    opt("It uses only the raw RGB values"),
                    opt(
                        "Scale-space detection plus an orientation and a gradient-histogram descriptor give invariance to scale and rotation",
                        correct=True,
                    ),
                    opt("It thresholds the histogram"),
                    opt("It applies the Wiener filter first"),
                ),
                "SIFT detects features across scales, assigns an orientation, and describes them with gradient histograms, giving scale/rotation invariance.",
            ),
            q(
                "What does the Laplacian-of-Gaussian response across scales reveal about a blob?",
                (
                    opt("Its colour"),
                    opt("Its characteristic size (the scale of peak response)", correct=True),
                    opt("Its motion vector"),
                    opt("Its compression ratio"),
                ),
                "Searching LoG (or DoG) across scales finds blobs and the scale of the peak response indicates the blob's size.",
            ),
        ),
        "Geometric transforms & interpolation": (
            q(
                "Why do geometric transforms use inverse mapping?",
                (
                    opt("Because it is faster to compute the forward matrix"),
                    opt(
                        "So every output pixel finds a source location, avoiding holes in the result",
                        correct=True,
                    ),
                    opt("Because forward mapping cannot rotate images"),
                    opt("To skip interpolation entirely"),
                ),
                "Inverse mapping asks where each output pixel came from, guaranteeing every output pixel is filled (no holes).",
            ),
            q(
                "Which interpolation method averages the 4 surrounding pixels?",
                (
                    opt("Nearest-neighbour"),
                    opt("Bilinear", correct=True),
                    opt("Bicubic"),
                    opt("Lanczos"),
                ),
                "Bilinear interpolation takes a weighted average of the 4 nearest pixels; nearest-neighbour copies just one.",
            ),
            q(
                "Why should downscaling pre-filter (blur) the image first?",
                (
                    opt("To increase the bit depth"),
                    opt("To avoid aliasing from removed high frequencies", correct=True),
                    opt("To equalise the histogram"),
                    opt("To convert it to YCbCr"),
                ),
                "Reducing resolution discards high frequencies; blurring first prevents those from aliasing into the downscaled image.",
            ),
        ),
    },
    final=(
        q(
            "What is the key advantage of filtering in the frequency domain?",
            (
                opt("It needs no Fourier transform"),
                opt(
                    "Convolution becomes a simple multiplication of the spectrum by a mask",
                    correct=True,
                ),
                opt("It removes all colour information"),
                opt("It avoids any loss of detail"),
            ),
            "By the convolution theorem, spatial convolution becomes multiplication in frequency, so filtering is masking the spectrum.",
        ),
        q(
            "The Wiener filter improves on the inverse filter mainly because it does what?",
            (
                opt("Keeps its gain bounded where the blur response is near zero", correct=True),
                opt("Ignores the noise entirely"),
                opt("Works only on binary images"),
                opt("Doubles the resolution"),
            ),
            "The Wiener term K keeps the restoration gain bounded where H is small, preventing the noise blow-up of inverse filtering.",
        ),
        q(
            "Which composite morphological operation removes small bright specks while preserving object size?",
            (
                opt("Closing"),
                opt("Opening", correct=True),
                opt("Dilation"),
                opt("Morphological gradient"),
            ),
            "Opening (erosion then dilation) clears small bright noise while keeping the overall size of larger objects.",
        ),
        q(
            "Otsu's thresholding works best when the histogram is shaped how?",
            (
                opt("Flat / uniform"),
                opt("Bimodal (two clear peaks)", correct=True),
                opt("A single sharp spike"),
                opt("Monotonically increasing"),
            ),
            "Otsu separates two classes, so it works best on a bimodal histogram where the threshold sits in the valley.",
        ),
        q(
            "What is the defining property a good feature detector aims for?",
            (
                opt("Maximum brightness"),
                opt(
                    "Repeatability: the same point is found again under scale, rotation and lighting changes",
                    correct=True,
                ),
                opt("Minimum file size"),
                opt("A flat region of constant intensity"),
            ),
            "Features must be repeatable and distinctive so the same physical point can be matched across images.",
        ),
        q(
            "When resampling during a geometric transform, what does bilinear interpolation use?",
            (
                opt("Only the single nearest pixel"),
                opt("A weighted average of the 4 nearest pixels", correct=True),
                opt("The full image histogram"),
                opt("The Fourier spectrum"),
            ),
            "Bilinear interpolation blends the 4 surrounding pixels, giving smoother results than nearest-neighbour.",
        ),
    ),
)
