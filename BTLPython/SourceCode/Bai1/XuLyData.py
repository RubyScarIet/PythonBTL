import pandas as pd

FILE_LIST = [
    "stats_standard.csv",
    "stats_shooting.csv",
    "stats_possession.csv",
    "stats_passing.csv",
    "stats_misc.csv",
    "stats_keeper.csv",
    "stats_gca.csv",
    "stats_defense.csv",
]

COLUMN_RENAME_MAPPING = [
    ("stats_misc.csv","stats_misc.csv","Lost","Lostm"),
    ("stats_standard.csv","stats_standard.csv","PrgC","PrgCs"),
    ("stats_standard.csv","stats_standard.csv","PrgP", "PrgPs"),
    ("stats_standard.csv","stats_standard.csv","PrgR", "PrgRs"),
    ("stats_passing.csv", "stats_passing.csv", "PrgP","PrgPp"),
    ("stats_passing.csv", "stats_passing.csv", "1/3", "Pto1/3"),
    ("stats_defense.csv", "stats_defense.csv", "Lost","Lostd"),
    ("stats_defense.csv", "stats_defense.csv", "Att","Attd"),
    ("stats_possession.csv","stats_possession.csv","Att","Attp"),
    ("stats_possession.csv","stats_possession.csv","PrgC","PrgCp"),
    ("stats_possession.csv","stats_possession.csv","1/3","Cto1/3"),
    ("stats_possession.csv","stats_possession.csv","PrgR","PrgRp"),
    ("stats_possession.csv","stats_possession.csv","Lost","Lostm"),
]

def clean_minutes_column(df: pd.DataFrame) -> pd.DataFrame:
    if 'Min' in df.columns:
        df['Min'] = (
            df['Min']
            .astype(str)
            .str.replace(",", "")
            .str.strip()
            .pipe(pd.to_numeric, errors='coerce')
        )
    return df

def clean_duplicate_headers(file_list, keyword='Rk'):
   
    print("\n🔄 CLEANING DUPLICATE HEADERS")
    for path in file_list:
        try:
            raw = pd.read_csv(path, header=None, encoding='utf-8-sig')
            if raw.empty:
                print(f"   ⚠️ {path} is empty — skipped")
                continue

            mask = ~raw.iloc[:,0].astype(str).str.startswith(keyword)
            mask.iloc[0] = True
            cleaned = raw[mask]

            cleaned.to_csv(path, index=False, header=False, encoding='utf-8-sig')
            print(f"   ✅ {path}: kept {len(cleaned)} rows")
        except Exception as e:
            print(f"   ❌ Error cleaning {path}: {e}")

def sort_and_renumber(file_list, sort_column='Player'):
  
    print("\n🔢 SORTING & RENUMBERING")
    for path in file_list:
        try:
            df = pd.read_csv(path, encoding='utf-8-sig')
            if sort_column not in df.columns:
                print(f"   ⚠️ {path} has no '{sort_column}' column — skipped")
                continue

            df = df.sort_values(sort_column)
            if 'Rk' in df.columns:
                df['Rk'] = range(1, len(df)+1)

            df.to_csv(path, index=False, encoding='utf-8-sig')
            print(f"   ✅ Sorted {path}")
        except Exception as e:
            print(f"   ❌ Error sorting {path}: {e}")

def rename_columns(mappings):
    
    print("\n✏️ RENAMING COLUMNS")
    for inp, out, old, new in mappings:
        try:
            df = pd.read_csv(inp, encoding='utf-8-sig')
            if df.empty:
                print(f"   ⚠️ {inp} is empty — skipped")
                continue

            if old not in df.columns:
                print(f"   ⚠️ '{old}' not found in {inp} — skipped")
                continue

            df = df.rename(columns={old: new})
            df.to_csv(out, index=False, encoding='utf-8-sig')
            print(f"   ✅ {inp}: {old} → {new}")
        except Exception as e:
            print(f"   ❌ Error renaming in {inp}: {e}")

def normalize_pos_column(df: pd.DataFrame) -> pd.DataFrame:
    
    if 'Pos' in df.columns:
        df['Pos'] = (
            df['Pos']
            .astype(str)
            .str.replace('"', '')  
            .str.replace(',', '-')  
        )
    return df
