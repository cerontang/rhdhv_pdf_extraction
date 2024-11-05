from openpyxl import Workbook, load_workbook
import re
import PyPDF2
import numpy as np
import pandas as pd
import os

#PURPOSE OF SCRIPT: DISTINGUISH IF GROUT WAS NOT LOGGED OR WAS LOGGED TOGETHER WITH OTHER DEPTHS (TYPICALLY ABOVE)
#OUTPUT: master_loggedList, master_notloggedList, value_masterdepthList

workbook = load_workbook(r"C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\Pier 3 Grout Information.xlsx", data_only=True)
sheet1 = workbook["Pier 3 Grout Information V3"]
sheet2 = workbook["Raw CSV full depth"]

depth_NogroutinfoList = []
VBH_NogroutinfoList = []

for i in range(2, 2266):
    depthtop_cell = "L"+str(i)
    if sheet1[depthtop_cell].value == "#N/A":
        depth_NogroutinfoList.append(sheet1["B"+str(i)].value)
        VBH_NogroutinfoList.append(sheet1["A"+str(i)].value)

master_NogroutinfoList = list(zip(VBH_NogroutinfoList, depth_NogroutinfoList))

# print(depth_NogroutinfoList)
# print(VBH_NogroutinfoList)
print(master_NogroutinfoList)

######################################################################################################################################################################

fullVBHList = []
fulldepthList = []

for i in range(2, 1710):
    fulldepthtop_cell = sheet2["C"+str(i)].value
    VBH_cell = sheet2["B"+str(i)].value
    fulldepthList.append(fulldepthtop_cell)
    fullVBHList.append(VBH_cell)

master_fulldepthList = list(zip(fullVBHList, fulldepthList))
#print(master_fulldepthList)

split_top_depthList = []
split_bottom_depthList = []

for i in range(len(master_fulldepthList)):
    split_top_depthList.append(master_fulldepthList[i][1].split()[1])
    split_bottom_depthList.append(master_fulldepthList[i][1].split()[3])

value_top_depthList = []
value_bottom_depthList = []

for i in split_top_depthList:
    value_topDepth = i
    value_topDepth = float(value_topDepth.replace("m", ""))
    value_top_depthList.append(value_topDepth)

for i in split_bottom_depthList:
    value_bottomDepth = i
    value_bottomDepth = float(value_bottomDepth.replace("m", ""))
    value_bottom_depthList.append(value_bottomDepth)

# print(value_top_depthList)
# print(value_bottom_depthList)

value_masterdepthList = list(zip(fullVBHList, value_top_depthList, value_bottom_depthList))

#for i in value_masterdepthList:
    #print(i)

# for i in master_NogroutinfoList:
#     print(i)

yesCount = 0
noCount = 0
depth_loggedList = []
VBH_loggedList = []
depth_notloggedList = []
VBH_notloggedList = []

for i in range(len(master_NogroutinfoList)):
    for j in range(len(value_masterdepthList)):
        if master_NogroutinfoList[i][0] == value_masterdepthList[j][0] and master_NogroutinfoList[i][1] > value_masterdepthList[j][1]:
            if master_NogroutinfoList[i][1] < value_masterdepthList[j][2]:
                print(master_NogroutinfoList[i][0], "at depth", master_NogroutinfoList[i][1], "- Is grout logged? YES")
                yesCount = yesCount + 1
                depth_loggedList.append(master_NogroutinfoList[i][1])
                VBH_loggedList.append(master_NogroutinfoList[i][0])
                break
    if j == len(value_masterdepthList)-1:
        if i == len(master_NogroutinfoList)-1 or i == len(master_NogroutinfoList)-2:
            continue
        print(master_NogroutinfoList[i][0], "at depth", master_NogroutinfoList[i][1], "- Is grout logged? NO")
        noCount = noCount + 1
        depth_notloggedList.append(master_NogroutinfoList[i][1])
        VBH_notloggedList.append(master_NogroutinfoList[i][0])


print("YES:", yesCount)
print("NO:", noCount)
result = "OK"
if yesCount+noCount != len(master_NogroutinfoList):
    result = "Not OK, PLEASE CHECK"
print("Total input cases:", len(master_NogroutinfoList), "->", result)

master_loggedList = list(zip(VBH_loggedList, depth_loggedList))
master_notloggedList = list(zip(VBH_notloggedList, depth_notloggedList))

def dataframeEngine (list):
    dataframe = pd.DataFrame(list)
    pd.set_option('display.max_rows', 5000)
    pd.set_option('display.max_columns', 5000)
    pd.set_option('display.width', 10000)
    print(dataframe)
    dataframe.to_csv('csv\LoggedList.csv')

# print(master_loggedList)
# print(master_notloggedList)
# print(value_masterdepthList)
# dataframeEngine(master_loggedList)
print(master_NogroutinfoList)
print(value_masterdepthList)






