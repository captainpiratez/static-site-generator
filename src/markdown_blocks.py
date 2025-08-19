from enum import Enum
import re
from htmlnode import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                html = HTML
                pass
            case BlockType.CODE:
                pass
            case BlockType.QUOTE:
                pass
            case BlockType.ULIST:
                pass
            case BlockType.OLIST:
                pass
            case BlockType.PARAGRAPH:
                pass


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