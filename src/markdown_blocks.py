from enum import Enum
import re
from htmlnode import *
from textnode import *
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html = HTMLNode("div")
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                heading_node = heading_to_html_node(block)
                children.append(heading_node)
            case BlockType.CODE:
                code_node = code_to_html_node(block)
                children.append(code_node)
            case BlockType.QUOTE:
                quote_node = quote_to_html_node(block)
                children.append(quote_node)
            case BlockType.ULIST:
                ulist_node = ulist_to_html_node(block)
                children.append(ulist_node)
            case BlockType.OLIST:
                olist_node = olist_to_html_node(block)
                children.append(olist_node)
            case BlockType.PARAGRAPH:
                paragraph_node = paragraph_to_html_node(block)
                children.append(paragraph_node)
    return ParentNode("div", children)


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    if re.match(r"^```(.*?)```", markdown, re.DOTALL):
        return BlockType.CODE
    if re.match(r"^(> ?.*\n?)+$", markdown, re.MULTILINE):
        return BlockType.QUOTE
    if re.match(r"^(- ?.*\n?)+$", markdown, re.MULTILINE):
        return BlockType.ULIST
    if re.match(r"^(\d+\. .*\n?)+$", markdown, re.MULTILINE):
        lines = [line for line in markdown.split('\n') if line.strip()]
        for idx, line in enumerate(lines):
            expected = f"{idx+1}. "
            if not line.startswith(expected):
                break
        else:
            return BlockType.OLIST
    return BlockType.PARAGRAPH


def heading_to_html_node(markdown):
    if markdown.startswith(("# ")):
        tag = "h1"
        text = markdown[2:]
    elif markdown.startswith(("## ")):
        tag = "h2"
        text = markdown[3:]
    elif markdown.startswith(("### ")):
        tag = "h3"
        text = markdown[4:]
    elif markdown.startswith(("#### ")):
        tag = "h4"
        text = markdown[5:]
    elif markdown.startswith(("##### ")):
        tag = "h5"
        text = markdown[6:]
    elif markdown.startswith(("###### ")):
        tag = "h6"
        text = markdown[7:]
    else:
        raise Exception("invalid heading")
    return ParentNode(tag, text_to_children(text))


def code_to_html_node(block):
    text = block[4:-3]  # ``` kısımlarını çıkar
    # LeafNode kullan çünkü code tag'inin içinde sadece text var
    code_node = LeafNode("code", text)
    # ParentNode kullan çünkü pre tag'inin içinde child var
    return ParentNode("pre", [code_node])



def paragraph_to_html_node(paragraph):
    # Satır sonlarını boşluklarla değiştir
    lines = paragraph.split("\n")
    text = " ".join(lines)
    return ParentNode("p", text_to_children(text))


def quote_to_html_node(block):
    lines = block.split("\n")  # Satırlara böl
    cleaned_lines = []
    for line in lines:
        # Her satırdan > ve boşluğu çıkar
        cleaned_line = line.lstrip("> ")  # > ve boşlukları temizle
        cleaned_lines.append(cleaned_line)
    
    # Satırları birleştir
    text = " ".join(cleaned_lines)
    return ParentNode("blockquote", text_to_children(text))


def ulist_to_html_node(block):
    lines = block.split("\n")  # Satırlara böl
    list_items = []
    
    for line in lines:
        # Her satırdan "- " kısmını çıkar
        text = line[2:]  # "- " kısmını çıkar
        # Her item için <li> oluştur
        li_node = ParentNode("li", text_to_children(text))
        list_items.append(li_node)
    
    # Tüm li'ları ul içine koy
    return ParentNode("ul", list_items)


def olist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        # Her satırdan "1. ", "2. " vs kısmını çıkar
        # Nokta ve boşluğu bul
        dot_index = line.find(". ")
        text = line[dot_index + 2:]  # ". " sonrasını al
        
        # Her item için <li> oluştur
        li_node = ParentNode("li", text_to_children(text))
        list_items.append(li_node)
    
    # Tüm li'ları ol içine koy
    return ParentNode("ol", list_items)


def text_to_children(text):
    nodes = []
    # Use your inline markdown parsing function to split text into TextNodes
    text_nodes = text_to_textnodes(text)
    for t_node in text_nodes:
        html_node = text_node_to_html_node(t_node)
        nodes.append(html_node)
    return nodes
    

def parse_inline_markdown(markdown):
    # Split on backticks (will give you alternating non-code/code)
    parts = re.split(r"(`[^`]+`)", markdown)
    nodes = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            nodes.append(TextNode(part[1:-1], "code"))  # remove backticks
        else:
            nodes.append(TextNode(part, "text"))
    return nodes