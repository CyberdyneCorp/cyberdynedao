"""Algorithms & Data Structures track: Basics -> Intermediate -> Advanced.

Complexity & Big-O, searching & sorting, recursion, core data structures, graph
traversal, greedy, dynamic programming and shortest paths. Lessons are `text`
with LaTeX, side-by-side MATLAB and Python code, and interactive ```plot blocks —
growth races, a binary-search interval that halves, animated array scans, and
animated graph traversals / DP table fills built by the helpers below. Runnable
Python labs are iterative (the restricted interpreter sandboxes functions, so
recursion is shown as reference and implemented with explicit stacks/queues).
"""

# Lesson prose uses typographic characters (×, →, ≈, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

import json
from typing import Any

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


def _num(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else str(v)


def _piecewise(values: list[float], var: str = "t") -> str:
    """A step lookup expression: returns values[floor(var)] via nested if()."""
    expr = _num(values[-1])
    for i in range(len(values) - 2, -1, -1):
        expr = f"if({var}<{i + 1},{_num(values[i])},{expr})"
    return expr


def _graph_block(
    title: str,
    nodes: dict[str, tuple[float, float]],
    edges: list[tuple[str, str]],
    *,
    visit: list[str] | None = None,
    weights: list[int] | None = None,
    animate_label: str = "visit order",
) -> str:
    """A node/edge graph; if ``visit`` is given, a marker animates through the
    nodes in that order (with a trail tracing the path)."""
    xs = [p[0] for p in nodes.values()]
    ys = [p[1] for p in nodes.values()]
    series: list[dict[str, Any]] = [
        {"points": [list(nodes[a]), list(nodes[b])], "color": "#cbd5e1"} for a, b in edges
    ]
    points: list[dict[str, Any]] = [
        {"x": x, "y": y, "label": name, "color": "#2563eb", "size": 10}
        for name, (x, y) in nodes.items()
    ]
    if weights:
        for (a, b), w in zip(edges, weights, strict=False):
            mx = round((nodes[a][0] + nodes[b][0]) / 2, 2)
            my = round((nodes[a][1] + nodes[b][1]) / 2, 2)
            points.append({"x": mx, "y": my, "label": str(w), "color": "#9333ea", "size": 3})
    spec: dict[str, Any] = {
        "title": title,
        "equal": True,
        "grid": False,
        "xRange": [min(xs) - 0.7, max(xs) + 0.7],
        "yRange": [min(ys) - 0.7, max(ys) + 0.7],
        "series": series,
        "points": points,
    }
    if visit:
        coords = [nodes[n] for n in visit]
        spec["animate"] = {"param": "t", "range": [0, len(visit)], "label": animate_label}
        spec["points"].append(
            {
                "xExpr": _piecewise([c[0] for c in coords]),
                "yExpr": _piecewise([c[1] for c in coords]),
                "color": "#dc2626",
                "size": 14,
                "label": "visiting",
                "trail": True,
            }
        )
    return "```plot\n" + json.dumps(spec, ensure_ascii=False) + "\n```"


def _grid_sweep_block(title: str, nx: int, ny: int, xlabel: str, ylabel: str) -> str:
    """A grid of subproblem cells with a marker sweeping row-major (a DP fill)."""
    points: list[dict[str, Any]] = [
        {"x": i, "y": j, "color": "#cbd5e1", "size": 5} for i in range(nx) for j in range(ny)
    ]
    points.append(
        {
            "xExpr": f"mod(floor(t),{nx})",
            "yExpr": f"floor(floor(t)/{nx})",
            "color": "#dc2626",
            "size": 13,
            "label": "computing",
            "trail": True,
        }
    )
    spec: dict[str, Any] = {
        "title": title,
        "grid": True,
        "equal": True,
        "xLabel": xlabel,
        "yLabel": ylabel,
        "xRange": [-0.6, nx - 0.4],
        "yRange": [-0.6, ny - 0.4],
        "animate": {"param": "t", "range": [0, nx * ny], "label": "cells filled"},
        "points": points,
    }
    return "```plot\n" + json.dumps(spec, ensure_ascii=False) + "\n```"


# Reusable graph pictures ----------------------------------------------------
_FIB_TREE = _graph_block(
    "Recursion tree of fib(3) — each call branches into two",
    {"f3": (2, 2), "f2": (1, 1), "f1a": (3, 1), "f1b": (0.3, 0), "f0": (1.7, 0)},
    [("f3", "f2"), ("f3", "f1a"), ("f2", "f1b"), ("f2", "f0")],
    visit=["f3", "f2", "f1b", "f0", "f1a"],
    animate_label="call order",
)
_MERGE_TREE = _graph_block(
    "Merge sort splits the array in half, recursively",
    {
        "n8": (4, 2),
        "l4": (2, 1),
        "r4": (6, 1),
        "a2": (1, 0),
        "b2": (3, 0),
        "c2": (5, 0),
        "d2": (7, 0),
    },
    [("n8", "l4"), ("n8", "r4"), ("l4", "a2"), ("l4", "b2"), ("r4", "c2"), ("r4", "d2")],
    visit=["n8", "l4", "a2", "b2", "r4", "c2", "d2"],
    animate_label="split order",
)
_BST = _graph_block(
    "Binary search tree — search 6 follows one path down",
    {"8": (4, 2), "3": (2, 1), "10": (6, 1), "1": (1, 0), "6": (3, 0), "14": (7, 0)},
    [("8", "3"), ("8", "10"), ("3", "1"), ("3", "6"), ("10", "14")],
    visit=["8", "3", "6"],
    animate_label="search path",
)
_BFS_NODES = {
    "A": (0, 2),
    "B": (1.6, 3),
    "C": (1.6, 1),
    "D": (3.2, 3),
    "E": (3.2, 1),
    "F": (4.8, 2),
}
_BFS_EDGES = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "F"), ("E", "F")]
_BFS = _graph_block(
    "Breadth-first search visits in rings from the start (A)",
    _BFS_NODES,
    _BFS_EDGES,
    visit=["A", "B", "C", "D", "E", "F"],
    animate_label="BFS order",
)
_DFS = _graph_block(
    "Depth-first search dives deep before backtracking",
    _BFS_NODES,
    _BFS_EDGES,
    visit=["A", "B", "D", "F", "E", "C"],
    animate_label="DFS order",
)
_DIJKSTRA = _graph_block(
    "Dijkstra expands nodes in order of distance from A",
    _BFS_NODES,
    _BFS_EDGES,
    weights=[4, 1, 2, 5, 3, 4, 2],
    visit=["A", "C", "B", "D", "F", "E"],
    animate_label="settle order",
)
_DP_GRID = _grid_sweep_block(
    "Dynamic programming fills a table of subproblems", 6, 5, "item", "capacity"
)

# Activity selection (greedy) — intervals on a timeline, chosen ones in green.
_ACTS = [(1, 3, 0, True), (2, 5, 1, False), (4, 7, 2, True), (5, 9, 3, False), (8, 10, 4, True)]
_ACTIVITY = (
    "```plot\n"
    + json.dumps(
        {
            "title": "Greedy activity selection: keep the earliest-finishing job",
            "xLabel": "time",
            "yLabel": "activity",
            "xRange": [0, 11],
            "yRange": [-0.5, 4.5],
            "grid": True,
            "series": [
                {
                    "points": [[s, row], [e, row]],
                    "color": "#16a34a" if sel else "#cbd5e1",
                    "label": "chosen" if sel else None,
                }
                for (s, e, row, sel) in _ACTS
            ],
        },
        ensure_ascii=False,
    )
    + "\n```"
)


# ── Algorithms — Basics ──────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="algorithms-basics",
    title="Algorithms — Basics",
    description=(
        "Think like a computer scientist: measuring cost with Big-O, searching "
        "(linear vs binary), elementary sorting, and recursion. Interactive "
        "growth races, a halving search interval and animated array scans, with "
        "MATLAB and Python code and a runnable lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Complexity & Big-O",
            "12 min",
            "# Complexity & Big-O\n\n"
            "An algorithm's **time complexity** says how its work grows with the input size "
            "$n$ — independent of the machine. **Big-O** keeps only the dominant term: "
            "$O(1)$, $O(\\log n)$, $O(n)$, $O(n\\log n)$, $O(n^2)$, $O(2^n)$. For small $n$ "
            "they're close; as $n$ grows they diverge brutally — choosing the green curve "
            "over the red one is what algorithm design is about:\n\n" + "```plot\n"
            '{"title": "Big-O: how work grows with input size n", "xLabel": "n", "yLabel": '
            '"operations", "xRange": [1, 8], "yRange": [0, 260], "functions": [{"expr": "x", '
            '"label": "O(n) linear", "color": "#16a34a"}, {"expr": "x*log2(x+1)", "label": '
            '"O(n log n)", "color": "#0891b2"}, {"expr": "x^2", "label": "O(n²) quadratic", '
            '"color": "#2563eb"}, {"expr": "2^x", "label": "O(2ⁿ) exponential", "color": '
            '"#dc2626"}]}\n'
            "```\n\n"
            "We care about the **worst case** (the guarantee) and usually ignore constants. "
            "Time it in practice with `tic/toc` (MATLAB) or `time.perf_counter()` (Python), "
            "but reason about it with Big-O.\n\n"
            "**Next:** the first big win — binary search.",
        ),
        _t(
            "Searching: linear vs binary",
            "12 min",
            "# Searching: linear vs binary\n\n"
            "**Linear search** scans every element — $O(n)$. If the array is **sorted**, "
            "**binary search** checks the middle and throws away half the candidates each "
            "step — $O(\\log n)$. Slide the step and watch the search interval **halve**:\n\n"
            + "```plot\n"
            '{"title": "Binary search halves the interval each step", "xLabel": "index", '
            '"yLabel": "", "xRange": [-1, 16], "yRange": [-1, 1.6], "controls": [{"name": '
            '"step", "range": [0, 4], "value": 0, "step": 1, "label": "step"}], "series": '
            '[{"points": [[0, 0], [15, 0]], "color": "#cbd5e1", "label": "sorted array 0..15"}], '
            '"vectors": [{"fromExpr": ["8-8/2^step", "0.6"], "xExpr": "8+8/2^step", "yExpr": '
            '"0.6", "color": "#16a34a", "label": "candidates left"}]}\n'
            "```\n\n"
            "16 elements take at most 4 comparisons ($\\log_2 16$); a million take only 20. "
            "Here is the candidate count, linear vs binary:\n\n" + "```plot\n"
            '{"title": "Candidates remaining per step", "xLabel": "steps", "yLabel": '
            '"candidates", "xRange": [0, 16], "yRange": [0, 16], "functions": [{"expr": '
            '"16-x", "label": "linear: −1 each step", "color": "#dc2626"}, {"expr": "16/2^x", '
            '"label": "binary: ÷2 each step", "color": "#16a34a"}]}\n'
            "```\n\n"
            "**MATLAB**\n"
            "```matlab\n"
            "lo = 1; hi = numel(a);\n"
            "while lo <= hi\n"
            "    mid = floor((lo + hi) / 2);\n"
            "    if a(mid) == target, break; elseif a(mid) < target, lo = mid + 1; else, hi = mid - 1; end\n"
            "end\n"
            "```\n\n"
            "**Python**\n"
            "```python\n"
            "lo, hi = 0, len(a) - 1\n"
            "while lo <= hi:\n"
            "    mid = (lo + hi) // 2\n"
            "    if a[mid] == target: break\n"
            "    elif a[mid] < target: lo = mid + 1\n"
            "    else: hi = mid - 1\n"
            "```\n\n"
            "**Next:** putting elements in order — sorting.",
        ),
        _t(
            "Elementary sorting",
            "12 min",
            "# Elementary sorting\n\n"
            "The simple sorts — **bubble**, **insertion**, **selection** — repeatedly compare "
            "neighbours and swap. They're easy but $O(n^2)$: doubling the array quadruples "
            "the work. The smarter $O(n\\log n)$ sorts (next course) pull far ahead:\n\n"
            + "```plot\n"
            '{"title": "Sorting cost: comparisons vs array size", "xLabel": "n", "yLabel": '
            '"comparisons", "xRange": [1, 30], "yRange": [0, 900], "functions": [{"expr": '
            '"x^2", "label": "bubble/insertion O(n²)", "color": "#dc2626"}, {"expr": '
            '"x*log2(x+1)", "label": "merge/quick O(n log n)", "color": "#16a34a"}]}\n'
            "```\n\n"
            "One pass scans the array comparing as it goes — press **Play** to watch the "
            "index sweep across (insertion sort grows a sorted prefix on the left):\n\n"
            + "```plot\n"
            '{"title": "A sorting pass scans the array", "xLabel": "index", "yLabel": '
            '"value", "xRange": [-0.5, 8.5], "yRange": [0, 10], "animate": {"param": "t", '
            '"range": [0, 8], "label": "scan index i"}, "series": [{"points": [[0,5],[1,2],'
            '[2,8],[3,1],[4,9],[5,3],[6,7],[7,4],[8,6]], "label": "array", "color": '
            '"#2563eb"}], "points": [{"xExpr": "floor(t)", "yExpr": '
            + '"'
            + _piecewise([5, 2, 8, 1, 9, 3, 7, 4, 6]).replace('"', '\\"')
            + '"'
            + ', "color": "#dc2626", "size": 11, "label": "current i"}]}\n'
            "```\n\n"
            "Two properties matter in practice: **stability** (equal keys keep their order) "
            "and **in-place** (no extra memory). The lab implements insertion sort.\n\n"
            "**Next:** algorithms that call themselves — recursion.",
        ),
        _t(
            "Recursion",
            "11 min",
            "# Recursion\n\n"
            "A **recursive** function solves a problem by calling itself on a smaller piece, "
            "stopping at a **base case**. Factorial: $n! = n\\cdot(n-1)!$, with $0! = 1$. Each "
            "call adds a frame to the **call stack**.\n\n"
            "```python\n"
            "def factorial(n):\n"
            "    if n <= 1: return 1          # base case\n"
            "    return n * factorial(n - 1)  # recursive case\n"
            "```\n\n"
            "But naive recursion can explode. `fib(n) = fib(n-1) + fib(n-2)` re-computes the "
            "same calls again and again — its call tree branches exponentially:\n\n"
            + _FIB_TREE
            + "\n\nThat's $O(2^n)$ calls; **memoizing** (caching results) collapses it to "
            "$O(n)$ — the gateway to dynamic programming in the Advanced course:\n\n" + "```plot\n"
            '{"title": "Naive recursion explodes; memoization is linear", "xLabel": "n", '
            '"yLabel": "calls", "xRange": [1, 14], "yRange": [0, 1000], "functions": '
            '[{"expr": "2^x", "label": "naive fib ~O(2ⁿ)", "color": "#dc2626"}, {"expr": "x", '
            '"label": "memoized O(n)", "color": "#16a34a"}]}\n'
            "```\n\n"
            "Any recursion can be rewritten **iteratively** with an explicit stack — which is "
            "exactly how the labs do it.\n\n"
            "**Next:** test what you've learned.",
        ),
        _code(
            "Lab: binary search & insertion sort",
            "12 min",
            "# Searching and sorting, iteratively (Python).\n\n"
            "a = [11, 3, 25, 7, 19, 2, 14, 9]\n\n"
            "# INSERTION SORT (in place, O(n^2)) — count the comparisons.\n"
            "comparisons = 0\n"
            "for i in range(1, len(a)):\n"
            "    key = a[i]\n"
            "    j = i - 1\n"
            "    while j >= 0 and a[j] > key:\n"
            "        comparisons = comparisons + 1\n"
            "        a[j + 1] = a[j]\n"
            "        j = j - 1\n"
            "    a[j + 1] = key\n"
            'print("sorted:", a, " comparisons:", comparisons)\n\n'
            "# BINARY SEARCH on the now-sorted array (O(log n)).\n"
            "target = 14\n"
            "lo, hi, steps, found = 0, len(a) - 1, 0, -1\n"
            "while lo <= hi:\n"
            "    steps = steps + 1\n"
            "    mid = (lo + hi) // 2\n"
            "    if a[mid] == target:\n"
            "        found = mid\n"
            "        break\n"
            "    elif a[mid] < target:\n"
            "        lo = mid + 1\n"
            "    else:\n"
            "        hi = mid - 1\n"
            'print("found", target, "at index", found, "in", steps, "steps")\n\n'
            "# Try it:\n"
            "#   - Sort a bigger random-ish list and watch comparisons grow ~ n^2.\n"
            "#   - Search a value that is absent: found stays -1 after ~log2(n) steps.\n",
        ),
        _quiz(),
    ),
)

# ── Algorithms — Intermediate ────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="algorithms-intermediate",
    title="Algorithms — Data Structures & Graphs",
    description=(
        "The efficient toolkit: divide-and-conquer sorting (merge & quick), the "
        "core data structures (stack, queue, hash map, heap, BST), and graph "
        "traversal (BFS & DFS). Animated split/search trees and graph traversals, "
        "with MATLAB and Python code and a runnable lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Divide & conquer: merge & quick sort",
            "13 min",
            "# Divide & conquer: merge & quick sort\n\n"
            "**Divide and conquer** splits a problem in half, solves each half, and combines. "
            "**Merge sort** splits to single elements then merges sorted runs; **quick sort** "
            "partitions around a pivot. Both run in $O(n\\log n)$ — the split tree has "
            "$\\log n$ levels, each costing $O(n)$:\n\n"
            + _MERGE_TREE
            + "\n\nThe runtime obeys the recurrence $T(n) = 2\\,T(n/2) + O(n)$, which the "
            "**Master theorem** (see Discrete Mathematics) solves to $\\Theta(n\\log n)$ — a "
            "huge win over the $O(n^2)$ simple sorts:\n\n" + "```plot\n"
            '{"title": "n log n vs n²", "xLabel": "n", "yLabel": "comparisons", "xRange": '
            '[1, 40], "yRange": [0, 1600], "functions": [{"expr": "x^2", "label": "O(n²)", '
            '"color": "#dc2626"}, {"expr": "x*log2(x+1)", "label": "O(n log n)", "color": '
            '"#16a34a"}]}\n'
            "```\n\n"
            "Quick sort is fastest in practice (cache-friendly, in-place) but $O(n^2)$ in the "
            "worst case; merge sort guarantees $O(n\\log n)$ and is stable. Python's `sorted` "
            "and MATLAB's `sort` use tuned hybrids (Timsort / introsort).\n\n"
            "**Next:** the data structures these algorithms run on.",
        ),
        _t(
            "Core data structures",
            "13 min",
            "# Core data structures\n\n"
            "The right structure makes an algorithm fast:\n\n"
            "| structure | access | use |\n"
            "|-----------|--------|-----|\n"
            "| **array / list** | index $O(1)$ | dense sequences |\n"
            "| **stack** (LIFO) | push/pop $O(1)$ | undo, DFS, call stack |\n"
            "| **queue** (FIFO) | enqueue/dequeue $O(1)$ | scheduling, BFS |\n"
            "| **hash map** | lookup $O(1)$ avg | dictionaries, dedup, caches |\n"
            "| **heap** (priority queue) | min/max $O(\\log n)$ | Dijkstra, scheduling |\n"
            "| **binary search tree** | search $O(\\log n)$ | ordered sets/maps |\n\n"
            "A **hash map** turns a key into a bucket index with a hash function (here "
            "`key mod m`) — giving near-constant lookup. Change the bucket count and watch "
            "keys map around (collisions share a bucket):\n\n" + "```plot\n"
            '{"title": "Hashing: bucket = key mod m (O(1) average lookup)", "xLabel": "key", '
            '"yLabel": "bucket", "xRange": [0, 24], "yRange": [0, 10], "controls": [{"name": '
            '"m", "range": [2, 10], "value": 7, "step": 1, "label": "buckets m"}], '
            '"functions": [{"expr": "mod(x, m)", "label": "key mod m", "color": "#2563eb"}]}\n'
            "```\n\n"
            "**MATLAB**: `containers.Map`, struct arrays, `[stack; x]`. "
            "**Python**: `dict`, `set`, `list` (stack), `collections.deque` (queue), "
            "`heapq` (heap). The lab uses lists as a queue and a stack.\n\n"
            "**Next:** trees and heaps in detail.",
        ),
        _t(
            "Trees, heaps & the BST",
            "12 min",
            "# Trees, heaps & the BST\n\n"
            "A **binary search tree (BST)** keeps smaller keys left, larger keys right — so "
            "searching follows a single root-to-leaf path in $O(\\log n)$ (when balanced). "
            "Press **Play** to search for **6**: at each node go left or right, never both:\n\n"
            + _BST
            + "\n\nUnbalanced inserts degrade a BST to $O(n)$ (a linked list); self-balancing "
            "trees (AVL, red-black) keep it $O(\\log n)$.\n\n"
            "A **heap** is a complete binary tree kept as a flat array where each parent "
            "beats its children (min-heap: parent ≤ children). It gives the min/max in "
            "$O(1)$ and insert/extract in $O(\\log n)$ — the engine behind **priority "
            "queues** and Dijkstra. For a node at index $i$: children at $2i+1$, $2i+2$.\n\n"
            "**Next:** searching graphs — BFS & DFS.",
        ),
        _t(
            "Graph traversal: BFS & DFS",
            "13 min",
            "# Graph traversal: BFS & DFS\n\n"
            "A **graph** is nodes joined by edges (roads, networks, dependencies). Two ways "
            "to visit every reachable node, both $O(V+E)$:\n\n"
            "- **BFS** uses a **queue** — it explores in expanding rings, so it finds the "
            "**fewest-hops** path. Press **Play**:\n\n"
            + _BFS
            + "\n\n- **DFS** uses a **stack** (or recursion) — it dives as deep as possible, "
            "then backtracks. Great for cycle detection, topological sort, connectivity:\n\n"
            + _DFS
            + "\n\n**Python (BFS, iterative)**\n"
            "```python\n"
            "from collections import deque\n"
            "seen, q = {start}, deque([start])\n"
            "while q:\n"
            "    u = q.popleft()\n"
            "    for v in adj[u]:\n"
            "        if v not in seen: seen.add(v); q.append(v)\n"
            "```\n\n"
            "**MATLAB**: `bfsearch(G, start)` / `dfsearch(G, start)` on a `graph` object. "
            "The lab implements both with plain lists.\n\n"
            "**Next:** test what you've learned.",
        ),
        _code(
            "Lab: BFS & DFS on a graph",
            "12 min",
            "# Breadth-first and depth-first search on an adjacency list (iterative).\n\n"
            "adj = {\n"
            '    "A": ["B", "C"],\n'
            '    "B": ["A", "C", "D"],\n'
            '    "C": ["A", "B", "E"],\n'
            '    "D": ["B", "F"],\n'
            '    "E": ["C", "F"],\n'
            '    "F": ["D", "E"],\n'
            "}\n\n"
            "# BFS with a list as a queue (pop from the front).\n"
            'start = "A"\n'
            "seen = [start]\n"
            "queue = [start]\n"
            "bfs_order = []\n"
            "while queue:\n"
            "    u = queue.pop(0)\n"
            "    bfs_order.append(u)\n"
            "    for v in adj[u]:\n"
            "        if v not in seen:\n"
            "            seen.append(v)\n"
            "            queue.append(v)\n"
            'print("BFS:", bfs_order)\n\n'
            "# DFS with a list as a stack (pop from the end) — iterative, no recursion.\n"
            "seen2 = []\n"
            "stack = [start]\n"
            "dfs_order = []\n"
            "while stack:\n"
            "    u = stack.pop()\n"
            "    if u in seen2:\n"
            "        continue\n"
            "    seen2.append(u)\n"
            "    dfs_order.append(u)\n"
            "    for v in adj[u]:\n"
            "        if v not in seen2:\n"
            "            stack.append(v)\n"
            'print("DFS:", dfs_order)\n\n'
            "# Try it:\n"
            "#   - Add an edge and watch both orders change.\n"
            "#   - BFS order is by distance from A; DFS plunges down one branch first.\n",
        ),
        _quiz(),
    ),
)

# ── Algorithms — Advanced ────────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="algorithms-advanced",
    title="Algorithms — Greedy, DP & Shortest Paths",
    description=(
        "Design techniques for hard problems: greedy algorithms, dynamic "
        "programming, shortest paths (Dijkstra & Bellman-Ford), and the limits of "
        "computation (P vs NP). Animated greedy/DP/Dijkstra visuals, with MATLAB "
        "and Python code and a runnable Dijkstra lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Greedy algorithms",
            "12 min",
            "# Greedy algorithms\n\n"
            "A **greedy** algorithm makes the locally-best choice at each step and never "
            "looks back. It's fast and simple — and **provably optimal** only when the "
            "problem has the *greedy-choice property* and *optimal substructure*.\n\n"
            "Classic: **activity selection** — fit the most non-overlapping jobs into a room. "
            "The greedy rule 'always take the next activity that **finishes earliest**' is "
            "optimal. The green bars are chosen; greedily skipping overlaps leaves room for "
            "more later:\n\n"
            + _ACTIVITY
            + "\n\nOther greedy wins: **Huffman coding** (see Information Theory), minimum "
            "spanning trees (**Kruskal/Prim**), and Dijkstra. But greedy **fails** on, e.g., "
            "arbitrary coin systems or 0/1 knapsack — there you need dynamic programming.\n\n"
            "**Next:** when greedy isn't enough — dynamic programming.",
        ),
        _t(
            "Dynamic programming",
            "14 min",
            "# Dynamic programming\n\n"
            "**Dynamic programming (DP)** cracks problems with **overlapping subproblems** "
            "and **optimal substructure** by solving each subproblem **once** and storing it "
            "— turning exponential recursion into polynomial time. The contrast is dramatic:\n\n"
            + "```plot\n"
            '{"title": "DP vs naive recursion", "xLabel": "n", "yLabel": "operations", '
            '"xRange": [1, 14], "yRange": [0, 1000], "functions": [{"expr": "2^x", "label": '
            '"naive recursion O(2ⁿ)", "color": "#dc2626"}, {"expr": "x^2", "label": '
            '"DP O(n²)", "color": "#16a34a"}]}\n'
            "```\n\n"
            "Two styles: **memoization** (top-down cache) and **tabulation** (bottom-up fill "
            "of a table). Press **Play** to watch a knapsack/LCS table fill, each cell built "
            "from already-solved neighbours:\n\n"
            + _DP_GRID
            + "\n\nFamous DPs: **Fibonacci**, **0/1 knapsack**, **longest common subsequence** "
            "(diff tools), **edit distance** (spell-check), matrix-chain order. The skill is "
            "spotting the recurrence and the table dimensions.\n\n"
            "**Next:** DP and greedy meet graphs — shortest paths.",
        ),
        _t(
            "Shortest paths: Dijkstra & Bellman-Ford",
            "13 min",
            "# Shortest paths: Dijkstra & Bellman-Ford\n\n"
            "On a **weighted** graph, the shortest path minimises total edge weight. The core "
            "operation is **relaxation**: if going through $u$ improves the distance to $v$, "
            "update it.\n\n"
            "**Dijkstra** repeatedly settles the nearest unsettled node (using a "
            "**priority queue / heap**) — $O((V+E)\\log V)$, but needs **non-negative** "
            "weights. Press **Play** to watch it expand outward from A by distance (edge "
            "weights in purple):\n\n"
            + _DIJKSTRA
            + "\n\n**Bellman-Ford** relaxes every edge $V-1$ times — slower ($O(VE)$) but "
            "handles **negative** weights and detects negative cycles. **A\\*** speeds "
            "Dijkstra up with a heuristic (game/GPS routing).\n\n"
            "**Python (Dijkstra with a heap)**\n"
            "```python\n"
            "import heapq\n"
            "dist = {s: 0}; pq = [(0, s)]\n"
            "while pq:\n"
            "    d, u = heapq.heappop(pq)\n"
            "    for v, w in adj[u]:\n"
            "        if d + w < dist.get(v, 1e9):\n"
            "            dist[v] = d + w; heapq.heappush(pq, (dist[v], v))\n"
            "```\n\n"
            "**MATLAB**: `shortestpath(G, s, t)` on a weighted `graph`. The lab implements "
            "Dijkstra from scratch.\n\n"
            "**Next:** the problems no fast algorithm can solve — P vs NP.",
        ),
        _t(
            "Complexity classes: P, NP & intractability",
            "12 min",
            "# Complexity classes: P, NP & intractability\n\n"
            "Some problems we can solve quickly; others we only know how to **check** "
            "quickly.\n\n"
            "- **P** — solvable in polynomial time (sorting, shortest paths, matching).\n"
            "- **NP** — a proposed solution can be *verified* in polynomial time.\n"
            "- **NP-complete** — the hardest in NP (travelling salesman, SAT, knapsack); a "
            "fast algorithm for one would crack them all. Whether $P = NP$ is the famous open "
            "question.\n\n"
            "Why it matters: brute force over $n$ items is $O(2^n)$ or $O(n!)$ — a wall you "
            "hit fast. At $n=20$, $n!$ already exceeds $10^{18}$:\n\n" + "```plot\n"
            '{"title": "Why brute force fails: polynomial vs exponential vs factorial", '
            '"xLabel": "problem size n", "yLabel": "operations", "xRange": [1, 12], "yRange": '
            '[0, 4096], "functions": [{"expr": "x^3", "label": "polynomial O(n³)", "color": '
            '"#16a34a"}, {"expr": "2^x", "label": "exponential O(2ⁿ)", "color": "#dc2626"}, '
            '{"expr": "exp(x*ln(x)-x)", "label": "factorial O(n!)", "color": "#9333ea"}]}\n'
            "```\n\n"
            "For NP-hard problems in practice we use **heuristics**, **approximation "
            "algorithms** (provably near-optimal), and solvers (SAT/ILP) — trading a "
            "guarantee of optimality for tractable runtime.\n\n"
            "**Next:** implement Dijkstra in code.",
        ),
        _code(
            "Lab: Dijkstra's shortest paths",
            "13 min",
            "# Dijkstra's algorithm from scratch (iterative, no heap library needed).\n\n"
            "# weighted graph as an adjacency list: node -> list of (neighbour, weight)\n"
            "adj = {\n"
            '    "A": [("B", 4), ("C", 1)],\n'
            '    "B": [("C", 2), ("D", 1)],\n'
            '    "C": [("B", 2), ("E", 5)],\n'
            '    "D": [("F", 3)],\n'
            '    "E": [("F", 2)],\n'
            '    "F": [],\n'
            "}\n"
            'nodes = ["A", "B", "C", "D", "E", "F"]\n'
            'start = "A"\n\n'
            "INF = 1e9\n"
            "dist = {}\n"
            "done = {}\n"
            "for n in nodes:\n"
            "    dist[n] = 0.0 if n == start else INF\n"
            "    done[n] = False\n\n"
            "# Repeatedly settle the nearest unsettled node, then relax its edges.\n"
            "for step in range(len(nodes)):\n"
            "    u = None\n"
            "    best = INF + 1\n"
            "    for n in nodes:\n"
            "        if not done[n] and dist[n] < best:\n"
            "            best = dist[n]\n"
            "            u = n\n"
            "    if u is None:\n"
            "        break\n"
            "    done[u] = True\n"
            "    for v, w in adj[u]:\n"
            "        if dist[u] + w < dist[v]:\n"
            "            dist[v] = dist[u] + w\n\n"
            'print("shortest distance from A:")\n'
            "for n in nodes:\n"
            '    print("  ", n, "=", dist[n])\n\n'
            "# Try it:\n"
            "#   - Change a weight and watch the shortest distances update.\n"
            "#   - The settle order here is A, C, B, D, E, F — by increasing distance.\n",
        ),
        _quiz(),
    ),
)


ALGORITHMS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)

__all__ = ["ALGORITHMS_COURSES"]
