/**
 * Prepares a user-attached file for the agent's interpreter workspace.
 *
 * The sandbox has pandas/numpy but NO PDF parser, so a PDF can't be read
 * there. We extract its text in the browser (pdf.js, lazily imported) and
 * upload that as a `.txt` the agent can `open()`. Everything else (CSV, code,
 * plain text, JSON) is uploaded as-is. The original filename is kept for
 * display so the user still sees "CV.pdf" on the chip.
 */

export interface PreparedUpload {
	/** What actually gets written to the interpreter workspace. */
	blob: Blob;
	/** Filename used in the workspace (and given to the agent to read). */
	uploadName: string;
	/** Original filename, shown to the user. */
	displayName: string;
	/** True when we converted a binary doc to extracted text. */
	extracted: boolean;
}

function stripExt(name: string): string {
	const i = name.lastIndexOf('.');
	return i > 0 ? name.slice(0, i) : name;
}

function isPdf(file: File): boolean {
	return file.type === 'application/pdf' || /\.pdf$/i.test(file.name);
}

/** Extract a PDF's text layer with pdf.js. Returns '' for scanned/imageonly
 *  PDFs (no extractable text). pdf.js is heavy, so it's imported on demand. */
export async function extractPdfText(file: File): Promise<string> {
	const pdfjs = await import('pdfjs-dist');
	const workerUrl = (await import('pdfjs-dist/build/pdf.worker.min.mjs?url')).default;
	pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;
	const data = new Uint8Array(await file.arrayBuffer());
	const doc = await pdfjs.getDocument({ data }).promise;
	const pages: string[] = [];
	for (let i = 1; i <= doc.numPages; i++) {
		const page = await doc.getPage(i);
		const content = await page.getTextContent();
		const line = content.items
			.map((it) => ('str' in it ? it.str : ''))
			.join(' ')
			.replace(/\s+/g, ' ')
			.trim();
		if (line) pages.push(`--- page ${i} ---\n${line}`);
	}
	return pages.join('\n\n');
}

export async function prepareUpload(file: File): Promise<PreparedUpload> {
	if (isPdf(file)) {
		try {
			const text = await extractPdfText(file);
			if (text.trim()) {
				return {
					blob: new Blob([text], { type: 'text/plain' }),
					uploadName: `${stripExt(file.name)}.txt`,
					displayName: file.name,
					extracted: true
				};
			}
		} catch {
			/* fall through — upload the original and let the agent report it */
		}
	}
	return { blob: file, uploadName: file.name, displayName: file.name, extracted: false };
}
