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
- **Build**: Vite, SvelteKit adapter
- **Assets**: SVG icons, WebP images

---

Built with ❤️ for the Cyberdyne DAO community
