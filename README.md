# 🏦 Automated ATM Cash Dispense Forecasting Engine

An end-to-end Machine Learning pipeline built using **Python**, **LightGBM**, and **PyArrow Parquet** to predict daily ATM cash requirements across multiple forecast horizons (**Day +1, Day +3, Day +7**).

The solution helps banking operations and cash management teams optimize ATM cash replenishment planning by learning historical withdrawal patterns, salary cycles, weekends, holidays, and regional events.

---

# 🚀 Project Status

This project is currently under active development.

## ✅ Working Scripts

- `convert_to_parquet.py`
- `v1 script.py`

## 🚧 Work in Progress

- `train_and_predict.py`
- `train_and_predictV2.py`

Future updates will focus on:

- Improved feature engineering
- Better prediction accuracy
- Advanced model tuning
- Additional forecasting improvements

---

# 📌 Features

- 🚀 High-performance data preprocessing using Parquet format
- 📊 Conversion of Excel transaction data into optimized datasets
- 🤖 LightGBM-based ATM cash forecasting
- 📈 Multi-horizon forecasting capability:
  - Day +1 Prediction
  - Day +3 Prediction
  - Day +7 Prediction

- 🧠 Feature engineering:
  - Salary period detection
  - Weekend impact
  - Long weekend detection
  - Holiday impact
  - Historical transaction patterns
  - Lag features
  - Rolling statistics

- 📄 Automated Excel forecast reports

---

# 📁 Repository Structure

```text
ATM_PREDICTION/
│
├── atm_ML_Script/
│   │
│   ├── data/
│   │   │
│   │   ├── transactions.xlsx          # Raw ATM transaction input file
│   │   ├── holiday_master.xlsx        # Holiday master input file
│   │   │
│   │   ├── raw/                       # Auto-used/created folder for raw files
│   │   │
│   │   ├── processed/                 # Auto-created by convert_to_parquet.py
│   │   │   ├── transactions.parquet
│   │   │   └── holiday_master.parquet
│   │   │
│   │   └── outputs/                   # Auto-created by prediction script
│   │       └── atm_predictions_output.xlsx
│   │
│   ├── convert_to_parquet.py          # ✅ Excel to Parquet conversion
│   ├── v1 script.py                   # ✅ Main forecasting pipeline
│   │
│   ├── train_and_predict.py           # 🚧 Under development
│   ├── train_and_predictV2.py         # 🚧 Under development
│   ├── holiday.py
│   └── requirements.txt
│
├── venv/
├── .gitignore
├── .gitmodules
└── README.md
```

> **Note:**  
> The `processed` and `outputs` folders are generated automatically by the scripts if they do not exist.

---

# ⚙️ Data Input Format

## 1. ATM Transaction Data

Input file:

```
data/transactions.xlsx
```

Required columns:

| Column Name | Data Type | Example | Description |
|-------------|-----------|---------|-------------|
| atm_id | String | ATM_1042 | Unique ATM identifier |
| date | Date/String | 2026-03-15 | Transaction date |
| dispense | Float/Integer | 1450000 | Total cash dispensed |
| state | String | MAHARASHTRA | State location |

`dispense` is the prediction target variable.

---

## 2. Holiday Master Data

Input file:

```
data/holiday_master.xlsx
```

Required columns:

| Column Name | Data Type | Example | Description |
|-------------|-----------|---------|-------------|
| date | Date/String | 2026-11-08 | Holiday date |
| state | String | MAHARASHTRA | Applicable state |
| holiday_name | String | Diwali Laxmi Pujan | Holiday description |

---

# 🚀 Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/your-username/atm-dispense-forecasting.git

cd ATM_PREDICTION
```

---

## 2. Install Dependencies

Navigate to project folder:

```bash
cd atm_ML_Script
```

Install requirements:

```bash
pip install -r requirements.txt
```

Example requirements:

```text
pandas>=2.0.0
numpy
lightgbm>=4.0.0
pyarrow
xlsxwriter
openpyxl
```

---

# 🔄 Execution Workflow

The complete pipeline works in two steps:

```
Excel Input Files
        |
        |
        v
convert_to_parquet.py
        |
        |
        v
Parquet Files
        |
        |
        v
v1 script.py
        |
        |
        v
ATM Forecast Output
```

---

# ⚡ Step 1: Convert Excel Files to Parquet

Place input Excel files inside:

```
atm_ML_Script/data/
```

Example:

```
data/
│
├── transactions.xlsx
└── holiday_master.xlsx
```

Run:

```bash
python convert_to_parquet.py
```

The script will:

- Read Excel files
- Convert them into Parquet format
- Create the processed folder automatically
- Save optimized datasets

Generated files:

```
data/
└── processed/

    ├── transactions.parquet
    └── holiday_master.parquet
```

---

# 🤖 Step 2: Run ATM Forecasting Model

Run:

```bash
python "v1 script.py"
```

The script performs:

- Loading Parquet datasets
- Feature engineering
- Historical pattern analysis
- Model training
- ATM dispense prediction
- Excel report generation

If the output folder does not exist, it will be created automatically.

---

# 📊 Output Format

Generated output:

```
data/outputs/atm_predictions_output.xlsx
```

The Excel workbook contains forecast results.

Example forecast sheets:

| Sheet | Forecast |
|-------|----------|
| 15-Aug-2026 | Next Day Forecast |
| 17-Aug-2026 | 3 Day Forecast |
| 21-Aug-2026 | 7 Day Forecast |

---

## Sample Output

| atm_id | reference_date | is_salary_period | is_long_weekend | holiday_name | predicted_dispense_amount | forecast_for_date |
|--------|---------------|-----------------|----------------|--------------|---------------------------|------------------|
| ATM_1001 | 2026-08-14 | 0 | 1 | Regular Day | 1250000 | 2026-08-15 |
| ATM_1002 | 2026-08-14 | 0 | 1 | Independence Day | 890000 | 2026-08-15 |

---

# 💡 Model Configuration

The LightGBM model configuration can be modified inside:

```
v1 script.py
```

Example:

```python
LGBMRegressor(
    learning_rate=0.05,
    n_estimators=500,
    max_depth=8,
    num_leaves=31
)
```

Parameters that can be tuned:

- Learning rate
- Number of estimators
- Tree depth
- Number of leaves
- Feature selection
- Validation strategy

---

# 🔄 Detailed Workflow

```
                 transactions.xlsx
                 holiday_master.xlsx
                         |
                         |
                         v
                  data folder
                         |
                         |
                         v
             convert_to_parquet.py
                         |
                         |
                         v
        processed/transactions.parquet
        processed/holiday_master.parquet
                         |
                         |
                         v
                  v1 script.py
                         |
                         |
                         v
             Feature Engineering
                         |
                         |
                         v
              LightGBM Forecast Model
                         |
                         |
                         v
          Day +1 / Day +3 / Day +7 Forecast
                         |
                         |
                         v
              outputs/Excel Report
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

The model uses:

- Historical ATM withdrawal trends
- ATM-specific behavior
- Salary cycle impact
- Weekend behavior
- Long weekend effects
- Holiday effects
- State-level holiday mapping
- Lag-based features
- Rolling averages

---

# 🚧 Future Improvements

Planned enhancements:

- Advanced feature engineering
- Hyperparameter optimization
- Model evaluation framework
- Improved forecasting accuracy
- Automated model retraining
- Version 2 prediction engine
- Better reporting dashboard

---

# 🎯 Use Cases

- ATM cash replenishment planning
- Cash logistics optimization
- Banking operations analytics
- Treasury planning
- Regional cash demand forecasting
- Currency inventory management

---

# 📄 License

This project is intended for educational, research, and enterprise analytics applications.

Modify and extend according to your organization's requirements.
