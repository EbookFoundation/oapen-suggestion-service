import test_ngrams
import test_oapen
import test_stopwords


def run_test(run_msg, func):
    print(run_msg, end=" ")
    func()
    print("OK")  # will throw on fail


def main():
    print("Testing connection to OAPEN.")
    try:
        run_test(
            "Attempting to get collection limit by id (ea93f8f0-430f-4a03-b7e2-5b06053585b0):",
            test_oapen.test_get_collection_limit,
        )
        run_test(
            "Attempting to get null collection:", test_oapen.test_get_collection_404
        )
    except Exception as e:
        print("\nFailed:")
        print(e)

    print("\nTesting stopwords generation.")
    try:
        run_test(
            "Testing stopwords correctly generated:",
            test_stopwords.test_stopwords_contains_all,
        )
    except Exception as e:
        print("Failed:")
        print(e)

    print("\nTesting ngrams functionality.")
    try:
        run_test("Testing process_text:", test_ngrams.test_process_text)
        run_test("Testing ngram generation:", test_ngrams.test_generate_ngram)
        run_test("Testing similarity score:", test_ngrams.test_similarity_score)

    except Exception as e:
        print("Failed:")
        print(e)


if __name__ == "__main__":
    main()
