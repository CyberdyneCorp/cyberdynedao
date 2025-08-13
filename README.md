# Cyberdyne DAO Terminal

A futuristic terminal-style application built with SvelteKit, featuring Web3Auth authentication, WalletConnect integration, and a retro cyberpunk aesthetic inspired by Cyberdyne Systems.

## 🏗️ Project Structure

This project is organized into a clean frontend-focused structure:

```
retro-terminal/
├── README.md                 # Project documentation
└── frontend/                 # Main application directory
    ├── Dockerfile            # Production Docker configuration
    ├── package.json          # Dependencies and scripts
    ├── svelte.config.js      # SvelteKit configuration
    ├── vite.config.ts        # Vite build configuration
    ├── tailwind.config.js    # Tailwind CSS configuration
    ├── .env                  # Environment variables
    ├── src/                  # Source code
    │   ├── app.html          # HTML template
    │   ├── app.css           # Global styles
    │   ├── lib/              # Shared libraries
    │   │   ├── components/   # Svelte components
    │   │   ├── web3/         # Web3Auth & wallet integration
    │   │   ├── stores/       # Svelte stores
    │   │   ├── utils/        # Utility functions
    │   │   └── types/        # TypeScript definitions
    │   └── routes/           # SvelteKit pages
    └── static/               # Static assets
        └── assets/           # Icons, images, and media
```

## ✨ Features

### 🎨 Visual & UX
- **Retro Terminal Interface**: Authentic green phosphor terminal styling
- **Cyberpunk Aesthetics**: Futuristic background animations and effects
- **ASCII Art Logo**: Animated Cyberdyne Systems branding
- **Glassmorphism UI**: Modern translucent interface elements
- **Interactive Windows**: Draggable, resizable window system
- **Responsive Design**: Optimized for desktop and mobile devices

### 🔗 Web3 Integration
- **Web3Auth Authentication**: Social login with Google integration
- **WalletConnect Support**: Mobile wallet connectivity via QR codes
- **Base Network**: Configured for Base mainnet with Infura RPC
- **Real-time Balance**: Live ETH balance display and updates
- **Professional Wallet UI**: Clean connected state with expandable details

### 🛠️ Technical
- **TypeScript**: Full type safety throughout the application
- **SvelteKit**: Modern web framework with static site generation
- **Tailwind CSS**: Utility-first CSS framework
- **Docker Ready**: Production-ready containerization
- **IPFS Compatible**: Static build optimized for decentralized hosting

## 🚀 Development

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Quick Start

```bash
# Navigate to frontend directory
cd frontend

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

Create a `.env` file in the `frontend/` directory:

```env
# Web3Auth Configuration (Required for social login)
VITE_WEB3AUTH_CLIENT_ID=your_web3auth_client_id
VITE_WEB3AUTH_NETWORK=sapphire_mainnet

# Infura Configuration (Required for Base Network RPC)
VITE_INFURA_ENDPOINT=https://base-mainnet.infura.io/v3/your_infura_api_key

# Base Network Configuration
VITE_CHAIN_ID=8453
VITE_NETWORK_NAME=Base Mainnet
VITE_NATIVE_CURRENCY=ETH

# App Configuration
VITE_APP_NAME=Cyberdyne DAO Terminal
VITE_APP_ENV=production
VITE_APP_URL=https://your-domain.com

# WalletConnect Configuration (Optional - for mobile wallets)
VITE_REOWN_PROJECT_ID=your_reown_project_id
VITE_REOWN_APP_NAME=Cyberdyne DAO Terminal
VITE_REOWN_APP_DESCRIPTION=Retro terminal interface for DAO operations
VITE_REOWN_APP_URL=https://your-domain.com
VITE_REOWN_APP_ICON=https://your-domain.com/assets/cyberdyne_logo.svg
```

### Getting API Keys

1. **Web3Auth Client ID** (Required):
   - Visit [Web3Auth Dashboard](https://dashboard.web3auth.io/)
   - Create a new project
   - Add your domain to the allowed origins
   - Copy the Client ID

2. **Infura API Key** (Required):
   - Visit [Infura](https://infura.io/)
   - Create a new project for Base network
   - Copy the API key and construct the endpoint URL

3. **Reown Project ID** (Optional):
   - Visit [WalletConnect Cloud](https://cloud.walletconnect.com/)
   - Create a new project
   - Copy the Project ID

### Wallet Connection Features

#### 🔑 Web3Auth (Primary Method)
- **Google Authentication**: One-click social login
- **Secure Key Management**: Non-custodial wallet creation
- **User-Friendly**: No seed phrases or complex setup
- **Custom Branding**: Cyberdyne logo in authentication modal

#### 📱 WalletConnect (Coming Soon)
- **Mobile Wallet Support**: MetaMask, Trust Wallet, etc.
- **QR Code Scanning**: Easy mobile connection
- **Multi-Wallet Compatibility**: 50+ supported wallets

### Connected State UI
- **Minimal Interface**: Shows only "CONNECTED" when collapsed
- **Expandable Details**: Click to view wallet information
- **Clean Design**: Semi-transparent black background with green accents
- **User Information**: Address, balance, email, name, and disconnect option

## 🐳 Docker Deployment

The project includes a production-ready Dockerfile for containerized deployment.

### Quick Deploy with Docker

```bash
# Navigate to frontend directory
cd frontend

# Build Docker image
docker build -t cyberdyne-terminal .

# Run container
docker run -p 80:80 cyberdyne-terminal
```

### Docker Configuration

The Dockerfile uses a multi-stage build:
1. **Builder Stage**: Node.js environment for building the SvelteKit app
2. **Production Stage**: Nginx Alpine for serving static files

**Features:**
- ✅ Optimized for production with Nginx
- ✅ Static file serving with proper caching headers
- ✅ SPA routing support with fallback handling
- ✅ Security headers included
- ✅ Small image size using Alpine Linux

### Coolify Deployment

This project is optimized for deployment on Coolify:

1. **Connect Repository**: Link your GitHub repository
2. **Set Build Context**: Point to `frontend/` directory
3. **Configure Environment Variables**: Add all `VITE_*` variables
4. **Deploy**: Coolify will automatically build and deploy using the Dockerfile

**Important**: Make sure to update `VITE_APP_URL` and related URLs to match your deployment domain.

## 🌐 Static Deployment

The application is also configured for static deployment (IPFS, Netlify, Vercel, etc.)

### Build for Static Hosting

```bash
# Navigate to frontend directory
cd frontend

# Build for static deployment
npm run build

# Preview static build
npm run preview
```

### Static Hosting Features

- ✅ **Pre-rendered Routes**: All pages generated at build time
- ✅ **Relative Paths**: Compatible with subdirectory deployments
- ✅ **SPA Fallback**: Client-side routing support
- ✅ **Asset Optimization**: Bundled and optimized static assets
- ✅ **No Server Required**: Pure static hosting compatible

## 📁 Detailed Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── components/          # Svelte components
│   │   │   ├── Web3Wallet.svelte    # Web3Auth wallet integration
│   │   │   ├── TopBar.svelte        # Navigation header  
│   │   │   ├── Terminal.svelte      # Terminal emulator
│   │   │   ├── TeamView.svelte      # Team member profiles
│   │   │   └── Window.svelte        # Draggable window system
│   │   ├── web3/                # Web3 integration
│   │   │   ├── web3AuthService.ts   # Web3Auth service
│   │   │   ├── config.ts            # Network configuration
│   │   │   └── contracts.ts         # Smart contract helpers
│   │   ├── stores/              # Svelte stores
│   │   │   ├── windowStore.ts       # Window management
│   │   │   └── web3Store.ts         # Web3 state management
│   │   ├── constants/           # App constants
│   │   │   ├── navigation.ts        # Navigation menu items
│   │   │   └── asciiLogo.ts         # ASCII art constants
│   │   ├── types/               # TypeScript interfaces
│   │   │   ├── web3.ts              # Web3 type definitions
│   │   │   └── cart.ts              # Shopping cart types
│   │   └── utils/               # Utility functions
│   │       └── terminalCommands.ts  # Terminal command handlers
│   ├── routes/                  # SvelteKit pages
│   │   ├── +layout.svelte           # App layout
│   │   └── +page.svelte             # Main page
│   └── app.css                  # Global styles & Tailwind
└── static/                      # Static assets
    └── assets/                  # Icons and images
        ├── cyberdyne_logo.svg       # Main logo
        ├── team/                    # Team member photos
        └── *.svg                    # Navigation icons
```

## 🎨 Design System

### Visual Elements
- **Retro Terminal**: Green phosphor text on dark backgrounds
- **Glassmorphism**: Translucent panels with backdrop blur
- **Cyberpunk Aesthetics**: Neon accents and futuristic styling
- **Professional UI**: Clean, minimal interface design

### Animations & Effects
- **ASCII Art**: Animated Cyberdyne logo with glow effects
- **Background Patterns**: Subtle grid and particle animations  
- **Smooth Transitions**: CSS animations for interactive elements
- **Hover States**: Interactive feedback on all clickable elements

## 🚀 Key Features

### 🔐 Web3 Wallet Integration
- **Web3Auth Service**: Secure social authentication with Google
- **Dynamic Imports**: Optimized loading to prevent SSR conflicts
- **Clean UI**: Minimal "CONNECTED" button with expandable details
- **Professional Design**: Semi-transparent panels with cyberpunk styling

### 🖥️ Terminal Interface
- **Authentic Styling**: Green phosphor text on dark terminal backgrounds
- **Interactive Commands**: Functional terminal with command processing
- **ASCII Art**: Animated Cyberdyne Systems logo
- **Responsive Design**: Works on desktop and mobile devices

### 🏗️ Architecture
- **TypeScript**: Full type safety throughout the application
- **Modular Design**: Clean separation of concerns and utilities
- **Performance Optimized**: Efficient loading and rendering
- **Production Ready**: Docker containerization and deployment configs

## 🔧 Technologies

- **🎨 Frontend**: SvelteKit, TypeScript, Tailwind CSS
- **🔗 Web3**: Web3Auth, ethers.js, Base Network, Infura
- **📦 Build**: Vite, SvelteKit Static Adapter
- **🐳 Deployment**: Docker, Nginx, Coolify-ready
- **🎭 Assets**: SVG icons, WebP images, custom animations

## 🏆 Recent Achievements

- ✅ **Web3Auth Integration**: Fully functional Google authentication
- ✅ **SSR Compatibility**: Resolved polyfill conflicts for server-side rendering
- ✅ **Docker Ready**: Production-optimized containerization
- ✅ **Clean UI**: Professional wallet interface with expandable details
- ✅ **Project Structure**: Organized into dedicated frontend directory
- ✅ **Performance**: Optimized builds and efficient asset loading

## 📋 Development Status

- 🟢 **Web3Auth Authentication**: Complete and working
- 🟡 **WalletConnect Integration**: Planned for future release
- 🟢 **Docker Deployment**: Ready for production
- 🟢 **Static Hosting**: IPFS and traditional hosting compatible
- 🟢 **Responsive Design**: Mobile and desktop optimized

## 🚀 Get Started

1. **Clone the repository**
2. **Navigate to frontend directory**: `cd frontend`
3. **Install dependencies**: `npm install`
4. **Configure environment**: Copy `.env` template and add your API keys
5. **Start development**: `npm run dev`
6. **Build for production**: `npm run build`

---

**Built with ❤️ by the Cyberdyne DAO Team**

*A futuristic terminal interface for the decentralized age*
