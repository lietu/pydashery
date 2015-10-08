# Which widgets should be enabled?
WIDGETS = [
    {
        "type": "Clock",
        # Optional, defaults to ISO-8601 -like format
        "format": "%m/%d/%Y\n%I:%M:%S %p"
    },
    {
        "type": "FunctionResult",
        "update_minutes": 0.0167,
        # Definition can be either "module.path:class.method" or
        # "module.path:function_name"
        "func": "time:time"
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
