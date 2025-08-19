/**
 * API utility functions for consistent HTTP requests
 */

export interface ApiResponse<T = any> {
	data?: T;
	error?: string;
	status: number;
}

export interface RequestOptions {
	headers?: Record<string, string>;
	timeout?: number;
}

/**
 * Base API client class
 */
class ApiClient {
	private baseUrl: string;
	private defaultHeaders: Record<string, string>;

	constructor(baseUrl = '', defaultHeaders = {}) {
		this.baseUrl = baseUrl;
		this.defaultHeaders = {
			'Content-Type': 'application/json',
			...defaultHeaders
		};
	}

	/**
	 * Generic request method
	 */
	private async request<T>(
		endpoint: string,
		options: RequestInit = {},
		requestOptions: RequestOptions = {}
	): Promise<ApiResponse<T>> {
		const url = `${this.baseUrl}${endpoint}`;
		const { timeout = 10000 } = requestOptions;

		const config: RequestInit = {
			headers: {
				...this.defaultHeaders,
				...requestOptions.headers,
				...options.headers
			},
			...options
		};

		try {
			// Create abort controller for timeout
			const controller = new AbortController();
			const timeoutId = setTimeout(() => controller.abort(), timeout);

			const response = await fetch(url, {
				...config,
				signal: controller.signal
			});

			clearTimeout(timeoutId);

			if (!response.ok) {
				return {
					error: `HTTP ${response.status}: ${response.statusText}`,
					status: response.status
				};
			}

			const contentType = response.headers.get('content-type');
			let data: T;

			if (contentType?.includes('application/json')) {
				data = await response.json();
			} else {
				data = await response.text() as unknown as T;
			}

			return {
				data,
				status: response.status
			};
		} catch (error) {
			if (error instanceof Error && error.name === 'AbortError') {
				return {
					error: 'Request timeout',
					status: 408
				};
			}

			return {
				error: error instanceof Error ? error.message : 'Unknown error occurred',
				status: 0
			};
		}
	}

	/**
	 * GET request
	 */
	async get<T>(endpoint: string, options?: RequestOptions): Promise<ApiResponse<T>> {
		return this.request<T>(endpoint, { method: 'GET' }, options);
	}

	/**
	 * POST request
	 */
	async post<T>(
		endpoint: string, 
		data?: any, 
		options?: RequestOptions
	): Promise<ApiResponse<T>> {
		return this.request<T>(
			endpoint, 
			{
				method: 'POST',
				body: data ? JSON.stringify(data) : undefined
			}, 
			options
		);
	}

	/**
	 * PUT request
	 */
	async put<T>(
		endpoint: string, 
		data?: any, 
		options?: RequestOptions
	): Promise<ApiResponse<T>> {
		return this.request<T>(
			endpoint, 
			{
				method: 'PUT',
				body: data ? JSON.stringify(data) : undefined
			}, 
			options
		);
	}

	/**
	 * DELETE request
	 */
	async delete<T>(endpoint: string, options?: RequestOptions): Promise<ApiResponse<T>> {
		return this.request<T>(endpoint, { method: 'DELETE' }, options);
	}
}

// Export a default instance
export const api = new ApiClient();

// Export the class for custom instances
export { ApiClient };