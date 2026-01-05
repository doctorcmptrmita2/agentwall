# ADR-006: Custom Login Page Design

**Date:** 2026-01-06  
**Status:** Implemented  
**Context:** Login page branding issues

## Problem

Default Filament login page had multiple issues:
1. Logo rendering broken (SVG not loading properly)
2. "Show password" button oversized
3. Generic appearance - not aligned with AgentWall brand
4. No tagline/value proposition visible

## Decision

Implemented custom Login page with:

### 1. Custom Login Controller
- Extended `Filament\Pages\Auth\Login`
- Added brand tagline: "Guard the Agent, Save the Budget"
- Clean, minimal form structure

### 2. Custom Blade View
- Inline SVG shield icon (no external file dependency)
- Gradient blue shield matching brand colors
- Split "Agent" (gray) + "Wall" (blue) typography
- Tagline prominently displayed
- Responsive, professional layout

### 3. Brand Color System
- Full blue palette (50-950) for consistency
- Primary: `#3b82f6` (blue-500)
- Accent: `#2563eb` (blue-600)
- Matches public site and FastAPI docs

## Consequences

### Positive
- **Enterprise-grade appearance** - builds trust
- **Brand consistency** - matches agentwall.io
- **No external dependencies** - inline SVG, no file loading issues
- **Fast load time** - minimal CSS, no extra assets
- **Maintainable** - single Blade file, easy to update

### Negative
- **Custom code to maintain** - can't auto-update Filament login
- **Testing required** - need to verify after Filament upgrades

## Alternatives Considered

1. **Fix SVG loading** - too fragile, browser-dependent
2. **Use PNG logo** - lower quality, not scalable
3. **Override CSS only** - insufficient control, hacky

## Implementation Files

- `app/Filament/Pages/Auth/Login.php` - Controller
- `resources/views/filament/pages/auth/login.blade.php` - View
- `app/Providers/Filament/AdminPanelProvider.php` - Registration

## Success Metrics

- ✅ Logo renders correctly on all browsers
- ✅ Professional, enterprise appearance
- ✅ Brand consistency with public site
- ✅ Fast page load (<500ms)
- ✅ Mobile responsive

## Notes

This aligns with **CTO Mandate** principle:
> "Güven Problemi: Enterprise frene basar"

A professional login page is the first impression. Generic = commodity. Custom = premium product.
