import xlwings as xw

source_path = r"C:\Users\921722\OneDrive - Royal HaskoningDHV\20230525 AD\test\results\Baku_BH Logs_outputs.xlsx"
WB = xw.Book(source_path)
WS = WB.sheets['Baku_SPT']

for i in range(2, 797):
    try:
        range = WS.range(f'C{i}').value
        range = range.split("-")
        depth = range[0]
        if len(range) == 2:
            WS.range(f'D{i}').value = depth
    except:
        pass