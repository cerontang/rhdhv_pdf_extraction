import re
import pdfplumber
import numpy as np
import pandas as pd
import xlwings as xw
import os

depth_top_list = []
depth_bottom_list = []
master_description_list = []
master_VBH_list = []


source_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\Pier 2 Grout Information.xlsx'
WB = xw.Book(source_path)
WS = WB.sheets['Pier2_Fugro_List']
VBH_Fugro_list = []
for i in range(2, 33):
    VBH_Fugro_list.append(WS.range(f'A{i}').value)
reportList = VBH_Fugro_list
reportLocation = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\Pier 2'

for i in reportList:
    VBH_file_path = reportLocation + f'\{i}.pdf'
    with pdfplumber.open(VBH_file_path) as pdf:
        totalPages = len(pdf.pages)
        local_description_string = ''
        for k in range(totalPages):
            textPage = pdf.pages[k]
            # Extraction of Description to get Grout Info
            boundingBox = (117.55, 154.39, 277.91, 749.42)
            #boundingBox = (0, 0, 595.21, 842)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            fullDescription = target_pageLocation.extract_text() #(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 20})
            #VISUAL DEBUG TOOL
            # im = target_pageLocation.to_image(resolution = 150)
            # im.save(f"img_fugro/{i}{k}.png", format="PNG")
            local_description_string = local_description_string + fullDescription + " "

    description_string_list_0 = local_description_string.strip().split()
    description_string_list = []
    #print(description_string_list)
    #print(i, description_string_list)
    #description_string_list.remove("R")
    for j in range(len(description_string_list_0)):
        if description_string_list_0[j] == 'R' or description_string_list_0[j] == 'D':
            continue
        description_string_list.append(description_string_list_0[j])

    #EXTRACTION OF PRIMARY DESCRIPTION
    for j in range(len(description_string_list)):
        if description_string_list[j] == '-':
            individual_description = ''
            depth_top_list.append(description_string_list[j-1].replace('m', ''))
            depth_bottom_list.append(description_string_list[j+1].replace('m', ''))
            for m in range(1, len(description_string_list)-j):
                if description_string_list[j+m] == '...':
                    for n in range(j+3, j+m):
                        individual_description += description_string_list[n] + ' '
                    break
                if description_string_list[j+m] == '-':
                    for n in range(j+3, j+m-2):
                        individual_description += description_string_list[n] + ' '
                    break
                if description_string_list[j + m] == 'Terminated':
                    for n in range(j+3, j+m):
                        individual_description += description_string_list[n] + ' '
                    break
            master_VBH_list.append(i)
            master_description_list.append(individual_description.strip())
            continue
        ######################################################################################################################
        # EXTRACTION OF SECONDARY DESCRIPTION
        if description_string_list[j] == '...':
            if description_string_list[j+1] == 'From':
                individual_description_secondary = ''
                depth_top_list.append(description_string_list[j + 2].replace('m', ''))
                depth_bottom_list.append(description_string_list[j + 4].replace('m', ''))
                for m in range(1, len(description_string_list) - j):
                    if description_string_list[j + m] == '...':
                        for n in range(j + 6, j + m):
                            individual_description_secondary += description_string_list[n] + ' '
                        break
                    if description_string_list[j + m] == '-':
                        for n in range(j + 6, j + m - 1):
                            individual_description_secondary += description_string_list[n] + ' '
                        break
                    if description_string_list[j + m] == 'Terminated':
                        for n in range(j + 3, j + m):
                            individual_description_secondary += description_string_list[n] + ' '
                        break
                master_VBH_list.append(i)
                master_description_list.append(individual_description_secondary.strip())
                continue
            if description_string_list[j+1] == 'At':
                individual_description_secondary = ''
                depth_top_list.append(description_string_list[j + 2].replace('m', ''))
                depth_bottom_list.append(" ")
                for m in range(1, len(description_string_list) - j):
                    if description_string_list[j + m] == '...':
                        for n in range(j + 4, j + m):
                            individual_description_secondary += description_string_list[n] + ' '
                        break
                master_VBH_list.append(i)
                master_description_list.append(individual_description_secondary.strip())
                continue

outputList = list(zip(master_VBH_list, depth_top_list, depth_bottom_list, master_description_list))

dataframe = pd.DataFrame(outputList)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)
dataframe.to_csv('csv\Pier2_GI_Description_Fugro.csv')

print(len(master_VBH_list), len(depth_top_list), len(depth_bottom_list), len(master_description_list))