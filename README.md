# 🏦 Automated ATM Cash Dispense Forecasting Engine

An end-to-end Machine Learning pipeline built using **Python**, **LightGBM**, and **PyArrow Parquet** to predict daily ATM cash requirements across multiple forecast horizons (**Day +1, Day +3, Day +7**).

The solution enables banking operations and cash logistics teams to optimize ATM replenishment planning, reduce idle cash holdings, and minimize cash-out events by learning historical withdrawal behavior along with salary cycles, weekends, and regional holiday effects.

> **Project Status**
>
> This project is currently under active development.
>
> ✅ **Working Scripts**
> - `convert_to_parquet.py`
> - `v1 script.py`
>
> 🚧 **Work in Progress**
> - `train_and_predict.py`
> - `train_and_predictV2.py`
> - `convert_to_excel.py`
> - `excel_script.py`
> - Additional improvements for feature engineering and prediction accuracy are being developed and will be updated in future releases.

---

# 📌 Features

- 🚀 High-performance data preprocessing using Apache Parquet
- 📈 Advanced feature engineering
  - Salary period indicators
  - Weekend & long-weekend detection
  - Holiday impact modeling
  - Festival identification
  - Rolling statistics
  - Historical lag features
- 🤖 LightGBM-based forecasting
- 📊 Automated Excel prediction reports
- ⚡ Optimized for large transaction datasets

---

# 📁 Repository Structure

```text
ATM_PREDICTION/
│
├── atm_ML_Script/
│   │
│   ├── data/
│   │   ├── raw/                     # Place raw Excel transaction files here
│   │   ├── processed/               # Generated Parquet datasets
│   │   └── outputs/                 # Prediction reports
│   │
│   ├── convert_to_parquet.py        # ✅ Converts Excel to Parquet
│   ├── v1 script.py                 # ✅ Main forecasting pipeline
│   │
│   ├── train_and_predict.py         # 🚧 Under development
│   ├── train_and_predictV2.py       # 🚧 Under development
│   ├── convert_to_excel.py          # 🚧 Under development
│   ├── excel_script.py              # 🚧 Under development
│   ├── holiday.py
│   └── requirements.txt
│
├── venv/
├── .gitignore
└── README.md
```

---

# ⚙️ Data Input Formats

## 1. Daily Transactions (`processed/transactions.parquet`)

The transaction dataset should contain the following schema.

| Column Name | Data Type | Example | Description |
|------------|-----------|----------|-------------|
| `atm_id` | String | ATM_1042 | Unique ATM identifier |
| `date` | Date / String | 2026-03-15 | Transaction date (YYYY-MM-DD) |
| `dispense` | Float / Integer | 1450000 | Total cash dispensed (Target Variable) |
| `state` | String | MAHARASHTRA | ATM state for regional holiday mapping |

---

## 2. Holiday Master (`processed/holiday_master.parquet`)

The holiday master dataset should contain:

| Column Name | Data Type | Example | Description |
|------------|-----------|----------|-------------|
| `date` | Date / String | 2026-11-08 | Holiday date |
| `state` | String | MAHARASHTRA | Applicable state |
| `holiday_name` | String | Diwali Laxmi Pujan | Holiday description |

---

# 🚀 Quickstart Guide

## 1. Clone Repository

```bash
git clone https://github.com/your-username/atm-dispense-forecasting.git

cd ATM_PREDICTION
```

---

## 2. Install Dependencies

```bash
pip install -r atm_ML_Script/requirements.txt
```

### Sample requirements.txt

```text
pandas>=2.0.0
numpy
lightgbm>=4.0.0
pyarrow
xlsxwriter
openpyxl
```

---

# 📂 Preparing Input Data

Place your raw transaction Excel files inside:

```text
atm_ML_Script/
    data/
        raw/
```

The preprocessing script will automatically read the Excel files from this folder and generate optimized Parquet datasets.

---

# ⚡ Step 1: Convert Excel to Parquet

Run the preprocessing script.

```bash
python convert_to_parquet.py
```

This converts Excel workbooks into compressed Parquet files for significantly faster loading and lower memory usage.

Generated files:

```text
data/
    processed/
        transactions.parquet
        holiday_master.parquet
```

---

# 🤖 Step 2: Run the Forecasting Pipeline

After preprocessing completes successfully, execute the main forecasting pipeline.

```bash
python "v1 script.py"
```

The script automatically:

- Loads transaction history
- Loads holiday master
- Performs feature engineering
- Creates lag and rolling features
- Trains the forecasting model
- Predicts ATM cash dispense
- Generates Excel prediction reports

---

# 📊 Output Excel Format

Prediction reports are generated inside:

```text
data/
    outputs/
```

Example:

```text
atm_predictions_output.xlsx
```

The workbook contains separate worksheets for each prediction horizon.

| Worksheet | Description |
|-----------|-------------|
| 15-Aug-2026 | Next-Day Forecast |
| 17-Aug-2026 | 3-Day Forecast |
| 21-Aug-2026 | 7-Day Forecast |

---

## Sample Output

| atm_id | reference_date | is_salary_period | is_long_weekend | holiday_name | predicted_dispense_amount | forecast_for_date |
|---------|----------------|-----------------|----------------|---------------|---------------------------|------------------|
| ATM_1001 | 2026-08-14 | 0 | 1 | Regular Day | 1,250,000 | 15-Aug-2026 |
| ATM_1002 | 2026-08-14 | 0 | 1 | Independence Day | 890,000 | 15-Aug-2026 |

---

# 💡 Customizing Configuration

Model parameters can be modified inside the forecasting script (`v1 script.py`) or future versions (`train_and_predict.py` and `train_and_predictV2.py`) as development progresses.

Typical LightGBM configuration:

```python
LGBMRegressor(
    learning_rate=0.05,
    n_estimators=500,
    max_depth=8,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8
)
```

You can customize:

- Learning rate
- Number of estimators
- Tree depth
- Number of leaves
- Early stopping
- Feature engineering
- Validation strategy
- Forecast horizons

---

# 🔄 Project Workflow

```text
                 Raw ATM Excel Files
                         │
                         ▼
              data/raw/
                         │
                         ▼
          convert_to_parquet.py
                         │
                         ▼
      Optimized Parquet Datasets
      (transactions.parquet &
       holiday_master.parquet)
                         │
                         ▼
                v1 script.py
                         │
        Feature Engineering
                         │
                         ▼
           LightGBM Model Training
                         │
                         ▼
      Day +1 / Day +3 / Day +7 Forecasts
                         │
                         ▼
      Formatted Excel Prediction Report
                         │
                         ▼
              data/outputs/
```

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- LightGBM
- PyArrow
- OpenPyXL
- XlsxWriter

---

# 📈 Forecast Features

The forecasting model incorporates multiple predictive signals, including:

- Historical ATM dispense patterns
- ATM-specific lag features
- Rolling mean statistics
- Weekend indicators
- Long weekend detection
- Salary period effects
- National holidays
- State holidays
- Festival impacts
- Calendar-based temporal features

---

# 🚧 Development Roadmap

Current version focuses on establishing the complete preprocessing and forecasting pipeline.

Upcoming improvements include:

- Improved feature engineering
- Hyperparameter optimization
- Enhanced prediction accuracy
- Automated model evaluation
- Better Excel reporting
- Modular training pipeline
- Version 2 forecasting engine
- Performance optimizations

---

# 🎯 Use Cases

- ATM cash replenishment planning
- Cash logistics optimization
- Banking operations analytics
- Treasury planning
- Currency inventory management
- Regional cash demand forecasting

---

# 📄 License

This project is intended for educational, research, and enterprise banking analytics applications. Feel free to modify and extend it according to your organization's forecasting requirements.
