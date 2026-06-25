"""Curated quiz questions for the Speech, Audio & Acoustics - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Linear predictive coding (LPC) & vocoders": (
            q(
                "What does linear predictive coding (LPC) model?",
                (
                    opt("The loudness contour of a recording"),
                    opt(
                        "Each sample as a weighted sum of previous samples, capturing the vocal-tract filter",
                        correct=True,
                    ),
                    opt("The room reverberation time"),
                    opt("The bit allocation of an MP3"),
                ),
                "LPC predicts each sample from past samples; its coefficients model the vocal-tract (all-pole) filter.",
            ),
            q(
                "In LPC, what does the residual (prediction error) represent?",
                (
                    opt("The vocal-tract filter"),
                    opt("The source excitation (pitch pulses or noise)", correct=True),
                    opt("The masking threshold"),
                    opt("The sample rate"),
                ),
                "The LPC coefficients are the filter; the leftover residual is the source excitation.",
            ),
            q(
                "How does a vocoder reconstruct speech at the decoder?",
                (
                    opt("By replaying the original waveform unchanged"),
                    opt(
                        "By driving the LPC filter with a pitch-pulse train (voiced) or noise (unvoiced)",
                        correct=True,
                    ),
                    opt("By applying a reverb tail"),
                    opt("By raising the bit depth"),
                ),
                "A vocoder excites the reconstructed LPC filter with pulses or noise to regenerate speech.",
            ),
        ),
        "Perceptual audio coding & masking (MP3/AAC)": (
            q(
                "What is the central trick of MP3/AAC perceptual coding?",
                (
                    opt("Doubling the sample rate"),
                    opt("Not coding what the listener cannot hear (masked sounds)", correct=True),
                    opt("Storing only the loudest channel"),
                    opt("Adding reverb to hide artifacts"),
                ),
                "Perceptual codecs discard or coarsely code masked, inaudible content.",
            ),
            q(
                "What is auditory masking?",
                (
                    opt("Muting a track during silence"),
                    opt(
                        "A loud tone raising the hearing threshold so quieter nearby sounds become inaudible",
                        correct=True,
                    ),
                    opt("Reversing the phase of a signal"),
                    opt("Adding a notch filter at 60 Hz"),
                ),
                "Masking is when a strong tone hides quieter sounds nearby in frequency (or time).",
            ),
            q(
                "Where does the psychoacoustic model send quantization noise in a perceptual encoder?",
                (
                    opt("Above the masking threshold so it is clearly audible"),
                    opt(
                        "Below the masking threshold in each band so it stays inaudible",
                        correct=True,
                    ),
                    opt("Into the highest-energy band regardless of hearing"),
                    opt("Into a separate uncompressed file"),
                ),
                "Bits are allocated so quantization noise stays below the masking threshold and is inaudible.",
            ),
        ),
        "The speech-recognition pipeline: MFCC features to models": (
            q(
                "What are MFCCs?",
                (
                    opt("The room impulse response coefficients"),
                    opt(
                        "Mel-frequency cepstral coefficients, a compact spectral-envelope feature",
                        correct=True,
                    ),
                    opt("The LPC residual samples"),
                    opt("The masking thresholds per band"),
                ),
                "MFCCs are mel-frequency cepstral coefficients, the classic compact ASR feature.",
            ),
            q(
                "Why is the mel filter bank used in MFCC extraction?",
                (
                    opt("To increase the sample rate"),
                    opt(
                        "To space frequency bands like the ear: fine at low frequency, coarse at high",
                        correct=True,
                    ),
                    opt("To remove all formants"),
                    opt("To convert text to phonemes"),
                ),
                "The mel scale groups frequencies perceptually, mimicking the ear's resolution.",
            ),
            q(
                "What does the language model contribute to an ASR system?",
                (
                    opt("It samples the microphone"),
                    opt(
                        "It scores how likely word sequences are, guiding the decoder", correct=True
                    ),
                    opt("It computes the FFT"),
                    opt("It cancels acoustic echo"),
                ),
                "The language model scores plausible word sequences, complementing the acoustic model.",
            ),
        ),
        "Speech synthesis (TTS) overview": (
            q(
                "What does the TTS front end do?",
                (
                    opt("Generates the final audio waveform"),
                    opt(
                        "Normalises text, converts graphemes to phonemes, and predicts prosody",
                        correct=True,
                    ),
                    opt("Cancels room reverberation"),
                    opt("Quantizes the spectrum for an MP3"),
                ),
                "The front end handles text normalisation, grapheme-to-phoneme and prosody prediction.",
            ),
            q(
                "In a modern neural TTS system, what does a neural vocoder do?",
                (
                    opt("Recognises words from audio"),
                    opt("Turns a predicted mel-spectrogram into a waveform", correct=True),
                    opt("Splits a song into stems"),
                    opt("Estimates the room RT60"),
                ),
                "A neural vocoder (WaveNet, HiFi-GAN) converts the predicted mel-spectrogram into audio.",
            ),
            q(
                "What is a drawback of concatenative TTS?",
                (
                    opt("It cannot produce any intelligible speech"),
                    opt("It can be brittle at the joins between recorded units", correct=True),
                    opt("It requires no recorded data at all"),
                    opt("It only works for music, not speech"),
                ),
                "Concatenative TTS stitches recorded units and can sound brittle at the joins.",
            ),
        ),
        "Room acoustics, beamforming & noise/echo cancellation": (
            q(
                "How does a room change the speech reaching a microphone?",
                (
                    opt(
                        "It convolves the speech with the room impulse response (reverberation)",
                        correct=True,
                    ),
                    opt("It increases the sample rate"),
                    opt("It removes the fundamental frequency"),
                    opt("It raises the bit depth"),
                ),
                "Room reflections convolve the speech with the room's impulse response, adding reverberation.",
            ),
            q(
                "How does a delay-and-sum beamformer favour a target direction?",
                (
                    opt("By amplifying every microphone equally"),
                    opt(
                        "By delaying each mic to realign the target direction so its signals add up",
                        correct=True,
                    ),
                    opt("By notching out 60 Hz hum"),
                    opt("By raising the compression ratio"),
                ),
                "Aligning the per-mic delays for one direction makes that target add coherently while off-axis noise partly cancels.",
            ),
            q(
                "What does acoustic echo cancellation (AEC) exploit?",
                (
                    opt("The unknown noise in the room"),
                    opt(
                        "The known far-end reference signal, modelled by an adaptive filter and subtracted",
                        correct=True,
                    ),
                    opt("The masking threshold of the ear"),
                    opt("The mel scale"),
                ),
                "AEC uses an adaptive filter on the known played-back reference to predict and subtract the echo.",
            ),
        ),
        "Modern deep-learning audio & applications": (
            q(
                "What do self-supervised models like wav2vec 2.0 and HuBERT do?",
                (
                    opt("Require fully labelled data for every task"),
                    opt(
                        "Learn powerful audio representations from largely unlabelled audio, then fine-tune",
                        correct=True,
                    ),
                    opt("Only work on text, not audio"),
                    opt("Replace the loudspeaker"),
                ),
                "Self-supervised models learn representations from unlabelled audio and are then fine-tuned per task.",
            ),
            q(
                "What is the 'cocktail-party' source-separation problem?",
                (
                    opt("Removing 60 Hz mains hum"),
                    opt("Isolating one speaker or stem from a mixture of sounds", correct=True),
                    opt("Increasing the dynamic range"),
                    opt("Converting text to phonemes"),
                ),
                "Source separation isolates one source (e.g. a speaker or instrument) from a mixture.",
            ),
            q(
                "Which classical concept remains the backbone even in deep-learning audio?",
                (
                    opt("The decibel reference pressure only"),
                    opt(
                        "Time-frequency analysis, the source-filter model and perceptual weighting",
                        correct=True,
                    ),
                    opt("The serial bitstream format of MP3"),
                    opt("The exact RT60 of a specific room"),
                ),
                "Spectrograms, source-filter thinking and perceptual weighting still underpin neural audio systems.",
            ),
        ),
    },
    final=(
        q(
            "What does LPC capture, and what is the residual?",
            (
                opt("LPC captures loudness; the residual is the noise floor"),
                opt(
                    "LPC captures the vocal-tract filter; the residual is the source excitation",
                    correct=True,
                ),
                opt("LPC captures pitch; the residual is the room"),
                opt("LPC captures the masking curve; the residual is the bit rate"),
            ),
            "LPC coefficients model the vocal-tract filter; the prediction residual is the excitation source.",
        ),
        q(
            "Perceptual codecs such as MP3 keep bits where the ear can tell. What enables this?",
            (
                opt("Doubling the sample rate"),
                opt(
                    "A psychoacoustic model of masking that hides quantization noise", correct=True
                ),
                opt("Adding reverberation"),
                opt("Storing the LPC residual losslessly"),
            ),
            "A psychoacoustic masking model lets the encoder keep quantization noise below the audible threshold.",
        ),
        q(
            "Which sequence describes the ASR front end correctly?",
            (
                opt("Waveform -> reverb -> compression -> text"),
                opt(
                    "Frame/window -> power spectrum -> mel filter bank -> log/DCT -> MFCCs",
                    correct=True,
                ),
                opt("Text -> phonemes -> prosody -> waveform"),
                opt("Microphone array -> beamform -> echo cancel -> MP3"),
            ),
            "MFCC extraction frames and windows, takes the spectrum, applies the mel bank, then log and DCT.",
        ),
        q(
            "Modern neural TTS predicts what intermediate representation before the vocoder?",
            (
                opt("An MP3 bitstream"),
                opt("A mel-spectrogram", correct=True),
                opt("A room impulse response"),
                opt("A set of LPC reflection coefficients only"),
            ),
            "Neural TTS predicts a mel-spectrogram from text, which a neural vocoder turns into a waveform.",
        ),
        q(
            "Which pair of techniques cleans up far-field, noisy capture?",
            (
                opt("Bit-depth reduction and dithering"),
                opt(
                    "Beamforming with a mic array and adaptive echo/noise cancellation",
                    correct=True,
                ),
                opt("Huffman coding and MDCT"),
                opt("Grapheme-to-phoneme and prosody prediction"),
            ),
            "Beamforming steers toward the talker; adaptive filters cancel echo and correlated noise.",
        ),
        q(
            "What is the throughline connecting classical and deep-learning audio?",
            (
                opt("Both ignore the human ear entirely"),
                opt(
                    "Time-frequency analysis, the source-filter model and perceptual weighting remain central",
                    correct=True,
                ),
                opt("Both rely solely on rectangular windows"),
                opt("Both avoid spectrograms"),
            ),
            "Spectrograms, source-filter reasoning and perceptual weighting underpin both classical and neural audio.",
        ),
    ),
)
