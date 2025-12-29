# ============================================================
# Validation & Replication of Table 5.1 (PVGIS SARAH3)
# Produces:
#  - validation_table_5_1.csv
#  - fig_monthly_energy_4cities.png
#  - fig_monthly_PR_4cities.png
# ============================================================

import re
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1) PVGIS CSV files (paths)
# -----------------------------
FILES = {
    "Berlin":   "PVdata_52.520_13.405_SA3_crystSi_1kWp_14_35deg_0deg.csv",
    "Cologne":  "PVdata_50.934_6.962_SA3_crystSi_1kWp_14_35deg_0deg.csv",
    "Hamburg":  "PVdata_53.550_10.000_SA3_crystSi_1kWp_14_35deg_0deg (2).csv",
    "Munich":   "PVdata_48.138_11.575_SA3_crystSi_1kWp_14_35deg_0deg (1).csv",
}

# -----------------------------
# 2) Table 5.1 values (thesis)
# -----------------------------
TABLE_5_1 = {
    "Berlin":  {"energy": 1049.41, "pr": 79.98},
    "Cologne": {"energy": 1038.09, "pr": 79.83},
    "Hamburg": {"energy": 989.88,  "pr": 80.07},
    "Munich":  {"energy": 1137.39, "pr": 79.43},
    "Average": {"energy": 1053.69, "pr": 79.83},
}

# -----------------------------
# 3) Read PVGIS monthly table
# -----------------------------
def read_pvgis_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Month"):
            start = i

    if start is None:
        raise ValueError(f"Month header not found in {filepath}")

    rows = []
    for line in lines[start + 1:]:
        if line.strip().startswith("Year"):
            break

        m = re.match(
            r"\s*(\d{1,2})\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)",
            line.replace("\t", " ")
        )
        if m:
            rows.append([
                int(m.group(1)),          # Month
                float(m.group(3)),        # E_m
                float(m.group(5)),        # H(i)_m
            ])

    df = pd.DataFrame(rows, columns=["Month", "E_m", "H_i_m"])
    df = df.sort_values("Month")

    if len(df) != 12:
        raise ValueError(f"{filepath}: expected 12 months, got {len(df)}")

    return df

# -----------------------------
# 4) Compute indicators
# -----------------------------
results = []
monthly_data = {}

for city, file in FILES.items():
    df = read_pvgis_csv(file)
    monthly_data[city] = df

    annual_energy = df["E_m"].sum()
    annual_pr = (df["E_m"].sum() / df["H_i_m"].sum()) * 100

    results.append({
        "City": city,
        "Annual_energy_calc_kWh": round(annual_energy, 2),
        "Annual_energy_table_kWh": TABLE_5_1[city]["energy"],
        "Energy_diff": round(annual_energy - TABLE_5_1[city]["energy"], 4),
        "PR_calc_%": round(annual_pr, 2),
        "PR_table_%": TABLE_5_1[city]["pr"],
        "PR_diff": round(annual_pr - TABLE_5_1[city]["pr"], 4),
    })

df_results = pd.DataFrame(results)

# Average row
avg_energy = df_results["Annual_energy_calc_kWh"].mean()
avg_pr = df_results["PR_calc_%"].mean()

df_results = pd.concat([
    df_results,
    pd.DataFrame([{
        "City": "Average",
        "Annual_energy_calc_kWh": round(avg_energy, 2),
        "Annual_energy_table_kWh": TABLE_5_1["Average"]["energy"],
        "Energy_diff": round(avg_energy - TABLE_5_1["Average"]["energy"], 4),
        "PR_calc_%": round(avg_pr, 2),
        "PR_table_%": TABLE_5_1["Average"]["pr"],
        "PR_diff": round(avg_pr - TABLE_5_1["Average"]["pr"], 4),
    }])
], ignore_index=True)

# Save validation table
df_results.to_csv("validation_table_5_1.csv", index=False)

print("\nVALIDATION RESULTS — Table 5.1\n")
print(df_results.to_string(index=False))
print("\nSaved: validation_table_5_1.csv")

# -----------------------------
# 5) FIGURE 1 — Monthly Energy
# -----------------------------
plt.figure(figsize=(10,5))
for city, df in monthly_data.items():
    plt.plot(df["Month"], df["E_m"], marker="o", label=city)

plt.xlabel("Month")
plt.ylabel("Monthly AC energy output (kWh)")
plt.title("Validation: Monthly PV Energy Output (PVGIS SARAH3, 1 kWp)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("fig_monthly_energy_4cities.png", dpi=200)
plt.close()

# -----------------------------
# 6) FIGURE 2 — Monthly PR
# -----------------------------
plt.figure(figsize=(10,5))
for city, df in monthly_data.items():
    pr = (df["E_m"] / df["H_i_m"]) * 100
    plt.plot(df["Month"], pr, marker="o", label=city)

plt.xlabel("Month")
plt.ylabel("PR (%)")
plt.title("Validation: Monthly Performance Ratio (PR)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("fig_monthly_PR_4cities.png", dpi=200)
plt.close()

print("\nFigures saved:")
print(" - fig_monthly_energy_4cities.png")
print(" - fig_monthly_PR_4cities.png")