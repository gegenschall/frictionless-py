import os
from .helpers import cached_property
from .metadata import Metadata
from .system import system
from . import helpers
from . import config


class File(Metadata):
    metadata_strict = True
    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["source"],
        "properties": {
            "source": {},
            "scheme": {"type": "string"},
            "format": {"type": "string"},
            "hashing": {"type": "string"},
            "encoding": {"type": "string"},
            "compression": {"type": "string"},
            "compressionPath": {"type": "string"},
            "contorl": {"type": "object"},
            "dialect": {"type": "object"},
            "newline": {"type": "string"},
            "stats": {
                "type": "object",
                "required": ["hash", "bytes", "rows"],
                "properties": {
                    "hash": {"type": "string"},
                    "bytes": {"type": "number"},
                    "rows": {"type": "number"},
                },
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
        control=None,
        dialect=None,
        newline=None,
        stats=None,
    ):

        # Set attributes
        self.setinitial("source", source)
        self.setinitial("scheme", scheme)
        self.setinitial("format", format)
        self.setinitial("hashing", hashing)
        self.setinitial("encoding", encoding)
        self.setinitial("compression", compression)
        self.setinitial("compressionPath", compression_path)
        self.setinitial("control", control)
        self.setinitial("dialect", dialect)
        self.setinitial("newline", newline)
        self.setinitial("stats", stats)

        # Detect attributes
        detect = helpers.detect_source_scheme_and_format(source)
        self.__detected_compression = config.DEFAULT_COMPRESSION
        self.__detected_compression_path = config.DEFAULT_COMPRESSION_PATH
        if detect[1] in config.COMPRESSION_FORMATS:
            self.__detected_compression = detect[1]
            source = source[: -len(detect[1]) - 1]
            if compression_path:
                source = os.path.join(source, compression_path)
            detect = helpers.detect_source_scheme_and_format(source)
        self.__detected_scheme = detect[0] or config.DEFAULT_SCHEME
        self.__detected_format = detect[1] or config.DEFAULT_FORMAT

        # Initialize file
        super().__init__(descriptor)

    @cached_property
    def path(self):
        return self.source if isinstance(self.source, str) else "memory"

    @cached_property
    def source(self):
        return self.get("source")

    @cached_property
    def scheme(self):
        return self.get("scheme", self.__detected_scheme)

    @cached_property
    def format(self):
        return self.get("format", self.__detected_format)

    @cached_property
    def hashing(self):
        return self.get("hashing", config.DEFAULT_HASHING)

    @cached_property
    def encoding(self):
        return self.get("encoding", config.DEFAULT_ENCODING)

    @cached_property
    def compression(self):
        return self.get("compression", self.__detected_compression)

    @cached_property
    def compression_path(self):
        return self.get("compressionPath", self.__detected_compression_path)

    @cached_property
    def control(self):
        control = self.get("control")
        if control is None:
            control = system.create_control(self, descriptor=control)
            return self.metadata_attach("control", control)
        return control

    @cached_property
    def dialect(self):
        dialect = self.get("dialect")
        if dialect is None:
            dialect = system.create_dialect(self, descriptor=dialect)
            return self.metadata_attach("dialect", dialect)
        return dialect

    @cached_property
    def newline(self):
        return self.get("newline")

    @cached_property
    def stats(self):
        return self.get("stats")

    # Expand

    def expand(self):
        self.setdefault("scheme", self.scheme)
        self.setdefault("format", self.format)
        self.setdefault("hashing", self.hashing)
        self.setdefault("encoding", self.encoding)
        self.setdefault("compression", self.compression)
        self.setdefault("compressionPath", self.compression_path)

    # Metadata

    def metadata_process(self):
        super().metadata_process()

        # Control
        control = self.get("control")
        if control is not None:
            control = system.create_control(self, descriptor=control)
            dict.__setitem__(self, "control", control)

        # Dialect
        dialect = self.get("dialect")
        if dialect is not None:
            dialect = system.create_dialect(self, descriptor=dialect)
            dict.__setitem__(self, "dialect", dialect)
