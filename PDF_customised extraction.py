import cv2
import pdfplumber
import os
import pandas as pd

#Just save a pdf in an empty folder, and paste in the link of the folder below as path
VBH_folder_path = r'C:\Users\921722\Royal HaskoningDHV\P-PC6298-Hunterston - Team\WIP\4. Geotechnical\02. OpenGround\1. Inputs\2. Lab Test Extraction\PSD 541325'
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

        for k in range(totalPages):
            local_description_list = []
            textPage = pdf.pages[k]

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
                boundingbox_list.append(boundingBox)
                print(boundingBox)
            else:
                boundingBox = boundingbox_list[0]
            ##############################################################
            ex_vert_lines = [307.20000000000005, 570.4000000000001]
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            im_debug = target_pageLocation.to_image(resolution=150)
            im_debug.debug_tablefinder({"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_x_tolerance": 30, "snap_y_tolerance": 5, "snap_x_tolerance": 5, "explicit_vertical_lines": ex_vert_lines, "keep_blank_chars": True})
            im_debug.save(f"img_select/debug/{k}_debug.png", format="PNG")

            ###This block below tries to extract the ID of the borehole per page, adjust bounding box as required
            try:
                id_bb = (96.0, 79.2, 263.20000000000005, 119.2)

                bb_location = textPage.crop(id_bb, relative=False)
                id_text = bb_location.extract_text(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "intersection_tolerance": 3, "snap_y_tolerance": 3, "snap_x_tolerance": 10, "keep_blank_chars": True})
                try:
                    id = id_text.replace("\n", " ")
                except:
                    id = id_text
            except:
                id = "ADD ID"

            extractedText = target_pageLocation.extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text", "intersection_x_tolerance": 30, "snap_y_tolerance": 5, "snap_x_tolerance": 5, "explicit_vertical_lines": ex_vert_lines, "keep_blank_chars": True})
            print(id, extractedText)

            if not extractedText:
                continue
            ####Raw data extracted up to this point
            ########################################################################################
            ### ADD Customised PARSING CODE BELOW!!!!!
            #vertical stack
            # depth_list = extractedText.split("\n")
            # for item in depth_list:
            #     d_list = [id]
            #     d_list.append(item)
            #     data_list.append(d_list)
            #     print(d_list)
            #stack column
            # local_description_list.append(id)
            # for item in extractedText[0]:
            #     print(item)
            #     local_description_list.append(item)
            # data_list.append(local_description_list)
            # print(local_description_list)
            ##########################################################################################
            # for item in extractedText [0]:
            #     d_list = [id]
            #     text = item[0].replace("\n", " ")
            #     if text == "":
            #         continue
            #     d_list.append(text)
            #     data_list.append(d_list)
            #     print(d_list)

            for item in extractedText [0]:
                d_list = [id]
                # if "" in item:
                #     continue
                for ele in item:
                    # if ele is None:
                    #     continue
                    print(ele)
                    ele = ele.replace("\n", " ")
                    d_list.append(ele)
                data_list.append(d_list)
                print(d_list)




print(data_list)
#
df = pd.DataFrame(data_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
df.to_csv(f'{VBH_folder_path}\data.csv')
print(df)