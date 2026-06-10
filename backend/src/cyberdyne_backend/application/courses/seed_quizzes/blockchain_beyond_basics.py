"""Curated quiz questions for the 'Blockchain: Beyond the Basics' course
(per-lesson checkpoints plus a final comprehensive quiz). Keys are the EXACT
content-lesson titles; every question is answerable from the lesson body."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Bitcoin Script": (
            q(
                "How does Bitcoin represent the coins you can spend?",
                (
                    opt("As account balances stored per address"),
                    opt("As coins (UTXOs) locked by a tiny program", correct=True),
                    opt("As entries in a central bank ledger"),
                    opt("As smart contracts holding ETH"),
                ),
                "Bitcoin has no balances; it has coins (UTXOs) each locked by a tiny program you must satisfy to spend.",
            ),
            q(
                "Why is Bitcoin Script deliberately not Turing-complete?",
                (
                    opt(
                        "So validation always terminates and cannot hang the network", correct=True
                    ),
                    opt("So it can run infinite loops for richer logic"),
                    opt("So only miners can read the scripts"),
                    opt("So contracts can call other contracts"),
                ),
                "Without loops or recursion, script validation always terminates and cannot hang the network.",
            ),
            q(
                "In P2PKH, what does the unlocking script (scriptSig) provide?",
                (
                    opt("OP_DUP OP_HASH160 and the public-key hash"),
                    opt("The signature and the public key", correct=True),
                    opt("Only the miner's address"),
                    opt("The full private key in plaintext"),
                ),
                "The scriptSig supplies the signature and the public key, while the scriptPubKey holds the puzzle opcodes.",
            ),
        ),
        "Run a Bitcoin Script (toy)": (
            q(
                "When does the toy evaluator consider a script to have succeeded?",
                (
                    opt("When the stack is empty at the end"),
                    opt("When it ends with a single truthy value on the stack", correct=True),
                    opt("When OP_ADD is the last token"),
                    opt("When two values remain on the stack"),
                ),
                "The script succeeds only if it ends with exactly one truthy (non-zero) value on the stack.",
            ),
            q(
                "What does OP_EQUALVERIFY do in the toy evaluator?",
                (
                    opt("Duplicates the top stack item"),
                    opt("Adds the top two stack items together"),
                    opt("Pops two values and raises an error if they are not equal", correct=True),
                    opt("Pushes a number literal onto the stack"),
                ),
                "OP_EQUALVERIFY pops two values and raises a ValueError when they differ, marking the script invalid.",
            ),
            q(
                "In the evaluator, what happens to a token that is not a known opcode?",
                (
                    opt("It is pushed onto the stack as an integer literal", correct=True),
                    opt("It is ignored and skipped"),
                    opt("It immediately ends the script as invalid"),
                    opt("It duplicates the top of the stack"),
                ),
                "Any token that is not an opcode is treated as a number literal and pushed onto the stack via int(token).",
            ),
        ),
        "Consensus & its types": (
            q(
                "What does consensus let blockchain nodes do?",
                (
                    opt("Agree on the next block without a central authority", correct=True),
                    opt("Encrypt every transaction with a private key"),
                    opt("Store coins as UTXOs instead of balances"),
                    opt("Compile Solidity contracts to bytecode"),
                ),
                "Consensus is the rule that lets thousands of nodes agree on the next block without a central authority.",
            ),
            q(
                "In Proof of Stake, who may add a block?",
                (
                    opt("The first node to solve a hash puzzle"),
                    opt("A validator chosen by stake", correct=True),
                    opt("A known, approved set of validators only"),
                    opt("A delegate that token-holders vote in"),
                ),
                "In PoS a validator is chosen by stake, in contrast to PoW where the first to solve a hash puzzle wins.",
            ),
            q(
                "What extra deterrent does Proof of Stake add against attacks?",
                (
                    opt("It burns more energy than Proof of Work"),
                    opt(
                        "Slashing, where misbehaving validators lose part of their stake",
                        correct=True,
                    ),
                    opt("It requires 51 percent of hash power"),
                    opt("It removes the need for finality"),
                ),
                "PoS adds slashing so misbehaving validators lose part of their stake, making attacks costly without burning energy.",
            ),
        ),
        "Cold wallets & self-custody": (
            q(
                "What do you actually hold when you own cryptocurrency?",
                (
                    opt("The coins themselves stored in your wallet app"),
                    opt(
                        "The private key that authorizes spending the on-chain coins", correct=True
                    ),
                    opt("A copy of the entire blockchain"),
                    opt("A signed certificate from an exchange"),
                ),
                "Coins live on-chain; what you hold is the private key that authorizes spending them.",
            ),
            q(
                "How does a hardware wallet keep the private key safe when signing?",
                (
                    opt("It uploads the key to the exchange for signing"),
                    opt(
                        "It signs on the device so only the signature returns and the key never leaves it",
                        correct=True,
                    ),
                    opt("It emails the signed transaction to the network"),
                    opt("It stores the key on the laptop for speed"),
                ),
                "The transaction goes to the device, you confirm on its screen, and only the signature comes back; the key never leaves.",
            ),
            q(
                "What is the correct way to back up a BIP-39 seed phrase?",
                (
                    opt("Save a photo of it in cloud storage"),
                    opt("Keep it in a password manager"),
                    opt(
                        "Write it on paper or steel and store copies in separate secure places",
                        correct=True,
                    ),
                    opt("Share it with your exchange support team"),
                ),
                "The seed phrase should be written on paper or steel with copies in separate secure places, never a photo or cloud note.",
            ),
        ),
        "Ethereum": (
            q(
                "How does Ethereum track funds compared with Bitcoin?",
                (
                    opt("It uses UTXOs like Bitcoin"),
                    opt("It keeps running balances in accounts", correct=True),
                    opt("It does not track funds at all"),
                    opt("It stores balances only on hardware wallets"),
                ),
                "Ethereum keeps running balances in accounts, closer to a bank ledger, rather than tracking unspent outputs.",
            ),
            q(
                "What is the purpose of gas on Ethereum?",
                (
                    opt("To encrypt smart contract source code"),
                    opt("To compensate validators and stop infinite loops", correct=True),
                    opt("To set a hard cap on the ETH supply"),
                    opt("To convert EOAs into contract accounts"),
                ),
                "Gas compensates validators and stops infinite loops; running out of gas reverts the transaction.",
            ),
            q(
                "What are the two kinds of Ethereum accounts?",
                (
                    opt(
                        "EOAs controlled by a private key and contract accounts controlled by code",
                        correct=True,
                    ),
                    opt("Hot accounts and cold accounts"),
                    opt("UTXO accounts and balance accounts"),
                    opt("Mining accounts and staking accounts"),
                ),
                "Ethereum has EOAs controlled by a private key (people) and contract accounts controlled by their code.",
            ),
        ),
        "Solidity": (
            q(
                "What does a Solidity contract resemble in structure?",
                (
                    opt(
                        "A class with persistent state and functions that read or change it",
                        correct=True,
                    ),
                    opt("A flat list of UTXOs"),
                    opt("A stack machine with no state"),
                    opt("A seed phrase of 12 or 24 words"),
                ),
                "A Solidity contract is much like a class: it has persistent on-chain state and functions that read or change it.",
            ),
            q(
                "Why does a view function cost no gas when called externally?",
                (
                    opt("Because it receives ETH directly"),
                    opt("Because it only reads state and does not change it", correct=True),
                    opt("Because it is marked payable"),
                    opt("Because it runs off-chain on the laptop"),
                ),
                "A view function only reads state, so it costs no gas when called externally, unlike functions that change state.",
            ),
            q(
                "What is the recommended defense against the reentrancy bug?",
                (
                    opt("Make every function payable"),
                    opt("Skip auditing to deploy faster"),
                    opt(
                        "Follow checks-effects-interactions: validate, update state, then make external calls",
                        correct=True,
                    ),
                    opt("Call out to other contracts before updating state"),
                ),
                "Checks-effects-interactions means validate inputs, update your own state, and only then make external calls.",
            ),
        ),
    },
    final=(
        q(
            "Which statement correctly contrasts the Bitcoin and Ethereum models?",
            (
                opt("Both use the UTXO model"),
                opt("Bitcoin uses UTXOs while Ethereum uses account balances", correct=True),
                opt("Bitcoin uses account balances while Ethereum uses UTXOs"),
                opt("Neither tracks funds on-chain"),
            ),
            "Bitcoin tracks unspent outputs (UTXOs) while Ethereum keeps running balances in accounts.",
        ),
        q(
            "How does Proof of Work finality differ from BFT-style finality?",
            (
                opt(
                    "PoW is probabilistic and gets safer with more blocks, while BFT is deterministic once validators vote",
                    correct=True,
                ),
                opt("PoW is deterministic while BFT is probabilistic"),
                opt("Both provide instant deterministic finality"),
                opt("Neither type of consensus offers any finality"),
            ),
            "PoW finality is probabilistic and strengthens as blocks pile on, while BFT finality is deterministic once validators vote.",
        ),
        q(
            "Why must Bitcoin Script avoid loops and recursion?",
            (
                opt("To let contracts call other contracts like money-legos"),
                opt("So validation always terminates and cannot hang the network", correct=True),
                opt("So scripts can run forever for security"),
                opt("To make every coin a smart contract"),
            ),
            "Bitcoin Script is intentionally not Turing-complete so validation always terminates and cannot hang the network.",
        ),
        q(
            "What is the core idea of self-custody with a cold wallet?",
            (
                opt("The exchange holds your keys for convenience"),
                opt(
                    "You control the private key offline, gaining total control and total responsibility",
                    correct=True,
                ),
                opt("Your coins are stored inside the hardware device"),
                opt("The seed phrase should be saved as a cloud photo"),
            ),
            "Self-custody means you hold the private key (kept offline on a cold wallet): total control and total responsibility.",
        ),
        q(
            "What does gas accomplish on the Ethereum Virtual Machine?",
            (
                opt(
                    "It compensates validators and stops infinite loops by reverting when exhausted",
                    correct=True,
                ),
                opt("It caps the total ETH supply"),
                opt("It encrypts the seed phrase"),
                opt("It converts probabilistic finality to deterministic finality"),
            ),
            "Gas paid in ETH compensates validators and stops infinite loops; running out of gas reverts the transaction.",
        ),
    ),
)
