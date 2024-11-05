from openpyxl import Workbook, load_workbook
import re
import PyPDF2
import numpy as np
import pandas as pd
import os

#PURPOSE OF SCRIPT: INSERT DEPTH FROM TOP TO BOTTOM WITH 0.5 METERS INCREMENT FOR ALL VBHs
#OUTPUT: export_masterList

workbook = load_workbook(r"C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\Pier 2 Grout Information.xlsx", data_only=True)
sheet1 = workbook["Depth Calcs_Fugro"]
#sheet2 = workbook["Pier 3 Grout Information Test V3"]

VBHnameList = []
firstlayertopdepthList = []
lastlayertopdepthList = []

for i in range(2, 24):
    VBHname_cell = "A"+str(i)
    VBHnameList.append(sheet1[VBHname_cell].value)
for i in range(2, 24):
    depthtop_firstlayer_cell = "B"+str(i)
    firstlayertopdepthList.append(sheet1[depthtop_firstlayer_cell].value)
for i in range(2, 24):
    depthtop_lastlayer_cell = "C"+str(i)
    lastlayertopdepthList.append(sheet1[depthtop_lastlayer_cell].value)

export_VBHnameList = []
export_correctdepthList = []
export_separateddepthList = []
export_separatedVBHList = []

masterList = list(zip(VBHnameList, firstlayertopdepthList, lastlayertopdepthList))

for i in range(len(masterList)):
    depthList = np.arange(masterList[i][1], masterList[i][2], 0.5).tolist()
    export_correctdepthList.append(depthList)
    print(masterList[i][0], " ", depthList)

for i in range(len(export_correctdepthList)):
    for j in range(len(export_correctdepthList[i])):
        export_separateddepthList.append(export_correctdepthList[i][j])
        export_separatedVBHList.append(masterList[i][0])

print(export_separateddepthList)
print(export_separatedVBHList)

export_masterList = list(zip(export_separatedVBHList, export_separateddepthList))
dataframe = pd.DataFrame(export_masterList, columns=['Name', 'Depth'])
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)
dataframe.to_csv('csv\pier2fugrogroutcorrecteddepth.csv')

