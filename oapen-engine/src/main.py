import data.oapen as OapenAPI
import data.oapen_db as OapenDB
import model.ngrams as Model
from data.connection import close_connection, connection

demo_books = {
    # should be similar
    "Quality Management and Accounting in Service Industries": "20.500.12657/54327",
    "Management Accountants’ Business Orientation and Involvement in Incentive Compensation": "20.500.12657/26999",
    # should be similar but different from first group
    "Immersion Into Noise": "20.500.12657/33907",
    "Ambisonics": "20.500.12657/23095",
}


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


def run_demo(show_results=True):
    items = []
    ngram_dict = {}

    print("---------------------------------")

    for name, handle in demo_books.items():
        item = OapenAPI.get_item(handle)

        items.append(item)

        text = Model.process_text(item.text)
        print(f"  {name}: text array\n{text[:30]}...\n")

        ngram_dict[handle] = Model.generate_ngram(text, 3)
        print(
            f"  {name}: ngram dictionary\n {list(ngram_dict[handle].items())[:30]}..."
        )

        print("---------------------------------")

    if show_results:
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


def cache_demo():
    print("Caching ngrams...")
    items = []

    for name, handle in demo_books.items():
        item = OapenAPI.get_item(handle)
        items.append(item)

    Model.cache_ngrams_from_items(items)
    print("Done caching ngrams.")


def query_db_demo():
    suggestions = OapenDB.get_all_suggestions()
    ngrams = OapenDB.get_all_ngrams()

    print("Querying suggestions...")
    for i in range(min(5, len(suggestions))):
        print(suggestions[i])

    print("Querying ngrams...")
    for i in range(min(5, len(ngrams))):
        print(ngrams[i][0], ngrams[i][1][0:4])


def run_ngrams():
    run_demo()
    cache_demo()


def main():
    run_demo(show_results=False)
    cache_demo()
    query_db_demo()

    close_connection(connection)
    return


if __name__ == "__main__":
    main()
