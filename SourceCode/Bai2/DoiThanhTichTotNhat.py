import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import os

def show_popup(title, message, image_path=None, wait_ms=5000):
    popup = tk.Tk()
    popup.title(title)
    popup.geometry("520x550")
    popup.configure(bg="white")
    popup.after(wait_ms, popup.destroy)

    frame = tk.Frame(popup, bg="white")
    frame.pack(expand=True, fill="both")

    if image_path and os.path.exists(image_path):
        img = Image.open(image_path).resize((300, 300))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(frame, image=logo, bg="white")
        logo_label.image = logo
        logo_label.pack(pady=15)
    else:
        tk.Label(frame, text="(Logo not found)", font=("Arial", 12), bg="white").pack(pady=15)

    label = tk.Label(frame, text=message, font=("Arial", 16, "bold"), bg="white")
    label.pack(pady=15)

    popup.mainloop()

df = pd.read_csv("results.csv")
df.replace("N/a", 0.0, inplace=True)
df.fillna(0.0, inplace=True)

attack_cols = ["Gls", "Ast", "xG", "xAG", "PrgPs", "SCA", "GCA"]
defense_cols = ["Tkl", "Blocks", "Int", "GA90", "Save%", "CS%"]
all_stat_cols = attack_cols + defense_cols

for col in all_stat_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

team_stats = df.groupby("Squad")[all_stat_cols].mean()

for col in all_stat_cols:
    min_val = team_stats[col].min()
    max_val = team_stats[col].max()
    if max_val > min_val:
        team_stats[col] = (team_stats[col] - min_val) / (max_val - min_val)
    else:
        team_stats[col] = 0.0

team_stats["TeamScore"] = (
    team_stats[attack_cols].mean(axis=1) * 0.6 +
    team_stats[defense_cols].mean(axis=1) * 0.4
)

best_team = team_stats["TeamScore"].idxmax()
best_score = team_stats["TeamScore"].max()

logo_path = f"logo/{best_team}.png"
if not os.path.exists(logo_path):
    logo_path = f"logo/{best_team}.jpg"
if not os.path.exists(logo_path):
    logo_path = None

show_popup(
    "🏆 Best Performing Team",
    f"🔥 {best_team} is performing the best\nin the 2024–2025 Premier League season!\n🏅 Score: {best_score:.2f}",
    logo_path,
    wait_ms=5000
)
