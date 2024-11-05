import xlwings as xw

source_path = r"C:\Users\921722\OneDrive - Royal HaskoningDHV\230125 BH Extraction\folder\output\FGE.xlsx"
WB = xw.Book(source_path)
WS = WB.sheets['SPT']

master_list = []
local_list = []
name_list = []

for i in range (2, 303):
    string = str(WS.range(f'C{i}').value).strip()
    depth = string.split(";")[0].replace("m", "")
    WS.range(f'D{i}').value = depth
    try:
        content = string.split(";")[1].split("N")[0].strip().replace("(", "").replace(")", "").split(",")
    except:
        content = string.split(";")[1].split("N")[0].strip().replace("(", "").replace(")", "")
    print(i, content)
    if len(content) >= 3:
        WS.range(f'F{i}').value = content[1]
        WS.range(f'G{i}').value = content[2]
    if len(content) == 2:
        WS.range(f'F{i}').value = content[1]
    if len(content) == 1:
        WS.range(f'E{i}').value = content[0]


