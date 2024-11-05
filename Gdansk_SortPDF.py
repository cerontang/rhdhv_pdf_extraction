import os
from PyPDF2 import PdfFileMerger
import pdfplumber

received_file_path = r'C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\Atterberg\script'
file_mainDir = os.listdir(received_file_path)
print(file_mainDir)

merger_f1 = PdfFileMerger()
merger_f2 = PdfFileMerger()

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
            if currentPage.height == 842.04:
                merger_f1.append(open(pdf_path, 'rb'), pages=(k, k+1))
            else:
                merger_f2.append(open(pdf_path, 'rb'), pages=(k, k+1))

merger_f1.write(r"C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\Atterberg\script\format_1\T5 GI Atterberg_f1.pdf")
merger_f1.close()
merger_f2.write(r"C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\Atterberg\script\format_2\T5 GI Atterberg_f2.pdf")
merger_f2.close()
