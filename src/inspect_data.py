import argparse
from pathlib import Path
import pandas as pd

pasrser = argparse.ArgumentParser(description= "Inspect a CSV file")

pasrser.add_argument("--input", required = True, help="file's path" )

args = pasrser.parse_args()

file_path = Path(args.input)

df = pd.read_csv(file_path, na_values = ["M"])

# print("\nfirst five rows")
# print(df.head())

# print("\nrows and columns")
# print(df.shape)

# print("\ncolumns names")
# print(df.columns.tolist())

# print("\nvolumns types")
# print(df.dtypes)

print("\nMissing values per column")
print(df.isna().sum())

# convert timestamp from str to datetime tpye
df["valid"] = pd.to_datetime(df["valid"], errors = "coerce")

print("\nMissing or unparseable timestamps:")
print(df["valid"].isna().sum())

#Select rows that have both a timestamp and a temperature.
usable = df.dropna(subset =["valid","tmpf"])

print("\nNumber of available temperature by minute:")
print(usable["valid"].dt.minute.value_counts().sort_index())

# check if every hour at :51 have a value
hourly = df.loc[(df["valid"].dt.minute ==51)& df ["tmpf"].notna(), ["valid","tmpf"]]

print("\nDuplicate timestamps")
print(hourly["valid"].duplicated().sum())

print("\nTime gaps occour")
print(hourly["valid"].diff().value_counts().sort_index())


