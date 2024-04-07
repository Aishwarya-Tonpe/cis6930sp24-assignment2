import argparse

import geocoder as geocoder
import pandas as pd
import pypdf
from Constants import strings
import re
import urllib
import urllib.request
from datetime import datetime
from collections import Counter
from geopy.geocoders import Nominatim
import requests
import googlemaps
import configparser
from opencage.geocoder import OpenCageGeocode

def download_data(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    local_file_path = strings.file_paths["local_file_path"]
    with open(local_file_path, "wb") as local_file:
        local_file.write(data)

    return local_file_path

def extract_data_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text(extraction_mode="layout")

    lines = text.splitlines()
    lines = lines[2:]
    lines = lines[:-1]

    data = []
    for l in lines:
        if(l != ""):
            date_pattern = r'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}'

            # Find all occurrences of the date pattern in the line
            matches = re.finditer(date_pattern, l)

            # If there are matches, split the line at each match
            if matches:
                indices = [match.start() for match in matches]
                matched_lines = [l[i:j].strip() for i, j in zip([0] + indices, indices + [None])]

                # Filter out empty lines
                matched_lines = list(filter(None, matched_lines))
                for ml in matched_lines:
                    split_line = re.split("   ", ml)
                    non_empty_list = [value for value in split_line if value is not None and value != ""]
                    extract_fields(non_empty_list, data)

            else:
                matched_lines =  [l.strip()]
                split_line = re.split("   ", l)

                non_empty_list = [value for value in split_line if value is not None and value != ""]
                extract_fields(non_empty_list, data)

    return data

def extract_fields(non_empty_list, data):
    if(len(non_empty_list) == 5):
        categories = ["Date/Time", "Incident Number", "Location", "Nature", "Incident ORI"]
        date_time = non_empty_list[0].strip()
        incident_number = non_empty_list[1].strip()
        location = non_empty_list[2].strip()
        if(non_empty_list[3] != " "):
            nature = non_empty_list[3].strip()
        else: nature = non_empty_list[3]
        incident_type = non_empty_list[4].strip()

        extracted_data = {
            strings.field_names["date_time"]: date_time,
            strings.field_names["incident_number"]: incident_number,
            strings.field_names["location"]: location,
            strings.field_names["nature"] : nature,
            strings.field_names["incident_type"]: incident_type
        }

        # Append the data to the list
        data.append(extracted_data)

    else:
        nature = ""
        for entry in non_empty_list:
            if(entry.isalpha()):
                nature = entry

        extracted_data = {
            strings.field_names["date_time"] : "",
            strings.field_names["incident_number"] : "",
            strings.field_names["location"] : "",
            strings.field_names["nature"] : nature,
            strings.field_names["incident_type"]: ""
        }

        data.append(extracted_data)

def get_day_hour_from_the_date(date_string):
    if int(date_string[0]) > 1 and date_string[1] != '/':
        date_string = date_string[1:]

    date_object = datetime.strptime(date_string, "%m/%d/%Y %H:%M")

    # Get the day of the week
    day_of_week = date_object.weekday()
    # Get the hour component from the datetime object
    hour = date_object.hour

    return (day_of_week, hour)

def get_coordinates(location, api_key):
    # gmaps = googlemaps.Client(key=api_key)
    # geocode_result = gmaps.geocode(location)
    geocoder = OpenCageGeocode(api_key)
    geocode_result = geocoder.geocode(location)
    if geocode_result:
        # Extract the latitude and longitude from the result
        # location = geocode_result[0]['geometry']['location']
        # latitude = location['lat']
        # longitude = location['lng']
        latitude = geocode_result[0]['geometry']['lat']
        longitude = geocode_result[0]['geometry']['lng']
        # coordinates_dict[location] = (longitude, latitude)
        return longitude, latitude
    else:
        print("No results found for the address:", location)
        return ()

def get_weather_code(date_string, location, api_key, longitude, latitude):

    if int(date_string[0]) > 1 and date_string[1] != '/':
        date_string = date_string[1:]

    date_object = datetime.strptime(date_string, "%m/%d/%Y %H:%M")

    # Extract the date and time components
    date = date_object.date()
    time = date_object.hour

    if latitude > 180 or latitude < -180 or longitude > 180 or longitude < -180:
        return -1


    weather_api = f"""https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={date}&end_date={date}&hourly=weather_code"""
    # Send a GET request to the API
    response = requests.get(weather_api)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        weather_data = response.json()
        weather_code_all_hours = weather_data['hourly']['weather_code']
        weather_code = weather_code_all_hours[int(time)]
    else:
        # Print an error message if the request was not successful
        weather_code = -1
        print(f"Error: {response.status_code}")

    return weather_code


def rank_locations(incident_data) :
    # Extract locations from incident data
    locations = [incident['Location'] for incident in incident_data]

    # Count occurrences of each location
    location_counter = Counter(locations)

    # Sort locations by frequency
    sorted_locations = sorted(location_counter, key=lambda x: (-location_counter[x], x))

    # Assign integer rankings to locations with tie-breaking logic
    location_rankings = {}
    rank = 1
    prev_count = None
    for location in sorted_locations:
        count = location_counter[location]
        # rank = rank + count
        new_rank = rank + count

        location_rankings[location] = rank
        rank = new_rank

    return location_rankings

def rank_incidents(incident_data):
    incident_type = [incident['nature'] for incident in incident_data]

    # Count occurrences of each incident
    incident_counter = Counter(incident_type)

    # Sort incidents by frequency
    sorted_incident_types = sorted(incident_counter, key=lambda x: (-incident_counter[x], x))

    # Assign integer rankings to incidents with tie-breaking logic
    incident_rankings = {}
    rank = 1
    prev_count = None
    for incident in sorted_incident_types:
        count = incident_counter[incident]
        new_rank = rank + count

        incident_rankings[incident] = rank
        rank = new_rank

    return incident_rankings


def get_side_of_the_town(location, central_latitude, central_longitude, api_key, longitude, latitude):
    longitude_diff = longitude - central_longitude
    latitude_diff = latitude - central_latitude

    # Determine the direction in terms of North (N) or South (S)
    if latitude_diff > 0:
        direction_ns = 'N'
    elif latitude_diff < 0:
        direction_ns = 'S'
    else:
        direction_ns = ''

    # Determine the direction in terms of East (E) or West (W)
    if longitude_diff > 0:
        direction_ew = 'E'
    elif longitude_diff < 0:
        direction_ew = 'W'
    else:
        direction_ew = ''

    side_of_town = direction_ns + direction_ew
    return side_of_town

def get_emsstat(record, info):
    flag = True
    if record['IncidentType'] == 'EMSSTAT':
        flag = int(True)
    elif record['IncidentType'] != 'EMSSTAT':
        target_index = info.index(record)
        if target_index < len(info) - 1:
            target_1 = info[target_index + 1]
            if target_1['IncidentType'] == 'EMSSTAT' and target_1['Location'] == record['Location'] and target_1['DateTime'] == record['DateTime']:
                flag = int(True)
            else:
                flag = int(False)
        if target_index < len(info) - 2:
            target_2 = info[target_index + 2]
            if target_2['IncidentType'] == 'EMSSTAT' and target_2['Location'] == record['Location'] and target_2['DateTime'] == record['DateTime']:
                flag = int(True)
            else:
                flag = int(False)
        else:
            flag = int(False)
    else:
        flag = int(False)

    return flag


# Function to perform data augmentation
def perform_data_augmentation(pdf_urls):
    all_augmented_data = []
    count = 1
    for url in pdf_urls:
        print("FILE", count)

        pdf_path = url.split('/')[-1]
        pdf = download_data(url)
        get_info = extract_data_from_pdf(pdf)
        pdf_info = get_info[1:]
        location_ranks = rank_locations(pdf_info)
        incident_ranks = rank_incidents(pdf_info)

        central_longitude = 35.220833
        central_latitude = -97.443611

        columns = ['Day of the Week', 'Time of Day', 'Weather',	'Location Rank',	'Side of Town',	'Incident Rank', 'Nature', 'EMSSTAT']
        config = configparser.ConfigParser()
        config.read('config.ini')
        # api_key = config['APIKeys']['weather_api_key']
        api_key = config['APIKeys']['open_cage_api_key']

        augmented_data = []
        for record in pdf_info:
            coordinates = get_coordinates(record["Location"], api_key)
            if len(coordinates) != 0:
                (longitude, latitude) = coordinates
            else:
                (longitude, latitude) = (9999, 9999)
            (day, hour) = get_day_hour_from_the_date(record['DateTime'])
            weather_code = get_weather_code(record['DateTime'], record['Location'], api_key, longitude, latitude)
            location_rank = location_ranks[record['Location']]
            side_of_town = get_side_of_the_town(record['Location'], central_latitude, central_longitude, api_key, longitude, latitude)
            incident_rank = incident_ranks[record['nature']]
            nature = record['nature']
            emssat = get_emsstat(record, pdf_info)
            new_record = (day, hour, weather_code, location_rank, side_of_town, incident_rank, nature, emssat)
            augmented_data.append(new_record)

        pd.set_option('display.max_rows', None)
        df = pd.DataFrame(augmented_data, columns=columns)
        print(df)
        all_augmented_data.append(df)
        count = count + 1

    return all_augmented_data

# Main function
def main(urls_file):
    # Read URLs from CSV file
    urls_df = pd.read_csv(urls_file, header=None, names=['URL'])

    # Extract URLs
    pdf_urls = urls_df['URL'].tolist()

    # Perform data augmentation
    augmented_data = perform_data_augmentation(pdf_urls)
    # print(augmented_data)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Perform data augmentation for incident reports")
    parser.add_argument("--urls", required=True, help="File containing URLs of incident reports")
    args = parser.parse_args()

    # Execute main function
    main(args.urls)
