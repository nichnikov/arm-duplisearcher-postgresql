import pytest
from gensim.matutils import corpus2csc

from config import VOCABULARY_SIZE
from src.texts_processing import TextsVectorsBoW

pytestmark = pytest.mark.unit


@pytest.fixture()
def tokens_corpus_vectors():
    tokens = [
        ["должностной", "инструкция", "классный", "руководитель"],
        ["должностной", "инструкция", "классный", "руководитель", "новый"],
        ["штатный", "норматив", "немедицинский", "персонал"],
    ]
    corpus = [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],
        [(5, 1), (6, 1), (7, 1), (8, 1)],
    ]
    vectors = [corpus2csc([x], num_terms=VOCABULARY_SIZE) for x in corpus]
    return tokens, corpus, vectors


def test_tokens2corpus(tokens_corpus_vectors):
    tokens, corpus, _ = tokens_corpus_vectors
    vectorizer = TextsVectorsBoW(max_dict_size=VOCABULARY_SIZE)
    assert vectorizer.tokens2corpus(tokens) == corpus


def test_tokens2vectors(tokens_corpus_vectors):
    tokens, _, vectors = tokens_corpus_vectors
    vectorizer = TextsVectorsBoW(max_dict_size=VOCABULARY_SIZE)
    result_vectors = vectorizer(tokens)
    assert len(result_vectors) == len(vectors)
    for result_csc, csc in zip(result_vectors, vectors):
        assert result_csc.shape == csc.shape
        assert result_csc.dtype == csc.dtype
        assert result_csc.nnz == csc.nnz
