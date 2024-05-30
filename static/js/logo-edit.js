// Функция для получения текущей темы
function getCurrentTheme() {
    return document.documentElement.getAttribute('data-bs-theme');
}

// Функция для обновления src изображения в зависимости от текущей темы
function updateImageSrc() {
    const theme = getCurrentTheme();
    const image = document.getElementById('themeImage');

    // Установите разные src в зависимости от текущей темы
    if (theme === 'light') {
        image.src = '/media/decor/favicon_bl.ico';
    } else if (theme === 'dark') {
        image.src = '/media/decor/favicon.ico';
    }
}

// Вызовите функцию при загрузке страницы и изменении темы
window.addEventListener('load', updateImageSrc);
document.addEventListener('themeChanged', updateImageSrc);
