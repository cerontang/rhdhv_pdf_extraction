import re
import pdfplumber
import numpy as np
import pandas as pd
import xlwings as xw
import os
from datetime import date
import cv2

reportPath = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20220520 Python Presentation\20220912\VBH logs\Fugro'
reportList = os.listdir(reportPath)

depth_top_list = []
depth_bottom_list = []
master_description_list = []
master_VBH_list = []
master_boundingbox_list = []
description_type_list = []
sameFormat = 'N'

for i in reportList:
    VBH_file_path = reportPath + f'\{i}'
    print(VBH_file_path)
    if not VBH_file_path.endswith('.pdf'):
        continue
    with pdfplumber.open(VBH_file_path) as pdf:
        totalPages = len(pdf.pages)
        local_description_string = ''
        for k in range(totalPages):
            textPage = pdf.pages[k]
            # Extraction of Description to get Grout Info
            boundingBox = (117.55, 154.39, 277.91, 749.42)

            if sameFormat == 'N':
                #Select Bounding Box
                print("Same format? (Y/N)")
                sameFormat = str(input())
                boundingBox = (0, 0, textPage.width, textPage.height)
                #print(boundingBox)
                target_pageLocation = textPage.crop(boundingBox, relative=False)
                select_img = target_pageLocation.to_image(resolution=150)
                select_img.save(f"img_select/{i}{k}.png", format="PNG")
                im = cv2.imread(f"img_select/{i}{k}.png")
                imResize = cv2.resize(im, (round(textPage.width*1.25), round(textPage.height*1.25)))
                fromCenter = False
                r = cv2.selectROI(imResize, fromCenter)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                #boundingBox = (131.75, 210, 267.46, 719)
                boundingBox = (r[0]*0.8, r[1]*0.8, r[0]*0.8+ r[2]*0.8, r[1]*0.8 + r[3]*0.8)
                master_boundingbox_list.append(boundingBox)
                #print(boundingBox)
                #########################
            else:
                boundingBox = master_boundingbox_list[0]

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
                    for n in range(j+3, j+m-1):
                        individual_description += description_string_list[n] + ' '
                    break
                if description_string_list[j + m] == 'Terminated':
                    for n in range(j+3, j+m):
                        individual_description += description_string_list[n] + ' '
                    break
            master_VBH_list.append(i.replace(".pdf", ""))
            master_description_list.append(individual_description.strip())
            description_type_list.append("Main")
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
                master_VBH_list.append(i.replace(".pdf", ""))
                master_description_list.append(individual_description_secondary.strip())
                description_type_list.append("Secondary")
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
                master_VBH_list.append(i.replace(".pdf", ""))
                master_description_list.append(individual_description_secondary.strip())
                description_type_list.append("Secondary")
                continue

outputList = list(zip(master_VBH_list, depth_top_list, depth_bottom_list, master_description_list, description_type_list))

dataframe = pd.DataFrame(outputList)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)
#dataframe.to_csv(f'csv\{date.today()}_VBH_GI_Description_Fugro.csv')

print(len(master_VBH_list), len(depth_top_list), len(depth_bottom_list), len(master_description_list))