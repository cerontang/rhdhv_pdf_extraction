import os
import shutil
from PyPDF2 import PdfFileMerger

groutingRecords_received_path = r'C:/Users/921722/Box/BI3753 Team/30 - Geotech/06-Grouting works/01 - Grouting Records/Pier 2/Pier 2  Individual Grouting Records Received 19-04-2022/'
groutingRecords_mainDir = os.listdir(groutingRecords_received_path)
print(groutingRecords_mainDir)

for fileName in groutingRecords_mainDir:
    separated_pdf_dir = r'C:/Users/921722/Box/BI3753 Team/30 - Geotech/06-Grouting works/01 - Grouting Records/Pier 2/Pier 2  Individual Grouting Records Received 19-04-2022/' + fileName
    separated_pdf_list = os.listdir(separated_pdf_dir)
    # CREATE file name
    fileName_split = fileName.split()
    # print(fileName_split)
    fileName_noNum = ''
    for i in range(len(fileName_split)):
        if i == 0:
            continue
        fileName_noNum += fileName_split[i] + " "
    fileName_noNum_trimmed = fileName_noNum.strip()
    #MERGE pdf
    merger = PdfFileMerger()
    for pdf in separated_pdf_list:
        if not pdf.endswith('.pdf'):
            continue
        separated_pdf_path = separated_pdf_dir + '/' + pdf
        merger.append(separated_pdf_path)

    merger.write(f"Pier 2 Individual Grouting Records - Received 19_04_2022/{fileName_noNum_trimmed}.pdf")
    merger.close()
