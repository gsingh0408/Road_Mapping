import pandas as pd
import geopandas as gpd
from shapely.wkt import loads

def load_geodata(csv_file_path):
    
    # Load dataset and convert WKT to geometries

    df = pd.read_csv(csv_file_path)
    geometries = []
    for wkt in df['WKT']:
        try:
            geom = loads(wkt)
            geometries.append(geom)
        except Exception as e:
            print(f"Error parsing WKT: {e}")
            geometries.append(None)
            
    gdf = gpd.GeoDataFrame(df, geometry=geometries, crs='EPSG:4326')
    return gdf.dropna(subset=['geometry'])

def get_zone_centroid(gdf, zone_name):
    """Get the centroid of a specified zone."""
    zone_row = gdf[gdf['name'].str.contains(zone_name, case=False, na=False)]
    if zone_row.empty:
        available = ", ".join(gdf['name'].tolist())
        raise ValueError(f"Zone '{zone_name}' not found. Available: {available}")
    
    centroid = zone_row.geometry.iloc[0].centroid
    return (centroid.y, centroid.x)