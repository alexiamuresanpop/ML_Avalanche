import requests
import json

# This file was my first attempt at getting a JSON of warnings from the API

# API parameters
region_id = 3011 #Tromso
language = 2  # English
start_date = "2025-01-01"
end_date = "2025-03-01"

# Construct the URL
url = (
    "https://api01.nve.no/hydrology/forecast/"
    f"avalanche/v6.3.2/api/Warning/Region/"
    f"{region_id}/{language}/{start_date}/{end_date}"
)

response = requests.get(url, timeout=30)
print("Status code:", response.status_code)
response.raise_for_status()

# Convert JSON response to Python objects
warnings = response.json()

print("Number of warnings:", len(warnings))

#save JSON
with open("test_warnings.json", "w", encoding="utf-8") as file:
    json.dump(warnings, file, indent=2, ensure_ascii=False)

print("JSON saved successfully!")