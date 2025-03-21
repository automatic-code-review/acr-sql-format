import os
import re

import automatic_code_review_commons as commons
import sqlparse


def __verify_ignore(content):
    return "acr-skip { acr-sql-format }" in content


def __extract_types(sql):
    types = []
    sql_upper = sql.upper()

    if "INSERT INTO" in sql_upper:
        if re.search(r'VALUES\s*\([^\\)]+\)\s*,\s*\(', sql_upper):
            types.append("INSERT_MULTI")
        else:
            types.append("INSERT")

    if "DELETE FROM" in sql_upper:
        types.append("DELETE")

    if "SELECT" in sql_upper:
        types.append("SELECT")

    if "UPDATE" in sql_upper:
        types.append("UPDATE")

    return types


def __format(sql):
    types = __extract_types(sql)

    if len(types) != 1:
        return False, None

    if types[0] == "INSERT":
        return True, __format_insert(sql)

    return False, None


def __format_insert(sql):
    def format_single_insert(match):
        insert_into, columns, values = match.groups()

        columns_list = [col.strip() for col in columns.split(",")]
        values_list = [val.strip() for val in values.split(",")]

        formatted_query = f"{insert_into} (\n"
        formatted_query += ",\n".join(f"    {col.lower()}" for col in columns_list)
        formatted_query += "\n) VALUES (\n"
        formatted_query += ",\n".join(f"    {val}" for val in values_list)
        formatted_query += "\n);"

        return formatted_query

    sql = sqlparse.format(sql, reindent=True, keyword_case='upper')

    formatted = re.sub(
        r"(INSERT INTO [\w\\.]+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);?",
        format_single_insert,
        sql.strip(),
        flags=re.MULTILINE | re.IGNORECASE
    )

    return formatted


def __standardize(sql):
    if sql is None:
        return sql

    while sql.endswith("\n"):
        sql = sql[0:len(sql) - 1]

    if not sql.endswith(";"):
        sql += ";"

    sql += "\n"

    return sql


def __formatted_to_string(formatted):
    return "<pre>" + "<br>".join(formatted) + "</pre>"


def __verify_regexs(data, regex_to_ignore):
    for regex in regex_to_ignore:
        if re.match(regex, data):
            return True

    return False


def verify(path, regex_to_ignore):
    print(f"Verificando arquivo {path}")

    if __verify_regexs(path, regex_to_ignore):
        return False, None

    with open(path, 'r', encoding='utf-8') as data:
        original = data.read()

    if __verify_ignore(original):
        return False, None

    accepted, formatted = __format(original)

    if not accepted:
        return False, None

    formatted = __standardize(formatted)

    return True, formatted


def review(config):
    path_source = config['path_source']
    changes = config['merge']['changes']
    comment_description_pattern = config['message']

    comments = []

    for change in changes:
        if change['deleted_file']:
            continue

        new_path = change['new_path']

        if not new_path.endswith(".sql"):
            continue

        path = os.path.join(path_source, new_path)

        with open(path, 'r', encoding='utf-8') as data:
            original = data.read()

        if __verify_ignore(original):
            continue

        accepted, formatted = __format(original)

        if not accepted:
            continue

        original = __standardize(original)
        formatted = __standardize(formatted)

        if original == formatted:
            continue

        comment_path = new_path
        comment_description = f"{comment_description_pattern}"
        comment_description = comment_description.replace("${FILE_PATH}", comment_path)
        comment_description = comment_description.replace("${FORMATTED}", __formatted_to_string(formatted.split('\n')))

        comments.append(commons.comment_create(
            comment_id=commons.comment_generate_id(comment_description),
            comment_path=comment_path,
            comment_description=comment_description,
            comment_snipset=False,
            comment_end_line=1,
            comment_start_line=1,
            comment_language="sql",
        ))

    return comments
