import fitz
import os

def extract_images_from_pages(pdf_path, output_folder, start_page=0, end_page=None):
    """
    Extracts images from a specified range of pages in a PDF document.

    Args:
        pdf_path (str): The path to the input PDF file.
        output_folder (str): The directory to save the extracted images.
        start_page (int): The 0-based index of the first page to process (inclusive).
        end_page (int, optional): The 0-based index of the last page to process (exclusive).
                                  If None, processes until the end of the document.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path) # Open the PDF document
    if end_page is None:
        end_page = doc.page_count

    print(f"Processing pages {start_page} to {end_page-1}...")

    # Use a set to store unique image XREFs to avoid duplicates
    image_xrefs = set()

    for page_num in range(start_page, end_page):
        # Ensure the page number is valid
        if 0 <= page_num < doc.page_count:
            page = doc[page_num]
            # Get a list of all images referenced by the page
            images = page.get_images(full=True)
            for img in images:
                xref = img[0]
                image_xrefs.add(xref)
                
    print(f"Found {len(image_xrefs)} unique images in the specified pages.")

    for index, xref in enumerate(image_xrefs):
        # Extract the image data
        image_dict = doc.extract_image(xref)
        if image_dict:
            image_bytes = image_dict["image"]
            image_ext = image_dict["ext"] # Get the original image extension (png, jpeg, bmp, etc.)
            
            # Save the image file
            image_filename = os.path.join(output_folder, f"image_{index+1}_xref{xref}.{image_ext}")
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
            print(f"Saved {image_filename}")

    doc.close()
    print("Image extraction complete.")

# Example usage:
# Replace "your_document.pdf" with your file path
# Replace "output_images" with your desired output folder
# This example extracts images from pages 0, 1, and 2
extract_images_from_pages("./encartes/encarte.pdf", "./images", start_page=0)
