"""Academy seed content — PyTorch — Basics.

A hands-on introduction to PyTorch: tensors and their operations,
automatic differentiation with autograd, building models with nn.Module,
losses and optimizers, the canonical training loop, feeding data with
Dataset and DataLoader, and a complete end-to-end image classifier with
saving/loading and GPU use. Every lesson is a direct explanation with
runnable examples and a mermaid diagram, followed by a checkpoint quiz;
the course closes with a comprehensive final quiz.
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


_PYTORCH_BASICS = SeedCourse(
    slug="pytorch-basics",
    title="PyTorch — Basics",
    description=(
        "Deep learning with PyTorch from zero: tensors, autograd, building "
        "models with nn.Module, losses and optimizers, the training loop, "
        "Dataset and DataLoader, and a complete digit classifier - explained "
        "directly, with runnable examples and a diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # ── Welcome ──────────────────────────────────────────────────
        _t(
            "Welcome — how this course works",
            "4 min",
            """# PyTorch — Basics

PyTorch is the most widely used framework for deep learning research and
one of the two dominant ones in production. If you know basic Python and
a little NumPy-style array thinking, this course takes you to the point
where you can build, train and save a real neural network.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it in runnable code, and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **What PyTorch is** - tensors, autograd, GPUs, define-by-run
2. **Tensors** - creating, shaping and operating on data
3. **Autograd** - how gradients are computed for you
4. **Models** - `nn.Module`, layers and the forward pass
5. **Losses and optimizers** - what "learning" minimizes and how
6. **The training loop** - the five lines at the heart of everything
7. **Data** - `Dataset` and `DataLoader`, batches and shuffling
8. **End to end** - a digit classifier, saving, loading and the GPU

Install with `pip install torch torchvision` - CPU is fine for this
whole course; every example runs in seconds.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome — how this course works",
            (
                q(
                    "What prior knowledge does this course assume?",
                    (
                        opt("Experience with TensorFlow"),
                        opt("Basic Python and some array thinking", correct=True),
                        opt("A CUDA-capable GPU"),
                        opt("Graduate-level calculus"),
                    ),
                    "Python plus NumPy-style array intuition is enough; a GPU is "
                    "optional - every example runs on CPU in seconds.",
                ),
                q(
                    "What will you be able to do by the end of the course?",
                    (
                        opt("Deploy large language models to production clusters"),
                        opt("Write custom CUDA kernels"),
                        opt(
                            "Build, train, evaluate and save a real neural network in PyTorch",
                            correct=True,
                        ),
                        opt("Design new optimization algorithms"),
                    ),
                    "The arc ends with a complete digit classifier: model, training "
                    "loop, evaluation, saving/loading and GPU use.",
                ),
            ),
        ),
        # ── 1. What is PyTorch ───────────────────────────────────────
        _t(
            "What is PyTorch?",
            "8 min",
            """# What is PyTorch?

PyTorch is three things stacked on top of each other:

1. **A tensor library** - like NumPy, but every operation can also run
   on a GPU. A tensor is an n-dimensional array of numbers: a scalar, a
   vector, a matrix, a batch of images.
2. **An autograd engine** - PyTorch records the operations you perform
   and can automatically compute gradients through them. Gradients are
   what training uses to improve a model.
3. **A neural-network toolkit** (`torch.nn`) - layers, loss functions
   and optimizers built from those two foundations.

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0])
w = torch.tensor([0.5, 0.5, 0.5], requires_grad=True)
y = (x * w).sum()   # y = 3.0, and PyTorch remembers how it was computed
y.backward()        # fills w.grad with dy/dw = x
print(w.grad)       # tensor([1., 2., 3.])
```

The signature property is **define-by-run** (a dynamic graph): the
computation graph is built *while your Python code executes*, not
compiled ahead of time. Ordinary `if` statements and loops work; you can
print any intermediate value; debugging is plain Python debugging. This
is why research moved to PyTorch - the code you read is the code that
runs.

```mermaid
graph TD
    T["Tensor library like NumPy"] --> A["Autograd records operations"]
    A --> G["Gradients computed automatically"]
    T --> GPU["Same code on CPU or GPU"]
    A --> NN["torch nn layers losses optimizers"]
    NN --> M["Trainable models"]
```

The one thing to remember: PyTorch is NumPy with gradients and GPUs -
everything else in this course is built from that.
""",
        ),
        quiz_lesson(
            "Quiz: What is PyTorch?",
            (
                q(
                    "What are the two foundational capabilities everything in PyTorch is built on?",
                    (
                        opt("HTML rendering and CSS styling"),
                        opt(
                            "GPU-capable tensors and automatic differentiation",
                            correct=True,
                        ),
                        opt("Database access and networking"),
                        opt("Image decoding and audio playback"),
                    ),
                    "A NumPy-like tensor library that runs on GPUs, plus an autograd "
                    "engine that computes gradients - torch.nn is built on both.",
                ),
                q(
                    "What does 'define-by-run' (dynamic graph) mean?",
                    (
                        opt("Models must be compiled before any code runs"),
                        opt(
                            "The computation graph is built as your Python code "
                            "executes, so normal control flow and debugging work",
                            correct=True,
                        ),
                        opt("The model definition lives in a YAML file"),
                        opt("Code only runs when a GPU is attached"),
                    ),
                    "PyTorch records operations while they happen - ifs, loops and "
                    "print() behave exactly like ordinary Python.",
                ),
                q(
                    "After y.backward() in the example, what does w.grad contain?",
                    (
                        opt("The gradient of y with respect to w", correct=True),
                        opt("A copy of the tensor y"),
                        opt("The learning rate"),
                        opt("Nothing - backward only checks for errors"),
                    ),
                    "backward() walks the recorded graph and fills .grad with the "
                    "derivative of the output with respect to each tracked tensor.",
                ),
            ),
        ),
        # ── 2. Tensors ───────────────────────────────────────────────
        _t(
            "Tensors — data in PyTorch",
            "10 min",
            """# Tensors — data in PyTorch

Everything in PyTorch is a **tensor**: the inputs, the model's weights,
the predictions, the loss. Getting comfortable with creating and
reshaping them is half the battle.

**Creating tensors:**

```python
import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])  # from data
z = torch.zeros(3, 4)                        # 3x4 of zeros
r = torch.randn(2, 3)                        # random normal values
s = torch.arange(6)                          # tensor([0, 1, 2, 3, 4, 5])
```

Every tensor has three attributes you will check constantly:

```python
a.shape   # torch.Size([2, 2])  - the dimensions
a.dtype   # torch.float32       - the number type
a.device  # cpu (or cuda:0)     - where it lives
```

**Shape is everything.** Most PyTorch bugs are shape bugs, and
`.reshape` / `.view` are the daily tools:

```python
x = torch.arange(12)        # shape [12]
m = x.reshape(3, 4)         # shape [3, 4]
f = m.reshape(-1)           # back to [12]; -1 means "figure it out"
b = m.unsqueeze(0)          # shape [1, 3, 4] - add a batch dimension
```

**Operations** are elementwise by default, `@` is matrix multiplication,
and **broadcasting** stretches compatible shapes automatically:

```python
u = torch.tensor([[1.0], [2.0], [3.0]])  # shape [3, 1]
v = torch.tensor([10.0, 20.0])           # shape [2]
print(u + v)                              # shape [3, 2] - broadcast
w = torch.randn(4, 3) @ torch.randn(3, 2) # shape [4, 2]
```

Reductions collapse dimensions: `t.sum()`, `t.mean(dim=0)`,
`t.argmax(dim=1)` - the `dim` argument says which axis disappears.

```mermaid
graph LR
    C["Create tensor zeros randn arange"] --> AT["shape dtype device"]
    AT --> R["reshape view unsqueeze"]
    R --> O["Elementwise ops and matmul"]
    O --> B["Broadcasting aligns shapes"]
    O --> RD["Reductions sum mean argmax"]
```

When something breaks, print `.shape` first - it is the answer more
often than not.
""",
        ),
        quiz_lesson(
            "Quiz: Tensors — data in PyTorch",
            (
                q(
                    "What does reshape(-1) do to a tensor?",
                    (
                        opt("Reverses the order of its elements"),
                        opt("Deletes the last dimension"),
                        opt(
                            "Flattens or resizes with the -1 dimension inferred "
                            "automatically from the element count",
                            correct=True,
                        ),
                        opt("Negates every value"),
                    ),
                    "-1 means 'compute this dimension for me' - reshape(-1) with no "
                    "other dims flattens the tensor.",
                ),
                q(
                    "Which three attributes describe every tensor?",
                    (
                        opt("shape, dtype and device", correct=True),
                        opt("rows, columns and depth"),
                        opt("name, id and version"),
                        opt("min, max and mean"),
                    ),
                    "Dimensions, number type, and whether it lives on CPU or GPU - "
                    "the first things to check when debugging.",
                ),
                q(
                    "Adding a tensor of shape [3, 1] to one of shape [2] produces "
                    "shape [3, 2]. What is this mechanism called?",
                    (
                        opt("Concatenation"),
                        opt("Broadcasting", correct=True),
                        opt("Pooling"),
                        opt("Padding"),
                    ),
                    "Broadcasting stretches size-1 (or missing) dimensions so "
                    "compatible shapes can be combined without copying data by hand.",
                ),
            ),
        ),
        # ── 3. Autograd ──────────────────────────────────────────────
        _t(
            "Autograd — gradients for free",
            "10 min",
            """# Autograd — gradients for free

Training a model means adjusting weights to reduce a loss, and the
adjustment direction is the **gradient** - the derivative of the loss
with respect to each weight. Computing those derivatives by hand for
millions of weights is impossible; **autograd does it automatically**.

Mark a tensor with `requires_grad=True` and PyTorch records every
operation involving it into a graph. Call `.backward()` on the final
scalar and the graph is walked in reverse (backpropagation), filling
each tracked tensor's `.grad`:

```python
import torch

w = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)
x = torch.tensor(3.0)

y = w * x + b        # y = 7.0; graph: y depends on w and b
loss = (y - 10.0) ** 2  # loss = 9.0

loss.backward()
print(w.grad)  # d loss / d w = 2 * (y - 10) * x = -18.0
print(b.grad)  # d loss / d b = 2 * (y - 10)     = -6.0
```

The gradient tells us: increasing `w` a little would *decrease* the loss
(negative gradient), so training will push `w` up. That is learning.

Three rules that prevent the classic bugs:

- **Gradients accumulate.** A second `backward()` *adds* to `.grad`,
  which is why every training step starts by zeroing gradients
  (`optimizer.zero_grad()`).
- **`backward()` needs a scalar** - you call it on the loss, a single
  number, not on a matrix.
- **Inference goes inside `torch.no_grad()`.** When you only want
  predictions, disabling recording saves memory and time:

```python
with torch.no_grad():
    prediction = w * x + b   # no graph is built here
```

```mermaid
graph LR
    W["Tensors with requires grad"] --> F["Forward pass computes loss"]
    F --> GR["Graph of operations recorded"]
    GR --> BW["backward walks graph in reverse"]
    BW --> G["grad filled for each weight"]
    G --> UP["Optimizer updates weights"]
```

Forward computes the loss, backward computes the blame - and .grad is
where the blame lands.
""",
        ),
        quiz_lesson(
            "Quiz: Autograd — gradients for free",
            (
                q(
                    "What does requires_grad=True on a tensor do?",
                    (
                        opt("Moves the tensor to the GPU"),
                        opt("Makes the tensor immutable"),
                        opt(
                            "Tells autograd to record operations on it so gradients can "
                            "be computed by backward()",
                            correct=True,
                        ),
                        opt("Normalizes its values to the 0-1 range"),
                    ),
                    "Tracked tensors become part of the computation graph; backward() "
                    "then fills their .grad fields.",
                ),
                q(
                    "Why does every training step call optimizer.zero_grad()?",
                    (
                        opt(
                            "Gradients accumulate across backward() calls, so they must "
                            "be reset before computing the new ones",
                            correct=True,
                        ),
                        opt("To reset the model's weights to zero"),
                        opt("To free all GPU memory"),
                        opt("It is optional decoration with no effect"),
                    ),
                    "backward() adds into .grad; without zeroing, each step would mix "
                    "old gradients into the new update.",
                ),
                q(
                    "When should code run inside torch.no_grad()?",
                    (
                        opt("During weight initialization only"),
                        opt(
                            "During inference/evaluation, when gradients are not needed "
                            "- it skips graph recording, saving memory and time",
                            correct=True,
                        ),
                        opt("Never - it disables the model"),
                        opt("Only when using a GPU"),
                    ),
                    "Predictions do not need a graph; no_grad() (and model.eval()) is "
                    "the standard evaluation idiom.",
                ),
            ),
        ),
        # ── 4. Models ────────────────────────────────────────────────
        _t(
            "Building models with nn.Module",
            "10 min",
            """# Building models with nn.Module

A model is a function with learnable weights. In PyTorch you write it as
a class inheriting **`nn.Module`**: layers are declared in `__init__`,
and **`forward`** says how data flows through them.

```python
import torch
from torch import nn

class DigitClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()          # 28x28 image -> 784 vector
        self.hidden = nn.Linear(784, 128)    # 784 inputs -> 128 outputs
        self.act = nn.ReLU()                 # nonlinearity
        self.out = nn.Linear(128, 10)        # 10 classes: digits 0-9

    def forward(self, x):
        x = self.flatten(x)
        x = self.act(self.hidden(x))
        return self.out(x)                   # raw scores called logits

model = DigitClassifier()
batch = torch.randn(32, 1, 28, 28)           # 32 fake grayscale images
logits = model(batch)                        # shape [32, 10]
```

What each piece is:

- **`nn.Linear(in, out)`** - a fully connected layer: `y = x @ W.T + b`,
  with `W` and `b` created for you, `requires_grad` already set.
- **`nn.ReLU()`** - the nonlinearity between layers. Without it,
  stacked linear layers collapse into one linear layer; nonlinearity is
  what lets networks learn curves, not just lines.
- **`model(batch)` calls `forward`** - you never call `forward`
  directly; calling the module also runs PyTorch's hooks.
- **`model.parameters()`** yields every weight in every registered
  layer - exactly what you will hand to the optimizer.

The first dimension is always the **batch**: shape `[32, 1, 28, 28]`
means 32 images processed together, and every layer preserves that
convention.

```mermaid
graph LR
    IN["Batch 32x1x28x28"] --> FL["Flatten to 32x784"]
    FL --> L1["Linear 784 to 128"]
    L1 --> RE["ReLU"]
    RE --> L2["Linear 128 to 10"]
    L2 --> LG["Logits 32x10"]
```

Declare layers in __init__, wire them in forward, call the model like a
function - that is every PyTorch model, from this one to a transformer.
""",
        ),
        quiz_lesson(
            "Quiz: Building models with nn.Module",
            (
                q(
                    "Where do a module's layers get declared, and where is data flow defined?",
                    (
                        opt("Both in a config dictionary"),
                        opt(
                            "Layers in __init__, data flow in forward",
                            correct=True,
                        ),
                        opt("Layers in forward, data flow in __init__"),
                        opt("Both must be in a separate build() method"),
                    ),
                    "__init__ creates the learnable pieces; forward composes them - "
                    "the universal nn.Module shape.",
                ),
                q(
                    "Why do networks need a nonlinearity like ReLU between linear layers?",
                    (
                        opt("It makes training run on multiple cores"),
                        opt("It converts tensors to integers for speed"),
                        opt(
                            "Without it, stacked linear layers collapse into a single "
                            "linear layer and cannot model curved relationships",
                            correct=True,
                        ),
                        opt("It is only needed for image data"),
                    ),
                    "Linear-of-linear is still linear; the nonlinearity is what gives "
                    "deep networks their expressive power.",
                ),
                q(
                    "What does model.parameters() provide?",
                    (
                        opt("The model's hyperparameters like learning rate"),
                        opt(
                            "Every learnable weight tensor in the registered layers - "
                            "what you pass to the optimizer",
                            correct=True,
                        ),
                        opt("A summary printout of the architecture"),
                        opt("The gradients from the last backward pass"),
                    ),
                    "The optimizer needs to know which tensors to update; "
                    "parameters() enumerates exactly those.",
                ),
            ),
        ),
        # ── 5. Losses & optimizers ───────────────────────────────────
        _t(
            "Losses and optimizers",
            "9 min",
            """# Losses and optimizers

Training needs two more pieces: a **loss function** that scores how
wrong the model is (one number - lower is better), and an **optimizer**
that uses gradients to nudge every weight in the direction that lowers
that number.

**Choosing the loss** follows the task:

```python
from torch import nn

loss_fn = nn.MSELoss()            # regression: predict a number
loss_fn = nn.CrossEntropyLoss()   # classification: pick a class
```

`CrossEntropyLoss` takes the model's raw **logits** (shape
`[batch, classes]`) and the true class indices (shape `[batch]`) - no
softmax layer needed; it is built in:

```python
import torch

logits = torch.tensor([[2.0, 0.5, 0.1], [0.2, 3.0, 0.3]])
targets = torch.tensor([0, 1])        # true classes
loss = nn.CrossEntropyLoss()(logits, targets)   # small: both correct
```

**The optimizer** implements gradient descent: after `backward()` fills
`.grad`, `optimizer.step()` moves each weight a little against its
gradient. The step size is the **learning rate** - the most important
hyperparameter in deep learning:

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)   # the classic
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)  # the default choice
```

- **SGD**: weight = weight - lr * grad. Simple, well understood.
- **Adam**: adapts the step per weight using running averages of
  gradients - usually converges faster with less tuning, which is why
  `Adam` with `lr=1e-3` is the standard starting point.

Too high a learning rate and the loss explodes or oscillates; too low
and training crawls. When in doubt, start at `1e-3` and adjust by
factors of 10.

```mermaid
graph LR
    P["Predictions logits"] --> L["Loss one number"]
    T["Targets"] --> L
    L --> B["backward fills grads"]
    B --> O["Optimizer step updates weights"]
    O --> P
```

Loss says how wrong; gradients say which way; the optimizer says how
far - repeated until the loss stops falling.
""",
        ),
        quiz_lesson(
            "Quiz: Losses and optimizers",
            (
                q(
                    "Which loss fits a classification problem, and what does it take as input?",
                    (
                        opt("MSELoss on softmax probabilities"),
                        opt(
                            "CrossEntropyLoss on raw logits plus true class indices - "
                            "softmax is built in",
                            correct=True,
                        ),
                        opt("L1Loss on one-hot vectors only"),
                        opt("Any loss works equally well for any task"),
                    ),
                    "CrossEntropyLoss expects unnormalized logits and integer "
                    "targets; adding your own softmax before it is a classic mistake.",
                ),
                q(
                    "What does optimizer.step() do?",
                    (
                        opt("Computes the gradients for the current batch"),
                        opt("Evaluates the model on the validation set"),
                        opt(
                            "Updates every registered weight using its .grad and the learning rate",
                            correct=True,
                        ),
                        opt("Advances the DataLoader to the next batch"),
                    ),
                    "backward() computes gradients; step() applies them - two "
                    "separate responsibilities.",
                ),
                q(
                    "The training loss oscillates wildly and sometimes explodes to "
                    "infinity. What is the first thing to try?",
                    (
                        opt("Adding more layers to the model"),
                        opt("Lowering the learning rate", correct=True),
                        opt("Removing the loss function"),
                        opt("Switching from GPU back to CPU"),
                    ),
                    "An exploding or oscillating loss is the signature of steps that "
                    "are too large - reduce lr by a factor of 10 and retry.",
                ),
            ),
        ),
        # ── 6. Training loop ─────────────────────────────────────────
        _t(
            "The training loop",
            "10 min",
            """# The training loop

Everything so far meets in five lines that you will write for the rest
of your PyTorch life. This is the heart of the framework - there is no
hidden `fit()` doing magic; you write the loop:

```python
import torch
from torch import nn

# tiny regression: learn y = 2x + 1 from noisy points
x = torch.linspace(-1, 1, 100).reshape(-1, 1)
y = 2 * x + 1 + 0.1 * torch.randn_like(x)

model = nn.Linear(1, 1)
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

for epoch in range(200):
    pred = model(x)              # 1. forward: predictions
    loss = loss_fn(pred, y)      # 2. loss: how wrong

    optimizer.zero_grad()        # 3. reset old gradients
    loss.backward()              # 4. backward: compute gradients
    optimizer.step()             # 5. update the weights

print(model.weight.item(), model.bias.item())  # close to 2.0 and 1.0
```

Run it: the printed weight and bias converge to the true 2 and 1. A
model just *learned* from data, and you can see every moving part.

The vocabulary around the loop:

- An **epoch** is one full pass over the training data.
- **`model.train()` / `model.eval()`** switch layer behavior (dropout,
  batch norm). Habit: `train()` before the loop, `eval()` before
  evaluation - even when the model has neither layer type yet.
- **Evaluation** wraps in `no_grad` and measures what you care about:

```python
model.eval()
with torch.no_grad():
    test_pred = model(x_test)
    accuracy = (test_pred.argmax(dim=1) == y_test).float().mean()
```

- **`loss.item()`** extracts the Python number for logging. Watch it
  fall epoch by epoch; if it does not, revisit the learning rate.

```mermaid
graph LR
    FW["1 forward pred"] --> LS["2 loss"]
    LS --> ZG["3 zero grad"]
    ZG --> BW["4 backward"]
    BW --> ST["5 step"]
    ST --> FW
    ST --> EV["eval with no grad each epoch"]
```

Forward, loss, zero, backward, step - say it like a mantra; every
PyTorch project from here to GPT is this loop with bigger pieces.
""",
        ),
        quiz_lesson(
            "Quiz: The training loop",
            (
                q(
                    "What is the correct order of the five training-loop steps?",
                    (
                        opt("backward, forward, loss, step, zero_grad"),
                        opt(
                            "forward, loss, zero_grad, backward, step",
                            correct=True,
                        ),
                        opt("step, zero_grad, forward, backward, loss"),
                        opt("loss, forward, step, backward, zero_grad"),
                    ),
                    "Predict, score, reset old gradients, compute new ones, update - "
                    "the canonical order (zero_grad anywhere before backward works).",
                ),
                q(
                    "What is an epoch?",
                    (
                        opt("One weight update"),
                        opt("One full pass over the training data", correct=True),
                        opt("One second of training time"),
                        opt("One layer of the network"),
                    ),
                    "Batches make up an epoch; epochs count how many times the model "
                    "has seen the whole dataset.",
                ),
                q(
                    "Why call model.eval() and wrap evaluation in torch.no_grad()?",
                    (
                        opt(
                            "eval() switches layers like dropout to inference behavior; "
                            "no_grad() skips gradient recording for speed and memory",
                            correct=True,
                        ),
                        opt("They freeze the weights permanently"),
                        opt("They are required or PyTorch raises an error"),
                        opt("They move the model back to the CPU"),
                    ),
                    "Two independent switches with one purpose: honest, efficient "
                    "evaluation - then model.train() to resume learning.",
                ),
            ),
        ),
        # ── 7. Data ──────────────────────────────────────────────────
        _t(
            "Data — Dataset and DataLoader",
            "9 min",
            """# Data — Dataset and DataLoader

Real datasets do not fit in one tensor on the GPU. PyTorch splits the
problem in two: a **`Dataset`** knows how to get *one* example, and a
**`DataLoader`** turns any dataset into shuffled **mini-batches**.

A custom dataset is a class with two methods:

```python
from torch.utils.data import Dataset, DataLoader

class PointsDataset(Dataset):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __len__(self):
        return len(self.x)          # how many examples

    def __getitem__(self, i):
        return self.x[i], self.y[i] # example number i

dataset = PointsDataset(x, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for batch_x, batch_y in loader:     # ready-made mini-batches
    ...
```

Why mini-batches instead of the whole dataset at once?

- **Memory** - a million images do not fit on any GPU at once.
- **Better training** - the slight noise of small batches actually
  helps models generalize; batch sizes of 32-256 are the norm.
- **`shuffle=True`** re-orders examples every epoch so the model never
  learns the accidental order of the file.

For the classics, `torchvision` ships datasets and the tensor
conversion in two lines:

```python
from torchvision import datasets, transforms

train_ds = datasets.MNIST(
    "data", train=True, download=True, transform=transforms.ToTensor()
)
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
```

`transform` runs on every example as it is loaded - `ToTensor()`
converts images to `[0, 1]` float tensors; augmentations (random crops,
flips) plug in the same way.

```mermaid
graph LR
    DS["Dataset len and getitem"] --> DL["DataLoader"]
    DL --> SH["Shuffle every epoch"]
    DL --> BT["Mini-batches of 32-256"]
    TF["Transform per example"] --> DS
    BT --> LOOP["Training loop consumes batches"]
```

Dataset answers "give me example i"; DataLoader answers "give me the
next shuffled batch" - and the training loop never worries about either.
""",
        ),
        quiz_lesson(
            "Quiz: Data — Dataset and DataLoader",
            (
                q(
                    "Which two methods must a custom Dataset implement?",
                    (
                        opt("__len__ and __getitem__", correct=True),
                        opt("open and close"),
                        opt("forward and backward"),
                        opt("fetch and commit"),
                    ),
                    "How many examples there are, and how to return example i - the "
                    "DataLoader builds everything else on those two.",
                ),
                q(
                    "What does the DataLoader add on top of a Dataset?",
                    (
                        opt("Gradient computation for the labels"),
                        opt("Automatic model evaluation"),
                        opt(
                            "Batching and per-epoch shuffling (plus parallel loading)",
                            correct=True,
                        ),
                        opt("Compression of the dataset on disk"),
                    ),
                    "It turns one-example access into an iterator of shuffled "
                    "mini-batches ready for the training loop.",
                ),
                q(
                    "Why train on mini-batches rather than the entire dataset per step?",
                    (
                        opt("PyTorch forbids tensors larger than 1 GB"),
                        opt(
                            "Full datasets rarely fit in memory, and the noise of "
                            "small batches helps generalization",
                            correct=True,
                        ),
                        opt("Mini-batches make the loss exactly zero"),
                        opt("Batches are only needed for text data"),
                    ),
                    "Practical memory limits plus a genuine training benefit made "
                    "batch sizes of 32-256 the standard.",
                ),
            ),
        ),
        # ── 8. End to end ────────────────────────────────────────────
        _t(
            "End to end — a digit classifier",
            "12 min",
            """# End to end — a digit classifier

Every piece from the course, assembled: train the `DigitClassifier` on
MNIST (28x28 handwritten digits), evaluate it, save it, and use the GPU
when there is one.

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

device = "cuda" if torch.cuda.is_available() else "cpu"

train_ds = datasets.MNIST("data", train=True, download=True,
                          transform=transforms.ToTensor())
test_ds = datasets.MNIST("data", train=False, download=True,
                         transform=transforms.ToTensor())
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=256)

model = nn.Sequential(               # same layers, compact form
    nn.Flatten(),
    nn.Linear(784, 128), nn.ReLU(),
    nn.Linear(128, 10),
).to(device)                         # move weights to the device

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(3):
    model.train()
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        loss = loss_fn(model(images), labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    model.eval()
    correct = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            correct += (model(images).argmax(dim=1) == labels).sum().item()
    print(f"epoch {epoch}: accuracy {correct / len(test_ds):.3f}")
```

Three epochs reach roughly 97% accuracy on a laptop CPU in about a
minute - a genuinely working digit reader from ~30 lines.

The two remaining practical skills:

**The device dance.** `.to(device)` moves the model once and every
batch as it is used; model and data must live on the **same** device or
PyTorch raises the famous "expected all tensors on the same device"
error.

**Saving and loading** uses the `state_dict` - a dictionary of weight
tensors, independent of your code layout:

```python
torch.save(model.state_dict(), "digits.pt")     # save weights

model.load_state_dict(torch.load("digits.pt"))  # load into same shape
model.eval()                                     # ready for inference
```

Save the `state_dict`, not the model object - it survives refactors and
is the convention every tutorial and codebase expects.

```mermaid
graph TD
    DATA["MNIST via DataLoader"] --> TRAIN["Training loop 3 epochs"]
    MODEL["Sequential model on device"] --> TRAIN
    TRAIN --> EVAL["eval accuracy on test set"]
    EVAL --> SAVE["save state dict"]
    SAVE --> LOAD["load state dict later"]
    LOAD --> INF["Inference with no grad"]
```

Tensors, autograd, module, loss, optimizer, loop, data - one page of
code, and it is the same page at every scale.
""",
        ),
        quiz_lesson(
            "Quiz: End to end — a digit classifier",
            (
                q(
                    "What causes the error 'expected all tensors to be on the same device'?",
                    (
                        opt("Using a batch size larger than 64"),
                        opt(
                            "The model was moved to the GPU but the data batches were "
                            "not (or vice versa)",
                            correct=True,
                        ),
                        opt("Calling backward() twice"),
                        opt("Mixing float and integer tensors"),
                    ),
                    "Model and data must live together: model.to(device) once, and "
                    "images.to(device) / labels.to(device) for every batch.",
                ),
                q(
                    "What is the recommended way to save a trained model?",
                    (
                        opt(
                            "torch.save(model.state_dict(), path) - the weights dictionary",
                            correct=True,
                        ),
                        opt("Pickling the entire Python process"),
                        opt("Copying the .py source file"),
                        opt("Printing the weights to a log file"),
                    ),
                    "The state_dict holds only the weight tensors, survives code "
                    "refactors, and is the convention everywhere.",
                ),
                q(
                    "How is test accuracy computed in the example?",
                    (
                        opt("By re-running the training loop on the test set"),
                        opt("It is read from the loss value directly"),
                        opt(
                            "argmax over the logits picks each predicted class, "
                            "compared with labels under torch.no_grad()",
                            correct=True,
                        ),
                        opt("CrossEntropyLoss returns accuracy as a second value"),
                    ),
                    "model(images).argmax(dim=1) turns logits into class predictions; "
                    "matches divided by dataset size give accuracy.",
                ),
            ),
        ),
        # ── Final quiz ───────────────────────────────────────────────
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is PyTorch?",
                    (
                        opt(
                            "A NumPy-like tensor library with automatic differentiation and GPU support, plus a neural-network toolkit on top",
                            correct=True,
                        ),
                        opt("A database for storing model weights"),
                        opt("A web framework for serving predictions"),
                        opt("A GPU driver installer"),
                    ),
                    "Tensors + autograd + torch.nn - every lesson in this course is "
                    "one of those three unfolding.",
                ),
                q(
                    "A tensor operation fails with a size mismatch. What should you inspect first?",
                    (
                        opt("The .shape of every tensor involved", correct=True),
                        opt("The Python version"),
                        opt("The learning rate"),
                        opt("The random seed"),
                    ),
                    "Most PyTorch bugs are shape bugs; printing .shape at each step "
                    "finds them fastest.",
                ),
                q(
                    "What happens when loss.backward() is called?",
                    (
                        opt("The optimizer updates all the weights"),
                        opt(
                            "Autograd walks the recorded graph in reverse and fills "
                            ".grad for every tensor with requires_grad=True",
                            correct=True,
                        ),
                        opt("The model's layers are re-initialized"),
                        opt("The DataLoader advances one batch"),
                    ),
                    "backward computes gradients; the separate optimizer.step() applies them.",
                ),
                q(
                    "Forgetting optimizer.zero_grad() in the loop causes…",
                    (
                        opt("an immediate exception"),
                        opt("the model to train twice as fast"),
                        opt(
                            "gradients from previous steps to accumulate into each "
                            "update, corrupting training",
                            correct=True,
                        ),
                        opt("the loss to become exactly zero"),
                    ),
                    "backward() adds into .grad, so stale gradients mix into every "
                    "step until they are zeroed.",
                ),
                q(
                    "Which pairing is correct for a 10-class classification model?",
                    (
                        opt("Sigmoid output layer + MSELoss"),
                        opt("Softmax layer + L1Loss"),
                        opt("Raw logits output + CrossEntropyLoss", correct=True),
                        opt("Raw logits output + MSELoss on class indices"),
                    ),
                    "CrossEntropyLoss applies the softmax internally - the model "
                    "outputs plain logits of shape [batch, 10].",
                ),
                q(
                    "Recite the training loop in order.",
                    (
                        opt("forward, loss, zero_grad, backward, step", correct=True),
                        opt("zero_grad, step, forward, loss, backward"),
                        opt("backward, step, loss, forward, zero_grad"),
                        opt("loss, backward, forward, zero_grad, step"),
                    ),
                    "Predict, score, reset, differentiate, update - the mantra behind "
                    "every PyTorch project.",
                ),
                q(
                    "What separates model.train() from model.eval()?",
                    (
                        opt("eval() deletes the gradients; train() restores them"),
                        opt(
                            "They switch the behavior of layers like dropout and batch "
                            "norm between learning and inference modes",
                            correct=True,
                        ),
                        opt("train() moves to GPU; eval() moves to CPU"),
                        opt("Nothing - they are synonyms"),
                    ),
                    "Some layers behave differently while learning; the two calls "
                    "flip that switch - pair eval() with torch.no_grad().",
                ),
                q(
                    "What division of labor do Dataset and DataLoader have?",
                    (
                        opt(
                            "Dataset returns one example by index; DataLoader batches, "
                            "shuffles and iterates them",
                            correct=True,
                        ),
                        opt("Dataset trains the model; DataLoader evaluates it"),
                        opt("Dataset lives on GPU; DataLoader on CPU"),
                        opt("They are two names for the same class"),
                    ),
                    "__len__/__getitem__ on one side; batch_size and shuffle on the other.",
                ),
                q(
                    "Your training runs but the loss barely moves. Which is the most "
                    "reasonable first experiment?",
                    (
                        opt("Delete the nonlinearities to simplify the model"),
                        opt(
                            "Raise the learning rate (or check it is not absurdly low)",
                            correct=True,
                        ),
                        opt("Reduce the dataset to 10 examples"),
                        opt("Remove zero_grad to let gradients accumulate"),
                    ),
                    "A flat loss usually means steps too small (or a wiring bug); the "
                    "learning rate is the first dial to turn.",
                ),
                q(
                    "Which snippet correctly prepares a saved model for predictions?",
                    (
                        opt(
                            "model.load_state_dict(torch.load('m.pt')); model.eval(); "
                            "predictions inside torch.no_grad()",
                            correct=True,
                        ),
                        opt("model = torch.load_source('m.py'); model.run()"),
                        opt("torch.save(model, 'm.pt'); model.train()"),
                        opt("model.load_weights('m.pt', gradients=True)"),
                    ),
                    "Load the state_dict into a matching architecture, switch to "
                    "eval mode, and predict without building graphs.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PYTORCH_COURSES: tuple[SeedCourse, ...] = (_PYTORCH_BASICS,)
