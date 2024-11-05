import pdfplumber
import re
import os
import pandas as pd

reportPath = 'pdf\APMHH_BHlogs_fugro.pdf'

master_List = []
bh_List = []
with pdfplumber.open(reportPath) as pdf:
    totalPages = len(pdf.pages)
    for k in range(totalPages):
        testPage = pdf.pages[k]
        boundingBox = (169, 170, 356, 753)
        target_pageLocation = testPage.crop(boundingBox, relative=False)
        #print(testPage.width, testPage.height)
        sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 5})
        sptText.pop(0)
        sptText[0][0] = sptText[0][0].replace('\n', " ")
        #print(sptText[0][0])
        #print("####################################")
        master_List.append(sptText[0][0])

        boundingBox2 = (421, 24.96, 569.7, 72.23)
        target_pageLocation2 = testPage.crop(boundingBox2, relative=False)
        bhName = target_pageLocation2.extract_table(table_settings={"snap_y_tolerance": 5})
        bhName[0].pop(0)
        bhName[0][0] = bhName[0][0].replace('\n', "")
        bh_List.append(bhName[0][0])

mergedList = list(zip(bh_List, master_List))

master_lineList = []
line_stringList = []
line_vbhList = []

for text in mergedList:
    split_string = text[1].split()
    #print(split_string)
    line_indexList = []

    for i in range(len(split_string)):
        if split_string[i] == 'at':
            line_indexList.append(i)
            continue
        if split_string[i] == 'm' and split_string[i + 3] == 'm':
            if split_string[i-2] == 'from' or split_string[i-2] == 'From':
                line_indexList.append(i-2)
                continue
            line_indexList.append(i-1)
            continue
    line_indexList.append(len(split_string))
    #print(line_indexList)
    for j in range(len(line_indexList)):
        lineString = ""
        if j == len(line_indexList)-1:
            break
        for k in range(line_indexList[j], line_indexList[j+1]):
            lineString = lineString + split_string[k] + " "

        lineString = lineString.replace("- ", "")
        lineString = lineString.strip()
        vbhString = text[0].replace("Borehole:", "")
        vbhString = vbhString.replace("(Stratigraphy)", "")
        vbhString = vbhString.strip()

        line_stringList.append(lineString)
        line_vbhList.append(vbhString)
        #print(vbhString, lineString)
master_lineList = list(zip(line_vbhList, line_stringList))

depthtopList = []
depthbottomList = []
descriptionList = []

for textDescription in master_lineList:

    splitDescription_list = textDescription[1].split()
    for i in range(len(splitDescription_list)):
        descriptionString = ""
        if splitDescription_list[i] == "at":
            depthtopList.append(splitDescription_list[i + 1])
            depthbottomList.append(None)
            for j in range(i+3, len(splitDescription_list)):
                descriptionString = descriptionString + splitDescription_list[j] + " "
            #print(descriptionString.strip())
            descriptionList.append(descriptionString.strip())
            break
        if splitDescription_list[i] == "m" and splitDescription_list[i+3] == "m":
            depthtopList.append(splitDescription_list[i-1])
            depthbottomList.append(splitDescription_list[i+2])
            for j in range(i+4, len(splitDescription_list)):
                descriptionString = descriptionString + splitDescription_list[j] + " "
            #print(descriptionString.strip())
            descriptionList.append(descriptionString.strip())
            break

outputList = list(zip(line_vbhList, depthtopList, depthbottomList, descriptionList))

for output in outputList:
    print(output)





dataframe = pd.DataFrame(outputList)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)

#dataframe.to_csv('csv\APMHH_GI_Description.csv')

