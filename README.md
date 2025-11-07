# MarkDown to HTML

## Known Limitations

* Proper paragraph lists are not supported. After a new line the converter assumes its a new paragraph and not a part of the previous list item.
* Nested lists not supported
* Nested conversions not fully supported. ie `***bold** italised*` should convert to `<em><strong>bold</strong> italised</em>` but doesnt
* Horizontal Rules, Blockquotes, Images, Muilti line code blocks, Line breaks, etc are not supported
* Text in code blocks not protected from further conversions. `**bold**` will be converted even tho its in a code block
* Links arent verified or checked that they have been properly encoded
* Special characters like 'greater than' or 'less than' are left as is and not properly esacped in the final html
* HTML Tags embedding aren't supported. Some tags like `<h>, <ol>, <li>` are just assumed be valid and others arent proccessed and will be surrounded by paragraph tags
* Headings can normally have extra # symbols at the end that dont change the text. This is not supported

## How to run tests using pytest

Entering the following commands in the command line will create and activate a new environment named md2html that has the nessary packages to run the script and the tests 

1. `conda env create -f environment.yml`
2. `conda activate md2html`

To run the test verify that the current directory contains the md2html.py and test_md2html.py files and run

1. `pytest`

To run the main script by itself 

1. `python md2html.py input.md output.md`
