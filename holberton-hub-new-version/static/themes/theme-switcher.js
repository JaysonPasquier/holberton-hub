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
        document.body.classList.remove(...this.themes.map(t => `theme-${t}`));
        document.body.classList.add(`theme-${theme}`);

        // Fix specific elements based on theme
        if (theme === 'dark' || theme === 'lastofus' || theme === 'darksoul' || theme === 'resident') {
            // Fix light backgrounds in dark modes
            const jumbotron = document.querySelector('.jumbotron.bg-light');
            if (jumbotron) jumbotron.classList.replace('bg-light', 'bg-dark');
        } else {
            // Restore light backgrounds when not in dark mode
            const jumbotron = document.querySelector('.jumbotron.bg-dark');
            if (jumbotron) jumbotron.classList.replace('bg-dark', 'bg-light');
        }

        // Dispatch event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));

        console.log(`Theme changed to: ${theme}`);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});
