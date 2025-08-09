<script lang="ts">
	interface NewsItem {
		title: string;
		source: string;
		author: string;
		image?: string;
	}

	const newsItems: NewsItem[] = [
		{
			title: 'Cyan Banister — From Homeless and Broke to Top Angel Investor...',
			source: '4',
			author: 'Tim Ferriss',
			image: 'https://images.unsplash.com/photo-1494790108755-2616c1f3c85d?w=150&h=150&fit=crop&crop=face'
		},
		{
			title: 'Cyan Banister, Arielle Zuckerberg Raise $181 Million to Back "Magi...',
			source: 'B',
			author: 'Lizette Chapman',
			image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
		},
		{
			title: 'Zivity founder finally takes it all off',
			source: 'VB',
			author: 'Paul Boutin',
			image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face'
		},
		{
			title: 'JFK Files, Nvidia\'s New Chip, Taco Bell AI, Intel CEO | Wed, March 19',
			source: '📺',
			author: 'TBPN',
			image: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=150&h=150&fit=crop'
		},
		{
			title: 'LA\'s Wildfire Disaster, Zuck Flips on Free Speech, Why Trump Wants...',
			source: '📺',
			author: 'All-In Podcast',
			image: 'https://images.unsplash.com/photo-1611348586804-61bf6c080437?w=150&h=150&fit=crop'
		},
		{
			title: 'News Panel with Cyan Banister and Erik Lanigan - TWiST #225',
			source: '📺',
			author: 'This Week in Startups',
			image: 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=150&h=150&fit=crop'
		}
	];
</script>

<div class="news-container">
	{#each newsItems as item}
		<article class="news-item">
			<img 
				src={item.image} 
				alt={item.title} 
				class="news-image"
			/>
			<div class="news-content">
				<h3 class="news-title">{item.title}</h3>
				<div class="news-meta">
					<span class="news-source">{item.source}</span>
					<span>•</span>
					<span class="news-author">{item.author}</span>
				</div>
			</div>
		</article>
	{/each}
</div>

<style>
	.news-container {
		padding: 16px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	
	.news-item {
		display: flex;
		gap: 16px;
		padding: 16px;
		border-bottom: 1px solid #e5e7eb;
		cursor: pointer;
		transition: background-color 0.15s ease;
	}
	
	.news-item:hover {
		background-color: #f9fafb;
	}
	
	.news-image {
		width: 80px;
		height: 80px;
		object-fit: cover;
		border: 2px solid #000;
		border-radius: 4px;
		flex-shrink: 0;
	}
	
	.news-content {
		flex: 1;
		min-width: 0;
	}
	
	.news-title {
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-weight: 700;
		font-size: 18px;
		line-height: 1.25;
		margin-bottom: 8px;
	}
	
	.news-meta {
		display: flex;
		align-items: center;
		gap: 8px;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-size: 14px;
		color: #6b7280;
	}
	
	.news-source {
		background: #dbeafe;
		color: #2563eb;
		padding: 4px 8px;
		border-radius: 4px;
		border: 1px solid #d1d5db;
		font-weight: 700;
	}
</style>