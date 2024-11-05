import os
import shutil
from PyPDF2 import PdfFileMerger

root_path = r"C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\Oedometer"
file_list = os.listdir(root_path)

merger = PdfFileMerger()


for file in file_list:
    if not file.endswith(".pdf"):
        continue
    file_path = f"{root_path}\{file}"
    merger.append(file_path)
    print(file)

merger.write(r"C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\Oedometer\script\T5 GI Oedometer_merged.pdf")
