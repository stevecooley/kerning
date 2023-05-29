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

#characterTable {
    border-collapse: collapse;
    width: 100%;
    padding: 8px;
    text-align: left;
}

#characterTable td {
    border: 1px solid #ddd;
}


.staticfontright {
    font-family: Helvetica;
    font-size: 16px;
    line-height: 1.5;
    text-align: right;
    padding: 10px;
}

.staticfontleft {
    font-family: Helvetica;
    font-size: 16px;
    line-height: 1.5;
    text-align: left;
    padding: 10px;
}

#characterTable td.activefont {
    font-family: inherit;
    text-align: center;
    padding: 20px;
    width: 25%;
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

.is-mobile #controlPanel {
    display: block;
    background-color: #cccccc;
    padding: 10px;
}

.is-mobile #toggleButton {
    display: block;
}

select,
input[type="range"] {
    width: 85%;
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 5px;
    margin-bottom: 10px;
    font-size: 16px;
    color: #000000;
}

.is-mobile select {
    height: 60px;
}

.is-mobile input[type="range"] {
    height: 20px;
}

@media screen and (max-width: 767px) {
    #controlPanel {
        padding: 10px;
    }

    .is-mobile select,
    .is-mobile input[type="range"] {
        padding: 5px;
    }
}

#resetButton {
    margin-left: 10px;
    background-color: #f0f0f0;
    padding: 5px 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
}

.is-mobile .spacer {
  margin-left: 20px; /* Adjust the value as needed */
}

.spacer {
  margin-left: 100px; /* Adjust the value as needed */
}

#anchorButtons {
    display: flex;
    justify-content: center;
    margin-top: 5px;
}

.anchor-button {
    margin: 0 5px;
    padding: 5px 5px;
    background-color: #f5f5f5;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.anchor-button:hover {
    background-color: #e0e0e0;
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
