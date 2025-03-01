# Creating Custom Game Themes with Game Assets

This guide explains how to create themes based on video games with custom fonts, images, and styling.

## Folder Structure

First, create the following directories:

```
/static/
  ├── themes/
  │   └── game-themes/  # Place your game theme CSS files here
  ├── fonts/
  │   └── games/        # Game-specific fonts
  └── images/
      └── games/        # Game-specific images and assets
          ├── last-of-us/
          ├── dark-souls/
          └── resident-evil/
```

## Step 1: Gather Game Assets

### Fonts
1. Find a font similar to the game title font (or exact if legally available)
2. Convert to web fonts (woff2, woff) using a tool like FontSquirrel converter
3. Place in `/static/fonts/games/[game-name]/`

### Images
For each game, collect:
1. Character images for left/right sides (transparent PNG is best)
2. Game logo/icon
3. Background textures or patterns
4. Any UI elements you want to incorporate

## Step 2: Create Game Theme CSS

1. Copy the `game-theme-template.css` file and rename it (e.g., `lastofus-theme.css`)
2. Update all paths to point to your game's assets
3. Set color variables based on the game's color palette
4. Customize fonts, images, and effects

## Step 3: The Last of Us Theme Example

For a Last of Us theme:

### Images to Use:
- Joel image for left side (semi-transparent)
- Ellie image for right side (semi-transparent)
- The Last of Us logo
- Optional: Spore/fungal textures for backgrounds

### Styling:
- Use the Last of Us title font for headings
- Dark, muted green/brown color palette
- Elements with minimal border-radius (more rectangular)
- Distressed textures on containers

### CSS Sample:
```css
/* The Last of Us theme specific styles */
:root {
  --theme-primary: #799156;       /* Muted olive green */
  --theme-secondary: #3b3a30;     /* Dark earth tone */
  --game-title-font: 'LastOfUsFont', serif;
}

/* Apply Joel image to left side */
body::before {
  background-image: url('/static/images/games/last-of-us/joel.png');
  opacity: 0.15;
}

/* Apply Ellie image to right side */
body::after {
  background-image: url('/static/images/games/last-of-us/ellie.png');
  opacity: 0.15;
}
```

## Step 4: Testing Your Theme

1. Add your theme to the theme switcher in `theme-switcher.js`
2. Test on different screen sizes (the character images may need adjustments)
3. Ensure text remains readable across all elements

## Font Usage Notes

If using commercial fonts, ensure you have proper licensing. Alternatives:
1. Use similar free fonts
2. Use CSS effects to approximate the style
3. Use SVG for game logo text instead of fonts

## Accessibility Considerations

1. Maintain sufficient contrast between text and backgrounds
2. Don't let decorative elements interfere with content readability
3. Test with screen readers to ensure compatibility
4. Provide sufficient sizing for text elements
