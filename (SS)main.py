import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Set the root folder path
root_folder = r"C:\Users\921722\Royal HaskoningDHV\P-PC6298-Hunterston - Team\WIP\4. Geotechnical\01. Ground Modelling\4. OpenGround output CSVs"

# Create a new Excel workbook
wb = Workbook()
wb.remove(wb.active)  # Remove the default sheet

# Iterate through all files in the root folder
for filename in os.listdir(root_folder):
    if filename.endswith('.csv'):
        # Read the CSV file
        csv_path = os.path.join(root_folder, filename)
        df = pd.read_csv(csv_path)

        # Create a new sheet with the CSV filename (without extension)
        sheet_name = os.path.splitext(filename)[0]
        ws = wb.create_sheet(title=sheet_name)

        # Write the dataframe to the sheet
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

# Save the Excel file
output_path = os.path.join(root_folder, "Summary of Ground Modelling_20240905.xlsx")
wb.save(output_path)

print(f"Excel file created successfully: {output_path}")