const themeButtons = document.querySelectorAll('[data-bs-theme-value]');

themeButtons.forEach(button => {
    button.addEventListener('click', function () {
        const themeValue = this.getAttribute('data-bs-theme-value');
        document.documentElement.setAttribute('data-bs-theme', themeValue);

        // Raise the themeChanged event after changing themes
        const event = new Event('themeChanged');
        document.dispatchEvent(event);
    });
});