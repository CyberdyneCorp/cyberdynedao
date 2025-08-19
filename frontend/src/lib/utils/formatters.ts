/**
 * Utility functions for formatting data consistently across components
 */

/**
 * Formats a date string into a readable format
 */
export function formatDate(dateString: string): string {
	return new Date(dateString).toLocaleDateString('en-US', { 
		year: 'numeric', 
		month: 'short', 
		day: 'numeric' 
	});
}

/**
 * Formats a Date object into a readable format
 */
export function formatDateObject(date: Date): string {
	return date.toLocaleDateString('en-US', {
		month: 'short',
		day: 'numeric',
		year: 'numeric'
	});
}

/**
 * Formats currency values
 */
export function formatPrice(price: number): string {
	return price >= 1000 ? `$${(price / 1000).toFixed(1)}k` : `$${price}`;
}

/**
 * Formats large numbers with appropriate suffixes
 */
export function formatNumber(num: number): string {
	if (num >= 1000000) {
		return `${(num / 1000000).toFixed(1)}M`;
	} else if (num >= 1000) {
		return `${(num / 1000).toFixed(1)}K`;
	}
	return num.toString();
}

/**
 * Formats percentage values
 */
export function formatPercentage(value: number): string {
	return `${value.toFixed(2)}%`;
}

/**
 * Truncates text to a specified length with ellipsis
 */
export function truncateText(text: string, maxLength: number): string {
	return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}