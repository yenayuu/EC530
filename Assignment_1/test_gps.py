import pytest
import pandas as pd
from distance_calculator import haversine, match_closest_points  

# Function to load CSV data
def load_csv_data(file_path):
    df = pd.read_csv(file_path)
    df_cleaned = df.dropna(subset=["latitude", "longitude"])  # Drop missing values
    return list(zip(df_cleaned["latitude"], df_cleaned["longitude"]))

# List of CSV files to test
csv_files = [
    "Boston 311 012225.csv",
    "world_cities.csv",
    "iata-icao.csv"
]

@pytest.mark.parametrize("csv_file", csv_files)
def test_haversine(csv_file):
    test_points = load_csv_data(csv_file)
    
    if len(test_points) >= 2:
        lat1, lon1 = test_points[0]
        lat2, lon2 = test_points[1]
        distance = haversine(lat1, lon1, lat2, lon2)
        assert distance > 0  # Ensure positive distance between two locations

@pytest.mark.parametrize("csv_file", csv_files)
def test_match_closest_points(csv_file):
    test_points = load_csv_data(csv_file)

    if len(test_points) >= 4:
        array1 = test_points[:2]  # First two locations
        array2 = test_points[2:4]  # Next two locations

        result = match_closest_points(array1, array2)
        assert len(result) == 2  # Ensure the correct number of matches
        for key, value in result.items():
            assert key in array1 and value in array2  # Ensure valid mappings
