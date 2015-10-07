# Which widgets should be enabled?
WIDGETS = [
    {
        "type": "Clock",
    },
    {
        "type": "Clock",
        "format": "%m/%d/%Y\n%I:%M:%S %p"
    },
    {
        "type": "ImageURL",
        "url": "http://www.foreca.fi/meteogram.php?loc_id=100658225&lang=fi",
        "update_minutes": 15
    },
    {
        "type": "Iframe",
        "url": "http://isitchristmas.com",
        "update_minutes": 15
    },
    {
        "type": "TextFile",
        "filename": "test.txt",
    },
    {
        "type": "Iframe",
        "url": "http://www.metoffice.gov.uk/mobile/forecast/ud9wx0fhw",
        "update_minutes": 15
    }

]

# Check for updates this many times per second
UPDATES_PER_SEC = 3

# Which interface and port to listen to
LISTEN_ADDRESS = "0.0.0.0"
LISTEN_PORT = 8080

# Reloads the app automatically when code changes are detected
DEBUG = True
