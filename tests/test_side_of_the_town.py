import os
from datetime import datetime
import pytest
from Assignment2 import get_side_of_the_town

# Test for get_side_of_the_town function
def test_get_side_of_the_town():
    # Test getting side of the town for a location
    api_key = 'AIzaSyB_ZUfU4vslpc0P1b601PjEbsHhCDofgfg'
    location = "New York"
    central_latitude = 40.7128
    central_longitude = -74.0060
    side_of_town = get_side_of_the_town(location, central_latitude, central_longitude, api_key)
    assert side_of_town == "SE"