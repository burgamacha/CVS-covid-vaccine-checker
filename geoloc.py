import json
import os
import googlemaps

API_KEY = os.getenv("GOOGLEMAPS_API_KEY")
KM_TO_MILES = 1/1.6

if not API_KEY:
    raise ValueError("GOOGLEMAPS_API_KEY must be defined as an env var")


maps_client = googlemaps.Client(key=API_KEY)


def get_distance(from_city, dest, miles=False):
    distance_geo = maps_client.distance_matrix(origins=from_city, destinations=dest)
    if 'rows' in distance_geo and len(distance_geo["rows"]) == 1:
        distance = distance_geo["rows"][0]['elements'][0]['distance']['value'] / 1000
    else:
        raise ValueError(f"Cannot compute distance between {from_city} and {dest}: {distance_geo} "
                         f"does not have one 'rows' element as expected: "
                         f"{json.dumps(distance_geo, indent=2)}")
    if miles:
        return KM_TO_MILES * distance
    return distance
