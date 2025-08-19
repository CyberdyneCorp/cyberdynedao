/**
 * Utility functions for data validation
 */

export interface ValidationResult {
	isValid: boolean;
	errors: string[];
}

/**
 * Validates email format
 */
export function validateEmail(email: string): boolean {
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	return emailRegex.test(email);
}

/**
 * Validates that a string is not empty or just whitespace
 */
export function validateRequired(value: string): boolean {
	return value.trim().length > 0;
}

/**
 * Validates string length within bounds
 */
export function validateLength(
	value: string, 
	min: number, 
	max: number
): boolean {
	const length = value.trim().length;
	return length >= min && length <= max;
}

/**
 * Validates that a number is within a range
 */
export function validateNumberRange(
	value: number, 
	min: number, 
	max: number
): boolean {
	return value >= min && value <= max;
}

/**
 * Validates wallet address format (basic Ethereum address validation)
 */
export function validateWalletAddress(address: string): boolean {
	const ethAddressRegex = /^0x[a-fA-F0-9]{40}$/;
	return ethAddressRegex.test(address);
}

/**
 * Comprehensive validation for common form fields
 */
export function validateField(
	value: string, 
	type: 'email' | 'required' | 'wallet' | 'text',
	options?: { minLength?: number; maxLength?: number }
): ValidationResult {
	const errors: string[] = [];
	
	switch (type) {
		case 'required':
			if (!validateRequired(value)) {
				errors.push('This field is required');
			}
			break;
			
		case 'email':
			if (!validateRequired(value)) {
				errors.push('Email is required');
			} else if (!validateEmail(value)) {
				errors.push('Please enter a valid email address');
			}
			break;
			
		case 'wallet':
			if (!validateRequired(value)) {
				errors.push('Wallet address is required');
			} else if (!validateWalletAddress(value)) {
				errors.push('Please enter a valid wallet address');
			}
			break;
			
		case 'text':
			if (options?.minLength && !validateLength(value, options.minLength, options.maxLength || Infinity)) {
				errors.push(`Must be between ${options.minLength} and ${options.maxLength || 'unlimited'} characters`);
			}
			break;
	}
	
	return {
		isValid: errors.length === 0,
		errors
	};
}