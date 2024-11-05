import xlwings as xw

source_path = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\Pier 2 Grout Information.xlsx'
WB = xw.Book(source_path)
WS = WB.sheets['Pier2_Grout_Fugro_D_only']
WS2 = WB.sheets['Pier2_GroutDescription_Fugro_V2']

for i in range(2, 457):
    groutList_inrange = []
    currentDepth = float(WS2.range(f'C{i}').value)
    currentDepth_lower = currentDepth + 0.5
    vbhName = WS2.range(f'B{i}').value
    print(vbhName, float(currentDepth))
    for j in range(2, 280):
        if vbhName != WS.range(f'B{j}').value:
            continue
        if currentDepth >= float(WS.range(f'C{j}').value) and currentDepth < float(WS.range(f'D{j}').value):
            groutList_inrange.append(WS.range(f'F{j}').value)
        if currentDepth < float(WS.range(f'C{j}').value) and currentDepth_lower >= float(WS.range(f'D{j}').value):
            groutList_inrange.append(WS.range(f'F{j}').value)
            break
    if len(groutList_inrange) == 0:
        groutList_inrange.append(float(0.00))
    grout_avg = sum(groutList_inrange)/len(groutList_inrange)
    #print(groutList_inrange)
    print(grout_avg)
    #WS2.range(f'D{i}').value = grout_avg