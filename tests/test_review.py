import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import review

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def __read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as data:
        return data.read()


def __save_output(name, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, name), "w", encoding="utf-8") as data:
        data.write(content)


def test_format_delete_in_clause_with_bind_param(tmp_path):
    sql = __read_fixture("delete_in_input.sql")

    path = tmp_path / "delete_in.sql"
    path.write_text(sql, encoding="utf-8")

    changed, formatted = review.verify(str(path), regex_to_ignore=[])

    __save_output("delete_in_formatted.sql", formatted or "")

    expected = __read_fixture("delete_in_expected.sql")

    assert changed is True
    assert formatted == expected


def test_format_delete_multiple_in_clauses_with_and(tmp_path):
    sql = __read_fixture("delete_multi_in_input.sql")

    path = tmp_path / "delete_multi_in.sql"
    path.write_text(sql, encoding="utf-8")

    changed, formatted = review.verify(str(path), regex_to_ignore=[])

    __save_output("delete_multi_in_formatted.sql", formatted or "")

    expected = __read_fixture("delete_multi_in_expected.sql")

    assert changed is True
    assert formatted == expected
