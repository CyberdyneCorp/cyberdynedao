<script lang="ts">
	import { teamMembers } from '$lib/data/team';

	const paletteClasses = {
		purple: {
			card: 'from-purple-50 to-purple-100 border-purple-200',
			title: 'text-purple-800',
			role: 'text-purple-600',
			border: 'border-purple-300',
			tagsWrap: 'bg-purple-100 border-purple-300',
			tag: 'bg-purple-200 text-purple-800'
		},
		green: {
			card: 'from-green-50 to-green-100 border-green-200',
			title: 'text-green-800',
			role: 'text-green-600',
			border: 'border-green-300',
			tagsWrap: 'bg-green-100 border-green-300',
			tag: 'bg-green-200 text-green-800'
		},
		orange: {
			card: 'from-orange-50 to-orange-100 border-orange-200',
			title: 'text-orange-800',
			role: 'text-orange-600',
			border: 'border-orange-300',
			tagsWrap: 'bg-orange-100 border-orange-300',
			tag: 'bg-orange-200 text-orange-800'
		},
		blue: {
			card: 'from-blue-50 to-blue-100 border-blue-200',
			title: 'text-blue-800',
			role: 'text-blue-600',
			border: 'border-blue-300',
			tagsWrap: 'bg-blue-100 border-blue-300',
			tag: 'bg-blue-200 text-blue-800'
		}
	} as const;
</script>

<div class="team-container">
	<div class="header-section mb-8">
		<h1 class="text-3xl font-mono font-bold text-center mb-6">About Us</h1>
		<p class="text-lg text-center text-gray-700 mb-8 max-w-4xl mx-auto leading-relaxed">
			We are a team formed by developers and researchers in Artificial Intelligence and financial markets.
			Our goal is to offer courses and products in the areas of Finance, Blockchain, and Games.
		</p>
	</div>

	<div class="team-members">
		<h2 class="text-2xl font-mono font-bold text-center mb-8 text-blue-800">Meet Our Team</h2>

		<div class="members-grid grid grid-cols-1 gap-4">
			{#each teamMembers as member}
				{@const p = paletteClasses[member.palette]}
				<div class="member-card bg-gradient-to-br {p.card} p-4 rounded-lg border-2">
					<div class="flex items-start gap-4">
						<div class="member-image flex-shrink-0">
							<img src={member.image} alt={member.name} class="w-16 h-16 rounded-full object-cover border-2 {p.border} shadow-lg" />
						</div>
						<div class="flex-1">
							<h3 class="text-lg font-mono font-bold {p.title} mb-1">{member.name}</h3>
							<h4 class="text-xs font-semibold {p.role} mb-2 uppercase tracking-wide">{member.title}</h4>
							<p class="text-sm text-gray-700 leading-relaxed mb-2">{member.bio}</p>
							<div class="skills {p.tagsWrap} border rounded p-2 mt-2">
								<div class="flex flex-wrap gap-1">
									{#each member.tags as tag}
										<span class="px-2 py-1 {p.tag} text-xs font-semibold rounded">{tag}</span>
									{/each}
								</div>
							</div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<div class="cta-section mt-12 text-center">
		<div class="bg-gradient-to-r from-blue-50 to-purple-50 p-8 rounded-lg border-2 border-blue-200">
			<h3 class="text-xl font-mono font-bold text-blue-800 mb-4">Ready to Learn with Us?</h3>
			<p class="text-gray-700 mb-6 max-w-2xl mx-auto">
				Join our community and explore the exciting worlds of Finance, Blockchain, AI, and Game Development with our expert team.
			</p>
			<button class="px-6 py-3 bg-blue-600 text-white font-mono font-semibold rounded-lg hover:bg-blue-700 transition-colors">
				Get Started Today
			</button>
		</div>
	</div>
</div>

<style>
	.team-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
	.member-card { transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }
	.member-card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); }
	.member-image img { transition: transform 0.2s ease-in-out; }
	.member-card:hover .member-image img { transform: scale(1.05); }
</style>
