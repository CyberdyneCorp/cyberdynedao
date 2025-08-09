<script lang="ts">
	// Investment portfolio view component
</script>

<div class="p-12 flex justify-center items-center">
	<div class="grid grid-cols-2 gap-x-20 gap-y-16 justify-items-center">
		<!-- Row 1 -->
		<div class="flex flex-col items-center gap-2 cursor-pointer">
			<div class="investment-icon folder-icon">
				<!-- Folder icon -->
				<div class="folder-tab"></div>
				<div class="folder-body">
					<div class="folder-line"></div>
					<div class="folder-line long"></div>
					<div class="folder-line medium"></div>
				</div>
			</div>
			<div class="px-2 py-1 bg-blue-400 border border-black shadow-sm text-center font-mono text-xs font-bold text-white">All</div>
		</div>

		<div class="flex flex-col items-center gap-2 cursor-pointer">
			<div class="investment-icon angel-icon">
				<!-- Angel/character icon -->
				<div class="angel-head"></div>
				<div class="angel-wing left"></div>
				<div class="angel-wing right"></div>
				<div class="angel-body"></div>
				<div class="angel-arm left"></div>
				<div class="angel-arm right"></div>
			</div>
			<div class="px-2 py-1 bg-blue-400 border border-black shadow-sm text-center font-mono text-xs font-bold text-white">Banister Angels</div>
		</div>

		<!-- Row 2 -->
		<div class="flex flex-col items-center gap-2 cursor-pointer">
			<div class="investment-icon folder-icon">
				<div class="folder-tab"></div>
				<div class="folder-body">
					<div class="folder-line"></div>
					<div class="folder-line long"></div>
					<div class="folder-line medium"></div>
				</div>
			</div>
			<div class="px-2 py-1 bg-blue-400 border border-black shadow-sm text-center font-mono text-xs font-bold text-white">Growth</div>
		</div>

		<div class="flex flex-col items-center gap-2 cursor-pointer">
			<div class="investment-icon chart-icon">
				<!-- Building/chart icon -->
				<div class="chart-bar short"></div>
				<div class="chart-bar tall"></div>
				<div class="chart-bar medium"></div>
				<div class="chart-bar mini"></div>
			</div>
			<div class="px-2 py-1 bg-blue-400 border border-black shadow-sm text-center font-mono text-xs font-bold text-white">Founders Fund</div>
		</div>

		<!-- Row 3 -->
		<div class="flex flex-col items-center gap-2 cursor-pointer">
			<div class="investment-icon eye-icon">
				<!-- Eye icon -->
				<div class="eye-outer">
					<div class="eye-inner">
						<div class="eye-pupil"></div>
					</div>
				</div>
			</div>
			<div class="px-2 py-1 bg-blue-400 border border-black shadow-sm text-center font-mono text-xs font-bold text-white">Long Journey</div>
		</div>

		<div class="flex flex-col items-center gap-2 cursor-pointer">
			<div class="investment-icon folder-icon">
				<div class="folder-tab"></div>
				<div class="folder-body">
					<div class="folder-line"></div>
					<div class="folder-line long"></div>
					<div class="folder-line medium"></div>
				</div>
			</div>
			<div class="px-2 py-1 bg-blue-400 border border-black shadow-sm text-center font-mono text-xs font-bold text-white">Exited</div>
		</div>
	</div>
</div>

<style>
	/* Keep only pixel art specific styles - layout handled by Tailwind */
	
	.folder-icon {
		background: #fed7aa;
	}
	
	.folder-tab {
		position: absolute;
		top: 8px;
		left: 8px;
		width: 56px;
		height: 8px;
		background: white;
		border: 1px solid #000;
	}
	
	.folder-body {
		position: absolute;
		top: 16px;
		left: 8px;
		width: 48px;
		height: 48px;
		background: #fdba74;
		border: 1px solid #000;
	}
	
	.folder-line {
		width: 12px;
		height: 4px;
		background: #000;
		margin: 8px 0 0 12px;
	}
	
	.folder-line.long {
		width: 32px;
	}
	
	.folder-line.medium {
		width: 24px;
	}
	
	.angel-icon {
		background: #fb923c;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.angel-head {
		position: absolute;
		top: 16px;
		left: 32px;
		width: 16px;
		height: 16px;
		background: #fde047;
		border: 1px solid #000;
	}
	
	.angel-wing {
		position: absolute;
		top: 24px;
		width: 8px;
		height: 12px;
		background: white;
		border: 1px solid #000;
	}
	
	.angel-wing.left {
		left: 16px;
	}
	
	.angel-wing.right {
		right: 16px;
	}
	
	.angel-body {
		position: absolute;
		top: 32px;
		left: 24px;
		width: 24px;
		height: 32px;
		background: #60a5fa;
		border: 1px solid #000;
	}
	
	.angel-arm {
		position: absolute;
		top: 40px;
		width: 8px;
		height: 8px;
		background: #fef08a;
		border: 1px solid #000;
	}
	
	.angel-arm.left {
		left: 16px;
	}
	
	.angel-arm.right {
		right: 16px;
	}
	
	.chart-icon {
		background: #f87171;
		display: flex;
		align-items: flex-end;
		justify-content: center;
		padding: 8px;
		gap: 4px;
	}
	
	.chart-bar {
		width: 8px;
		border: 1px solid #000;
	}
	
	.chart-bar.short {
		height: 16px;
		background: #dc2626;
	}
	
	.chart-bar.tall {
		height: 32px;
		background: #22d3ee;
	}
	
	.chart-bar.medium {
		height: 24px;
		background: #2563eb;
	}
	
	.chart-bar.mini {
		height: 12px;
		background: #6b7280;
	}
	
	.eye-icon {
		background: #3b82f6;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.eye-outer {
		width: 64px;
		height: 64px;
		background: #2563eb;
		border: 2px solid #000;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.eye-inner {
		width: 32px;
		height: 32px;
		background: white;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.eye-pupil {
		width: 16px;
		height: 16px;
		background: #000;
		border-radius: 50%;
	}
</style>