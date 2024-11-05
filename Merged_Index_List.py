import pdfplumber
import os
import pandas as pd

firstPage_list = []
lastPage_list = []
VBH_name_list = []

VBH_dir = r"C:\Users\921722\OneDrive - Royal HaskoningDHV\20221213 AD"
VBH_file_list = os.listdir(VBH_dir)

mergedPage = 0
for VBH_file in VBH_file_list:
    if not VBH_file.endswith(".pdf"):
        continue
    VBH_name = VBH_file.replace(".pdf", "")
    VBH_name_list.append(VBH_name)
    VBH_file_path = f'{VBH_dir}\{VBH_file}'
    with pdfplumber.open(VBH_file_path) as pdf:
        totalPages = len(pdf.pages)
        firstPage_list.append(mergedPage)
        mergedPage = mergedPage + totalPages
        lastPage = mergedPage - 1
        lastPage_list.append(lastPage)

output_list = list(zip(VBH_name_list, firstPage_list, lastPage_list))
df = pd.DataFrame(output_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(df)
df.to_csv(r"csv\index.csv")

