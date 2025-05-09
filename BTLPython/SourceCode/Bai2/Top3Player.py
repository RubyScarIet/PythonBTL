import pandas as pd

# List of performance metrics to analyze
METRICS = [
    "Age", "MP", "Starts", "Min", "Gls", "Ast", "CrdY", "CrdR", "xG", "xAG",
    "PrgCs", "PrgPs", "PrgRs", "Gls.1", "Ast.1", "xG.1", "xAG.1", "SoT%", "SoT/90",
    "G/Sh", "Dist", "Cmp", "Cmp%", "TotDist", "Cmp%.1", "Cmp%.2", "Cmp%.3",
    "KP", "Pto1/3", "PPA", "CrsPA", "PrgPp", "SCA", "SCA90", "GCA", "GCA90",
    "Tkl", "TklW", "Attd", "Lostd", "Blocks", "Sh", "Pass", "Int", "Touches",
    "Def Pen", "Def 3rd", "Mid 3rd", "Att 3rd", "Att Pen", "Attp", "Succ%",
    "Tkld%", "Carries", "PrgDist", "PrgCp", "Cto1/3", "CPA", "Mis", "Dis", "Rec",
    "PrgRp", "Fls", "Fld", "Off", "Crs", "Recov", "Won", "Lostm", "Won%",
    "GA90", "Save%", "CS%", "Save%.1"
]

# Input and output file paths
INPUT = "results.csv"
OUTPUT = "top3.txt"

print("🔄 Starting process ...")

try:
    # Load data from CSV file
    print(f"📂 Loading data from '{INPUT}' ...")
    df = pd.read_csv(INPUT, na_values=["N/a", "NA", "NaN", "-", ""], encoding="utf-8-sig", engine="python")
    if df.empty:
        raise ValueError(f"❌ Input file '{INPUT}' contains no data.")
    print("✅ Data loaded successfully.")

    # Sanitize the columns to handle missing values and convert to numeric
    print("🧹 Sanitizing columns ...")
    for col in METRICS:
        if col not in df.columns:
            print(f"⚠️ Column '{col}' not found, skipping.")
            continue

        if col == "Age":
            df["Age"] = df["Age"].fillna("0").astype(str)
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    print("✅ Columns sanitized.")

    # Ensure 'Player' column exists
    if "Player" not in df.columns:
        raise KeyError("❌ Input data must contain a 'Player' column.")

    # Compute Top-3 highest and lowest for each metric
    print("📊 Computing Top-3 for each metric ...")
    lines = ["Top‑3 HIGHEST & LOWEST for each metric:\n"]

    for metric in METRICS:
        if metric not in df.columns:
            continue

        lines.append(f"--- Metric: {metric} ---")
        valid = df[metric].notna()
        if valid.sum() < 3:
            lines.append(f"⚠️ Not enough valid data for '{metric}'.\n")
            continue

        sub = df.loc[valid, ["Player", metric]]

        if metric == "Age":
            high = sub.sort_values(by=metric, ascending=False, key=lambda s: s.str.lower()).head(3)
            low = sub.sort_values(by=metric, ascending=True, key=lambda s: s.str.lower()).head(3)
        else:
            high = sub.nlargest(3, metric)
            low = sub.nsmallest(3, metric)

        lines.append("Top‑3 Highest:")
        lines.extend(high.to_string(index=False).splitlines())
        lines.append("\nTop‑3 Lowest:")
        lines.extend(low.to_string(index=False).splitlines())
        lines.append("-" * 50)
        lines.append("")

    # Write the results to an output file
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Saved Top‑3 report to '{OUTPUT}'")
    print("🎉 Process complete.")

except FileNotFoundError:
    print(f"❌ File not found: {INPUT}")
except Exception as e:
    print(f"❌ Error: {e}")
