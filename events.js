document.addEventListener('DOMContentLoaded', function() {
    loadSettingsFromUrl();
});

document.querySelectorAll('input[name="colorScheme"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
        updateColorScheme();
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
