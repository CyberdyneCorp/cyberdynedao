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

<div class="p-4 flex flex-col gap-4">
	{#each newsItems as item}
		<article class="flex gap-4 p-4 border-b border-gray-200 cursor-pointer transition-colors duration-150 hover:bg-gray-50">
			<img 
				src={item.image} 
				alt={item.title} 
				class="w-20 h-20 object-cover border-2 border-black rounded flex-shrink-0"
			/>
			<div class="flex-1 min-w-0">
				<h3 class="font-mono font-bold text-lg leading-tight mb-2">{item.title}</h3>
				<div class="flex items-center gap-2 font-mono text-sm text-gray-600">
					<span class="bg-blue-100 text-blue-600 px-2 py-1 rounded border border-gray-300 font-bold">{item.source}</span>
					<span>•</span>
					<span>{item.author}</span>
				</div>
			</div>
		</article>
	{/each}
</div>

