---
name: pdf-tools
description: "Extract text, merge, split, and manipulate PDF files. Convert PDF to text/markdown."
metadata: {"nanobot":{"emoji":"📄","requires":{"bins":["python3"]},"python_packages":["pypdf2","pdfplumber"]}}
---

# PDF Tools Skill

Extract, merge, split, and manipulate PDF files.

## Extract Text from PDF

### Using pdfplumber (Best for Text)
```python
import pdfplumber

# Extract all text
with pdfplumber.open('document.pdf') as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
    print(text)

# Save to file
with pdfplumber.open('document.pdf') as pdf:
    with open('output.txt', 'w') as f:
        for page in pdf.pages:
            f.write(page.extract_text() + '\n\n')

# Extract text from specific page
with pdfplumber.open('document.pdf') as pdf:
    print(pdf.pages[0].extract_text())  # First page
```

### Using PyPDF2
```python
from PyPDF2 import PdfReader

reader = PdfReader('document.pdf')
text = ''
for page in reader.pages:
    text += page.extract_text()
print(text)

# Get number of pages
print(f"Pages: {len(reader.pages)}")

# Extract specific page
print(reader.pages[0].extract_text())
```

### CLI One-Liner
```bash
python -c "import pdfplumber; [print(p.extract_text()) for p in pdfplumber.open('file.pdf').pages]"
```

## Merge PDFs

```python
from PyPDF2 import PdfMerger

merger = PdfMerger()

# Add multiple PDFs
merger.append('file1.pdf')
merger.append('file2.pdf')
merger.append('file3.pdf')

# Write merged PDF
merger.write('merged.pdf')
merger.close()

# Merge with bookmark
merger = PdfMerger()
merger.append('file1.pdf', bookmark='Section 1')
merger.append('file2.pdf', bookmark='Section 2')
merger.write('merged_bookmarked.pdf')
```

## Split PDF

```python
from PyPDF2 import PdfReader, PdfWriter

# Split into individual pages
reader = PdfReader('document.pdf')
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f'page_{i+1}.pdf', 'wb') as out:
        writer.write(out)

# Split into ranges
reader = PdfReader('document.pdf')

# First 5 pages
writer = PdfWriter()
for i in range(5):
    writer.add_page(reader.pages[i])
with open('part1.pdf', 'wb') as out:
    writer.write(out)

# Pages 10-20
writer = PdfWriter()
for i in range(9, 20):
    writer.add_page(reader.pages[i])
with open('part2.pdf', 'wb') as out:
    writer.write(out)
```

## Extract Images from PDF

```python
import pdfplumber
from PIL import Image
import io

with pdfplumber.open('document.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        for j, image in enumerate(page.images):
            # Extract image data
            if 'stream' in image:
                img_data = image['stream'].get_data()
                with open(f'page{i+1}_img{j}.png', 'wb') as f:
                    f.write(img_data)
```

## PDF to Markdown

```python
import pdfplumber

def pdf_to_markdown(pdf_path, md_path):
    """Convert PDF to Markdown file."""
    with pdfplumber.open(pdf_path) as pdf:
        with open(md_path, 'w') as f:
            for i, page in enumerate(pdf.pages):
                f.write(f"# Page {i+1}\n\n")
                text = page.extract_text()
                # Basic formatting
                lines = text.split('\n')
                for line in lines:
                    f.write(line + '\n')
                f.write('\n---\n\n')

pdf_to_markdown('document.pdf', 'output.md')
```

## Get PDF Metadata

```python
from PyPDF2 import PdfReader

reader = PdfReader('document.pdf')
print(f"Title: {reader.metadata.get('/Title', 'N/A')}")
print(f"Author: {reader.metadata.get('/Author', 'N/A')}")
print(f"Subject: {reader.metadata.get('/Subject', 'N/A')}")
print(f"Creator: {reader.metadata.get('/Creator', 'N/A')}")
print(f"Pages: {len(reader.pages)}")
print(f"Encrypted: {reader.is_encrypted}")
```

## Rotate PDF Pages

```python
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader('input.pdf')
writer = PdfWriter()

for page in reader.pages:
    page.rotate(90)  # Rotate 90 degrees clockwise
    writer.add_page(page)

with open('rotated.pdf', 'wb') as out:
    writer.write(out)
```

## Add Watermark

```python
from PyPDF2 import PdfReader, PdfWriter

# Load watermark
watermark = PdfReader('watermark.pdf').pages[0]

reader = PdfReader('document.pdf')
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open('watermarked.pdf', 'wb') as out:
    writer.write(out)
```

## Complete Analysis Script

```python
import pdfplumber
import json

def analyze_pdf(pdf_path):
    """Extract comprehensive info from PDF."""
    result = {
        'file': pdf_path,
        'pages': 0,
        'text_length': 0,
        'tables': [],
        'content': []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        result['pages'] = len(pdf.pages)
        
        for i, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text()
            result['text_length'] += len(text)
            result['content'].append({
                'page': i + 1,
                'text': text[:500] + '...' if len(text) > 500 else text
            })
            
            # Extract tables
            tables = page.extract_tables()
            for j, table in enumerate(tables):
                result['tables'].append({
                    'page': i + 1,
                    'table': j + 1,
                    'rows': len(table),
                    'cols': len(table[0]) if table else 0
                })
    
    # Save analysis
    with open('pdf_analysis.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    return result

# Run
info = analyze_pdf('document.pdf')
print(f"Pages: {info['pages']}, Tables: {len(info['tables'])}")
```

## Install Dependencies

```bash
pip install pypdf2 pdfplumber pillow
```

## Tips

- `pdfplumber` is better for text extraction with layout
- `PyPDF2` is better for manipulation (merge, split, rotate)
- Use `pdf2image` to convert PDF pages to images
- For OCR PDFs, use `pytesseract` with `pdf2image`
- Handle encrypted PDFs: `reader.decrypt('password')`
