import os
from pypdf import PdfMerger  # Changed from PyPDF2 to pypdf
import glob

def merge_pdfs(folder_path):
    # Get all subdirectories in the given folder
    subdirs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

    # List of folders to exclude
    exclude_folders = ["ZZZ Done", "ZZZ Not Done"]

    for subdir in subdirs:
        # Skip excluded folders
        if subdir in exclude_folders:
            print(f"Skipping excluded folder: {subdir}")
            continue

        subdir_path = os.path.join(folder_path, subdir)
        pdf_files = glob.glob(os.path.join(subdir_path, "*.pdf"))

        # If there's more than one PDF file in the subdirectory
        if len(pdf_files) > 1:
            merger = PdfMerger()

            for pdf in pdf_files:
                merger.append(pdf)

            # Create the output filename
            output_filename = f"merged_{subdir}.pdf"
            output_path = os.path.join(subdir_path, output_filename)

            # Write the merged PDF
            merger.write(output_path)
            merger.close()

            print(f"Merged PDFs in {subdir} into {output_filename}")
        else:
            print(f"No PDFs to merge in {subdir}")

# Replace this with your actual folder path
root_folder = r"C:\Users\921722\Royal HaskoningDHV\P-PC6298-Hunterston - Team\WIP\4. Geotechnical\02. OpenGround\1. Inputs\2. Lab Test Extraction"

merge_pdfs(root_folder)