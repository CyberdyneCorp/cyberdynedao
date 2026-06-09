import { type Page, type TestInfo, expect } from '@playwright/test';

/**
 * Stub every backend call so the shell + window chrome render deterministically
 * and offline. These responsive specs assert layout/structure (the part of the
 * UI/UX that must not break on small screens), not live data — so we short-circuit
 * the dev-server proxy instead of hitting the real CyberdyneAuth / MATLAB / etc.
 * upstreams, which would make the suite slow and flaky.
 *
 * Bodies are intentionally permissive: `[]` reads as an empty list, `{}` as an
 * empty object. Views are wrapped in ErrorBoundary in the shell, so even an
 * unexpected shape degrades to an in-window message without taking the shell down.
 */
export async function stubBackend(page: Page): Promise<void> {
	await page.route('**/api/**', async (route) => {
		const url = route.request().url();
		// List-shaped endpoints get an array; everything else an empty object.
		const looksLikeList = /(courses|products|items|news|posts|teams?|investments|list|messages|sessions)/i.test(url);
		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: looksLikeList ? '[]' : '{}'
		});
	});
}

/**
 * Navigate to the app, collecting any uncaught page errors. Returns the error
 * sink so a test can assert the boot was clean.
 */
export async function bootApp(page: Page): Promise<string[]> {
	const pageErrors: string[] = [];
	page.on('pageerror', (err) => pageErrors.push(err.message));
	await stubBackend(page);
	await page.goto('/', { waitUntil: 'domcontentloaded' });
	await expect(page.locator('.cyberdyne-retro-shell')).toBeVisible();
	// Wait for the launcher grid to render so interactions land after hydration
	// has wired up the shell's click handlers (avoids first-click races).
	await expect(page.locator('.cy-dgrid .cy-dicon').first()).toBeVisible();
	return pageErrors;
}

/**
 * Assert the document does not scroll horizontally — the single most reliable
 * signal that something overflowed the viewport and broke a small-screen layout.
 * A 2px tolerance absorbs sub-pixel rounding.
 */
export async function expectNoHorizontalOverflow(page: Page): Promise<void> {
	const overflow = await page.evaluate(() => {
		const el = document.documentElement;
		return { scrollWidth: el.scrollWidth, clientWidth: el.clientWidth };
	});
	expect(
		overflow.scrollWidth,
		`page overflows horizontally: scrollWidth=${overflow.scrollWidth} > clientWidth=${overflow.clientWidth}`
	).toBeLessThanOrEqual(overflow.clientWidth + 2);
}

/**
 * Assert an element's box fits inside the viewport (no clipping off-screen to the
 * right or bottom of the initial fold by more than `tolerance`).
 */
export async function expectFitsViewport(page: Page, selector: string, tolerance = 4): Promise<void> {
	const box = await page.locator(selector).first().boundingBox();
	const vp = page.viewportSize();
	expect(box, `expected ${selector} to have a bounding box`).not.toBeNull();
	expect(vp, 'expected a viewport size').not.toBeNull();
	if (!box || !vp) return;
	expect(box.x, `${selector} left edge off-screen`).toBeGreaterThanOrEqual(-tolerance);
	expect(box.width, `${selector} wider than viewport`).toBeLessThanOrEqual(vp.width + tolerance);
	expect(box.x + box.width, `${selector} right edge past viewport`).toBeLessThanOrEqual(vp.width + tolerance);
}

/**
 * Assert an element does not scroll horizontally — i.e. its own content fits
 * within its box. Catches inner overflow that page-level checks miss (e.g. a
 * window body whose content spills past the right edge and gets clipped).
 */
export async function expectNoInnerHorizontalOverflow(
	page: Page,
	selector: string,
	tolerance = 2
): Promise<void> {
	const m = await page.locator(selector).first().evaluate((el) => ({
		scrollWidth: el.scrollWidth,
		clientWidth: el.clientWidth
	}));
	expect(
		m.scrollWidth,
		`${selector} content overflows horizontally: scrollWidth=${m.scrollWidth} > clientWidth=${m.clientWidth}`
	).toBeLessThanOrEqual(m.clientWidth + tolerance);
}

/**
 * Resolve the topmost element at a viewport point and report whether it lies
 * within `ancestorSelector`. Used to prove stacking order (e.g. that a modal
 * overlay actually sits above the desktop icons).
 */
export async function topElementIsWithin(
	page: Page,
	x: number,
	y: number,
	ancestorSelector: string
): Promise<boolean> {
	return page.evaluate(
		({ x, y, ancestorSelector }) => {
			const el = document.elementFromPoint(x, y);
			return !!el && !!el.closest(ancestorSelector);
		},
		{ x, y, ancestorSelector }
	);
}

/** Attach a desktop screenshot to the report as visual evidence of the layout. */
export async function attachScreenshot(page: Page, testInfo: TestInfo, name: string): Promise<void> {
	const buf = await page.screenshot({ fullPage: false });
	await testInfo.attach(name, { body: buf, contentType: 'image/png' });
}
