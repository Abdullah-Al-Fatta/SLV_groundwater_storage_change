"""
Created on Thu Mar  7 14:55:23 2025

@author: Abdullah Al Fatta
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- Load data --------------------
df = pd.read_csv(
    r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Diversion_data_m3.csv'
)

# Drop Total column if exists
df.drop(columns=['Total'], inplace=True, errors='ignore')

# -------------------- Prepare data --------------------
df.set_index('Year', inplace=True)

# Monthly totals (for panel b)
monthly_sum = df.sum()

# -------------------- Create side-by-side figure --------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)

# ===== (a) Stacked bar: Annual diversions =====
df.plot(
    kind='bar',
    stacked=True,
    ax=ax1,
    color=sns.color_palette("Paired", len(df.columns)),
    alpha=0.8
)

ax1.set_xlabel("Year", fontsize=14)
ax1.set_ylabel("Diversions (m³)", fontsize=14)
ax1.set_title("Annual Diversions by Month", fontsize=14)
ax1.tick_params(axis='x', rotation=45)
ax1.tick_params(axis='both', labelsize=14, length=6, width=1.5)
ax1.legend(title="Month", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=12)

# Panel label
ax1.text(-0.12, 1.05, "(a)", transform=ax1.transAxes,
         fontsize=14, fontweight="bold")

# ===== (b) Monthly total across years =====
bars = ax2.bar(monthly_sum.index, monthly_sum,
               color='chocolate', alpha=0.75)

ax2.set_xlabel("Month", fontsize=14)
ax2.set_ylabel("Total Diversion (m³)", fontsize=14)
ax2.set_title("Total Monthly Diversions (All Years)", fontsize=14)
ax2.tick_params(axis='x', rotation=45)
ax2.tick_params(axis='both', labelsize=13, length=6, width=1.5)

# Add edge styling
for bar in bars:
    bar.set_edgecolor('black')
    bar.set_linewidth(0.7)

# Panel label
ax2.text(-0.12, 1.05, "(b)", transform=ax2.transAxes,
         fontsize=14, fontweight="bold")

# Final layout
plt.tight_layout()

# Save outputs
# plt.savefig(
#     r'D:\OneDrive - Colostate\Al Fatta Smith\Writing\Final_data_20250512\Figures_20251106\Monthly_Diversions_side_by_side.png',
#     dpi=300,
#     bbox_inches='tight'
# )

plt.show()

