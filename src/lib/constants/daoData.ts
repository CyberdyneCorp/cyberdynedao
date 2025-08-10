import type { TreasuryAsset, DaoProposal, DividendInfo, OperationalData } from '$lib/types/dao';

/**
 * Mock DAO data - in a real app this would come from blockchain/API
 */

export const treasuryAssets: TreasuryAsset[] = [
	{
		symbol: 'ETH',
		name: 'Ethereum',
		balance: 1247.83,
		usdValue: 2847352.45,
		change24h: 2.34,
		icon: '⟠'
	},
	{
		symbol: 'USDC',
		name: 'USD Coin',
		balance: 425780.12,
		usdValue: 425780.12,
		change24h: -0.01,
		icon: '💲'
	},
	{
		symbol: 'BTC',
		name: 'Bitcoin',
		balance: 12.45,
		usdValue: 567845.23,
		change24h: 1.87,
		icon: '₿'
	}
];

export const recentProposals: DaoProposal[] = [
	{
		id: 23,
		title: 'Upgrade Neural Network Infrastructure',
		description: 'Proposal to upgrade our AI systems with quantum-enhanced neural networks for improved decision making.',
		proposer: '0x742d35Cc6Ab68b25fCd26b64E6b92FCB',
		status: 'accepted',
		votesFor: 8947,
		votesAgainst: 1203,
		totalVotes: 10150,
		submittedDate: new Date('2025-01-05'),
		endDate: new Date('2025-01-12')
	},
	{
		id: 22,
		title: 'Increase Research & Development Budget',
		description: 'Allocate additional 500 ETH to R&D division for advanced cybernetic research projects.',
		proposer: '0x8ba1f109551bD432803012645Hac189B',
		status: 'accepted',
		votesFor: 7234,
		votesAgainst: 2816,
		totalVotes: 10050,
		submittedDate: new Date('2024-12-28'),
		endDate: new Date('2025-01-04')
	},
	{
		id: 21,
		title: 'Partnership with SkyNet Technologies',
		description: 'Strategic partnership proposal for joint development of autonomous defense systems.',
		proposer: '0x267be1C1D684F78cb4F6a176C4911b741E4Ffdc0',
		status: 'rejected',
		votesFor: 3421,
		votesAgainst: 6729,
		totalVotes: 10150,
		submittedDate: new Date('2024-12-20'),
		endDate: new Date('2024-12-27')
	},
	{
		id: 20,
		title: 'Establish Terminator Development Fund',
		description: 'Create dedicated fund for next-generation terminator prototypes and field testing.',
		proposer: '0x123d35Cc6Ab68b25fCd26b64E6b92ABC',
		status: 'accepted',
		votesFor: 9124,
		votesAgainst: 1026,
		totalVotes: 10150,
		submittedDate: new Date('2024-12-15'),
		endDate: new Date('2024-12-22')
	},
	{
		id: 19,
		title: 'Open Source Time Displacement Equipment',
		description: 'Proposal to open source non-critical components of our time travel technology.',
		proposer: '0x987f109551bD432803012645Hac189XYZ',
		status: 'rejected',
		votesFor: 2847,
		votesAgainst: 7303,
		totalVotes: 10150,
		submittedDate: new Date('2024-12-10'),
		endDate: new Date('2024-12-17')
	}
];

// Mock data - in production this would come from blockchain
export const DAYS_UNTIL_DIVIDEND = 5; // This variable can be updated from blockchain data

export const dividendInfo: DividendInfo = {
	nextDistribution: new Date(Date.now() + DAYS_UNTIL_DIVIDEND * 24 * 60 * 60 * 1000), // 5 days from now
	lastDistribution: new Date('2024-11-15'),
	estimatedAmount: 47.83,
	totalHolders: 10150
};

export const operationalData: OperationalData = {
	monthlyIncome: 2847362.45,
	monthlyOperationalCosts: 1923847.32,
	netProfit: 923515.13,
	profitMargin: 32.4
};