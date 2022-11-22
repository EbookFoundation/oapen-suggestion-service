from typing import List

import psycopg2
from data.connection import connection
from model.oapen_types import NgramRow, SuggestionRow


def mogrify_ngrams(ngrams: List[NgramRow]) -> str:
    cursor = connection.cursor()
    args = ",".join(
        cursor.mogrify("(%s,%s::oapen_suggestions.ngram[])", x).decode("utf-8")
        for x in ngrams
    )
    return args


def mogrify_suggestions(suggestions: List[SuggestionRow]) -> str:
    cursor = connection.cursor()
    args = ",".join(
        cursor.mogrify("(%s,%s,%s::oapen_suggestions.suggestion[])", x).decode("utf-8")
        for x in suggestions
    )
    return args


def table_exists(table):
    cursor = connection.cursor
    query = """
            SELECT EXISTS (
                SELECT * FROM oapen_suggestions.tables WHERE table_name=%s
            )
            """

    try:
        cursor.execute(query, (table))
        res = cursor.fetchone()[0]
        return res
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def add_single_suggestion(suggestion: SuggestionRow) -> None:
    cursor = connection.cursor()
    query = """
            INSERT INTO oapen_suggestions.suggestions (handle, name, suggestions)
            VALUES (%s, %s, %s::oapen_suggestions.suggestion[])
            ON CONFLICT (handle)
            DO
                UPDATE SET suggestions = excluded.suggestions
            """

    try:
        cursor.execute(query, (suggestion[0], suggestion[1], suggestion[2]))
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def add_many_suggestions(suggestions: List[SuggestionRow]) -> None:
    cursor = connection.cursor()
    args = mogrify_suggestions(suggestions)
    query = f"""
            INSERT INTO oapen_suggestions.suggestions (handle, name, suggestions)
            VALUES {args}
            ON CONFLICT (handle)
                DO
                    UPDATE SET suggestions = excluded.suggestions
            """

    try:
        cursor.execute(query)
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def add_single_ngrams(ngram: NgramRow) -> None:
    cursor = connection.cursor()
    query = """
            INSERT INTO oapen_suggestions.ngrams (handle, ngrams)
            VALUES (%s, %s::oapen_suggestions.ngram[])
            ON CONFLICT (handle)
            DO
                UPDATE SET ngrams = excluded.ngrams
            """

    try:
        cursor.execute(query, ngram[0], ngram[1])
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def add_many_ngrams(ngrams: List[NgramRow]) -> None:
    cursor = connection.cursor()
    args = mogrify_ngrams(ngrams)
    query = f"""
            INSERT INTO oapen_suggestions.ngrams (handle, ngrams)
            VALUES {args}
            ON CONFLICT (handle)
            DO
                UPDATE SET ngrams = excluded.ngrams
            """

    try:
        cursor.execute(query)
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def get_all_ngrams(ngram_limit=None) -> List[NgramRow]:

    cursor = connection.cursor()

    query = """
            SELECT handle, CAST (ngrams AS oapen_suggestions.ngram[]), created_at, updated_at 
            FROM oapen_suggestions.ngrams
            """

    try:

        cursor.execute(query)
        records = cursor.fetchall()

        return records

    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def get_all_suggestions() -> List[SuggestionRow]:

    cursor = connection.cursor()
    query = """
            SELECT handle, name, CAST (suggestions AS oapen_suggestions.suggestion[]), created_at, updated_at 
            FROM oapen_suggestions.suggestions
            """

    try:

        cursor.execute(query)
        records = cursor.fetchall()

        return records

    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()
