import os
from PyPDF2 import PdfFileMerger
import pdfplumber
import cv2

received_file_path = r'C:\Users\921722\OneDrive - Royal HaskoningDHV\20220826 AD\Pier 2 VBH\folder\Fugro\folder'
file_mainDir = os.listdir(received_file_path)
print(file_mainDir)


merger_AHAM = PdfFileMerger()
master_boundingbox_list = []
VBH_name_list = []

for fileName in file_mainDir:
    if not fileName.endswith('.pdf'):
        continue
    pdf_path = f'{received_file_path}\{fileName}'
    #MERGE pdf
    with pdfplumber.open(pdf_path) as pdf:
        totalPages = len(pdf.pages)
        for k in range (0, totalPages):
            textPage = pdf.pages[k]
            if k == 0:
                boundingBox = (0, 0, textPage.width, textPage.height)
                # print(boundingBox)
                target_pageLocation = textPage.crop(boundingBox, relative=False)
                select_img = target_pageLocation.to_image(resolution=150)
                select_img.save(f"img_select/{fileName}{k}.png", format="PNG")
                im = cv2.imread(f"img_select/{fileName}{k}.png")
                imResize = cv2.resize(im, (round(textPage.width * 1.25), round(textPage.height * 1.25)))
                fromCenter = False
                r = cv2.selectROI(imResize, fromCenter)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                # boundingBox = (131.75, 210, 267.46, 719)
                boundingBox = (r[0] * 0.8, r[1] * 0.8, r[0] * 0.8 + r[2] * 0.8, r[1] * 0.8 + r[3] * 0.8)

            else:
                boundingBox = master_boundingbox_list[0]
            master_boundingbox_list.append(boundingBox)
            name_pageLocation = textPage.crop(boundingBox, relative=False)
            VBH_name = name_pageLocation.extract_text(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 20})
            VBH_name = VBH_name.replace("Borehole:\n", "").strip()
            VBH_name = VBH_name.replace("BOREHOLE No.:", "").strip()
            print(VBH_name)
            VBH_name_list.append(VBH_name)



    

