let videoPlayer = document.getElementById('videoPlayer');
let videoPlayerBlock = document.getElementById('videoPlayerBlock_1');
let frameNumberProgress = document.getElementById('frameNumber_1');
let frameNumberProgress_set = document.getElementById('frameNumber_1_set');
let stageNumberProgress = document.getElementById('angleNumber_1');
let stageNumberProgress_set = document.getElementById('angleNumber_1_set');
let rotateButton = document.getElementById('rotateButton_1');
let autoRotateButton = document.getElementById('autoRotateButton_1');
let modeButton = document.getElementById('modeButton_1');
let mineralsButton = document.getElementById('mineralsButton_1');
let modeImage = document.getElementById('polarizerImg');
let rotateImage = document.getElementById('stageImg');
let isRotating = false;
let isDragging = false;
let isSettingFrame = false;
let isSettingAngle = false;
let isSettingFrameImg = false;
let isSettingAngleImg = false;
let isSettingSpeed = false;
let isMineralsOn = false;
let isAutoRotating = false; // Variable to track auto-rotation state
let isParallelMode = true; // Default mode is "PPL"
let totalFrames = 360;
let duration = 12;
let rotatingSpeed = 1; // Set the rotation speed and play the video
let autoRotationFrameRate = 50; // frames per second
let autoRotateIntervalId;
let isEvenFrame = false;
let isOnPosition = false;

let nullPoint = 0;
let nullPointAngle = 0;
let nullFrame = 0;
let nullAngle = 0;
let nullDelta = 0;
let currentFrame = 0;
let currentAngle = 0;
let deltaAngle = 0;
let coordX = 0;
let coordY = 0;

// Blob objects to store video data
let videoBlobA, videoBlobB;

// Fetch video files and create Blobs
fetch(fileCPL)
    .then(response => response.blob())
    .then(blob => {
        videoBlobA = blob;

    });

fetch(filePPL)
    .then(response => response.blob())
    .then(blob => {
        videoBlobB = blob;
        // Set initial video source
        videoPlayer.src = URL.createObjectURL(blob);
    });

function toggleMode() {
    isParallelMode = !isParallelMode;

    if (isParallelMode) {
        modeButton.textContent = 'Switch to XPL mode';
        videoPlayer.src = URL.createObjectURL(videoBlobB);
        let temp = modeImage.src
        modeImage.src = '/media/asserts/Polarizer' + temp.slice(-6);
    } else {
        modeButton.textContent = 'Switch to PPL mode';
        videoPlayer.src = URL.createObjectURL(videoBlobA);
        let temp = modeImage.src
        modeImage.src = '/media/asserts/Polarizer-Analyzer' + temp.slice(-6);
    }

    updateFrame();
}

function toggleMinerals() {
    isMineralsOn = !isMineralsOn;
    let labels = document.querySelectorAll('.label-container');

    labels.forEach(label => {
        label.style.display = isMineralsOn ? 'block' : 'none';
    });

    if (!isOnPosition) {
        positionLabels();
    }
}

function positionLabels() {
    let labels = document.querySelectorAll('.label-container');

    labels.forEach(label => {
        let coordX = label.style.left;
        let coordY = label.style.top;

        // Getting the parent container
        let parentContainer = document.getElementById('videoPlayer');

        // Converting percentages to pixels for X and Y
        let pixelX = ((parentContainer.offsetWidth * parseFloat(coordX) / 100) - label.offsetWidth / 2) / parentContainer.offsetWidth * 100;
        let pixelY = ((parentContainer.offsetHeight * parseFloat(coordY) / 100) - label.offsetHeight / 2) / parentContainer.offsetHeight * 100;

        // Set coordinates in %
        label.style.left = pixelX + '%';
        label.style.top = pixelY + '%';
    });

    isOnPosition = true;
}


function toggleRotation() {
    isRotating = !isRotating;
    if (isRotating) {
        rotateButton.textContent = 'Switch to nicols rotation';
    } else {
        rotateButton.textContent = 'Switch to stage rotation';
    }
}

function toggleAutoRotate() {
    isAutoRotating = !isAutoRotating;

    if (isAutoRotating) {
        autoRotateIntervalId = setInterval(autoRotateFrames, 1000 / 30); // Call autoRotateFrames every frame (N frames per second)
        autoRotateButton.textContent = 'Turn auto-rotate mode off'; // Change button text when auto-rotate is on
    } else {
        clearInterval(autoRotateIntervalId);
        autoRotateButton.textContent = 'Turn auto-rotate mode on'; // Change button text when auto-rotate is off
    }
}

function rotateThinSection() {
    // Implementation of video rotation
    videoPlayerBlock.style.transform = `rotate(${currentAngle}deg)`;
    // Compensation rotation for labels
    let labels = document.querySelectorAll('.label-container');
    labels.forEach(label => {
        label.style.transform = `rotate(-${currentAngle}deg)`;
    });
    // Implementation of stage image rotation
    rotateImage.style.transform = `rotate(${currentAngle}deg)`;
}

function autoRotateFrames() {
    // We count a new frame depending on time
    currentFrame = (currentFrame + rotatingSpeed) % 360; // rotatingSpeed * 30 / 12 - скорость приращения
    if (isRotating) {
        currentAngle = Math.round((currentAngle + rotatingSpeed) % 360); // rotatingSpeed * 30 / 12 - скорость приращения
    }
    deltaAngle = (currentAngle - currentFrame + 1800) % 360;
    updateFrame();
}

function updateFrame() {

    frameNumberProgress.style.width = `${Math.round(deltaAngle / 359 * 100)}%`;
    frameNumberProgress.textContent = String(deltaAngle);
    stageNumberProgress.style.width = `${Math.round(currentAngle / 359 * 100)}%`;
    stageNumberProgress.textContent = String(currentAngle);
    // Implementation of nicols rotation
    videoPlayer.currentTime = (currentFrame / totalFrames) * duration;
    // Implementation of mode image rotation
    modeImage.style.transform = `rotate(${deltaAngle}deg)`;
    // Implementation of stage rotation
    if (isRotating) {
        rotateThinSection()
    }
}

videoPlayer.addEventListener('mousedown', function (event) {
    if (event.button === 0) { // Checking that it is the left mouse button
        isDragging = true;
        nullPoint = {x: event.clientX, y: event.clientY};

        let rect = videoPlayer.getBoundingClientRect();
        coordX = rect.left + rect.width / 2;
        coordY = rect.top + rect.height / 2;

        let deltaX = nullPoint.x - coordX;
        let deltaY = nullPoint.y - coordY;
        nullPointAngle = Math.round((Math.atan2(deltaY, deltaX) * 180 / Math.PI));
    }
});

frameNumberProgress_set.addEventListener('mousedown', function (event) {
    if (event.button === 0) { // Checking that it is the left mouse button
        isSettingFrame = true;
        nullPoint = {x: event.clientX, y: event.clientY};
    }
});

modeImage.addEventListener('mousedown', function (event) {
    if (event.button === 0) { // Checking that it is the left mouse button
        isSettingFrameImg = true;
        nullPoint = {x: event.clientX, y: event.clientY};

        let rect = modeImage.getBoundingClientRect();
        coordX = rect.left + rect.width / 2;
        coordY = rect.top + rect.height / 2;

        let deltaX = nullPoint.x - coordX;
        let deltaY = nullPoint.y - coordY;
        nullPointAngle = Math.round((Math.atan2(deltaY, deltaX) * 180 / Math.PI));
    }
});

stageNumberProgress_set.addEventListener('mousedown', function (event) {
    if (event.button === 0) { // Checking that it is the left mouse button
        isSettingAngle = true;
        nullPoint = {x: event.clientX, y: event.clientY};
    }
});

rotateImage.addEventListener('mousedown', function (event) {
    if (event.button === 0) { // Checking that it is the left mouse button
        isSettingAngleImg = true;
        nullPoint = {x: event.clientX, y: event.clientY};

        let rect = rotateImage.getBoundingClientRect();
        coordX = rect.left + rect.width / 2;
        coordY = rect.top + rect.height / 2;

        let deltaX = nullPoint.x - coordX;
        let deltaY = nullPoint.y - coordY;
        nullPointAngle = Math.round((Math.atan2(deltaY, deltaX) * 180 / Math.PI));
    }
});

document.addEventListener('mouseup', function (event) {
    if (event.button === 0) {
        isDragging = false;
        isSettingFrame = false;
        isSettingAngle = false;
        isSettingFrameImg = false;
        isSettingAngleImg = false;
        nullFrame = currentFrame;
        nullAngle = currentAngle;
        nullDelta = deltaAngle;
    }
});

document.addEventListener('mousemove', function (event) {
    if (isDragging) {
        let deltaX = event.clientX - coordX;
        let deltaY = event.clientY - coordY;
        let currentRotationAngle = Math.round((Math.atan2(deltaY, deltaX) * 180 / Math.PI));
        let frameValue = Math.round(currentRotationAngle - nullPointAngle);
        currentFrame = (nullFrame + frameValue + 360) % 360;
        if (isRotating) {
            currentAngle = (nullAngle + frameValue + 360) % 360;
        }
        deltaAngle = (currentAngle - currentFrame + 360) % 360;
        updateFrame();
    } else if (isSettingFrame) {
        deltaAngle = Math.round(((event.clientX - frameNumberProgress_set.getBoundingClientRect().left) / frameNumberProgress_set.offsetWidth) * 359);
        deltaAngle = Math.min(359, Math.max(0, deltaAngle))
        currentFrame = (currentAngle - deltaAngle + 1800) % 360;
        updateFrame();
    } else if (isSettingAngle) {
        currentAngle = Math.round(((event.clientX - stageNumberProgress_set.getBoundingClientRect().left) / stageNumberProgress_set.offsetWidth) * 359);
        currentAngle = Math.min(359, Math.max(0, currentAngle))
        currentFrame = (currentAngle - deltaAngle + 1800) % 360;
        updateFrame();
        rotateThinSection()
    } else if (isSettingFrameImg) {
        let deltaX = event.clientX - coordX;
        let deltaY = event.clientY - coordY;
        let currentRotationAngle = Math.round((Math.atan2(deltaY, deltaX) * 180 / Math.PI));
        let frameValue = Math.round((currentRotationAngle - nullPointAngle));
        frameValue = (frameValue + 360) % 360;
        deltaAngle = (nullDelta + frameValue + 360) % 360;
        currentFrame = (currentAngle - deltaAngle + 360) % 360;
        updateFrame();
    } else if (isSettingAngleImg) {
        let deltaX = event.clientX - coordX;
        let deltaY = event.clientY - coordY;
        let currentRotationAngle = Math.round((Math.atan2(deltaY, deltaX) * 180 / Math.PI));
        let angleValue = Math.round((currentRotationAngle - nullPointAngle));
        currentAngle = (nullAngle + angleValue + 360) % 360;
        currentFrame = (currentAngle - deltaAngle + 360) % 360;
        updateFrame();
        rotateThinSection()
    }

});

videoPlayer.addEventListener('touchstart', function (event) {
    isDragging = true;
    nullPoint = {x: event.touches[0].clientX, y: event.touches[0].clientY};
});

modeImage.addEventListener('touchstart', function (event) {
    isSettingFrameImg = true;
    nullPoint = {x: event.touches[0].clientX, y: event.touches[0].clientY};
});

rotateImage.addEventListener('touchstart', function (event) {
    isSettingAngleImg = true;
    nullPoint = {x: event.touches[0].clientX, y: event.touches[0].clientY};
});

document.addEventListener('touchend', function (event) {
    isDragging = false;
    nullFrame = currentFrame;
    nullAngle = currentAngle;
    nullDelta = deltaAngle;
    isSettingFrameImg = false;
    isSettingAngleImg = false;
});

document.addEventListener('touchmove', function (event) {
    if (isDragging) {
        let percentage = ((event.touches[0].clientX - nullPoint.x) / videoPlayer.offsetWidth);
        let frameValue = Math.round(percentage * 359);
        currentFrame = (nullFrame + frameValue + 1800) % 360;
        if (isRotating) {
            currentAngle = (nullAngle + frameValue + 1800) % 360;
        }
        deltaAngle = (currentAngle - currentFrame + 1800) % 360;
        updateFrame();
    } else if (isSettingFrameImg) {
        let percentage = ((event.touches[0].clientX - nullPoint.x) / modeImage.offsetWidth);
        let frameValue = Math.round(percentage * 359);
        deltaAngle = (nullDelta + frameValue + 1800) % 360;
        currentFrame = (currentAngle - deltaAngle + 1800) % 360;
        updateFrame();
    } else if (isSettingAngleImg) {
        let percentage = ((event.touches[0].clientX - nullPoint.x) / rotateImage.offsetWidth);
        let angleValue = Math.round(percentage * 359);
        currentAngle = (nullAngle + angleValue + 1800) % 360;
        currentFrame = (currentAngle - deltaAngle + 1800) % 360;
        updateFrame();
        rotateThinSection()
    }
});
