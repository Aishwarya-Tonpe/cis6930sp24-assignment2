import os
from datetime import datetime
import pytest
from Assignment2 import get_emsstat


# Test for get_emsstat function
def test_get_emsstat():
    # Test getting EMS status for a record
    record = {
        "IncidentType": "EMSSTAT"
    }
    info = []
    emsstat = get_emsstat(record, info)
    # Assert that EMS status is True
    assert emsstat == 1