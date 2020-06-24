import stringcase
from .helpers import cached_property
from .metadata import ControlledMetadata
from . import helpers
from . import config


class File(ControlledMetadata):
    metadata_profile = {  # type: ignore
        'type': 'object',
        'required': ['source'],
        'properties': {
            'source': {},
            'scheme': {'type': 'string'},
            'format': {'type': 'string'},
            'hashing': {'type': 'string'},
            'encoding': {'type': 'string'},
            'compression': {'type': 'string'},
            'compressionPath': {'type': 'string'},
            'statistics': {
                'type': 'object',
                'required': ['size', 'hash'],
                'properties': {'size': {'type': 'number'}, 'hash': {'type': 'string'}},
            },
        },
    }

    def __init__(
        self,
        descriptor=None,
        *,
        source=None,
        scheme=None,
        format=None,
        hashing=None,
        encoding=None,
        compression=None,
        compression_path=None,
        statistics=None,
    ):
        self.setdefined('source', source)
        self.setdefined('scheme', scheme)
        self.setdefined('format', format)
        self.setdefined('hashing', hashing)
        self.setdefined('encoding', encoding)
        self.setdefined('compression', compression)
        self.setdefined('compressionPath', compression_path)
        self.setdefined('statistics', statistics)
        super().__init__(descriptor)
        # Detect from source
        detect = helpers.detect_source_scheme_and_format(source)
        self.__detected_compression = None
        if detect[1] in config.SUPPORTED_COMPRESSION:
            self.__detected_compression = detect[1]
            detect = helpers.detect_source_scheme_and_format(source[: -len(detect[1])])
        self.__detected_scheme = detect[0]
        self.__detected_format = detect[1]

    def __setattr__(self, name, value):
        if name in [
            'scheme',
            'format',
            'hashing',
            'encoding',
            'compression',
            'compressionPath',
            'statistics',
        ]:
            self[stringcase.camelcase(name)] = value
        super().__setattr__(name, value)

    @cached_property
    def path(self):
        return self.source if isinstance(self.source, str) else 'memory'

    @cached_property
    def source(self):
        return self.get('source')

    @cached_property
    def scheme(self):
        return self.get('scheme', self.__detected_scheme)

    @cached_property
    def format(self):
        return self.get('format', self.__detected_format)

    @cached_property
    def hashing(self):
        return self.get('hashing', config.DEFAULT_HASHING)

    @cached_property
    def encoding(self):
        return self.get('encoding', config.DEFAULT_ENCODING)

    @cached_property
    def compression(self):
        default = self.__detected_compression or config.DEFAULT_COMPRESSION
        return self.get('compression', default)

    @cached_property
    def compression_path(self):
        return self.get('compressionPath')

    @cached_property
    def statistics(self):
        return self.get('statistics')

    # Expand

    def expand(self):
        self.setdetault('scheme', self.scheme)
        self.setdetault('format', self.format)
        self.setdetault('hashing', self.hashing)
        self.setdetault('encoding', self.hashing)
        self.setdetault('compression', self.compression)
