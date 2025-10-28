import sys
import os
import re

def convert_emphasis(text: str):
    lines = text.split('\n')

    one_star_pattern = re.compile(r'\*(\S|\S.*?\S)\*')
    two_star_pattern = re.compile(r'\*\*(\S|\S.*?\S)\*\*')
    three_star_pattern = re.compile(r'\*\*\*(\S|\S.*?\S)\*\*\*')

    one_score_pattern = re.compile(r'\b_(\S|\S.*?\S)_\b')
    two_score_pattern = re.compile(r'\b__(\S|\S.*?\S)__\b')
    three_score_pattern = re.compile(r'\b___(\S|\S.*?\S)___\b')

    text = re.sub(three_star_pattern, r'<em><strong>\1</strong></em>', text)
    text = re.sub(two_star_pattern, r'<strong>\1</strong>', text)
    text = re.sub(one_star_pattern, r'<em>\1</em>', text)

    text = re.sub(three_score_pattern, r'<em><strong>\1</strong></em>', text)
    text = re.sub(two_score_pattern, r'<strong>\1</strong>', text)
    text = re.sub(one_score_pattern, r'<em>\1</em>', text)

    return text
    
# def convert_paragraph(str):

def convert_headings(text: str):
    hashTag_pattern = re.compile(r'^(?P<hashTags>#{1,6})\s+(?P<header>.*)')
    alternate_pattern = re.compile(r'^(={2,})$|^(-{2,})$')
    
    lines = text.split("\n")
    converted_lines = []
    i = 0
    proccess_headings = True
    while i < len(lines):
        line = lines[i]
        if not proccess_headings:
            converted_lines.append(line)
            i += 1
            continue

        match = re.match(hashTag_pattern, line)

        if match:
            level = len(match.group("hashTags"))
            content = match.group("header").strip()

            head_id = content.replace(' ', '-').replace('*', '').replace('_', '')

            line = re.sub(hashTag_pattern, f'<h{level} id="{head_id}">{content}</h{level}>', line)
            converted_lines.append(line)

        elif i+1 < len(lines) and re.match(alternate_pattern, lines[i+1]):
            next_line = lines[i+1]

            level = 1 if next_line[0] == '=' else 2
            content = line.strip()

            head_id = content.replace(' ', '-').replace('*', '').replace('_', '')

            converted_lines.append(f'<h{level} id="{head_id}">{content}</h{level}>')
            i += 1
        else:
            proccess_headings = False
            converted_lines.append(line)

        i += 1

    return "\n".join(converted_lines)

# def convert_ordered_list(str):

# def convert_unordered_list(str):

def convert_code(text: str):
    code_pattern = re.compile(r'`(.*?)`')
    text = re.sub(code_pattern, r'<code>\1</code>', text)
    return text

def convert_link(text: str):
    url_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
    text = re.sub(url_pattern, r'<a href="\2">\1</a>', text)
    return text

def convert(text: str):
    
    blocks = text.split("\n\n")

    converted_blocks = []
    for block in blocks:
        block = convert_headings(block)
        block = convert_emphasis(block)
        block = convert_code(block)
        block = convert_link(block)

        converted_blocks.append(block)

    return "\n\n".join(converted_blocks)

def main():
    # md2html.py input.md output.html
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"invalid arguments expected (2 or 3) recieved ({len(sys.argv)})")
        print("Usage: python md2html.py input.md [output.html]")
        sys.exit(1)

    input_file = sys.argv[1]
    if os.path.splitext(input_file)[1] != ".md":
        print(f"input file is not a markdown file. recieved ({os.path.splitext(input_file)[1]})")
        print("Usage: python md2html.py input.md [output.html]")
        sys.exit(1)

    output_file = ""
    if len(sys.argv) == 3:
        output_file = sys.argv[2]

        if os.path.splitext(output_file)[1] != ".html":
            print(f"output file is not a html file. recieved ({os.path.splitext(output_file)[1]})")
            print("Usage: python md2html.py input.md [output.html]")
            sys.exit(1)
    else:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.html"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        html_output = convert(markdown_text)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)

        print("Done converting md to html")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    # except Exception as e:
    #     print(f"Error during conversion: {e}")
    #     sys.exit(1)

if __name__ == "__main__":
    main()