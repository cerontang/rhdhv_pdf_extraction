import os
import pandas as pd

path = r"C:\Users\921722\Box\BI3753 Team\99 - Temp\_SSCT\20230503 Trojan Shop Drawing Check\Version 2\PNGs"
list = os.listdir(path)
dataframe = pd.DataFrame(list)
dataframe.to_csv(f'csv/SDS_image_list.csv')

