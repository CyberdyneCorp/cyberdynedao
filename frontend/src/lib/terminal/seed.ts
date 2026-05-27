/**
 * Seed filesystem for the Linux-course sandbox.
 *
 * Boots a believable little world under `/home/user` plus a couple of
 * read-only system dirs (`/etc`, `/bin`, `/tmp`) so commands like
 * `ls /`, `cat /etc/os-release`, and `find /` have something to chew
 * on. Content is intentionally course-flavoured — the readme nudges
 * the student toward the commands the lesson covers.
 */

import { Vfs, makeDir, makeFile, type VfsDir } from './vfs';

export const HOME = '/home/user';

const README = `Welcome to the CyberdyneOS shell.

This is a sandboxed Linux terminal for the course. Nothing here touches
a real machine — explore freely, you can't break anything.

Try these to get your bearings:
  ls -la            list everything, long format
  cd projects       move into a directory
  cat notes/todo.md read a file
  tree              see the whole tree at once
  grep -rin todo .  search recursively, case-insensitive
  find . -name '*.md'
  vi scratch.txt    edit a file (i to insert, Esc then :wq to save)
  top               watch the (pretend) process list, q to quit
  help              list every command
`;

const TODO = `# TODO

- [x] open the terminal
- [ ] learn ls / cd / pwd
- [ ] edit this file with vi
- [ ] search with grep and find
`;

const LESSON = `Lesson 1 — Navigating the filesystem
=====================================

Everything in Linux is a path. "/" is the root. Your home is ~ (which
is ${HOME}). "." is here, ".." is the parent.

pwd  -> where am I?
ls   -> what's here?
cd   -> go somewhere
cat  -> show a file

Practice: cd into projects/, list it, then cd back with "cd .." or "cd ~".
`;

const HELLO_SH = `#!/bin/sh
# A sample script. This shell doesn't execute scripts yet —
# but you can read it with cat and edit it with vi.
echo "Hello from CyberdyneOS"
`;

const OS_RELEASE = `NAME="CyberdyneOS"
VERSION="1.0 (Skynet)"
ID=cyberdyne
PRETTY_NAME="CyberdyneOS 1.0"
HOME_URL="https://cyberdynecorp.ai"
`;

function withChildren(dir: VfsDir, children: Record<string, VfsDir['children'][string]>): VfsDir {
	dir.children = children;
	return dir;
}

export function seedFilesystem(): Vfs {
	const root = makeDir('');

	// /home/user
	const user = withChildren(makeDir('user'), {
		'readme.txt': makeFile('readme.txt', README),
		'lesson1.txt': makeFile('lesson1.txt', LESSON),
		'scratch.txt': makeFile('scratch.txt', ''),
		notes: withChildren(makeDir('notes'), {
			'todo.md': makeFile('todo.md', TODO),
			'ideas.md': makeFile('ideas.md', '# Ideas\n\n- build a robot\n- take over compiling\n')
		}),
		projects: withChildren(makeDir('projects'), {
			'hello.sh': makeFile('hello.sh', HELLO_SH, '-rwxr-xr-x'),
			demo: withChildren(makeDir('demo'), {
				'main.c': makeFile(
					'main.c',
					'#include <stdio.h>\n\nint main(void) {\n    printf("hello, world\\n");\n    return 0;\n}\n'
				),
				'README.md': makeFile('README.md', '# demo\n\nA tiny C program. TODO: add a Makefile.\n')
			})
		})
	});

	const home = withChildren(makeDir('home'), { user });

	const etc = withChildren(makeDir('etc'), {
		'os-release': makeFile('os-release', OS_RELEASE),
		hostname: makeFile('hostname', 'cyberdyne\n'),
		hosts: makeFile('hosts', '127.0.0.1\tlocalhost\n127.0.1.1\tcyberdyne\n')
	});

	const bin = withChildren(makeDir('bin'), {
		// Cosmetic — listing these makes `ls /bin` feel real.
		ls: makeFile('ls', '', '-rwxr-xr-x'),
		cat: makeFile('cat', '', '-rwxr-xr-x'),
		grep: makeFile('grep', '', '-rwxr-xr-x'),
		vi: makeFile('vi', '', '-rwxr-xr-x'),
		sh: makeFile('sh', '', '-rwxr-xr-x')
	});

	root.children['home'] = home;
	root.children['etc'] = etc;
	root.children['bin'] = bin;
	root.children['tmp'] = makeDir('tmp');

	return new Vfs(root, HOME);
}
