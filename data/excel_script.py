import pandas as pd
import calendar

# =====================================================
# FILE PATHS
# =====================================================

input_file = r"C:\Users\kp350028\OneDrive - NCR ATLEOS\Desktop\2025 Raw Uptime.xlsx"

output_file = r"C:\Users\kp350028\OneDrive - NCR ATLEOS\Desktop\Uptime_Daily_Format.xlsx"

# =====================================================
# READ EXCEL
# =====================================================

raw = pd.read_excel(input_file, header=None)

# Actual headers are in Row 1
headers = raw.iloc[1].tolist()

# Data starts from Row 2
df = raw.iloc[2:].copy()

df.columns = headers

df.columns = [str(col).strip() for col in df.columns]

print("\nColumns Found:")
print(df.columns.tolist())

# =====================================================
# RENAME COLUMNS
# =====================================================

df.rename(
    columns={
        "New ATM ID": "atm_id",
        "Data Month": "data_month",
        "LHO/Circle": "lho"
    },
    inplace=True
)

# =====================================================
# CONVERT MONTH COLUMN
# =====================================================

df["data_month"] = pd.to_datetime(df["data_month"])

# =====================================================
# FIND DAY COLUMNS
# =====================================================

day_cols = []

for col in df.columns:

    if str(col).isdigit():

        day_num = int(col)

        if 1 <= day_num <= 31:

            day_cols.append(col)

print(f"\nDay Columns Found: {len(day_cols)}")

# =====================================================
# BUILD DAILY DATASET
# =====================================================

records = []

for _, row in df.iterrows():

    atm_id = row["atm_id"]
    lho = row["lho"]

    month_dt = row["data_month"]

    year = month_dt.year
    month = month_dt.month

    max_days = calendar.monthrange(year, month)[1]

    for day_col in day_cols:

        day = int(day_col)

        if day > max_days:
            continue

        uptime = row[day_col]

        # Convert "-", blanks, NaN to 0
        if pd.isna(uptime):
            uptime = 0

        elif str(uptime).strip() in ["", "-"]:
            uptime = 0

        else:
            try:
                uptime = float(uptime)
            except:
                uptime = 0

        downtime = 100 - uptime

        actual_date = pd.Timestamp(
            year=year,
            month=month,
            day=day
        )

        records.append(
            [
                atm_id,
                lho,
                actual_date,
                uptime,
                downtime
            ]
        )

# =====================================================
# CREATE OUTPUT DATAFRAME
# =====================================================

output_df = pd.DataFrame(
    records,
    columns=[
        "atm_id",
        "lho",
        "date",
        "uptime_pct",
        "downtime_pct"
    ]
)

output_df = output_df.sort_values(
    ["atm_id", "date"]
).reset_index(drop=True)

print(f"\nRecords Generated: {len(records)}")
print(f"Rows Created: {len(output_df)}")

print("\nSample Output:")
print(output_df.head())

# =====================================================
# SAVE TO MULTIPLE SHEETS
# =====================================================

MAX_ROWS_PER_SHEET = 1000000

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    total_rows = len(output_df)

    sheet_num = 1

    for start_row in range(0, total_rows, MAX_ROWS_PER_SHEET):

        end_row = start_row + MAX_ROWS_PER_SHEET

        chunk = output_df.iloc[start_row:end_row]

        sheet_name = f"Part_{sheet_num}"

        print(
            f"Writing {sheet_name} "
            f"Rows {start_row:,} to {min(end_row,total_rows):,}"
        )

        chunk.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        sheet_num += 1

print("\nSUCCESS!")
print(f"Saved To:\n{output_file}")