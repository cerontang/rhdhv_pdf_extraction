import pdfplumber
import re
import os

#PROBLEM TO SOLVE: SECOND/THIRD PAGE FIRST SET OF DATA NOT WORKING

reportLocation = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\00 Received\220303 - Pier 2 VBH Data\Pier-2 - Final Logs'
reportList = os.listdir(reportLocation)
reportPath = 'pdf\VBH-1203-004.pdf'

master_sptList = []
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

        if k != 0:
            testPage = pdf.pages[k]
            boundingBox = (268, 220, 366, 650)
            target_pageLocation = testPage.crop(boundingBox, relative=False)
            # print(testPage.width, testPage.height)
            sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 5})
            # print(sptText)
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

            m = 0
            for dataSet in sptText:
                if m == 0:
                    m = m+1
                    continue
                if dataSet[0] == '30' and dataSet[1] == '37.5':
                    continue
                if not dataSet[0]:
                    continue
                master_sptList.append(dataSet)

        else:
            testPage = pdf.pages[k]
            boundingBox = (268, 0, 366, 841)
            target_pageLocation = testPage.within_bbox(boundingBox, relative=False)
            # print(testPage.width, testPage.height)
            sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 0})
            #print(sptText)

            for dataSet in sptText:
                if dataSet[0] == '30' and dataSet[1] == '37.5':
                    continue
                if not dataSet[0]:
                    continue
                master_sptList.append(dataSet)

print(depthList)




# print(len(master_sptList))
#
# for i in master_sptList:
#     print(i)





