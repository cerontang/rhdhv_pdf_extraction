import re
import PyPDF2
import numpy as np
import pandas as pd
import os

#PURPOSE OF SCRIPT: EXTRACT GROUT INFO INTO RAW CSV FORMAT, NEED TO MANUALLY OR USE OTHER SCRIPT TO FIX EXCEPTION CASES
#OUTPUT: masterList_outer (WITH FULL DEPTH STRING UNPROCESSED), masterList_outer2 (WITH TOP DEPTH EXTRACTED, BUT A BETTER METHOD CAN BE USED, REFER TO checkLoggedornot.py)

def groutinfoExtraction (rP, rN):
    text = ""
    with open(rP, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        totalPages = reader.numPages
        for pageNumber in range(totalPages):
            page = reader.getPage(pageNumber)
            text = text + page.extractText()

    textList = text.split()
    textList_index = list(enumerate(textList))

    for i in range(len(textList_index)):
        for j in range(len(textList_index[i])):
            if j != 1:
                continue
            if textList_index[i][j] == 'From' and textList_index[i + 2][j] == 'to':
                depthList_outer.append(
                    textList_index[i][j] + " " + textList_index[i + 1][j] + " " + textList_index[i + 2][j] + " " +
                    textList_index[i + 3][j])
                for k in range(10):
                    if textList_index[i + 3 + k][j] == 'grout':
                        if textList_index[i + 3 + k - 1][j] == 'of':
                            groutList_outer.append(textList_index[i + 3 + k - 2][j])
                        else:
                            groutList_outer.append(textList_index[i + 3 + k - 1][j])
                        rN = rN.replace('.pdf', '')
                        reportnameList_outer.append(rN)
                        break
                    if k==9 and textList_index[i + 3 + k][j] != 'grout' :
                        invaliddepthList_outer.append(textList_index[i][j] + " " + textList_index[i + 1][j] + " " + textList_index[i + 2][j] + " " + textList_index[i + 3][j])
                        depthList_outer.pop()
                        break

reportList = []
reportLocation = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\Pier 3'
reportList = os.listdir(reportLocation)
masterList_outer = []
groutList_outer = []
depthList_outer = []
invaliddepthList_outer = []
reportnameList_outer = []


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
    if SPTornot == 1:
        groutinfoExtraction(reportPath, i)


groutList_array = np.array(groutList_outer)
depthList_array = np.array(depthList_outer)
reportnameList_array = np.array(reportnameList_outer)

#print(invaliddepthList_outer)
#print(depthList_outer)

masterList_outer = zip(reportnameList_array, depthList_array, groutList_array)
dataframe = pd.DataFrame(list(masterList_outer), columns=['Name', 'Depth', 'Grout'])
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)

dataframe.to_csv('csv\groutinfo.csv')

depthTopList = []
groutList_value = []

for element in depthList_outer:
    depthTop = re.search(r"\d+.\d\dm\b", element)
    if depthTop != None:
        depthTop_no_units = re.sub(r"m", "", depthTop.group(0))
        depthTopList.append(depthTop_no_units)

depthTopList_array = np.array(depthTopList)

masterList_outer2 = zip(reportnameList_array, depthTopList_array, groutList_array)
dataframe2 = pd.DataFrame(list(masterList_outer2), columns=['Name', 'Depth', 'Grout'])
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe2)
dataframe2.to_csv('csv\pier3groutinfo.csv')





