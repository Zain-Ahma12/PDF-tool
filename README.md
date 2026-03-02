# PDF Page Select Tool

A lightweight Python utility for extracting specific pages from PDF files. This tool allows you to select individual pages or page ranges from a source PDF and create a new PDF containing only those pages.

## Features

- **Flexible Page Selection**: Select individual pages or ranges (e.g., `"11-15"`, `"22"`, `"100-103"`)
- **Automatic Sorting**: Pages are automatically sorted by their starting page number
- **Duplicate Removal**: Automatically removes duplicate page selections
- **Error Handling**: Validates page numbers and provides descriptive error messages
- **Partial Output Recovery**: If an invalid page number is encountered, saves all successfully processed pages to a partial output file
- **Simple API**: Easy-to-use Python function with clear documentation

## Requirements

- Python 3.7+
- PyMuPDF (fitz) - PDF manipulation library

## Installation

### Prerequisites
Ensure you have Python 3.7 or later installed on your system.

### Setup

1. **Clone or download this project** to your desired location

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv vir_env
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     vir_env\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source vir_env/bin/activate
     ```

4. **Install PyMuPDF**:
   ```bash
   pip install PyMuPDF
   ```

## Project Structure

```
pdf-tool/
├── main.py                    # Entry point with usage example
├── pdf_page_select_tool.py   # Core extraction function
├── Input/                     # Place source PDF files here
├── Output/                    # Successfully processed PDFs saved here
├── Partial processed pdf/     # Partially processed PDFs (if errors occur)
├── vir_env/                   # Virtual environment directory
├── README.md                  # This file
└── LICENSE                    # MIT License
```

## Usage

### Basic Usage

```python
from pdf_page_select_tool import extract_pages

# Define pages to extract
pages = ["11-15", "22", "100-103"]

# Extract pages and save result
extract_pages(
    input_path="Input/test.pdf",
    pages=pages,
    output_path="final_processed.pdf"
)
```

### API Reference

#### `extract_pages(input_path, pages, output_path="final_processed.pdf")`

Extracts specific pages from a PDF file and saves the result to a new PDF file.

**Parameters:**
- `input_path` (str): Path to the input PDF file
  - *Example*: `"Input/document.pdf"` or `r"Input\document.pdf"` (Windows)
  
- `pages` (list): List of page numbers or ranges (1-based indexing)
  - *Individual pages*: `["1", "5", "10"]`
  - *Page ranges*: `["11-15", "50-60"]`
  - *Mixed*: `["1", "11-15", "22", "100-103"]`
  - Pages can be in any order (will be sorted automatically)
  - Duplicates are automatically removed
  
- `output_path` (str, optional): Output filename (default: `"final_processed.pdf"`)
  - The file will be saved to the `Output/` directory on success
  - On error, a partial file (if any pages were successfully extracted) is saved to `Partial processed pdf/`

**Returns:**
- `None` (prints success message)

**Raises:**
- `ValueError`: If a page number is out of range (exceeds total pages in PDF)
  - A partial output file will be saved containing all successfully extracted pages

**Examples:**

```python
# Example 1: Extract specific pages from a textbook
pages = ["11-15", "22", "51-54", "100-103"]
extract_pages(
    input_path="Input/textbook.pdf",
    pages=pages,
    output_path="selected_chapters.pdf"
)
```

```python
# Example 2: Extract single pages
pages = ["1", "5", "10", "15"]
extract_pages(
    input_path="Input/document.pdf",
    pages=pages,
    output_path="important_pages.pdf"
)
```

```python
# Example 3: Extract a large range
pages = ["1-50"]
extract_pages(
    input_path="Input/large_document.pdf",
    pages=pages,
    output_path="first_50_pages.pdf"
)
```

## How It Works

1. **Parse Input**: The function accepts a list of page specifications (individual pages and/or ranges)
2. **Sort Pages**: All entries are sorted by their starting page number
3. **Expand Ranges**: Page ranges (e.g., "11-15") are expanded into individual page numbers
4. **Remove Duplicates**: Duplicate page numbers are automatically removed
5. **Validate**: Each page number is checked to ensure it exists in the source PDF
6. **Extract**: Valid pages are individually inserted into the output PDF in order
7. **Save**: The resulting PDF is saved to the `Output/` directory
8. **Error Handling**: If an invalid page is encountered, any successfully extracted pages are saved to `Partial processed pdf/`

## Error Handling

If you encounter an error with an out-of-range page number:

1. A partial PDF file will be saved with successfully extracted pages
2. The error message will indicate:
   - Which page number caused the error
   - The original entry that contained it
   - Total pages in the PDF
   - Location of the partial output file

**Example error:**
```
ValueError: Page number 400 (from entry 400-450) is out of range. PDF has 350 page(s) total.
Partial output (50 page(s)) saved to Partial processed pdf\final_processed.pdf
```

## Tips & Best Practices

- **Page Indexing**: Pages are 1-based (first page is 1, not 0)
- **Mixed Order**: Pages don't need to be in order - they'll be sorted automatically
  ```python
  pages = ["50-60", "1-10", "100"]  # Will be sorted
  ```
- **Unsorted Output**: The extracted pages appear in sorted order in the output PDF
- **Large PDFs**: For very large PDFs, consider breaking the extraction into smaller batches
- **File Paths**: Use raw strings (`r"..."`) for Windows paths to avoid issues with backslashes
  ```python
  # Windows example
  extract_pages(r"Input\my_file.pdf", pages=["1-10"])
  ```

## Common Use Cases

### Research Papers
Extract specific chapters or sections from academic papers:
```python
pages = ["1", "5-10", "15-20", "50-60"]  # Abstract, intro, related work, conclusion
extract_pages("Input/paper.pdf", pages, "selected_sections.pdf")
```

### Textbook Chapters
Extract required chapters for a course:
```python
pages = ["11-15", "22", "51-54", "63-68", "70-76"]
extract_pages("Input/textbook.pdf", pages, "course_materials.pdf")
```

### Document Consolidation
Combine relevant sections from multiple documents by running the tool multiple times

### Page Filtering
Remove unwanted pages (advertisements, blank pages, etc.) by specifying only desired pages

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fitz'"
**Solution**: Ensure PyMuPDF is installed
```bash
pip install PyMuPDF
```

### Issue: "FileNotFoundError" for input PDF
**Solution**: 
- Verify the file path is correct
- Use absolute paths for clarity: `os.path.join(os.getcwd(), "Input", "file.pdf")`
- Ensure the file exists in the `Input/` directory

### Issue: Pages appear in wrong order
**Solution**: This is expected behavior - pages are sorted by starting page number. If you want pages in a specific order, adjust your page list accordingly.

### Issue: Virtual environment not activating
**Solution**: 
- Ensure you're using the correct activation command for your OS
- Windows: Use `vir_env\Scripts\activate.bat` if `.activate` doesn't work
- Linux/macOS: Use `source vir_env/bin/activate`

## Performance

- **Speed**: Depends on PDF size and number of pages
- **Memory**: Loads entire PDFs into memory; acceptable for documents under 1GB
- **File Size Output**: Typically smaller than the input PDF since fewer pages are included

## Dependencies

- **PyMuPDF (fitz)**: Industry-standard PDF manipulation library
  - Fast and efficient
  - Supports reading and writing PDFs
  - Pure Python bindings to MuPDF C library

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Improve documentation

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [How It Works](#how-it-works) section for detailed operation information
3. Check error messages carefully - they usually indicate the exact problem

## Changelog

### Version 1.0
- Initial release
- Basic page extraction functionality
- Error handling and partial output recovery
- Support for individual pages and ranges

## Future Enhancements

Potential future features:
- GUI interface for easier page selection
- Batch processing multiple PDFs
- Page rotation and manipulation
- PDF merging from multiple sources
- Command-line interface (CLI)
- Progress indicators for large files

## Disclaimer

This tool is intended for legitimate and lawful purposes. Users are responsible for ensuring they have the right to extract and use pages from PDF files. Always respect copyright and licensing agreements.

---

**Created**: 2026  
**Python Version**: 3.7+  
**Last Updated**: March 2, 2026
