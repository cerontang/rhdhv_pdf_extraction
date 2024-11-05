import os
import cv2
import numpy as np
import pytesseract

def remove_table_lines(input_folder, output_folder):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    for image_file in image_files:
        # Read the input image
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to create a binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Perform morphological operations to enhance the table lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Find contours in the binary image
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area to remove small noise
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

        # Create a mask for the table lines
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, filtered_contours, -1, (255, 255, 255), cv2.FILLED)

        # Inpaint the table lines using the mask
        result = cv2.inpaint(image, mask, 3, cv2.INPAINT_NS)

        # Apply OCR to extract text
        text = pytesseract.image_to_string(result)

        # Draw bounding boxes around the detected text
        boxes = pytesseract.image_to_boxes(result)
        for box in boxes.splitlines():
            _, x, y, w, h, _ = box.split()
            cv2.rectangle(result, (int(x), result.shape[0] - int(y)), (int(w), result.shape[0] - int(h)), (0, 0, 0), -1)

        # Save the processed image to the output folder
        output_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_path, result)

        print(f"Processed: {image_file}")

    print("Table lines removal completed.")

# Example usage:
input_folder = r"C:\Users\921722\Box\PC1063 DCT Gdansk\PC3742-104-T3 dredging Claim C04\09 Claim C04\CTR GI\script\test\png"
output_folder = r"C:\Users\921722\Box\PC1063 DCT Gdansk\PC3742-104-T3 dredging Claim C04\09 Claim C04\CTR GI\script\test\png_out"
remove_table_lines(input_folder, output_folder)
