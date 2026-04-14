export interface LiquidityPosition {
	id: string;
	pair: string;
	token0: string;
	token1: string;
	token0Logo: string;
	token1Logo: string;
	totalValue: number;
	minPrice: number;
	maxPrice: number;
	currentPrice: number;
	feeAPY: number;
	pooledAssets: {
		token0Amount: number;
		token1Amount: number;
	};
	totalPnL: number;
	totalAPR: number;
	uncollectedFees: number;
	status: 'in-range' | 'out-of-range';
	compound: boolean;
}

export const liquidityPositions: LiquidityPosition[] = [
	{
		id: 'pos-1',
		pair: 'WETH/USDC',
		token0: 'WETH',
		token1: 'USDC',
		token0Logo: '🔷',
		token1Logo: '💵',
		totalValue: 12607.79,
		minPrice: 3099.514,
		maxPrice: 4101.002,
		currentPrice: 4601.119,
		feeAPY: 68.43,
		pooledAssets: { token0Amount: 3.2, token1Amount: 316.96 },
		totalPnL: -316.96,
		totalAPR: -46.59,
		uncollectedFees: 7.91,
		status: 'out-of-range',
		compound: true
	},
	{
		id: 'pos-2',
		pair: 'UNI/WETH',
		token0: 'UNI',
		token1: 'WETH',
		token0Logo: '🦄',
		token1Logo: '🔷',
		totalValue: 8450.32,
		minPrice: 0.0032,
		maxPrice: 0.0045,
		currentPrice: 0.0039,
		feeAPY: 24.8,
		pooledAssets: { token0Amount: 1250.5, token1Amount: 1.85 },
		totalPnL: 125.43,
		totalAPR: 12.4,
		uncollectedFees: 15.23,
		status: 'in-range',
		compound: false
	},
	{
		id: 'pos-3',
		pair: 'USDC/USDT',
		token0: 'USDC',
		token1: 'USDT',
		token0Logo: '💵',
		token1Logo: '💚',
		totalValue: 15000.0,
		minPrice: 0.998,
		maxPrice: 1.002,
		currentPrice: 0.9995,
		feeAPY: 8.2,
		pooledAssets: { token0Amount: 7500.25, token1Amount: 7499.75 },
		totalPnL: 45.8,
		totalAPR: 8.2,
		uncollectedFees: 12.34,
		status: 'in-range',
		compound: true
	},
	{
		id: 'pos-4',
		pair: 'ARB/WETH',
		token0: 'ARB',
		token1: 'WETH',
		token0Logo: '🔵',
		token1Logo: '🔷',
		totalValue: 5234.67,
		minPrice: 0.00045,
		maxPrice: 0.00065,
		currentPrice: 0.00052,
		feeAPY: 45.6,
		pooledAssets: { token0Amount: 5000.0, token1Amount: 1.15 },
		totalPnL: -89.23,
		totalAPR: -8.5,
		uncollectedFees: 28.45,
		status: 'in-range',
		compound: true
	}
];
