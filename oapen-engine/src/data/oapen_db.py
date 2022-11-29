from typing import List

import psycopg2
from model.oapen_types import NgramRow, SuggestionRow


class OapenDB:
    def __init__(self, connection):
        self.connection = connection

    def mogrify_ngrams(self, ngrams: List[NgramRow]) -> str:
        cursor = self.connection.cursor()
        args = ",".join(
            cursor.mogrify("(%s,%s::oapen_suggestions.ngram[])", x).decode("utf-8")
            for x in ngrams
        )
        cursor.close()
        return args

    def mogrify_suggestions(self, suggestions: List[SuggestionRow]) -> str:
        cursor = self.connection.cursor()
        args = ",".join(
            cursor.mogrify("(%s,%s,%s::oapen_suggestions.suggestion[])", x).decode(
                "utf-8"
            )
            for x in suggestions
        )
        return args

    def table_exists(self, table):
        cursor = self.connection.cursor
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

    def add_single_suggestion(self, suggestion: SuggestionRow) -> None:
        cursor = self.connection.cursor()
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

    def add_many_suggestions(self, suggestions: List[SuggestionRow]) -> None:
        cursor = self.connection.cursor()
        args = self.mogrify_suggestions(suggestions)
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

    def add_single_ngrams(self, ngram: NgramRow) -> None:
        cursor = self.connection.cursor()
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

    def add_many_ngrams(self, ngrams: List[NgramRow]) -> None:
        cursor = self.connection.cursor()
        args = self.mogrify_ngrams(ngrams)
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
            print(query[0:100])
        finally:
            cursor.close()

    def get_all_ngrams(self, ngram_limit=None) -> List[NgramRow]:
        cursor = self.connection.cursor()

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

    def get_all_suggestions(self) -> List[SuggestionRow]:
        cursor = self.connection.cursor()
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
