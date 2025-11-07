# know limitations
# doesnt support '<' and '>'

import sys
import os
import re

def convert_emphasis(text: str):
    flags = re.DOTALL

    three_star_pattern = re.compile(r'(?<!\*)\*{3}(?!\*)(?P<content>.*?)(?<!\*)\*{3}(?!\*)', flags)
    two_star_pattern = re.compile(r'(?<!\*)\*{2}(?!\*)(?P<content>.*?)(?<!\*\*)\*{2}', flags)
    one_star_pattern = re.compile(r'(?<!\*)\*{1}(?!\*)(?P<content>.*?)(?<!\*)\*{1}(?!\*)', flags)

    three_score_pattern = re.compile(r'\b(?<!_)_{3}(?!_)(?P<content>.*?)(?<!_)_{3}(?!_)\b', flags)
    two_score_pattern = re.compile(r'\b(?<!_)_{2}(?!_)(?P<content>.*?)(?<!_)_{2}(?!_)\b', flags)
    one_score_pattern = re.compile(r'\b(?<!_)_{1}(?!_)(?P<content>.*?)(?<!_)_{1}(?!_)\b', flags)

    def clean_content(match):
        content = match.group('content')
        # Strip whitespace and replace newlines with spaces
        cleaned_content = " ".join(content.split())
        return cleaned_content

    def replace_three(match):
        cleaned_content = clean_content(match)
        if not cleaned_content: 
            return match.group(0)  
        return f'<em><strong>{cleaned_content}</strong></em>'

    def replace_two(match):
        cleaned_content = clean_content(match)
        if not cleaned_content: 
            return match.group(0) 
        return f'<strong>{cleaned_content}</strong>'

    def replace_one(match):
        cleaned_content = clean_content(match)
        if not cleaned_content: 
            return match.group(0) 
        return f'<em>{cleaned_content}</em>'

    text = re.sub(three_star_pattern, replace_three, text)
    text = re.sub(two_star_pattern, replace_two, text)
    text = re.sub(one_star_pattern, replace_one, text)

    text = re.sub(three_score_pattern, replace_three, text)
    text = re.sub(two_score_pattern, replace_two, text)
    text = re.sub(one_score_pattern, replace_one, text)

    return text
    # flags = re.DOTALL 

    # patterns = [] 
    # \S makes sure no white spaces so ** doesnt get converted
    # one_star_pattern = re.compile(r'\*(?P<content>[^*]+?)\*', flags)
    # two_star_pattern = re.compile(r'\*\*(?P<content>[^*]+?)\*\*', flags)
    # three_star_pattern = re.compile(r'\*\*\*(?P<content>[^*]+?)\*\*\*', flags)

    # one_score_pattern = re.compile(r'\b_(?P<content>[^*]+?)_\b', flags)
    # two_score_pattern = re.compile(r'\b__(?P<content>[^*]+?)__\b', flags) 
    # three_score_pattern = re.compile(r'\b___(?P<content>[^*]+?)___\b', flags)
    
    # patterns = [
    #     three_star_pattern, two_star_pattern, one_star_pattern,
    #     three_score_pattern, two_score_pattern, one_score_pattern
    # ]

    # for pattern in patterns:
    #     matches = re.findall(pattern, text)
    #     for match in matches:
    #         text = text.replace(match, match.replace('\n',' '))

    # text = re.sub(three_star_pattern, r'<em><strong>\1</strong></em>', text)
    # text = re.sub(two_star_pattern, r'<strong>\1</strong>', text)
    # text = re.sub(one_star_pattern, r'<em>\1</em>', text)

    # text = re.sub(three_score_pattern, r'<em><strong>\1</strong></em>', text)
    # text = re.sub(two_score_pattern, r'<strong>\1</strong>', text)
    # text = re.sub(one_score_pattern, r'<em>\1</em>', text)
    
def convert_paragraph(text: str):
    #print(f'[[[[[{text}]]]]]]')
    html_tag_pattern = re.compile(r'^<(/?h\d|/?ol|/?ul|/?li|/?p)>')
    paragraph_tag_pattern = re.compile(r'<p>(?P<content>.*?)</p>')
    lines = text.split('\n')
    converted_lines = []

    def clean_line(line):
        cleaned_content = " ".join(line.split())
        return cleaned_content

    for i, line in enumerate(lines):
        print('['+line+']')
        match = re.match(html_tag_pattern, line)
        if not match: # paragraph start
            if len(converted_lines)-1 >= 0:
                prev_item = converted_lines[len(converted_lines)-1]
                print(prev_item)
                para_match = re.match(paragraph_tag_pattern, prev_item)
                if para_match:
                    print(para_match)
                    content = para_match.group('content')
                    converted_lines.pop()
                    line = clean_line(line)
                    if not line:
                        continue
                    converted_lines.append(f'<p>{content}<br>{line}</p>')
                else:
                    line = clean_line(line)
                    if not line:
                        continue
                    converted_lines.append(f'<p>{line}</p>')
            else:
                line = clean_line(line)
                if not line:
                    continue
                converted_lines.append(f'<p>{line}</p>')
        else:
            converted_lines.append(line)
    return '\n'.join(converted_lines)

    # match = re.match(html_tag_pattern, text)
    # if match:
    #     #print(f'not match>>> {text} <<<')
    #     return text

    # converted_text = []
    
    # lines = []
    # for line in text.split('\n'):
    #     stripped_line = line.strip()
    #     if stripped_line: 
    #         lines.append(stripped_line)
    
    # if lines:
    #     paragraph_content = "<br>".join(lines)
    #     converted_text.append(f'<p>{paragraph_content}</p>')

    # #print(f'match>>> {"\n".join(converted_text)}<<<')
    # return "\n".join(converted_text)

def convert_headings(text: str):
    hashTag_pattern = re.compile(r'^(?P<hashTags>#{1,6})\s+(?P<header>.*)')
    alternate_pattern = re.compile(r'^(={2,})$|^(-{2,})$')
    print(text)
    lines = text.split("\n")
    converted_lines = []
    i = 0
    proccess_headings = True
    while i < len(lines):
        line = lines[i].strip()
        if not proccess_headings:
            converted_lines.append(line)
            i += 1
            continue

        match = re.match(hashTag_pattern, line)

        if match:
            level = len(match.group("hashTags"))
            content = " ".join(match.group("header").split())

            line = re.sub(hashTag_pattern, f'<h{level}>{content}</h{level}>', line)
            converted_lines.append(line)

        elif i+1 < len(lines) and re.match(alternate_pattern, lines[i+1]):
            next_line = lines[i+1]

            level = 1 if next_line[0] == '=' else 2
            content = line.strip()

            converted_lines.append(f'<h{level}>{content}</h{level}>')
            i += 1
        else:
            proccess_headings = False
            converted_lines.append(line)

        i += 1
    print("\n".join(converted_lines))
    return "\n".join(converted_lines)

# fix; right now its assuming each list item is one liner
def convert_list_helper(text: str, list_type: str):
    list_item_pattern = ""
    if list_type == "ol":
        list_item_pattern = re.compile(r'^\d+\.\s+(?P<item>.*)')
    elif list_type == "ul":
        list_item_pattern = re.compile(r'^[-\*\+]\s+(?P<item>.*)')
    else:
        sys.exit(1)

    is_list = re.match(list_item_pattern, text)
    if is_list:

        html_list = [f'<{list_type}>\n']
        lines = text.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()
            match = re.match(list_item_pattern, line)
            if match: # new list item
                content = ' '.join(match.group('item').split())
                html_list.append(f'<li>{content}')
                html_list.append('</li>\n')
            else:
                if html_list[len(html_list)-1] == '</li>\n':
                    html_list.pop()
                html_list.append(' ' + line.strip())
                html_list.append('</li>\n')

        html_list.append(f'</{list_type}>')
        return ''.join(html_list)
    else:
        return text

    # in_list = False
    # converted_lines = []
    # lines = text.split("\n")
    # for i, line in enumerate(lines):
    #     line = line.strip()

    #     match = re.match(list_item_pattern, line)
    #     if match:
    #         if not in_list:
    #             in_list = True
    #             converted_lines.append(f'<{list_type}>')

    #         content = match.group("item").strip()
    #         converted_lines.append(f'<li>{content}</li>')
    #     else:
    #         if in_list:
    #             converted_lines.append(f'</{list_type}>')
    #             in_list = False
            
    #         converted_lines.append(line)
    # if in_list:
    #     converted_lines.append(f'</{list_type}>')

    # return "\n".join(converted_lines)

def convert_ordered_list(text: str):
    return convert_list_helper(text , "ol")

def convert_unordered_list(text: str):
    return convert_list_helper(text , "ul")

def convert_code(text: str):
    code_pattern = re.compile(r'`(?P<content>.*?)`')
    def clean_content(match):
        content = match.group('content')
        # Strip whitespace and replace newlines with spaces
        cleaned_content = " ".join(content.split())
        return cleaned_content

    def replace_code(match):
        cleaned_content = clean_content(match)
        if not cleaned_content:
            return match.group(0) 
        return f'<code>{cleaned_content}</code>'

    text = re.sub(code_pattern, replace_code, text)
    return text
# assumes link is valid
def convert_link(text: str):
    url_pattern = re.compile(r'\[(?P<content>.*?)\]\((?P<link>.*?)\)')

    def clean_content(match):
        content = match.group('content')
        # Strip whitespace and replace newlines with spaces
        cleaned_content = " ".join(content.split())
        return cleaned_content

    def replace_link(match):
        link = match.group('link')
        cleaned_content = clean_content(match)
        return f'<a href="{link}">{cleaned_content}</a>'

    text = re.sub(url_pattern, replace_link, text)
    return text

def convert(text: str):
    
    blocks = text.strip().split("\n\n")

    converted_blocks = []
    for block in blocks:
        block = block.strip()
        block = convert_headings(block)
        block = convert_unordered_list(block)
        block = convert_ordered_list(block)
        block = convert_emphasis(block)
        block = convert_code(block)
        block = convert_link(block)
        block = convert_paragraph(block)
        converted_blocks.append(block)

    text = "\n".join(converted_blocks)
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