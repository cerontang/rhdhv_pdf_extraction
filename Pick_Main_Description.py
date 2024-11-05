import re
import pdfplumber
import numpy as np
import pandas as pd
import xlwings as xw
import os
from datetime import date
import cv2

FGV_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\05-Ground Investigation\03 Factual Reports\APM HH 2022\05 OpenGround\Field Geological Descriptions.csv'
WB_FGV = xw.Book(FGV_path)
WS_FGV = WB_FGV.sheets["Field Geological Descriptions"]

FS_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\05-Ground Investigation\03 Factual Reports\APM HH 2022\05 OpenGround\Fracture Spacing.csv'
WB_FS = xw.Book(FS_path)
WS_FS = WB_FS.sheets["Fracture Spacing"]

for i in range(177, 205):
    BH_name = WS_FS.range(f"A{i}").value
    d_t = WS_FS.range(f"B{i}").value
    d_b = WS_FS.range(f"C{i}").value
    d_avg = (d_t + d_b) / 2
    print(d_avg)
    for j in range(2, 339):
        if BH_name != WS_FGV.range(f"A{j}").value:
            continue
        if d_avg >= WS_FGV.range(f"C{j}").value and d_avg <= WS_FGV.range(f"D{j}").value:
            WS_FS.range(f"N{i}").value = WS_FGV.range(f"I{j}").value
            break




