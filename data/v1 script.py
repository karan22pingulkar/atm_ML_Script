import os
from pathlib import Path

import pandas as pd

# import numpy as np

import lightgbm as lgb

# import holidays

# from datetime import datetime


# ==========================================

# CONFIGURATION

# ==========================================

# COUNTRY_CODE = "IN"  # Replace with your country code (e.g., 'IN', 'US', 'GB')

# TARGET_YEARS = [2025, 2026]  # Years covering your historical + forecast windows

BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = RAW_DIR / "processed"
OUTPUT_DIR = RAW_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_EXCEL = OUTPUT_DIR / "atm_predictions_output.xlsx"


# ==========================================

# 1. FAST PARQUET LOADING & FEATURE ENGINEERING

# ==========================================


def classify_holiday(event):

    event = str(event).lower()

    if any(
        x in event
        for x in [
            "2nd sat",
            "4th sat",
            "annual closing",
            "financial year end",
            "closing day"
        ]
    ):
        return "BANK"

    elif any(
        x in event
        for x in [
            "holi",
            "eid",
            "ramzan",
            "bakri",
            "moharram",
            "pongal",
            "bihu",
            "navami",
            "mahashivratri",
            "good friday",
            "christmas",
            "diwali",
            "dussehra",
            "durga",
            "ganesh",
            "onam"
        ]
    ):
        return "FESTIVAL"

    elif any(
        x in event
        for x in [
            "republic day",
            "independence day",
            "gandhi jayanti"
        ]
    ):
        return "NATIONAL"

    return "STATE"


def load_and_engineer_data():

    print(">>> Loading fast Parquet data...")
    print("Base directory :", BASE_DIR)
    print("Processed path :", PROCESSED_DIR)
    print("Transactions exists :", os.path.exists(
        os.path.join(PROCESSED_DIR, "transactions.parquet")))
    print("Holiday exists :", os.path.exists(
        os.path.join(PROCESSED_DIR, "holiday_master.parquet")))
    print(PROCESSED_DIR)
    print((PROCESSED_DIR / "transactions.parquet").exists())
    print((PROCESSED_DIR / "holiday_master.parquet").exists())

    df_tx = pd.read_parquet(PROCESSED_DIR / "transactions.parquet")

    holiday_df = pd.read_parquet(PROCESSED_DIR / "holiday_master.parquet")

    # df_meta = pd.read_parquet("data/processed/atm_metadata.parquet")

    # Merge Transaction + Metadata

    # df = pd.merge(df_tx, df_meta, on="atm_id", how="left")
    df = df_tx.copy()

    #  Data type cleanup
    df["dispense"] = pd.to_numeric(df["dispense"], errors="coerce")
    # df["uptime_pct"] = pd.to_numeric(
    # df["uptime_pct"]
    #         .astype(str)
    #         .str.replace("%", "", regex=False),
    #     errors="coerce"
    # )

    # df["downtime_pct"] = pd.to_numeric(
    #     df["downtime_pct"]
    #         .astype(str)
    #         .str.replace("%", "", regex=False),
    #     errors="coerce"
    # )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["state"] = (
        df["state"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df = df.sort_values(by=["atm_id", "date"]).reset_index(drop=True)
    # Remove ATMs with 100% zero dispense history

    atm_total_dispense = df.groupby("atm_id")["dispense"].transform("sum")

    removed_atms = df.loc[
        atm_total_dispense == 0,
        "atm_id"
    ].nunique()

    df = df[atm_total_dispense > 0]

    print(
        f">>> Removed {removed_atms} ATM(s) "
        f"with 100% zero dispense history."
    )

    print(">>> Generating Compound Calendar, Salary & Holiday Features...")

    # Date Parts

    df["day_of_week"] = df["date"].dt.dayofweek  # Mon=0, Fri=4, Sat=5, Sun=6

    df["day_of_month"] = df["date"].dt.day

    df["month"] = df["date"].dt.month

    df["is_friday"] = (df["day_of_week"] == 4).astype(int)

    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Salary Logic (Primary: 1st-7th; Month-end: 28th-31st)

    df["is_salary_week"] = df["day_of_month"].between(1, 7).astype(int)

    df["is_monthend_salary"] = df["day_of_month"].between(28, 31).astype(int)

    df["is_salary_period"] = (df["is_salary_week"] | df["is_monthend_salary"]).astype(
        int
    )
    # ==========================================
# Holiday Master Merge
# ==========================================

    holiday_df["date"] = pd.to_datetime(
        holiday_df["date"]
    )

    holiday_df["state"] = (
        holiday_df["state"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    holiday_df["holiday_type"] = (
        holiday_df["holiday_name"]
        .apply(classify_holiday)
    )

    holiday_df["is_holiday"] = 1

    holiday_df["is_major_festival"] = (
        holiday_df["holiday_name"]
        .astype(str)
        .str.lower()
            .str.contains(
                "holi|diwali|eid|durga|dussehra|christmas|onam",
                na=False
        )
        .astype(int)
    )

    holiday_df = holiday_df[
        [
            "date",
            "state",
            "holiday_name",
            "holiday_type",
            "is_holiday",
            "is_major_festival"
        ]
    ].drop_duplicates()

    df = pd.merge(
        df,
        holiday_df,
        on=["date", "state"],
        how="left"
    )

    df["holiday_name"] = (
        df["holiday_name"]
        .fillna("Regular Day")
    )

    df["holiday_type"] = (
        df["holiday_type"]
        .fillna("NONE")
    )

    df["is_holiday"] = (
        df["is_holiday"]
        .fillna(0)
        .astype(int)
    )

    df["is_major_festival"] = (
        df["is_major_festival"]
        .fillna(0)
        .astype(int)
    )

    # Holidays & Festivals

    # country_holidays = holidays.country_holidays(COUNTRY_CODE, years=TARGET_YEARS)

    # df["is_holiday"] = df["date"].apply(lambda d: 1 if d in country_holidays else 0)

    # df["holiday_name"] = (
    #     df["date"]
    #     .apply(lambda d: country_holidays.get(d, "Regular Day"))
    #     .astype("category")
    # )

    # Pre-Holiday surge flag (1 day BEFORE holiday)

    df["is_pre_holiday"] = (
        df.groupby("atm_id")["is_holiday"].shift(-1).fillna(0).astype(int)
    )

    # Long Weekend Logic (Consecutive blocks of >= 3 days off)

    is_off_day = (df["is_weekend"] == 1) | (df["is_holiday"] == 1)

    off_block_id = (is_off_day != is_off_day.shift(1)).cumsum()

    df["off_block_length"] = df.groupby(["atm_id", off_block_id])["date"].transform(
        "count"
    )

    df["is_long_weekend"] = ((is_off_day) & (
        df["off_block_length"] >= 3)).astype(int)

    df.drop(columns=["off_block_length"], inplace=True)

    # High-Impact Compound Event Interactions

    df["is_salary_friday"] = (
        (df["is_salary_period"] == 1) & (df["is_friday"] == 1)
    ).astype(int)

    df["is_salary_weekend"] = (
        (df["is_salary_period"] == 1) & (df["is_weekend"] == 1)
    ).astype(int)

    df["is_salary_weekend_holiday"] = (
        (df["is_salary_period"] == 1)
        & ((df["is_weekend"] == 1) | (df["is_friday"] == 1))
        & (df["is_holiday"] == 1)
    ).astype(int)

    df["is_salary_long_weekend"] = (
        (df["is_salary_period"] == 1) & (df["is_long_weekend"] == 1)
    ).astype(int)

    # Lags and Rolling Means

    grouped = df.groupby("atm_id")["dispense"]

    df["dispense_lag_1"] = grouped.shift(1)

    df["dispense_lag_2"] = grouped.shift(2)

    df["dispense_lag_7"] = grouped.shift(7)

    df["dispense_roll_mean_7"] = grouped.transform(
        lambda x: x.shift(1).rolling(7).mean()
    )

    df["dispense_roll_mean_14"] = grouped.transform(
        lambda x: x.shift(1).rolling(14, min_periods=11).mean()
    )

    # Fill missing categorical values
    # df["location_type"] = df["location_type"].fillna("Unknown")
    # df["city_tier"] = df["city_tier"].fillna("Unknown")

    # Categorical Conversions

    for col in ["atm_id", "state", "holiday_name", "holiday_type"]:

        if col in df.columns:

            df[col] = df[col].astype("category")

    # Remove rows with invalid critical data
    df = df.dropna(subset=["atm_id", "date", "dispense"])

    return df


# ==========================================

# 2. MODEL TRAINING & FORECASTING

# ==========================================


def train_and_forecast(df):

    feature_cols = [
        "atm_id",
        "state",
        # "location_type",
        # "city_tier",
        # "uptime_pct",
        # "downtime_pct",
        "day_of_week",
        "day_of_month",
        "month",
        "is_friday",
        "is_weekend",
        "is_salary_period",

        # Holiday Features
        "is_holiday",
        "holiday_name",
        "holiday_type",
        "is_major_festival",

        "is_pre_holiday",
        "is_long_weekend",

        # Compound Features
        "is_salary_friday",
        "is_salary_weekend",
        "is_salary_weekend_holiday",
        "is_salary_long_weekend",

        # Historical Features
        "dispense_lag_1",
        "dispense_lag_2",
        "dispense_lag_7",
        "dispense_roll_mean_7",
        "dispense_roll_mean_14",
    ]

    # Target Shifts for multi-horizon model

    df["target_1day"] = df.groupby("atm_id")["dispense"].shift(-1)

    df["target_3day"] = df.groupby("atm_id")["dispense"].shift(-3)

    df["target_7day"] = df.groupby("atm_id")["dispense"].shift(-7)

    cleaned_df = df.dropna(
        subset=["dispense_lag_7", "dispense_roll_mean_14"]).copy()
    if cleaned_df.empty:
        raise ValueError(
            "No data available after feature engineering. ")
        # "Ensure each ATM has at least 12 days of history.")

    # Train/Validation Time Split (Last 30 days validation)

    # Train/Validation Time Split

    split_date = cleaned_df["date"].max() - pd.Timedelta(days=7)

    train_df = cleaned_df[cleaned_df["date"] <= split_date]

    val_df = cleaned_df[cleaned_df["date"] > split_date]

    print("cleaned_df:", len(cleaned_df))
    print("train_df:", len(train_df))
    print("val_df:", len(val_df))

    for target in ["target_1day", "target_3day", "target_7day"]:
        print(
            target,
            "train rows:",
            train_df[target].notna().sum(),
            "val rows:",
            val_df[target].notna().sum()
        )

    predictions_dict = {}

    horizons = {
        "Next_Day": "target_1day",
        "Next_3_Days": "target_3day",
        "Next_Week": "target_7day",
    }

    latest_records = cleaned_df.groupby("atm_id").tail(1).copy()

    for label, target in horizons.items():

        print(f">>> Training LightGBM Model for [{label}] Prediction...")

        tr_sub = train_df.dropna(subset=[target])

        vl_sub = val_df.dropna(subset=[target])
        if len(tr_sub) == 0:
            print(f"Skipping{target}:no training rows")
            continue
        print(
            f"{target}:",
            "tr_sub=", len(tr_sub),
            "vl_sub=", len(vl_sub)
        )
        print("Training:", target)
        print("tr_sub shape:", tr_sub[feature_cols].shape)

        if len(vl_sub) > 0:
            print("vl_sub shape:", vl_sub[feature_cols].shape)

        print("Feature columns available:")
        print(tr_sub[feature_cols].columns.tolist())

        if tr_sub[feature_cols].shape[0] == 0:
            print(f"{target}: empty training feature set")
            continue
        if len(vl_sub) > 0 and vl_sub[feature_cols].shape[0] == 0:
            print(f"{target}: empty validation feature set")
            vl_sub = pd.DataFrame()

        model = lgb.LGBMRegressor(
            n_estimators=400,
            learning_rate=0.03,
            num_leaves=31,
            random_state=42,
            n_jobs=-1,
        )

        if len(vl_sub) > 100:
            model.fit(
                tr_sub[feature_cols],
                tr_sub[target],
                eval_set=[(vl_sub[feature_cols], vl_sub[target])],
                callbacks=[lgb.early_stopping(30, verbose=False)],
            )
        else:
            print(f"{target}: no validation rows, training without eval_set")

            model.fit(
                tr_sub[feature_cols],
                tr_sub[target]
            )

        latest_records[f"predicted_dispense_{label}"] = model.predict(
            latest_records[feature_cols]
        )

        latest_records[f"predicted_dispense_{label}"] = (latest_records[
            f"predicted_dispense_{label}"
        ].clip(lower=0)
            .round(0)
        )

        predictions_dict[label] = latest_records

    return predictions_dict

# ==========================================

# 3. EXPORT TO DESIGNED EXCEL FILE

# ==========================================


def export_to_excel(predictions_dict, output_path):

    print(f">>> Exporting formatted predictions to: {output_path}...")

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:

        workbook = writer.book

        # Formatting Styles

        header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "valign": "top",
                "fg_color": "#1F4E78",
                "font_color": "#FFFFFF",
                "border": 1,
            }
        )

        number_format = workbook.add_format(
            {
                "num_format": "#,##0",
                "border": 1
            }
        )

        for horizon_name, pred_df in predictions_dict.items():

            reference_date = pd.to_datetime(
                pred_df["date"].max()
            )

            if horizon_name == "Next_Day":
                forecast_date = (
                    reference_date + pd.Timedelta(days=1)
                ).strftime("%d-%b-%Y")

            elif horizon_name == "Next_3_Days":
                forecast_date = (
                    reference_date + pd.Timedelta(days=3)
                ).strftime("%d-%b-%Y")

            else:
                forecast_date = (
                    reference_date + pd.Timedelta(days=7)
                ).strftime("%d-%b-%Y")

            pred_col = f"predicted_dispense_{horizon_name}"

            export_cols = [
                "atm_id",
                "date",
                "is_salary_period",
                "is_long_weekend",
                "holiday_name",
                pred_col,
            ]

            report_df = pred_df[export_cols].copy()

            report_df.rename(
                columns={
                    "date": "reference_date",
                    pred_col: "predicted_dispense_amount",
                },
                inplace=True,
            )

            # Optional: Shows forecast target date inside sheet
            report_df["forecast_for_date"] = forecast_date

            # Split into multiple sheets if Excel row limit is exceeded

            MAX_ROWS = 1_000_000

            for i in range(0, len(report_df), MAX_ROWS):

                chunk = report_df.iloc[i:i + MAX_ROWS]

                if len(report_df) <= MAX_ROWS:
                    current_sheet = forecast_date
                else:
                    current_sheet = (
                        f"{forecast_date}_P{(i // MAX_ROWS) + 1}"
                    )[:31]

                chunk.to_excel(
                    writer,
                    sheet_name=current_sheet,
                    index=False
                )

                worksheet = writer.sheets[current_sheet]

                # Apply formatting

                for col_num, value in enumerate(chunk.columns.values):

                    worksheet.write(
                        0,
                        col_num,
                        value,
                        header_format
                    )

                    worksheet.set_column(
                        col_num,
                        col_num,
                        20
                    )

                # Predicted dispense column
                worksheet.set_column(
                    "F:F",
                    25,
                    number_format
                )

    print(">>> Export Complete Successfully!")


# ==========================================

# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":

    df = load_and_engineer_data()

    predictions = train_and_forecast(df)

    export_to_excel(predictions, OUTPUT_EXCEL)
