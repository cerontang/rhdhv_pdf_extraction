import os
import pdfplumber
import cv2
import pandas as pd

received_file_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20221103 AD\Pile Cap Reference Test Check\test report in sheet'
file_mainDir = os.listdir(received_file_path)
sameFormat = 'N'
master_boundingbox_list = []
skip_page_list = [0, 1]
sample_number_list = []
MDD_list = []

for file in file_mainDir:
    if not file.endswith(".pdf"):
        continue
    file_name = file.replace(".pdf", "")
    file_path = f'{received_file_path}\{file}'
    with pdfplumber.open(file_path) as pdf:
        totalPages = len(pdf.pages)
        local_description_list = []
        for k in range(totalPages):
            sampleNumber = None
            MDD = None
            if k in skip_page_list:
                continue
            textPage = pdf.pages[k]
            # Extraction of Description to get Grout Info
            if sameFormat == 'N':
                # Select Bounding Box
                print("Same format? (Y/N)")
                sameFormat = str(input())
                boundingBox = (0, 0, textPage.width, textPage.height)
                # print(boundingBox)
                target_pageLocation = textPage.crop(boundingBox, relative=False)
                select_img = target_pageLocation.to_image(resolution=150)
                select_img.save(f"img_select/{file}{k}.png", format="PNG")
                im = cv2.imread(f"img_select/{file}{k}.png")
                imResize = cv2.resize(im, (round(textPage.width * 1.25), round(textPage.height * 1.25)))
                fromCenter = False
                r = cv2.selectROI(imResize, fromCenter)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                # boundingBox = (131.75, 210, 267.46, 719)
                boundingBox = (r[0] * 0.8, r[1] * 0.8, r[0] * 0.8 + r[2] * 0.8, r[1] * 0.8 + r[3] * 0.8)
                master_boundingbox_list.append(boundingBox)
                # print(boundingBox)
                #########################
            else:
                boundingBox = master_boundingbox_list[0]
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            text = target_pageLocation.extract_text()
            text_list = text.split()
            if not "COMPATION" in text_list:
                continue
            print(k, text.split())
            for i in range(len(text_list)):
                if 'Sample#' in text_list[i]:
                    sampleNumber = text_list[i+1]
                if 'Mg/m' in text_list[i]:
                    MDD = text_list[i-1]
            if ((sampleNumber is None) and (MDD is None)):
                continue
            sample_number_list.append(sampleNumber)
            MDD_list.append(MDD)

output_list = list(zip(sample_number_list, MDD_list))
df = pd.DataFrame(output_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(df)

