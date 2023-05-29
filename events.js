document.addEventListener('DOMContentLoaded', function() {
    loadSettingsFromUrl();
});

document.querySelectorAll('input[name="colorScheme"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
        updateColorScheme();
        updateUrl();
    });
});

document.getElementById('toggleButton').addEventListener('click', toggleControlPanel);

document.getElementById('fontSelector').addEventListener('change', function() {
    changeFont();
    updateUrl();
});

document.getElementById('fontSizeSlider').addEventListener('input', function() {
    changeFontSize();
    updateUrl();
});

document.getElementById('letterSpacingSlider').addEventListener('input', function() {
    changeLetterSpacing();
    updateUrl();
});

document.getElementById('lineHeightSlider').addEventListener('input', function() {
    changeLineHeight();
    updateUrl();
});

// Add event listeners to the anchor tags
const anchorTags = document.getElementsByClassName('anchor-link');
for (let i = 0; i < anchorTags.length; i++) {
    anchorTags[i].addEventListener('click', function(event) {
        event.preventDefault();
        const anchorTag = event.target.dataset.anchor;
        selectedAnchor = anchorTag;
        updateUrlWithAnchor(anchorTag);
    });
}

function updateUrlWithAnchor(anchorTag) {
    if (typeof updateUrlWithAnchor.timeoutId !== 'undefined') {
        clearTimeout(updateUrlWithAnchor.timeoutId);
    }

    updateUrlWithAnchor.timeoutId = setTimeout(function() {
        let params = new URLSearchParams();
        params.set('anchor', anchorTag);
        params.set('fontSize', document.getElementById('fontSizeSlider').value);
        params.set('letterSpacing', document.getElementById('letterSpacingSlider').value);
        params.set('lineHeight', document.getElementById('lineHeightSlider').value);
        params.set('font', encodeURIComponent(document.getElementById('fontSelector').value));

        let updatedUrl = window.location.origin + window.location.pathname + '?' + params.toString();
        window.history.replaceState({}, '', updatedUrl);
        document.getElementById('shareLink').href = updatedUrl;
        document.getElementById('shareLink').textContent = 'Share this link';
    }, 100);
}

// Add event listeners to the anchor buttons
const anchorButtons = document.getElementsByClassName('anchor-button');
for (let i = 0; i < anchorButtons.length; i++) {
    anchorButtons[i].addEventListener('click', function(event) {
        event.preventDefault();
        const anchorTag = event.target.dataset.anchor;
        selectedAnchor = anchorTag;
        updateUrlWithAnchor(anchorTag);
    });
}
