"""Utility helpers for loading, cleaning, and KPIs."""
import pandas as pd

def load_sales(path: str) -> pd.DataFrame:
    """Load CSV and parse the 'date' column."""
    df = pd.read_csv(path, parse_dates=["date"])
    return df

def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: drop dup orders, impute missing prices by category median,
    recompute revenue, and remove impossible rows."""
    df = df.drop_duplicates(subset=["order_id"])
    df["price"] = df.groupby("category")["price"].transform(lambda s: s.fillna(s.median()))
    df["revenue"] = (df["price"] * df["quantity"]).round(2)
    df = df[(df["quantity"] > 0) & (df["price"] > 0)]
    return df

def kpis(df: pd.DataFrame) -> dict:
    """Compute summary metrics and series stats."""
    daily = df.groupby(df["date"].dt.to_period("D"))["revenue"].sum().to_timestamp()
    monthly = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().to_timestamp()

    avg_basket = df["revenue"].mean()
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_id"].nunique()
    total_revenue = df["revenue"].sum()

    if len(monthly) >= 2:
        growth = (monthly.iloc[-1] - monthly.iloc[-2]) / max(1e-9, monthly.iloc[-2])
    else:
        growth = 0.0

    return {
        "total_revenue": float(total_revenue),
        "total_orders": int(total_orders),
        "total_customers": int(total_customers),
        "avg_basket": float(avg_basket),
        "last_month_revenue": float(monthly.iloc[-1]) if len(monthly) else 0.0,
        "mom_growth": float(growth),
        "daily_series_points": int(len(daily)),
        "monthly_series_points": int(len(monthly)),
    }
