import re
import PyPDF2
import numpy as np
import pandas as pd
import os

reportLocation = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\Pier 3'
reportList = os.listdir(reportLocation)

print(len(reportList))



for i in reportList:
    SPTornot = 1
    x = 0
    reportPath = reportLocation+'\\'+i
    with open(reportPath, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        page = reader.getPage(0)
        text = page.extractText()
        textList = text.split()
        for j in textList:
            if j == 'SPT1':
                break
            else:
                x = x + 1
            if x == len(textList)-1:
                SPTornot = 0
                break

    print(i, " ", SPTornot)
    print(textList)

