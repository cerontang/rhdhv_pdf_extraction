import cv2
import pdfplumber
import os
import pandas as pd
import pyautogui



def countPDF (pdf_directory):
    pdfCount = 0
    pdf_list = os.listdir(pdf_directory)
    for file in pdf_list:
        if file.endswith(".pdf"):
            pdfCount += 1
            continue
    return pdfCount

def defineDirectory ():
    pdf_directory = str(pyautogui.prompt(text='Please enter the path of saved PDFs', title='PDF extraction tool v0.00', default=''))
    if os.path.exists(pdf_directory):
        return pdf_directory
    else:
        pyautogui.alert(text=f"Path invalid", title='PDF extraction tool v0.00', button='OK')
    # r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\Pier 2'


def pdfExtraction (PDF_file_path, PDF, extractType):
    with pdfplumber.open(PDF_file_path) as pdf:
        totalPages = len(pdf.pages)
        extractedData = []
        for k in range(totalPages):
            textPage = pdf.pages[k]
            # Data Extraction
            boundingBox = (0, 0, textPage.width, textPage.height)
            # print(boundingBox)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            select_img = target_pageLocation.to_image(resolution=150)
            select_img.save(f"img_select/{PDF}_{k}.png", format="PNG")
            im = cv2.imread(f"img_select/{PDF}_{k}.png")
            imResize = cv2.resize(im, (round(textPage.width * 1.25), round(textPage.height * 1.25)))
            fromCenter = False
            r = cv2.selectROI(imResize, fromCenter)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # boundingBox = (131.75, 210, 267.46, 719)
            boundingBox = (r[0] * 0.8, r[1] * 0.8, r[0] * 0.8 + r[2] * 0.8, r[1] * 0.8 + r[3] * 0.8)
            target_pageLocation = textPage.crop(boundingBox, relative=False)
            if extractType == 'Text Only':
                extractedData_local = target_pageLocation.extract_text(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 20})
                if len(extractedData) > 1:
                    extractedData.append(extractedData_local)
                    #extractedData = " ".join(extractedData)
                    continue
                extractedData.append(extractedData_local)
                continue
            if extractType == 'Table (Experimental)':
                extractedData_local = target_pageLocation.extract_tables(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "intersection_tolerance": 20})
                if k > 0:
                    extractedData.append(extractedData_local)
                    continue
                extractedData.append(extractedData_local)
                continue
        return list(extractedData)

if __name__ == "__main__":

    def main():
        ######MAIN CODE BLOCK STARTS HERE
        #1. Get Directory of PDF files
        pdf_directory = defineDirectory()
        pdfCount = countPDF(pdf_directory)
        if pdfCount == 0:
            pyautogui.alert(text=f"No PDF files are located.", title='PDF extraction tool v0.00', button='OK')
            main()
        else:
            pyautogui.alert(text=f"{pdfCount} PDF files are located.", title='PDF extraction tool v0.00', button='OK')
        ################################
        #2. Loop through PDF files and extract
        PDF_list = os.listdir(pdf_directory)
        masterExtraction_list = []
        for PDF in PDF_list:
            if not PDF.endswith('.pdf'):
                continue
            if PDF == 'Pier 2 Verification_220525.pdf':
                continue
            PDF_file_path = f'{pdf_directory}\{PDF}'
            extractType = pyautogui.confirm(text='Please select what to extract:', title='PDF extraction tool v0.00', buttons=['Text Only', 'Table (Experimental)'])
            extractedData = pdfExtraction (PDF_file_path, PDF, extractType)
            if extractType == 'Text Only':
                for i in range(len(extractedData)):
                    masterExtraction_list.append(extractedData[i].replace("\n", " "))
                    print(extractedData[i].replace("\n", " "))
            else:
                print(extractedData)
                print(len(extractedData))
                for i in range(len(extractedData)):
                    for j in range(len(extractedData[i][0])):
                        print(extractedData[i][0][j])
                        masterExtraction_list.append(extractedData[i][0][j])
        ##MAIN CODE BLOCK ENDS HERE
        #Dataframe Generation
        dataframe = pd.DataFrame(masterExtraction_list)
        pd.set_option('display.max_rows', 5000)
        pd.set_option('display.max_columns', 5000)
        pd.set_option('display.width', 10000)
        print(dataframe)
        csvName = str(pyautogui.prompt(text='Please enter the name for output PDF', title='PDF extraction tool v0.00', default=f"Output_{extractType}"))
        dataframe.to_csv(f'csv\{csvName}.csv')

    main()

