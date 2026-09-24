---
name: Sentiment Noir
colors:
  surface: '#0d1515'
  surface-dim: '#0d1515'
  surface-bright: '#333b3b'
  surface-container-lowest: '#080f10'
  surface-container-low: '#151d1e'
  surface-container: '#192122'
  surface-container-high: '#232b2c'
  surface-container-highest: '#2e3637'
  on-surface: '#dce4e4'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dce4e4'
  inverse-on-surface: '#2a3232'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dbe7'
  primary: '#e1fdff'
  on-primary: '#00363a'
  primary-container: '#00f2ff'
  on-primary-container: '#006a71'
  inverse-primary: '#00696f'
  secondary: '#ecffe3'
  on-secondary: '#003907'
  secondary-container: '#13ff43'
  on-secondary-container: '#007117'
  tertiary: '#fff6e4'
  on-tertiary: '#3b2f00'
  tertiary-container: '#fed83a'
  on-tertiary-container: '#725e00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#74f5ff'
  primary-fixed-dim: '#00dbe7'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#72ff70'
  secondary-fixed-dim: '#00e639'
  on-secondary-fixed: '#002203'
  on-secondary-fixed-variant: '#00530e'
  tertiary-fixed: '#ffe173'
  tertiary-fixed-dim: '#e8c423'
  on-tertiary-fixed: '#221b00'
  on-tertiary-fixed-variant: '#554500'
  background: '#0d1515'
  on-background: '#dce4e4'
  surface-variant: '#2e3637'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 72px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0em
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.1em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: 0.2em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  container-max: 1440px
---

## Brand & Style

The design system embodies a "Sentiment Noir" aesthetic—a fusion of high-end luxury and futuristic technical precision. It is designed for elite analytical environments where data is treated as a premium asset. The personality is authoritative, cinematic, and profoundly focused.

The visual direction leverages **Glassmorphism** and **Minimalism** to create a sense of depth and intelligence. By utilizing a dark-on-dark foundation with ultra-sharp, thin-stroke accents, the interface feels like a sophisticated digital cockpit. High-fidelity data visualizations and subtle glowing elements suggest a "living" intelligence behind the glass.

## Colors

The palette is anchored in absolute darkness to maximize contrast and focus. 
- **Core:** The primary background is a deep, true black (#050505) to ensure OLED-level depth.
- **Accents:** "Data Cyan" (#00F2FF) serves as the primary action and focus color, while "Logic Green" (#00FF41) is reserved for status indicators and success states.
- **Grays:** A scale of charcoal grays is used for subtle borders and container surfaces, ensuring the UI remains layered without losing its noir essence.
- **Luminance:** Pure white is used sparingly for primary headings to create a stark, commanding hierarchy.

## Typography

Typography uses a high-contrast pairing strategy. 
- **Headlines:** Montserrat provides a bold, wide, and aggressive presence for major statements and headers. It should be set with tight letter spacing for a modern, cinematic look.
- **Body:** Inter handles all long-form reading, providing exceptional clarity and a neutral professional tone.
- **Technical Data:** JetBrains Mono is utilized for all system labels, data points, and metadata, evoking a precise, "under-the-hood" feel.
- **Small Labels:** Use the `label-caps` style for section headers to create a rhythmic, structural feel across the layout.

## Layout & Spacing

The system employs a **Fluid Grid** with generous inner margins to maintain a sense of "premium" space. 
- **Desktop:** A 12-column grid with 24px gutters. Content is often centered or anchored to a 48px side margin to create asymmetrical, sophisticated compositions.
- **Mobile:** Reflows to a 4-column grid with 16px margins. 
- **Rhythm:** All spacing (padding, margins) must be multiples of the 4px base unit. 
- **Alignment:** Use rigid vertical alignment for technical data strings to maintain the "logical" aesthetic of the system.

## Elevation & Depth

Depth is not achieved through traditional drop shadows, but through **light and transparency**:
- **Glassmorphism:** Use background blurs (20px–40px) on surfaces with a low-opacity white or cyan tint (approx 4-8%).
- **Glowing Borders:** Surfaces should feature a 1px solid border. For active states, apply a subtle `0 0 8px` outer glow using the primary accent color.
- **Tonal Layering:** Higher elevation is represented by lighter charcoal grays (#1A1A1A) rather than physical shadows.
- **Masking:** Use radial gradients on background layers to create "hotspots" of light behind active data modules.

## Shapes

The shape language is "Technical-Soft." Most UI elements utilize a precise 4px (Soft) corner radius. This provides just enough refinement to feel premium without losing the sharp, geometric edge required by the futuristic Noir theme.
- **Interactive Elements:** Buttons and inputs use the base 4px radius.
- **Data Containers:** Cards and large panels may use an 8px (rounded-lg) radius to differentiate from smaller utility components.
- **Status Pips:** Always use 100% rounding (pill-shaped) for status indicators and small badges.

## Components

- **Buttons:** Primary buttons should be solid white with black text for maximum impact, or a 1px Data Cyan outline with a subtle glow on hover.
- **Input Fields:** Minimalist 1px bottom-border only, or a fully enclosed 1px charcoal border. Text should be mono-spaced during input.
- **Chips/Badges:** Small, 1px bordered containers using JetBrains Mono. Use Data Cyan for active filters and Logic Green for status.
- **Cards:** Transparent background with a `backdrop-filter: blur()`. Borders should be #FFFFFF at 10% opacity.
- **Data Visuals:** Charts should use thin 1px lines. Avoid solid fills; use gradients that bleed into the background darkness.
- **Scrollbars:** Ultra-thin (2px) and charcoal-colored to disappear into the background when not in use.