from typing import List

import psycopg2
from data.connection import connection
from model.oapen_types import OapenNgram


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


def add_single_suggestion(suggestion) -> None:
    cursor = connection.cursor()

    query = """
            INSERT INTO oapen_suggestions.suggestions (handle, name, suggestions)
            VALUES (%s, %s, %s::oapen_suggestions.suggestion[])
            ON CONFLICT (handle)
            DO
                UPDATE SET suggestions = (%s::oapen_suggestions.suggestion[])
            """

    try:
        cursor.execute(
            query, (suggestion[0], suggestion[1], suggestion[2], suggestion[2])
        )
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def add_many_suggestions(suggestions) -> None:
    cursor = connection.cursor()

    args = ",".join(
        cursor.mogrify("(%s,%s,%s::oapen_suggestions.suggestion[])", x).decode("utf-8")
        for x in suggestions
    )

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


def add_single_ngrams(ngram) -> None:
    cursor = connection.cursor()

    query = f"""
            INSERT INTO oapen_suggestions.ngrams (handle, ngrams)
            VALUES ({ngram[0]}, {ngram[1]}::oapen_suggestions.ngram[])
            ON CONFLICT (handle)
            DO
                UPDATE SET ngrams = {ngram[1]}
            """

    try:
        cursor.execute(query)
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()


def add_many_ngrams(ngrams) -> None:
    cursor = connection.cursor()

    args = ",".join(
        cursor.mogrify("(%s,%s::oapen_suggestions.ngram[])", x).decode("utf-8")
        for x in ngrams
    )

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


def get_all_ngrams() -> List[OapenNgram]:
    cursor = connection.cursor()

    query = """
            SELECT * FROM oapen_suggestions.ngrams
            """

    try:

        ngrams: List[OapenNgram] = []
        cursor.execute(query)
        records = cursor.fetchall()

        for i in range(1):
            # print(records[i])
            print(type(records[i][0]))
            print(type(records[i][1]))

        return ngrams

    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()
