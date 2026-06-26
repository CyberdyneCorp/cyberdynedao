"""Quiz questions for the Scientific Computing & Linux - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why Linux and the shell for science": (
            q(
                "Why is the shell preferred over a GUI for reproducible science?",
                (
                    opt("Every action is text that can be saved, shared and re-run", correct=True),
                    opt("It uses less electricity"),
                    opt("It cannot make mistakes"),
                    opt("It runs only on supercomputers"),
                ),
                "Text commands are recordable and repeatable, the basis of reproducibility.",
            ),
            q(
                "In `ls -l -h /data`, what is `-h`?",
                (
                    opt("A flag (option) modifying the command", correct=True),
                    opt("The program name"),
                    opt("A required argument"),
                    opt("A pipe"),
                ),
                "Flags begin with a dash and modify behaviour; here -h means human-readable.",
            ),
            q(
                "What does the Unix philosophy favour?",
                (
                    opt("Small programs that do one thing well, composed together", correct=True),
                    opt("One large program that does everything"),
                    opt("Proprietary closed tools"),
                    opt("Avoiding the command line entirely"),
                ),
                "Unix composes small focused tools via pipes.",
            ),
        ),
        "The filesystem and navigation": (
            q(
                "What does `..` refer to?",
                (
                    opt("The parent directory", correct=True),
                    opt("The current directory"),
                    opt("Your home directory"),
                    opt("The root directory"),
                ),
                "`.` is here, `..` is the parent, `~` is home.",
            ),
            q(
                "Which path is absolute?",
                (
                    opt("/home/ana/data", correct=True),
                    opt("../results"),
                    opt("data/reads.fq"),
                    opt("./script.sh"),
                ),
                "Absolute paths start at the root `/`.",
            ),
            q(
                "What does `cd` with no argument do?",
                (
                    opt("Returns to your home directory", correct=True),
                    opt("Goes to the root /"),
                    opt("Deletes the current directory"),
                    opt("Lists files"),
                ),
                "Bare `cd` takes you home (~).",
            ),
        ),
        "Files: create, copy, move, remove": (
            q(
                "Why is `rm` dangerous?",
                (
                    opt("It deletes permanently with no recycle bin", correct=True),
                    opt("It always needs sudo"),
                    opt("It renames files unexpectedly"),
                    opt("It only works on directories"),
                ),
                "Removed files are gone; there is no trash.",
            ),
            q(
                "Which glob matches all gzipped FASTQ files?",
                (
                    opt("*.fastq.gz", correct=True),
                    opt("?.fastq.gz"),
                    opt("fastq"),
                    opt("[fastq].gz"),
                ),
                "`*` matches any string, so *.fastq.gz matches them all.",
            ),
            q(
                "Which command renames a file?",
                (
                    opt("mv old.txt new.txt", correct=True),
                    opt("cp old.txt new.txt"),
                    opt("rm old.txt"),
                    opt("touch new.txt"),
                ),
                "mv both moves and renames.",
            ),
        ),
        "Permissions and ownership": (
            q(
                "What does the permission digit 7 mean for a class?",
                (
                    opt("read, write and execute (rwx)", correct=True),
                    opt("read only"),
                    opt("no permissions"),
                    opt("execute only"),
                ),
                "7 = 4+2+1 = rwx.",
            ),
            q(
                "For a directory, what does the execute (x) bit allow?",
                (
                    opt("Entering (traversing) the directory", correct=True),
                    opt("Running the directory as a program"),
                    opt("Deleting all files in it"),
                    opt("Nothing for directories"),
                ),
                "On a directory, x grants the right to enter it.",
            ),
            q(
                "What permission should an SSH private key have?",
                (
                    opt("600 (owner read/write only)", correct=True),
                    opt("777 (everyone everything)"),
                    opt("755"),
                    opt("644 with group read"),
                ),
                "SSH refuses overly open private keys; 600 is required.",
            ),
        ),
        "Pipes, redirection and text tools": (
            q(
                "What does the pipe `|` do?",
                (
                    opt("Feeds one program's stdout into the next's stdin", correct=True),
                    opt("Writes output to a file"),
                    opt("Runs two programs sequentially with no data flow"),
                    opt("Comments out a line"),
                ),
                "A pipe connects stdout to stdin.",
            ),
            q(
                "Which redirection appends stdout to a file?",
                (
                    opt(">>", correct=True),
                    opt(">"),
                    opt("2>"),
                    opt("<"),
                ),
                ">> appends; > overwrites.",
            ),
            q(
                "Which tool counts unique occurrences of lines?",
                (
                    opt("sort | uniq -c", correct=True),
                    opt("grep -v"),
                    opt("cut -f1"),
                    opt("wc -c"),
                ),
                "uniq -c (after sort) counts adjacent duplicates.",
            ),
        ),
        "Remote servers with SSH and scp": (
            q(
                "In key-based SSH auth, which key goes on the server?",
                (
                    opt("The public key", correct=True),
                    opt("The private key"),
                    opt("Both keys"),
                    opt("Your password file"),
                ),
                "The public key is installed on the server; the private key stays secret.",
            ),
            q(
                "What does `scp results.csv ana@host:/data/` do?",
                (
                    opt("Copies the local file to the remote /data/", correct=True),
                    opt("Deletes the remote file"),
                    opt("Downloads from the server"),
                    opt("Opens an interactive shell"),
                ),
                "scp copies local -> remote here.",
            ),
            q(
                "Which tool gives efficient, resumable file syncing?",
                (
                    opt("rsync", correct=True),
                    opt("cat"),
                    opt("chmod"),
                    opt("grep"),
                ),
                "rsync transfers only differences and can resume.",
            ),
        ),
    },
    final=(
        q(
            "What single character is the root of the Linux filesystem?",
            (opt("/", correct=True), opt("~"), opt("."), opt("C:")),
            "Linux has one root, /, with no drive letters.",
        ),
        q(
            "Which command shows your current directory?",
            (opt("pwd", correct=True), opt("cd"), opt("ls -l"), opt("whoami")),
            "pwd prints the working directory.",
        ),
        q(
            "chmod 755 file gives others which permissions?",
            (opt("r-x (read and execute)", correct=True), opt("rwx"), opt("rw-"), opt("---")),
            "The last digit 5 = r-x for others.",
        ),
        q(
            "What does `set` of pipes let you build?",
            (
                opt("Composed pipelines where data streams between small tools", correct=True),
                opt("Graphical windows"),
                opt("New filesystems"),
                opt("Encrypted tunnels"),
            ),
            "Pipes compose small tools into pipelines.",
        ),
        q(
            "Which command logs you into a remote server?",
            (opt("ssh ana@host", correct=True), opt("scp host"), opt("ping host"), opt("ls host")),
            "ssh opens an encrypted remote shell.",
        ),
        q(
            "Why does 'everything is a file' help in Unix?",
            (
                opt(
                    "The same commands manipulate files, directories and devices uniformly",
                    correct=True,
                ),
                opt("Files are never deleted"),
                opt("It encrypts all data automatically"),
                opt("It makes the GUI faster"),
            ),
            "Uniformity lets a small command set handle everything.",
        ),
    ),
)
