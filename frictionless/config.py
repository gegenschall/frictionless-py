import json
from .helpers import read_asset


# General

VERSION = read_asset('VERSION')
GEOJSON_PROFILE = json.loads(read_asset('profiles', 'geojson.json'))
INQUIRY_PROFILE = json.loads(read_asset('profiles', 'inquiry.json'))
REPORT_PROFILE = json.loads(read_asset('profiles', 'report.json'))
REMOTE_SCHEMES = ['http', 'https', 'ftp', 'ftps']
MISSING_VALUES = ['']
