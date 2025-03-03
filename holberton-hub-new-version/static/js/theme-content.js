
/**
 * Theme Content Manager
 * Updates page content based on the selected theme
 */
class ThemeContentManager {
    constructor() {
        this.init();
    }

    init() {
        // Listen for theme changes
        document.addEventListener('themeChanged', (event) => {
            if (event.detail && event.detail.theme) {
                this.updateContent(event.detail.theme);
            }
        });

        // Update based on current theme on page load
        const currentTheme = localStorage.getItem('holberton-hub-theme') || 'light';
        this.updateContent(currentTheme);
    }

    updateContent(theme) {
        console.log(`Updating content for theme: ${theme}`);

        // Update the "Connect with Peers" text
        const peerTextElem = document.getElementById('connect-peers-text');
        if (peerTextElem) {
            if (theme === 'holberton') {
                peerTextElem.textContent = peerTextElem.dataset.holberton;
            } else {
                peerTextElem.textContent = peerTextElem.dataset.default;
            }
            console.log(`Updated peer text to: ${peerTextElem.textContent}`);
        } else {
            console.log('Peer text element not found');
        }

        // Save theme to session via AJAX if CSRF token is available
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            fetch('/themes/set/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken.value
                },
                body: `theme=${theme}`
            }).then(response => {
                console.log('Theme saved to session');
            }).catch(error => {
                console.error('Error saving theme to session:', error);
            });
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeContentManager = new ThemeContentManager();
});
