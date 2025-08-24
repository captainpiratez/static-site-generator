import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node
from htmlnode import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)

    def test_code_block(self):
        code = "```\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block(self):
        quote = "> This is a quote\n> on two lines"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_unordered_list(self):
        ul = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(ul), BlockType.ULIST)

    def test_ordered_list(self):
        ol = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol), BlockType.OLIST)

    def test_paragraph(self):
        para = "Just a normal paragraph of text."
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# This is a heading

## This is h2

### This is h3 with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>This is a heading</h1><h2>This is h2</h2><h3>This is h3 with <b>bold</b> text</h3></div>"
        self.assertEqual(html, expected)

    def test_quote_block(self):
        md = """
> This is a quote
> with multiple lines
> and _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote with multiple lines and <i>italic</i> text</blockquote></div>"
        self.assertEqual(html, expected)

    def test_unordered_list(self):
        md = """
- First item with **bold**
- Second item
- Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item with <b>bold</b></li><li>Second item</li><li>Third item with <code>code</code></li></ul></div>"
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with _italic_
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item</li></ol></div>"
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
