import requests
import warnings
from math import radians, cos, sin, asin, sqrt

# from src.constants import ORS_API_KEY
ORS_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual OpenRouteService API key

warnings.filterwarnings('ignore')

def get_actual_road_route(start_coords, end_coords):
    
   
    print(f"Getting actual road route from {start_coords} to {end_coords}")
    
    
    routing_services = [
        _get_route_openrouteservice,
        _get_route_osrm_backup
    ]
    
    for service in routing_services:
        try:
            route = service(start_coords, end_coords)
            if route:
                print(f"✓ Got route with {len(route)} points")
                return route
        except Exception as e:
            print(f"Service failed: {str(e)}")
            continue
    
    print("All routing services failed, using interpolated route")
    return _create_interpolated_route(start_coords, end_coords)

def _get_route_openrouteservice(start_coords, end_coords):

    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [[start_coords[1], start_coords[0]], [end_coords[1], end_coords[0]]],
        "format": "geojson",
        "instructions": False
    }
    
    response = requests.post(url, json=body, headers=headers, timeout=20)
    
    if response.status_code == 200:
        data = response.json()
        coordinates = data['features'][0]['geometry']['coordinates']
        return [(coord[1], coord[0]) for coord in coordinates]
    else:
        raise Exception(f"OpenRouteService error: {response.status_code}")

def _get_route_osrm_backup(start_coords, end_coords): # Backup using OSRM public API

    url = f"https://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}"
    params = {'overview': 'full', 'geometries': 'geojson'}
    
    response = requests.get(url, params=params, timeout=15)
    if response.status_code == 200:
        data = response.json()
        if data.get('code') == 'Ok':
            coordinates = data['routes'][0]['geometry']['coordinates']
            return [(coord[1], coord[0]) for coord in coordinates]
    raise Exception("OSRM backup failed")

def _create_interpolated_route(start_coords, end_coords, points=50):
    lat1, lon1 = start_coords
    lat2, lon2 = end_coords
    
    route_points = []
    for i in range(points + 1):  # include endpoint
        t = i / points
        lat = lat1 + t * (lat2 - lat1)
        lon = lon1 + t * (lon2 - lon1)
        route_points.append((lat, lon))
    
    return route_points

def calculate_route_distance(route_points):
    total_distance = 0
    for i in range(len(route_points) - 1):   # loop through each segment
        lat1, lon1 = route_points[i]
        lat2, lon2 = route_points[i + 1]
        total_distance += _haversine_distance(lat1, lon1, lat2, lon2)
    return total_distance

def _haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2]) # convert to radians
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c