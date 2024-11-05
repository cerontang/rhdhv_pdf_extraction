import pdfplumber
import re
import os
import pandas as pd

VBH_folder_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\Pier 2'
VBH_list = os.listdir(VBH_folder_path)
master_description_list = []
master_depth_list = []
master_VBH_list = []
fugro_VBH_list = []
#print(VBH_list)

for VBH_file in VBH_list:
    if VBH_file == 'Pier 2 Verification_220525.pdf':
        continue
    if not VBH_file.endswith('.pdf'):
        continue
    VBH_file_path = f'C:/Users/921722/Box/BI3753 Team/30 - Geotech/06-Grouting works/02 - Verification/01 Copy of all verification BHs/Pier 2/{VBH_file}'
    #print(VBH_file_path)

    with pdfplumber.open(VBH_file_path) as pdf:
        #CHECK IF FILE IS FROM FUGRO
        firstPage = pdf.pages[0]
        if firstPage.height == 842:
            fugro_VBH_list.append(VBH_file.replace('.pdf', ''))
            continue
        #############################
        # append initial depth 0
        master_depth_list.append("0.00")
        totalPages = len(pdf.pages)
        local_description_list = []
        for k in range(totalPages):
            textPage = pdf.pages[k]
            # Extraction of Description to get Grout Info
            boundingBox = (131.75, 210, 267.46, 719)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            groutText = target_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 20})
            #VISUAL DEBUG TOOL
            im = target_pageLocation.to_image(resolution = 150)
            im.debug_tablefinder({"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 20})
            im.save(f"img_test/{VBH_file}{k}.png", format="PNG")
            for i, groutText_individual in enumerate(groutText):
                if i == 0:
                    continue
                if groutText_individual[0].strip().startswith("<Refer"):
                    continue
                if not groutText_individual[0]:
                    continue
                groutText_individual[0] = groutText_individual[0].replace("\n", " ")
                print(i, VBH_file, groutText_individual)
                local_description_list.append(groutText_individual[0])
            #######################################################################################################################
            #Extraction of depths
            boundingBox_depth = (40.5, 210, 71.72, 719)
            depth_pageLocation = textPage.crop(boundingBox_depth, relative=False)
            depths = depth_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 20})
            for j, depth_individual in enumerate(depths):
                if depth_individual[0] is None:
                    continue
                if depth_individual[0] == '':
                    continue
                if not depth_individual[0]:
                    continue
                depth_sorted_list = depth_individual[0].split()
                for depth_sorted_individual in depth_sorted_list:
                    master_depth_list.append(depth_sorted_individual)
                    #print(j, VBH_file, depth_sorted_individual)

        local_unique_description_list = []
        for index_description in range(len(local_description_list)):
            if index_description == 0:
                local_unique_description_list.append(local_description_list[index_description])
                continue
            if local_description_list[index_description].strip() == local_description_list[index_description-1].strip():
                continue

            local_unique_description_list.append(local_description_list[index_description])
        for description in local_unique_description_list:
            master_description_list.append(description)
            master_VBH_list.append(VBH_file.replace(".pdf", ""))


print(len(master_VBH_list), len(master_depth_list), len(master_description_list))
outputList1 = list(zip(master_VBH_list, master_depth_list, master_description_list))

dataframe = pd.DataFrame(outputList1)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)

for fugro_VBH in fugro_VBH_list:
    print(fugro_VBH)

#dataframe.to_csv('csv\Pier2_GI_Description.csv')