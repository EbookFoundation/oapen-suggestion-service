import data.oapen as OapenAPI
import data.oapen_db as OapenDB
import model.ngrams as Model
from data.connection import close_connection, connection


# to demo some functions
def test_functions():
    data = OapenAPI.get_collection_items_by_label(
        "Austrian Science Fund (FWF)", limit=100
    )
    # Uncomment to print raw text of first book
    # for item in data:
    #     print(item.get_text_bitstream())
    #     break
    df = Model.make_df(data)
    print(df.shape)
    print(df)
    sample_list = Model.get_text_by_handle(df, df.iloc[0].handle)
    print(sample_list[:10])
    sample_ngram_list = Model.generate_ngram_by_handle(df, df.iloc[0].handle, 3)
    print(Model.get_n_most_occuring(sample_ngram_list, 2))


# run demo with the above titles
def run_demo():
    demo_books = {
        # should be similar
        "Quality Management and Accounting in Service Industries": "20.500.12657/54327",
        "Management Accountants’ Business Orientation and Involvement in Incentive Compensation": "20.500.12657/26999",
        # should be similar but different from first group
        "Immersion Into Noise": "20.500.12657/33907",
        "Ambisonics": "20.500.12657/23095",
    }

    items = []
    ngram_dict = {}

    print("---------------------------------")

    for name, handle in demo_books.items():
        item = OapenAPI.get_item(handle)

        items.append(item)

        text = Model.process_text(item.get_text())
        print(f"  {name}: text array\n{text[:30]}...\n")

        ngram_dict[handle] = Model.generate_ngram(text, 3)
        print(
            f"  {name}: ngram dictionary\n {list(ngram_dict[handle].items())[:30]}..."
        )

        print("---------------------------------")

    for name, handle in demo_books.items():
        print(f"Showing similarity scores for all books relative to {name}:\n")
        for name2, handle2 in demo_books.items():
            # if handle == handle2:  # dont check self
            #     continue

            simple_similarity_score = 100 * Model.get_similarity_score(
                ngram_dict[handle], ngram_dict[handle2], n=10000
            )
            print(
                f"  Similarity score by simple count for title {name2}: {simple_similarity_score}%"
            )

            dict_similarity_score = 100 * Model.get_similarity_score_by_dict_count(
                ngram_dict[handle], ngram_dict[handle2]
            )
            print(
                f"  Similarity score by dict count for title {name2}: {dict_similarity_score}%"
            )
            print()


def run_caching_test():
    demo_books = {
        # should be similar
        "Quality Management and Accounting in Service Industries": "20.500.12657/54327",
        "Management Accountants’ Business Orientation and Involvement in Incentive Compensation": "20.500.12657/26999",
        # should be similar but different from first group
        "Immersion Into Noise": "20.500.12657/33907",
        "Ambisonics": "20.500.12657/23095",
    }

    items = []

    for name, handle in demo_books.items():
        item = OapenAPI.get_item(handle)
        items.append(item)

    Model.cache_ngrams_from_items(items)


def run_ngrams():
    # run_demo()
    run_caching_test()


def main():
    run_ngrams()

    OapenDB.get_all_ngrams()
    close_connection(connection)
    return


if __name__ == "__main__":
    main()
