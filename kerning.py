import configparser
import random
import os
import re
from fonts import fonts
from pangrams import pangrams
import ftplib
import urllib.parse


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def generate_text(pangram, length, mode="letter_pairs"):
    text = ""

    if mode == "pangram":
        text = " ".join([pangrams] * length)
    elif mode == "letter_pairs":
        pairs = [
            pangrams[i : i + 2]
            for i in range(len(pangrams) - 1)
            if pangrams[i].isalnum() and pangrams[i + 1].isalnum()
        ]
        for _ in range(length // 5):
            text += random.choice(pairs) + " "
    elif mode == "mixed":
        words = pangrams.split()
        for _ in range(length):
            text += random.choice(words) + " "
    else:
        raise ValueError("Invalid mode. Choose 'pangram', 'letter_pairs', or 'mixed'.")

    return text.strip()


def to_html(text):
    css = "\n".join(
        [
            f"""
        @font-face {{
            font-family: '{name}';
            src: url('{url}') format('truetype');
        }}
        """
            for name, url in fonts
        ]
    )

    css += """
    #controlPanel {
		position: fixed; 
		z-index: 1;        		
        top: 10px;
        right: 10px;
        background-color: #f0f0f0;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        display: none;
    }
    
    #controlPanel a {
  		text-decoration: none;
	}

	#controlPanel h1 {
		font-family: 'Cooley shape informal'; 
		font-size: 0.55em; 
		white-space: nowrap;
		margin-top: -20px;
		margin-bottom: 20px;
		}

	#sharelink {
		margin-top: 10px;
	}

    #toggleButton {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: #f0f0f0;
        padding: 5px 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        cursor: pointer;
    }
    
    body {
        font-family: cooley Draftsmanship;
        font-size: 16px;
        line-height: 1.5;
        margin: 0;
    }

    #textContainer {
        padding: 20px;
        background-color: #ffffff;
        color: #000000;
        font-size: 16px;
  		margin-top: -1em;
    }
    

	.random-color {
        animation: color 3s infinite;
    }

    @keyframes color {
        0% {
            color: #FF0000;
        }
        25% {
            color: #00FF00;
        }
        50% {
            color: #0000FF;
        }
        75% {
            color: #FF00FF;
        }
        100% {
            color: #FFFF00;
        }
    }
    """

    js = """
<script>
function changeFont() {
    let selectedFont = document.getElementById('fontSelector').value;
    document.getElementById('textContainer').style.fontFamily = selectedFont;
    updateUrl();
}

function changeFontSize() {
    let newSize = document.getElementById('fontSizeSlider').value;
    document.getElementById('textContainer').style.fontSize = newSize + 'px';
    document.getElementById('fontSizeValue').textContent = newSize;
}

function changeLetterSpacing() {
    let newSpacing = document.getElementById('letterSpacingSlider').value;
    document.getElementById('textContainer').style.letterSpacing = newSpacing + 'px';
    document.getElementById('letterSpacingValue').textContent = newSpacing; 
}

function changeLineHeight() {
    let newHeight = document.getElementById('lineHeightSlider').value;
    document.getElementById('textContainer').style.lineHeight = newHeight + 'px';
    document.getElementById('lineHeightValue').textContent = newHeight; 
}

function updateUrl() {
    let params = new URLSearchParams();
    params.set('fontSize', document.getElementById('fontSizeSlider').value);
    params.set('letterSpacing', document.getElementById('letterSpacingSlider').value);
    params.set('lineHeight', document.getElementById('lineHeightSlider').value);
    params.set('font', encodeURIComponent(document.getElementById('fontSelector').value));
    let updatedUrl = window.location.origin + window.location.pathname + '?' + params.toString();
    window.history.replaceState({}, '', updatedUrl);
    document.getElementById('shareLink').href = updatedUrl;
    // document.getElementById('shareLink').textContent = "Share this link: " + updatedUrl;
    document.getElementById('shareLink').textContent = "Share this link";
}

function updateUrl_new	() {
    let params = new URLSearchParams();
    params.set('fontSize', document.getElementById('fontSizeSlider').value);
    params.set('letterSpacing', document.getElementById('letterSpacingSlider').value);
    params.set('lineHeight', document.getElementById('lineHeightSlider').value);
    params.set('font', encodeURIComponent(document.getElementById('fontSelector').value));
    params.set('colorScheme', document.querySelector('input[name="colorScheme"]:checked').value);
    let updatedUrl = window.location.origin + window.location.pathname + '?' + params.toString();
    window.history.replaceState({}, '', updatedUrl);
    document.getElementById('shareLink').href = updatedUrl;
    // document.getElementById('shareLink').textContent = "Share this link: " + updatedUrl;
    document.getElementById('shareLink').textContent = "Share this link";
}

function loadSettingsFromUrl() {
    let params = new URLSearchParams(window.location.search);
    if (params.has('fontSize')) {
        document.getElementById('fontSizeSlider').value = params.get('fontSize');
        changeFontSize();
    }
    if (params.has('letterSpacing')) {
        document.getElementById('letterSpacingSlider').value = params.get('letterSpacing');
        changeLetterSpacing();
    }
    if (params.has('lineHeight')) {
        document.getElementById('lineHeightSlider').value = params.get('lineHeight');
        changeLineHeight();
    }
    if (params.has('font')) {
        let decodedFont = decodeURIComponent(params.get('font'));
        let fontSelector = document.getElementById('fontSelector');
        for (let i = 0; i < fontSelector.options.length; i++) {
            if (fontSelector.options[i].value === decodedFont) {
                fontSelector.selectedIndex = i;
                break;
            }
        }
        changeFont();
    }
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
    if (randomColors) {
        let spans = document.querySelectorAll('#textContainer span');
        for (let i = 0; i < spans.length; i++) {
            let r = Math.floor(Math.random() * 255);
            let g = Math.floor(Math.random() * 255);
            let b = Math.floor(Math.random() * 255);
            let color = `rgb(${r},${g},${b})`;
            spans[i].style.color = color;
        }
    } else {
        let spans = document.querySelectorAll('#textContainer span');
        for (let i = 0; i < spans.length; i++) {
            spans[i].style.color = textColor;
        }
    }
    updateUrl();
}

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



</script>
    """

    font_selector = """
    <select id="fontSelector" onchange="changeFont()" onchange="updateUrl()">
        {}
    </select>
    """.format(
        "\n".join([f'<option value="{name}">{name}</option>' for name, _ in fonts])
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
{css}
</style>
{js}
</head>
<body>
<div id="toggleButton" onclick="toggleControlPanel()">Toggle Controls</div>
<div id="controlPanel">
    <div style="text-align: right;">
        <button onclick="toggleControlPanel()" style="background: none; border: none;">X</button>
    </div>
    <div>
		<h1>
        	<a href="https://mastodon.social/@stevecooley" target="_blank" rel="noopener">
            	Steve Cooley Typefaces
        	</a>
    	</h1>    
    </div>
    <div>
        <label for="fontSizeSlider">Font size: </label>
        <input type="range" id="fontSizeSlider" min="6" max="300" value="16" oninput="changeFontSize()" onchange="updateUrl()">
        <span id="fontSizeValue">16</span>

    </div>
    <div>
		<label for="letterSpacingSlider">Letter spacing: </label>
        <input type="range" id="letterSpacingSlider" min="-50" max="100" value="0" oninput="changeLetterSpacing()" onchange="updateUrl()">
        <span id="letterSpacingValue">0</span>
    </div>
    <div>
        <label for="lineSpacingSlider">Line spacing: </label>
        <input type="range" id="lineHeightSlider" min="-10" max="300" value="16" oninput="changeLineHeight()" onchange="updateUrl()">
        <span id="lineHeightValue">16</span>
    </div>
    <div>
        <label for="fontSelector">Font: </label>
        {font_selector}
    </div>
    <div id="sharelink">
    	<a id="shareLink" href="" target="_blank" title="">Share</a>
	</div>
</div>
<div id="textContainer" style="font-family: cooleyshapesquareendsregular; font-size: 16px;">
{text}
</div>
</body>
</html>
"""


def save_html(text):
    file_name = "portfolio.html"
    with open(file_name, "w") as file:
        file.write(text)
    print(f"HTML saved to {file_name}.")


def upload_to_ftp(local_file, ftp_server, ftp_user, ftp_password, remote_path):
    with ftplib.FTP(ftp_server, ftp_user, ftp_password) as ftp:
        with open(local_file, "rb") as file:
            ftp.storbinary(f"STOR {remote_path}", file)
    print(f"File uploaded to {ftp_server}/{remote_path}.")


def main():
    text = generate_text(pangrams, 1, mode="pangram")
    html_text = to_html(text)
    save_html(html_text)

    config = read_config("config.ini")
    ftp_server = config.get("FTP", "server")
    ftp_user = config.get("FTP", "username")
    ftp_password = config.get("FTP", "password")
    remote_dir = config.get("FTP", "remote_path")
    remote_path = os.path.join(remote_dir, "portfolio.html")
    upload_to_ftp("portfolio.html", ftp_server, ftp_user, ftp_password, remote_path)


if __name__ == "__main__":
    main()
