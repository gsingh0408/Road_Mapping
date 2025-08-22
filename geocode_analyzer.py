import time
from geopy.geocoders import Nominatim

from .constants import MAJOR_CITIES

geolocator = Nominatim(user_agent="indian_route_finder", timeout=15)

def find_cities_along_actual_route(route_points, max_distance_km=25):
    
    print(f"Searching for cities along route with {len(route_points)} points...")
    
    cities_found = []
    processed_cities = set()
    
    sample_indices = _get_strategic_sample_points(route_points, target_samples=30)
    
    for i, idx in enumerate(sample_indices):
        try:
            lat, lon = route_points[idx]
            print(f"Geocoding point {i+1}/{len(sample_indices)}: ({lat:.4f}, {lon:.4f})")
            
            time.sleep(0.5)
            
            location = geolocator.reverse(f"{lat}, {lon}", timeout=15, language='en')
            
            if location and location.address:
                city_info = _extract_city_info(location, lat, lon, idx)
                
                if city_info and city_info['city_name'] not in processed_cities:
                    if _is_significant_city(city_info):
                        cities_found.append(city_info)
                        processed_cities.add(city_info['city_name'])
                        print(f"✓ Found city: {city_info['city_name']}, {city_info['state']}")
            
        except Exception as e:
            print(f"Error geocoding point {i}: {str(e)}")
            continue
    
    cities_found.sort(key=lambda x: x['route_index'])
    print(f"Found {len(cities_found)} cities along the route")
    return cities_found

def _get_strategic_sample_points(route_points, target_samples=30):
    if len(route_points) <= target_samples:
        return list(range(len(route_points)))
    
    indices = [0, len(route_points) - 1]
    step = len(route_points) // (target_samples - 2)
    for i in range(step, len(route_points) - 1, step):
        indices.append(i)
    
    return sorted(list(set(indices)))

def _extract_city_info(location, lat, lon, route_idx):
    try:
        address = location.address
        raw = location.raw
        
        city_name = None
        state_name = None
        district_name = None
        
        if 'address' in raw:
            addr = raw['address']
            for field in ['city', 'town', 'municipality', 'village', 'county', 'state_district']:
                if field in addr and addr[field]:
                    city_name = addr[field]
                    break
            
            state_name = addr.get('state', '')
            district_name = addr.get('state_district', addr.get('county', ''))
        
        if not city_name:
            parts = address.split(', ')
            for part in parts[:4]:
                if (len(part) > 2 and 
                    not any(skip in part.lower() for skip in ['road', 'highway', 'pin', 'postal', 'block', 'tehsil', 'mandal'])):
                    city_name = part.strip()
                    break
        
        if city_name:
            return {
                'city_name': city_name,
                'state': state_name or 'Unknown',
                'district': district_name or 'Unknown',
                'latitude': lat,
                'longitude': lon,
                'route_index': route_idx,
                'full_address': address,
                'type': raw.get('type', 'city')
            }
            
    except Exception as e:
        print(f"Error extracting city info: {e}")
    
    return None

def _is_significant_city(city_info):
    city_name = city_info['city_name']
    
    if city_name in MAJOR_CITIES:
        return True
    
    exclude_keywords = ['block', 'tehsil', 'mandal', 'panchayat', 'ward', 'sector']
    if any(keyword in city_name.lower() for keyword in exclude_keywords):
        return False
    
    if len(city_name) < 3:
        return False
    
    if any(char.isdigit() for char in city_name):
        return False
    
    return True