# Static Site Generator

A Python-based static site generator that converts Markdown files into HTML pages. This tool provides a complete pipeline for building static websites from Markdown content with support for various Markdown features including headings, lists, code blocks, quotes, images, and links.

## Features

- **Markdown to HTML Conversion**: Full Markdown syntax support
  - Headings (H1-H6)
  - Bold and italic text
  - Code blocks and inline code
  - Ordered and unordered lists
  - Block quotes
  - Links and images
- **Recursive Directory Processing**: Automatically processes nested content directories
- **Static Asset Copying**: Copies CSS, images, and other static files to the output directory
- **Template System**: Uses HTML templates with variable replacement
- **Base Path Support**: Configurable base path for deployment flexibility

## Project Structure

```
static-site-generator/
├── content/              # Markdown source files
│   ├── index.md
│   ├── blog/
│   └── contact/
├── static/               # Static assets (CSS, images)
│   ├── index.css
│   └── images/
├── docs/                 # Generated HTML output
├── src/                  # Source code
│   ├── main.py          # Entry point
│   ├── gencontent.py    # Page generation logic
│   ├── copystatic.py    # Static file copying
│   ├── markdown_blocks.py   # Block-level Markdown parsing
│   ├── inline_markdown.py   # Inline Markdown parsing
│   ├── htmlnode.py      # HTML node classes
│   ├── textnode.py      # Text node classes
│   └── test_*.py        # Unit tests
├── template.html         # HTML template
├── build.sh             # Build script
├── main.sh              # Run script
└── test.sh              # Test script
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/captainpiratez/static-site-generator.git
cd static-site-generator
```

2. Ensure Python 3.x is installed:
```bash
python3 --version
```

## Usage

### Basic Usage

Run the site generator with default settings (base path `/`):
```bash
python3 src/main.py
```

### Custom Base Path

Specify a custom base path for deployment to subdirectories:
```bash
python3 src/main.py /my-site/
```

### Using Scripts

```bash
# Build the site
./build.sh

# Run the generator
./main.sh

# Run tests
./test.sh
```

## How It Works

### 1. Content Processing

The generator reads Markdown files from the `content/` directory and converts them to HTML:

1. **Directory Traversal**: Recursively scans the content directory
2. **Markdown Parsing**: Parses Markdown syntax into an abstract syntax tree
3. **HTML Generation**: Converts the tree into HTML nodes
4. **Template Application**: Injects content into the HTML template
5. **File Writing**: Writes the generated HTML to the `docs/` directory

### 2. Static Asset Handling

All files in the `static/` directory (CSS, images, fonts, etc.) are recursively copied to the `docs/` directory, preserving the directory structure.

### 3. Template System

The `template.html` file supports the following placeholders:
- `{{ Title }}`: Replaced with the page title (extracted from the first H1 heading)
- `{{ Content }}`: Replaced with the generated HTML content

## Markdown Support

### Headings
```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Text Formatting
```markdown
**bold text**
*italic text*
`inline code`
```

### Lists
```markdown
- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2
```

### Code Blocks
````markdown
```
def hello():
    print("Hello, world!")
```
````

### Quotes
```markdown
> This is a quote
> Multiple lines supported
```

### Links and Images
```markdown
[Link text](https://example.com)
![Alt text](image.jpg)
```

## API Reference

### Core Modules

#### `main.py`
Entry point for the generator.

**Functions:**
- `main()`: Orchestrates the build process

**Configuration:**
- `dir_path_static`: Source directory for static files (default: `./static`)
- `dir_path_public`: Output directory (default: `./docs`)
- `dir_path_content`: Source directory for Markdown files (default: `./content`)
- `template_path`: HTML template file (default: `./template.html`)

#### `gencontent.py`
Handles Markdown to HTML conversion.

**Functions:**
- `generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)`: Recursively processes all Markdown files
- `generate_page(from_path, template_path, dest_path, basepath)`: Converts a single Markdown file to HTML
- `extract_title(md)`: Extracts the page title from Markdown content

#### `markdown_blocks.py`
Block-level Markdown parsing.

**Functions:**
- `markdown_to_html_node(markdown)`: Converts Markdown string to HTML node tree
- `markdown_to_blocks(markdown)`: Splits Markdown into block-level elements
- `block_to_block_type(block)`: Identifies the type of a Markdown block

**BlockType Enum:**
- `PARAGRAPH`
- `HEADING`
- `CODE`
- `QUOTE`
- `UNORDERED_LIST`
- `ORDERED_LIST`

#### `inline_markdown.py`
Inline Markdown parsing (bold, italic, code, links, images).

**Functions:**
- `text_to_textnodes(text)`: Converts raw text to TextNode objects
- `split_nodes_delimiter(old_nodes, delimiter, text_type)`: Splits nodes by delimiter
- `split_nodes_image(old_nodes)`: Extracts image nodes
- `split_nodes_link(old_nodes)`: Extracts link nodes
- `extract_markdown_images(text)`: Finds image syntax
- `extract_markdown_links(text)`: Finds link syntax

#### `htmlnode.py`
HTML node classes for building HTML trees.

**Classes:**
- `HTMLNode`: Base class for HTML nodes
- `LeafNode`: Node with no children (e.g., `<p>text</p>`)
- `ParentNode`: Node with children (e.g., `<div>...</div>`)

#### `textnode.py`
Text representation with type information.

**Classes:**
- `TextNode`: Represents a piece of text with formatting
- `TextType` Enum: TEXT, BOLD, ITALIC, CODE, LINK, IMAGE

**Functions:**
- `text_node_to_html_node(text_node)`: Converts TextNode to HTMLNode

## Testing

The project includes comprehensive unit tests for all modules.

### Run All Tests
```bash
python3 -m unittest discover
```

### Run Specific Test Modules
```bash
python3 -m unittest src.test_htmlnode
python3 -m unittest src.test_textnode
python3 -m unittest src.test_inline_markdown
python3 -m unittest src.test_markdown_blocks
```

### Test Coverage
- HTML node creation and rendering
- Text node conversion
- Inline Markdown parsing (bold, italic, code, links, images)
- Block-level Markdown parsing (headings, lists, quotes, code blocks)
- End-to-end content generation

## Development

### Adding New Markdown Features

1. **Inline features**: Add parsing logic to `inline_markdown.py`
2. **Block features**: Add parsing logic to `markdown_blocks.py`
3. **Add tests**: Create test cases in the appropriate test file
4. **Update documentation**: Document the new feature in this README

### Project Guidelines

- Follow PEP 8 style guidelines
- Write unit tests for all new features
- Keep functions small and focused
- Use type hints where appropriate
- Document complex logic with comments

## Configuration

### Customizing Paths

Edit the path variables in `main.py`:
```python
dir_path_static = "./static"    # Change static files location
dir_path_public = "./docs"      # Change output location
dir_path_content = "./content"  # Change content location
template_path = "./template.html"  # Change template location
```

### Customizing the Template

Edit `template.html` to change the HTML structure. The template must include:
- `{{ Title }}` placeholder for the page title
- `{{ Content }}` placeholder for the generated content

## Troubleshooting

### Common Issues

**Issue**: "No title found" error
**Solution**: Ensure each Markdown file has a level 1 heading (`# Title`)

**Issue**: Images/CSS not loading
**Solution**: Check that static files are in the `static/` directory and paths are correct

**Issue**: Links broken after deployment
**Solution**: Use the base path argument when running: `python3 src/main.py /your-base-path/`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Inspired by popular static site generators like Jekyll and Hugo
- Built as a learning project for understanding Markdown parsing and static site generation
- Boot.dev Guideded Project

