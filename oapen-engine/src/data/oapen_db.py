from typing import List, Union

import psycopg2
from model.oapen_types import NgramRow, SuggestionRow


class OapenDB:
    def __init__(self, connection):
        self.connection = connection

    def deduplicate(self, items: Union[List[NgramRow], List[SuggestionRow]]):
        seen = set()
        res = []
        for i in items:
            if i[0] not in seen:
                res.append(i)
                seen.add(i[0])
        return res

    def mogrify_ngrams(self, ngrams: List[NgramRow]) -> str:
        cursor = self.connection.cursor()
        ngrams = self.deduplicate(ngrams)
        args = ",".join(
            cursor.mogrify("(%s,%s::oapen_suggestions.ngram[])", x).decode("utf-8")
            for x in ngrams
        )
        cursor.close()
        return args

    def mogrify_suggestions(self, suggestions: List[SuggestionRow]) -> str:
        cursor = self.connection.cursor()
        suggestions = self.deduplicate(suggestions)
        args = ",".join(
            cursor.mogrify("(%s,%s,%s::oapen_suggestions.suggestion[])", x).decode(
                "utf-8"
            )
            for x in suggestions
        )
        return args

    def table_exists(self, table):
        cursor = self.connection.cursor()
        query = """
                SELECT EXISTS (
                    SELECT * FROM information_schema.tables WHERE table_name=%s
                )
                """

        try:
            cursor.execute(query, (table,))
            res = cursor.fetchone()[0]

            return res is not None
        except (Exception, psycopg2.Error) as error:
            print(error)
            return False
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
        try:
            cursor = self.connection.cursor()
            args = self.mogrify_ngrams(ngrams)
            query = f"""
                    INSERT INTO oapen_suggestions.ngrams (handle, ngrams)
                    VALUES {args}
                    ON CONFLICT (handle)
                        DO
                            UPDATE SET ngrams = excluded.ngrams
                """

            cursor.execute(query)
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            cursor.close()

    def get_all_ngrams(self, ngram_limit=None) -> List[NgramRow]:
        cursor = self.connection.cursor()
        query = """
                SELECT handle, CAST (ngrams AS oapen_suggestions.ngram[]), created_at, updated_at 
                FROM oapen_suggestions.ngrams
                """
        ret = None
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            ret = records

        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            cursor.close()
            return ret

    def get_all_suggestions(self) -> List[SuggestionRow]:
        cursor = self.connection.cursor()
        query = """
                SELECT handle, name, CAST (suggestions AS oapen_suggestions.suggestion[]), created_at, updated_at 
                FROM oapen_suggestions.suggestions
                """
        ret = None
        try:
            cursor.execute(query)
            records = cursor.fetchall()

            ret = records

        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            cursor.close()
            return ret

    def count_table(self, table_name) -> int or None:
        cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM %s"
        ret = None
        try:
            cursor.execute(query, (table_name,))
            count = cursor.fetchone()[0]
            ret = count
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            cursor.close()
            return ret

    def count_ngrams(self) -> int:
        return self.count_table("oapen_suggestions.ngrams")

    def count_suggestions(self) -> int:
        return self.count_table("oapen_suggestions.suggestions")
