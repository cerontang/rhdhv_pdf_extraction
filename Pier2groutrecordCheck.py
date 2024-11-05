import os
import re
import pandas as pd

groutingRecords_received_path = r'C:\Users\921722\Box\BI3753 Team\62 - Received Trojan\220419 - Pier-2, 3 and 4 Grouting Record\Pier-2 Grouting Record'
groutingRecords_mainDir = os.listdir(groutingRecords_received_path)
print(groutingRecords_mainDir)
probeArea_List = []
probeList = []
output_probeArea_List = []

for fileName in groutingRecords_mainDir:
    #EXCEPTION CASE FOR INUNDATION AREA
    if fileName == '73) INUNDATION-S2208 TO S2209' or fileName == '74) INUNDATION-S2210 TO S2209':
        groutingRecords_inun_path = r'C:/Users/921722/Box/BI3753 Team/62 - Received Trojan/220419 - Pier-2, 3 and 4 Grouting Record/Pier-2 Grouting Record/'+fileName
        groutingRecords_inunDir = os.listdir(groutingRecords_inun_path)
        for element in groutingRecords_inunDir:
            probeArea_List.append(element)
            # LIST OUT THE PROBE IN EACH AREA, APPEND AREA NAME AS WELL TO PLUG IN DATAFRAME
            probe_in_nun_area_path = r'C:/Users/921722/Box/BI3753 Team/62 - Received Trojan/220419 - Pier-2, 3 and 4 Grouting Record/Pier-2 Grouting Record/' + r'/' + fileName + r'/' + element
            probe_in_inun_area_List = os.listdir(probe_in_nun_area_path)
            for probe in probe_in_inun_area_List:
                probeList.append(probe)
                output_probeArea_List.append(element)
        continue
    #CREATE LIST OF AREA INCLUDED IN NEW RECEIVED INFO
    fileName_split = fileName.split()
    #print(fileName_split)
    fileName_noNum = ''
    for i in range(len(fileName_split)):
        if i == 0:
            continue
        fileName_noNum += fileName_split[i] + " "
    fileName_noNum_trimmed = fileName_noNum.strip()
    probeArea_List.append(fileName_noNum_trimmed)

    #LIST OUT THE PROBE IN EACH AREA, APPEND AREA NAME AS WELL TO PLUG IN DATAFRAME
    probe_in_area_path = r'C:/Users/921722/Box/BI3753 Team/62 - Received Trojan/220419 - Pier-2, 3 and 4 Grouting Record/Pier-2 Grouting Record/' + fileName
    probe_in_area_List = os.listdir(probe_in_area_path)
    #print(probe_in_area_List)
    for probe in probe_in_area_List:
        probeList.append(probe)
        output_probeArea_List.append(fileName_noNum_trimmed)

probeArea_List = sorted(probeArea_List)



df = pd.DataFrame(list(zip(output_probeArea_List, probeList)))
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)
print(df)
df.to_csv(r'csv\P2groutingrecordsPROBELIST.csv')

df2 = pd.DataFrame(probeArea_List)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)
print(df2)
df2.to_csv(r'csv\P2groutingrecordsAREALIST.csv')