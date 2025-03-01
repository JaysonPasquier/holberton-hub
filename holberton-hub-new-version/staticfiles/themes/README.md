# Holberton Hub Themes

This directory contains the theme files for Holberton Hub. The theme system allows users to switch between different visual styles:

## Available Themes

1. **Light Theme (`light-theme.css`)**: The default theme with a clean, light appearance.
2. **Dark Theme (`dark-theme.css`)**: A dark theme to reduce eye strain in low-light environments.
3. **Holberton Theme (`holberton-theme.css`)**: A theme styled with Holberton School brand colors and design elements.

## How to Add a New Theme

1. Create a new CSS file in this directory, e.g., `my-theme.css`
2. Copy the structure from one of the existing theme files
3. Modify the CSS variables in the `:root` section to change colors and styles
4. Add your theme to the theme switcher by updating the following files:
   - `/static/themes/theme-switcher.js` - Add your theme to the `themes` array
   - `/templates/base.html` - Add a new button in the theme-options section

## Theme Variable Reference

Each theme should define these CSS variables to ensure consistent styling:

- `--theme-primary`: Primary brand color
- `--theme-secondary`: Secondary/accent color
- `--theme-bg-primary`: Main background color
- `--theme-bg-secondary`: Secondary background color
- `--theme-text-primary`: Main text color
- `--theme-text-secondary`: Secondary text color
- `--theme-border-color`: Color for borders
- And more (see existing themes for reference)

## Theme Switcher

The `theme-switcher.js` file handles saving and restoring theme preferences using localStorage. Users' theme choices will persist across visits.
