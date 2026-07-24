import pandas as pd

# 1. Path to your input Parquet file and output Excel file
parquet_file = '../data/processed/transactions.parquet'
excel_file = '../data/raw/transactions.xlsx'

# 2. Read the Parquet file into a Pandas DataFramee
df = pd.read_parquet(parquet_file)

# 3. Export the DataFrame to an Excel file (without the index column)
df.to_excel(excel_file, index=False)

print(f"Successfully converted '{parquet_file}' to '{excel_file}'!")
