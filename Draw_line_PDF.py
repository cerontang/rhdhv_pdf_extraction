from pypdf import PdfReader, PdfWriter
from pypdf.generic import AnnotationBuilder

pdf_path = r"C:\Users\921722\OneDrive - Royal HaskoningDHV\230125 BH Extraction\folder\test page\test page.pdf"
reader = PdfReader(pdf_path)
page = reader.pages[0]
writer = PdfWriter()
writer.add_page(page)

# Add the line
annotation = AnnotationBuilder.rectangle(
    rect=(50, 550, 200, 650),
)
writer.add_annotation(page_number=0, annotation=annotation)

# Write the annotated file to disk
with open("annotated-pdf.pdf", "wb") as fp:
    writer.write(fp)