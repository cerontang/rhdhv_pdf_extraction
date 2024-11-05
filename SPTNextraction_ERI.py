import cv2
import pdfplumber
import os
import pandas as pd
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m-%d-%Y")

VBH_folder_path = r'C:\Users\921722\Box\PC1063 DCT Gdansk\PC3742-104-T3 dredging Claim C04\09 Claim C04\CTR GI\script\test'
VBH_list = os.listdir(VBH_folder_path)
sameFormat = 'N'
master_boundingbox_list = []
description_list = []
depth_t_list = []
depth_b_list = []
VBH_name_list = []
type_list = []
SPT_N_list = []
master_depth_list = []

for VBH_file in VBH_list:
    local_depth_list = []
    depth = 0
    if not VBH_file.endswith('.pdf'):
        continue
    VBH_file_path = f'{VBH_folder_path}\{VBH_file}'
    #print(VBH_file_path)

    with pdfplumber.open(VBH_file_path) as pdf:
        #############################
        totalPages = len(pdf.pages)
        #print(totalPages)
        local_description_list = []
        for k in range(totalPages):
            textPage = pdf.pages[k]
            # Extraction of Description to get Grout Info
            if len(master_boundingbox_list) > 1:
                if sameFormat == "Y" and k == 0:
                    boundingBox = master_boundingbox_list[0]
                else:
                    boundingBox = master_boundingbox_list[1]


            if sameFormat == "N" and k == 0:
                print("Same format? (Y/N)")
                sameFormat = str(input())
                textPage_next = pdf.pages[k + 1]
                #Select Bounding Box
                #Coordinates of first page bounding box
                boundingBox = (0, 0, textPage.width, textPage.height)
                #print(boundingBox)
                target_pageLocation = textPage.crop(boundingBox, relative=False)
                select_img = target_pageLocation.to_image(resolution=150)
                select_img.save(f"img_select/{VBH_file}{k}.png", format="PNG")
                im = cv2.imread(f"img_select/{VBH_file}{k}.png")
                imResize = cv2.resize(im, (round(textPage.width*1.25), round(textPage.height*1.25)))
                fromCenter = False
                r = cv2.selectROI(imResize, fromCenter)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                #boundingBox = (131.75, 210, 267.46, 719)
                boundingBox = (r[0]*0.8, r[1]*0.8, r[0]*0.8+ r[2]*0.8, r[1]*0.8 + r[3]*0.8)
                master_boundingbox_list.append(boundingBox)
                #Coordinates of subsequent pages bounding box
                boundingBox_next = (0, 0, textPage_next.width, textPage_next.height)
                target_pageLocation = textPage_next.crop(boundingBox_next, relative=False)
                select_img = target_pageLocation.to_image(resolution=150)
                select_img.save(f"img_select/{VBH_file}{k+1}.png", format="PNG")
                im = cv2.imread(f"img_select/{VBH_file}{k+1}.png")
                imResize = cv2.resize(im, (round(textPage.width * 1.25), round(textPage.height * 1.25)))
                fromCenter = False
                r = cv2.selectROI(imResize, fromCenter)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                boundingBox_next = (r[0] * 0.8, r[1] * 0.8, r[0] * 0.8 + r[2] * 0.8, r[1] * 0.8 + r[3] * 0.8)
                master_boundingbox_list.append(boundingBox_next)
                #########################
            elif k != 0:
                boundingBox = master_boundingbox_list[1]

            target_pageLocation = textPage.crop(boundingBox, relative=False)
            extractedText = target_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "text", "intersection_tolerance": 5, "snap_y_tolerance": 7})

            #CUSTOMISATION BLOCK
            # create a nicer raw description list
            if extractedText is None:
                continue
            #print(extractedText)
            description_raw_list = []
            for text in extractedText:
                text[0] = text[0].replace("\n", " ").strip()
                description_raw = text[0].split(". ")
                for description_0 in description_raw:
                    if description_0 == "SPT-N":
                        continue
                    if description_0 == "" or description_0 is None:
                        continue
                    description_raw_list.append(description_0)
                    #print(description)
            #generate lists for dataframe
            print(description_raw_list)
            for description in description_raw_list:
                VBH_name_list.append(VBH_file.replace(".pdf", ""))
                if description == "R":
                    SPT_N_list.append(50)
                else:
                    SPT_N_list.append(description)
                local_depth_list.append(depth)
                depth += 0.5
                #print(description)
    for d in local_depth_list:
        master_depth_list.append(d)


            ###################################################
output_list = list(zip(VBH_name_list, master_depth_list, SPT_N_list))
dataframe = pd.DataFrame(output_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)

dataframe.to_csv(f'csv/ERI_SPTN_{date_time}.csv')