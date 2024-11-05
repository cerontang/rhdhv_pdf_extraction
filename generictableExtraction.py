import pdfplumber
import re
import os
import pandas as pd

reportPath = r'pdf\Fugro 2021 Land and Marine BH logs.pdf'

outputList_SPT = []
BHnameList = []

# with pdfplumber.open(reportPath) as pdf:
#     totalPages = len(pdf.pages)
#     for k in range(totalPages):
#         testPage = pdf.pages[k]
#         boundingBox = (470, 178, 490, 753)
#         target_pageLocation = testPage.crop(boundingBox, relative=False)
#         #print(testPage.width, testPage.height)
#         sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 5})
#         #print(sptText)
#
#         for text in sptText:
#             if text[0] == 'No.':
#                 continue
#             sampInfo_list = text[0].split()
#             for i in range(len(sampInfo_list)):
#                 if i == 0:
#                     continue
#                 if i == len(sampInfo_list):
#                     break
#                 if sampInfo_list[i] == sampInfo_list[i-1]:
#                     sampInfo_list.remove(sampInfo_list[i])
#             #print(sampInfo_list)
#             for value in sampInfo_list:
#                 outputList.append(value)

###########################################################################################################
with pdfplumber.open(reportPath) as pdf:
    totalPages = len(pdf.pages)
    for k in range(totalPages):
        testPage = pdf.pages[k]
        #print(testPage.width, testPage.height)
        boundingBox = (45, 198, 310, 542)
        target_pageLocation = testPage.crop(boundingBox, relative=False)
        #print(testPage.width, testPage.height)
        sptText = target_pageLocation.extract_table(table_settings={"snap_y_tolerance": 5, "vertical_strategy": "text", "horizontal_strategy": "text"})
        #print(sptText)
        for textRow in sptText:
            if textRow[0] is None or textRow[0] == '':
                continue
            textRow[0] = textRow[0].replace(" -","")
            textRow[1] = textRow[1].replace("- ", "")
            if textRow[1] == '-':
                del textRow[1]
            #print(textRow)
            BHname_boundingBox = (90.05, 120.26, 120, 131.34)
            BHname_pageLocation = testPage.crop(BHname_boundingBox, relative=False)
            BHname = BHname_pageLocation.extract_text()
            textRow.insert(0, BHname.strip())
            outputList_SPT.append(textRow)
            print(textRow)
        im = target_pageLocation.to_image(resolution=150)
        im.debug_tablefinder(
            {"vertical_strategy": "text", "horizontal_strategy": "text", "intersection_tolerance": 20})
        im.save(f"img_test/{BHname}-{k}.png", format="PNG")

df = pd.DataFrame(outputList_SPT)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
df.columns = ['BH_name', 'Depth_t', 'Depth_b', 'Samp type', 'N1', 'N2', 'N3', 'SPT N', 'Nc']
print(df)
df.to_csv(r'csv\Fugro Marine and Land BH logs.csv')