import folium
import numpy as np

from route_finder import calculate_route_distance

def create_route_visualization_map(start_zone, end_zone, route_points, cities_data, gdf):
    
    center_lat = np.mean([point[0] for point in route_points])
    center_lon = np.mean([point[1] for point in route_points])
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    start_zone_geom = gdf[gdf['name'].str.contains(start_zone, case=False)].iloc[0]['geometry']
    end_zone_geom = gdf[gdf['name'].str.contains(end_zone, case=False)].iloc[0]['geometry']
    
    folium.GeoJson(
        start_zone_geom,
        style_function=lambda x: {'fillColor': 'green', 'color': 'green', 'weight': 2, 'fillOpacity': 0.3}
    ).add_child(folium.Tooltip(f"START: {start_zone}")).add_to(m)
    
    folium.GeoJson(
        end_zone_geom,
        style_function=lambda x: {'fillColor': 'red', 'color': 'red', 'weight': 2, 'fillOpacity': 0.3}
    ).add_child(folium.Tooltip(f"END: {end_zone}")).add_to(m)
    
    folium.PolyLine(
        route_points,
        color='blue',
        weight=4,
        opacity=0.8,
        popup='Actual Road Route'
    ).add_to(m)
    
    start_coords = [start_zone_geom.centroid.y, start_zone_geom.centroid.x]
    end_coords = [end_zone_geom.centroid.y, end_zone_geom.centroid.x]
    
    folium.Marker(
        start_coords,
        popup=f"<b>START</b><br>{start_zone}",
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(m)
    
    folium.Marker(
        end_coords,
        popup=f"<b>END</b><br>{end_zone}",
        icon=folium.Icon(color='red', icon='stop', prefix='fa')
    ).add_to(m)
    
    for i, city in enumerate(cities_data):
        folium.Marker(
            [city['latitude'], city['longitude']],
            popup=f"<b>{city['city_name']}</b><br>State: {city['state']}<br>Route Order: {i+1}",
            icon=folium.Icon(color='orange', icon='home', prefix='fa')
        ).add_to(m)
    
    total_distance = calculate_route_distance(route_points)
    legend_html = f'''
    <div style="position: fixed; top: 10px; right: 10px; width: 200px; height: 150px; 
                 background-color: white; border:2px solid grey; z-index:9999; 
                 font-size:12px; padding: 10px">
    <p><b>Route Information</b></p>
    <p>🟢 Start Zone: {start_zone}</p>
    <p>🔴 End Zone: {end_zone}</p>
    <p>🏠 Cities Found: {len(cities_data)}</p>
    <p>📏 Approx Distance: {total_distance:.0f} km</p>
    <p>🛣️ Blue Line: Actual Road Route</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m
