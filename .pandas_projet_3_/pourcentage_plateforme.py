import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =====================
# CONFIGURATION
# =====================
INPUT_FILE = r"C:\Users\ighik\OneDrive\Escritorio\malt_linkedin\REPORTING_FOOT.xlsx"
OUTPUT_FILE = r"C:\Users\ighik\OneDrive\Escritorio\malt_linkedin\TOTAUX_REPORTING_FOOT.xlsx"
GRAPH_TOTAL_FILE = r"C:\Users\ighik\OneDrive\Escritorio\malt_linkedin\REPORTING_FOOT_TOTAUX.pdf"
GRAPH_PERCENT_FILE = r"C:\Users\ighik\OneDrive\Escritorio\malt_linkedin\REPORTING_FOOT_POURCENTAGES.pdf"

# =====================
# FONCTIONS
# =====================
def to_number(value):
    """Convertit les formats 1K, 2.5M, 1 200 en nombre"""
    if pd.isna(value):
        return 0
    value = str(value).replace(" ", "").upper().replace(",", ".")
    try:
        if value.endswith("K"):
            return float(value[:-1]) * 1_000
        elif value.endswith("M"):
            return float(value[:-1]) * 1_000_000
        else:
            return float(value)
    except ValueError:
        return 0


def human_format(num):
    """Format lisible pour affichage"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(int(num))


# =====================
# LECTURE & NETTOYAGE
# =====================
df = pd.read_excel(INPUT_FILE)

df["Likes_num"] = df["LIKES"].apply(to_number)
df["Vues_num"] = df["VUES"].apply(to_number)

# =====================
# TOTAUX GLOBAUX
# =====================
total_likes = int(df["Likes_num"].sum())
total_vues = int(df["Vues_num"].sum())

df["TOTAL_LIKES"] = total_likes
df["TOTAL_VUES"] = total_vues

# =====================
# EXPORT EXCEL
# =====================
df_export = df.drop(columns=["Likes_num", "Vues_num"])
df_export.to_excel(OUTPUT_FILE, index=False)

# =====================
# AGRÉGATION PAR PLATEFORME
# =====================
totaux = (
    df.groupby("Plateforme")[["Likes_num", "Vues_num"]]
    .sum()
    .reset_index()
)

# =====================
# CALCUL DES %
# =====================
totaux["Likes_%"] = (totaux["Likes_num"] / total_likes) * 100
totaux["Vues_%"] = (totaux["Vues_num"] / total_vues) * 100

# =====================
# GRAPHIQUE TOTAUX
# =====================
x = np.arange(len(totaux))
width = 0.35

plt.figure(figsize=(10, 6))

plt.bar(x - width/2, totaux["Likes_num"], width, label="LIKES", alpha=0.8)
plt.bar(x + width/2, totaux["Vues_num"], width, label="VUES", alpha=0.6)

for i, row in totaux.iterrows():
    plt.text(i - width/2, row["Likes_num"], human_format(row["Likes_num"]),
             ha="center", va="bottom", fontsize=9)
    plt.text(i + width/2, row["Vues_num"], human_format(row["Vues_num"]),
             ha="center", va="bottom", fontsize=9)

plt.xticks(x, totaux["Plateforme"])
plt.title("Total des Likes et des Vues par plateforme")
plt.xlabel("Plateforme")
plt.ylabel("Nombre")
plt.legend()
plt.tight_layout()

plt.savefig(GRAPH_TOTAL_FILE)
plt.show()

# =====================
# GRAPHIQUE POURCENTAGES
# =====================
plt.figure(figsize=(10, 6))

plt.bar(x - width/2, totaux["Likes_%"], width, label="LIKES (%)", alpha=0.8)
plt.bar(x + width/2, totaux["Vues_%"], width, label="VUES (%)", alpha=0.6)

for i, row in totaux.iterrows():
    plt.text(i - width/2, row["Likes_%"], f"{row['Likes_%']:.1f}%",
             ha="center", va="bottom", fontsize=9)
    plt.text(i + width/2, row["Vues_%"], f"{row['Vues_%']:.1f}%",
             ha="center", va="bottom", fontsize=9)

plt.xticks(x, totaux["Plateforme"])
plt.title("Répartition des Likes et des Vues par plateforme (%)")
plt.xlabel("Plateforme")
plt.ylabel("Pourcentage (%)")
plt.legend()
plt.tight_layout()

plt.savefig(GRAPH_PERCENT_FILE)
plt.show()

