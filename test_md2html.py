from md2html import convert_emphasis, convert_headings, convert_code, convert_link, convert_ordered_list, convert_paragraph, convert_unordered_list, convert
import pytest

@pytest.mark.parametrize("content,expected", [
    ('This is how to *italicize*.',         'This is how to <em>italicize</em>.'),
    ('all that glitters is **not** gold',   'all that glitters is <strong>not</strong> gold'),
    ('This text is ***really important***.','This text is <em><strong>really important</strong></em>.'),
    ('This is how to _italicize_.',         'This is how to <em>italicize</em>.'),
    ('This text is really im___port___ant.','This text is really im___port___ant.'),
    ('This text is ___really important___.','This text is <em><strong>really important</strong></em>.'),
])
def test_convert_emphasis_normal(content,expected):
    assert convert_emphasis(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('''***
        this is a multi
        line 
        emphasis 
        ***''',                         '<em><strong>this is a multi line emphasis</strong></em>'),
    ('******',                          '******'),
    ('***   ***',                       '***   ***'),
    ('''Some text ***
        multi-line
        emphasis*** more text''',       'Some text <em><strong>multi-line emphasis</strong></em> more text'),
    ('***text with __bold__ inside***', '<em><strong>text with <strong>bold</strong> inside</strong></em>'),
    ('****four stars****',              '****four stars****'),
    ('''___
        this is a multi
        line 
        emphasis 
        ___''',                         '<em><strong>this is a multi line emphasis</strong></em>'),
    ('______',                          '______'),
    ('___   ___',                       '___   ___'),
    ('''Some text ___
        multi-line
        emphasis___ more text''',       'Some text <em><strong>multi-line emphasis</strong></em> more text'),
    ('___text with **bold** inside___', '<em><strong>text with <strong>bold</strong> inside</strong></em>'),
    ('____four underscores____',        '____four underscores____'),
])
def test_convert_emphasis_edge(content,expected):
    assert convert_emphasis(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('this is a normal paragraph','<p>this is a normal paragraph</p>'),
    ('This is a paragraph\nwith multiple lines\nbut should be one paragraph.','<p>This is a paragraph<br>with multiple lines<br>but should be one paragraph.</p>'),
    ('   theres extra   spaces\nin   this paragraph   ', '<p>theres extra spaces<br>in this paragraph</p>')
])
def test_convert_paragraph_normal(content, expected):
    assert convert_paragraph(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('',''),
    ('<h1>heading that should be put in paragraph</h1>', '<h1>heading that should be put in paragraph</h1>'),
    ('\n\n\n',''),
    ('<strong>This should be inside paragraph</strong>','<p><strong>This should be inside paragraph</strong></p>')
])
def test_convert_paragraph_edge(content, expected):
    assert convert_paragraph(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('# This is normal heading','<h1>This is normal heading</h1>'),
    ('Alternative Heading\n------','<h2>Alternative Heading</h2>'),
    ('  ###   The h3   header   with extra   space', '<h3>The h3 header with extra space</h3>')
])
def test_convert_heading_normal(content, expected):
    assert convert_headings(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('########## Too many hashtags','########## Too many hashtags'),
    ('#missing the space inbetween','#missing the space inbetween'),
    ('Not valid\nheading------','Not valid\nheading------'),
    ('# multiple\n  ###### headings\n in one block\n=======', '<h1>multiple</h1>\n<h6>headings</h6>\n<h1>in one block</h1>')
])
def test_convert_heading_edge(content, expected):
    assert convert_headings(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('1. item1\n2. item2\n3. item3', '<ol>\n<li>item1</li>\n<li>item2</li>\n<li>item3</li>\n</ol>'),
    ('1.invalid', '1.invalid'),
    ('1. numbers\n50. dont\n20. matter', '<ol>\n<li>numbers</li>\n<li>dont</li>\n<li>matter</li>\n</ol>'),
])
def test_convert_ordered_list_normal(content, expected):
    assert convert_ordered_list(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('''1.   extra
          2.   spaces   
        3. in    items''', '<ol>\n<li>extra</li>\n<li>spaces</li>\n<li>in items</li>\n</ol>'),
    ('1. multi\nline\nlist item', '<ol>\n<li>multi line list item</li>\n</ol>'),
    ('1. items with extra 2.\n3. 4. number 4', '<ol>\n<li>items with extra 2.</li>\n<li>4. number 4</li>\n</ol>'),
])
def test_convert_ordered_list_edge(content, expected):
    assert convert_ordered_list(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('* item1\n* item2\n* item3', '<ul>\n<li>item1</li>\n<li>item2</li>\n<li>item3</li>\n</ul>'),
    ('*invalid', '*invalid'),
    ('* symbol\n+ dont\n- matter', '<ul>\n<li>symbol</li>\n<li>dont</li>\n<li>matter</li>\n</ul>'),
])
def test_convert_unordered_list_normal(content, expected):
    assert convert_unordered_list(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('''*   extra
          *   spaces   
        * in    items''', '<ul>\n<li>extra</li>\n<li>spaces</li>\n<li>in items</li>\n</ul>'),
    ('- multi\nline\nlist item', '<ul>\n<li>multi line list item</li>\n</ul>'),
    ('+ items with extra -\n* + symbols +', '<ul>\n<li>items with extra -</li>\n<li>+ symbols +</li>\n</ul>'),
])
def test_convert_unordered_list_edge(content, expected):
    assert convert_unordered_list(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('This is `code`.', 'This is <code>code</code>.'),
    ('I prefer `pytest` over `unittest`.', 'I prefer <code>pytest</code> over <code>unittest</code>.'),
    ("This has no 'code' elements.", "This has no 'code' elements."),
])
def test_convert_code_normal(content, expected):
    assert convert_code(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('``', '``'),
    ('', ''),
    ('`  code with   extra    spaces  `', '<code>code with extra spaces</code>'),
])
def test_convert_code_edge(content, expected):
    assert convert_code(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('[text](url).', '<a href="url">text</a>.'),
    ('[ extra   spaces ](https://example.com).', '<a href="https://example.com">extra spaces</a>.'),
    ("[]()", '<a href=""></a>'),
])
def test_convert_link_normal(content, expected):
    assert convert_link(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('[[double nessed brackets]](url).', '<a href="url">[double nessed brackets]</a>.'),
    ('[](https://example.com).', '<a href="https://example.com"></a>.'),
    ('[**bold**](url)', '<a href="url">**bold**</a>'),
])
def test_convert_link_edge(content, expected):
    assert convert_link(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('''
# Simple Markdown

This is a simple markdown file

1. list item 1
2. list item 2
3. list item 3

I can **bold**, _italicize_, or ___both___

* this is nice
* this is fun''', '''<h1>Simple Markdown</h1>
<p>This is a simple markdown file</p>
<ol>
<li>list item 1</li>
<li>list item 2</li>
<li>list item 3</li>
</ol>
<p>I can <strong>bold</strong>, <em>italicize</em>, or <em><strong>both</strong></em></p>
<ul>
<li>this is nice</li>
<li>this is fun</li>
</ul>'''),
    ('''# Simple Markdown
## The second one

this paragraph has a [link](url)

now we are in a second paragraph

this paragraph is 
multiple lines''', '''<h1>Simple Markdown</h1>
<h2>The second one</h2>
<p>this paragraph has a <a href="url">link</a></p>
<p>now we are in a second paragraph</p>
<p>this paragraph is<br>multiple lines</p>'''),
    ('''#### Simple markdown
part 3
------

Im ***running*** out of_things_to **test *I* hop**e

* its correct
hopefully
+ theres no bugs
- and ''', '''<h4>Simple markdown</h4>
<h2>part 3</h2>
<p>Im <em><strong>running</strong></em> out of_things_to <strong>test <em>I</em> hop</strong>e</p>
<ul>
<li>its correct hopefully</li>
<li>theres no bugs</li>
<li>and</li>
</ul>'''),
])

def test_convert_normal(content, expected):
    assert convert(content) == expected

@pytest.mark.parametrize("content,expected", [
    ('''# Now
## I'm 
### bad at markdown
so theres going to be bad syntax
hopefully nothing goes bad
----

This is a paragraph
1. I didnt start this list correctly

Lets try again
*oppes still not right

######yeah... i give up''','''<h1>Now</h1>
<h2>I'm</h2>
<h3>bad at markdown</h3>
<p>so theres going to be bad syntax<br>hopefully nothing goes bad<br>----</p>
<p>This is a paragraph<br>1. I didnt start this list correctly</p>
<p>Lets try again<br>*oppes still not right</p>
<p>######yeah... i give up</p>'''),
    ('''# markdown #5

**
one
more
time
**

This list isnt formated the best

1. line1
line2
line 3
2. does it still work?''','''<h1>markdown #5</h1>
<p><strong>one more time</strong></p>
<p>This list isnt formated the best</p>
<ol>
<li>line1 line2 line 3</li>
<li>does it still work?</li>
</ol>'''),
    ('''# LAST ONE
This is the last test

*yAY*
-----

Lets see this **bold** and _italicized_ [___link___](url)

Lets have some empty cases ``, **, ******, ______,
[](),

1. **BOLD** 
2. _hi_

### random heading

* hi
- hello
how 
you 
doing''','''<h1>LAST ONE</h1>
<p>This is the last test</p>
<h2><em>yAY</em></h2>
<p>Lets see this <strong>bold</strong> and <em>italicized</em> <a href="url"><em><strong>link</strong></em></a></p>
<p>Lets have some empty cases ``, <strong>,</strong>****, ______,<br><a href=""></a>,</p>
<ol>
<li><strong>BOLD</strong></li>
<li><em>hi</em></li>
</ol>
<h3>random heading</h3>
<ul>
<li>hi</li>
<li>hello how you doing</li>
</ul>''')
])
def test_convert_edge(content, expected):
    assert convert(content) == expected