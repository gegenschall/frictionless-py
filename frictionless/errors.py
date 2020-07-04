from .metadata import Metadata
from . import exceptions


class Error(Metadata):
    """Error representation

    # Arguments
        descriptor? (str|dict): error descriptor

        note (str): note

    # Raises
        FrictionlessException: raise any error that occurs during the process

    """

    code = "error"
    name = "Error"
    tags = []  # type: ignore
    template = "{note}"
    description = "Error."

    def __init__(self, descriptor=None, *, note):
        self["code"] = self.code
        self["name"] = self.name
        self["tags"] = self.tags
        self["note"] = note
        self["message"] = self.template.format(**self)
        self["description"] = self.description
        super().__init__(descriptor)

    @property
    def note(self):
        return self["note"]

    @property
    def message(self):
        return self["message"]


class HeaderError(Error):
    """Header error representation

    # Arguments
        descriptor? (str|dict): error descriptor

        note (str): note
        cells (any[]): cells
        cell (any): cell
        field_name (str): field_name
        field_number (int): field_number
        field_position (int): field_position

    # Raises
        FrictionlessException: raise any error that occurs during the process

    """

    code = "header-error"
    name = "Header Error"
    tags = ["#head"]
    template = "Cell Error"
    description = "Cell Error"

    def __init__(
        self,
        descriptor=None,
        *,
        note,
        cells,
        cell,
        field_name,
        field_number,
        field_position,
    ):
        self["cells"] = cells
        self["cell"] = cell
        self["fieldName"] = field_name
        self["fieldNumber"] = field_number
        self["fieldPosition"] = field_position
        super().__init__(descriptor, note=note)


class RowError(Error):
    """Row error representation

    # Arguments
        descriptor? (str|dict): error descriptor

        cells (any[]): cells
        row_number (int): row_number
        row_position (int): row_position

    # Raises
        FrictionlessException: raise any error that occurs during the process

    """

    code = "row-error"
    name = "Row Error"
    tags = ["#body"]
    template = "Row Error"
    description = "Row Error"

    def __init__(self, descriptor=None, *, note, cells, row_number, row_position):
        self["cells"] = cells
        self["rowNumber"] = row_number
        self["rowPosition"] = row_position
        super().__init__(descriptor, note=note)

    # Create

    @classmethod
    def from_row(cls, row, *, note):
        return cls(
            note=note,
            cells=list(map(str, row.values())),
            row_number=row.row_number,
            row_position=row.row_position,
        )


class CellError(RowError):
    """Cell error representation

    # Arguments
        descriptor? (str|dict): error descriptor

        note (str): note
        cells (any[]): cells
        row_number (int): row_number
        row_position (int): row_position
        cell (any): cell
        field_name (str): field_name
        field_number (int): field_number
        field_position (int): field_position

    # Raises
        FrictionlessException: raise any error that occurs during the process

    """

    code = "cell-error"
    name = "Cell Error"
    tags = ["#body"]
    template = "Cell Error"
    description = "Cell Error"

    def __init__(
        self,
        descriptor=None,
        *,
        note,
        cells,
        row_number,
        row_position,
        cell,
        field_name,
        field_number,
        field_position,
    ):
        self["cell"] = cell
        self["fieldName"] = field_name
        self["fieldNumber"] = field_number
        self["fieldPosition"] = field_position
        super().__init__(
            descriptor,
            note=note,
            cells=cells,
            row_number=row_number,
            row_position=row_position,
        )

    # Create

    @classmethod
    def from_row(cls, row, *, note, field_name):
        # This algorithm can be optimized by storing more information in a row
        # At the same time, this function should not be called very often
        for field_number, [name, cell] in enumerate(row.items(), start=1):
            if field_name == name:
                field_position = row.field_positions[field_number - 1]
                return cls(
                    note=note,
                    cells=list(map(str, row.values())),
                    row_number=row.row_number,
                    row_position=row.row_position,
                    cell=str(cell),
                    field_name=field_name,
                    field_number=field_number,
                    field_position=field_position,
                )
        error = Error(note=f"Field {field_name} is not in the row")
        raise exceptions.FrictionlessException(error)


# General


class PackageError(Error):
    code = "package-error"
    name = "Package Error"
    tags = ["#general"]
    template = "The data package has an error: {note}"
    description = "A validation cannot be processed."


class ResourceError(Error):
    code = "resource-error"
    name = "Resource Error"
    tags = ["#general"]
    template = "The data resource has an error: {note}"
    description = "A validation cannot be processed."


class ReportError(Error):
    code = "report-error"
    name = "Report Error"
    tags = ["#general"]
    template = "The validation report has an error: {note}"
    description = "A validation cannot be presented."


class TaskError(Error):
    code = "task-error"
    name = "Task Error"
    tags = ["#general"]
    template = "The validation task has an error: {note}"
    description = "General task-level error."


class CheckError(Error):
    code = "check-error"
    name = "Check Error"
    tags = ["#general"]
    template = "The validation check has an error: {note}"
    description = "A validation check cannot be created"


# Table


class SourceError(Error):
    code = "source-error"
    name = "Source Error"
    tags = ["#table"]
    template = "The data source has not supported or has inconsistent contents: {note}"
    description = "Data reading error because of not supported or inconsistent contents."


class SchemeError(Error):
    code = "scheme-error"
    name = "Scheme Error"
    tags = ["#table"]
    template = "The data source could not be successfully loaded: {note}"
    description = "Data reading error because of incorrect scheme."


class FormatError(Error):
    code = "format-error"
    name = "Format Error"
    tags = ["#table"]
    template = "The data source could not be successfully parsed: {note}"
    description = "Data reading error because of incorrect format."


class EncodingError(Error):
    code = "encoding-error"
    name = "Encoding Error"
    tags = ["#table"]
    template = "The data source could not be successfully decoded: {note}"
    description = "Data reading error because of an encoding problem."


class HashingError(Error):
    code = "hashing-error"
    name = "Hashing Error"
    tags = ["#table"]
    template = "The data source could not be successfully hashed: {note}"
    description = "Data reading error because of a hashing problem."


class CompressionError(Error):
    code = "compression-error"
    name = "Compression Error"
    tags = ["#table"]
    template = "The data source could not be successfully decompressed: {note}"
    description = "Data reading error because of a decompression problem."


class SchemaError(Error):
    code = "schema-error"
    name = "Schema Error"
    tags = ["#table", "#schema"]
    template = "The data source could not be successfully described by the invalid Table Schema: {note}"
    description = "Provided schema is not valid."


class ChecksumError(Error):
    code = "checksum-error"
    name = "Checksum Error"
    tags = ["#table", "#integrity"]
    template = "The data source does not match the expected checksum: {note}"
    description = "This error can happen if the data is corrupted."


# Head


class ExtraHeaderError(HeaderError):
    code = "extra-header"
    name = "Extra Header"
    tags = ["#head", "#structure"]
    template = 'There is an extra header "{cell}" in field at position "{fieldPosition}"'
    description = "The first row of the data source contains header that does not exist in the schema."


class MissingHeaderError(HeaderError):
    code = "missing-header"
    name = "Missing Header"
    tags = ["#head", "#structure"]
    template = 'There is a missing header in the field "{fieldName}" at position "{fieldPosition}"'
    description = "Based on the schema there should be a header that is missing in the first row of the data source."


class BlankHeaderError(HeaderError):
    code = "blank-header"
    name = "Blank Header"
    tags = ["#head", "#structure"]
    template = 'Header in field at position "{fieldPosition}" is blank'
    description = "A column in the header row is missing a value. Headers should be provided and not be blank."


class DuplicateHeaderError(HeaderError):
    code = "duplicate-header"
    name = "Duplicate Header"
    tags = ["#head", "#structure"]
    template = 'Header "{cell}" in field at position "{fieldPosition}" is duplicated to header in another field: {note}'
    description = "Two columns in the header row have the same value. Column names should be unique."


class NonMatchingHeaderError(HeaderError):
    code = "non-matching-header"
    name = "Non-matching Header"
    tags = ["#head", "#schema"]
    template = 'Header "{cell}" in field {fieldName} at position "{fieldPosition}" does not match the field name in the schema'
    description = "One of the data source headers does not match the field name defined in the schema."


# Body


class ExtraCellError(CellError):
    code = "extra-cell"
    name = "Extra Cell"
    tags = ["#body", "#structure"]
    template = 'Row at position "{rowPosition}" has an extra value in field at position "{fieldPosition}"'
    description = "This row has more values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns."


class MissingCellError(CellError):
    code = "missing-cell"
    name = "Missing Cell"
    tags = ["#body", "#structure"]
    template = 'Row at position "{rowPosition}" has a missing cell in field "{fieldName}" at position "{fieldPosition}"'
    description = "This row has less values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns."


class BlankRowError(RowError):
    code = "blank-row"
    name = "Blank Row"
    tags = ["#body", "#structure"]
    template = 'Row at position "{rowPosition}" is completely blank'
    description = "This row is empty. A row should contain at least one value."


# TODO: merge with ConstraintError
class RequiredError(CellError):
    code = "required-error"
    name = "Required Error"
    tags = ["#body", "#schema"]
    template = 'Field "{fieldName}" at position "{fieldPosition}" is a required field, but row at position "{rowPosition}" has no value'
    description = "This field is a required field, but it contains no value."


class TypeError(CellError):
    code = "type-error"
    name = "Missing Cell"
    tags = ["#body", "#schema"]
    template = 'The cell "{cell}" in row at position "{rowPosition}" and field "{fieldName}" at position "{fieldPosition}" has incompatible type: {note}'
    description = "The value does not match the schema type and format for this field."


class ConstraintError(CellError):
    code = "constraint-error"
    name = "Constraint Error"
    tags = ["#body", "#schema"]
    template = 'The cell "{cell}" in row at position "{rowPosition}" and field "{fieldName}" at position "{fieldPosition}" does not conform to a constraint: {note}'
    description = "A field value does not conform to a constraint."


class UniqueError(CellError):
    code = "unique-error"
    name = "Unique Error"
    tags = ["#body", "#schema", "#integrity"]
    template = 'Row at position "{rowPosition}" has unique constraint violation in field "{fieldName}" at position "{fieldPosition}": {note}'
    description = "This field is a unique field but it contains a value that has been used in another row."


class PrimaryKeyError(RowError):
    code = "primary-key-error"
    name = "PrimaryKey Error"
    tags = ["#body", "#schema", "#integrity"]
    template = 'The row at position "{rowPosition}" does not conform to the primary key constraint: {note}'
    description = "Values in the primary key fields should be unique for every row"


class ForeignKeyError(RowError):
    code = "foreign-key-error"
    name = "ForeignKey Error"
    tags = ["#body", "#schema", "#integrity"]
    template = 'The row at position "{rowPosition}" does not conform to the foreign key constraint: {note}'
    description = "Values in the foreign key fields should exist in the reference table"


# Misc


class DuplicateRowError(RowError):
    code = "duplicate-row"
    name = "Duplicate Row"
    tags = ["#body", "#heuristic"]
    template = "Row at position {rowPosition} is duplicated: {note}"
    description = "The row is duplicated."


class DeviatedValueError(Error):
    code = "deviated-value"
    name = "Deviated Value"
    tags = ["#body", "#heuristic"]
    template = "There is a possible error because the value is deviated: {note}"
    description = "The value is deviated."


class TruncatedValueError(CellError):
    code = "truncated-value"
    name = "Truncated Value"
    tags = ["#body", "#heuristic"]
    template = "The cell {cell} in row at position {rowPosition} and field {fieldName} at position {fieldPosition} has an error: {note}"
    description = "The value is possible truncated."


class BlacklistedValueError(CellError):
    code = "blacklisted-value"
    name = "Blacklisted Value"
    tags = ["#body", "#regulation"]
    template = "The cell {cell} in row at position {rowPosition} and field {fieldName} at position {fieldPosition} has an error: {note}"
    description = "The value is blacklisted."


class SequentialValueError(CellError):
    code = "sequential-value"
    name = "Sequential Value"
    tags = ["#body", "#regulation"]
    template = "The cell {cell} in row at position {rowPosition} and field {fieldName} at position {fieldPosition} has an error: {note}"
    description = "The value is not sequential."


class RowConstraintError(RowError):
    code = "row-constraint"
    name = "Row Constraint"
    tags = ["#body", "#regulation"]
    template = "The row at position {rowPosition} has an error: {note}"
    description = "The value does not conform to the row constraint."
