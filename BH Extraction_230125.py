import cv2
import pdfplumber
import os
import pandas as pd

VBH_folder_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\230125 BH Extraction\folder'
VBH_list = os.listdir(VBH_folder_path)
sameFormat = 'N'
master_boundingbox_list = []
FGE_list = []
SDD_list = []
VBH_name_list_FGE = []
VBH_name_list_SDD = []


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
            print(textPage.width, textPage.height)
            boundingBox_name = (469, 4.5, 545.2, 37.4)
            target_pageLocation_name = textPage.crop(boundingBox_name, relative=False)
            VBH_name = target_pageLocation_name.extract_text(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "text_x_tolerance": 600, "text_y_tolerance": 1})
            VBH_name = str(VBH_name).strip()
            # Extraction of Description
            boundingBox = (132.0, 156.8, 388.0, 724.0)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            extractedText = target_pageLocation.extract_table(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "text_x_tolerance": 600, "text_y_tolerance": 1})
            print(extractedText)
            if extractedText is None:
                continue
            for item in extractedText:
                if len(item) > 1:
                    item[0] = item[-1]
                if item[0] == "":
                    item[0] = "###"
                item[0] = item[0].replace("\n", " ")
                #DETAILED DESCRIPTION
                if ";" in item[0]:
                    SDD_list.append(item[0])
                    VBH_name_list_SDD.append(VBH_name)
                    continue
                #FGE
                print(VBH_name, k+1, item[0])
                FGE_list.append(item[0])
                VBH_name_list_FGE.append(VBH_name)


dataframe_FGE = pd.DataFrame(list(zip(VBH_name_list_FGE, FGE_list)))
dataframe_SDD = pd.DataFrame(list(zip(VBH_name_list_SDD, SDD_list)))
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)

dataframe_FGE.to_csv(r'C:\Users\921722\OneDrive - Royal HaskoningDHV\230125 BH Extraction\folder\output\FGE.csv')
dataframe_SDD.to_csv(r'C:\Users\921722\OneDrive - Royal HaskoningDHV\230125 BH Extraction\folder\output\SDD.csv')

