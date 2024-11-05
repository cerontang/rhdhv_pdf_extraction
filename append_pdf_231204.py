import pdfplumber
import PyPDF2

def extract_pages_with_keyword(source_pdf_path, keyword, output_pdf_path):
    # Create a PDF writer object for the output file
    pdf_writer = PyPDF2.PdfFileWriter()

    # Open the source PDF file
    with pdfplumber.open(source_pdf_path) as pdf:
        # Iterate through each page in the PDF
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            # Check if the keyword exists in the current page
            if keyword.lower() in text.lower():
                # If keyword is found, read the page with PyPDF2
                pdf_reader = PyPDF2.PdfFileReader(source_pdf_path)
                # Add the current page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(i))

    # Write the pages with the keyword to the output file
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"Created '{output_pdf_path}' with pages containing '{keyword}'.")

# Example usage
source_pdf = r'C:\Users\921722\Downloads\CIRIA\CIRIA C574 - Copy-unlocked.pdf'  # Replace with your source PDF file path
keyword = 'permeability'
output_pdf = r'C:\Users\921722\Downloads\CIRIA\output\CIRIA C574_filtered.pdf'  # Replace with your desired output PDF file path

extract_pages_with_keyword(source_pdf, keyword, output_pdf)