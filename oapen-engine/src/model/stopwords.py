from nltk.corpus import stopwords  # pylint: disable=import-error


def read_from_files(filenames):
    stopwords_list = []
    for fn in filenames:
        with open(fn, "r") as f:
            stopwords_list += [line.rstrip() for line in f if line.rstrip() != ""]
    return stopwords_list


def get_all_stopwords():
    stopword_paths = [
        "src/model/stopwords_broken.txt",
        "src/model/stopwords_dutch.txt",
        "src/model/stopwords_filter.txt",
        "src/model/stopwords_publisher.txt",
    ]
    return list(
        set(
            stopwords.words("english")
            + stopwords.words("german")
            + stopwords.words("dutch")
            + read_from_files(stopword_paths)
        )
    )
