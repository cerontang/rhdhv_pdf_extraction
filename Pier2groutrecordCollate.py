import os
import shutil
from PyPDF2 import PdfFileMerger

groutingRecords_received_path = r'C:\Users\921722\Box\BI3753 Team\62 - Received Trojan\220419 - Pier-2, 3 and 4 Grouting Record\Pier-2 Grouting Record'
groutingRecords_mainDir = os.listdir(groutingRecords_received_path)
print(groutingRecords_mainDir)

for fileName in groutingRecords_mainDir:

    #EXCEPTION CASES
    probe_paste_path = r'C:/Users/921722/Box/BI3753 Team/30 - Geotech/06-Grouting works/01 - Grouting Records/Pier 2/Pier 2  Individual Grouting Records Received 19-04-2022/' + fileName
    if os.path.exists(probe_paste_path):
        continue
    #EXCEPTION CASES

    probes_received_path = r'C:/Users/921722/Box/BI3753 Team/62 - Received Trojan/220419 - Pier-2, 3 and 4 Grouting Record/Pier-2 Grouting Record/' + fileName
    probe_paste_path = r'C:/Users/921722/Box/BI3753 Team/30 - Geotech/06-Grouting works/01 - Grouting Records/Pier 2/Pier 2  Individual Grouting Records Received 19-04-2022/' + fileName

    shutil.copytree(probes_received_path, probe_paste_path)
    movedfileList = []


    for probe_fileName in os.listdir(probe_paste_path):
        #print(probe_fileName)
        source = probe_paste_path + '/' + probe_fileName
        destination = probe_paste_path
        #print(os.listdir(source))
        for pdfFile in os.listdir(source):
            pdf_path = source + '/' + pdfFile
            if os.path.isfile(pdf_path):
                shutil.move(pdf_path, destination)
                movedfileList.append(pdfFile)
                #print('moved', pdfFile)

    print(fileName, 'Total file moved:', len(movedfileList))