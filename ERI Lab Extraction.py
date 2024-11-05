import cv2
import pdfplumber
import os
import pandas as pd

VBH_folder_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\01 Final Logs to Check\Processed Logs_SSCT\ERI\labs'
VBH_list = os.listdir(VBH_folder_path)
master_boundingbox_list = []
firstRun = 'Y'
output_list = []

for VBH_file in VBH_list:
    if not VBH_file.endswith('.pdf'):
        continue
    VBH_name = VBH_file.replace(".pdf", "")
    VBH_file_path = f'{VBH_folder_path}\{VBH_file}'
    #print(VBH_file_path)

    with pdfplumber.open(VBH_file_path) as pdf:
        #############################
        totalPages = len(pdf.pages)
        # print(totalPages)
        local_description_list = []
        for k in range(totalPages):
            if k == 0:
                continue
            textPage = pdf.pages[k]
            if firstRun == "Y":
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
                master_boundingbox_list.append(boundingBox)
                firstRun = "N"
            else:
                boundingBox = master_boundingbox_list[0]
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            extractedText = target_pageLocation.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 5, "snap_y_tolerance": 7})
            #print(extractedText)
            for row in extractedText:
                local_list = []
                row.insert(0, f"{VBH_name}")
                print(row)
                for item in row:
                    if item is None:
                        continue
                    if "\n" in item:
                        continue
                    if item == "BH No." or item == "LL" or item == "PL":
                        continue
                    item = item.replace(" ", "").strip()
                    local_list.append(item)
                output_list.append(local_list)

for list in output_list:
    print(list)

dataframe = pd.DataFrame(output_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)
dataframe.to_csv(r"csv\230109_lab_test.csv")
