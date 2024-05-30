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
        image.src = '/media/asserts/favicon_bl.ico';
    } else if (theme === 'dark') {
        image.src = '/media/asserts/favicon.ico';
    }
}

// Function to update the color of SVG-logo depending on the current theme
function updateSVGColor() {

    const theme = getCurrentTheme();
    const fil0Elements = document.querySelectorAll('.fil0');

    // Set different src depending on current theme
    if (theme === 'light') {
        // Set fill for the entire class 'fil0'
        fil0Elements.forEach(element => {
            element.style.fill = 'rgba(33,37,41,0.75)';
        });
    } else if (theme === 'dark') {
        // Set fill for the entire class 'fil0'
        fil0Elements.forEach(element => {
            element.style.fill = 'rgba(222,226,230,0.75)';
        });
    }
}

// Function to update the src of 3d figures in material_view depending on the current theme
function updateFigure3dSrc() {

    const theme = getCurrentTheme();
    const figureElements = document.querySelectorAll('[id^="figure_"]');

    figureElements.forEach((figure) => {
        const currentSrc = figure.src;

        // Check the current theme and update the src accordingly
        if (theme === 'light' && currentSrc.includes('2b3035ff')) {
            figure.src = currentSrc.replace('2b3035ff', 'f8f9faff');
        } else if (theme === 'dark' && currentSrc.includes('f8f9faff')) {
            figure.src = currentSrc.replace('f8f9faff', '2b3035ff');
        }
    });
}

// Function to update the src of 3d figures inside cards depending on the current theme
function updateFigure3dSrc_card() {

    const theme = getCurrentTheme();
    const figureElements_card = document.querySelectorAll('[id^="card_figure_"]');

    figureElements_card.forEach((figure) => {
        const currentSrc = figure.src;

        // Check the current theme and update the src accordingly
        if (theme === 'light' && currentSrc.includes('212529ff')) {
            figure.src = currentSrc.replace('212529ff', 'f8f9faff');
        } else if (theme === 'dark' && currentSrc.includes('f8f9faff')) {
            figure.src = currentSrc.replace('f8f9faff', '212529ff');
        }
    });
}

function updatePolarizerImg() {

    const theme = getCurrentTheme();
    let image = document.getElementById('polarizerImg');

    // Set different src depending on current theme
    if (theme === 'light') {
        let temp = image.src
        image.src = temp.slice(0, -5) + 'b' + temp.slice(-4);
    } else if (theme === 'dark') {
        let temp = image.src
        image.src = temp.slice(0, -5) + 'w' + temp.slice(-4);
    }
}

function updateStageImg() {

    const theme = getCurrentTheme();
    let image = document.getElementById('stageImg');

    // Set different src depending on current theme
    if (theme === 'light') {
        image.src = '/media/asserts/Stage_b.png';
    } else if (theme === 'dark') {
        image.src = '/media/asserts/Stage_w.png';
    }
}

function updateDescContainerStyle() {
    const theme = getCurrentTheme();
    let descContainerElements = document.querySelectorAll('.desc-container_class');

    // Set different src depending on current theme
    if (theme === 'light') {
        // Set fill for the entire class 'fil0'
        descContainerElements.forEach(element => {
            element.style.background = '#f8f9faff';
            element.style.color = '#000000';
        });
    } else if (theme === 'dark') {
        // Set fill for the entire class 'fil0'
        descContainerElements.forEach(element => {
            element.style.background = '#2b3035ff';
            element.style.color = '#ffffff';
        });
    }
}

let themeImage = document.getElementById('themeImage');
const figureElements = document.querySelectorAll('[id^="figure_"]');
const figureElements_card = document.querySelectorAll('[id^="figure_card_"]');
const fil0Elements = document.querySelectorAll('.fil0');
let polarizerImg = document.getElementById('polarizerImg');
let stageImg = document.getElementById('stageImg');
let descContainers = document.querySelectorAll('.desc-container_class');

// Call a function when the page loads and the theme changes
if (themeImage) {
    window.addEventListener('load', updateImageSrc);
    document.addEventListener('themeChanged', updateImageSrc);
}
if (figureElements) {
    window.addEventListener('load', updateFigure3dSrc);
    document.addEventListener('themeChanged', updateFigure3dSrc);
}

if (figureElements_card) {
    window.addEventListener('load', updateFigure3dSrc_card);
    document.addEventListener('themeChanged', updateFigure3dSrc_card);
}

if (fil0Elements) {
    window.addEventListener('load', updateSVGColor);
    document.addEventListener('themeChanged', updateSVGColor);
}
if (polarizerImg) {
    window.addEventListener('load', updatePolarizerImg);
    document.addEventListener('themeChanged', updatePolarizerImg);
}
if (stageImg) {
    window.addEventListener('load', updateStageImg);
    document.addEventListener('themeChanged', updateStageImg);
}
if (descContainers) {
    window.addEventListener('load', updateDescContainerStyle);
    document.addEventListener('themeChanged', updateDescContainerStyle);
}
