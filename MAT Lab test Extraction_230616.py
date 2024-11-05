import cv2
import pdfplumber
import os
import pandas as pd
from datetime import datetime
import time
import xlwings as xw

now = datetime.now()
date_time = now.strftime("%m-%d-%Y")

VBH_folder_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20230615 GI Lab Extraction\MAT\extract'
VBH_list = os.listdir(VBH_folder_path)
VBH_name_list = []
content_list = []
data_list = []
boundingbox_list = []

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
#####SAMPLE INFO
            name_boundingBox = (96.0, 80.0, 263.2, 119.2)
            name_target_pageLocation = textPage.crop(name_boundingBox, relative=False)
            name = name_target_pageLocation.extract_tables(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 10, "snap_y_tolerance": 7, "snap_x_tolerance": 7, "keep_blank_chars": False})
            Borehole_ID = name[0][0][0]
            Sample_ID = name[0][1][0]
            Sample_Depth = name[0][2][0]
###################################################
            if len(boundingbox_list) == 0:
                boundingBox = (0, 0, textPage.width, textPage.height)
                # print(boundingBox)
                target_pageLocation = textPage.crop(boundingBox, relative=False)
                select_img = target_pageLocation.to_image(resolution=150)
                select_img.save(f"img_select/{VBH_file}{k}.png", format="PNG")
                im = cv2.imread(f"img_select/{VBH_file}{k}.png")
                imResize = cv2.resize(im, (round(textPage.width * 1.25), round(textPage.height * 1.25)))
                fromCenter = False
                r = cv2.selectROI(imResize, fromCenter)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                # boundingBox = (131.75, 210, 267.46, 719)
                boundingBox = (r[0] * 0.8, r[1] * 0.8, r[0] * 0.8 + r[2] * 0.8, r[1] * 0.8 + r[3] * 0.8)
                boundingbox_list.append(boundingBox)
                print(boundingBox)
            else:
                boundingBox = boundingbox_list[0]
            ##############################################################
            #boundingBox = (56.800000000000004, 142.4, 786.4, 529.6)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            im_debug = target_pageLocation.to_image(resolution=150)
            im_debug.debug_tablefinder({"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 10, "snap_y_tolerance": 7, "snap_x_tolerance": 7, "keep_blank_chars": False})
            im_debug.save(f"img_select/debug/{name}_debug.png", format="PNG")


            extractedText = target_pageLocation.extract_text(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "intersection_tolerance": 10, "snap_y_tolerance": 7, "snap_x_tolerance": 7, "keep_blank_chars": False})

            #print(extractedText.split())

            if extractedText is None:
                continue
            #CUSTOMISATION BLOCK
            text_list = extractedText.split()
            text_list.insert(0, Sample_Depth)
            text_list.insert(0, Sample_ID)
            text_list.insert(0, Borehole_ID)
            print(text_list)
            data_list.append(text_list)

#


df = pd.DataFrame(data_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
df.to_csv(f'C:/Users/921722/OneDrive - Royal HaskoningDHV/20230615 GI Lab Extraction/MAT/MAT PSD_Percentage Soil Type.csv')
print(df)