"""Academy seed content - GPU Programming with CUDA and OpenCL.

A hands-on introduction to general-purpose GPU programming: why GPUs are
throughput machines, the thread/block/grid (work-item/work-group/NDRange)
execution model, a first vector-add kernel in both CUDA and OpenCL, the
GPU memory hierarchy and coalescing, a worked tiled matrix-multiply with
shared memory, optimization and the classic pitfalls, and how to choose
between CUDA and OpenCL. Every lesson is a direct explanation with
runnable-style code examples and a mermaid diagram, followed by a
checkpoint quiz; the course closes with a comprehensive final quiz.
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


_GPU_PROGRAMMING = SeedCourse(
    slug="gpu-programming-cuda-opencl",
    title="GPU Programming with CUDA and OpenCL",
    description=(
        "General-purpose GPU programming from zero: why GPUs are throughput "
        "machines, the thread/block/grid execution model, first kernels in "
        "both CUDA and OpenCL, the memory hierarchy and coalescing, a tiled "
        "matrix-multiply with shared memory, optimization and pitfalls, and "
        "choosing between CUDA and OpenCL - with runnable examples and a "
        "diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# GPU Programming with CUDA and OpenCL

A modern GPU runs thousands of threads at once. Used well, it turns
hours of computation into seconds - which is why GPUs power deep
learning, scientific simulation, graphics, and finance. This course
teaches you to write that code, in both of the dominant APIs.

If you can read basic C, you can follow along. The approach is **small
and concrete**: every lesson explains one idea directly, shows it in a
short kernel you could compile, and draws the idea as a diagram. After
each lesson there is a short quiz; at the end, a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **Why GPUs** - throughput vs latency, and the SIMT model
2. **The execution model** - threads, blocks/work-groups, grids, warps
3. **A first CUDA kernel** - vector add, launch config, host/device memory
4. **A first OpenCL kernel** - the same program, portable across vendors
5. **The memory hierarchy** - global, shared, registers, and coalescing
6. **Tiled matrix multiply** - the classic shared-memory optimization
7. **Optimization and pitfalls** - occupancy, divergence, transfers
8. **CUDA vs OpenCL** - how to choose

**CUDA** (NVIDIA) and **OpenCL** (open, cross-vendor) share the same
mental model; once you know one, the other is mostly new spelling. To
run CUDA you need an NVIDIA GPU + the CUDA Toolkit (`nvcc`); OpenCL runs
on NVIDIA, AMD, Intel GPUs and CPUs. Every example here is small enough
to reason about without hardware.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What kind of workloads are GPUs designed to accelerate?",
                    (
                        opt("Single-threaded tasks with unpredictable branching"),
                        opt(
                            "Massively parallel work - the same operation over huge "
                            "amounts of data (high throughput)",
                            correct=True,
                        ),
                        opt("Disk and network input/output"),
                        opt("Tasks that must finish one item as fast as possible"),
                    ),
                    "GPUs trade per-item latency for throughput: thousands of threads "
                    "doing the same work over large data.",
                ),
                q(
                    "How do CUDA and OpenCL relate in this course?",
                    (
                        opt("They are unrelated and share no concepts"),
                        opt("OpenCL replaced CUDA years ago"),
                        opt(
                            "They share the same execution model - learn one and the "
                            "other is mostly new terminology",
                            correct=True,
                        ),
                        opt("CUDA runs only on CPUs; OpenCL only on GPUs"),
                    ),
                    "Threads/blocks/grids in CUDA map directly to "
                    "work-items/work-groups/NDRange in OpenCL.",
                ),
            ),
        ),
        # -- 1. Why GPUs -----------------------------------------------
        _t(
            "Why GPUs? Throughput over latency",
            "9 min",
            """# Why GPUs? Throughput over latency

A CPU is a **latency machine**: a few powerful cores, huge caches, branch
predictors and out-of-order execution - all to finish *one* task as fast
as possible. A GPU is a **throughput machine**: thousands of simple cores
that finish one item slowly but a million items quickly, by running them
in parallel.

The trade is deliberate. A GPU spends its transistors on **arithmetic
units** instead of caches and control logic, and it hides memory latency
not with big caches but by **oversubscription**: keep so many threads in
flight that whenever some are waiting on memory, others are ready to run.

The programming model is **SIMT** - Single Instruction, Multiple Threads.
You write **one** function (a *kernel*) describing what *one* thread does;
the hardware runs it across thousands of threads, each on its own slice of
the data. Threads execute in lockstep groups (a **warp** of 32 on NVIDIA,
a **wavefront** on AMD), so the code you write once is applied in parallel.

```cpp
// The CPU way: one thread walks the whole array, one element at a time.
for (int i = 0; i < n; i++)
    c[i] = a[i] + b[i];

// The GPU way: launch n threads; each does ONE element. All at once.
// (kernel body) int i = global_thread_index();  c[i] = a[i] + b[i];
```

When does the GPU win? When the work is **data-parallel** (same
operation over many elements), **arithmetically heavy** relative to the
data moved, and big enough to amortize the cost of shipping data across
the PCIe bus. A tiny array is faster on the CPU - you would spend more
time copying than computing.

```mermaid
graph TD
    CPU["CPU few strong cores"] --> LAT["Low latency per task"]
    GPU["GPU thousands of cores"] --> THR["High throughput many tasks"]
    THR --> SIMT["SIMT one kernel many threads"]
    SIMT --> WARP["Threads run in warps"]
    THR --> DP["Best for data parallel work"]
```

The one thing to remember: describe the work for a single thread; let the
GPU replicate it thousands of times.
""",
        ),
        quiz_lesson(
            "Quiz: Why GPUs? Throughput over latency",
            (
                q(
                    "What is the core design difference between a CPU and a GPU?",
                    (
                        opt("The CPU has more cores than the GPU"),
                        opt(
                            "The CPU optimizes latency (finish one task fast); the GPU "
                            "optimizes throughput (finish many tasks in parallel)",
                            correct=True,
                        ),
                        opt("The GPU runs only integer math"),
                        opt("The CPU cannot run parallel code at all"),
                    ),
                    "Few strong cores + big caches (CPU) vs thousands of simple cores "
                    "(GPU) - a latency-vs-throughput trade.",
                ),
                q(
                    "What does SIMT (Single Instruction, Multiple Threads) mean for how "
                    "you write GPU code?",
                    (
                        opt("You write a separate function for every thread"),
                        opt("You must manually assign work to each core"),
                        opt(
                            "You write one kernel describing one thread's work; the "
                            "hardware runs it across thousands of threads",
                            correct=True,
                        ),
                        opt("You write sequential loops that the compiler parallelizes"),
                    ),
                    "One kernel, many threads - each thread handles its own slice of the data.",
                ),
                q(
                    "How does a GPU hide the latency of slow memory accesses?",
                    (
                        opt("With very large caches like a CPU"),
                        opt("By running at a much higher clock speed"),
                        opt(
                            "By keeping many threads in flight so some are ready to run "
                            "while others wait on memory",
                            correct=True,
                        ),
                        opt("By prefetching the entire dataset into registers"),
                    ),
                    "Oversubscription: thousands of resident threads mean the scheduler "
                    "always has ready work to hide memory stalls.",
                ),
            ),
        ),
        # -- 2. Execution model ----------------------------------------
        _t(
            "The execution model - threads, blocks, grids",
            "10 min",
            """# The execution model - threads, blocks, grids

GPU work is organized as a **hierarchy**. You launch a **grid** of
**blocks**, and each block contains many **threads**. (OpenCL calls the
same three levels an **NDRange** of **work-groups** of **work-items**.)
The names differ; the structure is identical.

- A **thread** (work-item) is one instance of your kernel - it computes
  its own index and works on its own data.
- A **block** (work-group) is a group of threads that run on the same
  compute unit, can **cooperate** through fast shared memory, and can
  **synchronize** with a barrier.
- A **grid** (NDRange) is all the blocks for one kernel launch.

Each thread finds its unique global index from its coordinates. In CUDA:

```cpp
// 1D launch: which element am I responsible for?
int i = blockIdx.x * blockDim.x + threadIdx.x;
//      (which block)  (block size)  (which thread in block)
```

Because the total thread count is a multiple of the block size, it is
usually **larger than the data**. Every kernel therefore starts with a
**bounds check** so the extra threads do nothing:

```cpp
__global__ void add(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)              // guard: the last block may overhang
        c[i] = a[i] + b[i];
}
```

You choose the block size (commonly 128 or 256 threads) and compute the
grid size to cover the data: `blocks = (n + threads - 1) / threads`
(ceiling division). Blocks are scheduled independently and in any order -
so **blocks cannot depend on each other**, which is exactly what lets the
GPU scale from a small chip to a huge one with no code change.

Threads within a block run in **warps** of 32. Keeping the block size a
multiple of 32 avoids wasting lanes.

```mermaid
graph TD
    GRID["Grid all blocks"] --> B0["Block 0"]
    GRID --> B1["Block 1"]
    GRID --> BN["Block N"]
    B0 --> T0["Thread 0"]
    B0 --> T1["Thread 1"]
    B0 --> TM["Thread M"]
    B0 --> SM["Shared memory and barrier"]
```

Remember the shape: grid of blocks of threads. Threads in a block
cooperate; blocks are independent.
""",
        ),
        quiz_lesson(
            "Quiz: The execution model - threads, blocks, grids",
            (
                q(
                    "What is the correct hierarchy of a GPU kernel launch (CUDA terms)?",
                    (
                        opt("A thread of blocks of grids"),
                        opt("A grid of blocks of threads", correct=True),
                        opt("A warp of grids of blocks"),
                        opt("A block of grids of threads"),
                    ),
                    "You launch a grid; it contains blocks; each block contains "
                    "threads. OpenCL: NDRange of work-groups of work-items.",
                ),
                q(
                    "Why does almost every kernel start with a bounds check like `if (i < n)`?",
                    (
                        opt("To skip elements that are zero"),
                        opt(
                            "The total thread count is rounded up to a multiple of the "
                            "block size, so it usually exceeds n - extra threads must do "
                            "nothing",
                            correct=True,
                        ),
                        opt("To make the kernel run faster"),
                        opt("Because CUDA requires an if statement in every kernel"),
                    ),
                    "Ceiling-division grid sizing overshoots the data; the guard stops "
                    "the overhang threads from writing out of bounds.",
                ),
                q(
                    "Why must blocks be independent of one another?",
                    (
                        opt("Because blocks share all their registers"),
                        opt("Because the compiler merges them into one block"),
                        opt(
                            "Blocks are scheduled in any order across compute units, so "
                            "one cannot rely on another - which is what lets the same "
                            "code scale across GPU sizes",
                            correct=True,
                        ),
                        opt("They are not - blocks always run in order"),
                    ),
                    "Independent blocks are the scalability guarantee: the hardware runs "
                    "as many at once as it can fit.",
                ),
            ),
        ),
        # -- 3. First CUDA kernel --------------------------------------
        _t(
            "Your first CUDA kernel - vector add",
            "11 min",
            """# Your first CUDA kernel - vector add

Here is the full "hello world" of GPU computing: add two vectors. It
shows the whole lifecycle - allocate device memory, copy input up, launch
the kernel, copy the result back, free.

```cpp
#include <cuda_runtime.h>

// The KERNEL: runs on the GPU. __global__ = callable from host, runs on device.
__global__ void vecAdd(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
        c[i] = a[i] + b[i];
}

int main() {
    int n = 1 << 20;                 // ~1M elements
    size_t bytes = n * sizeof(float);

    float *a, *b, *c;                // host pointers (assume filled)
    float *dA, *dB, *dC;             // device pointers

    cudaMalloc(&dA, bytes);          // 1. allocate on the GPU
    cudaMalloc(&dB, bytes);
    cudaMalloc(&dC, bytes);

    cudaMemcpy(dA, a, bytes, cudaMemcpyHostToDevice);   // 2. copy inputs up
    cudaMemcpy(dB, b, bytes, cudaMemcpyHostToDevice);

    int threads = 256;                          // 3. launch config
    int blocks  = (n + threads - 1) / threads;  //    ceil(n / threads)
    vecAdd<<<blocks, threads>>>(dA, dB, dC, n);  //   <<<grid, block>>>

    cudaMemcpy(c, dC, bytes, cudaMemcpyDeviceToHost);   // 4. copy result back

    cudaFree(dA); cudaFree(dB); cudaFree(dC);           // 5. free
}
```

The pieces that are new:

- **`__global__`** marks a kernel - launched from the CPU (host), executed
  on the GPU (device). `__device__` functions run on the GPU but are
  called only from other GPU code.
- **`cudaMalloc` / `cudaMemcpy` / `cudaFree`** manage a **separate address
  space**. Host and device memory are distinct; you move data explicitly.
  (Unified Memory can automate this, but explicit copies make the cost
  visible - and the transfer is often the bottleneck.)
- **`<<<blocks, threads>>>`** is the launch. The triple-angle-bracket
  syntax sets the grid and block dimensions.
- **Kernel launches are asynchronous.** Control returns to the CPU
  immediately; the copy-back (or `cudaDeviceSynchronize()`) waits for the
  GPU to finish.

Always check errors in real code (`cudaGetLastError()` after the launch,
and the return of each API call) - a bad launch fails silently otherwise.

```mermaid
graph LR
    H1["Host allocate and fill"] --> UP["cudaMemcpy to device"]
    UP --> K["Launch kernel grid of blocks"]
    K --> DOWN["cudaMemcpy back to host"]
    DOWN --> F["cudaFree device memory"]
```

That five-step dance - allocate, copy up, launch, copy back, free - is
every CUDA program in miniature.
""",
        ),
        quiz_lesson(
            "Quiz: Your first CUDA kernel - vector add",
            (
                q(
                    "What does the `__global__` qualifier mark in CUDA?",
                    (
                        opt("A global variable shared by all threads"),
                        opt(
                            "A kernel: a function launched from the host (CPU) and "
                            "executed on the device (GPU)",
                            correct=True,
                        ),
                        opt("A function that runs on the CPU only"),
                        opt("A constant stored in global memory"),
                    ),
                    "__global__ = kernel (host-launched, device-run). __device__ = "
                    "device-only helper called from other GPU code.",
                ),
                q(
                    "Why are `cudaMemcpy` calls needed around the kernel launch?",
                    (
                        opt("To convert float to double"),
                        opt("To synchronize the CPU threads"),
                        opt(
                            "Host and device have separate address spaces, so input "
                            "data must be copied to the GPU and results copied back",
                            correct=True,
                        ),
                        opt("They are optional and only for logging"),
                    ),
                    "The GPU cannot read host RAM directly (without Unified Memory); "
                    "data crosses the bus explicitly.",
                ),
                q(
                    "What does `<<<blocks, threads>>>` specify?",
                    (
                        opt("The number of GPUs to use"),
                        opt("The input and output array sizes"),
                        opt(
                            "The grid (number of blocks) and block (threads per block) dimensions",
                            correct=True,
                        ),
                        opt("The amount of shared memory in bytes"),
                    ),
                    "The execution configuration: how many blocks, and how many threads "
                    "each block has.",
                ),
            ),
        ),
        # -- 4. First OpenCL kernel ------------------------------------
        _t(
            "Your first OpenCL kernel - the portable twin",
            "11 min",
            """# Your first OpenCL kernel - the portable twin

OpenCL runs the same vector add on NVIDIA, AMD, Intel - GPUs and CPUs
alike. The kernel is nearly identical to CUDA; the host code is more
verbose because OpenCL discovers the hardware at runtime instead of
compiling for one vendor.

The **kernel** (a string, compiled at runtime) - compare it to the CUDA
version:

```c
__kernel void vecAdd(__global const float* a,
                     __global const float* b,
                     __global float* c, int n) {
    int i = get_global_id(0);        // CUDA: blockIdx*blockDim + threadIdx
    if (i < n)
        c[i] = a[i] + b[i];
}
```

`__kernel` is CUDA's `__global__`; `__global` marks pointers into global
memory; `get_global_id(0)` is the flattened global index - OpenCL does the
`block * size + thread` arithmetic for you.

The **host** side follows a fixed setup ritual, done once:

```c
// 1. pick a platform + device, make a context and a command queue
clGetPlatformIDs(1, &platform, NULL);
clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);
cl_context ctx = clCreateContext(NULL, 1, &device, NULL, NULL, NULL);
cl_command_queue q = clCreateCommandQueue(ctx, device, 0, NULL);

// 2. build the program from the kernel source string
cl_program prog = clCreateProgramWithSource(ctx, 1, &src, NULL, NULL);
clBuildProgram(prog, 1, &device, NULL, NULL, NULL);
cl_kernel k = clCreateKernel(prog, "vecAdd", NULL);

// 3. buffers (device memory) + copy inputs
cl_mem dA = clCreateBuffer(ctx, CL_MEM_READ_ONLY, bytes, NULL, NULL);
clEnqueueWriteBuffer(q, dA, CL_TRUE, 0, bytes, a, 0, NULL, NULL);
// ... dB likewise, dC as CL_MEM_WRITE_ONLY ...

// 4. set args, then enqueue with a global (and optional local) size
clSetKernelArg(k, 0, sizeof(cl_mem), &dA);  // ... args 1..3 ...
size_t global = ((n + 255) / 256) * 256, local = 256;
clEnqueueNDRangeKernel(q, k, 1, NULL, &global, &local, 0, NULL, NULL);

// 5. read the result back
clEnqueueReadBuffer(q, dC, CL_TRUE, 0, bytes, c, 0, NULL, NULL);
```

The mapping to CUDA is direct: **context** ~ the device session,
**command queue** ~ the CUDA stream, **buffer** ~ `cudaMalloc`,
**EnqueueWriteBuffer/ReadBuffer** ~ `cudaMemcpy`, **EnqueueNDRangeKernel** ~
the `<<<...>>>` launch. Note OpenCL takes the **global size** (total
work-items) and **local size** (work-group size), where CUDA takes the
block count and block size - same information, expressed differently.

The cost of portability: more boilerplate and runtime kernel compilation.
The payoff: one code base across every vendor.

```mermaid
graph TD
    P["Platform and device"] --> C["Context and command queue"]
    C --> PR["Build program from source"]
    PR --> KE["Create kernel"]
    KE --> BUF["Buffers write inputs"]
    BUF --> ND["Enqueue NDRange kernel"]
    ND --> RD["Read buffer result"]
```

Same kernel, same model - OpenCL just asks you to name the hardware at
runtime instead of at compile time.
""",
        ),
        quiz_lesson(
            "Quiz: Your first OpenCL kernel - the portable twin",
            (
                q(
                    "What is OpenCL's main advantage over CUDA?",
                    (
                        opt("It is always faster"),
                        opt(
                            "Portability - the same code runs on NVIDIA, AMD and Intel "
                            "GPUs and CPUs",
                            correct=True,
                        ),
                        opt("It needs no host code"),
                        opt("It compiles kernels ahead of time only"),
                    ),
                    "OpenCL is an open, cross-vendor standard; CUDA is NVIDIA-only.",
                ),
                q(
                    "In an OpenCL kernel, what does `get_global_id(0)` return?",
                    (
                        opt("The number of work-groups"),
                        opt("The device id"),
                        opt(
                            "The work-item's flattened global index - the equivalent of "
                            "CUDA's blockIdx*blockDim + threadIdx",
                            correct=True,
                        ),
                        opt("The size of the global memory"),
                    ),
                    "OpenCL computes the global index for you; the argument selects the "
                    "dimension (0 for 1D).",
                ),
                q(
                    "Which OpenCL concept corresponds to a CUDA kernel launch `<<<...>>>`?",
                    (
                        opt("clCreateContext"),
                        opt("clCreateBuffer"),
                        opt("clEnqueueNDRangeKernel", correct=True),
                        opt("clBuildProgram"),
                    ),
                    "EnqueueNDRangeKernel submits the kernel with a global and local "
                    "size - the OpenCL equivalent of the triple-angle-bracket launch.",
                ),
            ),
        ),
        # -- 5. Memory hierarchy ---------------------------------------
        _t(
            "The memory hierarchy and coalescing",
            "11 min",
            """# The memory hierarchy and coalescing

Getting a kernel *correct* is easy; getting it *fast* is almost always
about **memory**. The GPU has a hierarchy, fastest and smallest first:

- **Registers** - per-thread, fastest. Your local variables live here.
- **Shared memory** (OpenCL: **local memory**) - per-block, on-chip, ~100x
  faster than global. Threads in a block use it to cooperate and to cache
  data they will reuse. A few tens of KB per block.
- **Global memory** - the big GPU DRAM (gigabytes), visible to all
  threads, but hundreds of cycles of latency. Every `cudaMemcpy` lands
  here.
- **Constant / texture memory** - small, cached, read-only paths for data
  all threads read.

The single most important global-memory rule is **coalescing**: when the
32 threads of a warp access global memory, the hardware combines their
requests into as few wide transactions as possible - *if* the addresses
are contiguous. Adjacent threads should touch adjacent addresses.

```cpp
int i = blockIdx.x * blockDim.x + threadIdx.x;

c[i] = a[i];            // COALESCED: thread i reads element i (contiguous)

c[i] = a[i * stride];   // STRIDED: threads jump apart -> many transactions,
                        // a fraction of the bandwidth
```

A strided or random access pattern can be 10x slower than a coalesced one
running the exact same arithmetic - the compute is idle, starved for data.

**Shared memory** is the programmable lever. Declared with `__shared__`
(CUDA) or `__local` (OpenCL), it lets a block load a chunk of global data
**once**, cooperatively, then reuse it many times from on-chip memory. Its
use requires a barrier - `__syncthreads()` (CUDA) / `barrier(...)`
(OpenCL) - so every thread finishes loading before any thread reads what
its neighbors loaded. The next lesson puts this to work.

```mermaid
graph TD
    REG["Registers per thread fastest"] --> SH["Shared memory per block"]
    SH --> GL["Global memory all threads slow"]
    GL --> CO["Coalesced access is key"]
    GL --> CN["Constant memory read only cached"]
```

Remember: registers and shared memory are fast and small; global is large
and slow. Speed comes from touching global memory contiguously and reusing
data in shared memory.
""",
        ),
        quiz_lesson(
            "Quiz: The memory hierarchy and coalescing",
            (
                q(
                    "How does shared memory (CUDA) / local memory (OpenCL) compare to "
                    "global memory?",
                    (
                        opt("It is larger but slower"),
                        opt(
                            "It is on-chip, per-block, and roughly 100x faster - but "
                            "small (tens of KB)",
                            correct=True,
                        ),
                        opt("It is identical to global memory"),
                        opt("It is per-thread and cannot be shared"),
                    ),
                    "Shared/local memory is the fast, cooperative scratchpad a block "
                    "uses to cache and reuse data.",
                ),
                q(
                    "What is memory coalescing?",
                    (
                        opt("Merging two kernels into one"),
                        opt("Compressing data before transfer"),
                        opt(
                            "When the threads of a warp access contiguous global "
                            "addresses, the hardware combines them into few wide "
                            "transactions",
                            correct=True,
                        ),
                        opt("Caching the whole array in registers"),
                    ),
                    "Adjacent threads touching adjacent addresses = coalesced = full "
                    "bandwidth. Strided access wastes it.",
                ),
                q(
                    "Why does cooperative use of shared memory require a barrier "
                    "(__syncthreads / barrier)?",
                    (
                        opt("To free the shared memory"),
                        opt("To coalesce the global reads"),
                        opt(
                            "So every thread finishes writing its part of the shared "
                            "tile before any thread reads what its neighbors wrote",
                            correct=True,
                        ),
                        opt("To copy shared memory back to global"),
                    ),
                    "Without the barrier a thread could read a shared slot before "
                    "another thread has filled it - a race.",
                ),
            ),
        ),
        # -- 6. Tiled matmul -------------------------------------------
        _t(
            "Worked example - tiled matrix multiply",
            "13 min",
            """# Worked example - tiled matrix multiply

Matrix multiply is the canonical GPU optimization. A naive kernel is
correct but **memory-bound**: to compute one output element `C[row][col]`
it reads a full row of A and a full column of B from slow global memory,
and every thread re-reads the same rows and columns.

```cpp
// Naive: each thread reads 2*N values from GLOBAL memory. Bandwidth-starved.
__global__ void matmulNaive(const float* A, const float* B, float* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < N && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < N; k++)
            sum += A[row * N + k] * B[k * N + col];
        C[row * N + col] = sum;
    }
}
```

**Tiling** fixes this. The block cooperatively loads a small square
**tile** of A and of B into shared memory, every thread reuses those tiles
for its partial sum, then the block advances to the next tile. Each value
is read from global memory **once per tile** instead of once per output
element - a reduction proportional to the tile width.

```cpp
#define T 16                          // 16x16 tile
__global__ void matmulTiled(const float* A, const float* B, float* C, int N) {
    __shared__ float sA[T][T];        // per-block scratchpad
    __shared__ float sB[T][T];

    int row = blockIdx.y * T + threadIdx.y;
    int col = blockIdx.x * T + threadIdx.x;
    float sum = 0.0f;

    for (int t = 0; t < N / T; t++) {          // slide across tiles
        sA[threadIdx.y][threadIdx.x] = A[row * N + (t * T + threadIdx.x)];
        sB[threadIdx.y][threadIdx.x] = B[(t * T + threadIdx.y) * N + col];
        __syncthreads();                        // tile fully loaded

        for (int k = 0; k < T; k++)             // reuse from FAST memory
            sum += sA[threadIdx.y][k] * sB[k][threadIdx.x];
        __syncthreads();                        // done before overwriting
    }
    C[row * N + col] = sum;
}
```

The two `__syncthreads()` are essential: the first ensures the tile is
fully loaded before anyone multiplies; the second ensures everyone is done
multiplying before the next iteration overwrites the tile. On real
hardware the tiled version is several times faster than the naive one -
same arithmetic, far less global-memory traffic.

```mermaid
graph TD
    GA["Global A and B slow"] --> LT["Load one tile to shared"]
    LT --> S1["Barrier tile ready"]
    S1 --> MUL["Multiply reuse from shared"]
    MUL --> S2["Barrier before next tile"]
    S2 --> LT
    MUL --> ACC["Accumulate partial sums"]
```

The pattern generalizes: load once into shared memory, synchronize, reuse
many times. It is how convolutions, reductions and stencils get fast too.
""",
        ),
        quiz_lesson(
            "Quiz: Worked example - tiled matrix multiply",
            (
                q(
                    "Why is the naive matrix-multiply kernel slow?",
                    (
                        opt("It uses too many registers"),
                        opt(
                            "It is memory-bound: every thread re-reads full rows/columns "
                            "from slow global memory",
                            correct=True,
                        ),
                        opt("It does not use enough threads"),
                        opt("Matrix multiply cannot run on a GPU"),
                    ),
                    "The arithmetic is fine; the kernel starves waiting on redundant "
                    "global-memory reads.",
                ),
                q(
                    "What does tiling change to speed matrix multiply up?",
                    (
                        opt("It reduces the number of output elements"),
                        opt("It switches to integer math"),
                        opt(
                            "The block loads small tiles of A and B into shared memory "
                            "once and reuses them, cutting global-memory traffic",
                            correct=True,
                        ),
                        opt("It removes the need for a bounds check"),
                    ),
                    "Read each value from global memory once per tile, then reuse it "
                    "from fast shared memory - far fewer slow accesses.",
                ),
                q(
                    "Why does the tiled kernel need two __syncthreads() per tile?",
                    (
                        opt("To allocate and free the shared tiles"),
                        opt(
                            "One so the tile is fully loaded before multiplying, one so "
                            "all threads finish multiplying before the tile is "
                            "overwritten",
                            correct=True,
                        ),
                        opt("To copy the result back to the host"),
                        opt("To coalesce the writes to C"),
                    ),
                    "Both barriers prevent races on the shared tile: read-after-write "
                    "and write-after-read.",
                ),
            ),
        ),
        # -- 7. Optimization & pitfalls --------------------------------
        _t(
            "Optimization and common pitfalls",
            "11 min",
            """# Optimization and common pitfalls

Once a kernel is correct, a handful of ideas explain most of the
performance - and most of the mistakes.

**Occupancy.** The GPU hides latency by having many warps resident. If
each thread uses too many registers, or a block asks for too much shared
memory, fewer blocks fit per compute unit and there is less work to hide
stalls. Aim for enough occupancy that memory latency is covered - but not
blindly; past a point more occupancy stops helping.

**Warp divergence.** All 32 threads of a warp share one instruction
pointer. When threads in a warp take **different branches** of an
`if`/`else`, the warp executes *both* paths, masking off the threads that
should not run each - so a divergent branch can halve throughput.

```cpp
// Divergent: neighbors in a warp take different paths -> both run.
if (threadIdx.x % 2 == 0) doA(); else doB();

// Better: make whole warps agree. Branch on (threadIdx.x / 32) so a warp
// takes one path together.
```

**Host-device transfers.** Copying across PCIe is slow and often the real
bottleneck. Move data up **once**, do as much work as possible on the GPU,
and bring back only results. A kernel that is faster than the CPU can
still lose overall if you copy the data both ways every call.

**Other levers.** Use enough parallelism to fill the GPU (small problems
just aren't worth it); prefer coalesced access (previous lessons); avoid
`float`-to-`double` if single precision suffices (double is much slower on
most GPUs); and always **check errors and measure** - never guess. Profile
with Nsight (CUDA) or your vendor's OpenCL profiler before optimizing.

```mermaid
graph TD
    OCC["Occupancy enough resident warps"] --> HIDE["Hides memory latency"]
    DIV["Warp divergence both paths run"] --> SLOW["Halves throughput"]
    XFER["PCIe transfers are costly"] --> ONCE["Copy up once compute much"]
    MEAS["Profile before optimizing"] --> WIN["Fix the real bottleneck"]
```

The habit that matters most: **measure first**. The bottleneck is usually
memory or transfers, rarely the arithmetic you were tempted to tune.
""",
        ),
        quiz_lesson(
            "Quiz: Optimization and common pitfalls",
            (
                q(
                    "What is warp divergence and why does it hurt performance?",
                    (
                        opt("Two kernels running at once - it helps performance"),
                        opt(
                            "Threads in a warp take different branches, so the warp runs "
                            "both paths (masking threads) - cutting throughput",
                            correct=True,
                        ),
                        opt("Threads reading different memory banks"),
                        opt("The grid being larger than the data"),
                    ),
                    "One instruction pointer per warp: divergent branches serialize the "
                    "paths. Make whole warps agree.",
                ),
                q(
                    "What does occupancy refer to?",
                    (
                        opt("The percentage of the array that is non-zero"),
                        opt("How full the PCIe bus is"),
                        opt(
                            "How many warps are resident per compute unit - more "
                            "resident warps means more work to hide memory latency",
                            correct=True,
                        ),
                        opt("The number of GPUs in the machine"),
                    ),
                    "Register and shared-memory use bound occupancy; enough occupancy "
                    "keeps the scheduler busy through stalls.",
                ),
                q(
                    "A kernel is faster than the CPU version but the whole program is "
                    "slower. What is the likely cause?",
                    (
                        opt("The kernel uses too few registers"),
                        opt("The GPU clock is too low"),
                        opt(
                            "Host-device data transfers over PCIe dominate - copying up "
                            "and back each call costs more than the compute saved",
                            correct=True,
                        ),
                        opt("Warp divergence in the CPU code"),
                    ),
                    "Transfers are a classic hidden bottleneck: keep data on the GPU and "
                    "move only results.",
                ),
            ),
        ),
        # -- 8. Choosing -----------------------------------------------
        _t(
            "CUDA vs OpenCL - choosing",
            "9 min",
            """# CUDA vs OpenCL - choosing

You now know both. They share the execution model and the memory
hierarchy, so the choice is about ecosystem and reach, not concepts.

**CUDA** - NVIDIA only.

- **Pros**: the richest ecosystem - cuBLAS, cuDNN, Thrust, and the
  libraries every deep-learning framework is built on; excellent tooling
  (Nsight); newest hardware features first; large community.
- **Cons**: locks you to NVIDIA hardware.

**OpenCL** - open, cross-vendor (NVIDIA, AMD, Intel; GPUs and CPUs).

- **Pros**: portability - one code base across vendors and even CPUs;
  royalty-free open standard; good when you cannot assume NVIDIA.
- **Cons**: more host boilerplate, runtime kernel compilation, a thinner
  library ecosystem, and features sometimes lag CUDA.

A quick way to decide:

```mermaid
graph TD
    Q["What matters most"] --> NV["NVIDIA only and top ecosystem"]
    Q --> PORT["Must run on many vendors"]
    NV --> CUDA["Choose CUDA"]
    PORT --> OCL["Choose OpenCL"]
    Q --> HI["Higher level is fine"]
    HI --> ABS["SYCL or libraries or directives"]
```

**The wider landscape.** Most people writing new code do **not** hand-write
kernels at all: they use libraries (cuBLAS, cuDNN), higher-level models
(**SYCL**, a modern single-source C++ standard; Kokkos), directive
approaches (**OpenACC**, OpenMP offload), or just a framework (PyTorch,
TensorFlow) that emits kernels for them. Knowing CUDA/OpenCL is what lets
you read, debug, and push past those tools when you need to.

Bottom line: **CUDA** for maximum performance and ecosystem on NVIDIA;
**OpenCL** (or SYCL) when portability across vendors is the priority. The
mental model you learned transfers to all of them.
""",
        ),
        quiz_lesson(
            "Quiz: CUDA vs OpenCL - choosing",
            (
                q(
                    "You need maximum performance and the richest library ecosystem on "
                    "NVIDIA hardware. Which do you pick?",
                    (
                        opt("OpenCL"),
                        opt("CUDA", correct=True),
                        opt("Neither works on NVIDIA"),
                        opt("They perform identically in every case"),
                    ),
                    "CUDA's ecosystem (cuBLAS, cuDNN, Nsight) and NVIDIA-first features "
                    "make it the choice when portability is not required.",
                ),
                q(
                    "Your code must run on NVIDIA, AMD and Intel GPUs from one source. "
                    "Which fits best?",
                    (
                        opt("CUDA"),
                        opt("OpenCL (or SYCL)", correct=True),
                        opt("CUDA compiled three times"),
                        opt("Neither supports more than one vendor"),
                    ),
                    "OpenCL is the open, cross-vendor standard; SYCL is a modern "
                    "higher-level alternative with the same portability goal.",
                ),
                q(
                    "What is true of most people writing new GPU-accelerated code today?",
                    (
                        opt("Everyone hand-writes CUDA kernels"),
                        opt(
                            "Many use libraries, frameworks (PyTorch), or higher-level "
                            "models (SYCL, OpenACC) rather than raw kernels",
                            correct=True,
                        ),
                        opt("GPUs are no longer used"),
                        opt("OpenCL is required by law"),
                    ),
                    "Raw kernels underpin the tools; knowing them lets you read, debug "
                    "and extend the libraries most code relies on.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is a GPU good at?",
                    (
                        opt("Finishing a single sequential task with the lowest latency"),
                        opt(
                            "High-throughput data-parallel work: the same operation over "
                            "huge amounts of data, across thousands of threads",
                            correct=True,
                        ),
                        opt("Disk and network input/output"),
                        opt("Running unpredictable branchy control flow"),
                    ),
                    "Throughput over latency, via SIMT - one kernel replicated across "
                    "many threads.",
                ),
                q(
                    "A kernel computes `int i = blockIdx.x * blockDim.x + threadIdx.x;`. "
                    "What is `i`?",
                    (
                        opt("The block index"),
                        opt("The number of threads per block"),
                        opt(
                            "This thread's unique global index across the whole grid", correct=True
                        ),
                        opt("The total number of threads"),
                    ),
                    "Block index times block size plus the in-block thread index gives "
                    "the flattened global index.",
                ),
                q(
                    "Why does nearly every kernel include `if (i < n)`?",
                    (
                        opt("To skip zero elements"),
                        opt(
                            "The launch rounds the thread count up past n, so overhang "
                            "threads must be guarded from writing out of bounds",
                            correct=True,
                        ),
                        opt("To make the kernel asynchronous"),
                        opt("CUDA syntax requires it"),
                    ),
                    "Ceiling-division grid sizing overshoots the data; the bounds check "
                    "protects the tail.",
                ),
                q(
                    "Match the pairs: CUDA `__global__`, `<<<...>>>`, `cudaMemcpy`. What "
                    "are the OpenCL equivalents?",
                    (
                        opt(
                            "`__kernel`, clEnqueueNDRangeKernel, clEnqueueWrite/ReadBuffer",
                            correct=True,
                        ),
                        opt("`__device__`, clCreateContext, clBuildProgram"),
                        opt("`__local`, clSetKernelArg, clCreateBuffer"),
                        opt("`__shared__`, clFinish, clReleaseKernel"),
                    ),
                    "Kernel qualifier, launch, and the host/device copies map one-to-one "
                    "between the two APIs.",
                ),
                q(
                    "Order the GPU memory spaces from fastest to slowest.",
                    (
                        opt("Global, shared, registers"),
                        opt("Registers, shared/local, global", correct=True),
                        opt("Shared, global, registers"),
                        opt("They all have the same speed"),
                    ),
                    "Per-thread registers (fastest), per-block shared/local memory, then "
                    "large slow global DRAM.",
                ),
                q(
                    "What is memory coalescing and why does it matter?",
                    (
                        opt("Merging kernels; it saves launches"),
                        opt(
                            "Contiguous global accesses by a warp combine into few wide "
                            "transactions - the key to using memory bandwidth",
                            correct=True,
                        ),
                        opt("Compressing data in registers"),
                        opt("Caching the grid configuration"),
                    ),
                    "Adjacent threads to adjacent addresses = full bandwidth; strided "
                    "access can be an order of magnitude slower.",
                ),
                q(
                    "In tiled matrix multiply, what does shared memory buy you?",
                    (
                        opt("More output elements"),
                        opt("A smaller grid"),
                        opt(
                            "Each A/B value is read from global memory once per tile and "
                            "reused many times from fast on-chip memory",
                            correct=True,
                        ),
                        opt("Automatic error checking"),
                    ),
                    "Load once, synchronize, reuse - the pattern that turns a "
                    "memory-bound kernel into a fast one.",
                ),
                q(
                    "Threads in a warp run `if (threadIdx.x % 2) A(); else B();`. What happens?",
                    (
                        opt("Only A() runs"),
                        opt("The warp is split into two warps"),
                        opt(
                            "Warp divergence: the warp executes both A() and B(), masking "
                            "the inactive threads on each - reducing throughput",
                            correct=True,
                        ),
                        opt("A compile error"),
                    ),
                    "One instruction pointer per warp forces both branch paths to run "
                    "when threads disagree.",
                ),
                q(
                    "Your GPU kernel beats the CPU but the program is slower overall. "
                    "First thing to check?",
                    (
                        opt("Add more threads per block"),
                        opt("Switch float to double"),
                        opt(
                            "Host-device transfer cost over PCIe - copy data up once and "
                            "keep it resident, returning only results",
                            correct=True,
                        ),
                        opt("Rewrite in OpenCL"),
                    ),
                    "Transfers are the classic hidden bottleneck; measure and minimize "
                    "them before tuning arithmetic.",
                ),
                q(
                    "When should you reach for CUDA over OpenCL?",
                    (
                        opt("When the code must run on AMD and Intel too"),
                        opt(
                            "When targeting NVIDIA and you want the richest ecosystem "
                            "and tooling (cuBLAS, cuDNN, Nsight)",
                            correct=True,
                        ),
                        opt("When you want zero host boilerplate"),
                        opt("CUDA is never preferable"),
                    ),
                    "CUDA for NVIDIA performance/ecosystem; OpenCL (or SYCL) when "
                    "cross-vendor portability is the priority.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

GPU_PROGRAMMING_COURSES: tuple[SeedCourse, ...] = (_GPU_PROGRAMMING,)
