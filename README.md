# Sales Data Analysis

Synthetic sales data analysis with Python. Generate realistic sales transactions, clean and validate data, compute KPIs, and visualize revenue trends by day, month, and category. Includes reproducible scripts and charts for portfolio demonstration. Simple end-to-end sales analytics: synthetic data generation, cleaning, KPIs, and charts.

---

## Features
- Generate synthetic daily orders
- Clean and validate data (deduplicate, impute, recompute revenue)
- Compute KPIs: daily/monthly revenue, average basket, growth rate
- Visualize revenue trends with Matplotlib
- Save outputs to the `outputs/` directory

---

## Project Structure
```
sales-data-analysis/
├─ README.md
├─ requirements.txt
├─ data/
│  └─ generate_sales.py
├─ src/
│  ├─ analyze_sales.py
│  └─ utils.py
└─ outputs/
   └─ figures & reports
```

---

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Generate Synthetic Data
```bash
python data/generate_sales.py --start 2023-01-01 --end 2024-12-31 --seed 42 --out data/sales.csv
```

---

## Run Analysis
```bash
python src/analyze_sales.py --input data/sales.csv --outdir outputs
```

The script produces KPIs and charts automatically.

**Outputs**
- `outputs/kpis.txt` – main KPIs
- `outputs/fig_daily_revenue.png`
- `outputs/fig_monthly_revenue.png`
- `outputs/fig_category_revenue.png`

---

## Sample Results

### Daily Revenue
<img width="1760" height="640" alt="fig_daily_revenue" src="https://github.com/user-attachments/assets/c8445fcf-103e-4f6a-9d27-f9fb72d06642" />

### Monthly Revenue
<img width="1760" height="640" alt="fig_monthly_revenue" src="https://github.com/user-attachments/assets/6f6014c5-c5b3-4aa9-bc73-5fa11aa69122" />

### Revenue by Category
<img width="1280" height="640" alt="fig_category_revenue" src="https://github.com/user-attachments/assets/7e49fd3f-7108-449a-b047-988c52dff030" />

---

## Data Schema
| column       | description                 |
|--------------|-----------------------------|
| date         | order date                  |
| order_id     | unique order identifier     |
| customer_id  | customer identifier         |
| category     | product category            |
| price        | unit price (after discount) |
| quantity     | order quantity              |
| revenue      | price * quantity            |
