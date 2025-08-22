
_________________________________________________________________________

Author : GAURAV SINGH 
Email id : gauravsch2000@gamil.com
linkedin : www.linkedin.com/in/gaurav-singh-987-data-analyst-

__________________________________________________________________________

# Indian Zone Route Analyzer
This Python project analyzes and visualizes road routes between different Indian geographic zones. It identifies major cities along the actual road network and generates interactive maps and data summaries.

## Features
Geospatial Analysis:- Uses `geopandas` to work with zone polygons and centroids.
Actual Road Routing:- Integrates with the OpenRouteService API to find realistic road routes. Includes a fallback to OSRM if the primary service fails.
City Detection:- Employs `geopy` for reverse geocoding along the route to identify cities and towns.
Data Visualization:- Creates interactive HTML maps using `folium`, showing start/end zones, the road route, and discovered cities.
Data Persistence:- Saves analysis results to CSV files for easy access and reporting.

## Project Structure
The project is organized into modular files for better readability and maintenance:
- main.py: The main entry point of the application.
- src: A directory containing all the core logic modules.
  - constants.py: Stores API keys and constant data.
  - data_loader.py: Handles loading and preprocessing of geospatial data.
  - route_finder.py : Manages calls to external routing APIs.
  - geocode_analyzer.py : Contains the logic for geocoding and filtering cities.
  - visualization.py : Responsible for creating the interactive map.

## Requirements
- Python 3.6+
- pandas
- geopandas
- shapely
- requests
- folium
- numpy
- geopy

