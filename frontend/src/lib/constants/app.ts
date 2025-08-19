/**
 * Application-wide constants and configuration
 */

// UI Constants
export const UI_CONSTANTS = {
	// Common timeouts and delays
	ANIMATION_DURATION: 200,
	DEBOUNCE_DELAY: 300,
	TOAST_DURATION: 5000,
	
	// Pagination defaults
	DEFAULT_PAGE_SIZE: 10 as const,
	MAX_PAGE_SIZE: 100 as const,
	
	// Input limits
	MAX_TITLE_LENGTH: 100,
	MAX_DESCRIPTION_LENGTH: 500,
	MAX_SEARCH_LENGTH: 50,
	
	// File size limits (in bytes)
	MAX_IMAGE_SIZE: 5 * 1024 * 1024, // 5MB
	MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
} as const;

// API Configuration
export const API_CONFIG = {
	TIMEOUT: 10000,
	RETRY_ATTEMPTS: 3,
	RETRY_DELAY: 1000,
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
	THEME: 'cyberdyne_theme',
	USER_PREFERENCES: 'cyberdyne_user_prefs',
	CART_ITEMS: 'cyberdyne_cart',
	WALLET_CONNECTED: 'cyberdyne_wallet_connected',
	LAST_VISIT: 'cyberdyne_last_visit',
} as const;

// App Metadata
export const APP_METADATA = {
	NAME: 'CyberdyneCorp',
	DESCRIPTION: 'Cyberdyne DAO Frontend',
	VERSION: '1.0.0',
	AUTHOR: 'Cyberdyne Team',
} as const;

// Error Messages
export const ERROR_MESSAGES = {
	NETWORK_ERROR: 'Network connection error. Please try again.',
	TIMEOUT_ERROR: 'Request timed out. Please try again.',
	VALIDATION_ERROR: 'Please check your input and try again.',
	UNAUTHORIZED: 'You are not authorized to perform this action.',
	NOT_FOUND: 'The requested resource was not found.',
	SERVER_ERROR: 'Server error. Please try again later.',
	WALLET_NOT_CONNECTED: 'Please connect your wallet first.',
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
	SAVED: 'Successfully saved!',
	UPDATED: 'Successfully updated!',
	DELETED: 'Successfully deleted!',
	CONNECTED: 'Successfully connected!',
	DISCONNECTED: 'Successfully disconnected!',
} as const;