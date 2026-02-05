# -*- coding: utf-8 -*-
"""
CUCALCULATEEVERYSCENARIOS
Created on Wed Sep 10 18:25:02 2025
###################### AUTOMATE CHAINED SCENARIOS CALCULATOR #############################
@author: USER
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 09:45:22 2025

@author: USER
"""
#%%
import win32com.client as win32
import os
import time

#%%
file_path = r"C:\insert your directory\CALCULADORACENARIOSCUCENCADEADO1.xlsm"

# open Excel
excel = win32.gencache.EnsureDispatch("Excel.Application")
excel.Visible = True     # True for debugging
excel.DisplayAlerts = False
wb = excel.Workbooks.Open(file_path)

ws_cenario = wb.Worksheets("DADOSCENARIO")
ws_mae     = wb.Worksheets("MATHEUSPLANILHAMAE")

# source rows (scenarios) and destination rows (master sheet)
ROW_SRC_START = 2    # source: starts at row 2 in DADOSCENARIO
ROW_SRC_END   = 158  # total 157 values (row 2 to 158) → equivalent to 6..162 in master
ROW_DST_START = 6    # destination: starts at row 6 in MATHEUSPLANILHAMAE

# 1) build scenario map: { "CEN_03": { "A":colA, "B":colB } }
mapping = {}
used_cols = ws_cenario.UsedRange.Columns.Count
for col in range(1, used_cols + 1):
    header = ws_cenario.Cells(1, col).Value
    if header is None:
        continue
    header = str(header).strip()
    if header.endswith("_A"):
        key = header[:-2]
        mapping.setdefault(key, {})['A'] = col
    elif header.endswith("_B"):
        key = header[:-2]
        mapping.setdefault(key, {})['B'] = col

# sort scenarios for consistency
keys = sorted(mapping.keys())

# function to copy values
def copy_range_values(src_ws, src_col, dst_ws, dst_col,
                      r1_src=ROW_SRC_START, r2_src=ROW_SRC_END, r1_dst=ROW_DST_START):
    src_range = src_ws.Range(src_ws.Cells(r1_src, src_col), src_ws.Cells(r2_src, src_col))
    dst_range = dst_ws.Range(dst_ws.Cells(r1_dst, dst_col), ws_mae.Cells(r1_dst + (r2_src - r1_src), dst_col))
    dst_range.Value = src_range.Value

# iterate scenarios
basename = os.path.basename(file_path)
total = len(keys)
print(f"detected scenarios: {total}")

count = 0
for key in keys:
    entry = mapping[key]
    if 'A' not in entry or 'B' not in entry:
        print(f"Skipping {key} (incomplete)")
        continue

    colA = entry['A']
    colB = entry['B']

    # copy to MATHEUSPLANILHAMAE: A -> E, B -> O
    copy_range_values(ws_cenario, colA, ws_mae, 5)
    copy_range_values(ws_cenario, colB, ws_mae, 15)

    # write identifier in Z1
    ws_mae.Range("Z1").Value = key

    # recalculate formulas
    wb.Application.Calculate()

    # run macro
    macro_full = f"'{basename}'!CadastrarResultado"
    try:
        excel.Application.Run(macro_full)
    except Exception as e:
        print(f"Error running macro for {key}: {e}")

    count += 1
    if count % 50 == 0:
        print(f"{count}/{total} scenarios processed... ({time.strftime('%H:%M:%S')})")

# save and close
wb.Save()
wb.Close(SaveChanges=True)
excel.Quit()
print(f"✅ Completed: {count} scenarios processed and saved in {file_path}")
# Don't forget to enable the Excel macro named 'CadastrarResultado'