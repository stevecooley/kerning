function changeFont() {
    let selectedFont = document.getElementById('fontSelector').value;
    document.getElementById('textContainer').style.fontFamily = selectedFont;
    updateUrl();
}

function changeFontSize() {
    let newSize = document.getElementById('fontSizeSlider').value;
    document.getElementById('textContainer').style.fontSize = newSize + 'px';
    document.getElementById('fontSizeValue').textContent = newSize;

    // Calculate the new line height based on the font size
    let lineHeight = Math.round(newSize * 1.1);
    document.getElementById('lineHeightSlider').value = lineHeight;
    document.getElementById('lineHeightValue').textContent = lineHeight;
    document.getElementById('textContainer').style.lineHeight = lineHeight + 'px';

    updateUrl();
}

function handleAnchorClick(event) {
  event.preventDefault();
  const anchorTag = event.target.dataset.anchor;
  selectedAnchor = anchorTag;
  updateUrl();
}

function changeLetterSpacing() {
    let newSpacing = document.getElementById('letterSpacingSlider').value;
    document.getElementById('textContainer').style.letterSpacing = newSpacing + 'px';
    document.getElementById('letterSpacingValue').textContent = newSpacing;
    updateUrl();
}

function changeLineHeight() {
    let newHeight = document.getElementById('lineHeightSlider').value;
    document.getElementById('textContainer').style.lineHeight = newHeight + 'px';
    document.getElementById('lineHeightValue').textContent = newHeight;
    updateUrl();
}

function toggleControlPanel() {
    let controlPanel = document.getElementById('controlPanel');
    if (controlPanel.style.display === 'block') {
        controlPanel.style.display = 'none';
    } else {
        controlPanel.style.display = 'block';
    }
}

function changeColorScheme() {
    let colorScheme = document.querySelector('input[name="colorScheme"]:checked').value;
    let textContainer = document.getElementById('textContainer');

    if (colorScheme === 'black') {
        textContainer.classList.remove('random-color');
        textContainer.style.color = 'black';
        textContainer.style.backgroundColor = 'white';
    } else if (colorScheme === 'random') {
        textContainer.classList.add('random-color');
        textContainer.style.backgroundColor = 'white';
    }
    updateUrl();
}

function updateColorScheme() {
    let scheme = document.querySelector('input[name="colorScheme"]:checked').value;
    let textColor = "#000";
    let bgColor = "#fff";
    let randomColors = false;

    if (scheme === "randomColors") {
        randomColors = true;
    } else if (scheme === "blackOnWhite") {
        bgColor = "#fff";
        textColor = "#000";
    }

    document.body.style.backgroundColor = bgColor;
    document.body.style.color = textColor;

    let spans = document.querySelectorAll('#textContainer span');
    for (let i = 0; i < spans.length; i++) {
        if (randomColors) {
            let r = Math.floor(Math.random() * 255);
            let g = Math.floor(Math.random() * 255);
            let b = Math.floor(Math.random() * 255);
            let color = `rgb(${r},${g},${b})`;
            spans[i].style.color = color;
        } else {
            spans[i].style.color = textColor;
        }
    }
    updateUrl();
}

function updateUrl() {
    if (typeof updateUrl.timeoutId !== 'undefined') {
        clearTimeout(updateUrl.timeoutId);
    }

	let selectedAnchor = null;

    updateUrl.timeoutId = setTimeout(function() {
        let params = new URLSearchParams();
        params.set('fontSize', document.getElementById('fontSizeSlider').value);
        params.set('letterSpacing', document.getElementById('letterSpacingSlider').value);
        params.set('lineHeight', document.getElementById('lineHeightSlider').value);
        params.set('font', encodeURIComponent(document.getElementById('fontSelector').value));
        params.set('anchor', selectedAnchor || ''); // Include the selected anchor tag

        let updatedUrl = window.location.origin + window.location.pathname + '?' + params.toString();
        window.history.replaceState({}, '', updatedUrl);
        document.getElementById('shareLink').href = updatedUrl;
        document.getElementById('shareLink').textContent = 'Share this link';
    }, 100);
}


function loadSettingsFromUrl() {
    let params = new URLSearchParams(window.location.search);

    if (params.has('fontSize')) {
        document.getElementById('fontSizeSlider').value = params.get('fontSize');
        document.getElementById('fontSizeValue').textContent = params.get('fontSize');
        changeFontSize();
    }

    if (params.has('letterSpacing')) {
        document.getElementById('letterSpacingSlider').value = params.get('letterSpacing');
        document.getElementById('letterSpacingValue').textContent = params.get('letterSpacing');
        changeLetterSpacing();
    }

    if (params.has('lineHeight')) {
        document.getElementById('lineHeightSlider').value = params.get('lineHeight');
        document.getElementById('lineHeightValue').textContent = params.get('lineHeight');
        changeLineHeight();
    }

    if (params.has('font')) {
        document.getElementById('fontSelector').value = decodeURIComponent(params.get('font'));
        changeFont();
    }
}

function resetSettings() {
    document.getElementById('fontSizeSlider').value = 16;
    document.getElementById('letterSpacingSlider').value = 0;
    document.getElementById('lineHeightSlider').value = 16;
    // document.getElementById('fontSelector').value = 'cooleytrampoline';
    changeFontSize();
    changeLetterSpacing();
    changeLineHeight();
    changeFont();
    updateUrl();
}

window.onload = function() {
    loadSettingsFromUrl();

    document.getElementById('fontSizeSlider').addEventListener('input', changeFontSize);
    document.getElementById('letterSpacingSlider').addEventListener('input', changeLetterSpacing);
    document.getElementById('lineHeightSlider').addEventListener('input', changeLineHeight);
    document.getElementById('fontSelector').addEventListener('change', changeFont);
    document.getElementById('colorScheme').addEventListener('change', changeColorScheme);
    document.getElementById('toggleControlPanel').addEventListener('click', toggleControlPanel);
};
