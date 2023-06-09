from typing import List, Union

import psycopg2
from logger.base_logger import logger
from model.oapen_types import NgramRow, SuggestionRow, UrlRow


class OapenDB:
    def __init__(self, connection):
        self.connection = connection

    def deduplicate(self, items: Union[List[NgramRow], List[SuggestionRow]]):
        seen = set()
        res = []
        for i in items:
            if i not in seen:
                res.append(i)
                seen.add(i)
        return res

    def mogrify_ngrams(self, ngrams: List[NgramRow]) -> str:
        ngrams = self.deduplicate(ngrams)
        cursor = self.connection.cursor()
        args = ",".join(
            cursor.mogrify(
                "(%s,%s,%s,%s::oapen_suggestions.ngram[])",
                (x.handle, x.name, x.thumbnail, x.ngrams),
            ).decode("utf-8")
            for x in ngrams
        )
        if not cursor.closed:
            cursor.close()
        return args

    def mogrify_suggestions(self, suggestions: List[SuggestionRow]) -> str:
        suggestions = self.deduplicate(suggestions)
        cursor = self.connection.cursor()
        args = ",".join(
            cursor.mogrify(
                "(%s,%s,%s,%s,%s)",
                (
                    x.handle,
                    x.suggestion,
                    x.suggestion_name,
                    x.suggestion_thumbnail,
                    x.score,
                ),
            ).decode("utf-8")
            for x in suggestions
        )
        if not cursor.closed:
            cursor.close()
        return args

    def mogrify_urls(self, urls: List[str]) -> str:
        cursor = self.connection.cursor()
        urls = [(x,) for x in urls]
        args = ",".join(
            cursor.mogrify(
                "(%s)",
                (
                    tuple(
                        x,
                    )
                ),
            ).decode("utf-8")
            for x in urls
        )

        if not cursor.closed:
            cursor.close()
        return args

    def table_exists(self, table_name):
        cursor = self.connection.cursor()
        query = """
                SELECT EXISTS (
                    SELECT * FROM information_schema.tables WHERE table_name=%s
                )
                """

        try:
            cursor.execute(query, (table_name,))
            res = cursor.fetchone()[0]

            return bool(res)
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
            return False
        finally:
            if not cursor.closed:
                cursor.close()

    def type_exists(self, type_name):
        cursor = self.connection.cursor()
        query = """
            SELECT EXISTS (
                SELECT 1 FROM pg_type WHERE typname = %s
            )
            """

        try:
            cursor.execute(query, (type_name,))
            res = cursor.fetchone()[0]

            return bool(res)
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
            return False
        finally:
            if not cursor.closed:
                cursor.close()

    def add_single_suggestion(self, suggestion: SuggestionRow) -> None:
        cursor = self.connection.cursor()
        query = """
                INSERT INTO oapen_suggestions.suggestions (handle, name, suggestions)
                VALUES (%s, %s, %s, %s)
                """

        try:
            cursor.execute(
                query, (suggestion[0], suggestion[1], suggestion[2], suggestion[3])
            )
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()

    def add_many_suggestions(self, suggestions: List[SuggestionRow]) -> None:
        cursor = self.connection.cursor()
        args = self.mogrify_suggestions(suggestions)

        query = f"""
                INSERT INTO oapen_suggestions.suggestions
                VALUES {args}
                """
        try:
            cursor.execute(query)
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
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
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()

    def add_many_ngrams(self, ngrams: List[NgramRow]) -> None:
        try:
            cursor = self.connection.cursor()
            args = self.mogrify_ngrams(ngrams)
            query = f"""
                    INSERT INTO oapen_suggestions.ngrams
                    VALUES {args}
                    ON CONFLICT (handle)
                        DO
                            UPDATE SET ngrams = excluded.ngrams
                """
            cursor.execute(query)
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()

    # get_empty = True -> Include rows with no ngrams in result
    def get_all_ngrams(self, get_empty=True) -> List[NgramRow]:
        cursor = self.connection.cursor()
        query = """
                SELECT handle, name, thumbnail, CAST (ngrams AS oapen_suggestions.ngram[]), created_at, updated_at 
                FROM oapen_suggestions.ngrams
                """
        if not get_empty:
            query += """
                     WHERE ngrams != \'{}\'
                     """
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            ret = [NgramRow(*record) for record in records]

        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()
            return ret

    def get_all_suggestions(self) -> List[SuggestionRow]:
        cursor = self.connection.cursor()
        query = """
                SELECT * FROM oapen_suggestions.suggestions
                """
        ret = None
        try:
            cursor.execute(query)
            records = cursor.fetchall()

            ret = [SuggestionRow(*record) for record in records]

        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()
            return ret

    def get_suggestions_for_item(self, handle) -> List[SuggestionRow]:
        cursor = self.connection.cursor()
        query = """
                SELECT * FROM oapen_suggestions.suggestions
                WHERE handle = \'%s\'
                """
        ret = None
        try:
            cursor.execute(query, handle)
            records = cursor.fetchall()

            ret = records

        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()
            return ret

    def get_suggestions_for_item(self, handle) -> List[SuggestionRow]:
        cursor = self.connection.cursor()
        query = """
                SELECT * FROM oapen_suggestions.suggestions
                WHERE handle = \'%s\'
                """
        ret = None
        try:
            cursor.execute(query, handle)
            records = cursor.fetchall()

            ret = records

        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
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
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()
            return ret

    def count_ngrams(self) -> int:
        return self.count_table("'oapen_suggestions.ngrams'")

    def count_suggestions(self) -> int:
        return self.count_table("'oapen_suggestions.suggestions'")

    def add_urls(self, urls):
        try:
            cursor = self.connection.cursor()
            args = self.mogrify_urls(urls)
            query = """
                    INSERT INTO oapen_suggestions.endpoints (endpoint)
                    VALUES {}
                    ON CONFLICT (endpoint)
                        DO
                            UPDATE SET completed = excluded.completed
                """.format(
                args
            )

            cursor.execute(query)
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()

    def get_incomplete_urls(self) -> List[UrlRow]:
        cursor = self.connection.cursor()
        query = """
                SELECT * 
                FROM oapen_suggestions.endpoints
                WHERE completed = FALSE
                """
        ret = None
        try:
            cursor.execute(query)
            records = cursor.fetchall()

            ret = [UrlRow(*record) for record in records]

        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()
            return ret

    def update_url(self, url, completed) -> None:
        cursor = self.connection.cursor()
        query = """
                UPDATE oapen_suggestions.endpoints
                SET completed = %s
                WHERE endpoint = %s
                """

        try:
            cursor.execute(query, (completed, url))
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            if not cursor.closed:
                cursor.close()
