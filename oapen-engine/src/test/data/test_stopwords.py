from model.stopwords_processor import STOPWORDS
import model.stopwords.stopwords_full_list as stopwords_full_list
# currently contains stopwords_filter, stopwords_publisher, stopwords_broken, stopwords_dutch_extra

# tests all at once
def test_stopwords_contains_all():
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_filter))
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_publisher))
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_broken))
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_dutch_extra))

# individual tests provided if needed
def test_stopwords_contains_stopwords_filter():
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_filter))
    
def test_stopwords_contains_stopwords_publisher():
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_publisher))

def test_stopwords_contains_stopwords_broken():
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_broken))

def test_stopwords_contains_stopwords_dutch_extra():
    assert(all(x in STOPWORDS for x in stopwords_full_list.stopwords_dutch_extra))