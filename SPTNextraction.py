import pdfplumber
import re
import os
import pandas as pd
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m-%d-%Y")

reportLocation = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20221017 AD\AHAM logs'
reportList = os.listdir(reportLocation)
manualCheckList = []
outer_sptList = []

for reportName in reportList:
    reportPath = reportLocation+'\\'+reportName
    master_sptList = []
    depthList = []
    with pdfplumber.open(reportPath) as pdf:
        totalPages = len(pdf.pages)
        for k in range(totalPages):
            if k != 0:
                testPage = pdf.pages[k]
                boundingBox = (268, 220, 366, 650)
                target_pageLocation = testPage.crop(boundingBox, relative=False)
                #print(testPage.width, testPage.height)
                sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 5})
                # print(sptText)
                if sptText == None:
                    #manualCheckList.append(reportName)
                    continue
                newpagefirstdataSet = list(sptText[0])
                newpagefirstdataSet_fixed = []
                for i in newpagefirstdataSet:
                    if not i:
                        continue
                    newpagefirstdataSet_fixed.append(i)
                master_sptList.append(newpagefirstdataSet_fixed)

                testPage = pdf.pages[k]
                boundingBox = (268, 0, 366, 841)
                target_pageLocation = testPage.within_bbox(boundingBox, relative=False)
                sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 0})
                if sptText == None:
                    #manualCheckList.append(reportName)
                    continue
                for dataSet in sptText:
                    if dataSet == sptText[0]:
                        continue
                    if dataSet[0] == '30' and dataSet[1] == '37.5':
                        continue
                    if not dataSet[0]:
                        continue
                    if not dataSet:
                        continue
                    master_sptList.append(dataSet)
            else:
                testPage = pdf.pages[k]
                boundingBox = (268, 0, 366, 841)
                target_pageLocation = testPage.within_bbox(boundingBox, relative=False)
                #print(testPage.width, testPage.height)
                sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 0})
                #print(sptText)
                if sptText == None:
                    manualCheckList.append(reportName)
                    continue
                for dataSet in sptText:
                    if dataSet[0] == '30' and dataSet[1] == '37.5':
                        continue
                    if not dataSet[0]:
                        continue
                    if dataSet[0] == 'SPT1':
                        break
                    master_sptList.append(dataSet)



    if not master_sptList:
        manualCheckList.append(reportName)
        continue
    for n in master_sptList:
        if not n:
            master_sptList.remove(n)

    if len(master_sptList) % 2 != 0:
        manualCheckList.append(reportName)
        continue
    master_sptList_merged = []

    #START HERE !!!!!

    if reportName == "VBH-1104-001.pdf":
        continue
    depthList = []
    with pdfplumber.open(reportPath) as pdf:
        totalPages = len(pdf.pages)
        for k in range(totalPages):
            testPage = pdf.pages[k]
            depth_boundingBox = (360, 205, 390, 700)
            depth_pageLocation = testPage.crop(depth_boundingBox, relative=False)
            depthText = depth_pageLocation.extract_table(table_settings={"snap_y_tolerance": 5})
            depths = depthText[1][0].split()
            for depth in depths:
                depthList.append(depth)

    print(reportName, "No. of SPT records:", len(master_sptList)/2, master_sptList)
    print(reportName, "No. of depth records:", len(depthList), depthList)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for spt_values in master_sptList:
        if len(spt_values) < 4:
            continue
        if spt_values[3] is None:
            continue
        spt_values[3] = spt_values[3].replace(">", "")
        spt_values[3] = spt_values[3].replace("a\n", "")
        outer_sptList.append(spt_values[3])

print("PLEASE MANUALLY CHECK: ", manualCheckList)
print(outer_sptList)
dataframe = pd.DataFrame(outer_sptList)
dataframe.to_csv(f'csv\ERI_SPTN_{date_time}.csv')





