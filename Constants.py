class strings:

    dbstrings = {
        "db_path" : "resources/normanpd.db",
        "create_db" : "CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT, nature TEXT, incident_ori TEXT)",
        "insert_db" : "INSERT INTO incidents VALUES ",
        "select_db" : "SELECT nature, COUNT(*) AS nature_count FROM incidents GROUP BY nature",
        "select_all_db" : "SELECT * FROM incidents",
        "drop_table" : "DROP TABLE IF EXISTS incidents"
    }

    file_paths = {
        "local_file_path" : "dwpdf.pdf"
    }

    field_names = {
        "date_time" : "DateTime",
        "incident_number" : "IncidentNumber",
        "location" : "Location",
        "nature" : "nature",
        "incident_type" : "IncidentType"
    }

    other = {
        "provide_incidents_url" : "Please provide the --incidents argument with a URL.",
        "seperator" : "|",
        "new_line" : "\n",
        "comma" : ","
    }

    test_constants = {
        "print_status_test_output" :
            """Traffic Stop|78
    Transfer/Interfacility|72
    Disturbance/Domestic|46
    Sick Person|44
    Alarm|24
    Welfare Check|20
    Check Area|18
    Contact a Subject|18
    Follow Up|18
    MVA With Injuries|16
    Supplement Report|14
    Unconscious/Fainting|14
    Breathing Problems|12
    Chest Pain|12
    Hemorrhage/Lacerations|12
    Traumatic Injury|12
    Falls|10
    Fraud|10
    Harassment / Threats Report|10
    Parking Problem|10
    Public Assist|10
    Trespassing|10
    Animal at Large|8
    Fire Alarm|8
    Hit and Run|8
    Larceny|8
    Motorist Assist|8
    Open Door/Premises Check|8
    Suspicious|8
    Unknown Problem/Man Down|8
    COP Relationships|6
    MVA Non Injury|6
    Missing Person|6
    Warrant Service|6
    Abdominal Pains/Problems|4
    Alarm Holdup/Panic|4
    Animal Trapped|4
    Cardiac Respritory Arrest|4
    Escort/Transport|4
    Found Item|4
    Heart Problems/AICD|4
    Mutual Aid|4
    Noise Complaint|4
    Officer Needed Nature Unk|4
    Overdose/Poisoning|4
    Reckless Driving|4
    Road Rage|4
    Stolen Vehicle|4
    Vandalism|4
    911 Call Nature Unknown|2
    Animal Complaint|2
    Animal Vicious|2
    Assault|2
    Assist Fire|2
    COP DDACTS|2
    Civil Standby|2
    Drug Violation|2
    Extra Patrol|2
    Fire Carbon Monoxide Alarm|2
    Fire Grass|2
    Foot Patrol|2
    Kidnapping|2
    Runaway or Lost Child|2
    Stake Out|2
    Test Call|2
    """,
        "extract_data_test_url_1" : "tmp/2024-01-01_daily_incident_summary.pdf",
        "extract_data_test_url_2" : "tmp/2024-01-04_daily_incident_summary.pdf",
        "extract_data_test_expected_count_1" : 329,
        "extract_data_test_expected_count_2" : 337,
    }