/**
 * A small modal text editor modelled on vi.
 *
 * Pure state machine: `feed(key)` takes one normalized key and mutates
 * the buffer, returning an optional ViAction the host applies (write
 * the buffer to the VFS, quit, or both). No DOM, no VFS access here —
 * the view-model owns persistence so this stays unit-testable.
 *
 * Supported (enough for the course's "edit a file" lesson):
 *   normal : h j k l ↑↓←→, 0 $ , G gg , x , dd , i a A o O , :
 *   insert : printable chars, Enter, Backspace, Esc
 *   command: :w :q :q! :wq :x  (with Esc to cancel)
 */

export type ViMode = 'normal' | 'insert' | 'command';

export type ViAction =
	| { kind: 'write' }
	| { kind: 'quit' }
	| { kind: 'write-quit' }
	| null;

export class ViEditor {
	lines: string[];
	row = 0;
	col = 0;
	mode: ViMode = 'normal';
	command = '';
	status = '';
	dirty = false;
	readonly filename: string;

	private pendingD = false; // saw first `d` of `dd`
	private pendingG = false; // saw first `g` of `gg`

	constructor(filename: string, content: string) {
		this.filename = filename;
		this.lines = content === '' ? [''] : content.replace(/\n$/, '').split('\n');
		this.status = `"${filename}" ${this.lines.length}L, ${content.length}C`;
	}

	text(): string {
		return this.lines.join('\n') + '\n';
	}

	private clampCol() {
		const max = this.mode === 'insert' ? this.lines[this.row].length : Math.max(0, this.lines[this.row].length - 1);
		if (this.col > max) this.col = max;
		if (this.col < 0) this.col = 0;
	}

	feed(key: string): ViAction {
		if (this.mode === 'insert') return this.feedInsert(key);
		if (this.mode === 'command') return this.feedCommand(key);
		return this.feedNormal(key);
	}

	// ── normal mode ────────────────────────────────────────────────────
	private feedNormal(key: string): ViAction {
		// two-key combos first
		if (this.pendingD) {
			this.pendingD = false;
			if (key === 'd') {
				this.deleteLine();
				return null;
			}
			// any other key cancels the pending d
		}
		if (this.pendingG) {
			this.pendingG = false;
			if (key === 'g') {
				this.row = 0;
				this.col = 0;
				return null;
			}
		}

		switch (key) {
			case 'h':
			case 'ArrowLeft':
				this.col = Math.max(0, this.col - 1);
				return null;
			case 'l':
			case 'ArrowRight':
				this.col = Math.min(Math.max(0, this.lines[this.row].length - 1), this.col + 1);
				return null;
			case 'k':
			case 'ArrowUp':
				this.row = Math.max(0, this.row - 1);
				this.clampCol();
				return null;
			case 'j':
			case 'ArrowDown':
				this.row = Math.min(this.lines.length - 1, this.row + 1);
				this.clampCol();
				return null;
			case '0':
				this.col = 0;
				return null;
			case '$':
				this.col = Math.max(0, this.lines[this.row].length - 1);
				return null;
			case 'G':
				this.row = this.lines.length - 1;
				this.clampCol();
				return null;
			case 'g':
				this.pendingG = true;
				return null;
			case 'x':
				this.deleteChar();
				return null;
			case 'd':
				this.pendingD = true;
				return null;
			case 'i':
				this.mode = 'insert';
				this.status = '-- INSERT --';
				return null;
			case 'a':
				this.mode = 'insert';
				this.col = Math.min(this.lines[this.row].length, this.col + 1);
				this.status = '-- INSERT --';
				return null;
			case 'A':
				this.mode = 'insert';
				this.col = this.lines[this.row].length;
				this.status = '-- INSERT --';
				return null;
			case 'o':
				this.lines.splice(this.row + 1, 0, '');
				this.row += 1;
				this.col = 0;
				this.mode = 'insert';
				this.dirty = true;
				this.status = '-- INSERT --';
				return null;
			case 'O':
				this.lines.splice(this.row, 0, '');
				this.col = 0;
				this.mode = 'insert';
				this.dirty = true;
				this.status = '-- INSERT --';
				return null;
			case ':':
				this.mode = 'command';
				this.command = '';
				this.status = ':';
				return null;
			default:
				return null;
		}
	}

	private deleteChar() {
		const line = this.lines[this.row];
		if (this.col < line.length) {
			this.lines[this.row] = line.slice(0, this.col) + line.slice(this.col + 1);
			this.dirty = true;
			this.clampCol();
		}
	}

	private deleteLine() {
		this.lines.splice(this.row, 1);
		if (this.lines.length === 0) this.lines = [''];
		if (this.row >= this.lines.length) this.row = this.lines.length - 1;
		this.col = 0;
		this.dirty = true;
	}

	// ── insert mode ────────────────────────────────────────────────────
	private feedInsert(key: string): ViAction {
		if (key === 'Escape') {
			this.mode = 'normal';
			this.status = '';
			this.col = Math.max(0, this.col - 1);
			return null;
		}
		if (key === 'Enter') {
			const line = this.lines[this.row];
			const before = line.slice(0, this.col);
			const after = line.slice(this.col);
			this.lines[this.row] = before;
			this.lines.splice(this.row + 1, 0, after);
			this.row += 1;
			this.col = 0;
			this.dirty = true;
			return null;
		}
		if (key === 'Backspace') {
			if (this.col > 0) {
				const line = this.lines[this.row];
				this.lines[this.row] = line.slice(0, this.col - 1) + line.slice(this.col);
				this.col -= 1;
				this.dirty = true;
			} else if (this.row > 0) {
				const prevLen = this.lines[this.row - 1].length;
				this.lines[this.row - 1] += this.lines[this.row];
				this.lines.splice(this.row, 1);
				this.row -= 1;
				this.col = prevLen;
				this.dirty = true;
			}
			return null;
		}
		if (key.length === 1) {
			const line = this.lines[this.row];
			this.lines[this.row] = line.slice(0, this.col) + key + line.slice(this.col);
			this.col += 1;
			this.dirty = true;
		}
		return null;
	}

	// ── command-line mode ──────────────────────────────────────────────
	private feedCommand(key: string): ViAction {
		if (key === 'Escape') {
			this.mode = 'normal';
			this.command = '';
			this.status = '';
			return null;
		}
		if (key === 'Backspace') {
			if (this.command === '') {
				this.mode = 'normal';
				this.status = '';
			} else {
				this.command = this.command.slice(0, -1);
				this.status = ':' + this.command;
			}
			return null;
		}
		if (key === 'Enter') {
			return this.execCommand(this.command);
		}
		if (key.length === 1) {
			this.command += key;
			this.status = ':' + this.command;
		}
		return null;
	}

	private execCommand(cmd: string): ViAction {
		this.mode = 'normal';
		const c = cmd.trim();
		switch (c) {
			case 'w':
				this.dirty = false;
				this.status = `"${this.filename}" written`;
				return { kind: 'write' };
			case 'q':
				if (this.dirty) {
					this.status = 'E37: No write since last change (add ! to override)';
					return null;
				}
				return { kind: 'quit' };
			case 'q!':
				return { kind: 'quit' };
			case 'wq':
			case 'x':
				this.dirty = false;
				return { kind: 'write-quit' };
			default:
				this.status = `E492: Not an editor command: ${c}`;
				return null;
		}
	}
}
