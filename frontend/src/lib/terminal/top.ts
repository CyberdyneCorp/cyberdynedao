/**
 * A fake-but-plausible `top`.
 *
 * Holds a static process roster and jitters CPU/MEM on each `tick()`
 * so the live view feels alive. RNG is injectable so tests are
 * deterministic. `render(cols)` returns the full screen as text.
 */

export interface Process {
	pid: number;
	user: string;
	pr: number;
	ni: number;
	virt: number;
	res: number;
	cpu: number;
	mem: number;
	time: string;
	command: string;
}

type Rng = () => number;

const ROSTER: Array<Pick<Process, 'pid' | 'user' | 'command'> & { base: number }> = [
	{ pid: 1, user: 'root', command: 'systemd', base: 0.1 },
	{ pid: 412, user: 'root', command: 'skynetd', base: 8 },
	{ pid: 533, user: 'root', command: 'dockerd', base: 2.3 },
	{ pid: 871, user: 'user', command: 'node', base: 12 },
	{ pid: 902, user: 'user', command: 'vite', base: 6.5 },
	{ pid: 1041, user: 'user', command: 'cyberdyne-shell', base: 1.2 },
	{ pid: 1188, user: 'postgres', command: 'postgres', base: 3.1 },
	{ pid: 1322, user: 'root', command: 'nginx', base: 0.7 },
	{ pid: 1567, user: 'user', command: 'matlab-llvm', base: 18 },
	{ pid: 1788, user: 'user', command: 'top', base: 0.5 }
];

export class TopModel {
	private rng: Rng;
	private uptimeMin = 137;
	processes: Process[];
	ticks = 0;

	constructor(rng: Rng = Math.random) {
		this.rng = rng;
		this.processes = ROSTER.map((p) => ({
			pid: p.pid,
			user: p.user,
			pr: 20,
			ni: 0,
			virt: 100000 + Math.floor(p.pid * 137),
			res: 20000 + Math.floor(p.pid * 31),
			cpu: p.base,
			mem: Math.min(40, p.base * 0.6 + 0.4),
			time: '0:0' + (p.pid % 9),
			command: p.command
		}));
	}

	private jitter(base: number, spread: number): number {
		const delta = (this.rng() - 0.5) * 2 * spread;
		return Math.max(0, Math.round((base + delta) * 10) / 10);
	}

	tick(): void {
		this.ticks += 1;
		for (let i = 0; i < this.processes.length; i++) {
			const p = this.processes[i];
			const base = ROSTER[i].base;
			p.cpu = this.jitter(base, Math.max(0.5, base * 0.35));
			p.mem = Math.min(40, this.jitter(base * 0.6 + 0.4, 0.3));
		}
		// Keep the heaviest hitters on top, like real top's %CPU sort.
		this.processes.sort((a, b) => b.cpu - a.cpu);
	}

	totalCpu(): number {
		return Math.round(this.processes.reduce((s, p) => s + p.cpu, 0) * 10) / 10;
	}

	render(): string {
		const load = (this.totalCpu() / 100).toFixed(2);
		const up = `${Math.floor(this.uptimeMin / 60)}:${String(this.uptimeMin % 60).padStart(2, '0')}`;
		const running = 1;
		const total = this.processes.length + 78; // pretend there are background tasks
		const cpuPct = Math.min(100, this.totalCpu()).toFixed(1);
		const idle = (100 - Math.min(100, this.totalCpu())).toFixed(1);

		const header = [
			`top - up ${up},  1 user,  load average: ${load}, ${(Number(load) * 0.9).toFixed(2)}, ${(Number(load) * 0.8).toFixed(2)}`,
			`Tasks: ${total} total,   ${running} running, ${total - running} sleeping,   0 stopped,   0 zombie`,
			`%Cpu(s): ${cpuPct.padStart(5)} us,  1.2 sy,  0.0 ni, ${idle.padStart(5)} id,  0.0 wa`,
			`MiB Mem :  16039.0 total,   4821.3 free,   6210.7 used,   5007.0 buff/cache`,
			`MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   9102.4 avail Mem`,
			''
		];

		const colHead = '  PID USER      PR  NI    VIRT    RES   %CPU  %MEM     TIME+ COMMAND';
		const rows = this.processes.map((p) => {
			return (
				String(p.pid).padStart(5) +
				' ' +
				p.user.padEnd(9) +
				String(p.pr).padStart(3) +
				String(p.ni).padStart(4) +
				String(p.virt).padStart(8) +
				String(p.res).padStart(7) +
				p.cpu.toFixed(1).padStart(7) +
				p.mem.toFixed(1).padStart(6) +
				('  ' + p.time).padStart(10) +
				' ' +
				p.command
			);
		});
		return [...header, colHead, ...rows].join('\n');
	}
}
