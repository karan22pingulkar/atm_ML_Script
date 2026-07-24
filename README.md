# 🏦 Automated ATM Cash Dispense Forecasting Engine

An end-to-end Machine Learning pipeline built using **Python**, **LightGBM**, and **PyArrow Parquet** to predict daily ATM cash requirements across multiple forecast horizons (**Day +1, Day +3, Day +7**).

The solution enables banking operations and cash logistics teams to optimize ATM replenishment planning, reduce idle cash holdings, and minimize cash-out events by learning historical withdrawal behavior along with salary cycles, weekends, and regional holiday effects.

---

# 📌 Features

- 🚀 **High-Performance Data Pipeline**
  - Converts raw multi-sheet Excel files into compressed Parquet datasets for significantly faster processing.

- 📈 **Advanced Feature Engineering**
  - Salary period indicators
  - Weekend & long-weekend detection
  - Holiday classification
  - Festival impact modeling
  - ATM-wise lag features
  - Rolling average features

- 🤖 **Machine Learning Forecasting**
  - LightGBM regression models
  - Independent models for:
    - Day +1 Forecast
    - Day +3 Forecast
    - Day +7 Forecast

- 📊 **Production Ready Reports**
  - Generates formatted Excel reports
  - Separate worksheets for each forecast horizon
  - Supports very large datasets

---

# 📁 Repository Structure

```text
.
├── data/
│   └── raw_atm_data.xlsx                 # Raw transaction workbook
│
├── processed/
│   ├── transactions.parquet              # Historical ATM transactions
│   └── holiday_master.parquet            # State-wise holiday calendar
│
├── outputs/
│   └── atm_predictions_output.xlsx       # Prediction report
│
├── preprocess.py                         # Excel → Parquet converter
├── forecast_engine.py                    # Model training & forecasting
├── requirements.txt                      # Python dependencies
└── README.md
```

---

# ⚙️ Data Input Formats

## 1. Daily Transactions (`processed/transactions.parquet`)

Your historical transaction dataset must contain the following schema.

| Column Name | Data Type | Example | Description |
|------------|-----------|----------|-------------|
| `atm_id` | String | ATM_1042 | Unique ATM identifier |
| `date` | Date / String | 2026-03-15 | Transaction date (YYYY-MM-DD) |
| `dispense` | Float / Integer | 1450000 | Total cash dispensed (Target Variable) |
| `state` | String | MAHARASHTRA | ATM state used for regional holiday mapping |

---

## 2. Holiday Master (`processed/holiday_master.parquet`)

This dataset contains state-level holiday information.

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

cd atm-dispense-forecasting
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### Sample `requirements.txt`

```text
pandas>=2.0.0
numpy
lightgbm>=4.0.0
pyarrow
xlsxwriter
```

---

## 3. Data Preprocessing

Convert raw Excel transaction logs into optimized Parquet datasets.

```bash
python preprocess.py
```

This step creates:

```
processed/
    transactions.parquet
    holiday_master.parquet
```

---

## 4. Train Models & Generate Forecasts

Run the forecasting engine.

```bash
python forecast_engine.py
```

The pipeline automatically:

- Loads historical transactions
- Loads holiday master
- Performs feature engineering
- Trains LightGBM models
- Generates forecasts for Day +1, Day +3, and Day +7
- Exports formatted Excel reports

---

# 📊 Output Excel Format

The prediction report is generated at:

```
outputs/
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

Model parameters can be modified inside:

```
forecast_engine.py
```

Typical LightGBM parameters include:

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
- Number of trees
- Maximum tree depth
- Number of leaves
- Early stopping
- Feature selection
- Validation strategy
- Forecast horizons

---

# 🔄 Forecast Workflow

```text
Raw Excel Files
        │
        ▼
preprocess.py
        │
        ▼
transactions.parquet
holiday_master.parquet
        │
        ▼
Feature Engineering
        │
        ▼
LightGBM Training
        │
        ▼
Day +1 Model
Day +3 Model
Day +7 Model
        │
        ▼
Excel Forecast Report
```

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- LightGBM
- PyArrow
- XlsxWriter

---

# 📈 Forecast Features

The model incorporates several predictive signals, including:

- Historical cash dispense trends
- ATM-level lag features
- Rolling averages
- Weekend indicators
- Long weekend detection
- Salary period effects
- National holidays
- State holidays
- Festival periods
- Calendar-based temporal features

---

# 🎯 Use Cases

- ATM cash replenishment optimization
- Cash logistics planning
- Currency inventory management
- Regional demand forecasting
- Banking operations analytics
- Treasury planning

---

# 📄 License

This project is intended for educational, research, and enterprise banking analytics applications. Modify and extend it according to your organization's forecasting requirements.
