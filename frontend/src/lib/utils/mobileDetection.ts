// Mobile detection utility
export function isMobileDevice(): boolean {
  // Check for touch capability
  const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  
  // Check screen width
  const isSmallScreen = window.innerWidth <= 768;
  
  // Check user agent for mobile devices
  const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  
  return hasTouch || isSmallScreen || isMobileUA;
}

export function isTabletDevice(): boolean {
  const width = window.innerWidth;
  return width > 768 && width <= 1024;
}

export function isSmallMobileDevice(): boolean {
  return window.innerWidth <= 480;
}

export function getDeviceType(): 'mobile' | 'tablet' | 'desktop' {
  if (isSmallMobileDevice()) return 'mobile';
  if (isMobileDevice()) return 'mobile';
  if (isTabletDevice()) return 'tablet';
  return 'desktop';
}

// Responsive breakpoints
export const BREAKPOINTS = {
  mobile: 768,
  tablet: 1024,
  desktop: 1025
} as const;

// Check if current screen size matches a breakpoint
export function isBreakpoint(breakpoint: keyof typeof BREAKPOINTS): boolean {
  const width = window.innerWidth;
  switch (breakpoint) {
    case 'mobile':
      return width <= BREAKPOINTS.mobile;
    case 'tablet':
      return width > BREAKPOINTS.mobile && width <= BREAKPOINTS.tablet;
    case 'desktop':
      return width > BREAKPOINTS.tablet;
    default:
      return false;
  }
}

// Get current breakpoint
export function getCurrentBreakpoint(): keyof typeof BREAKPOINTS {
  if (isBreakpoint('mobile')) return 'mobile';
  if (isBreakpoint('tablet')) return 'tablet';
  return 'desktop';
}
