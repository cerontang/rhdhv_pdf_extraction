import pdfplumber
import os
import pandas as pd

VBH_folder_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\230125 BH Extraction\folder'
VBH_list = os.listdir(VBH_folder_path)

level_list = []
name_list = []

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
            VBH_name = target_pageLocation_name.extract_text(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "text_x_tolerance": 600, "text_y_tolerance": 3})
            VBH_name = str(VBH_name).strip()
            # Extraction of Description
            boundingBox = (420, 156.8, 550, 724.0)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            extractedText = target_pageLocation.extract_text(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "text_x_tolerance": 5000, "text_y_tolerance": 10})

            if extractedText is None:
                continue
            extractedText = extractedText.replace("\n","###")
            SPT_list = extractedText.split("###")
            print(VBH_name, SPT_list)
            for item in SPT_list:
                level_list.append(item)
                name_list.append(VBH_name)

dataframe_level = pd.DataFrame(list(zip(name_list, level_list)))
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)

dataframe_level.to_csv(r'C:\Users\921722\OneDrive - Royal HaskoningDHV\230125 BH Extraction\folder\output\SPT.csv')
