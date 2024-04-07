import os
from datetime import datetime
import pytest
from Assignment2 import get_day_hour_from_the_date

# Test for get_day_hour_from_the_date function
def test_get_day_hour_from_the_date():
    # Test getting day and hour from a date string
    date_string = "3/1/2024 13:48"
    day, hour = get_day_hour_from_the_date(date_string)
    assert day == 4
    assert hour == 13