import configparser
import ftplib
# import random
import os
# import re
from fonts import fonts
from pangrams import pangrams
# import urllib.parse

pangram_anchors = [
    {
        "label": "Uppercase",
        "anchor": "UPPERCASE",
    },
    {
        "label": "Lowercase",
        "anchor": "lowercase",
    },
    {
        "label": "Uppercase Words",
        "anchor": "Uppercase-Words",
    },
    {
        "label": "Mixed Case Words",
        "anchor": "mIxEd-CaSe-WoRdS",
    },
    {
        "label": "Character Table",
        "anchor": "Character-Table",
    },
    {
        "label": "Lowercase Kerning",
        "anchor": "lowercase-kerning",
    },
    {
        "label": "Uppercase Kerning",
        "anchor": "UPPERCASE-kerning",
    },
    {
        "label": "Mixed Case Kerning",
        "anchor": "mIxEd-CaSe-kerning",
    }
]


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def generate_text(length):
    text = ""
    text = " ".join([pangrams] * length)
    return text.strip()


def to_html(text):


    js = """
<script>
<!-- I'm trying :( -->

</script>
    """

    font_selector = """
    <select id="fontSelector" onchange="changeFont()" onchange="updateUrl()">
        {}
    </select>
    """.format(
        "\n".join([f'<option value="{name}">{name}</option>' for name, _ in fonts])
    )

    css_link = '<link rel="stylesheet" href="styles.css">'
    js_link = '<script src="javascript.js"></script><script src="events.js"></script>'
    # Check if it's a mobile device
    is_mobile = """
    <script>
        function isMobileDevice() {
            return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
        }

        if (isMobileDevice()) {
            document.getElementsByTagName("html")[0].classList.add("is-mobile");
        }
    </script>
"""

        # Generate the text links
    links = []
    for item in pangram_anchors:
        anchor = item["anchor"]
        label = item["label"]
        link = f'<a href="#{anchor}">{label}</a> <br> '
        links.append(link)
    
    # Print the links
    anchor_tags = "Jump to: <br>"
    for link in links:
        anchor_tags += link
        anchor_tags += "\n"
        
    return f"""<!DOCTYPE html>
    <meta charset="UTF-8">
<html>
<head>


{css_link}
{js}
{js_link}
{is_mobile}
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
        <input type="range" id="fontSizeSlider" min="10" max="100" value="16" oninput="changeFontSize()" onchange="updateUrl()">
        <span id="fontSizeValue">16</span>
    </div>
    <div>
		<label for="letterSpacingSlider">Letter spacing: </label>
        <input type="range" id="letterSpacingSlider" min="-15" max="20" value="0" oninput="changeLetterSpacing()" onchange="updateUrl()">
        <span id="letterSpacingValue">0</span>
    </div>
    <div>
        <label for="lineSpacingSlider">Line spacing: </label>
        <input type="range" id="lineHeightSlider" min="-5" max="100" value="16" oninput="changeLineHeight()" onchange="updateUrl()">
        <span id="lineHeightValue">16</span>
    </div>
    <div>
        <label for="fontSelector">Font: </label>
        {font_selector}
    </div>
    <div id="sharelink">
    	<a id="shareLink" href="" target="_blank" title="">Share</a>
    	<span class="spacer"></span>
    	<button id="resetButton" onclick="resetSettings()">Reset</button>
	</div>
	<div>
	    {anchor_tags}
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

    text = generate_text(1)
    html_text = to_html(text)
    save_html(html_text)

    config = read_config("config.ini")
    ftp_server = config.get("FTP", "server")
    ftp_user = config.get("FTP", "username")
    ftp_password = config.get("FTP", "password")
    remote_dir = config.get("FTP", "remote_path")
    
    remote_path = os.path.join(remote_dir, "portfolio.html")
    upload_to_ftp("portfolio.html", ftp_server, ftp_user, ftp_password, remote_path)

    remote_path = os.path.join(remote_dir, "styles.css")
    upload_to_ftp("styles.css", ftp_server, ftp_user, ftp_password, remote_path)

    remote_path = os.path.join(remote_dir, "events.js")
    upload_to_ftp("events.js", ftp_server, ftp_user, ftp_password, remote_path)

    remote_path = os.path.join(remote_dir, "javascript.js")
    upload_to_ftp("javascript.js", ftp_server, ftp_user, ftp_password, remote_path)

if __name__ == "__main__":
    main()
