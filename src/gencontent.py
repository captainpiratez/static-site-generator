from markdown_blocks import markdown_to_html_node
import htmlnode
import os

def extract_title(markdown):
    blocks = markdown.split("\n")
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block.startswith("# "):
            return stripped_block[2:].strip()
    raise Exception("title not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    content = html_node.to_html()
    html = template.replace("{{ Title }}", title) 
    html = html.replace("{{ Content }}", content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, mode="w") as file:
        file.write(html)