import pytest
from frictionless import Table, exceptions


# Read


@pytest.mark.slow
def test_table_gsheet():
    source = 'https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUFUOACPp0Lkyl7b4/edit?usp=sharing'
    with Table(source) as table:
        assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


@pytest.mark.slow
def test_table_gsheet_with_gid():
    source = 'https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUFUOACPp0Lkyl7b4/edit#gid=960698813'
    with Table(source) as table:
        assert table.read() == [['id', 'name'], ['2', '中国人'], ['3', 'german']]


@pytest.mark.skip
@pytest.mark.slow
def test_table_gsheet_bad_url():
    table = Table('https://docs.google.com/spreadsheets/d/bad')
    with pytest.raises(exceptions.HTTPError):
        table.open()
