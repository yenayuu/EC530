import math

def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c  # Radius of Earth in kilometers

def match_closest_points(array1, array2):
    closest_points = {}
    for lat1, lon1 in array1:
        closest = min(array2, key=lambda point: haversine(lat1, lon1, point[0], point[1]))
        closest_points[(lat1, lon1)] = closest
    return closest_points
