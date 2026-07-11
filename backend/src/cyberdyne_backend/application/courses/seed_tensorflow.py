"""Academy seed content — TensorFlow — Basics.

A hands-on introduction to modern TensorFlow (2.x with Keras): tensors
and variables, automatic differentiation with GradientTape, building
models with Keras layers, the compile/fit workflow, input pipelines with
tf.data, writing a custom training loop, and a complete end-to-end digit
classifier with saving/loading. Every lesson is a direct explanation
with runnable examples and a mermaid diagram, followed by a checkpoint
quiz; the course closes with a comprehensive final quiz.

Companion to ``seed_pytorch`` — the two courses train the same digit
classifier so learners can compare the frameworks side by side.
"""

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


_TENSORFLOW_BASICS = SeedCourse(
    slug="tensorflow-basics",
    title="TensorFlow — Basics",
    description=(
        "Deep learning with modern TensorFlow (2.x + Keras) from zero: "
        "tensors and variables, GradientTape, Keras models, compile/fit, "
        "tf.data pipelines, custom training loops and a complete digit "
        "classifier - explained directly, with runnable examples and a "
        "diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # ── Welcome ──────────────────────────────────────────────────
        _t(
            "Welcome — how this course works",
            "4 min",
            """# TensorFlow — Basics

TensorFlow is one of the two dominant deep-learning frameworks, with an
ecosystem that reaches from research notebooks to phones (LiteRT) and
the browser (TensorFlow.js). If you know basic Python and a little
NumPy-style array thinking, this course takes you to the point where you
can build, train and save a real neural network.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it in runnable code, and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **What TensorFlow is** - tensors, eager execution, Keras, the
   ecosystem
2. **Tensors and variables** - immutable data, mutable weights
3. **GradientTape** - how gradients are computed for you
4. **Keras models** - `Sequential`, layers and activations
5. **compile and fit** - the built-in training workflow
6. **tf.data** - input pipelines: batch, shuffle, prefetch
7. **Custom training loops** - the five steps under fit's hood
8. **End to end** - a digit classifier, evaluation, saving and loading

Install with `pip install tensorflow` - CPU is fine for this whole
course; every example runs in seconds.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome — how this course works",
            (
                q(
                    "What prior knowledge does this course assume?",
                    (
                        opt("Experience with PyTorch"),
                        opt("Basic Python and some array thinking", correct=True),
                        opt("A CUDA-capable GPU"),
                        opt("Graduate-level calculus"),
                    ),
                    "Python plus NumPy-style array intuition is enough; a GPU is "
                    "optional - every example runs on CPU in seconds.",
                ),
                q(
                    "Which API does modern TensorFlow use for building models?",
                    (
                        opt("Keras, integrated as tf.keras", correct=True),
                        opt("Sessions and placeholders from TensorFlow 1"),
                        opt("Raw C++ graph definitions"),
                        opt("An external Lua scripting layer"),
                    ),
                    "Since TensorFlow 2, Keras is the built-in high-level API - "
                    "Sequential models, layers, compile and fit.",
                ),
            ),
        ),
        # ── 1. What is TensorFlow ────────────────────────────────────
        _t(
            "What is TensorFlow?",
            "8 min",
            """# What is TensorFlow?

TensorFlow is three things stacked on top of each other:

1. **A tensor library** - like NumPy, but every operation can also run
   on a GPU or TPU. A tensor is an n-dimensional array: a scalar, a
   vector, a matrix, a batch of images.
2. **An autodiff engine** - `tf.GradientTape` records the operations
   you perform and computes gradients through them. Gradients are what
   training uses to improve a model.
3. **Keras** (`tf.keras`) - the high-level toolkit of layers, losses,
   optimizers and the `fit` training workflow built on those two.

```python
import tensorflow as tf

x = tf.constant([1.0, 2.0, 3.0])
w = tf.Variable([0.5, 0.5, 0.5])

with tf.GradientTape() as tape:
    y = tf.reduce_sum(x * w)      # y = 3.0, recorded on the tape

grad = tape.gradient(y, w)        # dy/dw = x
print(grad)                       # tf.Tensor([1. 2. 3.], ...)
```

Since TensorFlow 2, code runs **eagerly**: operations execute
immediately, like NumPy, so ordinary `if` statements, loops and
`print()` work while you develop. When you need production speed, the
same code compiles to a graph with the **`@tf.function`** decorator -
develop eagerly, deploy compiled.

The other signature strength is the **ecosystem**: SavedModel exports
serve in TF Serving, run on phones via LiteRT (TensorFlow Lite), and in
the browser with TensorFlow.js.

```mermaid
graph TD
    T["Tensor library like NumPy"] --> A["GradientTape records operations"]
    A --> G["Gradients computed automatically"]
    T --> D["Same code on CPU GPU TPU"]
    A --> K["Keras layers losses fit"]
    K --> M["Trainable models"]
    M --> E["SavedModel to serving mobile browser"]
```

The one thing to remember: TensorFlow is NumPy with gradients and
accelerators, plus Keras on top - everything in this course is one of
those layers unfolding.
""",
        ),
        quiz_lesson(
            "Quiz: What is TensorFlow?",
            (
                q(
                    "What does eager execution mean in TensorFlow 2?",
                    (
                        opt("Models train before the data arrives"),
                        opt(
                            "Operations run immediately like NumPy, so normal Python "
                            "control flow and debugging work",
                            correct=True,
                        ),
                        opt("The GPU is always used even when absent"),
                        opt("Code must be compiled before it can run"),
                    ),
                    "TF2 executes eagerly by default - the TF1 world of building a "
                    "graph first and running it in a Session is gone.",
                ),
                q(
                    "What is @tf.function for?",
                    (
                        opt(
                            "Compiling a Python function into a TensorFlow graph for "
                            "production speed while still developing eagerly",
                            correct=True,
                        ),
                        opt("Marking a function as GPU-only"),
                        opt("Disabling gradients inside a function"),
                        opt("Importing Keras layers"),
                    ),
                    "Develop eagerly, then decorate hot paths - the same code gains "
                    "graph performance without a rewrite.",
                ),
                q(
                    "Which of these is part of TensorFlow's deployment ecosystem?",
                    (
                        opt(
                            "SavedModel served by TF Serving, LiteRT on mobile, TensorFlow.js in the browser",
                            correct=True,
                        ),
                        opt("Direct compilation to Excel macros"),
                        opt("A built-in web framework for dashboards"),
                        opt("Automatic conversion to Java applets"),
                    ),
                    "One trained model exports to servers, phones and browsers - a "
                    "major reason teams pick TensorFlow.",
                ),
            ),
        ),
        # ── 2. Tensors & variables ───────────────────────────────────
        _t(
            "Tensors and variables",
            "10 min",
            """# Tensors and variables

Everything in TensorFlow is a tensor: inputs, weights, predictions, the
loss. TensorFlow splits them into two kinds - and the split matters:

- **`tf.constant`** - immutable values: your data, intermediate
  results. Operations never modify a tensor; they return new ones.
- **`tf.Variable`** - mutable state: the model's weights. Training
  updates variables in place with `assign` / `assign_sub`.

```python
import tensorflow as tf

a = tf.constant([[1.0, 2.0], [3.0, 4.0]])  # immutable data
z = tf.zeros([3, 4])                        # 3x4 of zeros
r = tf.random.normal([2, 3])                # random values
w = tf.Variable(tf.zeros([2, 2]))           # mutable weights
w.assign_add(tf.ones([2, 2]))               # in-place update
```

Every tensor has the attributes you will check constantly:

```python
a.shape    # TensorShape([2, 2]) - the dimensions
a.dtype    # tf.float32          - the number type
a.numpy()  # back to a NumPy array whenever you want to look
```

**Shape is everything.** Most TensorFlow bugs are shape bugs, and
`tf.reshape` is the daily tool:

```python
x = tf.range(12)                  # shape [12]
m = tf.reshape(x, [3, 4])         # shape [3, 4]
f = tf.reshape(m, [-1])           # back to [12]; -1 means "figure it out"
b = tf.expand_dims(m, axis=0)     # shape [1, 3, 4] - add a batch dim
```

**Operations** are elementwise by default, `@` (or `tf.matmul`) is
matrix multiplication, and **broadcasting** stretches compatible shapes
automatically:

```python
u = tf.constant([[1.0], [2.0], [3.0]])   # shape [3, 1]
v = tf.constant([10.0, 20.0])            # shape [2]
print(u + v)                              # shape [3, 2] - broadcast
w2 = tf.random.normal([4, 3]) @ tf.random.normal([3, 2])  # shape [4, 2]
```

Reductions collapse dimensions: `tf.reduce_sum(t)`,
`tf.reduce_mean(t, axis=0)`, `tf.argmax(t, axis=1)` - the `axis`
argument says which dimension disappears.

```mermaid
graph LR
    C["constant immutable data"] --> OPS["Elementwise ops and matmul"]
    V["Variable mutable weights"] --> OPS
    OPS --> BR["Broadcasting aligns shapes"]
    OPS --> RD["Reductions sum mean argmax"]
    SH["shape dtype numpy"] --> DBG["First stop when debugging"]
```

Constants for data, Variables for weights, and print .shape first when
anything breaks.
""",
        ),
        quiz_lesson(
            "Quiz: Tensors and variables",
            (
                q(
                    "What is the difference between tf.constant and tf.Variable?",
                    (
                        opt("constant lives on CPU, Variable on GPU"),
                        opt(
                            "Constants are immutable values; Variables are mutable "
                            "state like model weights, updated with assign",
                            correct=True,
                        ),
                        opt("Variables cannot be used in arithmetic"),
                        opt("They are interchangeable synonyms"),
                    ),
                    "Data flows through immutable tensors; the weights that training "
                    "must update live in Variables.",
                ),
                q(
                    "What does tf.reshape(x, [-1]) do?",
                    (
                        opt("Reverses the element order"),
                        opt("Negates every value"),
                        opt(
                            "Flattens the tensor - the -1 dimension is inferred from "
                            "the element count",
                            correct=True,
                        ),
                        opt("Removes the batch dimension only"),
                    ),
                    "-1 means 'compute this dimension for me'; with no other dims it flattens.",
                ),
                q(
                    "Adding shape [3, 1] to shape [2] gives shape [3, 2]. Which "
                    "mechanism is at work?",
                    (
                        opt("Padding"),
                        opt("Concatenation"),
                        opt("One-hot encoding"),
                        opt("Broadcasting", correct=True),
                    ),
                    "Broadcasting stretches size-1 or missing dimensions so "
                    "compatible shapes combine without manual copying.",
                ),
            ),
        ),
        # ── 3. GradientTape ──────────────────────────────────────────
        _t(
            "GradientTape — gradients for free",
            "10 min",
            """# GradientTape — gradients for free

Training means adjusting weights to reduce a loss, and the adjustment
direction is the **gradient** - the derivative of the loss with respect
to each weight. Computing those by hand for millions of weights is
impossible; **`tf.GradientTape` does it automatically**.

Open a tape, compute the loss inside it, then ask the tape for
gradients:

```python
import tensorflow as tf

w = tf.Variable(2.0)
b = tf.Variable(1.0)
x = tf.constant(3.0)

with tf.GradientTape() as tape:
    y = w * x + b                  # y = 7.0, recorded
    loss = (y - 10.0) ** 2         # loss = 9.0

dw, db = tape.gradient(loss, [w, b])
print(dw)  # d loss / d w = 2 * (y - 10) * x = -18.0
print(db)  # d loss / d b = 2 * (y - 10)     = -6.0
```

The gradient tells us: increasing `w` a little would *decrease* the
loss (negative gradient), so training will push `w` up. That is
learning.

The rules that prevent the classic bugs:

- **Only what happens inside the `with` block is recorded.** Compute
  the loss inside the tape; use the gradients outside it.
- **Variables are watched automatically; constants are not.** To
  differentiate with respect to a plain tensor, call
  `tape.watch(tensor)` first.
- **A tape can be used once.** `tape.gradient(...)` releases its
  resources; call it a single time with a list of all the variables you
  need (or pass `persistent=True` when experimenting).
- **Applying the update** is one line with an optimizer:

```python
optimizer = tf.keras.optimizers.SGD(learning_rate=0.1)
optimizer.apply_gradients(zip([dw, db], [w, b]))
```

```mermaid
graph LR
    V["Variables watched by tape"] --> F["Forward pass inside with block"]
    F --> REC["Operations recorded"]
    REC --> GR["tape gradient loss vs weights"]
    GR --> AP["optimizer apply gradients"]
    AP --> V
```

Forward inside the tape, gradient from the tape, apply with the
optimizer - the manual heartbeat that fit() automates.
""",
        ),
        quiz_lesson(
            "Quiz: GradientTape — gradients for free",
            (
                q(
                    "Where must the loss computation happen for GradientTape to work?",
                    (
                        opt("Inside the 'with tf.GradientTape() as tape:' block", correct=True),
                        opt("Inside a @tf.function only"),
                        opt("Anywhere - the tape sees all code in the file"),
                        opt("In a separate thread"),
                    ),
                    "The tape records only the operations executed inside its with "
                    "block; gradients are then asked for outside it.",
                ),
                q(
                    "Which tensors does the tape watch automatically?",
                    (
                        opt("All tensors in memory"),
                        opt("tf.Variable objects - constants need tape.watch()", correct=True),
                        opt("Only tensors on the GPU"),
                        opt("Only tensors named with a w_ prefix"),
                    ),
                    "Trainable state is what training differentiates against, so "
                    "Variables are watched by default.",
                ),
                q(
                    "You call tape.gradient() twice on the same tape and the second "
                    "call fails. Why?",
                    (
                        opt("Gradients can only be computed on Tuesdays"),
                        opt("The loss must be recomputed between calls"),
                        opt(
                            "A tape releases its resources after one gradient call - "
                            "ask for all gradients at once or use persistent=True",
                            correct=True,
                        ),
                        opt("The second call needs a new optimizer"),
                    ),
                    "One tape, one gradient call - pass a list of variables to get "
                    "everything together.",
                ),
            ),
        ),
        # ── 4. Keras models ──────────────────────────────────────────
        _t(
            "Building models with Keras",
            "10 min",
            """# Building models with Keras

A model is a function with learnable weights. The fastest way to build
one in TensorFlow is **`tf.keras.Sequential`** - a stack of layers,
data flowing top to bottom:

```python
import tensorflow as tf
from tensorflow.keras import layers

model = tf.keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),      # 28x28 image -> 784 vector
    layers.Dense(128, activation="relu"),      # fully connected + ReLU
    layers.Dense(10),                          # 10 classes: raw logits
])

batch = tf.random.normal([32, 28, 28])          # 32 fake grayscale images
logits = model(batch)                           # shape [32, 10]
model.summary()                                 # layer-by-layer overview
```

What each piece is:

- **`layers.Dense(units)`** - a fully connected layer:
  `y = x @ W + b`, with `W` and `b` created as Variables for you.
- **`activation="relu"`** - the nonlinearity, attached right on the
  layer. Without nonlinearities, stacked Dense layers collapse into one
  linear layer; ReLU is what lets networks learn curves, not just
  lines.
- **The last layer outputs raw logits** - no softmax. The loss will
  handle that (next lesson), which is numerically safer.
- **`model(batch)` runs the forward pass**; the first dimension is
  always the **batch**.
- **`model.summary()`** prints every layer with its output shape and
  parameter count - the first tool for checking your architecture.

When a plain stack is not enough (multiple inputs, branches), the same
layers compose in **subclassing** style - declare layers in
`__init__`, wire them in `call` - the direct sibling of PyTorch's
`nn.Module`:

```python
class DigitClassifier(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.flatten = layers.Flatten()
        self.hidden = layers.Dense(128, activation="relu")
        self.out = layers.Dense(10)

    def call(self, x):
        return self.out(self.hidden(self.flatten(x)))
```

```mermaid
graph LR
    IN["Batch 32x28x28"] --> FL["Flatten to 32x784"]
    FL --> D1["Dense 128 ReLU"]
    D1 --> D2["Dense 10"]
    D2 --> LG["Logits 32x10"]
```

Sequential for stacks, subclassing for anything else - either way, it
is layers declared once and composed into a forward pass.
""",
        ),
        quiz_lesson(
            "Quiz: Building models with Keras",
            (
                q(
                    "What does tf.keras.Sequential represent?",
                    (
                        opt("A database of pretrained models"),
                        opt(
                            "A model built as a stack of layers that data flows through in order",
                            correct=True,
                        ),
                        opt("A queue of training jobs"),
                        opt("A list of GPUs to train on"),
                    ),
                    "Sequential is the simplest model form: layer after layer, top to bottom.",
                ),
                q(
                    "Why do stacked Dense layers need an activation like ReLU?",
                    (
                        opt("It converts outputs to integers for speed"),
                        opt("It is required by the GPU driver"),
                        opt(
                            "Without a nonlinearity, stacked linear layers collapse "
                            "into a single linear layer and cannot model curves",
                            correct=True,
                        ),
                        opt("It only matters for text data"),
                    ),
                    "Linear-of-linear is still linear; the activation gives depth its "
                    "expressive power.",
                ),
                q(
                    "Why does the final Dense(10) layer have no softmax activation?",
                    (
                        opt("Softmax is deprecated in TensorFlow 2"),
                        opt(
                            "The loss function applies it internally from the raw "
                            "logits, which is numerically safer",
                            correct=True,
                        ),
                        opt("Softmax only works with exactly 2 classes"),
                        opt("It is a bug in the example"),
                    ),
                    "Output logits and let the loss handle normalization - the same "
                    "convention as CrossEntropyLoss in PyTorch.",
                ),
            ),
        ),
        # ── 5. compile & fit ─────────────────────────────────────────
        _t(
            "compile and fit — the Keras workflow",
            "10 min",
            """# compile and fit — the Keras workflow

Keras packages the whole training procedure into two calls. **`compile`**
declares *how* to train; **`fit`** runs the loop:

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)

history = model.fit(
    x_train, y_train,
    epochs=3,
    batch_size=64,
    validation_split=0.1,     # hold out 10% to watch generalization
)
```

The three compile ingredients:

- **Optimizer** - how weights move. `Adam` with `lr=1e-3` is the
  standard starting point; `SGD` is the classic. Too high a learning
  rate and the loss explodes; too low and training crawls.
- **Loss** - what training minimizes.
  `SparseCategoricalCrossentropy(from_logits=True)` fits classification
  with integer labels and a logits-output model - **`from_logits=True`
  is the flag everyone forgets**, and forgetting it silently degrades
  training.
- **Metrics** - numbers reported for humans (accuracy), not optimized
  directly.

What `fit` does per epoch: shuffle, split into batches, and for each
batch run exactly the tape-gradient-apply cycle from the GradientTape
lesson - forward, loss, gradients, update - then report metrics on the
validation split.

`fit` returns a **`history`** object whose `history.history` dict holds
the loss and metrics per epoch - plot it, and watch for the classic
signature of **overfitting**: training accuracy climbing while
validation accuracy stalls or drops.

Evaluation and prediction are one-liners:

```python
model.evaluate(x_test, y_test)          # loss and metrics on unseen data
probs = tf.nn.softmax(model(x_new))     # predictions for new inputs
```

```mermaid
graph LR
    CP["compile optimizer loss metrics"] --> FT["fit epochs batches"]
    FT --> LP["Per batch forward loss grads update"]
    FT --> VAL["Validation split each epoch"]
    FT --> H["history losses and metrics"]
    H --> OV["Watch for overfitting"]
```

compile declares the recipe, fit turns the crank - and history tells
you whether it worked.
""",
        ),
        quiz_lesson(
            "Quiz: compile and fit — the Keras workflow",
            (
                q(
                    "What are the three things model.compile() configures?",
                    (
                        opt("Optimizer, loss and metrics", correct=True),
                        opt("CPU, GPU and TPU"),
                        opt("Train, validation and test sets"),
                        opt("Layers, weights and biases"),
                    ),
                    "How to update (optimizer), what to minimize (loss), and what to "
                    "report (metrics).",
                ),
                q(
                    "Your model outputs raw logits. What must the "
                    "SparseCategoricalCrossentropy loss get?",
                    (
                        opt("from_logits=True", correct=True),
                        opt("normalize=True"),
                        opt("A softmax layer added after the loss"),
                        opt("One-hot encoded labels only"),
                    ),
                    "from_logits=True tells the loss to apply the softmax itself; "
                    "omitting it with a logits model silently hurts training.",
                ),
                q(
                    "Training accuracy keeps climbing while validation accuracy "
                    "stalls and drops. What is this called?",
                    (
                        opt("Broadcasting"),
                        opt("Underfitting"),
                        opt(
                            "Overfitting - the model memorizes training data instead of generalizing",
                            correct=True,
                        ),
                        opt("Gradient explosion"),
                    ),
                    "The gap between the two curves in history is the standard "
                    "overfitting signature - the validation split exists to reveal it.",
                ),
            ),
        ),
        # ── 6. tf.data ───────────────────────────────────────────────
        _t(
            "Input pipelines with tf.data",
            "9 min",
            """# Input pipelines with tf.data

Real datasets do not fit in one tensor. **`tf.data.Dataset`** is
TensorFlow's answer: a description of a data stream, built by chaining
transformations, consumed batch by batch.

```python
import tensorflow as tf

dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))

train_ds = (
    dataset
    .shuffle(10_000)      # re-order examples every epoch
    .batch(64)            # mini-batches of 64
    .prefetch(tf.data.AUTOTUNE)  # prepare next batch while GPU trains
)

for batch_x, batch_y in train_ds:   # ready-made mini-batches
    ...

model.fit(train_ds, epochs=3)       # fit consumes datasets directly
```

The three everyday transformations:

- **`shuffle(buffer)`** - randomizes order each epoch so the model
  never learns the accidental order of the file.
- **`batch(n)`** - groups examples into mini-batches. Why batches?
  Memory (a million images do not fit at once) and better training (the
  slight noise of small batches helps generalization); 32-256 is the
  norm.
- **`prefetch(AUTOTUNE)`** - overlaps data preparation with training,
  so the accelerator never waits for input. This one line is the
  cheapest speedup in TensorFlow.

Per-example processing plugs in with **`map`**:

```python
def normalize(image, label):
    return tf.cast(image, tf.float32) / 255.0, label

train_ds = dataset.map(normalize).shuffle(10_000).batch(64).prefetch(
    tf.data.AUTOTUNE
)
```

The chain order matters: `map` before `batch` processes one example at
a time; `shuffle` before `batch` shuffles examples rather than whole
batches.

```mermaid
graph LR
    SRC["from tensor slices"] --> MP["map per example transform"]
    MP --> SF["shuffle each epoch"]
    SF --> BT["batch 32 to 256"]
    BT --> PF["prefetch AUTOTUNE"]
    PF --> FIT["fit or manual loop consumes"]
```

Describe the stream once - map, shuffle, batch, prefetch - and both fit
and custom loops drink from it.
""",
        ),
        quiz_lesson(
            "Quiz: Input pipelines with tf.data",
            (
                q(
                    "What does prefetch(tf.data.AUTOTUNE) do?",
                    (
                        opt("Downloads datasets from the internet automatically"),
                        opt(
                            "Prepares the next batches while the current one trains, "
                            "so the accelerator never waits for data",
                            correct=True,
                        ),
                        opt("Caches the whole dataset on the GPU"),
                        opt("Skips corrupted examples"),
                    ),
                    "Overlapping input preparation with computation is the cheapest "
                    "speedup available - one chained call.",
                ),
                q(
                    "Why train on mini-batches instead of the whole dataset per step?",
                    (
                        opt("TensorFlow forbids tensors larger than 1 GB"),
                        opt(
                            "Full datasets rarely fit in memory, and the noise of "
                            "small batches helps generalization",
                            correct=True,
                        ),
                        opt("Batches make the loss exactly zero"),
                        opt("Batches are only needed for image data"),
                    ),
                    "Practical memory limits plus a real training benefit made batch "
                    "sizes of 32-256 the standard.",
                ),
                q(
                    "Where should shuffle() go relative to batch() and why?",
                    (
                        opt(
                            "Before batch(), so individual examples are shuffled "
                            "rather than whole batches",
                            correct=True,
                        ),
                        opt("After batch(), to shuffle faster"),
                        opt("It does not matter at all"),
                        opt("shuffle() must always be the last call"),
                    ),
                    "Shuffling after batching only re-orders fixed batches; before "
                    "batching it re-mixes examples every epoch.",
                ),
            ),
        ),
        # ── 7. Custom training loops ─────────────────────────────────
        _t(
            "Custom training loops",
            "10 min",
            """# Custom training loops

`fit` covers the standard cases; research tricks, unusual losses and
multi-model setups (like GANs) need the loop written out. Everything
from the previous lessons assembles into five steps - the same five as
every deep-learning framework:

```python
import tensorflow as tf

# tiny regression: learn y = 2x + 1 from noisy points
x = tf.reshape(tf.linspace(-1.0, 1.0, 100), [-1, 1])
y = 2 * x + 1 + 0.1 * tf.random.normal(x.shape)

model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
loss_fn = tf.keras.losses.MeanSquaredError()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.1)

for epoch in range(200):
    with tf.GradientTape() as tape:
        pred = model(x)               # 1. forward: predictions
        loss = loss_fn(y, pred)       # 2. loss: how wrong

    grads = tape.gradient(loss, model.trainable_variables)   # 3. gradients
    optimizer.apply_gradients(zip(grads, model.trainable_variables))  # 4. update
    # 5. repeat - and log loss.numpy() to watch it fall

w, b = model.layers[0].get_weights()
print(w, b)   # close to 2.0 and 1.0
```

Run it: the printed weight and bias converge to the true 2 and 1. A
model just *learned*, and you can see every moving part - this loop is
exactly what `fit` runs under the hood.

Details that matter:

- **`model.trainable_variables`** collects every weight from every
  layer - what you differentiate against and update.
- **No zero_grad here**: unlike PyTorch, each tape is fresh, so
  gradients never accumulate between steps by accident.
- **Speed**: decorate the step with `@tf.function` and TensorFlow
  compiles it to a graph - typically several times faster:

```python
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        loss = loss_fn(y, model(x))
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))
    return loss
```

```mermaid
graph LR
    FW["1 forward inside tape"] --> LS["2 loss"]
    LS --> GR["3 tape gradient"]
    GR --> AP["4 apply gradients"]
    AP --> FW
    TF["tf function compiles step"] --> FW
```

Forward, loss, gradient, apply - fit turns this crank for you; now you
can turn it yourself when the recipe is not standard.
""",
        ),
        quiz_lesson(
            "Quiz: Custom training loops",
            (
                q(
                    "In a custom loop, what does model.trainable_variables give you?",
                    (
                        opt("The learning-rate schedule"),
                        opt(
                            "Every learnable weight across all layers - the list to "
                            "differentiate against and update",
                            correct=True,
                        ),
                        opt("The gradients from the last step"),
                        opt("A frozen copy of the model"),
                    ),
                    "tape.gradient(loss, model.trainable_variables) plus "
                    "apply_gradients over the same list is the whole update.",
                ),
                q(
                    "Why is there no zero_grad step in TensorFlow custom loops?",
                    (
                        opt("Gradients are cleared by the garbage collector hourly"),
                        opt(
                            "Each GradientTape is fresh per step, so gradients never "
                            "accumulate between iterations by accident",
                            correct=True,
                        ),
                        opt("TensorFlow models have no gradients"),
                        opt("apply_gradients throws away the model weights"),
                    ),
                    "The tape lives inside the loop body - a new recording every "
                    "step, unlike PyTorch's accumulating .grad fields.",
                ),
                q(
                    "What does decorating the training step with @tf.function achieve?",
                    (
                        opt("It prints the loss automatically"),
                        opt("It moves the model to the GPU"),
                        opt(
                            "It compiles the step into a graph, typically making it "
                            "several times faster",
                            correct=True,
                        ),
                        opt("It saves the model after every step"),
                    ),
                    "Develop eagerly, then compile the hot path - the TF2 performance idiom.",
                ),
            ),
        ),
        # ── 8. End to end ────────────────────────────────────────────
        _t(
            "End to end — a digit classifier",
            "12 min",
            """# End to end — a digit classifier

Every piece from the course, assembled: train a classifier on MNIST
(28x28 handwritten digits), evaluate it, save it, load it back.

```python
import tensorflow as tf
from tensorflow.keras import layers

# 1. data: keras ships MNIST; normalize to [0, 1]
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

train_ds = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .shuffle(60_000).batch(64).prefetch(tf.data.AUTOTUNE)
)

# 2. model
model = tf.keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation="relu"),
    layers.Dense(10),
])

# 3. recipe + training
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)
model.fit(train_ds, epochs=3)

# 4. honest evaluation on unseen data
model.evaluate(x_test, y_test)   # ~97% accuracy

# 5. predictions for new images
logits = model(x_test[:5])
classes = tf.argmax(logits, axis=1)   # predicted digits
```

Three epochs reach roughly 97% accuracy on a laptop CPU in about a
minute - a genuinely working digit reader from ~25 lines.

The remaining practical skills:

**Saving and loading.** The native Keras format stores architecture,
weights and optimizer state in one file:

```python
model.save("digits.keras")                       # everything in one file
restored = tf.keras.models.load_model("digits.keras")
restored.evaluate(x_test, y_test)                # same accuracy
```

For deployment (TF Serving, LiteRT, TensorFlow.js), export a
**SavedModel** directory instead: `model.export("digits_savedmodel")`.

**Devices.** TensorFlow places operations on the GPU automatically when
one is visible - the same code runs unchanged on CPU and GPU. Check
what it found with `tf.config.list_physical_devices("GPU")`.

```mermaid
graph TD
    DATA["MNIST via tf data pipeline"] --> TRAIN["compile and fit 3 epochs"]
    MODEL["Sequential Flatten Dense"] --> TRAIN
    TRAIN --> EVAL["evaluate on test set"]
    EVAL --> SAVE["save digits keras"]
    SAVE --> LOAD["load model restores everything"]
    SAVE --> DEP["export SavedModel for serving"]
```

Tensors, tape, layers, compile, fit, data, save - one page of code, and
it is the same page at every scale.
""",
        ),
        quiz_lesson(
            "Quiz: End to end — a digit classifier",
            (
                q(
                    "Why are the MNIST pixel values divided by 255.0 before training?",
                    (
                        opt("To convert the images to grayscale"),
                        opt(
                            "To normalize inputs to the [0, 1] range, which trains "
                            "far more stably than raw 0-255 values",
                            correct=True,
                        ),
                        opt("To reduce the dataset size on disk"),
                        opt("Because Dense layers only accept values below 1"),
                    ),
                    "Normalized inputs keep gradients well-scaled - a tiny "
                    "preprocessing step with a large training effect.",
                ),
                q(
                    "What does model.save('digits.keras') store?",
                    (
                        opt("Only the layer names"),
                        opt("Only the training history"),
                        opt(
                            "Architecture, weights and optimizer state in one file - "
                            "load_model restores the whole model",
                            correct=True,
                        ),
                        opt("A screenshot of model.summary()"),
                    ),
                    "The native .keras format round-trips everything; SavedModel "
                    "export is the sibling for serving and mobile.",
                ),
                q(
                    "How are class predictions obtained from the model's outputs?",
                    (
                        opt(
                            "tf.argmax over the logits picks the highest-scoring class",
                            correct=True,
                        ),
                        opt("The loss function returns them"),
                        opt("model.fit returns predictions"),
                        opt("Rounding each logit to the nearest integer"),
                    ),
                    "Logits of shape [batch, 10] become digit predictions via "
                    "argmax along the class axis.",
                ),
            ),
        ),
        # ── Final quiz ───────────────────────────────────────────────
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is TensorFlow?",
                    (
                        opt(
                            "A NumPy-like tensor library with automatic "
                            "differentiation and accelerator support, with Keras as "
                            "its model-building toolkit",
                            correct=True,
                        ),
                        opt("A JavaScript charting library"),
                        opt("A database for storing model weights"),
                        opt("A GPU driver installer"),
                    ),
                    "Tensors + GradientTape + Keras - every lesson is one of those "
                    "layers unfolding.",
                ),
                q(
                    "Model weights should be stored in…",
                    (
                        opt("tf.constant tensors"),
                        opt("Python lists"),
                        opt(
                            "tf.Variable objects - mutable state the optimizer updates",
                            correct=True,
                        ),
                        opt("JSON files reloaded every step"),
                    ),
                    "Constants are immutable data; Variables are the trainable state "
                    "GradientTape watches automatically.",
                ),
                q(
                    "What is the role of tf.GradientTape?",
                    (
                        opt(
                            "Recording operations during the forward pass so gradients "
                            "of the loss can be computed for the watched variables",
                            correct=True,
                        ),
                        opt("Measuring how long training takes"),
                        opt("Storing datasets on disk"),
                        opt("Rolling back failed weight updates"),
                    ),
                    "Forward inside the tape, tape.gradient for the derivatives, "
                    "optimizer.apply_gradients for the update.",
                ),
                q(
                    "Which compile() configuration is correct for a logits-output "
                    "classifier with integer labels?",
                    (
                        opt("loss=SparseCategoricalCrossentropy(from_logits=True)", correct=True),
                        opt("loss=MeanSquaredError()"),
                        opt("loss=SparseCategoricalCrossentropy(from_logits=False)"),
                        opt("metrics=['loss'] with no loss argument"),
                    ),
                    "Integer labels -> Sparse variant; logits output -> "
                    "from_logits=True. The forgotten flag silently degrades training.",
                ),
                q(
                    "What does model.fit() do with a validation_split?",
                    (
                        opt(
                            "Holds out that fraction of training data and reports loss "
                            "and metrics on it each epoch, revealing overfitting",
                            correct=True,
                        ),
                        opt("Trains a second model on the held-out part"),
                        opt("Deletes that fraction of the dataset"),
                        opt("Splits each batch in half"),
                    ),
                    "The training/validation curve gap in history is how you catch a "
                    "model that memorizes instead of generalizing.",
                ),
                q(
                    "Order the canonical tf.data pipeline correctly.",
                    (
                        opt("map -> shuffle -> batch -> prefetch", correct=True),
                        opt("batch -> shuffle -> map -> prefetch"),
                        opt("prefetch -> batch -> shuffle -> map"),
                        opt("shuffle -> prefetch -> map -> batch"),
                    ),
                    "Per-example transforms first, shuffle examples not batches, then "
                    "batch, and prefetch last to overlap with training.",
                ),
                q(
                    "In a custom training loop, the weight update is performed by…",
                    (
                        opt(
                            "optimizer.apply_gradients over grads zipped with trainable_variables",
                            correct=True,
                        ),
                        opt("calling loss.backward()"),
                        opt("assigning to model.weights directly"),
                        opt("re-running model.compile()"),
                    ),
                    "tape.gradient computes; apply_gradients applies - the TF "
                    "spelling of backward + step.",
                ),
                q(
                    "Why decorate a training step with @tf.function?",
                    (
                        opt("It compiles the eager code into a graph for speed", correct=True),
                        opt("It is required for GradientTape to work"),
                        opt("It saves the model after each step"),
                        opt("It disables the GPU for reproducibility"),
                    ),
                    "Eager for development, graph for performance - the same code, "
                    "one decorator apart.",
                ),
                q(
                    "Training loss explodes to NaN after a few steps. Which is the "
                    "most reasonable first fix?",
                    (
                        opt(
                            "Lower the learning rate (and check input normalization)", correct=True
                        ),
                        opt("Add more Dense layers"),
                        opt("Remove the loss function"),
                        opt("Switch shuffle() off"),
                    ),
                    "Exploding losses are the signature of oversized steps or "
                    "unnormalized inputs - the learning rate is the first dial.",
                ),
                q(
                    "Which statement about saving is correct?",
                    (
                        opt(
                            "model.save('m.keras') stores architecture, weights and "
                            "optimizer state; load_model restores the whole model",
                            correct=True,
                        ),
                        opt("Only weights can ever be saved in TensorFlow"),
                        opt("Saving requires re-training after loading"),
                        opt("The .keras file only works on the machine that wrote it"),
                    ),
                    "One file round-trips the model; SavedModel export serves "
                    "deployment targets like TF Serving, LiteRT and TensorFlow.js.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

TENSORFLOW_COURSES: tuple[SeedCourse, ...] = (_TENSORFLOW_BASICS,)
