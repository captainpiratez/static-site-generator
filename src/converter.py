from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text_type == TextType.TEXT:
                parts = node.text.split(delimiter)
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        node_type = TextType.TEXT
                    else:
                        node_type = text_type
                    new_nodes.append(TextNode(part, node_type))
            else:
                new_nodes.append(node)
    return new_nodes