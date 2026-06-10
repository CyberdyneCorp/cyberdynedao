from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is a blockchain?": (
            q(
                "How is a blockchain described as a distributed ledger?",
                (
                    opt("A single database stored only on one trusted central server"),
                    opt(
                        "A database that many computers keep a copy of, agreeing on the same history without a central authority",
                        correct=True,
                    ),
                    opt("A spreadsheet that a bank edits on behalf of its customers"),
                    opt("A private file that only miners are allowed to read"),
                ),
                "A blockchain is a distributed ledger where many computers hold the same history and agree without trusting a central authority.",
            ),
            q(
                "What problem does a blockchain solve for digital money?",
                (
                    opt("Slow internet connections between banks"),
                    opt("The high cost of printing paper currency"),
                    opt(
                        "Double-spending, where the same coin could be copied and paid to two people",
                        correct=True,
                    ),
                    opt("Forgetting your account password"),
                ),
                "Because digital money is just data that can be copied, a blockchain prevents double-spending by having everyone agree which transaction came first.",
            ),
            q(
                "According to the lesson, why do you store only small things like amounts and hashes on a blockchain?",
                (
                    opt("Because every write costs money in the form of a gas fee", correct=True),
                    opt("Because the kernel cannot read large files"),
                    opt("Because reading is slow but writing is free"),
                    opt("Because files must always be encrypted first"),
                ),
                "Every write costs a gas fee, so you store small things like amounts, hashes, and short strings rather than files.",
            ),
        ),
        "Hashing & blocks": (
            q(
                "Which hash function does Bitcoin use as described in the lesson?",
                (
                    opt("MD5"),
                    opt("SHA-256", correct=True),
                    opt("CRC32"),
                    opt("Base64"),
                ),
                "The lesson states Bitcoin uses SHA-256 to turn any input into a fixed-size fingerprint.",
            ),
            q(
                "What does the avalanche property of a hash function mean?",
                (
                    opt("The same input always produces the same hash"),
                    opt("You can reverse the hash back into its input"),
                    opt(
                        "Change one character and the hash looks completely different", correct=True
                    ),
                    opt("The hash grows longer as the input grows longer"),
                ),
                "Avalanche means changing one character of the input makes the resulting hash look completely different.",
            ),
            q(
                "Why does editing Block 1 break every block after it?",
                (
                    opt("Because the timestamp field is recalculated for the whole chain"),
                    opt(
                        "Because each block includes the previous block's hash, so a changed hash no longer matches",
                        correct=True,
                    ),
                    opt("Because miners delete blocks that have been edited"),
                    opt("Because the nonce is shared across all blocks at once"),
                ),
                "Each block includes the previous block's hash, so editing a block changes its hash and the next block's previous-hash no longer matches, breaking the chain.",
            ),
        ),
        "Consensus & Proof of Work": (
            q(
                "In Proof of Work, what are miners searching for?",
                (
                    opt("A previous hash that matches the genesis block"),
                    opt(
                        "A nonce that makes the block's hash fall below a target, such as starting with N zeros",
                        correct=True,
                    ),
                    opt("A validator chosen by the size of their stake"),
                    opt("A timestamp that is earlier than all other blocks"),
                ),
                "Miners race to find a nonce that makes the block hash fall below a target, in practice starting with N zeros.",
            ),
            q(
                "What asymmetry makes Proof of Work secure?",
                (
                    opt("Finding the nonce is hard but checking it is instant", correct=True),
                    opt("Finding the nonce is instant but checking it is hard"),
                    opt("Both finding and checking the nonce are equally hard"),
                    opt("Neither finding nor checking the nonce requires any work"),
                ),
                "Finding the nonce takes lots of guessing while verifying it is a single instant hash, and that asymmetry secures the chain.",
            ),
            q(
                "Compared with Proof of Work, what is true of Proof of Stake?",
                (
                    opt("It uses very high energy and is used by Bitcoin"),
                    opt("It picks the writer as the first to solve a hash puzzle"),
                    opt("It uses low energy and chooses a validator by stake", correct=True),
                    opt("It requires controlling 51% of the hash power to attack"),
                ),
                "The lesson's table shows Proof of Stake uses low energy and selects a validator chosen by stake, unlike Proof of Work.",
            ),
        ),
        "Mine a block (toy example)": (
            q(
                "What does the variable named zeros control in the toy miner?",
                (
                    opt("The number of transactions in the block"),
                    opt("The difficulty: more zeros means more work", correct=True),
                    opt("The reward paid to the miner"),
                    opt("The length of the block hash in characters"),
                ),
                "The lesson sets zeros as the difficulty, where more required leading zeros means more work.",
            ),
            q(
                "How does the toy miner find a valid nonce?",
                (
                    opt("It picks a random nonce once and accepts whatever hash results"),
                    opt(
                        "It increments the nonce in a loop until the digest starts with the target zeros",
                        correct=True,
                    ),
                    opt("It reverses the target hash to compute the nonce directly"),
                    opt("It asks the network to supply the correct nonce"),
                ),
                "The code loops, incrementing nonce and rehashing until the digest startswith the target string of zeros.",
            ),
            q(
                "What does the comment say about the toy_hash function compared with real Bitcoin?",
                (
                    opt("It is more secure than SHA-256"),
                    opt(
                        "It is a tiny teaching hash that is not secure, while real Bitcoin uses SHA-256",
                        correct=True,
                    ),
                    opt("It is the exact hash Bitcoin uses in production"),
                    opt("It cannot produce leading zeros at all"),
                ),
                "The comment notes toy_hash is a tiny teaching hash that is not secure, whereas real Bitcoin uses SHA-256.",
            ),
        ),
        "Bitcoin": (
            q(
                "Who launched Bitcoin and in what year?",
                (
                    opt("Vitalik Buterin in 2015"),
                    opt("The pseudonymous Satoshi Nakamoto in 2009", correct=True),
                    opt("A consortium of banks in 2009"),
                    opt("Satoshi Nakamoto in 2140"),
                ),
                "Bitcoin was launched in 2009 by the pseudonymous Satoshi Nakamoto as a peer-to-peer electronic cash system.",
            ),
            q(
                "What is Bitcoin's maximum supply?",
                (
                    opt("Unlimited, growing with demand"),
                    opt("21 million, a fixed cap", correct=True),
                    opt("210,000 coins"),
                    opt("100 million satoshis"),
                ),
                "Bitcoin has a fixed maximum supply of 21 million, which creates digital scarcity.",
            ),
            q(
                "In the UTXO model, how does a Bitcoin wallet hold value?",
                (
                    opt("As an account balance updated by the bank"),
                    opt(
                        "As Unspent Transaction Outputs that are consumed whole as inputs",
                        correct=True,
                    ),
                    opt("As a single number stored on a central server"),
                    opt("As staked tokens earning interest"),
                ),
                "Bitcoin does not store balances; a wallet owns Unspent Transaction Outputs that are consumed whole as inputs, creating new outputs.",
            ),
        ),
    },
    final=(
        q(
            "Which statement best captures what a blockchain is?",
            (
                opt("A central server owned by a bank that records all payments"),
                opt(
                    "A distributed ledger many computers copy and agree on without a central authority",
                    correct=True,
                ),
                opt("A single offline file that stores money as plain text"),
                opt("A graphical app that prints new coins on demand"),
            ),
            "A blockchain is a distributed ledger that many computers copy and agree on without trusting a central authority.",
        ),
        q(
            "Why is tampering with an old block detectable?",
            (
                opt(
                    "Because each block embeds the previous block's hash, so a change breaks every later block",
                    correct=True,
                ),
                opt("Because the bank reviews every block before it is added"),
                opt("Because the nonce is encrypted with a private key"),
                opt("Because blocks store their data only in plain text"),
            ),
            "Each block includes the previous block's hash, so altering a block changes its hash and breaks the link to every block after it.",
        ),
        q(
            "What must an attacker control to rewrite history under Proof of Work?",
            (
                opt("More than 50% of the network's hash power", correct=True),
                opt("The single trusted middleman's private key"),
                opt("More than half of all UTXOs in existence"),
                opt("The genesis block's timestamp"),
            ),
            "A 51% attack requires controlling more than half the network's hash power to out-mine everyone else.",
        ),
        q(
            "Which property does Bitcoin's 21 million cap create?",
            (
                opt("Unlimited money printing"),
                opt("Digital scarcity with a fixed supply", correct=True),
                opt("A guaranteed yearly interest rate"),
                opt("A reliance on a central bank"),
            ),
            "The fixed 21 million cap creates digital scarcity because no new money can be printed beyond it.",
        ),
        q(
            "What makes Proof of Work hashing effective for securing the chain?",
            (
                opt("Finding a valid nonce is hard while verifying it is instant", correct=True),
                opt("Both finding and verifying a nonce take the same long time"),
                opt("Hashes can be reversed to recover the original input"),
                opt("The same input can produce many different hashes"),
            ),
            "Proof of Work relies on the asymmetry that finding a valid nonce is hard but checking it is a single instant hash.",
        ),
    ),
)
