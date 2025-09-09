"""Generate synthetic sales orders for a date range."""
import argparse
import numpy as np
import pandas as pd

CATEGORIES = ["Electronics", "Home", "Beauty", "Toys", "Grocery"]

def make_dates(start, end):
    return pd.date_range(start=start, end=end, freq="D")

def simulate_day(d, base_orders=120, trend_per_month=0.01, season_amp=0.2, rng=None):
    """Return a list of rows for a single day."""
    # Seasonality by month and a mild upward trend over time
    month = d.month
    season = 1 + season_amp * np.sin(2 * np.pi * (month / 12.0))
    months_since_start = (d.year - 2000) * 12 + d.month
    trend = 1 + trend_per_month * (months_since_start % 120)

    lam = base_orders * season * trend
    orders = max(0, rng.poisson(lam=lam))

    rows = []
    for _ in range(orders):
        order_id = f"{d.strftime('%Y%m%d')}-{rng.integers(100000, 999999)}"
        customer_id = rng.integers(1000, 9999)
        category = rng.choice(CATEGORIES, p=[0.28, 0.22, 0.18, 0.16, 0.16])

        # Category-based price ranges
        base_price = {
            "Electronics": rng.uniform(40, 300),
            "Home": rng.uniform(10, 120),
            "Beauty": rng.uniform(5, 60),
            "Toys": rng.uniform(5, 80),
            "Grocery": rng.uniform(1, 30),
        }[category]

        # Occasional promotions/discounts
        discount_factor = rng.choice([1.0, 0.9, 0.8, 0.7], p=[0.7, 0.15, 0.1, 0.05])
        price = round(base_price * discount_factor, 2)
        quantity = int(max(1, rng.poisson(lam=1.8)))
        revenue = round(price * quantity, 2)

        rows.append([d.date(), order_id, customer_id, category, price, quantity, revenue])
    return rows

def maybe_inject_noise(df, rng, frac_missing=0.002, frac_outliers=0.001):
    """Inject a small amount of missing values and outliers for realism."""
    n = len(df)
    if n == 0:
        return df

    # Missing prices
    miss_idx = rng.choice(n, size=int(n * frac_missing), replace=False)
    df.loc[miss_idx, "price"] = np.nan

    # Outlier quantities
    out_idx = rng.choice(n, size=int(n * frac_outliers), replace=False)
    df.loc[out_idx, "quantity"] = df.loc[out_idx, "quantity"] * rng.integers(8, 20)
    df.loc[out_idx, "revenue"] = df.loc[out_idx, "price"] * df.loc[out_idx, "quantity"]
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=str, required=True)
    ap.add_argument("--end", type=str, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="data/sales.csv")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    dates = make_dates(args.start, args.end)

    all_rows = []
    for d in dates:
        all_rows.extend(simulate_day(d, rng=rng))

    df = pd.DataFrame(
        all_rows,
        columns=["date", "order_id", "customer_id", "category", "price", "quantity", "revenue"],
    )
    df = maybe_inject_noise(df, rng)
    df["date"] = pd.to_datetime(df["date"])
    df.to_csv(args.out, index=False)
    print(f"[OK] wrote {args.out} with {len(df):,} rows")

if __name__ == "__main__":
    main()
