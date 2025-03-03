/**
 * Theme Switcher for Holberton Hub
 * Handles switching between different visual themes and persisting user preferences
 */

class ThemeManager {
    constructor() {
        // Update the themes array - removed game themes
        this.themes = [
            'light', 'dark', 'holberton',
            'purple', 'pink', 'orange', 'green', 'blue',
            'teal', 'gold', 'red', 'mint', 'gray'
        ];
        this.defaultTheme = 'light';
        this.storageKey = 'holberton-hub-theme';
        this.themeStylesheetId = 'theme-stylesheet';
        this.initialized = false;

        // Initialize
        this.init();
    }

    init() {
        if (this.initialized) return;

        // Apply saved theme or default
        const savedTheme = this.getSavedTheme();
        this.applyTheme(savedTheme || this.defaultTheme);

        // Listen for theme changes from the theme selection page
        document.addEventListener('themeSelect', (e) => {
            if (e.detail && e.detail.theme) {
                this.applyTheme(e.detail.theme);
            }
        });

        this.initialized = true;

        // Log for debugging
        console.log(`Theme system initialized with ${savedTheme || this.defaultTheme} theme`);
    }

    getSavedTheme() {
        return localStorage.getItem(this.storageKey);
    }

    // Update the applyTheme method to add the appropriate theme class
    applyTheme(theme) {
        if (!this.themes.includes(theme)) {
            theme = this.defaultTheme;
        }

        // Update theme stylesheet link
        let link = document.getElementById(this.themeStylesheetId);
        if (!link) {
            link = document.createElement('link');
            link.id = this.themeStylesheetId;
            link.rel = 'stylesheet';
            document.head.appendChild(link);
        }

        link.href = `/static/themes/${theme}-theme.css`;

        // Save user preference
        localStorage.setItem(this.storageKey, theme);

        // Update body class - remove all theme classes first
        const currentClasses = [...document.body.classList];
        currentClasses.forEach(cls => {
            if (cls.startsWith('theme-')) {
                document.body.classList.remove(cls);
            }
        });

        // Add the new theme class
        document.body.classList.add(`theme-${theme}`);

        // For dark themes, also add a generic dark class
        const isDarkTheme = theme === 'dark' || theme.includes('dark');
        if (isDarkTheme) {
            document.body.classList.add('theme-generic-dark');
        }

        // Dispatch event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));

        console.log(`Theme changed to: ${theme}`);

        // If any theme-specific content update is needed
        if (this.updateThemeSpecificContent) {
            this.updateThemeSpecificContent(theme);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Add this function to your existing theme-switcher.js file
window.themeManager = window.themeManager || {};

// Extend themeManager with a method to update content based on theme
window.themeManager.updateThemeSpecificContent = function(theme) {
    // Update the "Connect with Peers" text
    const peerText = document.querySelector('.fa-users').closest('.card-body').querySelector('p');
    if (peerText) {
        if (theme === 'holberton') {
            peerText.textContent = 'Find and network with other Holberton students and other !';
        } else {
            peerText.textContent = 'Connect with like-minded developers and build your professional network.';
        }
    }

    // You can add more theme-specific content updates here
}

// Extend the applyTheme method to update content too
const originalApplyTheme = window.themeManager.applyTheme;
window.themeManager.applyTheme = function(theme) {
    // Call the original method to change stylesheets
    if (originalApplyTheme) {
        originalApplyTheme(theme);
    }

    // Update content
    this.updateThemeSpecificContent(theme);

    // Save theme to session via AJAX
    fetch('/themes/set/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `theme=${theme}`
    });
}
