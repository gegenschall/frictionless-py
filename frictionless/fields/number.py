import re
from decimal import Decimal
from ..helpers import cached_property
from ..field import Field


class NumberField(Field):
    supported_constraints = [
        'required',
        'minimum',
        'maximum',
        'enum',
    ]

    # Read

    def read_cell_cast(self, cell):
        if isinstance(cell, str):
            if self.read_cell_cast_processor:
                cell = self.read_cell_cast_processor(cell)
            try:
                return Decimal(cell)
            except Exception:
                return None
        elif isinstance(cell, Decimal):
            return cell
        elif cell is True or cell is False:
            return None
        elif isinstance(cell, int):
            return cell
        elif isinstance(cell, float):
            return Decimal(str(cell))
        return None

    @cached_property
    def read_cell_cast_processor(self):
        if set(['groupChar', 'decimalChar', 'bareNumber']).intersection(self.keys()):
            group_char = self.get('groupChar', DEFAULT_GROUP_CHAR)
            decimal_char = self.get('decimalChar', DEFAULT_DECIMAL_CHAR)

            def processor(cell):
                cell = cell.replace(group_char, '')
                cell = cell.replace(decimal_char, '.')
                if self.read_cell_cast_pattern:
                    cell = self.read_cell_cast_pattern.sub('', cell)
                return cell

            return processor

    @cached_property
    def read_cell_cast_pattern(self):
        if not self.get('bareNumber', DEFAULT_BARE_NUMBER):
            return re.compile(r'((^\D*)|(\D*$))')

    # Write

    def write_cell_cast(self, cell):
        return str(cell)


# Internal

DEFAULT_GROUP_CHAR = ''
DEFAULT_DECIMAL_CHAR = '.'
DEFAULT_BARE_NUMBER = True
