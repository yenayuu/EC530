# GPS Distance Calculation and Closest Point Matching

This Python project calculates the distance between GPS coordinates using the the closest distance and matches each point in one set of coordinates to the closest point in another set.

---

## Features
1. **Haversine Formula**: Accurately calculates the distance between two GPS coordinates, considering the Earth's curvature.
2. **Closest Point Matching**: Matches each point in the first array of GPS coordinates to the closest point in the second array.
3. **Efficient Computation**: Uses Python's built-in `min()` function with a custom `lambda` to determine the closest points efficiently.

---

## Formula Explanation
This Haversine formula calculates the great-circle distance between two points on a sphere using their latitudes and longitudes:

\[
d = 2r \cdot \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)
\]

Where:
- \( r \): Earth's radius (6371 km by default)
- \( \phi \): Latitude (in radians)
- \( \lambda \): Longitude (in radians)
- \( \Delta \phi \): Difference in latitudes
- \( \Delta \lambda \): Difference in longitudes

---

## Requirements
This code requires Python 3 and the built-in `math` module.

---

## How to Use

### Input
The code expects two lists of GPS coordinates (latitude, longitude):
1. `array1`: The points you want to match.
2. `array2`: The points to which `array1` points will be matched.

Example:
```python
array1 = [(40.7128, -74.0060), (34.0522, -118.2437)]  # NYC, LA
array2 = [(41.8781, -87.6298), (29.7604, -95.3698)]   # Chicago, Houston
```

### Execution
Run the script to see the mapping of each point in `array1` to its closest point in `array2`.

```python
result = match_closest_points(array1, array2)
print(result)
```

### Output
The output is a dictionary where:
- Keys are points from `array1`.
- Values are the closest points from `array2`.

Example Output:
```
{
    (40.7128, -74.006): (41.8781, -87.6298),
    (34.0522, -118.2437): (29.7604, -95.3698)
}
```

---

## Code Overview
### 1. **Haversine Function**
Calculates the great-circle distance between two points:
```python
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(a))
```

### 2. **Closest Point Matching Function**
Finds the closest point in `array2` for each point in `array1`:
```python
def match_closest_points(array1, array2):
    closest_points = {}
    for lat1, lon1 in array1:
        closest = min(array2, key=lambda point: haversine(lat1, lon1, point[0], point[1]))
        closest_points[(lat1, lon1)] = closest
    return closest_points
```

---

## Example

### Input:
```python
array1 = [(40.7128, -74.0060), (34.0522, -118.2437)]  # NYC, LA
array2 = [(41.8781, -87.6298), (29.7604, -95.3698)]   # Chicago, Houston
```

### Output:
```
{
    (40.7128, -74.006): (41.8781, -87.6298),
    (34.0522, -118.2437): (29.7604, -95.3698)
}
```



## Notes
- The Earth's radius is set to 6371 km (for kilometers). You can change it to 3958.8 if you want the result in miles.
- Ensure that the arrays are not empty; otherwise, the function will return an empty dictionary.



