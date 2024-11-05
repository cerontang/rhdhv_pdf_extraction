import cv2
import pdfplumber
import os
import pandas as pd
from datetime import datetime
import time
import xlwings as xw

now = datetime.now()
date_time = now.strftime("%m-%d-%Y")

VBH_folder_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20230525 AD\test'
VBH_list = os.listdir(VBH_folder_path)
VBH_name_list = []
content_list = []
data_list = []

source_path = r"C:\Users\921722\OneDrive - Royal HaskoningDHV\20230525 AD\test\results\Baku_BH Logs_outputs.xlsx"
WB = xw.Book(source_path)
WS = WB.sheets['name_list']

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
            name = WS.range(f'A{k + 1}').value
            print(name)
            #Select Bounding Box
            #Coordinates of first page bounding box
            boundingBox = (0, 0, textPage.width, textPage.height)
            #print(boundingBox)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            select_img = target_pageLocation.to_image(resolution=150)
            select_img.save(f"img_select/{name}.png", format="PNG")
            im = cv2.imread(f"img_select/{name}.png")
            imResize = cv2.resize(im, (round(textPage.width*1.25), round(textPage.height*1.25)))
            fromCenter = False
            r = cv2.selectROI(imResize, fromCenter)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            #boundingBox = (131.75, 210, 267.46, 719)
            boundingBox = (r[0]*0.8, r[1]*0.8, r[0]*0.8+ r[2]*0.8, r[1]*0.8 + r[3]*0.8)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            #print(boundingBox)

            im_debug = target_pageLocation.to_image(resolution=150)
            im_debug.debug_tablefinder({"vertical_strategy": "lines", "horizontal_strategy": "text", "intersection_tolerance": 5, "snap_y_tolerance": 7})
            im_debug.save(f"img_select/debug/{name}_debug.png", format="PNG")


            extractedText = target_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "text", "intersection_tolerance": 5, "snap_y_tolerance": 7})

            print(extractedText)
            if extractedText is None:
                continue
            #CUSTOMISATION BLOCK
            for data in extractedText:
                if '' in data:
                    continue
                data.insert(0, name)
                print(data)
                data_list.append(data)
#


df = pd.DataFrame(data_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
df.to_csv(f'csv/Baku_SPT.csv')

print(df)