"""Curated quiz questions for the Linux track (per-lesson checkpoints + a
final comprehensive quiz per course). Kept beside ``seed_linux`` so the course
module stays readable. Keys are the EXACT content-lesson titles; the seed
interleaves a checkpoint quiz after each via ``with_checkpoint_quizzes``."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedQuizQuestion, opt, q

_LINUX_BASICS_QUIZZES: dict[str, tuple[SeedQuizQuestion, ...]] = {
    "What is Linux?": (
        q(
            "In Linux terminology, what is a distribution such as Ubuntu or Fedora?",
            (
                opt("Just the Linux kernel by itself"),
                opt(
                    "The Linux kernel plus GNU tools, a package manager, and a desktop or server stack",
                    correct=True,
                ),
                opt("A proprietary fork of Unix sold by a vendor"),
                opt("The shell program that reads your commands"),
            ),
            "A distribution bundles the Linux kernel with the GNU tools, a package manager, and a desktop or server stack on top.",
        ),
        q(
            "According to the Unix philosophy described, why is everything treated as a file?",
            (
                opt(
                    "So that regular files, directories, devices, and even kernel state are read and written like files",
                    correct=True,
                ),
                opt("Because Linux can only store data in plain text files"),
                opt("To force every program to use a graphical interface"),
                opt("Because files are the only thing the kernel can encrypt"),
            ),
            "The 'everything is a file' rule means regular files, directories, devices, and kernel state are all read and written like files.",
        ),
        q(
            "What is the role of the kernel in a Linux system?",
            (
                opt("It is the desktop environment users interact with"),
                opt("It is the package manager that installs software"),
                opt(
                    "It is the one program that talks to the hardware and shares it fairly between processes",
                    correct=True,
                ),
                opt("It is a collection of small text-processing tools"),
            ),
            "The kernel is the single program that talks to the hardware and shares it fairly among every other process.",
        ),
    ),
    "The shell & the filesystem": (
        q(
            "How is the Linux filesystem organized compared to Windows?",
            (
                opt("It uses separate C: and D: drive letters"),
                opt(
                    "It is a single tree rooted at / with every device mounted inside it",
                    correct=True,
                ),
                opt("Each user gets a completely independent filesystem"),
                opt("There is no hierarchy; all files live in one flat directory"),
            ),
            "Linux has no drive letters; there is a single tree rooted at / and every disk or device is mounted somewhere inside it.",
        ),
        q(
            "Which command changes to your home directory?",
            (
                opt("cd .."),
                opt("cd -"),
                opt("cd ~", correct=True),
                opt("pwd"),
            ),
            "The ~ expands to /home/you, so cd ~ moves to your home directory.",
        ),
        q(
            "What does a path that starts with / indicate?",
            (
                opt("It is an absolute path", correct=True),
                opt("It is a relative path"),
                opt("It refers to the parent directory"),
                opt("It is a hidden file"),
            ),
            "Paths are absolute when they start at /, and relative otherwise.",
        ),
    ),
    "Working with files & directories": (
        q(
            "Which command follows a log file, streaming new lines as they are written?",
            (
                opt("cat app.log"),
                opt("head -n 20 app.log"),
                opt("tail -f app.log", correct=True),
                opt("less app.log"),
            ),
            "tail -f follows the file and streams new lines live.",
        ),
        q(
            "What does the -p flag do in mkdir -p project/src?",
            (
                opt("It makes parent directories as needed", correct=True),
                opt("It prints the directory after creating it"),
                opt("It protects the directory from deletion"),
                opt("It creates the directory only if it is empty"),
            ),
            "The -p flag makes any missing parent directories as needed.",
        ),
        q(
            "What is a symbolic link created with ln -s?",
            (
                opt("A compressed copy of a file"),
                opt("A pointer to another path, like a shortcut", correct=True),
                opt("A backup that updates automatically"),
                opt("A renamed version of the original file"),
            ),
            "A symbolic link is a pointer to another path, so running the link follows it to the real target.",
        ),
    ),
    "Users, ownership & permissions": (
        q(
            "In the permission bits, what numeric value does r (read) have?",
            (
                opt("1"),
                opt("2"),
                opt("4", correct=True),
                opt("7"),
            ),
            "Read is 4, write is 2, and execute is 1.",
        ),
        q(
            "What does chmod 755 deploy.sh produce?",
            (
                opt("rw-r--r-- (owner rw, others r)"),
                opt("rwxr-xr-x (runnable by all, writable by owner)", correct=True),
                opt("rwxrwxrwx (full access for everyone)"),
                opt("r-xr-xr-x (read and execute for all, no write)"),
            ),
            "755 means owner rwx (7) and group and others r-x (5), giving rwxr-xr-x.",
        ),
        q(
            "What is the recommended way to run a single command with elevated rights?",
            (
                opt("Log in directly as root"),
                opt("Use sudo to run that one command", correct=True),
                opt("Change every file to chmod 777"),
                opt("Use chgrp to join the root group"),
            ),
            "The principle of least privilege says to run as a normal user and use sudo only for the specific commands that need it.",
        ),
    ),
    "Processes & system monitoring": (
        q(
            "What is the PID of the init/systemd process that every other process descends from?",
            (
                opt("0"),
                opt("1", correct=True),
                opt("9"),
                opt("1234"),
            ),
            "Every process descends from init/systemd, which has PID 1.",
        ),
        q(
            "What does appending & to a command do, as in ./long-task &?",
            (
                opt("It runs the command in the background", correct=True),
                opt("It force-kills the command"),
                opt("It redirects output to a file"),
                opt("It runs the command as root"),
            ),
            "The & runs the command in the background instead of tying up the shell.",
        ),
        q(
            "Which signal does kill -9 send, and why is it a last resort?",
            (
                opt("SIGTERM, because it politely asks the process to stop"),
                opt(
                    "SIGKILL, because it force-kills the process and cannot be caught", correct=True
                ),
                opt("SIGINT, because it behaves like pressing Ctrl-C"),
                opt("SIGCHLD, because it notifies the parent process"),
            ),
            "kill -9 sends SIGKILL, a force-kill used as a last resort after a polite SIGTERM.",
        ),
    ),
    "Pipes, redirection & text tools": (
        q(
            "Which three standard streams does every program have?",
            (
                opt("stdin (0), stdout (1), and stderr (2)", correct=True),
                opt("input, cache, and output"),
                opt("read, write, and append"),
                opt("pipe, socket, and file"),
            ),
            "Every program has input (0), normal output (1), and errors (2).",
        ),
        q(
            "What is the difference between > and >> when redirecting stdout?",
            (
                opt("> appends while >> overwrites"),
                opt("> overwrites the file while >> appends to it", correct=True),
                opt("Both overwrite the file identically"),
                opt("> writes to stderr while >> writes to stdout"),
            ),
            "A single > overwrites the target file, while >> appends to it.",
        ),
        q(
            'What does the pipe | do in cat access.log | grep " 404 " | wc -l?',
            (
                opt("It runs each command in a separate terminal"),
                opt("It sends one command's stdout into the next command's stdin", correct=True),
                opt("It saves the output of each command to a file"),
                opt("It runs the commands in the background"),
            ),
            "A pipe sends one command's stdout into the next command's stdin, chaining small tools into a pipeline.",
        ),
    ),
    "Packages, networking & SSH": (
        q(
            "Which package manager belongs to the Debian/Ubuntu family?",
            (
                opt("dnf"),
                opt("pacman"),
                opt("apt", correct=True),
                opt("brew"),
            ),
            "Debian/Ubuntu use apt, while Fedora/RHEL use dnf and Arch uses pacman.",
        ),
        q(
            "What does SSH provide for working on remote machines?",
            (
                opt("An encrypted shell on another machine", correct=True),
                opt("A graphical desktop streamed over the network"),
                opt("A package repository mirror"),
                opt("A way to mount a remote disk as a local drive"),
            ),
            "SSH gives you an encrypted shell on another machine, the bedrock of server work.",
        ),
        q(
            "After setting up key-based login, which file must be kept secret and never leave your machine?",
            (
                opt("The public key ending in .pub"),
                opt("The private key, such as ~/.ssh/id_ed25519", correct=True),
                opt("The known_hosts file"),
                opt("The authorized_keys file on the server"),
            ),
            "Keep the private key (~/.ssh/id_ed25519) secret; only the .pub file ever leaves your machine.",
        ),
    ),
}

_LINUX_BASICS_FINAL: tuple[SeedQuizQuestion, ...] = (
    q(
        "Which statement best captures the relationship between the Linux kernel and a distribution?",
        (
            opt("The kernel and the distribution are the same thing"),
            opt(
                "The distribution is the kernel plus GNU tools, a package manager, and a desktop or server stack",
                correct=True,
            ),
            opt("The distribution is the hardware the kernel runs on"),
            opt("The kernel is built on top of the distribution"),
        ),
        "Linux is the kernel, while a distribution bundles that kernel with GNU tools, a package manager, and a desktop or server stack.",
    ),
    q(
        "Which command lists files in a long view including hidden ones with human-readable sizes?",
        (
            opt("ls -lah", correct=True),
            opt("pwd"),
            opt("cd ~"),
            opt("man ls"),
        ),
        "ls -lah gives a long view, includes hidden files, and shows human-readable sizes.",
    ),
    q(
        "Using the octal permission trick, what does chmod 644 report.txt set?",
        (
            opt("rwxr-xr-x"),
            opt("rw-r--r-- (owner rw, others r)", correct=True),
            opt("rwxrwxrwx"),
            opt("r--r--r--"),
        ),
        "6 is rw- for the owner and 4 is r-- for group and others, giving rw-r--r--.",
    ),
    q(
        "What does the one-liner awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5 produce?",
        (
            opt("The five largest files in the directory"),
            opt("The top 5 IP addresses hitting the server", correct=True),
            opt("The last five lines of the log"),
            opt("The five most recently modified files"),
        ),
        "It extracts the first column (IPs), counts duplicates, sorts by count descending, and shows the top 5.",
    ),
    q(
        "Which pairing of tool and purpose is correct?",
        (
            opt("ps aux lists every running process with user, PID, %CPU and %MEM", correct=True),
            opt("df -h follows a service's logs live"),
            opt("grep creates parent directories as needed"),
            opt("scp generates an SSH key pair"),
        ),
        "ps aux shows every process with its user, PID, %CPU, %MEM, and command.",
    ),
)


_LINUX_INTERMEDIATE_QUIZZES: dict[str, tuple[SeedQuizQuestion, ...]] = {
    "Kernel space vs. user space": (
        q(
            "How does a user-space program get the kernel to do something privileged like opening a file or sending a packet?",
            (
                opt("By writing directly to the hardware registers"),
                opt(
                    "By making a system call, which switches the CPU into kernel mode", correct=True
                ),
                opt("By loading a kernel module for each request"),
                opt("By sending a message to another user process"),
            ),
            "A system call switches the CPU into kernel mode, runs the kernel handler, and switches back.",
        ),
        q(
            "Why is the Linux kernel described as monolithic?",
            (
                opt(
                    "Because the scheduler, memory manager, filesystems, network stack and drivers all run in one kernel address space",
                    correct=True,
                ),
                opt("Because it cannot load or unload any code at runtime"),
                opt("Because each subsystem runs in its own isolated process"),
                opt("Because it passes messages between subsystems for every operation"),
            ),
            "Linux is monolithic because all its core subsystems share a single kernel address space, avoiding inter-subsystem message passing.",
        ),
        q(
            "Which tool shows the exact system calls a program makes, with -c giving a summary count?",
            (
                opt("lsmod"),
                opt("dmesg"),
                opt("strace", correct=True),
                opt("printk"),
            ),
            "strace traces the system calls a program makes, and strace -c prints a summary count of each syscall.",
        ),
    ),
    "System calls & file I/O in C": (
        q(
            "By convention, which file descriptor numbers are stdin, stdout and stderr?",
            (
                opt("1, 2, 3"),
                opt("0, 1, 2", correct=True),
                opt("2, 1, 0"),
                opt("0, 2, 4"),
            ),
            "By convention 0 is stdin, 1 is stdout and 2 is stderr.",
        ),
        q(
            "What does open() return on success, and how is an error reported?",
            (
                opt(
                    "The lowest free file descriptor on success, or -1 on error with the reason in errno",
                    correct=True,
                ),
                opt("Always file descriptor 3, with errors printed to stderr"),
                opt("A pointer to a FILE struct, or NULL on error"),
                opt("The size of the file, or 0 on error"),
            ),
            "open returns the lowest free descriptor, or -1 on error with the reason left in errno.",
        ),
        q(
            "What does read() return when it reaches end of file?",
            (
                opt("-1"),
                opt("0", correct=True),
                opt("EOF as a negative errno"),
                opt("The total file size"),
            ),
            "read returns the number of bytes read, and 0 at end of file.",
        ),
    ),
    "Processes: fork, exec & signals": (
        q(
            "What does fork() return in the child versus the parent process?",
            (
                opt("0 in the child, the child's PID in the parent", correct=True),
                opt("The child's PID in the child, 0 in the parent"),
                opt("-1 in both on success"),
                opt("The parent's PID in the child, 0 in the parent"),
            ),
            "fork returns twice: 0 in the child and the child's PID in the parent.",
        ),
        q(
            "What happens to the current process image when an exec* call succeeds?",
            (
                opt(
                    "It is replaced with the new program, keeping the same PID, and exec never returns",
                    correct=True,
                ),
                opt("A new child process is spawned while the parent continues"),
                opt("The process forks and then runs the new program in the child"),
                opt("Control returns to the caller after the new program exits"),
            ),
            "exec* replaces the process image with a new program under the same PID and, on success, never returns.",
        ),
        q(
            "Which two signals cannot be caught or ignored, explaining why kill -9 always works?",
            (
                opt("SIGINT and SIGTERM"),
                opt("SIGKILL and SIGSTOP", correct=True),
                opt("SIGCHLD and SIGINT"),
                opt("SIGTERM and SIGSTOP"),
            ),
            "SIGKILL (9) and SIGSTOP cannot be caught or ignored, which is why kill -9 always works.",
        ),
    ),
    "Sockets & I/O multiplexing": (
        q(
            "Which four calls does a TCP server walk through to start accepting connections?",
            (
                opt("open, read, write, close"),
                opt("socket, bind, listen, accept", correct=True),
                opt("socket, connect, send, recv"),
                opt("create, bind, poll, accept"),
            ),
            "A TCP server walks socket, bind, listen and accept.",
        ),
        q(
            "Which readiness API scales to tens of thousands of descriptors with O(1) readiness and underlies high-performance servers?",
            (
                opt("select"),
                opt("poll"),
                opt("epoll", correct=True),
                opt("accept"),
            ),
            "epoll offers O(1) readiness and scales to tens of thousands of descriptors, the basis of high-performance servers.",
        ),
        q(
            "In the epoll example, what does passing -1 as the timeout to epoll_wait do?",
            (
                opt("Returns immediately without blocking"),
                opt("Blocks forever until a descriptor is ready", correct=True),
                opt("Waits exactly one second"),
                opt("Signals an error condition"),
            ),
            "A timeout of -1 makes epoll_wait block forever until a descriptor becomes ready.",
        ),
    ),
    "Your first kernel module": (
        q(
            "Which pair of macros registers a kernel module's entry and exit points?",
            (
                opt("module_init and module_exit", correct=True),
                opt("insmod and rmmod"),
                opt("kmalloc and kfree"),
                opt("printk and dmesg"),
            ),
            "module_init and module_exit register the module's entry and exit functions.",
        ),
        q(
            "How do you allocate and then release memory inside a kernel module, given there is no malloc?",
            (
                opt("Use malloc and free as in user space"),
                opt("Use kmalloc to allocate and kfree to release it", correct=True),
                opt("Use copy_to_user and copy_from_user"),
                opt("Use printk with GFP_KERNEL"),
            ),
            "Kernel code allocates with kmalloc and must release it with kfree.",
        ),
        q(
            'Why must a kernel module declare MODULE_LICENSE("GPL")?',
            (
                opt("Because a non-GPL license taints the kernel", correct=True),
                opt("Because it sets the module's memory allocation flags"),
                opt("Because it registers the module's init function"),
                opt("Because insmod refuses to load any module without a version"),
            ),
            "MODULE_LICENSE is required because a non-GPL license taints the kernel.",
        ),
    ),
    "Kernel APIs: lists, locking & deferred work": (
        q(
            "When choosing between a spinlock and a mutex, which is correct?",
            (
                opt(
                    "A spinlock busy-waits and cannot sleep, suiting very short or interrupt-context sections",
                    correct=True,
                ),
                opt("A spinlock may sleep, suiting long process-context sections"),
                opt("A mutex busy-waits and is used in interrupt context"),
                opt("Both may sleep and are interchangeable"),
            ),
            "A spinlock busy-waits and cannot sleep, so it fits very short critical sections or interrupt context, while a mutex may sleep.",
        ),
        q(
            "Why is slow or sleepy work pushed from an interrupt handler to a workqueue?",
            (
                opt(
                    "Because an interrupt handler must be fast and cannot sleep, while a workqueue runs in a kernel thread in process context that can sleep",
                    correct=True,
                ),
                opt("Because workqueues run with interrupts disabled for speed"),
                opt("Because interrupt handlers cannot allocate memory at all"),
                opt("Because a workqueue holds a spinlock for the whole task"),
            ),
            "An interrupt handler must be fast and cannot sleep, so slow work is deferred to a workqueue running in a kernel thread that can sleep.",
        ),
        q(
            "In the timer example, what does mod_timer(&t, jiffies + HZ) schedule?",
            (
                opt("The timer to fire in about one second", correct=True),
                opt("The timer to fire immediately"),
                opt("The timer to fire after HZ minutes"),
                opt("The timer to be deleted synchronously"),
            ),
            "HZ ticks equal one second, so jiffies + HZ schedules the timer to fire in about one second.",
        ),
    ),
    "Writing a character device driver": (
        q(
            "How do open, read, write and close on a /dev file reach a character driver's code?",
            (
                opt("Through the driver's file_operations table via the VFS", correct=True),
                opt("By calling the driver's module_init function each time"),
                opt("Directly through kmalloc and kfree"),
                opt("Through the epoll readiness interface"),
            ),
            "Operations on the /dev file are routed by the VFS into the driver's file_operations callbacks.",
        ),
        q(
            "Why must a user pointer marked __user never be dereferenced directly in the kernel?",
            (
                opt(
                    "Because it belongs to another address space and may be malicious or unmapped, so copy_to_user and copy_from_user are used",
                    correct=True,
                ),
                opt("Because it always points to read-only memory"),
                opt("Because dereferencing it would taint the kernel license"),
                opt("Because it must first be passed through kmalloc"),
            ),
            "A __user pointer belongs to another address space and may be malicious or unmapped, so the safe copy_to_user and copy_from_user helpers are used.",
        ),
        q(
            "What is the purpose of ioctl in a character device driver?",
            (
                opt("To move a stream of bytes in and out of the device"),
                opt("To issue out-of-band commands such as reset or set a mode", correct=True),
                opt("To allocate the device's major and minor numbers"),
                opt("To create the /dev node for the device"),
            ),
            "Reads and writes move data, while ioctl issues out-of-band commands such as reset or setting a mode.",
        ),
    ),
}

_LINUX_INTERMEDIATE_FINAL: tuple[SeedQuizQuestion, ...] = (
    q(
        "What is the defining difference between user space and kernel space?",
        (
            opt("User space is privileged and owns the hardware, while kernel space is isolated"),
            opt(
                "Kernel space is the privileged core that owns the hardware, while user space is unprivileged and isolated",
                correct=True,
            ),
            opt("Both run at the same privilege level but in different files"),
            opt("User space runs drivers while kernel space runs applications"),
        ),
        "Kernel space is the privileged core that owns and arbitrates the hardware, while user-space programs are unprivileged and isolated.",
    ),
    q(
        "Which set of four system calls drives files, pipes, sockets and device files alike because everything is a file?",
        (
            opt("open, read, write, close", correct=True),
            opt("socket, bind, listen, accept"),
            opt("fork, exec, wait, kill"),
            opt("kmalloc, kfree, copy_to_user, copy_from_user"),
        ),
        "Because everything is a file, the same open, read, write and close calls drive regular files, pipes, sockets and device files.",
    ),
    q(
        "Which classic pattern lets a shell run a typed command in a new process?",
        (
            opt("exec then fork"),
            opt(
                "fork then exec, where the shell forks and the child execs the command",
                correct=True,
            ),
            opt("Two forks with no exec"),
            opt("A single exec that spawns a child"),
        ),
        "The shell forks and then the child execs the command, the classic fork-then-exec pattern.",
    ),
    q(
        "Why can a single Nginx process hold tens of thousands of connections?",
        (
            opt("Because it spawns one thread blocked in recv per client"),
            opt(
                "Because it relies on epoll's O(1) readiness to watch many descriptors at once",
                correct=True,
            ),
            opt("Because select rescans a fixed-size set on every call"),
            opt("Because it loads a kernel module per connection"),
        ),
        "epoll's O(1) readiness lets a single process watch tens of thousands of descriptors, which is why one Nginx process scales so far.",
    ),
    q(
        "In a character driver, how is data safely moved between the kernel and a user buffer?",
        (
            opt("By dereferencing the __user pointer directly"),
            opt(
                "With copy_to_user to send kernel data out and copy_from_user to bring user data in",
                correct=True,
            ),
            opt("With kmalloc and kfree on the user pointer"),
            opt("By calling printk with the user buffer"),
        ),
        "copy_to_user moves data from kernel to user and copy_from_user moves it from user to kernel, safely crossing the address-space boundary.",
    ),
)


_LINUX_ADVANCED_QUIZZES: dict[str, tuple[SeedQuizQuestion, ...]] = {
    "The Linux device model": (
        q(
            "In the Linux device model, what does the bus core do when a discovered device matches a driver's id_table?",
            (
                opt("It loads the module from /sys automatically"),
                opt("It calls that driver's probe(device)", correct=True),
                opt("It calls the driver's remove() first"),
                opt("It allocates a gendisk for the device"),
            ),
            "On a match the bus core calls the driver's probe(device) to bring the device up.",
        ),
        q(
            "What is the purpose of the devm_* managed-resource helpers?",
            (
                opt(
                    "They tie a resource's lifetime to the device so the core frees them on remove or probe failure",
                    correct=True,
                ),
                opt("They speed up DMA transfers by caching bus addresses"),
                opt("They replace the id_table with a Device Tree node"),
                opt("They disable interrupts during probe"),
            ),
            "devm_* helpers bind a resource's lifetime to the device, eliminating manual cleanup on remove or probe failure.",
        ),
        q(
            "Which command lists every PCI device through the sysfs mirror of the device model?",
            (
                opt("ls /sys/class/net/"),
                opt("ls /sys/module/"),
                opt("ls /sys/bus/pci/devices/", correct=True),
                opt("udevadm info /dev/sda"),
            ),
            "The lesson shows ls /sys/bus/pci/devices/ as the way to list every PCI device under sysfs.",
        ),
    ),
    "Platform drivers & the Device Tree": (
        q(
            "Why do controllers soldered onto an SoC (UARTs, I2C, GPIO) need the Device Tree?",
            (
                opt(
                    "They are platform devices that cannot be discovered, so the kernel learns about them from the Device Tree",
                    correct=True,
                ),
                opt("They announce a vendor/product id like PCI and USB devices"),
                opt("They require coherent DMA to be enumerated"),
                opt("They can only be loaded as character devices"),
            ),
            "Non-enumerable platform devices cannot announce themselves, so the kernel learns of them from the Device Tree.",
        ),
        q(
            "Which Device Tree property is the matchmaker that binds a node to a driver's of_match_table?",
            (
                opt("reg"),
                opt("interrupts"),
                opt("compatible", correct=True),
                opt("status"),
            ),
            "The compatible string is matched against the driver's of_match_table to bind device and driver.",
        ),
        q(
            "What do platform_get_resource and platform_get_irq pull from the matched Device Tree node?",
            (
                opt("The compatible string and clocks"),
                opt("The reg (MMIO) and interrupts properties", correct=True),
                opt("The status and of_node fields"),
                opt("The vendor and product ids"),
            ),
            "They extract the reg and interrupts entries from the DT node so the same driver works on any board describing the device.",
        ),
    ),
    "Interrupts & DMA": (
        q(
            "Why must an interrupt handler check the status register and return IRQ_NONE when appropriate?",
            (
                opt(
                    "Because IRQF_SHARED lets several devices share one line, so the handler must tell when the interrupt was not its",
                    correct=True,
                ),
                opt("Because returning IRQ_HANDLED would disable DMA"),
                opt("Because the top half is allowed to sleep"),
                opt("Because coherent DMA requires explicit cache syncing"),
            ),
            "With IRQF_SHARED multiple devices share a line, so a handler returns IRQ_NONE when the interrupt was not raised by its device.",
        ),
        q(
            "Which DMA API is described as best for long-lived buffers like descriptor rings?",
            (
                opt("dma_map_single (streaming DMA)"),
                opt("dma_alloc_coherent (coherent/consistent DMA)", correct=True),
                opt("dma_set_mask_and_coherent"),
                opt("dma_mapping_error"),
            ),
            "Coherent DMA via dma_alloc_coherent is recommended for long-lived buffers such as descriptor rings.",
        ),
        q(
            "What does the DMA direction argument (DMA_TO_DEVICE, DMA_FROM_DEVICE) tell the kernel?",
            (
                opt("Which CPU should handle the interrupt"),
                opt("Which way to flush caches", correct=True),
                opt("Whether to use MSI or MSI-X"),
                opt("How large the descriptor ring must be"),
            ),
            "The direction tells the kernel which way to flush caches for the transfer.",
        ),
    ),
    "Block drivers": (
        q(
            "What sits between the filesystem and a block driver that a char device's byte stream does not have?",
            (
                opt(
                    "A whole block layer that batches, merges, reorders and schedules I/O into requests",
                    correct=True,
                ),
                opt("A net_device_ops table"),
                opt("A file_operations table mapped through VFS"),
                opt("An of_match_table from the Device Tree"),
            ),
            "The block layer batches, merges, reorders and schedules I/O into requests between the filesystem and the driver.",
        ),
        q(
            "Which API do modern block drivers use, providing a tag_set with a queue_rq op?",
            (
                opt("NAPI"),
                opt("the multi-queue API (blk-mq)", correct=True),
                opt("epoll"),
                opt("the URB submission API"),
            ),
            "Modern block drivers use the multi-queue blk-mq API, supplying a tag_set with a queue_rq operation.",
        ),
        q(
            "What is the bio in the block layer?",
            (
                opt("The starting sector returned by blk_rq_pos"),
                opt("The block_device_operations table"),
                opt("The unit of I/O describing pages to/from sectors", correct=True),
                opt("The I/O scheduler such as mq-deadline or BFQ"),
            ),
            "The bio is the unit of I/O: a description of pages moving to or from given sectors.",
        ),
    ),
    "Network drivers": (
        q(
            "What structure does a NIC driver register, and which ops table does it implement?",
            (
                opt("A gendisk implementing block_device_operations"),
                opt("A net_device implementing net_device_ops", correct=True),
                opt("A cdev implementing file_operations"),
                opt("A platform_device implementing of_match_table"),
            ),
            "A NIC driver registers a net_device and implements the net_device_ops callbacks.",
        ),
        q(
            "What is the sk_buff (skb) in a network driver?",
            (
                opt("A per-CPU request queue"),
                opt("A socket buffer: a packet plus headroom for headers", correct=True),
                opt("A bus address handed to the device for DMA"),
                opt("A Base Address Register mapped with pci_iomap"),
            ),
            "The sk_buff is the socket buffer holding a packet plus headroom for headers as it travels the stack.",
        ),
        q(
            "How does NAPI avoid melting the CPU at high packet rates?",
            (
                opt(
                    "It disables RX interrupts under load and polls a budget of packets in softirq context",
                    correct=True,
                ),
                opt("It maps each packet with coherent DMA"),
                opt("It uses one interrupt per packet for accuracy"),
                opt("It moves all receive work into the hardware top half"),
            ),
            "NAPI disables RX interrupts under load and polls a budget of packets in softirq, re-enabling interrupts when traffic drains.",
        ),
    ),
    "PCI & USB drivers": (
        q(
            "How does a PCI device expose its registers, and what maps one into kernel space?",
            (
                opt("Through a Device Tree reg property mapped by devm_ioremap_resource"),
                opt("Through BARs (Base Address Registers), mapped by pci_iomap", correct=True),
                opt("Through an sk_buff mapped by skb_put"),
                opt("Through a URB submitted with usb_submit_urb"),
            ),
            "A PCI device exposes registers via BARs, and pci_iomap maps one into kernel space for ioread32/iowrite32.",
        ),
        q(
            "What does pci_set_master enable for a PCI device?",
            (
                opt("Message-signalled interrupts only"),
                opt("Bus-mastering DMA", correct=True),
                opt("Mapping of BAR 0"),
                opt("Hot-plug disconnect handling"),
            ),
            "pci_set_master enables bus-mastering DMA so the device can read and write memory directly.",
        ),
        q(
            "What rides a URB (USB Request Block) and how is an async transfer completed?",
            (
                opt("A USB transfer, completed via a callback after usb_submit_urb", correct=True),
                opt("A block request, completed via blk_mq_end_request"),
                opt("A packet, completed via napi_gro_receive"),
                opt("A DMA descriptor, completed via dma_unmap_single"),
            ),
            "A USB transfer rides a URB; after usb_submit_urb the completion callback runs later for async transfers.",
        ),
    ),
    "Debugging kernel code": (
        q(
            "Why are dev_dbg/pr_debug messages not visible by default, and how are they enabled?",
            (
                opt("They are compiled out entirely and need a kernel rebuild"),
                opt(
                    "They are compiled in but off, and flipped on at runtime via /sys/kernel/debug/dynamic_debug/control",
                    correct=True,
                ),
                opt("They only print to ftrace, never to dmesg"),
                opt("They require KASAN to be enabled first"),
            ),
            "dev_dbg/pr_debug are compiled in but off by default and are enabled at runtime through dynamic_debug/control.",
        ),
        q(
            "Which sanitizer catches use-after-free and out-of-bounds memory access?",
            (
                opt("KMEMLEAK"),
                opt("lockdep"),
                opt("KASAN", correct=True),
                opt("KGDB"),
            ),
            "KASAN catches use-after-free and out-of-bounds memory accesses.",
        ),
        q(
            "What does a kernel oops/panic print to help locate the failing code?",
            (
                opt("A core dump file in the current directory"),
                opt("The failing instruction, the registers, and a call trace", correct=True),
                opt("A list of every loaded module under /sys/module"),
                opt("The Device Tree node that triggered the fault"),
            ),
            "An oops/panic prints the failing instruction, the registers, and a call trace you can decode to a line.",
        ),
    ),
}

_LINUX_ADVANCED_FINAL: tuple[SeedQuizQuestion, ...] = (
    q(
        "Across PCI, USB and platform drivers, what common lifecycle does the bus core drive?",
        (
            opt(
                "It matches a device against a driver's id_table (or compatible) and calls probe, with remove/disconnect undoing it",
                correct=True,
            ),
            opt("It always loads the driver from the Device Tree regardless of bus"),
            opt("It calls queue_rq for every device before probe"),
            opt("It maps all device registers with dma_alloc_coherent"),
        ),
        "The core matches device to driver and calls probe to bring it up, with remove or disconnect tearing it down in reverse.",
    ),
    q(
        "Why must an interrupt top half be fast and not sleep, and where does heavy work go?",
        (
            opt(
                "It runs in interrupt context, so heavy or sleepy work is deferred to a bottom half like a workqueue or tasklet",
                correct=True,
            ),
            opt("It runs in process context, so it can sleep and allocate freely"),
            opt("It must call dma_map_single before returning IRQ_HANDLED"),
            opt("It must register a net_device before scheduling work"),
        ),
        "The top half runs in interrupt context and cannot sleep, so heavy work is deferred to a bottom half such as a workqueue.",
    ),
    q(
        "Which statement correctly pairs a driver family with its core data unit?",
        (
            opt("Block drivers move sk_buffs; network drivers move bios"),
            opt("Block drivers move bios/requests; network drivers move sk_buffs", correct=True),
            opt("Both block and network drivers move URBs"),
            opt("Character drivers move bios; block drivers move sk_buffs"),
        ),
        "Block drivers service requests built from bios, while network drivers move sk_buffs through the stack.",
    ),
    q(
        "For an SoC controller that cannot be enumerated, how does the same driver work across different boards?",
        (
            opt(
                "Only the Device Tree changes; the driver matches on compatible and reads reg/interrupts from the DT node",
                correct=True,
            ),
            opt("The driver hardcodes the MMIO base and IRQ for each board"),
            opt("The board announces a PCI vendor/device id at boot"),
            opt("The kernel rebuilds the driver per board from kbuild"),
        ),
        "Platform drivers match on compatible and pull reg and interrupts from the DT node, so only the Device Tree changes per board.",
    ),
    q(
        "What is the recommended order of attack when debugging a misbehaving driver?",
        (
            opt(
                "Reproduce, read dmesg, enable dynamic_debug, then reach for ftrace and the sanitizers",
                correct=True,
            ),
            opt("Enable KGDB first, then read the BARs, then reproduce"),
            opt("Run addr2line before reproducing the bug"),
            opt("Turn on KASAN only after ftrace finds nothing"),
        ),
        "The lesson's order is reproduce, read dmesg, turn on dynamic_debug, then use ftrace and the sanitizers.",
    ),
)

__all__ = [
    "_LINUX_ADVANCED_FINAL",
    "_LINUX_ADVANCED_QUIZZES",
    "_LINUX_BASICS_FINAL",
    "_LINUX_BASICS_QUIZZES",
    "_LINUX_INTERMEDIATE_FINAL",
    "_LINUX_INTERMEDIATE_QUIZZES",
]
