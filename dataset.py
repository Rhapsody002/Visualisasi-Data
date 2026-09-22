import matplotlib.pyplot as plt
import pandas as pd

path = r"C:\Works\Semester 5\Statistika\Dzaky.xlsx"
dataraw = pd.read_excel(path)
print("--- DATA RAW ---")
print(dataraw.head())

grade_order = ["A", "AB", "B", "BC", "C", "D"]
dataraw["Grade"] = pd.Categorical(
    dataraw["Grade"], categories=grade_order, ordered=True
)

# Tabel Frekuensi
datafrq = pd.crosstab(index=dataraw["Grade"], columns="Frekuensi")
print("\n--- TABEL FREKUENSI GRADE ---")
print(datafrq)

# ================================Statistika Deskriptif===================================
dataraw["Final Score"] = pd.to_numeric(
    dataraw["Final Score"], errors="coerce"
)
dt = dataraw["Final Score"]

stats_dict = {
    "Jumlah Data (Count)": len(dt),
    "Rata-rata (Mean)": dt.mean(),
    "Standar Deviasi (Std)": dt.std(),
    "Nilai Minimum (Min)": dt.min(),
    "Kuartil 1 (Q1 - 25%)": dt.quantile(0.25),
    "Median (Q2 - 50%)": dt.median(),
    "Kuartil 3 (Q3 - 75%)": dt.quantile(0.75),
    "Nilai Maksimum (Max)": dt.max(),
    "Standard Error (SE)": dt.sem(),
    "Modus (Mode)": dt.mode().iloc[0],
    "Varians (Variance)": dt.var(),
    "Jangkauan (Range)": dt.max() - dt.min(),
    "Kemiringan (Skewness)": dt.skew(),
    "Keruncingan (Kurtosis)": dt.kurtosis(),
}

stats_df = pd.DataFrame(
    list(stats_dict.items()), columns=["Parameter Statistik", "Nilai"]
)
stats_df["Nilai"] = stats_df["Nilai"].round(4)

print("\n" + "=" * 50)
print("       RINGKASAN STATISTIKA DESKRIPTIF        ")
print("=" * 50)
print(stats_df.to_string(index=False))
print("=" * 50)

# ================================Visualisasi Data===================================
plt.style.use(
    "seaborn-v0_8-whitegrid"
    if "seaborn-v0_8-whitegrid" in plt.style.available
    else "default"
)
fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
fig.suptitle(
    "DASHBOARD ANALISIS DISTRIBUSI GRADE MAHASISWA",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)

colors = ["#2b5c8f", "#4682b4", "#5f9ea0", "#87ceeb", "#d95f02", "#a60000"]

# Line Chart
axes[0].plot(
    datafrq.index,
    datafrq["Frekuensi"],
    color="#2b5c8f",
    linewidth=2.5,
    zorder=1,
)
axes[0].fill_between(
    datafrq.index, datafrq["Frekuensi"], color="#2b5c8f", alpha=0.12
)
axes[0].scatter(
    datafrq.index,
    datafrq["Frekuensi"],
    color=colors,
    s=90,
    edgecolors="white",
    linewidth=1.5,
    zorder=2,
)
for idx, (grade, val) in enumerate(zip(datafrq.index, datafrq["Frekuensi"])):
    axes[0].annotate(
        f"{val}",
        (grade, val),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontweight="bold",
        fontsize=9,
        color=colors[idx],
    )
axes[0].set_title("1. Tren Frekuensi Nilai", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Grade")
axes[0].set_ylabel("Jumlah Mahasiswa")
axes[0].set_ylim(0, max(datafrq["Frekuensi"]) + 2)
axes[0].grid(True, linestyle=":", alpha=0.6)

# Bar Chart
bars = axes[1].barh(
    datafrq.index,
    datafrq["Frekuensi"],
    color=colors,
    edgecolor="black",
    alpha=0.85,
)
axes[1].set_title(
    "2. Distribusi Frekuensi (Horizontal)", fontsize=11, fontweight="bold"
)
axes[1].set_xlabel("Jumlah Mahasiswa")
axes[1].set_ylabel("Grade")
axes[1].invert_yaxis()
axes[1].grid(axis="x", linestyle=":", alpha=0.6)

for bar in bars:
    width = bar.get_width()
    axes[1].text(
        width + 0.2,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width)} mhs",
        ha="left",
        va="center",
        fontweight="bold",
        fontsize=9,
    )

# Donut Chart
wedges, texts, autotexts = axes[2].pie(
    datafrq["Frekuensi"],
    labels=datafrq.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    pctdistance=0.75,
    wedgeprops={"width": 0.4, "edgecolor": "white", "linewidth": 2},
)
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontweight("bold")
axes[2].set_title(
    "3. Proporsi Grade (Donut Chart)", fontsize=11, fontweight="bold"
)

# Ditaruh paling akhir
plt.tight_layout()
plt.show()