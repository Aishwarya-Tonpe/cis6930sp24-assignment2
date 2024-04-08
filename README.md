NAME : Aishwarya Tonpe

HOW TO RUN THE CODE : 
Use command : pipenv run python assignment2.py --urls files.csv

BUGS AND ASSUMPTIONS : 
1. Assumed that the date time format does not change
2. Assumed that data in every pdf will be first downloaded and then processed
3. Assumed that its reasonable to use Google Maps API which needs API-key or open-cage API which also needs API key
4. In case of Google API and Open-cage, only 2500 free requests are permitted per day


IMPORTANT FUNCTIONS : 
1. get_day_hour_from_the_date(date_string):
    - Converts a date string (`date_string`) into day of the week (0=Monday, 1=Tuesday, ...) and hour.
    - Parses the date string to extract day and hour components.
    - Returns a tuple `(day_of_week, hour)`. 
   
2. get_coordinates(location, api_key):
    - Retrieves latitude and longitude coordinates for a given `location` using a geocoding API (`googlemaps` in this case).
    - `api_key`: API key used for geocoding.
    - Returns a tuple `(longitude, latitude)`.

3. get_weather_code(date_string, location, api_key):
    - Obtains weather information (e.g., weather code) for a specific `date_string` and `location`.
    - Calls `get_coordinates` to retrieve coordinates for the location.
    - Uses an external weather API (`open-meteo.com`) to get weather data based on coordinates and date.
    - Returns the weather code corresponding to the specified time.

4. rank_locations(incident_data):
    - Ranks locations based on the frequency of occurrence within `incident_data`.
    - Utilizes `Counter` to count occurrences of each location.
    - Assigns rankings to locations based on occurrence frequency.

5. rank_incidents(incident_data):
    - Ranks incident types based on their frequency within `incident_data`.
    - Uses `Counter` to count occurrences of each incident type.
    - Assigns rankings to incident types based on occurrence frequency.

6. get_side_of_the_town(location, central_latitude, central_longitude, api_key):
    - Determines the side of town (e.g., NE, NW, SE, SW) for a given `location`.
    - Compares the location's coordinates with central coordinates to ascertain direction (North/South, East/West).
    - Returns a string representing the side of town.
   
7. get_emsstat(record, info):
    - Checks if the incident record has an associated `EMSSTAT` event.
    - Searches within `info` (list of incident records) to find corresponding `EMSSTAT` events for the same location and date/time.
    - Returns `True` if an associated `EMSSTAT` event is found; otherwise, returns `False`.

