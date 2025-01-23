import math

# Function to calculate the distance between two GPS points using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])  # Convert to radians
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(a))  # Return distance in kilometers (6371 is the radius of Earth in Kilometers)

# Function to match each point in array1 to the closest point in array2
def match_closest_points(array1, array2):
    closest_points = {}
    for lat1, lon1 in array1:
        closest = min(array2, key=lambda point: haversine(lat1, lon1, point[0], point[1]))  # Find the closest point
        closest_points[(lat1, lon1)] = closest
    return closest_points

# Example Usage
if __name__ == "__main__":
    array1 = [(40.7128, -74.0060), (34.0522, -118.2437)]  # NYC, LA
    array2 = [(41.8781, -87.6298), (29.7604, -95.3698)]   # Chicago, Houston
    
    result = match_closest_points(array1, array2)
    print(result)
