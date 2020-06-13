import tabulator
import tableschema
from .metadata import Metadata
from . import exceptions


class Error(Metadata):
    code = 'error'
    name = 'Error'
    tags = []  # type: ignore
    template = 'Error'
    description = 'Error.'

    def __init__(self, *, details):
        self['code'] = self.code
        self['name'] = self.name
        self['tags'] = self.tags
        self['details'] = details
        self['message'] = self.template.format(**self)
        self['description'] = self.description

    @property
    def details(self):
        return self['details']

    @property
    def message(self):
        return self['message']

    # Helpers

    @staticmethod
    def from_exception(exception):
        Error = SourceError
        details = str(exception)
        if isinstance(exception, tabulator.exceptions.SourceError):
            Error = SourceError
        elif isinstance(exception, tabulator.exceptions.SchemeError):
            Error = SchemeError
        elif isinstance(exception, tabulator.exceptions.FormatError):
            Error = FormatError
        elif isinstance(exception, tabulator.exceptions.EncodingError):
            Error = EncodingError
        elif isinstance(exception, tabulator.exceptions.CompressionError):
            Error = CompressionError
        elif isinstance(exception, tableschema.exceptions.TableSchemaException):
            Error = SchemaError
        return Error(details=details)


class HeaderError(Error):
    code = 'header-error'
    name = 'Header Error'
    tags = ['#head']
    template = 'Cell Error'
    description = 'Cell Error'

    def __init__(self, *, details, cells, cell, field_name, field_number, field_position):
        self['cells'] = cells
        self['cell'] = cell
        self['fieldName'] = field_name
        self['fieldNumber'] = field_number
        self['fieldPosition'] = field_position
        super().__init__(details=details)


class RowError(Error):
    code = 'row-error'
    name = 'Row Error'
    tags = ['#body']
    template = 'Row Error'
    description = 'Row Error'

    def __init__(self, *, details, cells, row_number, row_position):
        self['cells'] = cells
        self['rowNumber'] = row_number
        self['rowPosition'] = row_position
        super().__init__(details=details)

    # Helpers

    @classmethod
    def from_row(cls, row, *, details):
        return cls(
            details=details,
            cells=list(map(str, row.values())),
            row_number=row.row_number,
            row_position=row.row_position,
        )


class CellError(RowError):
    code = 'cell-error'
    name = 'Cell Error'
    tags = ['#body']
    template = 'Cell Error'
    description = 'Cell Error'

    def __init__(
        self,
        *,
        details,
        cells,
        row_number,
        row_position,
        cell,
        field_name,
        field_number,
        field_position,
    ):
        self['cell'] = cell
        self['fieldName'] = field_name
        self['fieldNumber'] = field_number
        self['fieldPosition'] = field_position
        super().__init__(
            details=details, cells=cells, row_number=row_number, row_position=row_position
        )

    # Helpers

    @classmethod
    def from_row(cls, row, *, details, field_name):
        # This algorithm can be optimized by storing more information in a row
        # At the same time, this function should not be called very often
        for field_number, [name, cell] in enumerate(row.items(), start=1):
            if field_name == name:
                field_position = row.field_positions[field_number - 1]
                return cls(
                    details=details,
                    cells=list(map(str, row.values())),
                    row_number=row.row_number,
                    row_position=row.row_position,
                    cell=str(cell),
                    field_name=field_name,
                    field_number=field_number,
                    field_position=field_position,
                )
        message = f'Field {field_name} is not in the row'
        raise exceptions.FrictionlessException(message)


# Metadata


class TaskError(Error):
    code = 'task-error'
    name = 'Task Error'
    tags = ['#metadata']
    template = 'The validation task has an error: {details}'
    description = 'General task-level error.'


class ReportError(Error):
    code = 'report-error'
    name = 'Report Error'
    tags = ['#metadata']
    template = 'The validation report has an error: {details}'
    description = 'A validation cannot be presented.'


class PackageError(Error):
    code = 'package-error'
    name = 'Package Error'
    tags = ['#metadata']
    template = 'The data package has an error: {details}'
    description = 'A validation cannot be processed.'


class ResourceError(Error):
    code = 'resource-error'
    name = 'Resource Error'
    tags = ['#metadata']
    template = 'The data resource has an error: {details}'
    description = 'A validation cannot be processed.'


class SchemaError(Error):
    code = 'schema-error'
    name = 'Schema Error'
    tags = ['#metadata']
    template = 'The data source could not be successfully described by the invalid Table Schema: {details}'
    description = 'Provided schema is not valid.'


# Table


class SourceError(Error):
    code = 'source-error'
    name = 'Source Error'
    tags = ['#table']
    template = 'The data source has not supported or has inconsistent contents: {details}'
    description = 'Data reading error because of not supported or inconsistent contents.'


class SchemeError(Error):
    code = 'scheme-error'
    name = 'Scheme Error'
    tags = ['#table']
    template = 'The data source could not be successfully loaded: {details}'
    description = 'Data reading error because of incorrect scheme.'


class FormatError(Error):
    code = 'format-error'
    name = 'Format Error'
    tags = ['#table']
    template = 'The data source could not be successfully parsed: {details}'
    description = 'Data reading error because of incorrect format.'


class EncodingError(Error):
    code = 'encoding-error'
    name = 'Encoding Error'
    tags = ['#table']
    template = 'The data source could not be successfully decoded: {details}'
    description = 'Data reading error because of an encoding problem.'


class CompressionError(Error):
    code = 'compression-error'
    name = 'Compression Error'
    tags = ['#table']
    template = 'The data source could not be successfully decompressed: {details}'
    description = 'Data reading error because of a decompression problem.'


class SizeError(Error):
    code = 'size-error'
    name = 'Size Error'
    tags = ['#table', '#integrity']
    template = 'The data source does not match the expected size in bytes: {details}'
    description = 'This error can happen if the data is corrupted.'


class HashError(Error):
    code = 'hash-error'
    name = 'Hash Error'
    tags = ['#table', '#integrity']
    template = 'The data source does not match the expected hash: {details}'
    description = 'This error can happen if the data is corrupted.'


# Head


class ExtraHeaderError(HeaderError):
    code = 'extra-header'
    name = 'Extra Header'
    tags = ['#head', '#structure']
    template = 'There is an extra header "{cell}" in field at position "{fieldPosition}"'
    description = 'The first row of the data source contains header that does not exist in the schema.'


class MissingHeaderError(HeaderError):
    code = 'missing-header'
    name = 'Missing Header'
    tags = ['#head', '#structure']
    template = 'There is a missing header in the field "{fieldName}" at position "{fieldPosition}"'
    description = 'Based on the schema there should be a header that is missing in the first row of the data source.'


class BlankHeaderError(HeaderError):
    code = 'blank-header'
    name = 'Blank Header'
    tags = ['#head', '#structure']
    template = 'Header in field at position "{fieldPosition}" is blank'
    description = 'A column in the header row is missing a value. Headers should be provided and not be blank.'


class DuplicateHeaderError(HeaderError):
    code = 'duplicate-header'
    name = 'Duplicate Header'
    tags = ['#head', '#structure']
    template = 'Header "{cell}" in field at position "{fieldPosition}" is duplicated to header in another field: {details}'
    description = 'Two columns in the header row have the same value. Column names should be unique.'


class NonMatchingHeaderError(HeaderError):
    code = 'non-matching-header'
    name = 'Non-matching Header'
    tags = ['#head', '#schema']
    template = 'Header "{cell}" in field {fieldName} at position "{fieldPosition}" does not match the field name in the schema'
    description = 'One of the data source headers does not match the field name defined in the schema.'


# Body


class ExtraCellError(CellError):
    code = 'extra-cell'
    name = 'Extra Cell'
    tags = ['#body', '#structure']
    template = 'Row at position "{rowPosition}" has an extra value in field at position "{fieldPosition}"'
    description = 'This row has more values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns.'


class MissingCellError(CellError):
    code = 'missing-cell'
    name = 'Missing Cell'
    tags = ['#body', '#structure']
    template = 'Row at position "{rowPosition}" has a missing cell in field "{fieldName}" at position "{fieldPosition}"'
    description = 'This row has less values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns.'


class BlankRowError(RowError):
    code = 'blank-row'
    name = 'Blank Row'
    tags = ['#body', '#structure']
    template = 'Row at position "{rowPosition}" is completely blank'
    description = 'This row is empty. A row should contain at least one value.'


class RequiredError(CellError):
    code = 'required-error'
    name = 'Required Error'
    tags = ['#body', '#schema']
    template = 'Field "{fieldName}" at position "{fieldPosition}" is a required field, but row at position "{rowPosition}" has no value'
    description = 'This field is a required field, but it contains no value.'


class TypeError(CellError):
    code = 'type-error'
    name = 'Missing Cell'
    tags = ['#body', '#schema']
    template = 'The cell "{cell}" in row at position "{rowPosition}" and field "{fieldName}" at position "{fieldPosition}" has incompatible type: {details}'
    description = 'The value does not match the schema type and format for this field.'


class ConstraintError(CellError):
    code = 'constraint-error'
    name = 'Constraint Error'
    tags = ['#body', '#schema']
    template = 'The cell "{cell}" in row at position "{rowPosition}" and field "{fieldName}" at position "{fieldPosition}" does not conform to a constraint: {details}'
    description = 'A field value does not conform to a constraint.'


class UniqueError(CellError):
    code = 'unique-error'
    name = 'Unique Error'
    tags = ['#body', '#schema', '#integrity']
    template = 'Row at position "{rowPosition}" has unique constraint violation in field "{fieldName}" at position "{fieldPosition}": {details}'
    description = 'This field is a unique field but it contains a value that has been used in another row.'


class PrimaryKeyError(RowError):
    code = 'primary-key-error'
    name = 'PrimaryKey Error'
    tags = ['#body', '#schema', '#integrity']
    template = 'The row at position "{rowPosition}" does not conform to the primary key constraint: {details}'
    description = 'Values in the primary key fields should be unique for every row'


class ForeignKeyError(RowError):
    code = 'foreign-key-error'
    name = 'ForeignKey Error'
    tags = ['#body', '#schema', '#integrity']
    template = 'The row at position "{rowPosition}" does not conform to the foreign key constraint: {details}'
    description = 'Values in the foreign key fields should exist in the reference table'