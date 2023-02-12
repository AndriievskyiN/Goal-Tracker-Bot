from openpyxl import Workbook

wb = Workbook()
wb.create_sheet("2023 Лютий 4")
ws = wb["2023 Лютий 4"]

print(ws)
