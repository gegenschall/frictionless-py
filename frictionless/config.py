import json
from .helpers import read_asset


# General

VERSION = read_asset('VERSION')
GEOJSON_PROFILE = json.loads(read_asset('profiles', 'geojson.json'))
INQUIRY_PROFILE = json.loads(read_asset('profiles', 'inquiry.json'))
REPORT_PROFILE = json.loads(read_asset('profiles', 'report.json'))
SCHEMA_PROFILE = json.loads(read_asset('profiles', 'schema.json'))
REMOTE_SCHEMES = ['http', 'https', 'ftp', 'ftps']
MISSING_VALUES = ['']
INFER_CONFIDENCE = 0.9
INFER_SAMPLE = 100
LIMIT_MEMORY = 1000
HEADERS_ROW = 1
HEADERS_JOINER = ' '
