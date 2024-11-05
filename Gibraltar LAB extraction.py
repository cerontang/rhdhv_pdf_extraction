import cv2
import pdfplumber
import os
import pandas as pd

VBH_folder_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\05-Ground Investigation\03 GI Results\Landside 2022\01 BH Logs'
VBH_list = os.listdir(VBH_folder_path)
sameFormat = 'N'
master_boundingbox_list = []
description_list = []
depth_t_list = []
depth_b_list = []
VBH_name_list = []
type_list = []
row_list = []

for VBH_file in VBH_list:
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
            if sameFormat == "N" and k == 0:
                print("Same format? (Y/N)")
                sameFormat = str(input())
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
                #########################
            elif sameFormat == "N" and k != 0:
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
                #########################
            elif sameFormat == "Y" and k != 0:
                boundingBox = master_boundingbox_list[0]
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            extractedText = target_pageLocation.extract_text(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 5, "snap_y_tolerance": 7})

            try:
                print(extractedText)
            except:
                pass
#             for row in extractedText:
#                 local_list = []
#                 for cell in row:
#                     try:
#                         cell = cell.replace("\n", " ")
#                     except:
#                         pass
#                     local_list.append(cell)
#                 row_list.append(local_list)
#
# dataframe = pd.DataFrame(row_list)
# pd.set_option('display.max_rows', 5000)
# pd.set_option('display.max_columns', 5000)
# pd.set_option('display.width', 10000)
#
# print(dataframe)
# dataframe.to_csv(r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20230206 AD\extract\land\vibrocore_PSD.csv')