import xlwings as xw
import pandas as pd

WB = xw.Book(r"C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\PSD\output\PSD output summary.xlsx")
WS = WB.sheets['i2 % Passing']

index_list = list(range(30))
type_list = ['500mm', '300mm', '150mm', '125mm', '90mm', '75mm', '63mm', '50mm', '37.5mm', '28mm', '20mm', '14mm', '10mm', '6.3mm', '5mm', '3.35mm', '2mm', '1.18mm', '0.6mm', '0.425mm', '0.3mm', '0.212mm', '0.15mm', '0.063mm', 'A', 'B', 'C', 'D', 'E', 'F']

merged_list = list(zip(index_list, type_list))


BH_name_list = []
ID_list = []
d_t_list = []
d_b_list = []
type_list = []
percentage_list = []


for i in range (2, 56):
    rowNumber = str(i)
    BH_name = WS.range(f'A{i}').value
    ID = WS.range(f'B{i}').value
    d_t = WS.range(f'C{i}').value
    d_b = WS.range(f'D{i}').value
    for index, type in merged_list:
        BH_name_list.append(BH_name)
        ID_list.append(ID)
        d_t_list.append(d_t)
        d_b_list.append(d_b)
        type_list.append(type)
        percentage_list.append(WS.range('E' + rowNumber).offset(0, index).value)

output_list = list(zip(BH_name_list, ID_list, d_t_list, d_b_list, type_list, percentage_list))
dataframe = pd.DataFrame(output_list)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
print(dataframe)
dataframe.to_csv(r'C:\Users\921722\Box\PC1063 DCT Gdansk\T5 GI Test Results\A_Test-data\PSD\output\formatted PSD.csv')