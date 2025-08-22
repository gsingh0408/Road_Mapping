import pandas as pd
import warnings

from data_loader import load_geodata, get_zone_centroid
from route_finder import get_actual_road_route, calculate_route_distance
from geocode_analyzer import find_cities_along_actual_route
from visualization import create_route_visualization_map

warnings.filterwarnings('ignore')

class IndianZoneRouteFinder:
    def __init__(self, csv_file_path):
        self.gdf = load_geodata(csv_file_path)
    
    def analyze_route(self, start_zone, end_zone):
        try:
            print(f"\n{'='*80}")
            print(f"ACTUAL ROUTE: {start_zone} → {end_zone}")
            print(f"{'='*80}")
            
            print("\n1. Getting zone coordinates...")
            start_coords = get_zone_centroid(self.gdf, start_zone)
            end_coords = get_zone_centroid(self.gdf, end_zone)
            print(f"   Start: {start_coords} ({start_zone})")
            print(f"   End: {end_coords} ({end_zone})")
            
            print("\n2. Getting actual road route...")
            route_points = get_actual_road_route(start_coords, end_coords)
            
            if not route_points:
                return {"error": "Could not generate route"}
            
            distance = calculate_route_distance(route_points)
            print(f"   Route distance: {distance:.1f} km")
            
            print("\n3. Finding cities along actual road route...")
            cities_data = find_cities_along_actual_route(route_points)
            
            print("\n4. Creating route visualization...")
            route_map = create_route_visualization_map(start_zone, end_zone, route_points, cities_data, self.gdf)
            
            print("\n5. Saving results...")
            cities_file, summary_file = self.save_results_to_csv(start_zone, end_zone, cities_data, route_points)
            
            map_file = f"route_map_{start_zone.replace(' ', '_')}_to_{end_zone.replace(' ', '_')}.html"
            route_map.save(map_file)
            print(f" Interactive map saved to: {map_file}")
            
            self._display_results(start_zone, end_zone, distance, cities_data)
            
            return {
                'start_zone': start_zone,
                'end_zone': end_zone,
                'distance_km': distance,
                'cities_found': cities_data,
                'route_points': route_points,
                'map': route_map,
                'files_saved': [cities_file, summary_file, map_file]
            }
            
        except Exception as e:
            print(f"\n  Error analyzing route: {str(e)}")
            return {"error": str(e)}

    def save_results_to_csv(self, start_zone, end_zone, cities_data, route_points):
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        
        if cities_data:
            cities_df = pd.DataFrame(cities_data)
            cities_file = f"cities_along_route_{start_zone.replace(' ', '_')}_to_{end_zone.replace(' ', '_')}_{timestamp}.csv"
            cities_df.to_csv(cities_file, index=False)
            print(f" Cities saved to: {cities_file}")
        else:
            cities_file = None
        
        summary_data = {
            'start_zone': [start_zone],
            'end_zone': [end_zone],
            'total_cities_found': [len(cities_data)],
            'route_distance_km': [calculate_route_distance(route_points)],
            'analysis_date': [pd.Timestamp.now()],
            'cities_list': ['; '.join([city['city_name'] for city in cities_data])]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_file = f"route_summary_{start_zone.replace(' ', '_')}_to_{end_zone.replace(' ', '_')}_{timestamp}.csv"
        summary_df.to_csv(summary_file, index=False)
        print(f" Summary saved to: {summary_file}")
        
        return cities_file, summary_file

    def _display_results(self, start_zone, end_zone, distance, cities_data):
        """Print results to console."""
        print(f"\n{'='*80}")
        print("ROUTE ANALYSIS RESULTS")
        print(f"{'='*80}")
        print(f"Route: {start_zone} → {end_zone}")
        print(f"Distance: {distance:.1f} km")
        print(f"Cities found along actual road route: {len(cities_data)}")
        
        if cities_data:
            print("\nCITIES ALONG THE ROUTE (in order of travel):")
            print("-" * 50)
            for i, city in enumerate(cities_data, 1):
                print(f"{i:2d}. {city['city_name']:<20} ({city['state']})")

def main():
    try:
        print("🇮🇳 INDIAN ZONE ROUTE ANALYZER")
        print("Finding cities along actual road routes between Indian zones")
        print("="*80)
        
        analyzer = IndianZoneRouteFinder('HubCodes.csv')
        
        print("\nAvailable Indian Zones:")
        print("-" * 40)
        zones = analyzer.gdf['name'].tolist()
        for i, zone in enumerate(zones, 1):
            print(f"{i:2d}. {zone}")
        
        routes_to_analyze = [
            ("Tamil Nadu", "Karnataka North"),
            ("Maharashtra North", "Gujarat"),
            ("UP - West", "Punjab"),
            ("Bengal", "Bihar"),
            ("Andhra Pradesh East", "Telangana")
        ]
        
        print(f"\n🚗 Analyzing {len(routes_to_analyze)} routes for cities along actual roads...")
        
        for start_zone, end_zone in routes_to_analyze:
            result = analyzer.analyze_route(start_zone, end_zone)
            if 'error' not in result:
                print(f"\n✅ {start_zone} → {end_zone}: {len(result['cities_found'])} cities found")
            else:
                print(f"\n {start_zone} → {end_zone}: {result['error']}")
            
            print("-" * 80)
        
        print(f"\n ANALYSIS COMPLETE!")
        print("All results saved to CSV files and interactive HTML maps.")
        print("Open the HTML map files in your browser to see the detailed routes!")
        
    except FileNotFoundError:
        print(" Error: HubCodes.csv file not found in current directory")
        print("Please ensure the CSV file is in the same folder as this script.")
    except Exception as e:
        print(f" Error: {str(e)}")

if __name__ == "__main__":
    main()