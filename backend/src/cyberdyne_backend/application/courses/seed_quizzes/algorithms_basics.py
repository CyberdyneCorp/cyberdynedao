"""Curated quiz questions for the Algorithms - Basics course. Keys are the
EXACT content-lesson titles; the seed interleaves a checkpoint quiz after each
content lesson plus a final comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Complexity & Big-O": (
            q(
                "What does an algorithm's time complexity describe?",
                (
                    opt("How much memory the program allocates at startup"),
                    opt(
                        "How its work grows with the input size n, independent of the machine",
                        correct=True,
                    ),
                    opt("The exact number of seconds it runs on a given laptop"),
                    opt("How many lines of source code the algorithm contains"),
                ),
                "Time complexity says how the work grows with the input size n, independent of the machine.",
            ),
            q(
                "What does Big-O notation keep when describing growth?",
                (
                    opt("Only the dominant term, dropping constants", correct=True),
                    opt("Every term and every constant factor exactly"),
                    opt("The best case running time only"),
                    opt("The amount of memory used per operation"),
                ),
                "Big-O keeps only the dominant term and usually ignores constants.",
            ),
            q(
                "Which case does Big-O analysis usually care about as the guarantee?",
                (
                    opt("The best case"),
                    opt("The average case across random inputs"),
                    opt("The worst case", correct=True),
                    opt("The case with the smallest input"),
                ),
                "We care about the worst case because it is the guarantee.",
            ),
        ),
        "Searching: linear vs binary": (
            q(
                "What is the time complexity of linear search, which scans every element?",
                (
                    opt("O(log n)"),
                    opt("O(1)"),
                    opt("O(n)", correct=True),
                    opt("O(n^2)"),
                ),
                "Linear search scans every element, so it is O(n).",
            ),
            q(
                "What does binary search require of the array before it can be used?",
                (
                    opt("The array must be sorted", correct=True),
                    opt("The array must contain only unique values"),
                    opt("The array must be stored as a linked list"),
                    opt("The array must have a power-of-two length"),
                ),
                "Binary search works only on a sorted array, checking the middle and discarding half each step.",
            ),
            q(
                "At most how many comparisons does binary search need for 16 elements?",
                (
                    opt("16"),
                    opt("8"),
                    opt("4", correct=True),
                    opt("1"),
                ),
                "16 elements take at most 4 comparisons because log2 of 16 is 4.",
            ),
        ),
        "Elementary sorting": (
            q(
                "What is the time complexity of the simple sorts such as bubble, insertion, and selection?",
                (
                    opt("O(n log n)"),
                    opt("O(n^2)", correct=True),
                    opt("O(log n)"),
                    opt("O(n)"),
                ),
                "Bubble, insertion, and selection sort are all O(n^2).",
            ),
            q(
                "What does the stability property of a sort mean?",
                (
                    opt("Equal keys keep their original relative order", correct=True),
                    opt("The sort never crashes on large inputs"),
                    opt("The sort uses no extra memory"),
                    opt("The sort always runs in O(n log n) time"),
                ),
                "Stability means equal keys keep their original order after sorting.",
            ),
            q(
                "What does it mean for a sort to be in-place?",
                (
                    opt("It keeps equal keys in their original order"),
                    opt("It uses no extra memory", correct=True),
                    opt("It only works on already-sorted data"),
                    opt("It guarantees O(n log n) comparisons"),
                ),
                "An in-place sort uses no extra memory.",
            ),
        ),
        "Recursion": (
            q(
                "What stops a recursive function from calling itself forever?",
                (
                    opt("The call stack"),
                    opt("The base case", correct=True),
                    opt("The recursive case"),
                    opt("Memoization"),
                ),
                "A recursive function stops at the base case.",
            ),
            q(
                "Roughly what is the cost of naive fib(n) defined as fib(n-1) + fib(n-2)?",
                (
                    opt("O(n)"),
                    opt("O(log n)"),
                    opt("O(2^n)", correct=True),
                    opt("O(n^2)"),
                ),
                "Naive fib re-computes the same calls and branches exponentially, about O(2^n).",
            ),
            q(
                "What does memoizing the naive Fibonacci recursion reduce its cost to?",
                (
                    opt("O(n)", correct=True),
                    opt("O(2^n)"),
                    opt("O(n^2)"),
                    opt("O(1)"),
                ),
                "Memoizing caches results and collapses the cost to O(n).",
            ),
        ),
        "Lab: binary search & insertion sort": (
            q(
                "In the lab, what does the variable comparisons count during the insertion sort?",
                (
                    opt(
                        "The number of times an element is shifted while greater than the key",
                        correct=True,
                    ),
                    opt("The number of elements in the array"),
                    opt("The number of steps the binary search takes"),
                    opt("The final sorted index of the target"),
                ),
                "comparisons is incremented inside the while loop each time a[j] > key, counting the shifts.",
            ),
            q(
                "In the lab, what runs first before the binary search executes?",
                (
                    opt("The binary search runs first, then the array is sorted"),
                    opt("The insertion sort sorts the array in place", correct=True),
                    opt("A recursive Fibonacci is computed"),
                    opt("The array is reversed"),
                ),
                "The lab runs insertion sort in place first, then binary searches the now-sorted array.",
            ),
            q(
                "In the lab, what value does found keep if the target is absent?",
                (
                    opt("0"),
                    opt("-1", correct=True),
                    opt("The array length"),
                    opt("The last index searched"),
                ),
                "found is initialized to -1 and stays -1 when the target is not found.",
            ),
        ),
    },
    final=(
        q(
            "Which growth rate is fastest (worst) as n becomes large?",
            (
                opt("O(log n)"),
                opt("O(n)"),
                opt("O(n log n)"),
                opt("O(2^n)", correct=True),
            ),
            "Exponential O(2^n) grows the fastest and is the worst of the listed orders.",
        ),
        q(
            "Which search achieves O(log n) by discarding half the candidates each step?",
            (
                opt("Linear search"),
                opt("Binary search", correct=True),
                opt("Bubble sort"),
                opt("Depth-first search"),
            ),
            "Binary search checks the middle and throws away half the candidates each step, giving O(log n).",
        ),
        q(
            "Which sorts run in O(n^2), making them slower than the O(n log n) sorts?",
            (
                opt("Bubble, insertion, and selection sort", correct=True),
                opt("Merge and quick sort"),
                opt("Binary and linear search"),
                opt("Dijkstra and Bellman-Ford"),
            ),
            "The elementary sorts (bubble, insertion, selection) are O(n^2).",
        ),
        q(
            "What does memoization do for an exponential recursion like naive Fibonacci?",
            (
                opt("It removes the base case entirely"),
                opt("It caches results, collapsing O(2^n) to O(n)", correct=True),
                opt("It makes the recursion use more memory than time"),
                opt("It converts the function into a quadratic O(n^2) sort"),
            ),
            "Memoization caches subresults so each is computed once, collapsing O(2^n) to O(n).",
        ),
        q(
            "What property must an array have for binary search to work correctly?",
            (
                opt("It must be sorted", correct=True),
                opt("It must be a power of two in length"),
                opt("It must contain only positive numbers"),
                opt("It must be stored as a stack"),
            ),
            "Binary search requires a sorted array so it can discard half the range each step.",
        ),
    ),
)
