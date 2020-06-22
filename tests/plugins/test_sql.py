import pytest
from frictionless import Table, exceptions


# Read


def test_table_format_sql(database_url):
    with Table(database_url, table='data') as table:
        assert table.read() == [[1, 'english'], [2, '中国人']]


def test_table_format_sql_order_by(database_url):
    with Table(database_url, table='data', order_by='id') as table:
        assert table.read() == [[1, 'english'], [2, '中国人']]


def test_table_format_sql_order_by_desc(database_url):
    with Table(database_url, table='data', order_by='id desc') as table:
        assert table.read() == [[2, '中国人'], [1, 'english']]


def test_table_format_sql_table_is_required_error(database_url):
    with pytest.raises(exceptions.TabulatorException) as excinfo:
        Table(database_url).open()
    assert 'table' in str(excinfo.value)


def test_table_format_sql_headers(database_url):
    with Table(database_url, table='data', headers=1) as table:
        assert table.headers == ['id', 'name']
        assert table.read() == [[1, 'english'], [2, '中国人']]


# Write


def test_table_save_sqlite(database_url):
    source = 'data/table.csv'
    with Table(source, headers=1) as table:
        assert table.save(database_url, table='test_table_save_sqlite') == 2
    with Table(
        database_url, table='test_table_save_sqlite', order_by='id', headers=1
    ) as table:
        assert table.read() == [['1', 'english'], ['2', '中国人']]
        assert table.headers == ['id', 'name']