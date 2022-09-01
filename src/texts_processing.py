import copy
import logging
import re

from gensim.corpora import Dictionary
from gensim.matutils import corpus2csc
from pymystem3 import Mystem
from scipy.sparse import csc_matrix

logger = logging.getLogger(__name__)


class TextsTokenizer:
    """Tokenizer"""

    def __init__(self):
        self.m = Mystem()

    def texts2tokens(self, texts: list[str]) -> list[list[str]]:
        """Lemmatization for texts in list. It returns list with lemmatized texts."""
        text_ = "\n".join(texts)
        text_ = re.sub(r"[^\w\n\s]", " ", text_)
        lm_texts = "".join(self.m.lemmatize(text_))
        return [lm_q.split() for lm_q in lm_texts.split("\n")][:-1]

    def __call__(self, texts: list[str]) -> list[list[str]]:
        return self.texts2tokens(texts)


class TextsVectorsBoW:
    """"""

    def __init__(self, max_dict_size: int):
        self.dictionary = None
        self.max_dict_size = max_dict_size

    def tokens2corpus(self, tokens: list[list]) -> list[list]:
        """queries2vectors new_queries tuple: (text, query_id)
        returns new vectors with query ids for sending in searcher"""

        if self.dictionary is None:
            gensim_dict_ = Dictionary(tokens)
            assert len(gensim_dict_) <= self.max_dict_size, "len(gensim_dict) must be less then max_dict_size"
            self.dictionary = Dictionary(tokens)
        else:
            gensim_dict_ = copy.deepcopy(self.dictionary)
            gensim_dict_.add_documents(tokens)
            if len(gensim_dict_) <= self.max_dict_size:
                self.dictionary = gensim_dict_
        return [self.dictionary.doc2bow(lm_q) for lm_q in tokens]

    def tokens2vectors(self, tokens: list[list]) -> list[csc_matrix]:
        """"""
        corpus = self.tokens2corpus(tokens)
        return [corpus2csc([x], num_terms=self.max_dict_size) for x in corpus]

    def __call__(self, tokens: list[list]) -> list[csc_matrix]:
        return self.tokens2vectors(tokens)
