import io
import os
import json


# Helpers


def read_asset(*paths):
    dirname = os.path.dirname(__file__)
    return io.open(os.path.join(dirname, 'assets', *paths)).read().strip()


# General

VERSION = read_asset('VERSION')
GEOJSON_PROFILE = json.loads(read_asset('profiles', 'geojson.json'))
INQUIRY_PROFILE = json.loads(read_asset('profiles', 'inquiry.json'))
REPORT_PROFILE = json.loads(read_asset('profiles', 'report.json'))
SCHEMA_PROFILE = json.loads(read_asset('profiles', 'schema.json'))
REMOTE_SCHEMES = ['http', 'https', 'ftp', 'ftps']
MISSING_VALUES = ['']
INFER_VOLUME = 100
INFER_CONFIDENCE = 0.9
DETECT_ENCODING_VOLUME = 10000
DETECT_ENCODING_CONFIDENCE = 0.5
DEFAULT_HASHING = 'md5'
DEFAULT_COMPRESSION = 'no'
LIMIT_MEMORY = 1000
HEADERS_ROW = 1
HEADERS_JOINER = ' '

# Tabulator
# TODO: rework

DEFAULT_SCHEME = 'file'
DEFAULT_ENCODING = 'utf-8'
DEFAULT_SAMPLE_SIZE = 100
SUPPORTED_COMPRESSION = ['zip', 'gz']
SUPPORTED_HASHING_ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']
ENCODING_CONFIDENCE = 0.5
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
    + 'AppleWebKit/537.36 (KHTML, like Gecko) '
    + 'Chrome/54.0.2840.87 Safari/537.36'
}
HTTP_TIMEOUT = 10
CSV_SAMPLE_LINES = 100
# http://docs.sqlalchemy.org/en/latest/dialects/index.html
SQL_SCHEMES = ['firebird', 'mssql', 'mysql', 'oracle', 'postgresql', 'sqlite', 'sybase']
S3_DEFAULT_ENDPOINT_URL = 'https://s3.amazonaws.com'

# Loaders

LOADERS = {
    's3': 'frictionless.plugins.aws.AwsLoader',
    'file': 'frictionless.loaders.local.LocalLoader',
    'http': 'frictionless.loaders.remote.RemoteLoader',
    'https': 'frictionless.loaders.remote.RemoteLoader',
    'ftp': 'frictionless.loaders.remote.RemoteLoader',
    'ftps': 'frictionless.loaders.remote.RemoteLoader',
    'stream': 'frictionless.loaders.stream.StreamLoader',
    'text': 'frictionless.loaders.text.TextLoader',
}

# Parsers

PARSERS = {
    'csv': 'frictionless.plugins.csv.CsvParser',
    'gsheet': 'frictionless.plugins.gsheet.GsheetParser',
    'html': 'frictionless.plugins.html.HtmlTableParser',
    'inline': 'frictionless.parsers.inline.InlineParser',
    'json': 'frictionless.plugins.json.JsonParser',
    'jsonl': 'frictionless.plugins.json.NdjsonParser',
    'ndjson': 'frictionless.plugins.json.NdjsonParser',
    'ods': 'frictionless.plugins.ods.OdsParser',
    'sql': 'frictionless.plugins.sql.SqlParser',
    'tsv': 'frictionless.plugins.tsv.TsvParser',
    'xls': 'frictionless.plugins.excel.XlsParser',
    'xlsx': 'frictionless.plugins.excel.XlsxParser',
}

# Writers

WRITERS = {
    'csv': 'frictionless.plugins.csv.CsvWriter',
    'json': 'frictionless.plugins.json.JsonWriter',
    'xlsx': 'frictionless.plugins.excel.XlsxWriter',
    'sql': 'frictionless.plugins.sql.SqlWriter',
}
