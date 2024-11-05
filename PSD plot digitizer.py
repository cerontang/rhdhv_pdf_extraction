import cv2
import numpy as np
import pdfplumber
import os
from io import BytesIO

def digitize_plot(i):
    # Download the image from the provided URL

    #img = cv2.imdecode(np.frombuffer(i, np.uint8), cv2.IMREAD_COLOR)
    img = i
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Apply Hough line transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

    # Extract the coordinates of the detected line
    line_coords = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        line_coords.append([(x1, y1), (x2, y2)])

    # Display the detected line
    line_img = np.zeros_like(img)
    for line in line_coords:
        cv2.line(line_img, line[0], line[1], (0, 0, 255), 2)

    # Display the original image and the detected line
    cv2.imshow('Original Image', img)
    cv2.imshow('Detected Line', line_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Extract the x and y coordinates of the detected line
    x_coords = [point[0] for point in line_coords[0]]
    y_coords = [point[1] for point in line_coords[0]]

    # Return the digitized data
    return x_coords, y_coords

VBH_folder_path = r'C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\PSD\script\format_1'
VBH_list = os.listdir(VBH_folder_path)
# Example usage

for VBH_file in VBH_list:
    if not VBH_file.endswith('.pdf'):
        continue
    VBH_file_path = f'{VBH_folder_path}\{VBH_file}'
    with pdfplumber.open(VBH_file_path) as pdf:
        #############################
        totalPages = len(pdf.pages)
        # print(totalPages)
        local_description_list = []
        for k in range(totalPages):
            textPage = pdf.pages[k]
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
            boundingBox = (r[0] * 0.8, r[1] * 0.8, r[0] * 0.8 + r[2] * 0.8, r[1] * 0.8 + r[3] * 0.8)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            pass_img = target_pageLocation.to_image(resolution=150)
            pass_img.save(f"img_select/{VBH_file}{k}_pass.png", format="PNG")
            im_pass = cv2.imread(f"img_select/{VBH_file}{k}_pass.png")
            x_values, y_values = digitize_plot(im_pass)

            print("X values:", x_values)
            print("Y values:", y_values)
