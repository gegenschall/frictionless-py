import io
import json
import requests
import jsonschema
import stringcase
from copy import deepcopy
from operator import setitem
from functools import partial
from importlib import import_module
from .helpers import cached_property
from . import exceptions
from . import helpers


class Metadata(helpers.ControlledDict):
    """Metadata representation

    # Arguments
        descriptor? (str|dict): schema descriptor

    # Raises
        FrictionlessException: raise any error that occurs during the process

    """

    metadata_Error = None
    metadata_profile = None
    metadata_strict = False
    metadata_duplicate = False

    def __init__(self, descriptor=None):
        self.__Error = self.metadata_Error or import_module("frictionless.errors").Error
        metadata = self.metadata_extract(descriptor)
        for key, value in metadata.items():
            dict.setdefault(self, key, value)
        self.__onchange__()

    def __setattr__(self, name, value):
        if hasattr(self, "_Metadata__Error"):
            attr = type(self).__dict__.get(name)
            if attr:
                write = getattr(attr, "metadata_write", None)
                if write:
                    if callable(write):
                        return callable(self, value)
                    return setitem(self, stringcase.camelcase(name), value)
        return super().__setattr__(name, value)

    def __onchange__(self, onchange=None):
        super().__onchange__(onchange)
        if hasattr(self, "_Metadata__Error"):
            for key, attr in type(self).__dict__.items():
                reset = getattr(attr, "metadata_reset", None)
                if reset and key in self.__dict__:
                    self.__dict__.pop(key)
            self.metadata_process()
            if self.metadata_strict:
                for error in self.metadata_errors:
                    raise exceptions.FrictionlessException(error)

    @property
    def metadata_valid(self):
        return not len(self.metadata_errors)

    @property
    def metadata_errors(self):
        return list(self.metadata_validate())

    def setinitial(self, key, value):
        if value is not None:
            dict.__setitem__(self, key, value)

    # Import/Export

    def to_dict(self):
        return self.copy()

    # Attach

    def metadata_attach(self, name, value):
        if self.get(name) is not value:
            onchange = partial(metadata_attach, self, name)
            if isinstance(value, dict):
                if not isinstance(value, Metadata):
                    value = helpers.ControlledDict(value)
                value.__onchange__(onchange)
            elif isinstance(value, list):
                value = helpers.ControlledList(value)
                value.__onchange__(onchange)
        return value

    # Extract

    # TODO: support yaml?
    def metadata_extract(self, descriptor):
        try:
            if descriptor is None:
                return {}
            if isinstance(descriptor, dict):
                return deepcopy(descriptor) if self.metadata_duplicate else descriptor
            if isinstance(descriptor, str):
                if helpers.is_remote_path(descriptor):
                    response = requests.get(descriptor)
                    response.raise_for_status()
                    metadata = response.json()
                    assert isinstance(metadata, dict)
                    return metadata
                with io.open(descriptor, encoding="utf-8") as file:
                    metadata = json.load(file)
                    assert isinstance(metadata, dict)
                    return metadata
            raise TypeError("descriptor type is not supported")
        except Exception as exception:
            note = f'canot extract metadata "{descriptor}" because "{exception}"'
            raise exceptions.FrictionlessException(self.__Error(note=note)) from exception

    # Process

    def metadata_process(self):
        pass

    # Validate

    def metadata_validate(self):
        if self.metadata_profile:
            validator_class = jsonschema.validators.validator_for(self.metadata_profile)
            validator = validator_class(self.metadata_profile)
            for error in validator.iter_errors(self):
                metadata_path = "/".join(map(str, error.path))
                profile_path = "/".join(map(str, error.schema_path))
                note = '"%s" at "%s" in metadata and at "%s" in profile'
                note = note % (error.message, metadata_path, profile_path)
                yield self.__Error(note=note)
        yield from []

    # Save

    def metadata_save(self, target):
        try:
            helpers.ensure_dir(target)
            with io.open(target, mode="w", encoding="utf-8") as file:
                json.dump(self, file, indent=2, ensure_ascii=False)
        except Exception as exc:
            raise exceptions.FrictionlessException(self.__Error(note=str(exc))) from exc

    # Helpers

    @staticmethod
    def property(func=None, *, reset=True, write=True):

        # Actual property
        def metadata_property(func):
            prop = cached_property(func)
            setattr(prop, "metadata_reset", reset)
            setattr(prop, "metadata_write", write)
            return prop

        # Allow both forms
        return metadata_property(func) if func else metadata_property


# Internal


def metadata_attach(self, name, value):
    copy = dict if isinstance(value, dict) else list
    setitem(self, name, copy(value))
