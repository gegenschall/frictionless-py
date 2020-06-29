import pytest
from frictionless import Table
from frictionless.plugins.html import HtmlDialect


# Read


@pytest.mark.parametrize(
    "source, selector",
    [
        ("data/table1.html", "table"),
        ("data/table2.html", "table"),
        ("data/table3.html", ".mememe"),
        ("data/table4.html", ""),
    ],
)
def test_table_html(source, selector):
    dialect = HtmlDialect(selector=selector)
    with Table(source, dialect=dialect) as table:
        assert table.headers == ["id", "name"]
        assert table.read_data() == [["1", "english"], ["2", "中国人"]]
