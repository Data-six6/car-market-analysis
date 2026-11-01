# Used Car Market Analysis

End-to-end analysis of a used-car listings dataset: data quality assessment,
cleaning, exploratory data analysis, SQL business questions, and a Power BI
dashboard.

## Project structure

```
used-car-market-analysis/
├── data/
│   ├── raw/original_dataset.csv
│   └── processed/used_cars_cleaned.csv
├── notebooks/exploratory_data_analysis.ipynb
├── scripts/
│   ├── data_quality.py
│   └── data_cleaning.py
├── sql/business_analysis.sql
├── powerbi/used_car_dashboard.pbix
├── outputs/
│   ├── charts/
│   ├── business_insights.md
│   └── data_quality_report.md
├── screenshots/
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place the source dataset at `data/raw/original_dataset.csv`.

## Workflow

1. Assess data quality:
   ```bash
   python scripts/data_quality.py
   ```
2. Clean the dataset:
   ```bash
   python scripts/data_cleaning.py
   ```
3. Run the exploratory notebook:
   ```bash
   jupyter notebook notebooks/exploratory_data_analysis.ipynb
   ```
4. Load `data/processed/used_cars_cleaned.csv` into your SQL database and run
   `sql/business_analysis.sql`.
5. Connect Power BI to the cleaned CSV and build/save
   `powerbi/used_car_dashboard.pbix`.

## Deliverables

- `outputs/data_quality_report.md` — completeness, uniqueness, and validity findings.
- `outputs/business_insights.md` — pricing, vehicle, and seller insights.
- `outputs/charts/` — exported analysis figures.
- `screenshots/` — dashboard snapshots.

## License

MIT — see [LICENSE](LICENSE).
