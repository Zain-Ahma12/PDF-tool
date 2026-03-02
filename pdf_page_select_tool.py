import fitz # PyMuPDF - library for reading and writing PDF files
import os # Standard library for file and directory operations

def extract_pages(input_path: str, pages: list, output_path: str = "final_processed.pdf") -> None:
    """
    Extracts specific pages from a PDF file and saves the result to a new PDF file.
    
    ---
    Parameters:
    - input_path (str): The path to the input PDF file.
    -pages            : List of pages number/ranges (1-based, e.g. ["417", "456-611"]).
                        Can be unsorted - the function will sort it automatically.
    - output_path (str): Output filename (default: final_processed.pdf).
                         Saved to 'Output/' on success, or 'Partial processed pdf/' on error.
    
    ---
    Output:
    - On success: A new PDF file containing the specified pages, save to Output folder
    
    ---
    Example:
    - extract_pages(
        input_path="Input/test.pdf", // can be changed
        pages=["417", "456-611"], // can be changed
        output_path="final_processed.pdf" // can be changed
    )
    """
    
    # 1. Sort the pages list by the starting page number of each entry.
    def sort_key(entry: str) -> int:
        """
        Helper function to sort a list of page entries. 
        Extracts the first number from the entry and returns it as an integer.
        """
        return int(entry.split("-")[0])
    
    pages = sorted(pages, key=sort_key) #Sort entries in ascending order by their starting page number
    
    # 2. Expand ranges and remove duplicates and create an ordered list of unique ints.
    
    seen = set()      # Tracks already-added page numbers to avoide duplicates
    page_numbers = [] # Final ordered list of unique page numbers
    
    for entry in pages:            # Loop through each entry (e.g. "11-15" or "22")
        entry = entry.strip()      # Remove leading and trailing whitespace
        
        if "-" in entry:           # If the entry is a range (e.g. "11-15")
            start, end = map(int, entry.split("-")) # Extract the start and end page numbers
            for p in range(start, end + 1):        # Loop through each page number in the range
                if p not in seen:                  # Only add the page number if it hasn't been added before
                    seen.add(p)                    # Add the page number to the seen set
                    page_numbers.append(p)         # Add the page number to the ordered list
        else:                                      # If the entry is not a range (e.g. "11")
            p = int(entry)
            if p not in seen:                      # Only add the page number if it hasn't been added before
                seen.add(p)                        # Add the page number to the seen set
                page_numbers.append(p)             # Add the page number to the ordered list
                

    # 3. Open source PDF and prepare output PDF
    source_pdf = fitz.open(input_path) # Open the source PDF file
    total_pages = source_pdf.page_count # Get the total number of pages in the source PDF
    
    output_dir = os.path.join(os.getcwd(), "Output")                 # Define the output directory
    partial_dir = os.path.join(os.getcwd(), "Partial processed pdf") # Define the partial output directory
    
    os.makedirs(output_dir, exist_ok=True) # Create the output directory if it doesn't exist
    os.makedirs(partial_dir, exist_ok=True) # Create the partial output directory if it doesn't exist
    
    # 4. Build the output PDF page by page
    
    output_pdf = fitz.open() # Open the output PDF file for writing
    
    def find_original_entry(page_num: int) -> str:
        """
        Return the original entry string (e.g. "11-15") that contains the given page number.
        """
        for entry in pages: # Check each original entry
            entry = entry.strip()                       # Remove leading and trailing whitespace
            if "-" in entry:                            # If it is a range
                start, end = map(int, entry.split("-")) # Extract the start and end page numbers
                if start <= page_num <= end:            # If the given page number is within the range
                    return entry                        # Return the original entry string
                else:
                    if int(entry) == page_num:         # If the given page number is a single page
                        return entry                   # Return the original entry string
        return str(page_num)
        
    for page_num in page_numbers:                      # Iterate over each resolved page number
        if page_num > total_pages or page_num < 1:     # If the page number is out of range
            partial_path = os.path.join(partial_dir, output_path) # Build the partial output path
            pages_saved = len(output_pdf)
            if pages_saved > 0:
                output_pdf.save(partial_path) # Save the partial output PDF
            output_pdf.save(partial_path) # Save the partial output PDF
            source_pdf.close() # Close the source PDF file
            output_pdf.close() # Close the output PDF file
            
            original_entry = find_original_entry(page_num) # Find the original entry that caused the error
            raise ValueError(
                f"Page number {page_num} (from entry {original_entry}) is out of range. "
                f"PDF has {total_pages} page(s) total.\n"
                f"Partial output ({pages_saved} page(s)) saved to {partial_path}"
            )
        
        output_pdf.insert_pdf(source_pdf, from_page=page_num-1, to_page=page_num-1, start_at=output_pdf.page_count) # Insert the page from the source PDF into the output PDF    
        
    final_path = os.path.join(output_dir, output_path) # Build the full path for the final output PDF file
    
    output_pdf.save(final_path) # Save the final output PDF file
    output_pdf.close() # Close the output PDF file
    source_pdf.close() # Close the source PDF file
    
    print(f"Successfully extracted {len(page_numbers)} page(s) from {input_path} to {final_path}")
    
    
    if __name__ == "__main__":
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
    "736-738"
]
        input_path = r"Input\test.pdf" # can be changed
        output_path = "final_processed.pdf" # can be changed
        
        extract_pages(
            input_path=input_path,
            pages=pages,
            output_path=output_path
        )