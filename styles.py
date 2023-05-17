import configparser
from fonts import fonts

def generate_css(fonts):
    css = ""
    for name, url in fonts:
        css += f"""
@font-face {{
    font-family: '{name}';
    src: url('{url}') format('truetype');
}}
"""

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

    return css

def save_css(css):
    file_name = "styles.css"
    with open(file_name, "w") as file:
        file.write(css)
    print(f"CSS saved to {file_name}.")

def main():
    css = generate_css(fonts)
    save_css(css)

if __name__ == "__main__":
    main()
