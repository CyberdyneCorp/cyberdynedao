/**
 * A tiny in-browser Unix-like filesystem.
 *
 * Backs the Linux-course terminal sandbox — every `ls` / `cd` / `cat`
 * runs against this tree, no network, no real FS. The model is
 * deliberately minimal: nodes are either directories (a child map) or
 * files (a string body). No symlinks, no permissions enforcement
 * (mode is cosmetic, shown by `ls -l`), no inodes.
 *
 * Paths follow Unix rules: `/` root, `.`/`..`, and `~` → the home dir
 * passed to the resolver. Everything is case-sensitive.
 */

export type NodeKind = 'file' | 'dir';

export interface VfsFile {
	kind: 'file';
	name: string;
	content: string;
	mode: string; // cosmetic, e.g. "-rw-r--r--"
	mtime: number; // epoch ms
}

export interface VfsDir {
	kind: 'dir';
	name: string;
	mode: string; // e.g. "drwxr-xr-x"
	mtime: number;
	children: Record<string, VfsNode>;
}

export type VfsNode = VfsFile | VfsDir;

export class VfsError extends Error {
	constructor(message: string) {
		super(message);
		this.name = 'VfsError';
	}
}

const DEFAULT_FILE_MODE = '-rw-r--r--';
const DEFAULT_DIR_MODE = 'drwxr-xr-x';

export function makeDir(name: string, mode = DEFAULT_DIR_MODE): VfsDir {
	return { kind: 'dir', name, mode, mtime: Date.now(), children: {} };
}

export function makeFile(name: string, content = '', mode = DEFAULT_FILE_MODE): VfsFile {
	return { kind: 'file', name, content, mode, mtime: Date.now() };
}

export function isDir(node: VfsNode | null | undefined): node is VfsDir {
	return !!node && node.kind === 'dir';
}

export function isFile(node: VfsNode | null | undefined): node is VfsFile {
	return !!node && node.kind === 'file';
}

/**
 * Split a path into normalized segments, applying `.`/`..`/`~`.
 *
 * Returns an *absolute* segment list (relative to root). `cwd` and
 * `home` must themselves be absolute (leading `/`).
 */
export function normalizePath(path: string, cwd: string, home: string): string[] {
	let p = path.trim();
	if (p === '') p = '.';

	// `~` expansion — only as the first segment.
	if (p === '~' || p.startsWith('~/')) {
		p = home + p.slice(1);
	}

	const startAbsolute = p.startsWith('/');
	const base = startAbsolute ? [] : splitAbs(cwd);

	const out = base.slice();
	for (const seg of p.split('/')) {
		if (seg === '' || seg === '.') continue;
		if (seg === '..') {
			if (out.length > 0) out.pop();
			continue;
		}
		out.push(seg);
	}
	return out;
}

function splitAbs(absPath: string): string[] {
	return absPath.split('/').filter((s) => s !== '');
}

export function segmentsToPath(segments: string[]): string {
	return '/' + segments.join('/');
}

/** Pretty-print an absolute path, collapsing the home prefix to `~`. */
export function displayPath(absPath: string, home: string): string {
	if (absPath === home) return '~';
	if (absPath.startsWith(home + '/')) return '~' + absPath.slice(home.length);
	return absPath;
}

export class Vfs {
	private root: VfsDir;
	readonly home: string;

	constructor(root?: VfsDir, home = '/home/user') {
		this.root = root ?? makeDir('');
		this.home = home;
	}

	getRoot(): VfsDir {
		return this.root;
	}

	/** Resolve a path to its node, or null if any segment is missing. */
	resolve(path: string, cwd: string): VfsNode | null {
		const segs = normalizePath(path, cwd, this.home);
		let node: VfsNode = this.root;
		for (const seg of segs) {
			if (!isDir(node)) return null;
			const next: VfsNode | undefined = node.children[seg];
			if (!next) return null;
			node = next;
		}
		return node;
	}

	/** Resolve, throwing VfsError with a Unix-style message on miss. */
	resolveOrThrow(path: string, cwd: string): VfsNode {
		const node = this.resolve(path, cwd);
		if (!node) throw new VfsError(`${path}: No such file or directory`);
		return node;
	}

	/** Return the parent dir node + final segment name for a path. */
	private parentOf(path: string, cwd: string): { parent: VfsDir; name: string; segs: string[] } {
		const segs = normalizePath(path, cwd, this.home);
		if (segs.length === 0) throw new VfsError(`${path}: Is a directory`);
		const name = segs[segs.length - 1];
		const parentSegs = segs.slice(0, -1);
		let node: VfsNode = this.root;
		for (const seg of parentSegs) {
			if (!isDir(node)) throw new VfsError(`${path}: Not a directory`);
			const next: VfsNode | undefined = node.children[seg];
			if (!next) throw new VfsError(`${path}: No such file or directory`);
			node = next;
		}
		if (!isDir(node)) throw new VfsError(`${path}: Not a directory`);
		return { parent: node, name, segs };
	}

	readFile(path: string, cwd: string): string {
		const node = this.resolveOrThrow(path, cwd);
		if (isDir(node)) throw new VfsError(`${path}: Is a directory`);
		return node.content;
	}

	writeFile(path: string, content: string, cwd: string): void {
		const { parent, name } = this.parentOf(path, cwd);
		const existing = parent.children[name];
		if (isDir(existing)) throw new VfsError(`${path}: Is a directory`);
		if (isFile(existing)) {
			existing.content = content;
			existing.mtime = Date.now();
		} else {
			parent.children[name] = makeFile(name, content);
		}
		parent.mtime = Date.now();
	}

	/** Create an empty file or bump mtime if it exists (touch). */
	touch(path: string, cwd: string): void {
		const { parent, name } = this.parentOf(path, cwd);
		const existing = parent.children[name];
		if (existing) {
			existing.mtime = Date.now();
		} else {
			parent.children[name] = makeFile(name, '');
			parent.mtime = Date.now();
		}
	}

	mkdir(path: string, cwd: string, parents = false): void {
		const segs = normalizePath(path, cwd, this.home);
		if (segs.length === 0) throw new VfsError(`cannot create directory '${path}': File exists`);
		let node: VfsDir = this.root;
		for (let i = 0; i < segs.length; i++) {
			const seg = segs[i];
			const last = i === segs.length - 1;
			const existing = node.children[seg];
			if (existing) {
				if (!isDir(existing)) throw new VfsError(`cannot create directory '${path}': Not a directory`);
				if (last && !parents) throw new VfsError(`cannot create directory '${path}': File exists`);
				node = existing;
				continue;
			}
			if (!last && !parents) {
				throw new VfsError(`cannot create directory '${path}': No such file or directory`);
			}
			const dir = makeDir(seg);
			node.children[seg] = dir;
			node.mtime = Date.now();
			node = dir;
		}
	}

	/** Remove a file (or, with recursive, a directory subtree). */
	rm(path: string, cwd: string, recursive = false): void {
		const { parent, name, segs } = this.parentOf(path, cwd);
		if (segs.length === 0) throw new VfsError(`cannot remove '${path}'`);
		const node = parent.children[name];
		if (!node) throw new VfsError(`cannot remove '${path}': No such file or directory`);
		if (isDir(node) && !recursive) throw new VfsError(`cannot remove '${path}': Is a directory`);
		delete parent.children[name];
		parent.mtime = Date.now();
	}

	rmdir(path: string, cwd: string): void {
		const { parent, name } = this.parentOf(path, cwd);
		const node = parent.children[name];
		if (!node) throw new VfsError(`failed to remove '${path}': No such file or directory`);
		if (!isDir(node)) throw new VfsError(`failed to remove '${path}': Not a directory`);
		if (Object.keys(node.children).length > 0) {
			throw new VfsError(`failed to remove '${path}': Directory not empty`);
		}
		delete parent.children[name];
		parent.mtime = Date.now();
	}

	/** Copy a file (recursive for dirs). dest may be a dir or a new name. */
	cp(src: string, dest: string, cwd: string, recursive = false): void {
		const srcNode = this.resolveOrThrow(src, cwd);
		if (isDir(srcNode) && !recursive) throw new VfsError(`-r not specified; omitting directory '${src}'`);
		const clone = cloneNode(srcNode);
		this.placeInto(dest, cwd, clone, srcNode.name);
	}

	/** Move/rename. */
	mv(src: string, dest: string, cwd: string): void {
		const srcNode = this.resolveOrThrow(src, cwd);
		const { parent: srcParent, name: srcName } = this.parentOf(src, cwd);
		// Remove from source, then place into dest.
		const detached = srcParent.children[srcName];
		delete srcParent.children[srcName];
		srcParent.mtime = Date.now();
		try {
			this.placeInto(dest, cwd, detached, srcNode.name);
		} catch (e) {
			// Roll back on failure so a bad mv doesn't lose the node.
			srcParent.children[srcName] = detached;
			throw e;
		}
	}

	/** Drop `node` at `dest`: into it if dest is a dir, else as that name. */
	private placeInto(dest: string, cwd: string, node: VfsNode, fallbackName: string): void {
		const destNode = this.resolve(dest, cwd);
		if (isDir(destNode)) {
			node.name = fallbackName;
			destNode.children[fallbackName] = node;
			destNode.mtime = Date.now();
			return;
		}
		const { parent, name } = this.parentOf(dest, cwd);
		node.name = name;
		parent.children[name] = node;
		parent.mtime = Date.now();
	}

	/** Sorted child names of a dir (for ls / completion). */
	list(path: string, cwd: string): VfsNode[] {
		const node = this.resolveOrThrow(path, cwd);
		if (isFile(node)) return [node];
		return Object.values(node.children).sort((a, b) => a.name.localeCompare(b.name));
	}

	toJSON(): string {
		return JSON.stringify({ home: this.home, root: this.root });
	}

	static fromJSON(json: string): Vfs {
		const parsed = JSON.parse(json) as { home: string; root: VfsDir };
		return new Vfs(parsed.root, parsed.home);
	}
}

function cloneNode(node: VfsNode): VfsNode {
	if (isFile(node)) {
		return { ...node };
	}
	const children: Record<string, VfsNode> = {};
	for (const [k, v] of Object.entries(node.children)) {
		children[k] = cloneNode(v);
	}
	return { ...node, children };
}
