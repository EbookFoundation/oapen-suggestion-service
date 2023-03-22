import model.ngrams as ngrams

test_text1 = "Foxes are cunning animals. There was a quick, red fox known to avoid crossing roads during the day, doing so only at night."
test_text2 = "The quick red fox jumped over the lazy brown dog. It had a fantastic time doing so, as it felt finally free. The fox had been in the zoo for far too long, held in captivity."

processed_text1 = ['foxes', 'cunning', 'animals', 'quick', 'red', 'fox', 'known', 'avoid', 'crossing', 'roads', 'day', 'night']
processed_text2 = ['quick', 'red', 'fox', 'jumped', 'lazy', 'brown', 'dog', 'fantastic', 'time', 'felt', 'finally', 'free', 'fox', 'zoo', 'far', 'long', 'held', 'captivity']

ngrams1 = {
    'foxes cunning animals': 1, 
    'cunning animals quick': 1, 
    'animals quick red': 1, 
    'quick red fox': 1, 
    'red fox known': 1, 
    'fox known avoid': 1, 
    'known avoid crossing': 1, 
    'avoid crossing roads': 1, 
    'crossing roads day': 1, 
    'roads day night': 1
}
ngrams2 = {
    'quick red fox': 1, 
    'red fox jumped': 1, 
    'fox jumped lazy': 1, 
    'jumped lazy brown': 1, 
    'lazy brown dog': 1, 
    'brown dog fantastic': 1, 
    'dog fantastic time': 1, 
    'fantastic time felt': 1, 
    'time felt finally': 1, 
    'felt finally free': 1, 
    'finally free fox': 1, 
    'free fox zoo': 1, 
    'fox zoo far': 1, 
    'zoo far long': 1, 
    'far long held': 1, 
    'long held captivity': 1
}

def test_process_text():
    assert(ngrams.process_text(test_text1) == processed_text1)
    assert(ngrams.process_text(test_text2) == processed_text2)

def test_generate_ngram():
    assert(ngrams.generate_ngram(processed_text1) == ngrams1)
    assert(ngrams.generate_ngram(processed_text2) == ngrams2)

def test_similarity_score():
    assert(ngrams.get_similarity_score(ngrams1, ngrams2, n=5, as_percent=False) == 1)
    assert(ngrams.get_similarity_score(ngrams1, ngrams2, n=5, as_percent=True) == 0.2)
    