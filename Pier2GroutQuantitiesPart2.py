import pandas as pd
import xlwings as xw

source_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\Pier 2 Grout Information.xlsx'
WB = xw.Book(source_path)
WS = WB.sheets['Pier2_GroutDescription_Fugro_V1']
WS2 = WB.sheets['Pier2_AHAM_0.5 depth']

MD_list = []

for i in range(239, 626):
    main_or_detail = "D"
    textString = WS.range(f'e{i}').value
    textList = textString.split()
    for text in textList:
        if text.isupper():
            main_or_detail = "M"
            break
    MD_list.append(main_or_detail)
    WS.range(f'h{i}').value = main_or_detail
    print(main_or_detail, textString)

# dataframe = pd.DataFrame(MD_list)
# pd.set_option('display.max_rows', 5000)
# pd.set_option('display.max_columns', 5000)
# pd.set_option('display.width', 10000)
# dataframe.to_csv('csv\Pier2_Fugro_Main-Detail_list')

# for i in range(2, 718):
#     if WS.range(f'F{i}').value == 0:
#         continue
#     fullDescription_string = WS.range(f'E{i}').value
#     fullDescription_split = fullDescription_string.split()
#     for j in range(len(fullDescription_split)):
#         if fullDescription_split[j] == 'grout':
#             if fullDescription_split[j-1] == 'of':
#                 WS.range(f'F{i}').value = fullDescription_split[j-2]
#                 print(fullDescription_split[j-2])
#                 continue
#             WS.range(f'F{i}').value = fullDescription_split[j-1]
#             print(fullDescription_split[j-1])

#
# manual_check_list = []
# unique_manual_check_list = []
# for i in range(2, 1436):
#     currentDepth = float(WS2.range(f'C{i}').value)
#     vbhName = WS2.range(f'B{i}').value
#     print(vbhName, float(currentDepth))
#     for j in range(2, 718):
#         if vbhName != WS.range(f'B{j}').value:
#             continue
#         if currentDepth >= float(WS.range(f'C{j}').value) and currentDepth <= float(WS.range(f'D{j}').value):
#             WS2.range(f'G{i}').value = WS.range(f'G{j}').value
#             break


