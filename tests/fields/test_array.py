import pytest
from frictionless import Field


# General


@pytest.mark.parametrize(
    'format, source, target',
    [
        ('default', [], []),
        ('default', (), []),
        ('default', '[]', []),
        ('default', ['key', 'value'], ['key', 'value']),
        ('default', ('key', 'value'), ['key', 'value']),
        ('default', '["key", "value"]', ['key', 'value']),
        ('default', {'key': 'value'}, None),
        ('default', '{"key": "value"}', None),
        ('default', 'string', None),
        ('default', 1, None),
        ('default', '3.14', None),
        ('default', '', None),
    ],
)
def test_read_cell_array(format, source, target):
    field = Field({'name': 'name', 'type': 'array', 'format': format})
    cell, note = field.read_cell(source)
    assert cell == target