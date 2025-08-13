/**
 * DAO-related TypeScript interfaces
 */

export interface TreasuryAsset {
	symbol: string;
	name: string;
	balance: number;
	usdValue: number;
	change24h: number;
	icon?: string;
}

export interface DaoProposal {
	id: number;
	title: string;
	description: string;
	proposer: string;
	status: 'accepted' | 'rejected' | 'pending';
	votesFor: number;
	votesAgainst: number;
	totalVotes: number;
	submittedDate: Date;
	endDate: Date;
}

export interface DividendInfo {
	nextDistribution: Date;
	lastDistribution: Date;
	estimatedAmount: number;
	totalHolders: number;
}

export interface OperationalData {
	monthlyIncome: number;
	monthlyOperationalCosts: number;
	netProfit: number;
	profitMargin: number;
}