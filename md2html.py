import sys
import os
import re

# def convert_emphasis(str):

# def convert_paragraph(str):

def convert_headings(text: str):
    
    lines = text.split('\n')

    hashTag_pattern = re.compile(r'^(?P<hashTags>#{1,6})\s+(?P<header>.*)$')
    alternate_pattern = re.compile(r'^(={2,})$|^(-{2,})')
    converted_strings = []
    for i, line in enumerate(lines):
        match = re.match(hashTag_pattern, line)
        if match:
            level = len(match.group("hashTags"))
            content = match.group("header")
            line = re.sub(hashTag_pattern, f"<h{level}>{content}</h{level}>", line)
            converted_strings.append(line)
            continue

        match = re.match(alternate_pattern, lines[i])
        if match:
            level = 1 if line[0] == '=' else 2

            content = ""
            if i>0:
                content = lines[i-1]
                converted_strings.pop()

            converted_strings.append(f"<h{level}>{content}<h{level}>")
            continue

        converted_strings.append(line)

    return "\n".join(converted_strings)

# def convert_ordered_list(str):

# def convert_unordered_list(str):

# def convert_code(str):

# def convert_link(str):

def convert(text: str):
    

    text = convert_headings(text)
    return text

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