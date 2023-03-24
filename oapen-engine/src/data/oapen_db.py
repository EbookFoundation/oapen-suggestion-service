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
            if i[0] not in seen:
                res.append(i)
                seen.add(i[0])
        return res

    def mogrify_ngrams(self, ngrams: List[NgramRow]) -> str:
        ngrams = self.deduplicate(ngrams)
        cursor = self.connection.cursor()
        args = ",".join(
            cursor.mogrify("(%s,%s::oapen_suggestions.ngram[])", x).decode("utf-8")
            for x in ngrams
        )
        cursor.close()
        return args

    def mogrify_suggestions(self, suggestions: List[SuggestionRow]) -> str:
        suggestions = self.deduplicate(suggestions)
        cursor = self.connection.cursor()
        args = ",".join(
            cursor.mogrify("(%s,%s,%s::oapen_suggestions.suggestion[])", x).decode(
                "utf-8"
            )
            for x in suggestions
        )
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

        cursor.close()
        return args

    def mogrify_stopwords(self, stopwords: List[str]) -> str:
        cursor = self.connection.cursor()
        stopwords = [(s,) for s in stopwords]
        args = ",".join(
            cursor.mogrify(
                "(%s)",
                (
                    tuple(
                        x,
                    )
                ),
            ).decode("utf-8")
            for x in stopwords
        )
        cursor.close()
        return args

    def mogrify_handles(self, handles: List[str]) -> str:
        cursor = self.connection.cursor()
        stopwords = [(h,) for h in handles]
        args = ",".join(
            cursor.mogrify(
                "%s",
                (
                    tuple(
                        x,
                    )
                ),
            ).decode("utf-8")
            for x in stopwords
        )
        cursor.close()
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
            logger.error(error)
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
            logger.error(error)
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
            logger.error(error)
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
            logger.error(error)
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
            logger.error(error)
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
            logger.error(error)
        finally:
            cursor.close()
            return ret

    def get_ngrams_with_handles(self, handles: List[str]) -> List[NgramRow]:
        cursor = self.connection.cursor()
        ret = None
        try:
            args = self.mogrify_handles(handles)
            query = """
                    SELECT handle, CAST (ngrams AS oapen_suggestions.ngram[]), created_at, updated_at 
                    FROM oapen_suggestions.ngrams
                    WHERE handle IN ({});
                    """.format(
                args
            )
            cursor.execute(query)
            records = cursor.fetchall
            ret = records
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
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
            logger.error(error)
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
            logger.error(error)
        finally:
            cursor.close()
            return ret

    def count_ngrams(self) -> int:
        return self.count_table("'oapen_suggestions.ngrams'")

    def count_suggestions(self) -> int:
        return self.count_table("'oapen_suggestions.suggestions'")

    def count_stopwords(self) -> int:
        return self.count_table("'oapen_suggestions.stopwords'")

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

            ret = records

        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
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
            cursor.close()

    def get_new_stopwords(self, stopwords):
        ret = None
        try:
            cursor = self.connection.cursor()
            args = self.mogrify_stopwords(stopwords)
            query = """
                DROP TABLE IF EXISTS temp_stopwords;
                CREATE TEMPORARY TABLE temp_stopwords (stopword text);
                INSERT INTO temp_stopwords (stopword) VALUES {};
                SELECT DISTINCT temp_stopwords.stopword
                FROM (
                    temp_stopwords LEFT OUTER JOIN oapen_suggestions.stopwords
                    ON temp_stopwords.stopword=oapen_suggestions.stopwords.stopword
                    )
                WHERE oapen_suggestions.stopwords.stopword IS NULL;
                """.format(
                args
            )

            cursor.execute(query)
            records = cursor.fetchall()
            ret = records
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            cursor.close()
            return ret

    def update_stopwords(self, stopwords):
        try:
            cursor = self.connection.cursor()
            args = self.mogrify_stopwords(stopwords)
            query = """
                DELETE FROM oapen_suggestions.stopwords;
                INSERT INTO oapen_suggestions.stopwords (stopword)
                VALUES {args};
                """.format(
                args
            )

            cursor.execute(query)
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            cursor.close()

    def get_all_items_containing_stopwords(self, stopwords):
        ret = None
        try:
            cursor = self.connection.cursor()
            query = """
                    SELECT handle
                    FROM oapen_suggestions.ngrams
                    WHERE EXISTS (
                        SELECT 1
                        FROM UNNEST(ngrams) AS ng
                        WHERE ng.ngram ~ '(^|\s)({})($|\s)'
                    );
                """.format(
                "|".join(stopwords)
            )

            cursor.execute(query)
            records = cursor.fetchall()
            ret = records
        except (Exception, psycopg2.Error) as error:
            logger.error(error)
        finally:
            cursor.close()
            return ret
