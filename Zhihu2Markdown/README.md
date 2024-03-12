# Zhihu2Markdown

# ==============

## Description
This is a simple tool to convert Zhihu answer to markdown file.
Specifically finetuned for math formula.

## Configuration

Replace configs in `config.json` with your own.

## Usage
`main.py` [-h] [-o OUTPUT] [-i IMAGE_DIR] article_url

Transform zhihu article to Markdown format

positional arguments:
  article_url           URL of zhihu article

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name
  -i IMAGE_DIR, --image_dir IMAGE_DIR
                        If present, download image to the image dir path
