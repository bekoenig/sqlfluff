"""Db2 dialect-specific parser tests.

Positive SQL cases live in ``test/fixtures/dialects/db2/``. These tests pin
the shape of Db2-specific trailing clauses on ``CREATE TABLE`` so that they
are modelled as dedicated segments instead of generic keywords or aliases.
"""

import pytest

from sqlfluff.core import Linter

TRAILING_CLAUSE_CASES = [
    pytest.param(
        "CREATE TABLE t (a INT) ORGANIZE BY ROW;",
        "table_organization_clause",
        id="organize_by_row",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) ORGANIZE BY COLUMN;",
        "table_organization_clause",
        id="organize_by_column",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) DISTRIBUTE BY HASH (a);",
        "distribution_clause",
        id="distribute_by_hash",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) DISTRIBUTE BY RANDOM;",
        "distribution_clause",
        id="distribute_by_random",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) DISTRIBUTE BY REPLICATION;",
        "distribution_clause",
        id="distribute_by_replication",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) IN ts;",
        "tablespace_clause",
        id="in_tablespace",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) IN ts INDEX IN ts2 LONG IN ts3;",
        "tablespace_clause",
        id="in_tablespace_with_index_and_long",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) WITH RESTRICT ON DROP;",
        "with_restrict_on_drop_clause",
        id="with_restrict_on_drop",
    ),
]


@pytest.mark.parametrize("sql,expected_type", TRAILING_CLAUSE_CASES)
def test_create_table_trailing_clause(sql: str, expected_type: str) -> None:
    """Db2 trailing clauses parse into their own segment types."""
    parsed = Linter(dialect="db2").parse_string(sql)
    assert parsed.tree is not None
    types = parsed.tree.type_set()
    assert "unparsable" not in types, f"Unparsable section in: {sql}"
    assert expected_type in types, f"Expected {expected_type} in {sorted(types)}"


def test_create_table_trailing_clauses_combined() -> None:
    """All Db2 trailing clauses can be combined on one table."""
    sql = (
        "CREATE TABLE t (a INT) "
        "ORGANIZE BY ROW "
        "DISTRIBUTE BY HASH (a) "
        "IN ts INDEX IN ts2 LONG IN ts3 "
        "WITH RESTRICT ON DROP;"
    )
    parsed = Linter(dialect="db2").parse_string(sql)
    assert parsed.tree is not None
    types = parsed.tree.type_set()
    assert "unparsable" not in types, f"Unparsable section in: {sql}"
    assert {
        "table_organization_clause",
        "distribution_clause",
        "tablespace_clause",
        "with_restrict_on_drop_clause",
    } <= types


TABLE_OPTION_CASES = [
    pytest.param(
        "CREATE TABLE t (a INT) COMPRESS YES;",
        "compress_clause",
        id="compress_yes",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) COMPRESS YES ADAPTIVE;",
        "compress_clause",
        id="compress_yes_adaptive",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) COMPRESS YES STATIC;",
        "compress_clause",
        id="compress_yes_static",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) COMPRESS NO;",
        "compress_clause",
        id="compress_no",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) VALUE COMPRESSION;",
        "value_compression_clause",
        id="value_compression",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) DATA CAPTURE NONE;",
        "data_capture_clause",
        id="data_capture_none",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) DATA CAPTURE CHANGES;",
        "data_capture_clause",
        id="data_capture_changes",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) NOT LOGGED INITIALLY;",
        "not_logged_initially_clause",
        id="not_logged_initially",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) CCSID UNICODE;",
        "ccsid_clause",
        id="ccsid_unicode",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) CCSID ASCII;",
        "ccsid_clause",
        id="ccsid_ascii",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) CCSID 1208;",
        "ccsid_clause",
        id="ccsid_numeric",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) SECURITY POLICY p;",
        "security_policy_clause",
        id="security_policy",
    ),
    pytest.param(
        "CREATE TABLE t (a INT) OPTIONS (remote_table 's.t');",
        "table_options",
        id="table_options",
    ),
]


@pytest.mark.parametrize("sql,expected_type", TABLE_OPTION_CASES)
def test_create_table_table_option(sql: str, expected_type: str) -> None:
    """Db2 table options parse into their own segment types."""
    parsed = Linter(dialect="db2").parse_string(sql)
    assert parsed.tree is not None
    types = parsed.tree.type_set()
    assert "unparsable" not in types, f"Unparsable section in: {sql}"
    assert expected_type in types, f"Expected {expected_type} in {sorted(types)}"


def test_create_table_table_options_combined() -> None:
    """Table options can be combined with the other trailing clauses."""
    sql = (
        "CREATE TABLE t (a INT) "
        "ORGANIZE BY ROW "
        "COMPRESS YES ADAPTIVE "
        "VALUE COMPRESSION "
        "DATA CAPTURE CHANGES "
        "NOT LOGGED INITIALLY "
        "CCSID UNICODE "
        "SECURITY POLICY p "
        "OPTIONS (remote_table 's.t');"
    )
    parsed = Linter(dialect="db2").parse_string(sql)
    assert parsed.tree is not None
    types = parsed.tree.type_set()
    assert "unparsable" not in types, f"Unparsable section in: {sql}"
    assert {
        "table_organization_clause",
        "compress_clause",
        "value_compression_clause",
        "data_capture_clause",
        "not_logged_initially_clause",
        "ccsid_clause",
        "security_policy_clause",
        "table_options",
    } <= types
