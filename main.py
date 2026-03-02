from pdf_page_select_tool import extract_pages
import fitz # PyMuPDF - library for reading and writing PDF files
import os # Standard library for file and directory operations


pages = [
    "11-15",
    "22",
    "51-54",
    "63-68",
    "70-76",
    "80-82",
    "85-90",
    "93-96",
    "100-103",
    "128-137",
    "144-146",
    "168-171",
    "183-193",
    "253",
    "260-261",
    "277",
    "293-294",
    "301-312",
    "322-333",
    "345-346",
    "417",
    "419",
    "423-438",
    "444-446",
    "461-468",
    "476-478",
    "487-496",
    "512-513",
    "516",
    "526-534",
    "536-539",
    "541-545",
    "552-554",
    "559-562",
    "574-624",
    "627-631",
    "653-667",
    "669-672",
    "683-704",
    "720-728",
    "736-738",
    "759-791"
]

input_path = r"Input\test.pdf" # can be changed
output_path = "final_processed.pdf" # can be changed
        
extract_pages(
    input_path=input_path,
    pages=pages,
    output_path=output_path
)