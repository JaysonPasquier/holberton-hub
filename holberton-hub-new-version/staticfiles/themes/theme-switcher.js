
/**
 * Theme Switcher for Holberton Hub
 * Handles switching between different visual themes and persisting user preferences
 */

class ThemeManager {
    constructor() {
        this.themes = ['light', 'dark', 'holberton'];
        this.defaultTheme = 'light';
        this.storageKey = 'holberton-hub-theme';
        this.themeStylesheetId = 'theme-stylesheet';
        this.initialized = false;

        // DOM references
        this.themeSwitchers = document.querySelectorAll('.theme-switcher');

        // Initialize
        this.init();
    }

    init() {
        if (this.initialized) return;

        // Apply saved theme or default
        const savedTheme = this.getSavedTheme();
        this.applyTheme(savedTheme || this.defaultTheme);

        // Attach event listeners to theme switchers
        this.themeSwitchers.forEach(switcher => {
            switcher.addEventListener('click', (event) => {
                const theme = event.currentTarget.getAttribute('data-theme');
                if (theme) {
                    this.applyTheme(theme);
                }
            });
        });

        // Mark icons as active based on current theme
        this.updateActiveThemeIcon(savedTheme || this.defaultTheme);

        this.initialized = true;
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

        // Update body class
        document.body.className = document.body.className
            .replace(/theme-\w+/g, '')
            .trim();
        document.body.classList.add(`theme-${theme}`);

        // Update active icons
        this.updateActiveThemeIcon(theme);

        // Dispatch event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    updateActiveThemeIcon(activeTheme) {
        this.themeSwitchers.forEach(switcher => {
            const theme = switcher.getAttribute('data-theme');
            const iconActive = switcher.querySelector('.theme-icon-active');
            const iconInactive = switcher.querySelector('.theme-icon-inactive');

            if (theme === activeTheme) {
                switcher.classList.add('active');
                if (iconActive) iconActive.classList.remove('d-none');
                if (iconInactive) iconInactive.classList.add('d-none');
            } else {
                switcher.classList.remove('active');
                if (iconActive) iconActive.classList.add('d-none');
                if (iconInactive) iconInactive.classList.remove('d-none');
            }
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});
