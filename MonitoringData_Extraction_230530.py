import cv2
import pdfplumber
import os
import pandas as pd
from datetime import datetime
import time
import xlwings as xw

now = datetime.now()
date_time = now.strftime("%m-%d-%Y")

VBH_folder_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20230928 Extraction\PSD'
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
            name = str(VBH_file.replace(".pdf", ""))
            if k == 0:
                continue
            check_boundingBox = (56.0, 113.6, 125.6, 141.6)
            check_target_pageLocation = textPage.crop(check_boundingBox, relative=False)
            switch = check_target_pageLocation.extract_text()
            if "point" not in switch.lower():
                pass
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
                print(boundingBox)
                boundingbox_list.append(boundingBox)
            else:
                boundingBox = boundingbox_list[0]
            ##############################################################
            #boundingBox = (56.800000000000004, 142.4, 786.4, 529.6)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            im_debug = target_pageLocation.to_image(resolution=150)
            im_debug.debug_tablefinder({"vertical_strategy": "text", "horizontal_strategy": "text", "intersection_tolerance": 10, "snap_y_tolerance": 7, "snap_x_tolerance": 7, "keep_blank_chars": True})
            im_debug.save(f"img_select/debug/{name}_debug.png", format="PNG")


            extractedText = target_pageLocation.extract_table(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "intersection_tolerance": 10, "snap_y_tolerance": 7, "snap_x_tolerance": 7, "keep_blank_chars": True})

            print(extractedText)
            if extractedText is None:
                continue
            #CUSTOMISATION BLOCK
            for data in extractedText:
                if all(element == '' for element in data):
                    continue
                data.insert(0, name)
                print(data)
                data_list.append(data)
#


df = pd.DataFrame(data_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
df.to_csv(f'csv/MTB Manhole Monitoring Data_230719.csv')

print(df)