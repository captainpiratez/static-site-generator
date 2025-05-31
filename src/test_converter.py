from textnode import TextNode, TextType
from converter import split_nodes_delimiter  # Replace with your file name

def test_split_nodes_code():
    input_nodes = [TextNode("This is `code` here", TextType.TEXT)]
    result = split_nodes_delimiter(input_nodes, "`", TextType.CODE)
    assert len(result) == 3
    assert result[0].text == "This is "
    assert result[0].text_type == TextType.TEXT
    assert result[1].text == "code"
    assert result[1].text_type == TextType.CODE
    assert result[2].text == " here"
    assert result[2].text_type == TextType.TEXT

test_split_nodes_code()