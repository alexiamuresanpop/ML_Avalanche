import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("avalanche_dataset")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / f"warnings_winter_2023_2026.csv"

df = pd.read_csv("avalanche_dataset\warnings_winter_RAW_2023_2026.csv")

# Exclude identifiers and dates
# I also exclude RegionTypeName because A and B are incredibly unbalanced
# and it introduces data leakage

exclude = ["RegId", "RegionTypeName","PublishTime","ValidFrom", "ValidTo"]
X = df.drop(columns=exclude)

#I forgot to add this to the other file when there is no wind in general
X["wind_direction_change"]=X["wind_direction_change"].fillna(0)

#Error in upper case

X['cloud_cover'] = df['cloud_cover'].replace('Not Given', 'Not given')

X.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
