"""Curated Linux courses: a three-level track that goes from everyday Linux
use up to writing kernel modules and device drivers.

Grounded in the user's Obsidian ``Operational Systems/Linux`` vault (kernel
architecture, system programming, kernel modules, and the device-driver
families — char/block/net/PCI/USB/platform — plus Device Tree, DMA and kernel
debugging).

Lessons are ``text`` with syntax-highlighted code fences (bash / c / dts) —
there's no Linux runtime in the Academy, so shell commands and kernel C are
illustrative. Each course ends with a knowledge-check quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_linux_quizzes import (
    _LINUX_ADVANCED_FINAL,
    _LINUX_ADVANCED_QUIZZES,
    _LINUX_BASICS_FINAL,
    _LINUX_BASICS_QUIZZES,
    _LINUX_INTERMEDIATE_FINAL,
    _LINUX_INTERMEDIATE_QUIZZES,
)
from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    quiz_lesson,
    with_checkpoint_quizzes,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ── Linux — Basics ───────────────────────────────────────────────────────────

_LINUX_BASICS = SeedCourse(
    slug="linux-basics",
    title="Linux — Basics",
    description=(
        "Get comfortable on the Linux command line: what Linux is, navigating "
        "the filesystem, working with files, users and permissions, processes, "
        "pipes and text tools, and managing packages, networking and SSH — the "
        "day-to-day skills every developer and sysadmin needs."
    ),
    level="Beginner",
    lessons=with_checkpoint_quizzes(
        (
            _t(
                "What is Linux?",
                "8 min",
                """\
# What is Linux?

**Linux** is the open-source kernel Linus Torvalds released in 1991. The thing
you actually install — Ubuntu, Debian, Fedora, Arch — is a **distribution**: the
Linux kernel plus the GNU tools, a package manager, and a desktop or server
stack on top.

```mermaid
flowchart TB
  U[Your programs: shell, browser, servers] --> L[GNU userland: coreutils, bash]
  L --> K[Linux kernel: processes, memory, files, devices]
  K --> H[Hardware: CPU, RAM, disks, network]
```

The **kernel** is the one program that talks to the hardware and shares it
fairly between every other process. Everything else is just a program.

## The Unix philosophy

Linux inherits Unix's design rules, and they explain almost everything you'll
see:

- **Everything is a file** — regular files, directories, devices (`/dev/sda`),
  even kernel state (`/proc`, `/sys`) are read and written like files.
- **Small tools, one job each** — `ls` lists, `grep` filters, `sort` sorts.
- **Compose with pipes** — chain those small tools to do big things.
- **Text is the universal interface** — config and output are plain text you
  can read, diff, and script.

## Why it runs the world

Linux powers most web servers, all 500 of the top supercomputers, Android
phones, and nearly every cloud VM and container. Learning it is learning the
environment your code will actually run in.

**Next:** the shell — where you type commands — and moving around the filesystem.
""",
            ),
            _t(
                "The shell & the filesystem",
                "10 min",
                """\
# The shell & the filesystem

The **shell** (usually `bash` or `zsh`) is the program that reads the commands
you type and runs them. The `$` is its **prompt**; you type a command and press
Enter.

## One big tree

Linux has no `C:\\` drives. There is a single tree rooted at `/`, and every disk
or device is *mounted* somewhere inside it.

```mermaid
flowchart TD
  R["/"] --> home[/home/you/]
  R --> etc[/etc — config/]
  R --> usr[/usr — programs/]
  R --> var[/var — logs, spool/]
  R --> dev[/dev — devices/]
  R --> tmp[/tmp — scratch/]
```

This is the **Filesystem Hierarchy Standard**. Useful landmarks: `/etc` (system
config), `/home/<user>` (your files), `/usr/bin` (installed programs), `/var/log`
(logs), `/tmp` (temporary), `/dev` (devices), `/proc` & `/sys` (live kernel info).

## Moving around

```bash
pwd                 # print working directory — where am I?
ls                  # list files here
ls -lah             # long view, all (incl. hidden), human-readable sizes
cd /var/log         # change to an absolute path
cd ..               # up one level
cd ~                # home directory ( ~ == /home/you )
cd -                # back to the previous directory
```

Paths are **absolute** when they start at `/`, **relative** otherwise. `.` is
"here", `..` is "the parent", `~` is "my home".

## Help is built in

```bash
man ls              # the manual page (press q to quit)
ls --help           # quick option summary
type cd             # what kind of command is this?
```

> Tip: press **Tab** to auto-complete commands and paths — it saves typing and
> prevents typos.

**Next:** creating, copying, moving and finding files.
""",
            ),
            _t(
                "Working with files & directories",
                "11 min",
                """\
# Working with files & directories

A handful of commands cover almost all file work.

## Look at files

```bash
cat notes.txt          # dump the whole file
less big.log           # scroll a big file (q quits, / searches)
head -n 20 app.log     # first 20 lines
tail -n 20 app.log     # last 20 lines
tail -f app.log        # follow — stream new lines live
```

## Create, copy, move, delete

```bash
mkdir -p project/src       # -p makes parent dirs as needed
touch project/src/main.c   # create an empty file (or bump its timestamp)
cp main.c main.bak         # copy
cp -r project backup       # -r copies a directory tree
mv main.bak src/           # move (also how you rename)
mv old.txt new.txt         # rename
rm temp.txt                # delete a file
rm -r build/               # delete a directory tree
```

> **`rm` is permanent** — there is no recycle bin. Double-check before
> `rm -r`, and never run `rm -rf /`.

## Find things

```bash
find . -name "*.log"            # files matching a pattern, recursively
find /var -size +100M           # files larger than 100 MB
find . -mtime -1                # modified in the last day
du -sh *                        # how big is each thing here?
df -h                           # free space per mounted filesystem
```

## Links

A **symbolic link** is a pointer to another path — like a shortcut:

```bash
ln -s /opt/app/current/bin/app /usr/local/bin/app
```

Now running `app` follows the link to the real binary.

**Next:** who can do what — users, ownership and permissions.
""",
            ),
            _t(
                "Users, ownership & permissions",
                "11 min",
                """\
# Users, ownership & permissions

Linux is multi-user from the ground up. Every file has an **owner**, a **group**,
and a set of permissions for *owner / group / others*.

```bash
ls -l report.txt
# -rw-r--r-- 1 ada staff 2048 Jun 9 10:00 report.txt
```

Read that first column left to right:

```text
-   rw-   r--   r--
^   ^     ^     ^
|   owner group others
type (- file, d dir, l link)
```

`r` = read (4), `w` = write (2), `x` = execute (1). For a **directory**, `x`
means "may enter it".

## Changing permissions

```bash
chmod u+x deploy.sh        # add execute for the owner
chmod 644 report.txt       # rw-r--r-- (owner rw, others r)
chmod 755 deploy.sh        # rwxr-xr-x (runnable by all, writable by owner)
chmod -R 750 secrets/      # recurse into a directory
```

The octal trick: add the numbers per column. `7 = rwx`, `6 = rw-`, `5 = r-x`,
`4 = r--`.

## Changing owner

```bash
sudo chown ada report.txt          # change owner
sudo chown ada:devs report.txt     # owner and group
sudo chgrp devs report.txt         # group only
```

## Becoming root, carefully

`root` (UID 0) can do anything. Don't log in as root — use **`sudo`** to run a
single command with elevated rights:

```bash
sudo apt update            # run one command as root
sudo systemctl restart ssh
```

> Principle of least privilege: run as a normal user, reach for `sudo` only for
> the specific commands that need it.

**Next:** the programs that are actually running — processes.
""",
            ),
            _t(
                "Processes & system monitoring",
                "10 min",
                """\
# Processes & system monitoring

A **process** is a running program. Each has a numeric **PID**, an owner, and a
parent (every process descends from `init`/`systemd`, PID 1).

## Seeing what's running

```bash
ps aux                 # every process: user, PID, %CPU, %MEM, command
ps aux | grep nginx    # just the ones matching nginx
top                    # live, sorted dashboard (q quits)
htop                   # nicer top, if installed
```

## Foreground, background & jobs

```bash
./long-task            # runs in the foreground (ties up the shell)
./long-task &          # & runs it in the background
jobs                   # list this shell's background jobs
fg %1                  # bring job 1 back to the foreground
```

`Ctrl-C` interrupts the foreground process; `Ctrl-Z` suspends it (resume with
`bg`).

## Stopping a process

```bash
kill 1234              # politely ask PID 1234 to stop (SIGTERM)
kill -9 1234           # force-kill (SIGKILL) — last resort
pkill -f long-task     # kill by name/command pattern
```

## Services with systemd

Most distributions manage long-running services with **systemd**:

```bash
systemctl status ssh           # is the SSH server running?
sudo systemctl restart nginx   # restart a service
sudo systemctl enable docker   # start it automatically at boot
journalctl -u nginx -f         # follow a service's logs
```

> `/proc/<pid>/` exposes everything the kernel knows about a process as files —
> `cat /proc/1234/status`. "Everything is a file" in action.

**Next:** wiring tools together with pipes and redirection.
""",
            ),
            _t(
                "Pipes, redirection & text tools",
                "11 min",
                """\
# Pipes, redirection & text tools

This is where the Unix philosophy pays off: small tools, joined together.

## Streams: stdin, stdout, stderr

Every program has three streams — input (0), normal output (1), and errors (2).
You can **redirect** them to files:

```bash
echo "hello" > out.txt      # stdout INTO out.txt (overwrite)
echo "again" >> out.txt     # APPEND to out.txt
sort < names.txt            # feed a file in as stdin
make 2> errors.log          # send only errors to a file
make > build.log 2>&1       # send output AND errors to one file
```

## The pipe `|`

A **pipe** sends one command's stdout into the next command's stdin:

```mermaid
flowchart LR
  A[cat access.log] -->|stdout| B[grep 404] -->|stdout| C[wc -l]
```

```bash
cat access.log | grep " 404 " | wc -l    # how many 404s?
```

## The essential text tools

```bash
grep "ERROR" app.log              # lines matching a pattern
grep -ri "todo" src/              # recursive, case-insensitive
wc -l app.log                     # count lines
sort names.txt | uniq -c          # sort, then count duplicates
cut -d: -f1 /etc/passwd           # field 1, ':'-delimited
sed 's/foo/bar/g' in.txt          # stream edit: replace foo with bar
awk '{print $1, $4}' access.log   # print columns 1 and 4
```

A real one-liner — the top 5 IPs hitting your server:

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5
```

> Each tool does one thing; the **pipe** is the glue that turns them into a
> data-processing pipeline.

**Next:** installing software, networking and connecting to remote machines.
""",
            ),
            _t(
                "Packages, networking & SSH",
                "10 min",
                """\
# Packages, networking & SSH

## Installing software

You don't download installers — a **package manager** fetches and installs from
trusted repositories, resolving dependencies for you. Which one depends on the
distro family:

| Family | Manager | Install | Update index |
|--------|---------|---------|--------------|
| Debian/Ubuntu | `apt` | `sudo apt install git` | `sudo apt update` |
| Fedora/RHEL | `dnf` | `sudo dnf install git` | `sudo dnf check-update` |
| Arch | `pacman` | `sudo pacman -S git` | `sudo pacman -Sy` |

```bash
sudo apt update              # refresh the package list
sudo apt install htop        # install
sudo apt upgrade             # upgrade everything installed
apt search nginx             # find a package
```

## Looking at the network

```bash
ip addr                      # your interfaces and IP addresses
ping -c 3 example.com        # is the host reachable?
ss -tulpn                    # listening TCP/UDP ports (who's serving)
curl -I https://example.com  # fetch HTTP headers
dig example.com              # DNS lookup
```

## SSH — working on remote machines

**SSH** gives you an encrypted shell on another machine — the bedrock of server
work.

```bash
ssh ada@server.example.com           # open a remote shell
ssh -p 2222 ada@host                 # non-default port
scp report.txt ada@host:/tmp/        # copy a file to the server
scp ada@host:/var/log/app.log .      # copy one back
```

### Key-based login (no passwords)

```bash
ssh-keygen -t ed25519                # generate a key pair (once)
ssh-copy-id ada@host                 # install your public key on the server
```

After that, `ssh ada@host` logs you in with the key — more secure and no typing
passwords. Keep the **private** key (`~/.ssh/id_ed25519`) secret; only the
`.pub` ever leaves your machine.

> These seven lessons are the daily-driver toolkit. The **Intermediate** course
> goes under the hood: system calls, processes in C, and your first kernel module.

**Next:** check what you've learned.
""",
            ),
            quiz_lesson("Check your knowledge", _LINUX_BASICS_FINAL),
        ),
        _LINUX_BASICS_QUIZZES,
    ),
)


# ── Linux — Intermediate ─────────────────────────────────────────────────────

_LINUX_INTERMEDIATE = SeedCourse(
    slug="linux-intermediate",
    title="Linux — Intermediate: System Programming & Kernel Modules",
    description=(
        "Go under the hood: how the kernel and user space split work, the system "
        "calls behind file and process operations, sockets and I/O multiplexing, "
        "and then cross into kernel space — build, load and debug your first "
        "loadable kernel module and a character device driver."
    ),
    level="Intermediate",
    lessons=with_checkpoint_quizzes(
        (
            _t(
                "Kernel space vs. user space",
                "9 min",
                """\
# Kernel space vs. user space

Linux runs code in two privilege worlds. **User space** is where your programs
live, isolated from each other and from the hardware. **Kernel space** is the
privileged core that owns the hardware and arbitrates access to it.

```mermaid
flowchart TB
  subgraph U[User space — unprivileged]
    A[your app] & B[bash] & C[nginx]
  end
  subgraph K[Kernel space — privileged]
    SC[System call interface]
    SUB[Subsystems: process, memory, VFS, net, drivers]
  end
  A & B & C -->|syscall| SC --> SUB --> HW[Hardware]
```

A user program can't touch hardware or another process's memory directly. When
it needs the kernel to do something privileged — open a file, send a packet,
fork — it makes a **system call**, which switches the CPU into kernel mode,
runs the kernel's handler, and switches back.

## A monolithic (but modular) kernel

Linux is **monolithic**: the scheduler, memory manager, filesystems, network
stack and drivers all run in one kernel address space (fast — no message
passing between them). But it's also **modular**: drivers and features can be
loaded and unloaded at runtime as **kernel modules** (later in this course).

## The major subsystems

| Subsystem | Responsibility |
|-----------|----------------|
| Process scheduler | which task runs on which CPU, and when |
| Memory management | virtual memory, paging, the page cache |
| VFS | a uniform file interface over every filesystem |
| Network stack | sockets, TCP/IP, packet routing |
| Device drivers | the code that speaks to real hardware |

## Watching syscalls

`strace` shows the exact system calls a program makes — the boundary in action:

```bash
strace -f ls /tmp        # trace ls; -f follows child processes
strace -c ls             # a summary count of each syscall
```

**Next:** the file syscalls — open, read, write, close — from C.
""",
            ),
            _t(
                "System calls & file I/O in C",
                "11 min",
                """\
# System calls & file I/O in C

Under every high-level "open a file" is a handful of system calls operating on
**file descriptors** — small integers the kernel hands back to refer to an open
file, socket or pipe. By convention 0 = stdin, 1 = stdout, 2 = stderr.

## open / read / write / close

```c
#include <fcntl.h>
#include <unistd.h>

int fd = open("file.txt", O_RDWR | O_CREAT | O_TRUNC, 0644);
if (fd < 0) { perror("open"); return 1; }

char buf[256];
ssize_t n = read(fd, buf, sizeof(buf));   // returns bytes read, 0 at EOF
write(fd, "hello\\n", 6);                  // returns bytes written

close(fd);
```

`open` returns the lowest free descriptor (or -1 on error, with the reason in
`errno`). The mode `0644` is the permission bits you met in Basics.

### Common open flags

```text
O_RDONLY  O_WRONLY  O_RDWR        access mode (pick one)
O_CREAT   create if missing       O_EXCL  fail if it already exists
O_TRUNC   truncate to empty       O_APPEND  always write at the end
O_NONBLOCK  don't block on I/O     O_CLOEXEC  close on exec()
```

## Moving within a file

```c
off_t pos = lseek(fd, 0, SEEK_END);   // size of the file
lseek(fd, 0, SEEK_SET);               // back to the start
```

## Inspecting a file

```c
#include <sys/stat.h>
struct stat st;
fstat(fd, &st);
printf("size = %ld bytes\\n", (long) st.st_size);
```

> Because **everything is a file**, these same four calls — `open`, `read`,
> `write`, `close` — also drive pipes, sockets and device files. Learn them once.

**Next:** creating processes with fork and exec.
""",
            ),
            _t(
                "Processes: fork, exec & signals",
                "11 min",
                """\
# Processes: fork, exec & signals

## fork() — clone the current process

`fork()` creates a near-identical **child** process. It returns **twice**: `0`
in the child, the child's PID in the parent.

```c
#include <unistd.h>
#include <sys/wait.h>

pid_t pid = fork();
if (pid == 0) {
    // child
    printf("child here, my pid is %d\\n", getpid());
} else {
    // parent
    int status;
    waitpid(pid, &status, 0);   // reap the child, avoid a zombie
    printf("child finished\\n");
}
```

## exec() — become a different program

`exec*` replaces the current process image with a new program — same PID, brand
new code. The classic pattern is **fork then exec**: the shell forks, and the
child execs the command you typed.

```c
char *args[] = {"ls", "-l", NULL};
execvp("ls", args);          // on success, never returns
perror("execvp");            // only reached if exec failed
```

```mermaid
flowchart LR
  P[shell] -->|fork| C[child copy]
  C -->|execvp ls| L[ls runs]
  P -->|waitpid| W[waits for exit]
  L --> W
```

## Signals — asynchronous notifications

Signals interrupt a process to tell it something happened (`SIGINT` from
`Ctrl-C`, `SIGTERM` from `kill`, `SIGCHLD` when a child exits).

```c
#include <signal.h>

void on_sigint(int sig) { /* clean up, then exit */ }

struct sigaction sa = {0};
sa.sa_handler = on_sigint;
sigemptyset(&sa.sa_mask);
sa.sa_flags = SA_RESTART;
sigaction(SIGINT, &sa, NULL);   // install the handler
```

`SIGKILL` (9) and `SIGSTOP` cannot be caught or ignored — that's why `kill -9`
always works.

**Next:** handling many connections at once with I/O multiplexing.
""",
            ),
            _t(
                "Sockets & I/O multiplexing",
                "11 min",
                """\
# Sockets & I/O multiplexing

## A TCP server, end to end

A **socket** is a file descriptor for a network connection. A server walks four
calls — `socket`, `bind`, `listen`, `accept`:

```c
#include <sys/socket.h>
#include <netinet/in.h>

int srv = socket(AF_INET, SOCK_STREAM, 0);        // TCP socket
int opt = 1;
setsockopt(srv, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

struct sockaddr_in addr = {
    .sin_family = AF_INET,
    .sin_addr.s_addr = INADDR_ANY,
    .sin_port = htons(8080),                       // host->network byte order
};
bind(srv, (struct sockaddr *)&addr, sizeof(addr));
listen(srv, 10);                                   // backlog of 10

int cli = accept(srv, NULL, NULL);                 // blocks for a client
char buf[1024];
recv(cli, buf, sizeof(buf), 0);
send(cli, "ok\\n", 3, 0);
close(cli);
```

## Serving many clients: select → poll → epoll

A thread blocked in `recv()` can serve only one client. To watch **many**
descriptors at once, Linux offers three readiness APIs:

| API | Scales to | Notes |
|-----|-----------|-------|
| `select` | a few hundred fds | simple, but rescans a fixed-size set each call |
| `poll` | thousands | array of `pollfd`, no `FD_SETSIZE` limit |
| `epoll` | tens of thousands | O(1) readiness, the basis of high-perf servers |

```c
#include <sys/epoll.h>

int ep = epoll_create1(0);
struct epoll_event ev = { .events = EPOLLIN, .data.fd = srv };
epoll_ctl(ep, EPOLL_CTL_ADD, srv, &ev);

struct epoll_event events[64];
int n = epoll_wait(ep, events, 64, -1);            // -1 = block forever
for (int i = 0; i < n; i++) {
    int fd = events[i].data.fd;                    // this fd is ready
    /* accept() if fd == srv, else recv() */
}
```

`epoll` is why a single Nginx process can hold tens of thousands of connections.

**Next:** crossing into the kernel — your first loadable module.
""",
            ),
            _t(
                "Your first kernel module",
                "11 min",
                """\
# Your first kernel module

A **loadable kernel module** (`.ko`) is kernel code you can insert and remove at
runtime — no reboot. Drivers, filesystems and features ship this way.

## The smallest module

```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static int __init hello_init(void)
{
    printk(KERN_INFO "hello: module loaded\\n");
    return 0;              // 0 = success; non-zero aborts the load
}

static void __exit hello_exit(void)
{
    printk(KERN_INFO "hello: module unloaded\\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");     // required — non-GPL taints the kernel
MODULE_AUTHOR("Ada");
MODULE_DESCRIPTION("A first module");
MODULE_VERSION("1.0");
```

`module_init`/`module_exit` register the entry and exit points. `__init` marks
code that can be freed after load; `printk` is the kernel's `printf` (there's no
libc here), and `KERN_INFO` is its log level.

## Building & loading

A one-line `Makefile` drives the kernel's build system (kbuild):

```makefile
obj-m += hello.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
```

```bash
make                       # produces hello.ko
sudo insmod hello.ko       # insert it
lsmod | grep hello         # confirm it's loaded
dmesg | tail               # see your printk output
sudo rmmod hello           # remove it (runs hello_exit)
```

## Kernel memory & golden rules

There's no `malloc`; you allocate with `kmalloc` and **must** free it:

```c
char *buf = kmalloc(1024, GFP_KERNEL);   // GFP_KERNEL: may sleep
if (!buf) return -ENOMEM;
/* ... */
kfree(buf);
```

> Kernel code shares one address space with everything else: a null-deref or a
> leak can crash or destabilise the whole machine. Check every return, free
> everything you allocate, and use `GFP_ATOMIC` (not `GFP_KERNEL`) in code that
> can't sleep, like interrupt handlers.

**Next:** the kernel toolbox — lists, locks, timers and deferred work.
""",
            ),
            _t(
                "Kernel APIs: lists, locking & deferred work",
                "11 min",
                """\
# Kernel APIs: lists, locking & deferred work

The kernel ships its own data structures and concurrency primitives. Four come
up constantly.

## Intrusive linked lists

You embed a `struct list_head` in your own struct and use the macros:

```c
#include <linux/list.h>

struct item {
    int value;
    struct list_head list;       // the link, embedded in the data
};

LIST_HEAD(my_list);              // the list head

list_add_tail(&it->list, &my_list);

struct item *pos;
list_for_each_entry(pos, &my_list, list)
    pr_info("value = %d\\n", pos->value);
```

## Locking: spinlocks vs. mutexes

Concurrency is everywhere (SMP, interrupts, preemption). Pick by context:

| Primitive | Use when | Can sleep? |
|-----------|----------|------------|
| **spinlock** | very short critical section, or in interrupt context | **no** — busy-waits |
| **mutex** | longer section in process context | yes |

```c
DEFINE_SPINLOCK(lock);
unsigned long flags;
spin_lock_irqsave(&lock, flags);     // also disables local IRQs
/* critical section — keep it tiny */
spin_unlock_irqrestore(&lock, flags);

DEFINE_MUTEX(m);
mutex_lock(&m);
/* ... may sleep here ... */
mutex_unlock(&m);
```

Never sleep while holding a spinlock — it can deadlock the CPU.

## Timers — run something later

```c
static struct timer_list t;
static void fired(struct timer_list *t) { pr_info("ding\\n"); }

timer_setup(&t, fired, 0);
mod_timer(&t, jiffies + HZ);     // fire in ~1 second (HZ ticks = 1s)
/* on cleanup */
del_timer_sync(&t);
```

## Deferred work — escape interrupt context

An interrupt handler must be fast and can't sleep. Push slow or sleepy work to a
**workqueue**, which runs in a kernel thread (process context, *can* sleep):

```c
static struct work_struct work;
static void worker(struct work_struct *w) { /* may sleep, allocate, etc. */ }

INIT_WORK(&work, worker);
schedule_work(&work);            // queue it; runs soon in a kthread
```

This **top-half / bottom-half** split — do the urgent bit in the handler,
defer the rest — is the backbone of driver interrupt handling (Advanced course).

**Next:** put it together — a character device driver.
""",
            ),
            _t(
                "Writing a character device driver",
                "12 min",
                """\
# Writing a character device driver

A **character device** moves a stream of bytes — a serial port, `/dev/null`,
a sensor. To user space it's just a file in `/dev`; `open`/`read`/`write`/`close`
on that file land in *your* driver via a `file_operations` table.

```mermaid
flowchart LR
  U["user: read(fd, ...)"] --> V[VFS] --> F[".read in file_operations"] --> D[your driver code]
```

## The file_operations table

```c
#include <linux/fs.h>
#include <linux/uaccess.h>

static int     dev_open(struct inode *inode, struct file *file);
static int     dev_release(struct inode *inode, struct file *file);
static ssize_t dev_read(struct file *f, char __user *ubuf, size_t len, loff_t *off);
static ssize_t dev_write(struct file *f, const char __user *ubuf, size_t len, loff_t *off);

static const struct file_operations fops = {
    .owner   = THIS_MODULE,
    .open    = dev_open,
    .release = dev_release,
    .read    = dev_read,
    .write   = dev_write,
};
```

## Crossing the user/kernel boundary

A user pointer (`__user`) must **never** be dereferenced directly — it belongs
to another address space and may be malicious or unmapped. Use the safe copies:

```c
static char store[256];

static ssize_t dev_read(struct file *f, char __user *ubuf, size_t len, loff_t *off)
{
    size_t n = min(len, sizeof(store));
    if (copy_to_user(ubuf, store, n))     // kernel -> user
        return -EFAULT;
    return n;                              // bytes delivered
}

static ssize_t dev_write(struct file *f, const char __user *ubuf, size_t len, loff_t *off)
{
    size_t n = min(len, sizeof(store));
    if (copy_from_user(store, ubuf, n))   // user -> kernel
        return -EFAULT;
    return n;
}
```

## Registering the device

Allocate a device number, bind your `fops` with a `cdev`, and create the
`/dev` node so user space can reach it:

```c
static dev_t devno;
static struct cdev cdev;
static struct class *cls;

static int __init drv_init(void)
{
    alloc_chrdev_region(&devno, 0, 1, "mychar");   // pick a major/minor
    cdev_init(&cdev, &fops);
    cdev_add(&cdev, devno, 1);
    cls = class_create("mychar");
    device_create(cls, NULL, devno, NULL, "mychar"); // -> /dev/mychar
    return 0;
}

static void __exit drv_exit(void)
{
    device_destroy(cls, devno);
    class_destroy(cls);
    cdev_del(&cdev);
    unregister_chrdev_region(devno, 1);             // teardown in reverse
}
```

Test it like any file:

```bash
echo "hi" | sudo tee /dev/mychar     # calls dev_write
sudo cat /dev/mychar                 # calls dev_read
```

## ioctl — out-of-band commands

Reads and writes move data; **`ioctl`** issues commands (reset, set a mode).
Encode each command with the `_IO*` macros so the size and direction are checked:

```c
#define MYDEV_MAGIC 'm'
#define MYDEV_RESET     _IO(MYDEV_MAGIC, 0)
#define MYDEV_SET_VALUE _IOW(MYDEV_MAGIC, 1, int)   // user writes an int
#define MYDEV_GET_VALUE _IOR(MYDEV_MAGIC, 2, int)   // user reads an int
```

> You've now crossed from user space into the kernel and back. The **Advanced**
> course builds on this `probe`/`file_operations` model for real hardware:
> platform, block, network, PCI and USB drivers, plus interrupts and DMA.

**Next:** check your knowledge.
""",
            ),
            quiz_lesson("Check your knowledge", _LINUX_INTERMEDIATE_FINAL),
        ),
        _LINUX_INTERMEDIATE_QUIZZES,
    ),
)


# ── Linux — Advanced ─────────────────────────────────────────────────────────

_LINUX_ADVANCED = SeedCourse(
    slug="linux-advanced",
    title="Linux — Advanced: Device Drivers",
    description=(
        "Write real device drivers. The Linux driver model and probe/remove "
        "lifecycle, platform drivers bound through the Device Tree, interrupts "
        "and DMA, then the major driver families — block, network, PCI and USB — "
        "and how to debug kernel code when it goes wrong."
    ),
    level="Advanced",
    lessons=with_checkpoint_quizzes(
        (
            _t(
                "The Linux device model",
                "10 min",
                """\
# The Linux device model

Hardware enumeration in Linux is built on three abstractions that snap together:
**buses**, **devices** and **drivers**. A bus discovers devices; the core matches
each device to a driver that claims to support it; the driver's **`probe`** runs
to bring it up, and **`remove`** tears it down.

```mermaid
flowchart TB
  BUS[Bus: PCI / USB / platform] -->|enumerates| DEV[Device]
  DRV[Driver: id_table] -->|registers with bus| BUS
  BUS -->|match device.id == driver.id| M{match?}
  M -->|yes| P[driver.probe device] --> READY[device live]
  M -->|no| SKIP[left unbound]
```

## Match, then probe

Every driver carries an **id_table** — the devices it supports. The bus core
compares each discovered device against every driver's table; on a hit it calls
that driver's `probe(device)`. Probe is where you map registers, request IRQs,
allocate state and register with the relevant subsystem. `remove` (or
`disconnect`) undoes it, in reverse.

This is identical in shape to the `file_operations` model from the Intermediate
course — a table of callbacks the core invokes — just at the device level.

## Everything shows up in sysfs

The model is mirrored under `/sys` as files you can read:

```bash
ls /sys/bus/pci/devices/        # every PCI device
ls /sys/class/net/              # every network interface
ls /sys/module/                 # every loaded module
udevadm info /dev/sda           # the device's attributes & path
```

## Managed resources (devm)

Probe paths are error-prone: acquire five things, and any failure must release
the earlier four. **`devm_*`** helpers tie a resource's lifetime to the device —
the core frees them automatically on remove or probe failure:

```c
void *p   = devm_kzalloc(&pdev->dev, size, GFP_KERNEL);
void __iomem *io = devm_ioremap_resource(&pdev->dev, res);
devm_request_irq(&pdev->dev, irq, handler, 0, "mydrv", priv);
```

No matching `free`/`iounmap`/`free_irq` needed — that eliminates a whole class
of cleanup bugs.

**Next:** the most common driver type — platform drivers and the Device Tree.
""",
            ),
            _t(
                "Platform drivers & the Device Tree",
                "11 min",
                """\
# Platform drivers & the Device Tree

Devices on enumerable buses (PCI, USB) announce themselves. But the controllers
soldered onto an SoC — UARTs, I2C blocks, GPIO — can't be discovered. These are
**platform devices**, and the kernel learns about them from the **Device Tree**:
a data description of the hardware, separate from the driver code.

## A Device Tree node

```dts
uart0: serial@10000000 {
    compatible = "vendor,uart-1.0", "ns16550a";
    reg = <0x10000000 0x1000>;        // MMIO base and size
    interrupts = <0 42 4>;            // controller, line, flags
    clocks = <&clk_uart>;
    status = "okay";
};
```

The **`compatible`** string is the matchmaker: the driver advertises the same
string in its `of_match_table`, and the core binds them.

## The driver side

```c
#include <linux/platform_device.h>
#include <linux/of.h>

static const struct of_device_id my_of_match[] = {
    { .compatible = "vendor,uart-1.0" },
    { }                                  // sentinel
};
MODULE_DEVICE_TABLE(of, my_of_match);

static int my_probe(struct platform_device *pdev)
{
    struct resource *res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    void __iomem *base = devm_ioremap_resource(&pdev->dev, res);   // map regs
    int irq = platform_get_irq(pdev, 0);

    u32 baud;
    of_property_read_u32(pdev->dev.of_node, "current-speed", &baud); // read DT

    platform_set_drvdata(pdev, base);
    return 0;
}

static int my_remove(struct platform_device *pdev) { return 0; }   // devm cleans up

static struct platform_driver my_driver = {
    .probe  = my_probe,
    .remove = my_remove,
    .driver = {
        .name = "my-uart",
        .of_match_table = my_of_match,
    },
};
module_platform_driver(my_driver);     // generates init/exit for you
```

`platform_get_resource` and `platform_get_irq` pull the `reg` and `interrupts`
out of the matched DT node, so the *same driver* works on any board that
describes the device — only the Device Tree changes.

**Next:** responding to hardware — interrupts and DMA.
""",
            ),
            _t(
                "Interrupts & DMA",
                "12 min",
                """\
# Interrupts & DMA

Two mechanisms let a driver work *with* hardware instead of busy-polling it.

## Interrupts: top half / bottom half

When hardware needs attention it raises an **IRQ**. Your handler runs in
interrupt context — it must be fast and **cannot sleep**. So you split the work:

```mermaid
flowchart LR
  HW[device raises IRQ] --> TH["top half: handler — ack, read status (fast)"]
  TH -->|schedule| BH["bottom half: workqueue/tasklet — heavy work"]
```

```c
#include <linux/interrupt.h>

static irqreturn_t my_isr(int irq, void *dev_id)
{
    struct my_dev *d = dev_id;
    u32 status = ioread32(d->base + STATUS);   // ack the hardware
    if (!(status & MY_PENDING))
        return IRQ_NONE;                        // not ours (shared line)
    schedule_work(&d->work);                    // defer the heavy lifting
    return IRQ_HANDLED;
}

devm_request_irq(&pdev->dev, irq, my_isr, IRQF_SHARED, "mydrv", d);
```

`IRQF_SHARED` lets several devices share one line — which is why a handler must
check the status register and return `IRQ_NONE` when the interrupt wasn't its.

## DMA: move data without the CPU

For bulk transfers the device reads/writes memory directly (**DMA**), and only
interrupts when done. A driver hands the device a **bus address**, not a kernel
virtual one.

### Coherent (consistent) DMA — for long-lived buffers like descriptor rings:

```c
#include <linux/dma-mapping.h>

dma_addr_t handle;
void *cpu = dma_alloc_coherent(dev, size, &handle, GFP_KERNEL);
// CPU uses `cpu`; the device uses `handle`. No explicit syncing needed.
dma_free_coherent(dev, size, cpu, handle);
```

### Streaming DMA — for a one-shot buffer you already have:

```c
dma_addr_t dma = dma_map_single(dev, buf, len, DMA_TO_DEVICE);
if (dma_mapping_error(dev, dma)) { /* bail */ }
// kick the device with `dma`, wait for completion...
dma_unmap_single(dev, dma, len, DMA_TO_DEVICE);
```

Direction (`DMA_TO_DEVICE`, `DMA_FROM_DEVICE`, `DMA_BIDIRECTIONAL`) tells the
kernel which way to flush caches. First, declare what your device can address:

```c
dma_set_mask_and_coherent(dev, DMA_BIT_MASK(64));   // 64-bit capable
```

> The pattern across real drivers: set up a **coherent** descriptor ring once,
> map each transfer **streaming**, and let a completion **interrupt** drive the
> bottom half that recycles buffers.

**Next:** the block layer — disks and the request queue.
""",
            ),
            _t(
                "Block drivers",
                "11 min",
                """\
# Block drivers

A **block device** stores fixed-size blocks you can address randomly — disks,
SSDs, RAM disks. Unlike a char device's byte stream, the kernel sits a whole
**block layer** between the filesystem and your driver: it batches, merges,
reorders and schedules I/O into **requests**.

```mermaid
flowchart TB
  FS[filesystem / page cache] --> BIO[bio: a block I/O unit]
  BIO --> MQ["blk-mq: per-CPU queues, merge & schedule"]
  MQ --> RQ["your queue_rq(request)"] --> DISK[(media)]
```

## Registering a disk

Modern drivers use the multi-queue API (**blk-mq**). You provide a `tag_set`
with your `queue_rq` op, allocate a `gendisk`, set its capacity and `add_disk`:

```c
#include <linux/blkdev.h>
#include <linux/blk-mq.h>

static const struct blk_mq_ops mq_ops = { .queue_rq = my_queue_rq };

dev->tag_set.ops          = &mq_ops;
dev->tag_set.nr_hw_queues = 1;
dev->tag_set.queue_depth  = 128;
blk_mq_alloc_tag_set(&dev->tag_set);

dev->gd = blk_mq_alloc_disk(&dev->tag_set, NULL, dev);
dev->gd->fops = &my_block_ops;             // block_device_operations
set_capacity(dev->gd, NSECTORS);           // size in 512-byte sectors
add_disk(dev->gd);
```

## Servicing a request

The block layer calls `queue_rq` with a `request`; you iterate its segments and
move bytes to/from the backing store:

```c
static blk_status_t my_queue_rq(struct blk_mq_hw_ctx *hctx,
                                const struct blk_mq_queue_data *bd)
{
    struct request *req = bd->rq;
    struct bio_vec bvec;
    struct req_iterator iter;
    sector_t sector = blk_rq_pos(req);             // starting sector

    blk_mq_start_request(req);
    rq_for_each_segment(bvec, req, iter) {
        void *buf = page_address(bvec.bv_page) + bvec.bv_offset;
        bool write = rq_data_dir(req) == WRITE;
        transfer(dev, sector, bvec.bv_len, buf, write);
        sector += bvec.bv_len >> 9;                // /512 bytes per sector
    }
    blk_mq_end_request(req, BLK_STS_OK);
    return BLK_STS_OK;
}
```

The unit of I/O is the **`bio`**: a description of "these pages, to/from these
sectors". The block layer merges adjacent bios into requests and picks an
**I/O scheduler** (mq-deadline, BFQ, none) before they reach you — so a RAM
disk and an NVMe SSD expose the *same* `queue_rq` interface.

**Next:** the network stack and packet-pushing drivers.
""",
            ),
            _t(
                "Network drivers",
                "11 min",
                """\
# Network drivers

A NIC driver registers a **`net_device`** and implements `net_device_ops`. The
unit of data is the **`sk_buff`** (socket buffer, "skb") — a packet plus the
headroom for headers as it travels up and down the stack.

## Registering an interface

```c
#include <linux/netdevice.h>
#include <linux/etherdevice.h>

static const struct net_device_ops my_ops = {
    .ndo_open       = my_open,        // ifconfig up   -> alloc rings, request irq
    .ndo_stop       = my_stop,        // ifconfig down
    .ndo_start_xmit = my_xmit,        // transmit one skb
    .ndo_get_stats64 = my_stats,
};

struct net_device *dev = alloc_etherdev(sizeof(struct my_priv));
dev->netdev_ops = &my_ops;
eth_hw_addr_random(dev);              // or read it from the hardware
register_netdev(dev);                 // -> appears as eth0, enp3s0, ...
```

## Transmit and receive

```c
static netdev_tx_t my_xmit(struct sk_buff *skb, struct net_device *dev)
{
    /* program the hardware to DMA skb->data (skb->len bytes) */
    dev_kfree_skb(skb);               // free once the NIC has it
    return NETDEV_TX_OK;
}
```

On receive you wrap incoming bytes in a fresh skb and push it up the stack:

```c
struct sk_buff *skb = netdev_alloc_skb(dev, len + 2);
skb_reserve(skb, 2);                  // align the IP header
skb_put(skb, len);                    // claim len bytes of payload
memcpy(skb->data, rx_buffer, len);
skb->protocol = eth_type_trans(skb, dev);
napi_gro_receive(&priv->napi, skb);   // hand to the stack
```

## NAPI — interrupt storms vs. polling

At high packet rates, one interrupt per packet melts the CPU. **NAPI** disables
RX interrupts under load and **polls** a budget of packets in softirq context,
re-enabling interrupts only when traffic drains:

```c
static int my_poll(struct napi_struct *napi, int budget)
{
    int done = process_rx(napi, budget);
    if (done < budget) {              // ran dry before the budget
        napi_complete_done(napi, done);
        enable_rx_irq(priv);          // back to interrupt-driven
    }
    return done;
}
netif_napi_add(dev, &priv->napi, my_poll);
```

The interrupt handler then just schedules NAPI (`napi_schedule`) instead of
processing packets itself — the top-half / bottom-half split again, tuned for
throughput.

**Next:** discoverable buses — PCI and USB.
""",
            ),
            _t(
                "PCI & USB drivers",
                "11 min",
                """\
# PCI & USB drivers

PCI and USB are **enumerable** buses: devices announce a vendor/product id, the
core matches a driver's `id_table`, and calls `probe`. Same device model as
before — only the bus glue differs.

## PCI

```c
#include <linux/pci.h>

static const struct pci_device_id ids[] = {
    { PCI_DEVICE(0x8086, 0x1234) },   // vendor, device
    { 0, }
};
MODULE_DEVICE_TABLE(pci, ids);

static int my_probe(struct pci_dev *pdev, const struct pci_device_id *id)
{
    pci_enable_device(pdev);
    pci_request_regions(pdev, "mydrv");
    pci_set_master(pdev);                          // allow it to DMA

    void __iomem *regs = pci_iomap(pdev, 0, 0);    // map BAR 0

    int n = pci_alloc_irq_vectors(pdev, 1, 1, PCI_IRQ_MSIX | PCI_IRQ_MSI);
    request_irq(pci_irq_vector(pdev, 0), my_isr, 0, "mydrv", priv);
    return 0;
}

static struct pci_driver my_pci = {
    .name = "mydrv", .id_table = ids,
    .probe = my_probe, .remove = my_remove,
};
module_pci_driver(my_pci);
```

A PCI device exposes its registers through **BARs** (Base Address Registers);
`pci_iomap` maps one into kernel space, then `ioread32`/`iowrite32` touch the
registers. `pci_set_master` enables bus-mastering DMA; **MSI/MSI-X** are
message-signalled interrupts (no shared IRQ line).

## USB

```c
#include <linux/usb.h>

static const struct usb_device_id ids[] = {
    { USB_DEVICE(0x1234, 0x5678) },
    { }
};
MODULE_DEVICE_TABLE(usb, ids);

static int my_probe(struct usb_interface *intf, const struct usb_device_id *id)
{
    struct usb_device *udev = interface_to_usbdev(intf);
    /* walk intf->cur_altsetting to find bulk-in/out endpoints */
    usb_set_intfdata(intf, dev);
    return 0;
}
```

USB transfers ride a **URB** (USB Request Block) — built, submitted, and
completed via a callback:

```c
struct urb *urb = usb_alloc_urb(0, GFP_KERNEL);
usb_fill_bulk_urb(urb, udev, usb_rcvbulkpipe(udev, ep_in),
                  buf, len, on_complete, dev);
usb_submit_urb(urb, GFP_KERNEL);          // async; on_complete() runs later
```

(For simple, synchronous transfers `usb_bulk_msg` / `usb_control_msg` block
until done.) USB is hot-pluggable, so `disconnect` can fire at any time — your
driver must cancel in-flight URBs and stop touching the device immediately.

**Next:** what to do when a driver misbehaves — kernel debugging.
""",
            ),
            _t(
                "Debugging kernel code",
                "10 min",
                """\
# Debugging kernel code

In user space a crash is a core dump; in the kernel a bad pointer can take down
the machine. These are the tools that keep that rare.

## printk and dynamic debug

`printk` has log levels; `pr_*` are the shorthands. Read them with `dmesg`:

```c
pr_err("mydrv: probe failed: %d\\n", ret);
pr_info("mydrv: %u packets\\n", n);
dev_dbg(&pdev->dev, "register state: %#x\\n", val);   // ties msg to the device
```

`dev_dbg`/`pr_debug` are compiled in but **off** by default — flip them on at
runtime without recompiling:

```bash
echo 'module mydrv +p' > /sys/kernel/debug/dynamic_debug/control
dmesg -w                                    # watch the log live
```

## Reading an oops

A null-deref or bad access prints an **oops/panic**: the failing instruction,
the registers, and a **call trace**. Decode the trace to the exact line:

```bash
./scripts/decode_stacktrace.sh vmlinux < oops.txt
addr2line -e mydrv.ko 0x4f2               # offset -> file:line
```

`BUG_ON(cond)` panics on an invariant; `WARN_ON_ONCE(cond)` logs a trace once
and keeps going — prefer `WARN` for recoverable surprises.

## ftrace — trace the live kernel

`ftrace` records the kernel's own function calls with near-zero overhead:

```bash
cd /sys/kernel/tracing
echo function > current_tracer
echo my_probe > set_ftrace_filter
cat trace                                  # see who called what, with timings
```

`trace_printk()` from your code lands in this same buffer — far cheaper than
`printk` for hot paths.

## The sanitizers

Build the kernel (or your module) with these and the bugs announce themselves:

| Tool | Catches |
|------|---------|
| **KASAN** | use-after-free, out-of-bounds memory access |
| **KMEMLEAK** | leaked allocations (`kmalloc` never freed) |
| **lockdep** | lock-ordering deadlocks, *before* they happen |
| **KGDB** | source-level breakpoints over a serial console |

> Order of attack: reproduce, read `dmesg`, turn on `dynamic_debug`, then reach
> for `ftrace` and the sanitizers. Most driver bugs are a missing return check,
> an unfreed resource, or a sleep under a spinlock — all three are exactly what
> KASAN, KMEMLEAK and lockdep are built to surface.

**Next:** check your knowledge.
""",
            ),
            quiz_lesson("Check your knowledge", _LINUX_ADVANCED_FINAL),
        ),
        _LINUX_ADVANCED_QUIZZES,
    ),
)


LINUX_COURSES: tuple[SeedCourse, ...] = (
    _LINUX_BASICS,
    _LINUX_INTERMEDIATE,
    _LINUX_ADVANCED,
)

__all__ = ["LINUX_COURSES"]
