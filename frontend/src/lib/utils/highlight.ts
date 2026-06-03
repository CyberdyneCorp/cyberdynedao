/**
 * Tiny syntax-highlighting helper around highlight.js.
 *
 * Registers only the languages the academy uses (keeps the bundle lean):
 * MATLAB, Python, (System)Verilog, C, C++, Bash, TypeScript, JavaScript.
 * Used by the editable code-lesson editor and to colour fenced code blocks
 * in markdown lessons. Pair with a light hljs theme (imported globally in
 * +layout.svelte).
 */
import hljs from 'highlight.js/lib/core';
import matlab from 'highlight.js/lib/languages/matlab';
import python from 'highlight.js/lib/languages/python';
import verilog from 'highlight.js/lib/languages/verilog';
import c from 'highlight.js/lib/languages/c';
import cpp from 'highlight.js/lib/languages/cpp';
import bash from 'highlight.js/lib/languages/bash';
import typescript from 'highlight.js/lib/languages/typescript';
import javascript from 'highlight.js/lib/languages/javascript';

hljs.registerLanguage('matlab', matlab);
hljs.registerLanguage('python', python);
hljs.registerLanguage('verilog', verilog);
hljs.registerLanguage('c', c);
hljs.registerLanguage('cpp', cpp);
hljs.registerLanguage('bash', bash);
hljs.registerLanguage('typescript', typescript);
hljs.registerLanguage('javascript', javascript);

// Map the names authors actually type (fence labels / lesson language) to
// the registered grammar.
hljs.registerAliases(['systemverilog', 'sv'], { languageName: 'verilog' });
hljs.registerAliases(['c++', 'cxx', 'cc'], { languageName: 'cpp' });
hljs.registerAliases(['octave', 'm'], { languageName: 'matlab' });
hljs.registerAliases(['py'], { languageName: 'python' });
hljs.registerAliases(['js'], { languageName: 'javascript' });
hljs.registerAliases(['ts'], { languageName: 'typescript' });
hljs.registerAliases(['sh', 'shell', 'zsh'], { languageName: 'bash' });

function escapeHtml(s: string): string {
	return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** Highlight `code` as `lang`, returning HTML. Falls back to escaped plain
 * text for unknown/empty languages. */
export function highlight(code: string, lang?: string): string {
	const name = (lang ?? '').toLowerCase().trim();
	if (name && hljs.getLanguage(name)) {
		try {
			return hljs.highlight(code, { language: name, ignoreIllegals: true }).value;
		} catch {
			/* fall through */
		}
	}
	return escapeHtml(code);
}

/** Highlight a rendered `<code class="language-x">` element in place
 * (used for markdown code fences). Safe to call repeatedly. */
export function highlightElement(el: HTMLElement): void {
	try {
		delete el.dataset.highlighted;
		hljs.highlightElement(el);
	} catch {
		/* leave as-is */
	}
}

/** Whether we have a grammar for this language (after alias resolution). */
export function isSupportedLanguage(lang?: string): boolean {
	return !!(lang && hljs.getLanguage(lang.toLowerCase().trim()));
}
