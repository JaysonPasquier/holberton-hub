# Holberton Hub Themes

This directory contains the CSS files for the various themes available in Holberton Hub.

## Available Themes

1. **Light Theme (`light-theme.css`)**: Default theme with a clean, light appearance.
2. **Dark Theme (`dark-theme.css`)**: Dark mode to reduce eye strain.
3. **Holberton Theme (`holberton-theme.css`)**: Theme with Holberton School branding.

### Additional Color Themes

4. **Purple Theme (`purple-theme.css`)**: A modern theme with deep purple as the main color.
5. **Pink Theme (`pink-theme.css`)**: A vibrant theme featuring pink colors.
6. **Orange Theme (`orange-theme.css`)**: A warm theme with orange accent colors.
7. **Green Theme (`green-theme.css`)**: A nature-inspired green theme.
8. **Blue Theme (`blue-theme.css`)**: A calming theme with blue as the primary color.
9. **Teal Theme (`teal-theme.css`)**: A refreshing theme with teal/turquoise tones.
10. **Gold Theme (`gold-theme.css`)**: A luxurious theme using gold/amber colors.
11. **Red Theme (`red-theme.css`)**: A bold theme with red as the primary color.
12. **Mint Theme (`mint-theme.css`)**: A fresh theme with mint/seafoam green tones.
13. **Gray Theme (`gray-theme.css`)**: A sleek monochrome theme with elegant gray tones.

## How to Create a New Theme

To create a custom theme:

1. Duplicate one of the existing theme CSS files and rename it (e.g., `my-custom-theme.css`).
2. Modify the CSS variables in the `:root` section to create your color palette.
3. Add your theme name to the `themes` array in the `theme-switcher.js` file.
4. (Optional) Add a preview card for your theme in the theme selection page.

## CSS Variables

Key CSS variables you can customize:

```css
:root {
    /* Main colors */
    --theme-primary: #your-primary-color;
    --theme-primary-hover: #your-hover-color;
    --theme-secondary: #your-secondary-color;

    /* Background colors */
    --theme-bg-primary: #background-color;
    --theme-bg-secondary: #secondary-bg-color;

    /* Text colors */
    --theme-text-primary: #main-text-color;
    --theme-text-secondary: #secondary-text-color;

    /* Component colors */
    --theme-card-bg: #card-background;
    --theme-nav-bg: #navbar-color;
    --theme-footer-bg: #footer-color;

    /* And more... */
}
```

## Theme Switcher

The theme selection system uses `theme-switcher.js` to handle theme switching and user preferences. Theme preferences are stored in the user's browser using localStorage.
