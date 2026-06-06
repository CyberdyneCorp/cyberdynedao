import { describe, expect, it, vi } from 'vitest';

// Stub pdf.js so prepareUpload's PDF branch is exercised without the real
// (worker-backed) library.
vi.mock('pdfjs-dist', () => ({
	GlobalWorkerOptions: { workerSrc: '' },
	getDocument: () => ({
		promise: Promise.resolve({
			numPages: 1,
			getPage: () =>
				Promise.resolve({
					getTextContent: () =>
						Promise.resolve({ items: [{ str: 'Hello' }, { str: 'CV' }] })
				})
		})
	})
}));
vi.mock('pdfjs-dist/build/pdf.worker.min.mjs?url', () => ({ default: 'worker.js' }));

import { prepareUpload } from '../fileAttachment';

describe('prepareUpload', () => {
	it('passes a non-PDF file through unchanged', async () => {
		const file = new File(['a,b\n1,2'], 'data.csv', { type: 'text/csv' });
		const prepared = await prepareUpload(file);
		expect(prepared.extracted).toBe(false);
		expect(prepared.uploadName).toBe('data.csv');
		expect(prepared.displayName).toBe('data.csv');
		expect(prepared.blob).toBe(file);
	});

	it('extracts text from a PDF and uploads it as .txt', async () => {
		const file = new File([new Uint8Array([1, 2, 3])], 'CV.pdf', { type: 'application/pdf' });
		const prepared = await prepareUpload(file);
		expect(prepared.extracted).toBe(true);
		expect(prepared.uploadName).toBe('CV.txt');
		expect(prepared.displayName).toBe('CV.pdf');
		expect(await prepared.blob.text()).toContain('Hello CV');
	});
});
