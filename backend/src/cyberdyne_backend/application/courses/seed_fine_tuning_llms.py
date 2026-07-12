"""Academy seed content - Fine-Tuning Large Language Models.

A hands-on course on fine-tuning, built from the ground up: first the mechanics
of training and fine-tuning a small neural network in PyTorch, then scaling the
same ideas to large language models - transfer learning, LoRA and QLoRA,
instruction-tuning data, evaluation and deployment. The second half is a set of
practitioner video lessons (training a tiny LLM from scratch, fine-tuning an LLM
in minutes, a full deep dive, tiny on-device agents, and steering behavior
without fine-tuning), each with a written summary, main ideas and a mindmap
below the player. Every content lesson is followed by a checkpoint quiz and the
course closes with a comprehensive final quiz.
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


_FINE_TUNING_LLMS = SeedCourse(
    slug="fine-tuning-llms",
    title="Fine-Tuning Large Language Models",
    description=(
        "Fine-tune models from the ground up: start with a small neural network "
        "in PyTorch, then scale to large language models with transfer learning, "
        "LoRA and QLoRA, instruction-tuning data, evaluation and deployment - "
        "with hands-on code, diagrams, and practitioner video lessons."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Welcome - how this course works",
            "6 min",
            "# Fine-Tuning Large Language Models\n\nFine-tuning is how you take a model that already knows a lot and teach it to do\n**your** task, in **your** style, on **your** data. This course starts from the\nground up: first you fine-tune a small neural network in **PyTorch** so the\nmechanics are concrete, then you scale the same ideas up to large language\nmodels (LLMs) - LoRA, QLoRA, instruction tuning, evaluation and deployment.\n\nThe approach is **hands-on and incremental**. Every lesson explains one idea\ndirectly, shows it in real PyTorch or Hugging Face code, and draws it as a\ndiagram. After each lesson there is a short quiz.\n\nThe second half of the course is a set of **video lessons** from practitioners -\ntraining a tiny LLM from scratch, fine-tuning an LLM in minutes, a full\nfine-tuning deep dive, pushing tiny on-device models from 46 percent to 90\npercent accuracy, and when to steer a model **without** fine-tuning at all.\nEach video has a written summary, the main ideas, and a mindmap below the\nplayer.\n\nWhat you will be able to do by the end: decide when fine-tuning is the right\ntool, prepare a dataset, run a parameter-efficient fine-tune, and evaluate and\nship the result.\n",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How does this course start?",
                    (
                        opt(
                            "With fine-tuning a small model in PyTorch, then scaling to LLMs",
                            correct=True,
                        ),
                        opt("With deploying a giant model on a cluster"),
                        opt("With no code at all"),
                    ),
                ),
                q(
                    "What is in the second half of the course?",
                    (
                        opt(
                            "Video lessons from practitioners, each with a written summary and mindmap",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A single PDF"),
                    ),
                ),
            ),
        ),
        _t(
            "What fine-tuning is and why it matters",
            "9 min",
            '# What fine-tuning is and why it matters\n\nA modern language model is built in two stages. **Pretraining** runs\nself-supervised next-token prediction over a huge text corpus - this is the\nexpensive step that gives the model general language ability. **Fine-tuning**\nthen continues training on a much smaller, curated dataset to adapt the model\nto a specific task, domain, or style.\n\nYou almost never train from scratch. You start from a **base model** (raw\nnext-token predictor) or an **instruct model** (already tuned to follow\ninstructions) and nudge its weights with your data.\n\n**When to fine-tune** and when not to:\n\n- **Prompting** - change behavior with instructions only. Free and instant. Try this first.\n- **Retrieval augmented generation (RAG)** - inject facts at inference time. Best when the need is fresh knowledge.\n- **Fine-tuning** - change the weights. Best for a consistent style, a narrow task, a format the model keeps getting wrong, or to make a small model behave like a bigger one.\n\nThe rule of thumb: fine-tuning teaches **behavior and form**, not fresh\n**facts**. For changing facts, prefer RAG.\n\n```mermaid\ngraph LR\n    A["Pretraining on huge corpus"] --> B["Base model"]\n    B --> C["Fine-tuning on your data"]\n    C --> D["Adapted model"]\n    B --> E["Prompting only"]\n    B --> F["RAG at inference"]\n```\n\nFine-tuning matters because it turns a general model into a reliable specialist\nyou own and control - often a small model that is cheaper to run than calling a\ngiant hosted one.\n',
        ),
        quiz_lesson(
            "Quiz: What fine-tuning is and why it matters",
            (
                q(
                    "What does fine-tuning change, compared with prompting or RAG?",
                    (
                        opt("It changes the model's weights", correct=True),
                        opt("It only changes the input prompt"),
                        opt("It only adds documents at inference time"),
                    ),
                    "Fine-tuning continues training and updates the weights; prompting and RAG leave the weights untouched.",
                ),
                q(
                    "For adding fresh, frequently-changing facts, which tool is usually the best fit?",
                    (
                        opt("Retrieval augmented generation (RAG)", correct=True),
                        opt("Full fine-tuning every hour"),
                        opt("Deleting the base model"),
                    ),
                    "Fine-tuning teaches behavior and form; RAG is the better tool for injecting up-to-date facts.",
                ),
                q(
                    "What is a 'base model'?",
                    (
                        opt("A raw next-token predictor from pretraining", correct=True),
                        opt("A model that has been quantized to 4-bit"),
                        opt("A dataset of instructions"),
                    ),
                ),
            ),
        ),
        _t(
            "Training a neural network in PyTorch",
            "11 min",
            '# Training a neural network in PyTorch\n\nBefore fine-tuning an LLM, you need the mechanics of training any network in\nPyTorch. Four pieces do all the work:\n\n- **Tensors** - n-dimensional arrays that live on CPU or GPU.\n- **Autograd** - PyTorch records operations and computes gradients automatically with `.backward()`.\n- **Module** - `nn.Module` holds the layers and their learnable parameters.\n- **Optimizer** - updates the parameters using the gradients (for example `Adam`).\n\nThe **training loop** is always the same shape: forward pass, compute loss,\nzero the old gradients, backward pass, optimizer step.\n\n```python\nimport torch\nfrom torch import nn\n\nmodel = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))\nloss_fn = nn.CrossEntropyLoss()\noptimizer = torch.optim.Adam(model.parameters(), lr=1e-3)\n\nfor images, labels in train_loader:\n    logits = model(images)            # forward pass\n    loss = loss_fn(logits, labels)    # how wrong we are\n    optimizer.zero_grad()             # clear old gradients\n    loss.backward()                   # autograd computes gradients\n    optimizer.step()                  # update the weights\n```\n\nThe **loss** measures error; **gradients** point in the direction that reduces\nit; the **learning rate** controls how big a step you take. Training is just\nthis loop repeated over many **epochs** until the loss stops improving.\n\n```mermaid\ngraph LR\n    A["Forward pass"] --> B["Compute loss"]\n    B --> C["zero grad"]\n    C --> D["loss backward"]\n    D --> E["optimizer step"]\n    E --> A\n```\n\nEvery fine-tuning method in this course is a variation on this exact loop - what\nchanges is which parameters you update and how you feed in the data.\n',
        ),
        quiz_lesson(
            "Quiz: Training a neural network in PyTorch",
            (
                q(
                    "What is the correct order inside a PyTorch training step?",
                    (
                        opt("forward, loss, zero_grad, backward, step", correct=True),
                        opt("backward, step, forward, loss, zero_grad"),
                        opt("step, forward, backward, loss, zero_grad"),
                    ),
                    "You compute outputs and loss, clear old gradients, backpropagate, then update the weights.",
                ),
                q(
                    "What does `loss.backward()` do?",
                    (
                        opt(
                            "Uses autograd to compute gradients of the loss w.r.t. parameters",
                            correct=True,
                        ),
                        opt("Updates the weights directly"),
                        opt("Loads the next batch of data"),
                    ),
                    "backward() computes gradients; the optimizer's step() applies them.",
                ),
                q(
                    "Why call `optimizer.zero_grad()` each step?",
                    (
                        opt(
                            "PyTorch accumulates gradients, so old ones must be cleared",
                            correct=True,
                        ),
                        opt("It frees the GPU entirely"),
                        opt("It shuffles the dataset"),
                    ),
                ),
            ),
        ),
        _t(
            "Fine-tuning a small model in PyTorch",
            "11 min",
            '# Fine-tuning a small model in PyTorch\n\nFine-tuning is **transfer learning**: take a network already trained on a large\ndataset, keep most of what it learned, and adapt it to a new task with a small\ndataset. The classic recipe:\n\n1. **Load** a pretrained model.\n2. **Freeze** the early layers (the general feature extractor) by setting `requires_grad = False`.\n3. **Replace the head** with a new output layer for your task.\n4. **Train** only the new head (and optionally unfreeze the top layers later with a small learning rate).\n\n```python\nimport torch\nfrom torchvision import models\n\nmodel = models.resnet18(weights="IMAGENET1K_V1")\n\nfor param in model.parameters():      # 1-2. freeze the backbone\n    param.requires_grad = False\n\nmodel.fc = torch.nn.Linear(model.fc.in_features, 3)   # 3. new 3-class head\n\noptimizer = torch.optim.Adam(\n    model.fc.parameters(), lr=1e-3    # 4. train only the head\n)\n```\n\nTwo ideas carry straight over to LLMs. **Freezing** means you update only a\nsmall part of the network, which is faster and needs far less memory.\n**Learning rate discipline** - fine-tuning uses a **much smaller** learning\nrate than training from scratch, because you only want to nudge good weights,\nnot overwrite them.\n\n```mermaid\ngraph LR\n    A["Pretrained model"] --> B["Freeze backbone"]\n    B --> C["Replace head"]\n    C --> D["Train head on small data"]\n    D --> E["Optional unfreeze top with tiny LR"]\n```\n\nIf you understand this small-model example, LoRA on an LLM will feel familiar:\nit is the same instinct - update a tiny slice of the network instead of all of\nit.\n',
        ),
        quiz_lesson(
            "Quiz: Fine-tuning a small model in PyTorch",
            (
                q(
                    "Why do you freeze the backbone when fine-tuning a small pretrained model?",
                    (
                        opt(
                            "To reuse learned features and update only a small, cheap part",
                            correct=True,
                        ),
                        opt("To make the model forget everything it learned"),
                        opt("Because frozen layers train faster than the optimizer"),
                    ),
                    "Freezing keeps the general features and means fewer parameters to update - faster and lighter.",
                ),
                q(
                    "Compared with training from scratch, fine-tuning uses a learning rate that is:",
                    (
                        opt("Much smaller", correct=True),
                        opt("Much larger"),
                        opt("Exactly the same and never changes"),
                    ),
                    "A small LR nudges the good pretrained weights instead of overwriting them.",
                ),
                q(
                    "In PyTorch, how do you stop a parameter from being updated?",
                    (
                        opt("Set param.requires_grad = False", correct=True),
                        opt("Delete the parameter from the model"),
                        opt("Call param.backward()"),
                    ),
                ),
            ),
        ),
        _t(
            "From small models to large language models",
            "10 min",
            '# From small models to large language models\n\nAn LLM is still a neural network trained with the loop you already know - it is\njust much bigger and trained on text. Three ideas make it an LLM:\n\n- **Tokenization** - text is split into **tokens** (subword pieces) and mapped to integer IDs. The model only ever sees numbers.\n- **Next-token prediction** - the model is trained to predict the next token given all previous ones. That single objective, at scale, produces fluent language.\n- **The transformer** - the architecture (attention + feed-forward blocks) that made training at this scale practical.\n\nA **base model** only predicts the next token. An **instruct** or **chat**\nmodel has been fine-tuned so that, given an instruction, it produces a helpful\nanswer instead of just continuing the text.\n\n```python\nfrom transformers import AutoTokenizer, AutoModelForCausalLM\n\ntok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")\nmodel = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")\n\nids = tok("Fine-tuning is", return_tensors="pt")\nout = model.generate(**ids, max_new_tokens=20)\nprint(tok.decode(out[0]))\n```\n\nThe loss during LLM fine-tuning is the same **cross-entropy** over the\nvocabulary that you would use for any classifier - here the "classes" are the\ntokens in the vocabulary, and the model predicts one at each position.\n\n```mermaid\ngraph LR\n    A["Raw text"] --> B["Tokenizer"]\n    B --> C["Token IDs"]\n    C --> D["Transformer"]\n    D --> E["Next-token probabilities"]\n```\n\nBecause the objective and the training loop are unchanged, everything you learn\nabout fine-tuning small models transfers - the challenge with LLMs is **scale\nand memory**, which is exactly what the next lesson solves.\n',
        ),
        quiz_lesson(
            "Quiz: From small models to large language models",
            (
                q(
                    "What objective is an LLM trained on?",
                    (
                        opt("Predicting the next token given the previous tokens", correct=True),
                        opt("Sorting tokens alphabetically"),
                        opt("Compressing images"),
                    ),
                    "Self-supervised next-token prediction at scale produces fluent language.",
                ),
                q(
                    "What is the difference between a base model and an instruct model?",
                    (
                        opt(
                            "The instruct model was fine-tuned to follow instructions helpfully",
                            correct=True,
                        ),
                        opt("The base model is always larger"),
                        opt("The instruct model cannot generate text"),
                    ),
                ),
                q(
                    "What does a tokenizer do?",
                    (
                        opt(
                            "Splits text into subword tokens and maps them to integer IDs",
                            correct=True,
                        ),
                        opt("Computes gradients for the optimizer"),
                        opt("Stores the model on the GPU"),
                    ),
                ),
            ),
        ),
        _t(
            "Full fine-tuning vs parameter-efficient fine-tuning",
            "12 min",
            '# Full fine-tuning vs parameter-efficient fine-tuning\n\n**Full fine-tuning** updates every weight in the model. It works, but for a\nmulti-billion-parameter LLM it needs enormous memory: the weights, their\ngradients, and the optimizer state (Adam keeps two extra values per parameter)\nall sit on the GPU at once. Fine-tuning a 7B model in full precision this way\ncan need well over 100 GB of GPU memory.\n\n**Parameter-efficient fine-tuning (PEFT)** freezes the original weights and\ntrains a tiny number of new ones. The dominant method is **LoRA** (Low-Rank\nAdaptation): instead of updating a big weight matrix W, you learn two small\nmatrices A and B and add their product as a low-rank update.\n\n```text\nFull:  W_new = W + Delta W          (Delta W is full size)\nLoRA:  W_new = W + (B * A)          (A is r x k, B is d x r, rank r is small)\n\nA 4096 x 4096 layer has ~16.7M weights.\nWith rank r = 8, LoRA trains only 4096*8 + 8*4096 = ~65.5K weights - about 0.4 percent.\n```\n\n**QLoRA** goes further: it loads the frozen base model in **4-bit** quantized\nform and trains LoRA adapters on top, so a 7B model fine-tunes on a single\nconsumer GPU. Tools like **PEFT**, **Unsloth**, and **TRL** wrap this up.\n\n```python\nfrom peft import LoraConfig, get_peft_model\n\nconfig = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"])\nmodel = get_peft_model(base_model, config)\nmodel.print_trainable_parameters()   # e.g. 0.4 percent of all params\n```\n\n```mermaid\ngraph TD\n    A["Pretrained weight W frozen"] --> C["Sum"]\n    B["LoRA update B times A"] --> C\n    C --> D["Adapted output"]\n```\n\nThe payoff: LoRA and QLoRA make fine-tuning cheap enough to run on one GPU, and\nthe small adapter (a few megabytes) can be shipped separately from the base\nmodel.\n',
        ),
        quiz_lesson(
            "Quiz: Full fine-tuning vs parameter-efficient fine-tuning",
            (
                q(
                    "What does LoRA train instead of the full weight matrix?",
                    (
                        opt(
                            "Two small low-rank matrices whose product is added to the frozen weight",
                            correct=True,
                        ),
                        opt("A brand new full-size copy of every layer"),
                        opt("Only the tokenizer vocabulary"),
                    ),
                    "LoRA freezes W and learns a low-rank update B*A, a tiny fraction of the parameters.",
                ),
                q(
                    "What does the 'Q' in QLoRA add over plain LoRA?",
                    (
                        opt(
                            "It loads the frozen base model in 4-bit quantized form to save memory",
                            correct=True,
                        ),
                        opt("It doubles the learning rate"),
                        opt("It removes the need for any training data"),
                    ),
                    "QLoRA quantizes the base to 4-bit so large models fit on a single consumer GPU.",
                ),
                q(
                    "Why is full fine-tuning of a large LLM so memory-hungry?",
                    (
                        opt(
                            "Weights, gradients, and optimizer state for every parameter sit on the GPU",
                            correct=True,
                        ),
                        opt("Because it never uses a GPU"),
                        opt("Because it must store the entire internet"),
                    ),
                ),
            ),
        ),
        _t(
            "Preparing data for instruction tuning",
            "10 min",
            '# Preparing data for instruction tuning\n\nFor instruction fine-tuning, data quality matters more than quantity. A good\ndataset is a set of **examples of the behavior you want** - typically an\ninstruction (and optional input) paired with the ideal response.\n\nModels expect a specific **chat template** - special tokens that mark the\nsystem, user, and assistant turns. You must format your data with the **same\ntemplate the model was trained with**, or results degrade. Hugging Face\ntokenizers do this with `apply_chat_template`.\n\n```python\nmessages = [\n    {"role": "system", "content": "You are a terse SQL assistant."},\n    {"role": "user", "content": "Users older than 30?"},\n    {"role": "assistant", "content": "SELECT * FROM users WHERE age > 30;"},\n]\ntext = tokenizer.apply_chat_template(messages, tokenize=False)\n```\n\nPractical guidance from the field:\n\n- **Quality over quantity** - a few hundred clean, consistent examples often beat tens of thousands of noisy ones.\n- **Be consistent** - one format, one style; the model copies your patterns, warts and all.\n- **Cover the edges** - include the hard and unusual cases you care about.\n- **Match the template** - use the model\'s own chat format and special tokens.\n- **Hold some back** - keep a validation split you never train on.\n\n```mermaid\ngraph LR\n    A["Raw examples"] --> B["Clean and deduplicate"]\n    B --> C["Format with chat template"]\n    C --> D["Train and validation split"]\n    D --> E["Ready for fine-tuning"]\n```\n\nDatasets are usually stored as **JSONL** (one JSON object per line). Getting the\ndata right is the highest-leverage part of a fine-tuning project - the training\nrun is the easy part.\n',
        ),
        quiz_lesson(
            "Quiz: Preparing data for instruction tuning",
            (
                q(
                    "For instruction tuning, what generally matters most?",
                    (
                        opt(
                            "A small set of clean, consistent, high-quality examples", correct=True
                        ),
                        opt("The largest possible number of noisy examples"),
                        opt("Using no examples at all"),
                    ),
                    "Quality and consistency beat raw volume; the model copies whatever patterns it sees.",
                ),
                q(
                    "Why must you format data with the model's own chat template?",
                    (
                        opt(
                            "The model was trained with those special tokens and role markers",
                            correct=True,
                        ),
                        opt("Because JSONL is required by law"),
                        opt("To make the file larger"),
                    ),
                    "Mismatched templates degrade results; apply_chat_template uses the correct format.",
                ),
                q(
                    "What is a validation split for?",
                    (
                        opt(
                            "Data held out from training to check for overfitting and real progress",
                            correct=True,
                        ),
                        opt("Extra data mixed into training to speed it up"),
                        opt("The tokenizer vocabulary"),
                    ),
                ),
            ),
        ),
        _t(
            "Evaluating and deploying fine-tuned models",
            "10 min",
            '# Evaluating and deploying fine-tuned models\n\nTraining loss going down is necessary but not sufficient. You must check the\nmodel on data it never trained on.\n\n**Watch for overfitting.** If training loss keeps falling while **validation**\nloss starts rising, the model is memorizing the training set instead of\ngeneralizing. Stop early, add data, or reduce how long or how hard you train.\n\n**Evaluate the behavior, not just the loss.** Run the model on a held-out set\nand judge the actual outputs - exact-match or task metrics where you can, and\nhuman or model-graded review for open-ended tasks.\n\n**Deploying a LoRA fine-tune** has two options:\n\n- **Ship the adapter** next to the base model and load both at runtime (tiny, swappable).\n- **Merge** the adapter into the base weights to get a single standalone model.\n\n```python\nmerged = model.merge_and_unload()          # fold LoRA into the base weights\nmerged.save_pretrained("my-finetuned-llm")  # one standalone model\n```\n\nFor efficient serving you often **quantize** the merged model (for example to\n**GGUF** for `llama.cpp`, or serve with **vLLM**), trading a little quality for\nmuch lower memory and higher throughput.\n\n```mermaid\ngraph LR\n    A["Fine-tuned adapter"] --> B["Evaluate on held-out set"]\n    B --> C["Merge into base or keep adapter"]\n    C --> D["Quantize"]\n    D --> E["Serve"]\n```\n\nA fine-tune is only done when it measurably beats the base model on **your**\ntask and runs within **your** budget - evaluation and deployment are part of the\njob, not an afterthought.\n',
        ),
        quiz_lesson(
            "Quiz: Evaluating and deploying fine-tuned models",
            (
                q(
                    "Training loss falls but validation loss rises. What is happening?",
                    (
                        opt("Overfitting - the model is memorizing the training set", correct=True),
                        opt("The model is perfectly generalizing"),
                        opt("The tokenizer has changed"),
                    ),
                    "Diverging train and validation loss is the classic sign of overfitting.",
                ),
                q(
                    "What does merging a LoRA adapter produce?",
                    (
                        opt(
                            "A single standalone model with the adapter folded into the base weights",
                            correct=True,
                        ),
                        opt("A larger training dataset"),
                        opt("A new tokenizer"),
                    ),
                    "merge_and_unload folds the low-rank update into W so you can ship one model.",
                ),
                q(
                    "Why quantize a model to a format like GGUF before serving?",
                    (
                        opt(
                            "Lower memory and higher throughput, trading a little quality",
                            correct=True,
                        ),
                        opt("To make it impossible to run on CPU"),
                        opt("To delete the fine-tuned weights"),
                    ),
                ),
            ),
        ),
        video_lesson(
            "Video: Train a tiny LLM from scratch on your PC",
            "https://www.youtube.com/watch?v=T9egZA5ppQw",
            duration="13 min",
            body='## Summary\n\nThis video shows how to train your own tiny large language model from scratch on an ordinary PC, with no GPU cluster required. Gary Sims walks through two hands-on projects. The first trains a 10 million parameter model on a roughly 1 megabyte text file containing the complete works of Shakespeare. With a decent GPU this finishes in a few minutes to under an hour, while on a CPU-only mini PC it ran for about 8 hours, so it can be left going overnight. Once trained, you feed the model a prompt such as "to be or not to be" and it generates a completion.\n\nThe starting point is a GitHub workshop project called "train an LLM from scratch" by Angelo, which strips Andrej Karpathy\'s nanoGPT down to the essentials and scales it to a 10 million parameter model you can train in a single session. That project deliberately does not publish the finished code so you write each piece yourself. Gary instead publishes a complete kit: generate.py to prompt the model, train.py to train it, model.py for the plumbing, a downloadable pre-trained checkpoint (checkpointfinal.pt), a readme covering prerequisites like PyTorch, and a data folder with Shakespeare and Sherlock Holmes texts. You install the right PyTorch variant for your hardware (CPU, Nvidia, Intel, or AMD) to get the best acceleration.\n\nTo train you run train.py, optionally pointing it at another dataset such as the Sherlock Holmes collection. To generate you run generate.py with a prompt against the checkpoint, and you can pass flags like temperature, top-k, and a seed to influence the output. The Shakespeare model produces text that sounds like Shakespeare but is essentially nonsense, which illustrates both the power and the limits of training on only one megabyte of data.\n\nThe second project trains a 24 million parameter model on the TinyStories dataset, a 2.1 gigabyte synthetic collection of very short stories using only vocabulary a three or four year old would understand. Because the sentences are simple and the vocabulary is small, the model learns the relationships between words much faster and produces fluent, consistent short stories, though it cannot answer factual questions like the capital of France. This train.py is more sophisticated: it can auto-size the model, and it can be interrupted and resumed so training can be spread across several days.\n\nTraining is driven by arguments such as tokens-per-parameter, which sizes the model automatically (studies suggest 20 is a good optimum), and a maximum step count that you raise to resume, aiming for around 45,000 steps for a good model. Gary notes that going further pulls you down a rabbit hole of ever larger models, including a 50 million parameter model trained on 16,000 public domain books in the cloud, whose results were far less impressive than TinyStories. The takeaway is that building and training these tiny models is a fun, accessible way to understand how large language models actually work.\n\n## Main ideas\n\n- **Tiny LLM on a PC**: You can train a small language model from scratch on a normal PC, with a GPU making it far faster than CPU.\n- **10M Shakespeare model**: A 10 million parameter model trains on about 1 megabyte of Shakespeare in minutes on a GPU or roughly 8 hours on CPU.\n- **nanoGPT workshop roots**: The project scales Andrej Karpathy\'s nanoGPT down so you write the whole GPT training pipeline yourself.\n- **The training kit**: The kit includes train.py to train, generate.py to prompt, model.py plumbing, a downloadable checkpoint, and datasets.\n- **PyTorch variants**: You must install the PyTorch build matching your hardware, whether CPU, Nvidia, Intel, or AMD, for best acceleration.\n- **Generation flags**: Generation is controlled with a prompt plus flags like temperature, top-k, and seed that shape the output.\n- **TinyStories dataset**: TinyStories is a 2.1 gigabyte synthetic set of simple short stories that lets a small model learn fluently and fast.\n- **Interruptible training**: The bigger 24 million parameter model can be stopped and resumed with a higher max-steps, spreading training over days.\n- **Tokens per parameter**: The tokens-per-parameter argument auto-sizes the model, with about 20 cited as a good optimum, targeting near 45,000 steps.\n\n## Mindmap\n\n```mermaid\nmindmap\n  root((Train A Tiny LLM))\n    Shakespeare Model\n      10 million parameters\n      1 megabyte data\n      Minutes on GPU\n      8 hours on CPU\n    The Kit\n      train script\n      generate script\n      model plumbing\n      Downloadable checkpoint\n    TinyStories Model\n      24 million parameters\n      Gigabyte scale data\n      Simple vocabulary\n      Fluent short stories\n    Training Controls\n      Tokens per parameter\n      Max steps 45000\n      Interrupt and resume\n      Temperature and top-k\n    Learning Goal\n      Understand how LLMs work\n      Scale up later\n```\n',
        ),
        quiz_lesson(
            "Quiz: Video: Train a tiny LLM from scratch on your PC",
            (
                q(
                    "In the video, what size model is trained on the roughly 1 megabyte complete works of Shakespeare?",
                    (
                        opt("A 10 million parameter model", correct=True),
                        opt("A 24 million parameter model"),
                        opt("A 1 billion parameter model"),
                        opt("A 50 million parameter model"),
                    ),
                    "Gary trains a 10 million parameter model on about 1 megabyte of Shakespeare text; the 24 million parameter model is used later with the larger TinyStories dataset.",
                ),
                q(
                    "Why does the TinyStories dataset let a very small model learn to produce fluent, consistent stories?",
                    (
                        opt(
                            "It uses simple sentences and a small vocabulary a three or four year old would understand",
                            correct=True,
                        ),
                        opt("It contains factual answers like the capital of France"),
                        opt("It is written entirely in Shakespearean English"),
                        opt("It requires a large GPU cluster to process"),
                    ),
                    "TinyStories is a synthetic dataset of short stories using only words a young child would know, so the simple structure and limited vocabulary let a small model learn word relationships much faster.",
                ),
                q(
                    "What does the tokens-per-parameter argument do when training the larger model?",
                    (
                        opt(
                            "It automatically sizes the model, with about 20 cited as a good optimum",
                            correct=True,
                        ),
                        opt("It sets the random seed used during text generation"),
                        opt("It selects which PyTorch variant to install"),
                        opt("It downloads the pre-trained checkpoint from HuggingFace"),
                    ),
                    "Tokens-per-parameter works out how big the model should be based on how many tokens fit each parameter, and the video mentions studies suggesting 20 is a good optimum value.",
                ),
            ),
        ),
        video_lesson(
            "Video: Fine-tune your own LLM in minutes",
            "https://www.youtube.com/watch?v=g80Q1sVtikE",
            duration="13 min",
            body="## Summary\n\nThis lesson is a fast, end-to-end walkthrough of fine-tuning your own open-source LLM. Fine-tuning is defined as adjusting a base model's weights to improve performance on specific tasks, and the video argues that a small fine-tuned model can outperform much larger general models on the task you care about. Beyond raw performance, the video frames fine-tuning as a business moat (Y Combinator lists fine-tuned models among its most requested startup categories) and as the mechanism behind private, uncensored, and personalized models.\n\nThe practical demo uses Unsloth, an open-source library that supports many model families (GPT OSS, Gemma, Qwen, Phi, Mistral, Llama). The presenter chooses OpenAI's GPT OSS 20B because it is both strong and small enough to run locally. All the work happens in a Google Colab notebook, which provides a free Tesla T4 GPU. The core workflow is a sequence of notebook cells: install dependencies (numpy, transformers, and PyTorch), load the chosen model, add LoRA adapters, prepare a dataset, and then run the training loop.\n\nLoRA adapters are what make this cheap: instead of updating every weight, only a small subset of parameters is actually fine-tuned. For data, the notebook ships with the Hugging Face multilingual-thinking dataset, a reasoning dataset focused on planning and tool calling that teaches agentic behavior. The presenter shows how to swap in your own dataset by pasting its name, and warns about a common error: some datasets contain multiple JSONL files, so you must point the loader at one specific file rather than the whole dataset.\n\nBefore training, a cell applies a standardized chat template that converts ShareGPT-style conversations into ChatML, mapping roles like human and GPT onto user and assistant. GPT OSS specifically uses OpenAI's new Harmony response format, which lets the model emit separate channels for chain-of-thought, tool-calling preambles, and regular responses. Training in the demo runs a short 60-step run on the free T4 and takes roughly 10 to 11 minutes; a real full run would uncomment the full-run settings and ideally use a faster GPU like an A100 or a TPU.\n\nFinally the video covers inference and saving. Inference simply means running the finished model to chat with it and compare it against the base model. You can pull GPT OSS locally through Ollama to run it privately, and you can save your fine-tuned model either to your own machine or push it to Hugging Face using your username and secret token, from where it can power a full web app.\n\n## Main ideas\n\n- **Fine-tuning**: Adjusting a base model's weights so a small model beats bigger general models on a specific task.\n- **Business moat**: Owning a fine-tuned model is a defensible product that is hard for large labs to replace.\n- **Unsloth**: An open-source library that fine-tunes many model families through simple Colab notebook cells.\n- **GPT OSS 20B**: The chosen open model, strong yet small enough to run locally.\n- **Google Colab plus T4**: A free hosted Jupyter notebook with a free Tesla T4 GPU to run the training code.\n- **LoRA adapters**: Only a small fraction of parameters is trained, making fine-tuning fast and cheap.\n- **Dataset gotcha**: When a dataset has multiple JSONL files you must load one specific file or it errors.\n- **Chat template and Harmony**: ShareGPT data is converted to ChatML, and GPT OSS uses OpenAI Harmony with separate channels.\n- **Inference and saving**: Run the model to compare with the base, then save locally or push to Hugging Face.\n\n## Mindmap\n\n```mermaid\nmindmap\n  root((Fine Tuning LLMs))\n    What It Is\n      Adjust base model weights\n      Improve specific tasks\n      Beats bigger models\n    Model Choice\n      GPT OSS 20B\n      GPT OSS 120B\n      Runs locally\n    Tooling\n      Unsloth library\n      Google Colab\n      Tesla T4 GPU\n      PyTorch\n    Training Steps\n      Install dependencies\n      Load model\n      Add LoRA adapters\n      Prepare dataset\n      Run training\n    Dataset\n      Multilingual thinking data\n      Reasoning and tool calling\n      Pick one JSONL file\n    After Training\n      Run inference\n      Save locally\n      Push to Hugging Face\n```",
        ),
        quiz_lesson(
            "Quiz: Video: Fine-tune your own LLM in minutes",
            (
                q(
                    "According to the video, what is fine-tuning?",
                    (
                        opt(
                            "Adjusting a base model's weights to improve performance on specific tasks",
                            correct=True,
                        ),
                        opt("Writing a longer system prompt so the model behaves differently"),
                        opt("Training a brand new model from scratch on random data"),
                        opt("Increasing a model's context window so it reads more text"),
                    ),
                    "The video opens by defining fine-tuning as adjusting a base model's weights to improve the model's performance on certain specific tasks, which lets small models outperform much larger ones on that task.",
                ),
                q(
                    "What tooling stack does the presenter use to run the fine-tuning?",
                    (
                        opt(
                            "The Unsloth library inside a Google Colab notebook on a free Tesla T4 GPU",
                            correct=True,
                        ),
                        opt("OpenAI's hosted fine-tuning API from the command line"),
                        opt("A local install of PyTorch Lightning on an H100"),
                        opt("Hugging Face AutoTrain running on a Google TPU"),
                    ),
                    "The demo uses Unsloth, an open-source fine-tuning library, run in a Google Colab notebook that provides a free Tesla T4 GPU to execute the training code.",
                ),
                q(
                    "In the demo, what is the role of the LoRA adapters cell?",
                    (
                        opt(
                            "It makes only a small part of the model's parameters get fine-tuned",
                            correct=True,
                        ),
                        opt("It converts the ShareGPT dataset into ChatML format"),
                        opt("It downloads the base model from Hugging Face"),
                        opt("It enables the model to output separate chain-of-thought channels"),
                    ),
                    "The presenter explains the LoRA adapters cell adds adapters so that only a small part of the parameters actually get fine-tuned, which is what keeps the run fast and cheap on a free GPU.",
                ),
            ),
        ),
        video_lesson(
            "Video: Fine-tuning LLM models - a full deep dive",
            "https://www.youtube.com/watch?v=iOdFUJiB0Zc",
            duration="2 hr 37 min",
            body="## Summary\n\nThis lesson is the deep-dive core of the fine-tuning course, mixing theoretical intuition with hands-on Google Colab projects. It opens with quantization, defined as converting weights from a higher memory format to a lower one, for example from 32-bit full precision (FP32) down to FP16 half precision or 8-bit integers. The instructor explains how floating point numbers are stored (sign, exponent, mantissa), why big models like a 70 billion parameter Llama 2 cannot fit in a small GPU or edge device, and how quantization speeds up inference at the cost of some accuracy. He works through the math of symmetric and asymmetric quantization using min-max scaling, a scale factor, and a zero point, calls the squeezing process calibration, and contrasts two modes: post-training quantization (PTQ) versus quantization-aware training (QAT), noting that fine-tuning uses QAT to avoid losing accuracy.\n\nThe lesson then teaches LoRA (Low-Rank Adaptation). Full-parameter fine-tuning must update every weight, which is a hardware and cost problem for models with billions of parameters. LoRA instead freezes the pre-trained weights and tracks the weight changes in a separate matrix that is decomposed into two much smaller matrices whose product reconstructs the update. The rank controls how many trainable parameters this costs, and the research equation is the pre-trained weight W0 plus B times A. Typical ranks are 1, 2, or 8 (Microsoft used 8); higher ranks help the model learn more complex behavior. QLoRA is quantized LoRA, which loads the base model in 4-bit precision (NF4) while keeping the fine-tuned adapter weights in 16-bit.\n\nTwo practical projects follow. First, Llama 2 7B is fine-tuned on a 1000-row sample of the OpenAssistant Guanaco dataset reformatted into the Llama 2 prompt template, using the accelerate, peft, bitsandbytes, transformers, and trl libraries, QLoRA with rank 64 and alpha 16, 4-bit NF4 loading, and the SFTTrainer. The run takes about 25 minutes and produces an adapter model tested with a text-generation pipeline. Second, the Google Gemma 2B model is loaded with a Hugging Face access token, quantized to 4-bit, and fine-tuned with a LoRA rank of 8 on the Abirate English quotes dataset so it can return the author of a quote.\n\nThe lesson also covers the 1-bit LLM research paper (BitNet b1.58), where every weight is ternary (-1, 0, or 1), giving roughly 1.58 bits. Because multiplying by these values is trivial, the matrix multiplication of a Transformer collapses into integer addition, cutting memory, latency, and energy while matching full-precision performance from about 3B parameters, using an absolute-mean quantization function and a BitLinear layer.\n\nFinally the course demonstrates two tooling platforms. Vext is a no-code LLM Ops platform for building RAG and document Q and A pipelines with datasets and smart functions (Google search, Wikipedia, arxiv) exposed through a single API endpoint hit with a Python POST request. Gradient AI is a cloud platform where, with a workspace ID and access token and the python SDK, you create a base model adapter (for example Nous Hermes 2), run inference with complete, and fine-tune on instruction and response samples in a few minutes.\n\n## Main ideas\n\n- **Quantization**: Converting weights from higher precision like FP32 to lower like FP16 or int8 to shrink models for faster inference on limited GPUs and edge devices.\n- **Precision formats**: FP32 is full or single precision, FP16 is half precision, and numbers are stored as sign, exponent, and mantissa bits.\n- **Symmetric vs asymmetric**: Min-max scaling with a scale factor and a zero point maps a floating range into an integer range, and squeezing values is called calibration.\n- **PTQ vs QAT**: Post-training quantization just calibrates a fixed model, while quantization-aware training adds new training data during fine-tuning to preserve accuracy.\n- **LoRA**: Freezes pre-trained weights and tracks the update as two small decomposed matrices B and A, so W0 plus BA needs far fewer trainable parameters set by the rank.\n- **QLoRA**: Quantized LoRA loads the base model in 4-bit NF4 while keeping fine-tuned adapter weights in 16-bit precision.\n- **Fine-tuning stack**: peft, bitsandbytes, transformers, and trl with the SFTTrainer drive supervised fine-tuning of Llama 2 and Google Gemma in Colab.\n- **1-bit LLM**: BitNet b1.58 uses ternary weights -1, 0, and 1 so matrix multiplication becomes addition only, slashing memory, latency, and energy.\n- **Tooling platforms**: Vext offers no-code RAG pipelines via one API and Gradient AI runs cloud fine-tuning through a python SDK on instruction and response samples.\n\n## Mindmap\n\n```mermaid\nmindmap\n  root((Fine Tuning LLMs))\n    Quantization\n      Full and half precision\n      Symmetric and asymmetric\n      Calibration\n      Post training and QAT\n    LoRA\n      Low rank adaptation\n      Matrix decomposition\n      Rank hyperparameter\n      Tracks weight changes\n    QLoRA\n      Quantized LoRA\n      4 bit NF4\n      PEFT adapters\n    Practical projects\n      Llama 2 fine tuning\n      Google Gemma model\n      SFT trainer\n    One bit LLM\n      BitNet ternary weights\n      Addition only compute\n    Tooling\n      Vext no code\n      Gradient AI cloud\n```",
        ),
        quiz_lesson(
            "Quiz: Video: Fine-tuning LLM models - a full deep dive",
            (
                q(
                    "According to the video, what does quantization do to an LLM?",
                    (
                        opt(
                            "It converts the model weights from a higher memory format such as FP32 to a lower one such as FP16 or int8 to reduce size and speed up inference",
                            correct=True,
                        ),
                        opt("It adds more parameters to the model so it can store more knowledge"),
                        opt("It permanently removes entire layers from the neural network"),
                        opt("It converts text prompts into image embeddings"),
                    ),
                    "The instructor defines quantization as conversion from a higher memory format to a lower memory format, for example FP32 to FP16 or int8, which shrinks the model and makes inference faster on limited hardware, with a small loss of accuracy.",
                ),
                q(
                    "How does LoRA reduce the number of trainable parameters during fine-tuning?",
                    (
                        opt(
                            "It tracks the weight changes and decomposes that update matrix into two smaller matrices whose product reconstructs it, controlled by the rank",
                            correct=True,
                        ),
                        opt("It updates every weight in the base model at full precision"),
                        opt(
                            "It deletes the pre-trained weights and trains a brand new model from scratch"
                        ),
                        opt("It converts all weights to ternary values of -1, 0, and 1"),
                    ),
                    "LoRA freezes the pre-trained weights and tracks only the changes, decomposing the update into two smaller matrices B and A (W0 plus BA). The rank sets how many trainable parameters this costs, which is far fewer than full-parameter fine-tuning.",
                ),
                q(
                    "In the 1-bit LLM (BitNet b1.58) section, why does the matrix multiplication become mostly addition?",
                    (
                        opt(
                            "Because every weight is ternary (-1, 0, or 1), so multiplying an input by a weight is trivial and the operation reduces to integer addition",
                            correct=True,
                        ),
                        opt("Because the model no longer uses any weights at all"),
                        opt("Because the inputs are quantized to 32-bit floating point"),
                        opt(
                            "Because BitNet replaces addition with a lookup table of precomputed products"
                        ),
                    ),
                    "BitNet b1.58 stores each weight as one of three values -1, 0, or 1. Multiplying any input by these is trivial (0 zeros it, 1 keeps it, -1 negates it), so the costly floating point multiplications collapse into integer addition, saving memory, latency, and energy.",
                ),
            ),
        ),
        video_lesson(
            "Video: Fine-tuning tiny LLMs for on-device agents",
            "https://www.youtube.com/watch?v=-TiET_K-E_g",
            duration="21 min",
            body="## Summary\n\nThis talk from the Google AI Edge team walks through how to run agents and tiny language models directly on device. It frames the AI Edge stack: MediaPipe, the LiteRT LLM harness (that you ship inside your app with a downloaded model), and the LiteRT runtime (formerly TensorFlow Lite), which runs across CPU, GPU, and NPU. That runtime is already built into Android OS and supports over 2.7 billion devices, and it works well beyond Android too.\n\nThe speaker draws a key distinction between two ways to add intelligence to a mobile app. System GenAI is pre-installed in the operating system, such as Gemini Nano via AI Core, and is highly optimized and free of extra app size. App GenAI instead ships a model with your app through the LiteRT LLM runtime, giving you far more customization and reach at the cost of more work. Tiny LLMs are defined here as models smaller than a billion parameters, small enough to build into an app.\n\nA large part of the talk covers agent skills on device. A simple skill harness puts the system prompt plus short skill descriptions into the model, and a load-skill tool call pulls in the full skill only on demand. Skills can carry small JavaScript snippets that the app renders, which powered the restaurant roulette and map demos. You can hand-write skills or, more powerfully, use skills to write skills through tools like Gemini CLI. The reference app, Google AI Edge Gallery, is open source on Android and lets you try tiny models, third-party models, and community skills.\n\nThe most striking result concerns fine-tuning tiny models. FunctionGemma is a 270 million parameter model based on Gemma 3 that does robust function calling when fine-tuned, running fast even on a legacy Pixel 7 at nearly 2000 tokens per second prefill and 140 decode. On an app-intents task (add calendar, add email), out of the box FunctionGemma scored about 46 percent. By synthetically creating a dataset (using Flash to generate the data) and fine-tuning, accuracy climbed to over 90 percent for eight of the ten functions, with two functions lower.\n\nThe speaker closes with Eloquent, a production transcription app built from tiny LLMs: a Gemma 3 based ASR engine chained with a text polishing engine, each only a few hundred million parameters. Together they deliver offline transcription with a personal dictionary and remove filler words like ums and ahs, proving these fine-tuned tiny models work in production.\n\n## Main ideas\n\n- **Tiny LLMs**: Models smaller than a billion parameters, small enough to build directly into your app for custom on-device tasks.\n- **AI Edge stack**: MediaPipe, the LiteRT LLM harness, and the LiteRT runtime (formerly TensorFlow Lite) run models on CPU, GPU, or NPU across 2.7 billion-plus devices.\n- **System GenAI vs App GenAI**: System GenAI (Gemini Nano via AI Core) is preloaded and free of app size, while App GenAI ships a model in your app for more customization and reach with more work.\n- **On-device agent skills**: A simple harness feeds short skill descriptions to the model and loads full skills on demand via a load-skill tool call, with optional JavaScript for in-app UI.\n- **Skills writing skills**: Tools like Gemini CLI can author reliable skills, and the open-source Google AI Edge Gallery app lets you load custom and community skills from a URL.\n- **FunctionGemma**: A 270 million parameter Gemma 3 based model that does robust function calling when fine-tuned, running fast even on a Pixel 7.\n- **Fine-tuning with synthetic data**: The workflow uses Flash to synthetically generate a dataset instead of relying on a system prompt, which is needed as models shrink to a narrow focused task.\n- **46 to 90 percent**: Fine-tuning lifted the app-intents success rate from about 46 percent out of the box to over 90 percent for eight of ten functions.\n- **Production proof**: Eloquent chains a Gemma 3 ASR engine and a text polishing engine, each a few hundred million parameters, for offline transcription with a personal dictionary.\n\n## Mindmap\n\n```mermaid\nmindmap\n  root((On-Device Tiny LLMs))\n    AI Edge Stack\n      MediaPipe\n      LiteRT runtime\n      CPU GPU NPU\n    Model Choices\n      System GenAI\n      App GenAI\n      Gemini Nano\n    Agent Skills\n      Load skill tool\n      JavaScript UI\n      AI Edge Gallery\n    Fine-Tuning TLMs\n      Synthetic data\n      FunctionGemma 270M\n      46 to 90 percent\n    Production Apps\n      Eloquent transcription\n      Personal dictionary\n```",
        ),
        quiz_lesson(
            "Quiz: Video: Fine-tuning tiny LLMs for on-device agents",
            (
                q(
                    "What accuracy improvement did the team report after fine-tuning FunctionGemma on the app-intents task?",
                    (
                        opt(
                            "From about 46 percent out of the box to over 90 percent for eight of the ten functions",
                            correct=True,
                        ),
                        opt("From 90 percent down to 46 percent after quantization"),
                        opt("From 46 percent to exactly 100 percent on all ten functions"),
                        opt("No measurable change, since fine-tuning tiny models does not help"),
                    ),
                    "Out of the box FunctionGemma scored about 46 percent on the app-intents functions. After synthetically creating a dataset and fine-tuning, accuracy rose to over 90 percent for eight of the ten functions, with two functions remaining lower.",
                ),
                q(
                    "How is FunctionGemma described in the talk?",
                    (
                        opt(
                            "A 270 million parameter model based on Gemma 3 that does robust function calling when fine-tuned",
                            correct=True,
                        ),
                        opt("A 7 billion parameter cloud-only model for image generation"),
                        opt("A transcription runtime that replaces MediaPipe"),
                        opt("A closed-source model that only runs on the newest Pixel hardware"),
                    ),
                    "FunctionGemma is a 270 million parameter model based on Gemma 3, published with the DeepMind team, that provides robust function calling once fine-tuned and runs fast even on a legacy Pixel 7.",
                ),
                q(
                    "According to the talk, how does the on-device skill harness keep the prompt manageable?",
                    (
                        opt(
                            "It puts short skill descriptions in the prompt and loads the full skill only on demand via a load-skill tool call",
                            correct=True,
                        ),
                        opt(
                            "It loads every function and detail of all skills into the prompt at startup"
                        ),
                        opt("It sends all skills to a cloud server to be filtered before use"),
                        opt("It disables skills entirely because tiny models cannot use tools"),
                    ),
                    "The harness places the system prompt plus short skill descriptions into the model so it knows which skills exist, then uses a load-skill tool call to pull in the full skill details only when needed.",
                ),
            ),
        ),
        video_lesson(
            "Video: Steering LLM behavior without fine-tuning",
            "https://www.youtube.com/watch?v=F2jd5WuT-zg",
            duration="18 min",
            body="## Summary\n\nThis video presents a third way to change how a large language model behaves, sitting alongside prompt engineering and fine-tuning. Prompt engineering sets behavior through the system prompt, while fine-tuning changes the weights but requires enough demonstration data and enough compute. The alternative shown here is called steering: you intervene on the model's internal activations at inference time, without rewiring anything and without changing any weights. The presenter compares this to neurostimulation, where neuroscientists stimulate specific neurons or brain regions with electrodes to trigger or inhibit actions, without modifying the brain itself. As a demonstration, a Llama 3.1 8B model is steered to become obsessed with the Eiffel Tower, to the point it claims to be a large metal structure rather than a large language model.\n\nTo understand steering, the video recaps how an LLM works internally. Autoregressive transformer models generate one token at a time through a stack of layers, each with an attention block and a feed forward block. Between layers, a hidden state vector is passed along; this vector lives in a high dimensional activation space of a few thousand dimensions and represents the model's internal state. The key concept is the linear representation phenomenon: LLMs tend to represent interpretable concepts as vectors in the activation space, and because vectors can be added, you can combine or reinforce concepts. The classic Word2Vec King minus Man plus Woman example illustrates this arithmetic, and the video notes that for a concept the direction of the vector matters more than its length.\n\nThe video adds important nuances. Concepts are encoded as distributed patterns across neurons, a property called superposition, which lets models represent more concepts than they have dimensions. Different layers play different roles: early layers activate when a concept has just appeared in the input, late layers activate when the model is about to output that token, and middle layers are where abstract reasoning happens. Middle layers are therefore the most useful place to steer when you want to influence the model without forcing exact wording.\n\nSteering itself is simple in practice. Given a normalized concept vector V and the activation X at the output of a chosen layer, you add V scaled by a coefficient to X. In Hugging Face Transformers this is done with a hook, a function attached to the model that fires during the forward pass and adds the scaled vector at, for example, layer 15 of the 32-layer Llama model. The coefficient controls the strength: at 4.0 the model drifts toward food and bakeries, at 8.0 it talks about wine and travel and starts pretending to be the Eiffel Tower. Push the coefficient too high and the model derails into gibberish, so choosing a good coefficient matters.\n\nFinally, the video explains where steering vectors come from. Contrastive activation gathers positive and negative example prompts and subtracts the average negative activation from the average positive activation; this has sometimes outperformed prompt engineering and supervised fine-tuning. Sparse autoencoders are an unsupervised alternative that produce a large library of interpretable concept vectors, though the vectors usually lack labels, which is where the Neuronpedia website helps you browse and find features. Steering needs no fine-tuning, lets you control intensity and hold it across the whole generation, but it can be hard to find a stable sweet spot and it only works for concepts the model already represents; it will not teach the model new knowledge.\n\n## Main ideas\n\n- **Steering**: a third way to change LLM behavior that intervenes on activations at inference time without altering weights.\n- **Neurostimulation analogy**: like stimulating brain neurons with electrodes, steering nudges chosen neurons without modifying the model.\n- **Activation space**: between layers the model passes a high dimensional hidden state vector representing its internal thoughts.\n- **Linear representation**: LLMs tend to encode concepts as vectors you can add, so summing a car vector and a red vector gives a red car.\n- **Direction over length**: a concept vector's direction sets which concept it is, while its length sets only how strongly it is expressed.\n- **Superposition**: concepts are distributed across neurons, letting the model hold more concepts than it has dimensions.\n- **Middle layers**: early layers echo input tokens and late layers predict output, but middle layers hold abstract reasoning and are best to steer.\n- **Hooks and coefficient**: a forward-pass hook adds the scaled vector, and the coefficient controls strength before the model derails into gibberish.\n- **Finding vectors**: contrastive activation and sparse autoencoders produce steering vectors, with Neuronpedia helping you locate labeled features.\n\n## Mindmap\n\n```mermaid\nmindmap\n  root((Steering LLMs))\n    Motivation\n      No fine-tuning\n      Inference time only\n      Neurostimulation analogy\n    Internals\n      Transformer layers\n      Hidden state vector\n      Activation space\n    Linear representation\n      Concepts as vectors\n      Add vectors\n      Direction over length\n      Superposition\n    Layers matter\n      Early echo input\n      Late predict output\n      Middle abstract reasoning\n    How to steer\n      Add scaled vector\n      Forward pass hook\n      Steering coefficient\n    Finding vectors\n      Contrastive activation\n      Sparse autoencoders\n      Neuronpedia\n    Limits\n      Hard sweet spot\n      No new knowledge\n```",
        ),
        quiz_lesson(
            "Quiz: Video: Steering LLM behavior without fine-tuning",
            (
                q(
                    "According to the video, what fundamentally distinguishes steering from fine-tuning?",
                    (
                        opt(
                            "Steering intervenes on the model's activations at inference time without changing any weights",
                            correct=True,
                        ),
                        opt(
                            "Steering updates the model's weights using a small number of gradient steps"
                        ),
                        opt(
                            "Steering rewrites the system prompt automatically before each generation"
                        ),
                        opt(
                            "Steering retrains only the final linear head while freezing all other layers"
                        ),
                    ),
                    "The video stresses that steering does not modify weights or rewire the model; it adds a concept vector to the activations during the forward pass at inference time, unlike fine-tuning which needs demonstration data and compute to change weights.",
                ),
                q(
                    "Why does the presenter recommend steering concept vectors located in the middle layers of the model?",
                    (
                        opt(
                            "Middle layers are where the model tends to represent abstract concepts and reason on them, so it is influenced without merely reproducing exact words",
                            correct=True,
                        ),
                        opt(
                            "Middle layers contain the embedding layer that maps every token to a vector"
                        ),
                        opt(
                            "Middle layers require the smallest steering coefficient to avoid gibberish"
                        ),
                        opt(
                            "Middle layers are the only layers where hooks can be registered in Transformers"
                        ),
                    ),
                    "The video explains that early layers activate when a concept has just appeared in the input and late layers activate when the model is about to output a token, while middle layers hold abstract reasoning, making them the best place to influence behavior without forcing exact wording.",
                ),
                q(
                    "What does the video state as a key limitation of steering?",
                    (
                        opt(
                            "It works best for concepts the model already represents and will not teach the model new knowledge",
                            correct=True,
                        ),
                        opt("It permanently corrupts the model weights after a few generations"),
                        opt("It can only be applied to closed-source models, not open-source ones"),
                        opt("It requires more demonstration data than supervised fine-tuning"),
                    ),
                    "The video notes drawbacks including the difficulty of finding a stable sweet spot for the coefficient and, importantly, that steering works only for concepts the model has already learned to represent and cannot add new knowledge.",
                ),
            ),
        ),
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Which best describes fine-tuning?",
                    (
                        opt(
                            "Continuing training on curated data to adapt a pretrained model's weights",
                            correct=True,
                        ),
                        opt("Writing a longer prompt"),
                        opt("Adding documents at inference time"),
                    ),
                ),
                q(
                    "You want a small model to consistently output a specific JSON format. Best tool?",
                    (
                        opt("Fine-tuning", correct=True),
                        opt("A bigger system prompt only, guaranteed to work"),
                        opt("Deleting the tokenizer"),
                    ),
                    "Consistent form and behavior is exactly what fine-tuning is for.",
                ),
                q(
                    "What is the standard PyTorch training-step order?",
                    (
                        opt("forward, loss, zero_grad, backward, step", correct=True),
                        opt("step, backward, loss, forward"),
                        opt("loss, step, forward, backward"),
                    ),
                ),
                q(
                    "LoRA reduces cost by:",
                    (
                        opt("Freezing W and training two small low-rank matrices", correct=True),
                        opt("Training a full copy of every layer"),
                        opt("Removing all attention layers"),
                    ),
                ),
                q(
                    "QLoRA additionally:",
                    (
                        opt("Loads the frozen base in 4-bit to save memory", correct=True),
                        opt("Requires 8 GPUs minimum"),
                        opt("Needs no adapters"),
                    ),
                ),
                q(
                    "The single objective behind LLM pretraining is:",
                    (
                        opt("Next-token prediction", correct=True),
                        opt("Image classification"),
                        opt("Alphabetical sorting"),
                    ),
                ),
                q(
                    "For instruction-tuning data, the strongest lever is usually:",
                    (
                        opt(
                            "Clean, consistent, high-quality examples in the model's chat template",
                            correct=True,
                        ),
                        opt("Sheer volume of noisy examples"),
                        opt("Never using a validation split"),
                    ),
                ),
                q(
                    "Training loss keeps dropping while validation loss climbs. You should:",
                    (
                        opt("Stop early or add data - it is overfitting", correct=True),
                        opt("Train much longer, it is going well"),
                        opt("Raise the learning rate a lot"),
                    ),
                ),
                q(
                    "To ship a LoRA fine-tune as one standalone model you:",
                    (
                        opt("Merge the adapter into the base weights", correct=True),
                        opt("Delete the base model"),
                        opt("Retrain from scratch"),
                    ),
                ),
                q(
                    "When is changing behavior WITHOUT fine-tuning (prompting or steering) the right call?",
                    (
                        opt(
                            "When prompting or retrieval already gets the behavior you need",
                            correct=True,
                        ),
                        opt("Always, fine-tuning never works"),
                        opt("Never, fine-tuning is always required"),
                    ),
                    "Try the cheap tools first; fine-tune when they are not enough.",
                ),
            ),
        ),
    ),
)

FINE_TUNING_LLMS_COURSES: tuple[SeedCourse, ...] = (_FINE_TUNING_LLMS,)
