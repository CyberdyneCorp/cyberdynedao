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

### Web3 Integration
- **Dual Wallet Support**: Both WalletConnect (mobile wallets) and Web3Auth (social login)
- **Base Network**: Configured for Base mainnet with Infura RPC
- **ERC-20 Support**: Token balance and transfer capabilities
- **Reactive State**: Real-time wallet connection status and balance updates

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

## 🔐 Web3 Configuration

### Environment Setup

Create a `.env` file with the following variables:

```env
# Infura Configuration (Base Network)
VITE_INFURA_API_KEY=ae1053a98c944d53968e5d725319be8f
VITE_INFURA_ENDPOINT=https://base-mainnet.infura.io/v3/ae1053a98c944d53968e5d725319be8f

# Base Network Configuration
VITE_CHAIN_ID=8453
VITE_NETWORK_NAME=Base Mainnet
VITE_NATIVE_CURRENCY=ETH

# WalletConnect (Reown AppKit)
VITE_REOWN_PROJECT_ID=your_reown_project_id

# Web3Auth
VITE_WEB3AUTH_CLIENT_ID=your_web3auth_client_id
```

### Getting API Keys

1. **Reown Project ID**:
   - Visit [WalletConnect Cloud](https://cloud.walletconnect.com/)
   - Create a new project
   - Copy the Project ID

2. **Web3Auth Client ID**:
   - Visit [Web3Auth Dashboard](https://dashboard.web3auth.io/)
   - Create a new project
   - Copy the Client ID

### Wallet Connection Options

The application provides two wallet connection methods:

#### 1. WalletConnect (Mobile Wallets)
- **QR Code Scanning**: Perfect for mobile wallets like MetaMask Mobile
- **Multi-Wallet Support**: Works with 50+ popular wallets
- **Cross-Platform**: Connect from any device

#### 2. Web3Auth (Social Login)  
- **Google Authentication**: Sign in with your Google account
- **Email/Password**: Passwordless email authentication
- **Social Providers**: Support for multiple OAuth providers

### Usage

The wallet connection modal automatically appears when users click "Connect Wallet". Users can choose between:
- **WalletConnect**: Displays QR code for mobile wallet scanning
- **Web3Auth**: Opens social authentication modal

Both methods provide:
- Real-time balance updates
- Network switching to Base
- Transaction signing capabilities
- Secure session management

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

## 🌐 Web3 Integration

This application is integrated with **Base Network** using **ethers.js** for Web3 functionality.

### Environment Setup

Create a `.env` file in the project root:

```env
# Infura Configuration
VITE_INFURA_API_KEY=your_infura_api_key
VITE_INFURA_ENDPOINT=https://base-mainnet.infura.io/v3/your_infura_api_key

# Base Network Configuration
VITE_CHAIN_ID=8453
VITE_NETWORK_NAME=Base Mainnet
VITE_NATIVE_CURRENCY=ETH

# App Configuration
VITE_APP_NAME=Cyberdyne DAO Terminal
VITE_APP_ENV=development
```

### Web3 Features

- **🔗 Wallet Connection**: Connect MetaMask and other Web3 wallets
- **🌐 Base Network**: Configured for Base mainnet (Chain ID: 8453)  
- **💰 Balance Display**: Real-time ETH balance updates
- **🔄 Network Switching**: Automatic network switching to Base
- **📱 Responsive**: Works on desktop and mobile Web3 browsers
- **⚡ Transaction Support**: Send transactions and interact with contracts
- **🎯 Contract Integration**: ERC-20 token support with standard methods

### Usage Examples

```typescript
// Connect wallet
import { web3Actions, walletInfo } from '$lib/stores/web3Store';
await web3Actions.connectWallet();

// Check connection status
$: console.log('Connected:', $walletInfo?.isConnected);

// Get token balance
import { contractManager } from '$lib/web3/contracts';
const balance = await contractManager.getTokenBalance(tokenAddress, userAddress);

// Send transaction  
import { walletManager } from '$lib/web3/wallet';
const txHash = await walletManager.sendTransaction(to, value);
```

### Web3 Architecture

```
src/lib/web3/
├── config.ts          # Network configuration & provider setup
├── wallet.ts          # Wallet connection & management
├── contracts.ts       # Smart contract interactions
└── stores/
    └── web3Store.ts   # Svelte stores for Web3 state
```

## 🔧 Technologies

- **Frontend**: SvelteKit, TypeScript
- **Web3**: ethers.js, Base Network, Infura
- **Styling**: Tailwind CSS, Custom CSS animations
- **Build**: Vite, SvelteKit Static Adapter
- **Deployment**: IPFS, Static hosting
- **Assets**: SVG icons, WebP images

---

Built with ❤️ for the Cyberdyne DAO community
