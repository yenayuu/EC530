import pytest
import pandas as pd
from distance_calculator import haversine, match_closest_points

def load_csv_data(file_path):
    df = pd.read_csv(file_path)

    # Normalize lat/lon column names
    for lat_col in ["latitude", "lat"]:
        for lon_col in ["longitude", "lng", "lon"]:
            if lat_col in df.columns and lon_col in df.columns:
                df_cleaned = df.dropna(subset=[lat_col, lon_col])
                return list(zip(df_cleaned[lat_col], df_cleaned[lon_col]))

    raise ValueError(f"No valid latitude/longitude columns found in {file_path}")

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
        assert isinstance(distance, float)
        assert distance >= 0

def test_haversine_zero_distance():
    assert haversine(0, 0, 0, 0) == 0

def test_match_basic_accuracy():
    a1 = [(0, 0)]
    a2 = [(0, 1), (1, 0)]
    result = match_closest_points(a1, a2)
    assert len(result) == 1
    assert result[(0, 0)] in a2

def test_match_multiple():
    a1 = [(0, 0), (10, 10)]
    a2 = [(0, 1), (9.9, 10.1)]
    result = match_closest_points(a1, a2)
    assert result[(0, 0)] == (0, 1)
    assert result[(10, 10)] == (9.9, 10.1)

@pytest.mark.parametrize("csv_file", csv_files)
def test_match_closest_points(csv_file):
    test_points = load_csv_data(csv_file)
    if len(test_points) >= 4:
        array1 = test_points[:2]
        array2 = test_points[2:4]
        result = match_closest_points(array1, array2)
        assert len(result) == 2
        for key, val in result.items():
            assert key in array1
            assert val in array2
