import os

import pandas as pd
import polars as pl


# ==========================================
# PATHS
# ==========================================

RAW_DIR = "raw"

PROCESSED_DIR = "processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


# ==========================================
# VALIDATION
# ==========================================

def validate_columns(df, required_columns, file_name):

    missing = set(required_columns) - set(df.columns)

    if missing:

        raise ValueError(
            f"{file_name} is missing required columns: {missing}"
        )


# ==========================================
# EXCEL TO PARQUET CONVERSION
# ==========================================



def convert_excel_to_parquet():

    # ==========================================
    # TRANSACTIONS
    # ==========================================

    print(">>> [1/2] Converting 'transactions.xlsx' to Parquet format...")

    tx_excel_path = os.path.join(
        RAW_DIR,
        "transactions.xlsx"
    )
    print("Current Working Directory:", os.getcwd())
    print("Transactions Path:", os.path.abspath(tx_excel_path))
    print("Exists:", os.path.exists(tx_excel_path))

    tx_parquet_path = os.path.join(
        PROCESSED_DIR,
        "transactions.parquet"
    )

    # Fast multi-threaded reading via Polars
    # Read ALL sheets from transactions workbook

# Read ALL sheets from transactions workbook

    sheet_data = pd.read_excel(
        tx_excel_path,
        sheet_name=None
    )

    # Merge all sheets into one dataframe

    df_tx = pl.from_pandas(
        pd.concat(
            sheet_data.values(),
            ignore_index=True
        )
    )

    print(
        f"  Loaded {len(sheet_data)} sheets "
        f"with {df_tx.height} total rows"
    )


    validate_columns(
        df_tx,
        [
            "atm_id",
            "date",
            "dispense"
        ],
        "transactions.xlsx"
    )

    df_tx.write_parquet(
        tx_parquet_path,
        compression="snappy"
    )

    print(f"  Saved: {tx_parquet_path}")

    # ==========================================
    # ATM METADATA (CURRENTLY DISABLED)
    # ==========================================

    # Uncomment if metadata becomes available later

    # print(">>> [2/3] Converting 'atm_metadata.xlsx' to Parquet format...")

    # meta_excel_path = os.path.join(
    #     RAW_DIR,
    #     "atm_metadata.xlsx"
    # )

    # meta_parquet_path = os.path.join(
    #     PROCESSED_DIR,
    #     "atm_metadata.parquet"
    # )

    # df_meta = pl.read_excel(
    #     meta_excel_path
    # )

    # validate_columns(
    #     df_meta,
    #     [
    #         "atm_id",
    #         "location_type",
    #         "city_tier",
    #         "uptime_pct",
    #         "downtime_pct"
    #     ],
    #     "atm_metadata.xlsx"
    # )

    # df_meta.write_parquet(
    #     meta_parquet_path,
    #     compression="snappy"
    # )

    # print(f"  Saved: {meta_parquet_path}")

    # ==========================================
    # HOLIDAY MASTER
    # ==========================================

    print(">>> [2/2] Converting 'holiday_master.xlsx' to Parquet format...")

    holiday_excel_path = os.path.join(
        RAW_DIR,
        "holiday_master.xlsx"
    )

    holiday_parquet_path = os.path.join(
        PROCESSED_DIR,
        "holiday_master.parquet"
    )

    # Read holiday workbook

    df_holiday = pl.read_excel(
        holiday_excel_path
    )

    validate_columns(
        df_holiday,
        [
            "date",
            "state",
            "holiday_name"
        ],
        "holiday_master.xlsx"
    )

    # Ensure date datatype

    df_holiday = df_holiday.with_columns(
        pl.col("date").cast(pl.Date)
    )

    # Remove duplicate holiday rows

    df_holiday = df_holiday.unique()

    df_holiday.write_parquet(
        holiday_parquet_path,
        compression="snappy"
    )

    print(f"  Saved: {holiday_parquet_path}")

    # ==========================================
    # COMPLETE
    # ==========================================

    print(">>> Conversion Complete Successfully!")


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    convert_excel_to_parquet()