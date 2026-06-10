"""Curated quiz questions for the Algorithms - Intermediate course
(per-lesson checkpoints keyed by exact content-lesson title plus a final
comprehensive quiz). Grounded in the lesson bodies of seed_algorithms."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Divide & conquer: merge & quick sort": (
            q(
                "What time complexity do both merge sort and quick sort run in?",
                (
                    opt("O(n)"),
                    opt("O(n log n)", correct=True),
                    opt("O(n^2)"),
                    opt("O(log n)"),
                ),
                "The lesson states both run in O(n log n) because the split tree has log n levels each costing O(n).",
            ),
            q(
                "How does quick sort compare to merge sort according to the lesson?",
                (
                    opt(
                        "Quick sort is fastest in practice but O(n^2) worst case; merge sort guarantees O(n log n) and is stable",
                        correct=True,
                    ),
                    opt("Quick sort is always faster and never degrades to O(n^2)"),
                    opt("Merge sort is in-place while quick sort needs extra memory"),
                    opt("Both are unstable and both guarantee O(n log n) worst case"),
                ),
                "Quick sort is cache-friendly and in-place but O(n^2) worst case, while merge sort guarantees O(n log n) and is stable.",
            ),
            q(
                "Which recurrence describes the runtime of these divide-and-conquer sorts?",
                (
                    opt("T(n) = T(n-1) + O(1)"),
                    opt("T(n) = 2 T(n/2) + O(n)", correct=True),
                    opt("T(n) = T(n/2) + O(1)"),
                    opt("T(n) = 2 T(n) + O(n)"),
                ),
                "The lesson gives T(n) = 2 T(n/2) + O(n), which the Master theorem solves to Theta(n log n).",
            ),
        ),
        "Core data structures": (
            q(
                "What ordering discipline does a stack follow?",
                (
                    opt("FIFO (first in, first out)"),
                    opt("LIFO (last in, first out)", correct=True),
                    opt("Sorted by key"),
                    opt("Random access by index"),
                ),
                "The lesson labels the stack LIFO and uses it for undo, DFS, and the call stack.",
            ),
            q(
                "According to the lesson, how does a hash map compute which bucket a key goes in?",
                (
                    opt("It sorts the keys and uses binary search"),
                    opt("It applies a hash function such as key mod m", correct=True),
                    opt("It stores every key in a single bucket"),
                    opt("It uses the heap parent-child index formula"),
                ),
                "A hash map turns a key into a bucket index with a hash function, shown here as key mod m, giving near-constant lookup.",
            ),
            q(
                "Which structure is described as a priority queue with min/max in O(log n) operations?",
                (
                    opt("The heap", correct=True),
                    opt("The queue"),
                    opt("The array / list"),
                    opt("The hash map"),
                ),
                "The lesson lists the heap as the priority queue used by Dijkstra and scheduling, with O(log n) operations.",
            ),
        ),
        "Trees, heaps & the BST": (
            q(
                "How does a binary search tree organize its keys?",
                (
                    opt("Smaller keys left, larger keys right", correct=True),
                    opt("All keys in insertion order in a flat array"),
                    opt("Larger keys left, smaller keys right"),
                    opt("Keys hashed into buckets"),
                ),
                "A BST keeps smaller keys left and larger keys right, so a search follows a single root-to-leaf path.",
            ),
            q(
                "What can cause a BST to degrade to O(n) search time?",
                (
                    opt("Using a balanced red-black variant"),
                    opt("Unbalanced inserts that make it behave like a linked list", correct=True),
                    opt("Storing the tree as a flat array"),
                    opt("Searching for a key that is present"),
                ),
                "Unbalanced inserts degrade a BST to O(n), like a linked list; self-balancing trees keep it O(log n).",
            ),
            q(
                "In a heap stored as a flat array, where are the children of the node at index i?",
                (
                    opt("At i-1 and i-2"),
                    opt("At 2i+1 and 2i+2", correct=True),
                    opt("At i/2 and i/2+1"),
                    opt("At 2i and 2i+1"),
                ),
                "The lesson states that for a node at index i, the children are at 2i+1 and 2i+2.",
            ),
        ),
        "Graph traversal: BFS & DFS": (
            q(
                "What is the time complexity of both BFS and DFS on a graph?",
                (
                    opt("O(V log V)"),
                    opt("O(V+E)", correct=True),
                    opt("O(V*E)"),
                    opt("O(V^2)"),
                ),
                "The lesson states both BFS and DFS visit every reachable node in O(V+E).",
            ),
            q(
                "Which data structure does BFS use, and what kind of path does it find?",
                (
                    opt("A stack, finding the deepest path"),
                    opt("A queue, finding the fewest-hops path", correct=True),
                    opt("A heap, finding the cheapest path"),
                    opt("A hash map, finding any path"),
                ),
                "BFS uses a queue and explores in expanding rings, so it finds the fewest-hops path.",
            ),
            q(
                "Which traversal uses a stack or recursion and is good for cycle detection and topological sort?",
                (
                    opt("BFS"),
                    opt("DFS", correct=True),
                    opt("Dijkstra"),
                    opt("Binary search"),
                ),
                "DFS uses a stack or recursion, dives as deep as possible then backtracks, and is great for cycle detection and topological sort.",
            ),
        ),
        "Lab: BFS & DFS on a graph": (
            q(
                "In the lab, how is BFS implemented using a plain list as a queue?",
                (
                    opt("By popping from the front with queue.pop(0)", correct=True),
                    opt("By popping from the end with stack.pop()"),
                    opt("By sorting the list each iteration"),
                    opt("By using recursion instead of a loop"),
                ),
                "The BFS lab uses a list as a queue and pops from the front with queue.pop(0).",
            ),
            q(
                "How does the lab's DFS pop nodes from its list used as a stack?",
                (
                    opt("From the front with pop(0)"),
                    opt("From the end with pop(), iteratively without recursion", correct=True),
                    opt("By recursion on each neighbour"),
                    opt("In sorted order of node label"),
                ),
                "The DFS lab uses a list as a stack, popping from the end with pop(), iteratively with no recursion.",
            ),
            q(
                "According to the lab comments, how do the BFS and DFS orders differ?",
                (
                    opt(
                        "BFS order is by distance from A; DFS plunges down one branch first",
                        correct=True,
                    ),
                    opt("DFS order is by distance from A; BFS dives down one branch first"),
                    opt("Both produce the identical visit order"),
                    opt("BFS visits nodes in alphabetical order only"),
                ),
                "The lab notes that BFS order is by distance from A while DFS plunges down one branch first.",
            ),
        ),
    },
    final=(
        q(
            "Which recurrence and result characterize merge and quick sort?",
            (
                opt("T(n) = 2 T(n/2) + O(n), giving Theta(n log n)", correct=True),
                opt("T(n) = T(n-1) + O(1), giving O(n)"),
                opt("T(n) = T(n/2) + O(1), giving O(log n)"),
                opt("T(n) = 2 T(n) + O(n), giving O(2^n)"),
            ),
            "Divide-and-conquer sorts obey T(n) = 2 T(n/2) + O(n), which the Master theorem solves to Theta(n log n).",
        ),
        q(
            "Which structure gives near-constant average lookup by hashing a key to a bucket?",
            (
                opt("Binary search tree"),
                opt("Hash map", correct=True),
                opt("Heap"),
                opt("Stack"),
            ),
            "A hash map uses a hash function such as key mod m to give O(1) average lookup.",
        ),
        q(
            "Which traversal finds the fewest-hops path and which data structure does it use?",
            (
                opt("DFS, using a queue"),
                opt("BFS, using a queue", correct=True),
                opt("BFS, using a stack"),
                opt("DFS, using a heap"),
            ),
            "BFS uses a queue and explores in expanding rings, finding the fewest-hops path.",
        ),
        q(
            "For a heap stored as a flat array, what are the child indices of node i and its key operation cost?",
            (
                opt("Children at 2i+1 and 2i+2, with insert/extract in O(log n)", correct=True),
                opt("Children at i-1 and i-2, with insert/extract in O(1)"),
                opt("Children at i/2, with insert/extract in O(n)"),
                opt("Children at 2i and 2i+1, with insert/extract in O(n log n)"),
            ),
            "A heap places children at 2i+1 and 2i+2, gives min/max in O(1), and insert/extract in O(log n).",
        ),
        q(
            "What time complexity do both BFS and DFS achieve when traversing a graph?",
            (
                opt("O(V+E)", correct=True),
                opt("O(V*E)"),
                opt("O(V^2)"),
                opt("O(E log V)"),
            ),
            "Both BFS and DFS visit every reachable node in O(V+E).",
        ),
    ),
)
