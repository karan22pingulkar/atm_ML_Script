# 🏦 Automated ATM Cash Dispense Forecasting Engine

An end-to-end Machine Learning pipeline built using **Python**, **LightGBM**, and **PyArrow Parquet** to predict daily ATM cash requirements across multi-day horizons (**Day +1, Day +3, Day +7**). 

This tool helps bank operations and cash logistics teams optimize cash replenishment schedules, minimize stockout risks, and reduce holding costs by modeling complex calendar patterns, salary cycles, and state-level holiday impacts.

---

## 📌 Features & Architecture Highlights

* **High-Performance Data Pipeline:** Converts raw multi-sheet Excel workbooks into fast, compressed `.parquet` files for optimized load times and low memory consumption.
* **Smart Feature Engineering:**
  * **Salary Dynamics:** Features for monthly paydays (1st–7th and 28th–31st) and Friday/weekend salary overlaps.
  * **Holiday & Event Classification:** Classifies holidays into **BANK**, **FESTIVAL**, **NATIONAL**, or **STATE** categories.
  * **Compound Behavioral Signals:** Generates indicators for long weekends, pre-holiday cash surges, and major cultural festivals (e.g., Diwali, Holi, Eid, Christmas).
  * **Rolling Temporal Lags:** Lags (1, 2, 7 days) and rolling mean averages (7, 14 days) captured on a per-ATM level.
* **Direct Multi-Horizon Forecasting:** Trains separate LightGBM regressors for specific operational target dates:
  * 🎯 **Next Day ($T+1$)**
  * 🎯 **Next 3 Days ($T+3$)**
  * 🎯 **Next Week ($T+7$)**
* **Production-Ready Excel Export:** Formats multi-tab prediction reports (`xlsxwriter`) with automated sheet chunking to stay safely within Excel limits (1M+ rows per sheet).

---

## 📁 Repository Structure

```text
.
├── data/
│   └── raw_atm_data.xlsx         # Raw multi-sheet Excel input files
├── processed/
│   ├── transactions.parquet      # Structured transaction history
│   └── holiday_master.parquet    # State-wise holiday calendar master
├── outputs/
│   └── atm_predictions_output.xlsx # Formatted Multi-Horizon Forecasts
├── preprocess.py                 # Converter script: Excel -> Parquet
├── forecast_engine.py            # Main training & prediction script
├── requirements.txt              # Required dependencies
└── README.md                     # Project documentation
