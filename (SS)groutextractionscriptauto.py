import re
import PyPDF2
import numpy as np
import pandas as pd
import os

def infoExtraction (rP, rN):
    text = ""
    with open(rP, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        totalPages = reader.numPages
        for pageNumber in range(totalPages):
            page = reader.getPage(pageNumber)
            text = text + page.extractText()

    textList = text.split()
    textList_index = list(enumerate(textList))

    depthList = []
    groutList = []
    reportnameList = []

    for i in range(len(textList_index)):
        for j in range(len(textList_index[i])):
            if j != 1:
                continue
            if textList_index[i][j] == 'From' and textList_index[i + 2][j] == 'to':
                depthList.append(
                    textList_index[i][j] + " " + textList_index[i + 1][j] + " " + textList_index[i + 2][j] + " " +
                    textList_index[i + 3][j])
            if textList_index[i][j] == 'grout':
                if textList_index[i - 1][j] == 'of':
                    groutList.append(textList_index[i - 2][j])
                else:
                    groutList.append(textList_index[i - 1][j])
                rN = rN.replace('.pdf', '')
                reportnameList.append(rN)

    groutList_array = np.array(groutList)
    depthList_array = np.array(depthList)
    reportnameList_array = np.array(reportnameList)

    masterList = zip(reportnameList_array, depthList_array, groutList_array)
    dataframe = pd.DataFrame(list(masterList), columns=['Name', 'Depth', 'Grout'])

    print(dataframe)


reportList = []
reportLocation = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\Pier 3'
reportList = os.listdir(reportLocation)


for i in reportList:
    SPTornot = 1
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
                SPTornot = SPTornot - 1
    if SPTornot == 1:
        infoExtraction(reportPath, i)