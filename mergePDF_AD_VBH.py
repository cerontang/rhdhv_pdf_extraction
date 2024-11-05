import os
from PyPDF2 import PdfFileMerger
import pdfplumber

received_file_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20230928 Extraction\PSD'
file_mainDir = os.listdir(received_file_path)
print(file_mainDir)

merger_fugro = PdfFileMerger()
#merger_AHAM = PdfFileMerger()

for fileName in file_mainDir:
    if not fileName.endswith('.pdf'):
        continue
    pdf_path = f'{received_file_path}\{fileName}'
    #MERGE pdf
    with pdfplumber.open(pdf_path) as pdf:
        totalPages = len(pdf.pages)
        for k in range (0, totalPages):
            currentPage = pdf.pages[k]
            print(currentPage.height)
            if currentPage.height >= 792:
                continue
            else:
                merger_fugro.append(open(pdf_path, 'rb'), pages=(k, k+1))

merger_fugro.write(r"C:\Users\921722\OneDrive - Royal HaskoningDHV\20230928 Extraction\PSD\PSD_filtered.pdf")
merger_fugro.close()
# merger_AHAM.write(r"C:\Users\921722\Downloads\P2 All AHAM VBH merged 220826.pdf")
# merger_AHAM.close()

    

