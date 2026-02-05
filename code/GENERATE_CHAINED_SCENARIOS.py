# -*- coding: utf-8 -*-
""" CHAINED LOGIC SCENARIO (generate scenarios)
@author: Matheus
"""
#%%
import pandas as pd
import numpy as np
import re
import itertools

#%%
# 1) Read CSV
FILE = r"C:\insert your directory\cenariosvolume.csv"
df = pd.read_csv(FILE, sep=None, engine="python", encoding="utf-8-sig")

# ---- NEW: if there are negative values in the CSV, set them to zero here ----
df = df.clip(lower=0)

#%%
# 2) Normalize column names
def norm(c):
    return re.sub(r'[^0-9A-Za-z]+', '', str(c)).upper()

df = df.rename(columns={c: norm(c) for c in df.columns})

print("Available columns:", list(df.columns))

#%%
# 3) Detect emitters
emissores = sorted({
    int(re.match(r"(\d+)[ABM]", c).group(1))
    for c in df.columns if re.match(r"(\d+)[ABM]", c) and not c.startswith("0")
})

print("Detected emitters:", emissores)

#%%
# 4) Generate scenarios
todos_cenarios = []
for r in range(1, len(emissores) + 1):
    for comb in itertools.combinations(emissores, r):
        todos_cenarios.append(comb)

print(f"Total generated scenarios: {len(todos_cenarios)}")

#%%
# 5) Process scenarios
resultados = {}

for combo in todos_cenarios:
    nome_cenario = "_".join([f"{e:02d}" for e in combo])

    if len(combo) == 1:
        # Scenario with 1 emitter
        emissor = combo[0]
        colA = f"{emissor}A"
        colB = f"{emissor}B"
        colM = f"{emissor}M"

        df[colM] = pd.to_numeric(df[colM], errors="coerce").fillna(1).astype(int)
        mask = (df[colM] == 0)

        EM_A = np.where(mask, df[colA], df["0A"])
        EM_B = np.where(mask, df[colB], df["0B"])

        # 🔒 Zero floor
        EM_A = np.clip(EM_A, 0, None)
        EM_B = np.clip(EM_B, 0, None)

    else:
        # Scenario with >=2 emitters → chained logic
        RefA = df["0A"].copy()
        RefB = df["0B"].copy()

        DifA = np.zeros(len(df))
        DifB = np.zeros(len(df))

        for emissor in combo:
            colA = f"{emissor}A"
            colB = f"{emissor}B"
            colM = f"{emissor}M"

            if colM not in df.columns:
                continue

            df[colM] = pd.to_numeric(df[colM], errors="coerce").fillna(1).astype(int)
            mask = (df[colM] == 0)

            # Incremental update
            DifA = np.where(mask, DifA + (RefA - df[colA]), DifA)
            DifB = np.where(mask, DifB + (RefB - df[colB]), DifB)

            # ---- NEW: lock DifA/DifB to never exceed RefA/RefB ----
            DifA = np.clip(DifA, 0, RefA)
            DifB = np.clip(DifB, 0, RefB)

        EM_A = RefA - DifA
        EM_B = RefB - DifB

        # 🔒 Guaranteed zero floor
        EM_A = np.clip(EM_A, 0, None)
        EM_B = np.clip(EM_B, 0, None)

    resultados[f"CEN_{nome_cenario}_A"] = EM_A
    resultados[f"CEN_{nome_cenario}_B"] = EM_B

#%%
# 6) Export
final = pd.DataFrame(resultados)
OUT = r"C:\insert your directory\scenarios_chained.xlsx"
final.to_excel(OUT, index=False, engine="openpyxl")
print(f"✅ Single file saved (chained logic). Don't forget to get volumes 0A and 0B from cenario_volume table and insert them in two new columns to the left of the first scenario in the generated table. You need rename columns CEN_00_A and CEN_00_B: {OUT}")
# ⚠️ IMPORTANT NOTE:
# If you choose to automate CU calculation for all scenarios:
# 1. Copy all cells from this file
# 2. Paste them into a worksheet named 'DADOSCENARIO' in the 'CALCULADORACENARIOSCUCENCADEADO1' spreadsheet
# 3. Another code will be used to collect data from the 'DADOSCENARIO' sheet
#    and input it into 'MATHEUSPLANILHAMAE' for calculation.