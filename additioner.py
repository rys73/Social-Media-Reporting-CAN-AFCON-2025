import pandas as pd

# CONFIG
INPUT_FILE = r"C:\Users\ighik\OneDrive\Escritorio\malt_linkedin\REPORTING_FOOT.xlsx"
OUTPUT_FILE = r"C:\Users\ighik\OneDrive\Escritorio\malt_linkedin\FINAL_REPORTING_FOOT.xlsx"

# CONVERSION
def to_number(value):
    if pd.isna(value):
        return 0
    
    value = str(value).replace(" ", "").upper()
    value = value.replace(",", ".")

    try:
        if value.endswith("K"):
           return float(value[:-1]) * 1_000
        elif value.endswith("M"):
            return float(value[:-1]) * 1_000_000
        else:
            return float(value)
    except:
        return 0

df = pd.read_excel(INPUT_FILE)

df["LIKES_NUM"] = df["LIKES"].apply(to_number)
df["VUES_NUM"] = df["VUES"].apply(to_number)

total_likes = int(df["LIKES_NUM"].sum())
total_vues = int(df["VUES_NUM"].sum())

df["TOTAL_LIKES"] = total_likes
df["TOTAL_VUES"] = total_vues

df.drop(columns=["LIKES_NUM", "VUES_NUM"], inplace=True)

df.to_excel(OUTPUT_FILE, index=False)

