"""Curated quiz questions for the Algorithms - Advanced course (per-lesson
checkpoints + a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each one."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Greedy algorithms": (
            q(
                "When is a greedy algorithm provably optimal according to the lesson?",
                (
                    opt("Whenever it runs faster than dynamic programming"),
                    opt(
                        "When the problem has the greedy-choice property and optimal substructure",
                        correct=True,
                    ),
                    opt("Only when all inputs are sorted in advance"),
                    opt("When the problem has overlapping subproblems"),
                ),
                "Greedy is provably optimal only when the problem has the greedy-choice property and optimal substructure.",
            ),
            q(
                "In activity selection, which greedy rule is optimal?",
                (
                    opt("Always take the activity that starts earliest"),
                    opt("Always take the shortest activity"),
                    opt("Always take the next activity that finishes earliest", correct=True),
                    opt("Always take the activity with the fewest overlaps"),
                ),
                "The optimal rule is to always take the next activity that finishes earliest, leaving room for more later.",
            ),
            q(
                "On which problems does the lesson say greedy fails, requiring dynamic programming instead?",
                (
                    opt("Arbitrary coin systems or 0/1 knapsack", correct=True),
                    opt("Minimum spanning trees built by Kruskal or Prim"),
                    opt("Huffman coding of symbols"),
                    opt("Dijkstra shortest paths"),
                ),
                "Greedy fails on arbitrary coin systems or the 0/1 knapsack, where dynamic programming is needed.",
            ),
        ),
        "Dynamic programming": (
            q(
                "Which two properties must a problem have for dynamic programming to apply?",
                (
                    opt("Greedy-choice property and non-negative weights"),
                    opt("Overlapping subproblems and optimal substructure", correct=True),
                    opt("Polynomial time and bounded recursion depth"),
                    opt("Sorted input and a single base case"),
                ),
                "DP applies to problems with overlapping subproblems and optimal substructure, solving each subproblem once.",
            ),
            q(
                "What are the two DP styles named in the lesson?",
                (
                    opt("Recursion and iteration"),
                    opt(
                        "Memoization (top-down cache) and tabulation (bottom-up fill)", correct=True
                    ),
                    opt("Divide and conquer and backtracking"),
                    opt("Relaxation and settling"),
                ),
                "The two styles are memoization, a top-down cache, and tabulation, a bottom-up fill of a table.",
            ),
            q(
                "Which of these is listed as a famous dynamic programming problem?",
                (
                    opt("Breadth-first search"),
                    opt("Activity selection"),
                    opt("Longest common subsequence", correct=True),
                    opt("Hashing with key mod m"),
                ),
                "Longest common subsequence (used in diff tools) is listed among the famous DPs.",
            ),
        ),
        "Shortest paths: Dijkstra & Bellman-Ford": (
            q(
                "What is the core operation shared by shortest-path algorithms?",
                (
                    opt(
                        "Relaxation: update the distance to v if going through u improves it",
                        correct=True,
                    ),
                    opt("Partitioning the graph around a pivot node"),
                    opt("Hashing each node into a bucket"),
                    opt("Memoizing the distance table top-down"),
                ),
                "The core operation is relaxation: if going through u improves the distance to v, update it.",
            ),
            q(
                "What requirement does Dijkstra impose that Bellman-Ford does not?",
                (
                    opt("The graph must be undirected"),
                    opt("Edge weights must be non-negative", correct=True),
                    opt("The graph must contain a negative cycle"),
                    opt("All edges must have equal weight"),
                ),
                "Dijkstra needs non-negative weights, while Bellman-Ford handles negative weights and detects negative cycles.",
            ),
            q(
                "Which data structure lets Dijkstra repeatedly settle the nearest unsettled node?",
                (
                    opt("A hash map"),
                    opt("A binary search tree"),
                    opt("A priority queue / heap", correct=True),
                    opt("A FIFO queue"),
                ),
                "Dijkstra uses a priority queue / heap to repeatedly settle the nearest unsettled node.",
            ),
        ),
        "Complexity classes: P, NP & intractability": (
            q(
                "How does the lesson define the class NP?",
                (
                    opt("Problems solvable in polynomial time"),
                    opt(
                        "Problems where a proposed solution can be verified in polynomial time",
                        correct=True,
                    ),
                    opt("Problems that require factorial time to solve"),
                    opt("Problems with no known verification method"),
                ),
                "NP is the class where a proposed solution can be verified in polynomial time.",
            ),
            q(
                "What is true of NP-complete problems like travelling salesman or SAT?",
                (
                    opt("They are the easiest problems in P"),
                    opt("A fast algorithm for one would crack them all", correct=True),
                    opt("They can always be solved greedily"),
                    opt("They are verifiable only in exponential time"),
                ),
                "NP-complete problems are the hardest in NP; a fast algorithm for one would crack them all.",
            ),
            q(
                "What practical approaches does the lesson recommend for NP-hard problems?",
                (
                    opt(
                        "Heuristics, approximation algorithms, and solvers like SAT/ILP",
                        correct=True,
                    ),
                    opt("Always running brute force over all n items"),
                    opt("Switching the input to a sorted order"),
                    opt("Refusing to solve them at all"),
                ),
                "In practice we use heuristics, approximation algorithms, and SAT/ILP solvers, trading guaranteed optimality for tractable runtime.",
            ),
        ),
        "Lab: Dijkstra's shortest paths": (
            q(
                "In the lab, how is the weighted graph represented?",
                (
                    opt("As a matrix of all pairwise distances"),
                    opt(
                        "As an adjacency list mapping each node to a list of (neighbour, weight) pairs",
                        correct=True,
                    ),
                    opt("As a binary heap of edges"),
                    opt("As a flat array indexed by node number"),
                ),
                "The lab stores the graph as an adjacency list: each node maps to a list of (neighbour, weight) pairs.",
            ),
            q(
                "What does each iteration of the main loop do after selecting node u?",
                (
                    opt("Marks u done, then relaxes its outgoing edges", correct=True),
                    opt("Removes u from the graph entirely"),
                    opt("Pushes all of u's neighbours onto a stack"),
                    opt("Resets every distance back to INF"),
                ),
                "Each step settles the nearest unsettled node u (marks it done) and then relaxes its edges.",
            ),
            q(
                "According to the lab, what is the settle order produced from start A?",
                (
                    opt("A, B, C, D, E, F"),
                    opt("A, C, B, D, E, F", correct=True),
                    opt("A, B, D, F, E, C"),
                    opt("F, E, D, C, B, A"),
                ),
                "The lab notes the settle order is A, C, B, D, E, F - by increasing distance from A.",
            ),
        ),
    },
    final=(
        q(
            "Which design technique solves overlapping subproblems by storing each result once?",
            (
                opt("Greedy"),
                opt("Dynamic programming", correct=True),
                opt("Divide and conquer"),
                opt("Brute force"),
            ),
            "Dynamic programming solves overlapping subproblems once and stores the results, turning exponential recursion into polynomial time.",
        ),
        q(
            "Which shortest-path algorithm requires non-negative edge weights?",
            (
                opt("Bellman-Ford"),
                opt("Dijkstra", correct=True),
                opt("Breadth-first search"),
                opt("Floyd-Warshall"),
            ),
            "Dijkstra requires non-negative weights, whereas Bellman-Ford can handle negative weights.",
        ),
        q(
            "What greedy rule optimally solves activity selection?",
            (
                opt("Pick the activity that finishes earliest", correct=True),
                opt("Pick the longest activity"),
                opt("Pick the activity that starts latest"),
                opt("Pick the activity with the most overlaps"),
            ),
            "Choosing the next activity that finishes earliest is the optimal greedy rule for activity selection.",
        ),
        q(
            "What does the P vs NP question ask?",
            (
                opt("Whether every problem can be brute-forced in factorial time"),
                opt(
                    "Whether problems verifiable in polynomial time can also be solved in polynomial time",
                    correct=True,
                ),
                opt("Whether greedy always beats dynamic programming"),
                opt("Whether Dijkstra is faster than Bellman-Ford"),
            ),
            "P vs NP asks whether every problem whose solution can be verified quickly (NP) can also be solved quickly (P).",
        ),
        q(
            "Why does brute force fail on NP-hard problems as input size grows?",
            (
                opt("It runs in O(n log n) time"),
                opt("It needs O(2^n) or O(n!) operations, a wall hit fast", correct=True),
                opt("It always returns the wrong answer"),
                opt("It requires non-negative edge weights"),
            ),
            "Brute force over n items costs O(2^n) or O(n!), which explodes quickly - at n=20, n! already exceeds 10^18.",
        ),
    ),
)
