# Import dependencies
import json
import re
from pathlib import Path

import pandas as pd
import numpy as np
import requests

# API settings
start_date = "2023-12-01"
end_date = "2026-05-31"

API_URL = ("https://api01.nve.no/hydrology/forecast/avalanche/v6.3.2/api/"f"Warning/All/2/{start_date}/{end_date}")

# Download JSON from API
response = requests.get(API_URL, timeout=500)
response.raise_for_status()
warnings = response.json()

# Create paths for download
OUTPUT_DIR = Path("avalanche_dataset")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_JSON = OUTPUT_DIR / f"warnings_{start_date}_{end_date}.json"
OUTPUT_CSV = OUTPUT_DIR / f"warnings_winter_RAW_2023_2026.csv"

if not isinstance(warnings, list):
    raise ValueError("Expected a JSON list of warning records.")

with OUTPUT_JSON.open("w", encoding="utf-8") as file:
    json.dump(warnings, file, ensure_ascii=False, indent=2)

print(f"Downloaded {len(warnings)} warnings.")

# Helper functions
def safe_column_name(name):
    """Convert API names into consistent column names."""
    name = str(name).strip().lower()
    name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    return name.strip("_")


def get_weather_measurements(weather):
    """
    Flatten MountainWeather.MeasurementTypes into columns.

    Example: Wind -> Speed -> Fresh breeze becomes weather_wind_speed = 'Fresh breeze'
    """
    result = {}

    for measurement in weather.get("MeasurementTypes", []) or []:
        measurement_name = measurement.get("Name", "unknown")

        for subtype in measurement.get("MeasurementSubTypes", []) or []:
            subtype_name = subtype.get("Name", "unknown")

            column = (
                "weather_"
                + safe_column_name(measurement_name)
                + "_"
                + safe_column_name(subtype_name)
            )

            result[column] = subtype.get("Value")

    return result

# List variables
metadata_columns = [
    "RegId",
    "RegionId",
    "RegionName",
    "RegionTypeName",
    "DangerLevel",
    "ValidFrom",
    "ValidTo",
    "PublishTime",
]

time_columns = [
    "wind_shift_start",
    "wind_shift_end",
    "freezing_level_start",
    "freezing_level_end",
    "rain_snow_line_start",
    "rain_snow_line_end",
]

numeric_columns = [
    "DangerLevel",
    "rainfall_most_exposed_area",
    "rainfall_average",
    "temperature_min",
    "temperature_max",
    "freezing_level_masl",
    "rain_snow_line_altitude_masl",
]


# Construct columns for dataset
rows = []

for warning in warnings:
    # Create initial dictionary with top-level metadata fields
    row = {field: warning.get(field) for field in metadata_columns}

    weather = warning.get("MountainWeather") or {}

    # Cloud cover
    row["cloud_cover"] = weather.get("CloudCoverName")

    # Flatten weather measurements
    measurements = get_weather_measurements(weather)

    # Rainfall
    row["rainfall_most_exposed_area"] = measurements.get( "weather_rainfall_most_exposed_area")
    row["rainfall_average"] = measurements.get("weather_rainfall_average")

    # Initial wind speed
    row["wind_speed"] = measurements.get("weather_wind_speed")
    row["wind_direction"] = measurements.get("weather_wind_direction")

    # Temperature
    row["temperature_min"] = measurements.get("weather_temperature_min")
    row["temperature_max"] = measurements.get("weather_temperature_max")

    # Freezing level
    row["freezing_level_masl"] = measurements.get("weather_freezing_level_masl")
    row["freezing_level_start"] = measurements.get("weather_freezing_level_timeperiode_start")
    row["freezing_level_end"] = measurements.get("weather_freezing_level_timeperiode_end")

    # Rain/snow line
    row["rain_snow_line_altitude_masl"] = measurements.get("weather_rain_snow_line_altitude_masl")
    row["rain_snow_line_start"] = measurements.get("weather_rain_snow_line_altitude_timeperiode_start")
    row["rain_snow_line_end"] = measurements.get("weather_rain_snow_line_altitude_timeperiode_end")

    # Wind shift
    row["wind_shift_speed"] = measurements.get("weather_wind_shift_to_speed")
    row["wind_shift_direction"] = measurements.get("weather_wind_shift_to_direction")

    # Wind-shift time endpoints
    row["wind_shift_start"] = measurements.get("weather_wind_shift_to_timeperiode_start")
    row["wind_shift_end"] = measurements.get("weather_wind_shift_to_timeperiode_end")

    rows.append(row)

df = pd.DataFrame(rows)

# Derive features for published time
df["publish_month"] = pd.to_datetime(df["PublishTime"], format="mixed", errors="coerce").dt.month
df["publish_hour"] = pd.to_datetime(df["PublishTime"], format="mixed", errors="coerce").dt.hour


# Convert time endpoints to numeric values
for column in time_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Replace null values with zero
df[time_columns] = df[time_columns].fillna(0)


# Convert numeric columns to actual numbers
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df[numeric_columns] = df[numeric_columns].fillna(0)


# If missing values in wind is because there was no wind
df["cloud_cover"] = (df["cloud_cover"].fillna("Not Given"))
df["wind_speed"] = (df["wind_speed"].fillna("No Wind"))
df["wind_direction"] = (df["wind_direction"].fillna("No Wind"))

# If no wind change -> fill wind_shift with prevailing wind
df["wind_shift_speed"] = df["wind_shift_speed"].fillna(df["wind_speed"])
df["wind_shift_direction"] = df["wind_shift_direction"].fillna(df["wind_direction"])

# Quantify wind direction change
direction_degrees = {
    "N": 0,
    "NE": 45,
    "E": 90,
    "SE": 135,
    "S": 180,
    "SW": 225,
    "W": 270,
    "NW": 315,
}

df["wind_direction_degrees"] = df["wind_direction"].map(direction_degrees)
df["wind_shift_direction_degrees"] = df["wind_shift_direction"].map(
    direction_degrees
)

# Smallest angular change between directions
difference = (
    df["wind_shift_direction_degrees"] - df["wind_direction_degrees"]
).abs()

df["wind_direction_change"] = np.minimum(difference, 360 - difference)


# Geographical region mapping
geographical_region_by_id = {
    # Svalbard / Arctic
    3001: "Svalbard / Arctic",
    3002: "Svalbard / Arctic",
    3003: "Svalbard / Arctic",
    3004: "Svalbard / Arctic",

    # Northern Norway
    3005: "Northern Norway",
    3006: "Northern Norway",
    3007: "Northern Norway",
    3008: "Northern Norway",
    3009: "Northern Norway",
    3010: "Northern Norway",
    3011: "Northern Norway",
    3012: "Northern Norway",
    3013: "Northern Norway",
    3014: "Northern Norway",
    3015: "Northern Norway",
    3016: "Northern Norway",
    3017: "Northern Norway",
    3018: "Northern Norway",

    # Trøndelag
    3019: "Trøndelag",
    3020: "Trøndelag",

    # Western Norway
    3021: "Western Norway",
    3022: "Western Norway",
    3023: "Western Norway",
    3024: "Western Norway",
    3026: "Western Norway",
    3027: "Western Norway",
    3028: "Western Norway",
    3029: "Western Norway",
    3030: "Western Norway",
    3031: "Western Norway",
    3033: "Western Norway",
    3034: "Western Norway",
    3036: "Western Norway",

    # Southern Norway
    3037: "Southern Norway",
    3038: "Southern Norway",

    # Eastern Norway
    3025: "Eastern Norway",
    3032: "Eastern Norway",
    3035: "Eastern Norway",
    3039: "Eastern Norway",
    3040: "Eastern Norway",
    3041: "Eastern Norway",
    3042: "Eastern Norway",
    3043: "Eastern Norway",
    3044: "Eastern Norway",
    3045: "Eastern Norway",
    3046: "Eastern Norway",
}

df["geographical_region"] = df["RegionId"].map(geographical_region_by_id)

# Due to class imbalance for Level 5 I've decided to classify the risk like this

risk= {
    1: "Low",
    2: "Medium",
    3: "High",
    4: "High",
    5: "High"
}

df["risk"] = df["DangerLevel"].map(risk)

# Exclude DangerLevel == 0
df = df[df["DangerLevel"].notna() & (df["DangerLevel"] != 0)].copy()


# Organize columns
column_order = [
    # Identifiers and target
    "RegId",
    "RegionId",
    "RegionName",
    "geographical_region",
    "RegionTypeName",
    "risk",

    # Warning timing
    "ValidFrom",
    "ValidTo",
    "PublishTime",
    "publish_hour",
    "publish_month",

    # Weather predictors
    "cloud_cover",
    "rainfall_most_exposed_area",
    "rainfall_average",
    "wind_speed",
    "wind_shift_speed",
    "wind_direction",
    "wind_shift_direction",
    "wind_direction_change",
    "wind_shift_start",
    "wind_shift_end",
    "temperature_min",
    "temperature_max",
    "freezing_level_masl",
    "freezing_level_start",
    "freezing_level_end",
    "rain_snow_line_altitude_masl",
    "rain_snow_line_start",
    "rain_snow_line_end",
]

df = df[column_order]

df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("\nSaved!")
print(f"CSV: {OUTPUT_CSV}")
print(f"Rows: {len(df)}")
print(f"Regions represented: {df['RegionId'].nunique()}")
print("Danger-level distribution:")
print(df["risk"].value_counts().sort_index())
