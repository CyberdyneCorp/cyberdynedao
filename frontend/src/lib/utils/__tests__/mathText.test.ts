import { describe, expect, it } from 'vitest';
import { parseInlineMath } from '../mathText';

describe('parseInlineMath', () => {
	it('returns a single text run when there is no inline math', () => {
		expect(parseInlineMath('plain prose')).toEqual([{ kind: 'text', text: 'plain prose' }]);
	});

	it('splits inline \\( … \\) math from surrounding text', () => {
		expect(parseInlineMath('for any angle \\(x\\) here')).toEqual([
			{ kind: 'text', text: 'for any angle ' },
			{ kind: 'math', code: 'x' },
			{ kind: 'text', text: ' here' }
		]);
	});

	it('handles multiple inline formulas', () => {
		expect(parseInlineMath('\\(a\\) and \\(b^2\\)')).toEqual([
			{ kind: 'math', code: 'a' },
			{ kind: 'text', text: ' and ' },
			{ kind: 'math', code: 'b^2' }
		]);
	});

	it('does not treat single-$ as math', () => {
		expect(parseInlineMath('costs $5 and $10')).toEqual([{ kind: 'text', text: 'costs $5 and $10' }]);
	});

	it('keeps empty \\(\\) as literal text', () => {
		expect(parseInlineMath('empty \\(\\) here')).toEqual([
			{ kind: 'text', text: 'empty ' },
			{ kind: 'text', text: '\\(\\)' },
			{ kind: 'text', text: ' here' }
		]);
	});
});
