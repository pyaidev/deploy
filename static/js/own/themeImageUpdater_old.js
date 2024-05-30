// Function to get the current chapter
function getCurrentTheme() {
    return document.documentElement.getAttribute('data-bs-theme');
}

// Function to update the src of an image depending on the current theme
function updateImageSrc() {
    const theme = getCurrentTheme();
    const image = document.getElementById('themeImage');

    // Set different src depending on current theme
    if (theme === 'light') {
        image.src = '/media/decor/favicon_bl.ico';
    } else if (theme === 'dark') {
        image.src = '/media/decor/favicon.ico';
    }
}

var themeImage = document.getElementById('themeImage');
// Call a function when the page loads and the theme changes
if (themeImage) {
    window.addEventListener('load', updateImageSrc);
    document.addEventListener('themeChanged', updateImageSrc);
}