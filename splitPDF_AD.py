import os
from PyPDF2 import PdfFileMerger
import pdfplumber
import xlwings as xw

received_file_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20221213 AD\merged'
file_mainDir = os.listdir(received_file_path)

XL_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20221213 AD\folder\index.csv'
WB = xw.Book(XL_path)
WS = WB.sheets["index"]

i_list = []
j_list = []
VBH_name_list = []
indexList_start = 2
indexList_end = 33

for a in range(indexList_start, indexList_end):
    i_list.append(int(WS.range(f"B{a}").value))
    j_list.append(int(WS.range(f"C{a}").value))
    VBH_name_list.append(str(WS.range(f"A{a}").value))


#index = 1
for index in range(0, indexList_end - indexList_start):
    merger = PdfFileMerger()
    i = i_list[index]
    j = j_list[index]
    VBH_name = VBH_name_list[index]
    for fileName in file_mainDir:
        if not fileName.endswith('.pdf'):
            continue
        pdf_path = f'{received_file_path}\{fileName}'
        #MERGE pdf
        with pdfplumber.open(pdf_path) as pdf:
            totalPages = len(pdf.pages)
            merger.append(open(pdf_path, 'rb'), pages=(i, j+1))


    merger.write(f"C:/Users/921722/OneDrive - Royal HaskoningDHV/20221213 AD/sorted/{VBH_name}.pdf")
    merger.close()

        
    

