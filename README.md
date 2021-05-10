# pypdf-lib
 
A (maybe) Better PDF Parsing for Python focused on textual extraction. WIP. 

This library is a Python Wrapper built around [PdfAct](https://github.com/ad-freiburg/pdfact), which is built using Java.

## Pre-requisites

- `Java`

```bash
# Linux
apt-get update && apt-get install -y default-jre # openjdk-8-jre-headless / openjdk-11-jdk / openjdk-11-jre-headless

# Mac
brew install java

# Windows
# idk
```

## Installation

```python
!pip install --upgrade git+https://github.com/trisongz/pypdf-lib.git
!pip install --upgrade pypdf-lib

```

## Usage

```python
from pypdf import PyPDF
from fileio import File

base_dir = '/content/output'
File.mkdirs(base_dir)

# Using a remap function expects the file extension to be mapped properly - i.e. if 'txt' is selected, .txt file extension should be returned.

def remap_fnames(fname):
    fname = File.base(fname).replace('- ', '').replace(' ', '_').strip().replace('.pdf', '.json')
    return File.join(base_dir, fname)

converter = PyPDF(input_dir='/content/inputs', output_dir='/content/output', units=['paragraphs', 'blocks'], visualize=True)

# remap_funct is optional. 
for res in converter.extract(remap_funct=remap_fnames):
    print(res)
    # > /content/output/your_json_file_1.json

converter.extracted
'''
{'/content/inputs/input_1.pdf': '/content/output/your_json_file_1.json',
 '/content/inputs/input_2.pdf': '/content/output/your_json_file_2.json',
 '/content/inputs/input_3.pdf': '/content/output/your_json_file_3.json',
 'params': {'exclude_roles': None,
  'format': 'json',
  'include_roles': ['title',
   'body',
   'appendix',
   'keywords',
   'heading',
   'general_terms',
   'toc',
   'caption',
   'table',
   'other',
   'categories',
   'keywords',
   'page_header'],
  'units': ['paragraphs', 'blocks'],
  'visualize': True,
  'with_control_characters': False}}
'''
```