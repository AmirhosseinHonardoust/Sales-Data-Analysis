"""Run the sales analysis pipeline and export charts + KPIs."""
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_sales, clean_sales, kpis

def ensure_outdir(path: str):
    os.makedirs(path, exist_ok=True)

def plot_daily_revenue(df: pd.DataFrame, outdir: str):
    ser = df.groupby(df["date"].dt.to_period("D"))["revenue"].sum().to_timestamp()
    ax = ser.plot(figsize=(11, 4), title="Daily Revenue")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_daily_revenue.png"), dpi=160)
    plt.close(fig)

def plot_monthly_revenue(df: pd.DataFrame, outdir: str):
    ser = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().to_timestamp()
    ax = ser.plot(kind="bar", figsize=(11, 4), title="Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_monthly_revenue.png"), dpi=160)
    plt.close(fig)

def plot_category_share(df: pd.DataFrame, outdir: str):
    ser = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    ax = ser.plot(kind="bar", figsize=(8, 4), title="Revenue by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_category_revenue.png"), dpi=160)
    plt.close(fig)

def write_kpis_txt(k: dict, outdir: str):
    path = os.path.join(outdir, "kpis.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("=== KPIs ===\n")
        for key, val in k.items():
            f.write(f"{key}: {val}\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=str, required=True, help="path to sales.csv")
    ap.add_argument("--outdir", type=str, default="outputs")
    args = ap.parse_args()

    ensure_outdir(args.outdir)

    df = load_sales(args.input)
    df_clean = clean_sales(df)
    k = kpis(df_clean)

    plot_daily_revenue(df_clean, args.outdir)
    plot_monthly_revenue(df_clean, args.outdir)
    plot_category_share(df_clean, args.outdir)
    write_kpis_txt(k, args.outdir)

    print("[OK] Analysis complete.")
    print(f"Outputs saved to: {args.outdir}")

if __name__ == "__main__":
    main()
