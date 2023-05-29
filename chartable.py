import unicodedata

def generate_unicode_table(start, end):
    table = '<table id="characterTable">\n'
    table += '  <tr>\n'
    table += '    <th class="staticfontright">Code</th>\n'
    table += '    <th class="staticfontright">Character</th>\n'
    table += '    <th class="staticfontleft">Name</th>\n'
    table += '  </tr>\n'

    for code_point in range(start, end+1):
        char = chr(code_point)
        name = unicodedata.name(char, 'Unknown')
        code = f'U+{code_point:04X}'
        table += f'  <tr>\n'
        table += f'    <td class="staticfontright"><a href="https://unicodeplus.com/{code}">{code}</a></td>\n'
        table += f'    <td class="activefont">{char}</td>\n'
        table += f'    <td class="staticfontleft"><a href="https://en.wikipedia.org/wiki/{code}">{name}</a></td>\n'
        table += f'  </tr>\n'

    table += '</table>'
    return table


# Save the Unicode table to a file
file_name = 'chartable.html'
def save_unicode_table(text, file_name):
    with open(file_name, "w") as file:
        file.write(text)
    print(f"Unicode table saved to {file_name}.")

def main(output_file=False):
    # Generate the Unicode table from U+0000 to U+00FF, eventually
    unicode_table = generate_unicode_table(0x0020, 0x007E)
    unicode_table += generate_unicode_table(0x00A0, 0x00FF)

    if output_file:
        save_unicode_table(unicode_table, "chartable.txt")
    else:
        print(unicode_table)


if __name__ == "__main__":
    main(output_file=True)