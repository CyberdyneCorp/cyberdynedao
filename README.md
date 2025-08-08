# Retro Terminal Website Clone

A pixel-perfect recreation of a retro terminal-style website using Svelte, Tailwind CSS, and TypeScript.

## Features

- Retro terminal aesthetic with animated pixel background
- Navigation sidebar with SVG icons
- Terminal window interface
- Shopping cart functionality
- Responsive design
- Smooth retro button interactions

## Development

```bash
npm install
npm run dev
```

## Assets

SVG icons are located in `/static/assets/` and include:
- substack.svg
- read.svg
- investments.svg
- watch.svg
- contact.svg
- listen.svg
- enigma.svg
- shop.svg
- cart.svg

## Structure

- `src/routes/+page.svelte` - Main application layout
- `src/lib/components/Sidebar.svelte` - Navigation sidebar
- `src/lib/components/TerminalWindow.svelte` - Main terminal interface
- `src/app.css` - Custom retro styling and Tailwind configuration

## Building

```sh
npm run build
```

You can preview the production build with `npm run preview`.
