import cv2
import pdfplumber
import os
import pandas as pd
from datetime import date

VBH_folder_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20220727 AD\FS extract'
VBH_file_list = os.listdir(VBH_folder_path)

master_FI_list = []
master_Depth_t_list = []
master_Depth_b_list = []
master_BH_name_list = []

for VBH_file in VBH_file_list:
    if not VBH_file.endswith('.pdf'):
        continue
    VBH_file_path = f"{VBH_folder_path}\{VBH_file}"
    with pdfplumber.open(VBH_file_path) as pdf:
        totalPages = len(pdf.pages)
        for k in range(totalPages):
            textPage = pdf.pages[k]
            FI_boundingBox = (516.8000000000001, 217.60000000000002, 529.6, 717.6)
            FI_target_pageLocation = textPage.crop(FI_boundingBox, relative=False)
            FI_list = FI_target_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"})
            if FI_list is None:
                continue
            print(VBH_file, FI_list)
            for FI in FI_list:
                if FI[0] is None or FI[0] == '':
                    continue
                master_FI_list.append(FI[0])
                master_BH_name_list.append(VBH_file.split('.')[0])

            Depth_t_boundingBox = (360.8, 218.4, 389.2, 719.2)
            Depth_t_target_pageLocation = textPage.crop(Depth_t_boundingBox, relative=False)
            Depth_t_list = Depth_t_target_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"})
            if Depth_t_list is None:
                continue
            for Depth_t in Depth_t_list:
                if Depth_t[0] is None or Depth_t[0] == '':
                    continue
                if '\n' in Depth_t[0]:
                    continue
                master_Depth_t_list.append(Depth_t[0])

            Depth_b_boundingBox = (389.2, 218.4, 417.6, 719.2)
            Depth_b_target_pageLocation = textPage.crop(Depth_b_boundingBox, relative=False)
            Depth_b_list = Depth_b_target_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"})
            if Depth_b_list is None:
                continue
            for Depth_b in Depth_b_list:
                if Depth_b[0] is None or Depth_b[0] == '':
                    continue
                if '\n' in Depth_b[0]:
                    continue
                #special case here
                if Depth_b[0] == '20.31':
                    continue
                ###########################
                master_Depth_b_list.append(Depth_b[0])



print(master_Depth_t_list)
print(master_Depth_b_list)
print(master_FI_list)

outputList = list(zip(master_BH_name_list, master_Depth_t_list, master_Depth_b_list, master_FI_list))
dataframe = pd.DataFrame(outputList)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)
dataframe.to_csv(f'csv\{date.today()}_AHAM_VBH_FS.csv')