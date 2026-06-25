"""Curated quiz questions for the Image & Video Processing - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Image compression & the DCT (JPEG)": (
            q(
                "Why does the DCT help compress natural images?",
                (
                    opt("It increases the number of non-zero coefficients"),
                    opt(
                        "It concentrates energy in a few low-frequency coefficients, leaving most high-frequency ones near zero",
                        correct=True,
                    ),
                    opt("It converts the image to binary"),
                    opt("It removes all colour"),
                ),
                "Natural-image energy concentrates in low-frequency DCT coefficients, so most high-frequency ones are near zero and can be discarded.",
            ),
            q(
                "In the JPEG pipeline, where does the (lossy) information loss occur?",
                (
                    opt("During the zig-zag scan"),
                    opt("During quantisation of the DCT coefficients", correct=True),
                    opt("During Huffman coding"),
                    opt("During RGB to YCbCr conversion"),
                ),
                "Quantisation divides coefficients by a table and rounds, zeroing many of them; that is the lossy, compressing step.",
            ),
            q(
                "What artifact appears at low JPEG quality settings?",
                (
                    opt("Salt-and-pepper noise"),
                    opt("Blocking at the 8x8 block boundaries", correct=True),
                    opt("Chromatic aberration in the lens"),
                    opt("Motion blur"),
                ),
                "Coarse quantisation per 8x8 block makes block edges visible, the classic JPEG blocking artifact.",
            ),
        ),
        "Wavelets & JPEG2000": (
            q(
                "What key property do wavelets have that the block DCT lacks?",
                (
                    opt("They are localised in both space and frequency", correct=True),
                    opt("They ignore high frequencies"),
                    opt("They only work on binary images"),
                    opt("They require no transform"),
                ),
                "Wavelets are localised in space and frequency, giving multi-resolution detail and avoiding block boundaries.",
            ),
            q(
                "How does JPEG2000 avoid the blocking artifacts seen in JPEG?",
                (
                    opt("By using a larger 16x16 DCT block"),
                    opt(
                        "By transforming the whole image with wavelets instead of 8x8 blocks",
                        correct=True,
                    ),
                    opt("By skipping quantisation"),
                    opt("By converting to RGB first"),
                ),
                "JPEG2000 applies a whole-image wavelet transform, so it has no 8x8 blocks and degrades as gentle blur/ringing.",
            ),
            q(
                "What does JPEG2000's embedded coding enable?",
                (
                    opt("Lossless audio storage"),
                    opt(
                        "Scalable quality/resolution by truncating the stream at any point",
                        correct=True,
                    ),
                    opt("Faster motion estimation"),
                    opt("Removal of the DC term"),
                ),
                "Embedded, most-significant-first coding lets you truncate the bitstream anywhere for scalable quality and resolution.",
            ),
        ),
        "Video basics & temporal redundancy": (
            q(
                "What is temporal redundancy in video?",
                (
                    opt("Repeated colours within a single frame"),
                    opt("The near-identical content of consecutive frames", correct=True),
                    opt("The duplication of audio tracks"),
                    opt("The overhead of the file header"),
                ),
                "Consecutive frames are nearly identical, so most content repeats over time; codecs predict frames to exploit this.",
            ),
            q(
                "Which frame type is coded on its own and serves as a random-access point?",
                (
                    opt("I-frame (intra)", correct=True),
                    opt("P-frame (predicted)"),
                    opt("B-frame (bidirectional)"),
                    opt("Residual frame"),
                ),
                "An I-frame is coded independently like a JPEG and is an entry point for random access.",
            ),
            q(
                "Why does video compress far better than a folder of independent JPEGs?",
                (
                    opt("Because frames are stored at lower resolution"),
                    opt(
                        "Because most frames send only motion plus a small residual, not the whole image",
                        correct=True,
                    ),
                    opt("Because audio is removed"),
                    opt("Because colour is discarded"),
                ),
                "P/B frames transmit only motion vectors and small residuals, giving 10-100x better compression than independent frames.",
            ),
        ),
        "Motion estimation & compensation": (
            q(
                "What does block matching produce for each block?",
                (
                    opt("A histogram"),
                    opt(
                        "A motion vector pointing to the best match in the reference frame",
                        correct=True,
                    ),
                    opt("A quantisation table"),
                    opt("A colour-space conversion"),
                ),
                "Block matching searches the reference frame for the best-matching block; the offset is the motion vector.",
            ),
            q(
                "What is the residual in motion compensation?",
                (
                    opt("The motion vector itself"),
                    opt(
                        "The difference between the current block and the motion-compensated prediction",
                        correct=True,
                    ),
                    opt("The Huffman code length"),
                    opt("The frame rate"),
                ),
                "The residual is current minus prediction; it is transform-coded like a small image and added back at decode time.",
            ),
            q(
                "Why do codecs interpolate the reference frame to sub-pixel positions?",
                (
                    opt("To reduce the frame rate"),
                    opt(
                        "Because objects rarely move a whole number of pixels, so half/quarter-pixel matches are better",
                        correct=True,
                    ),
                    opt("To convert RGB to YCbCr"),
                    opt("To remove the DC coefficient"),
                ),
                "Real motion is usually fractional; sub-pixel interpolation of the reference yields much better matches and smaller residuals.",
            ),
        ),
        "Video coding: MPEG, H.264 & HEVC": (
            q(
                "What is a GOP (Group of Pictures)?",
                (
                    opt("A group of pixels in one block"),
                    opt(
                        "A sequence of frames such as I B B P ... that structures prediction and random access",
                        correct=True,
                    ),
                    opt("A quantisation table"),
                    opt("A colour palette"),
                ),
                "A GOP groups frames (e.g. I B B P B B P) with an I-frame anchoring random access and P/B frames using prediction.",
            ),
            q(
                "Roughly how does H.264 compare to MPEG-2 in efficiency?",
                (
                    opt("About half as efficient"),
                    opt("About the same"),
                    opt(
                        "About twice as efficient (same quality at half the bitrate)", correct=True
                    ),
                    opt("Ten times as efficient"),
                ),
                "H.264 roughly doubles MPEG-2 efficiency via variable block sizes, quarter-pixel motion, multiple references and CABAC.",
            ),
            q(
                "What does rate-distortion optimisation minimise when choosing coding modes?",
                (
                    opt("Only the bitrate, ignoring quality"),
                    opt("J = D + lambda·R, trading distortion against bits", correct=True),
                    opt("The frame rate"),
                    opt("The number of colour channels"),
                ),
                "Encoders minimise J = D + lambda*R, balancing distortion D against bit cost R when selecting modes.",
            ),
        ),
        "Learning-based vision & applications": (
            q(
                "How do CNNs differ from classical vision pipelines that use SIFT or HOG?",
                (
                    opt("They use no convolution at all"),
                    opt(
                        "They learn the filters from data rather than using hand-crafted ones",
                        correct=True,
                    ),
                    opt("They only work on binary images"),
                    opt("They require no training data"),
                ),
                "CNNs learn their convolution kernels directly from data, replacing hand-designed features like SIFT/HOG.",
            ),
            q(
                "What do early convolution layers of a trained CNN tend to learn?",
                (
                    opt("Whole-object templates only"),
                    opt(
                        "Edge, colour and blob detectors resembling Gabor/SIFT-like filters",
                        correct=True,
                    ),
                    opt("Huffman codes"),
                    opt("Motion vectors"),
                ),
                "Early layers learn simple edge/colour/blob detectors; deeper layers compose them into textures, parts and objects.",
            ),
            q(
                "Which task pairing with a typical architecture is correct?",
                (
                    opt("Semantic segmentation with U-Net", correct=True),
                    opt("Object detection with the DCT"),
                    opt("Classification with the watershed transform"),
                    opt("Denoising with Huffman coding"),
                ),
                "U-Net is a standard architecture for semantic segmentation; detection uses YOLO/Faster R-CNN, classification uses ResNet.",
            ),
        ),
    },
    final=(
        q(
            "What is the core transform at the heart of JPEG?",
            (
                opt("The Discrete Cosine Transform (DCT)", correct=True),
                opt("The Hough transform"),
                opt("The watershed transform"),
                opt("The Sobel operator"),
            ),
            "JPEG applies a 2-D DCT to each 8x8 block, then quantises and entropy-codes the coefficients.",
        ),
        q(
            "What advantage do wavelets give JPEG2000 over block-DCT JPEG?",
            (
                opt("Smaller headers only"),
                opt(
                    "Whole-image, multi-resolution coding with no 8x8 blocking and scalable quality",
                    correct=True,
                ),
                opt("No need for entropy coding"),
                opt("Lossy-only operation"),
            ),
            "A whole-image wavelet transform removes blocking and supports embedded, scalable quality/resolution coding.",
        ),
        q(
            "Which frame type is typically the smallest because it predicts from both past and future?",
            (
                opt("I-frame"),
                opt("P-frame"),
                opt("B-frame", correct=True),
                opt("Key frame"),
            ),
            "B-frames are bidirectionally predicted from past and future references, so they carry the least data.",
        ),
        q(
            "In motion estimation, what is transmitted alongside the motion vector?",
            (
                opt("The full reference frame"),
                opt("The residual (transform-coded difference from the prediction)", correct=True),
                opt("The histogram of the block"),
                opt("The colour palette"),
            ),
            "The encoder sends the motion vector plus the small residual; the decoder shifts the reference and adds the residual.",
        ),
        q(
            "How does HEVC (H.265) generally compare to H.264?",
            (
                opt("About half the efficiency"),
                opt("About 2x more efficient, especially at 4K/HDR", correct=True),
                opt("Identical efficiency"),
                opt("Only useful for still images"),
            ),
            "HEVC roughly doubles H.264 efficiency using large quad-tree coding units and better prediction, helping 4K/HDR.",
        ),
        q(
            "What is the unifying idea connecting classical filters and CNN features?",
            (
                opt("Both rely on the watershed transform"),
                opt(
                    "Both use convolution; CNNs learn the kernels instead of hand-designing them",
                    correct=True,
                ),
                opt("Both avoid any spatial filtering"),
                opt("Both require bimodal histograms"),
            ),
            "CNN convolution layers are the same operation as classical filtering, but the kernels are learned from data.",
        ),
    ),
)
