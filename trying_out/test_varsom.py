import requests
import pandas as pd

# First time trying the API to see if it works
# It worked! It returned a csv of all regions

url = (
    "https://api01.nve.no/hydrology/forecast/"
    "avalanche/v6.3.2/api/Archive/Region/json"
)

response = requests.get(url, timeout=30)

print("Status code:", response.status_code)
response.raise_for_status()

regions = response.json()

print("Number of regions:", len(regions))
print("First three results:")

for region in regions[:3]:
    print(region)

df_regions = pd.DataFrame(regions)

print(df_regions.head())
print("\n",df_regions["TypeName"].value_counts(dropna=False))

df_regions.to_csv("regions.csv", index=False)