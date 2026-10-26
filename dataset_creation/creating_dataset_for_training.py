import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("avalanche_dataset")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / f"warnings_winter_2023_2026.csv"

df = pd.read_csv("avalanche_dataset\warnings_winter_RAW_2023_2026.csv")

# Exclude identifiers and columns that only add noise
# I also excluded RegionTypeName because B regions only issue warnings for level 4-5 so it's not informative for this task

exclude = ["RegId", "RegionId", "RegionTypeName","PublishTime","ValidFrom", "ValidTo"]
X = df.drop(columns=exclude)

#I forgot to add the condition that when there's No Wind then the wind_direction_change is 0
#The columns was already transformed so the remaining null values are situations with no Wind
X["wind_direction_change"]=X["wind_direction_change"].fillna(0)

#Error in upper case for preexisting category
X['cloud_cover'] = df['cloud_cover'].replace('Not Given', 'Not given')

X.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
