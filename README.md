# Cyberdyne DAO Terminal

A futuristic terminal-style application built with SvelteKit, featuring background animations, ASCII art, and a retro computing aesthetic inspired by Cyberdyne Systems.

## ✨ Features

### Visual & UX
- **Futuristic Background Animations**: Cyber grid patterns, glowing particles, and digital rain effects
- **ASCII Cyberdyne Logo**: Large animated logo with wavy glow effects
- **Retro Terminal Interface**: Authentic terminal emulation with green phosphor styling
- **Glassmorphism UI**: Modern glass-style navigation with backdrop blur effects
- **Interactive Desktop Icons**: Grid-based navigation system with hover animations
- **Draggable Windows**: Multi-window interface with resize functionality

### Technical
- **TypeScript**: Full type safety across the application
- **Modular Architecture**: Well-organized component and utility structure
- **Responsive Design**: Mobile-friendly layout with adaptive components
- **Shopping Cart**: E-commerce functionality with cart management
- **Team Profiles**: Dynamic team member showcase with images and skills

## 🛠️ Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🌐 IPFS Deployment

This application is configured for static deployment to IPFS using SvelteKit's static adapter.

### Quick Deploy

```bash
# Build for IPFS deployment
npm run build:ipfs

# Preview IPFS build locally
npm run preview:ipfs
```

### IPFS Configuration

The application uses `@sveltejs/adapter-static` with the following IPFS-optimized settings:

- **Static Generation**: All routes are pre-rendered at build time
- **Relative Paths**: Uses relative paths for better IPFS compatibility
- **Fallback Handling**: Includes `index.html` fallback for SPA routing
- **Asset Optimization**: Assets are bundled into the `build/` directory

### Deployment Options

#### Option 1: IPFS Desktop/CLI
```bash
# Build the application
npm run build:ipfs

# Add to IPFS (using IPFS CLI)
ipfs add -r build/

# Or using IPFS Desktop: drag the build/ folder into IPFS Desktop
```

#### Option 2: Pinata/Fleek
1. Build the application: `npm run build:ipfs`
2. Upload the `build/` folder to your preferred IPFS pinning service
3. Access your app via the generated IPFS hash

#### Option 3: Web3.Storage/NFT.Storage
```bash
# Build the application  
npm run build:ipfs

# Upload using w3cli (install with: npm install -g @web3-storage/w3cli)
w3 put build/
```

### IPFS Gateway Access

Once deployed, access your app through IPFS gateways:
- `https://ipfs.io/ipfs/YOUR_HASH`
- `https://gateway.pinata.cloud/ipfs/YOUR_HASH`
- `https://YOUR_HASH.ipfs.dweb.link`

### Static Build Configuration

The static adapter is configured in `svelte.config.js`:

```javascript
adapter: adapter({
  pages: 'build',
  assets: 'build', 
  fallback: 'index.html',
  precompress: false,
  strict: true
})
```

### Important Notes for IPFS

- ✅ All routes are pre-rendered for static hosting
- ✅ Uses relative paths for IPFS compatibility
- ✅ Includes fallback routing for SPA navigation
- ✅ Assets are self-contained in the build directory
- ✅ No server-side functionality required

## 📁 Project Structure

```
src/
├── lib/
│   ├── components/          # Svelte components
│   │   ├── Window.svelte    # Draggable window system
│   │   ├── TopBar.svelte    # Navigation header
│   │   ├── Terminal.svelte  # Terminal emulator
│   │   ├── TeamView.svelte  # Team member profiles
│   │   └── ...
│   ├── constants/           # App constants
│   │   ├── navigation.ts    # Navigation menu items
│   │   └── asciiLogo.ts     # ASCII art constants
│   ├── styles/              # CSS modules
│   │   └── backgroundAnimations.css
│   ├── types/               # TypeScript interfaces
│   │   └── cart.ts          # Shopping cart types
│   ├── utils/               # Utility functions
│   │   ├── navigationHelpers.ts
│   │   └── terminalCommands.ts
│   └── stores/              # Svelte stores
│       └── windowStore.ts   # Window management
├── routes/                  # SvelteKit pages
│   ├── +layout.svelte      # App layout
│   └── +page.svelte        # Main page
└── app.css                 # Global styles & Tailwind
```

## 🎨 Assets

### Icons & Images
Located in `/static/assets/`:
- **Navigation Icons**: `blockchain_icon.svg`, `crypto_icon.svg`, `products_icon.svg`, etc.
- **Team Photos**: Individual member photos in `team/` subdirectory
- **System Icons**: `favicon.svg`, `icon_menu.svg`, `icon_terminal.svg`

### Animations
- **Cyber Grid**: Moving grid pattern with pulse animation
- **Glow Particles**: Floating cyan particles with scaling effects
- **Digital Rain**: Matrix-style falling digital elements
- **ASCII Logo**: Breathing and wavy glow text effects

## 🚀 Key Components

### Window System
- Draggable windows with title bars
- Resizable window handles
- Focus management and z-index stacking
- Multiple window types (Terminal, Team, Products, etc.)

### Background Animations
- Modular CSS architecture in `/lib/styles/`
- Hardware-accelerated animations
- Configurable opacity and timing
- Performance-optimized with minimal DOM impact

### Terminal Interface
- Command history and auto-completion
- Authentic retro phosphor styling
- Interactive command processing
- Scrollable output with custom scrollbars

## 🎯 Architecture Highlights

- **Clean Separation**: Logic, styles, and constants properly modularized
- **Type Safety**: Comprehensive TypeScript interfaces throughout
- **Reusable Utilities**: Shared functions eliminate code duplication
- **Modern CSS**: CSS Grid, Flexbox, and CSS animations
- **Component Composition**: Flexible, composable Svelte components

## 📝 Recent Improvements

- ✅ Extracted background animations to separate CSS module
- ✅ Created shared navigation utilities to reduce duplication  
- ✅ Implemented proper TypeScript interfaces for cart system
- ✅ Organized constants and ASCII art into dedicated files
- ✅ Removed unused components and optimized asset usage
- ✅ Enhanced build process and code organization

## 🔧 Technologies

- **Frontend**: SvelteKit, TypeScript
- **Styling**: Tailwind CSS, Custom CSS animations
- **Build**: Vite, SvelteKit Static Adapter
- **Deployment**: IPFS, Static hosting
- **Assets**: SVG icons, WebP images

---

Built with ❤️ for the Cyberdyne DAO community
