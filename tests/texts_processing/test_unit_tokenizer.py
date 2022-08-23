import pytest

from src.texts_processing import TextsTokenizer

pytestmark = pytest.mark.unit


def test_texts2tokens():
    tokenizer = TextsTokenizer()
    tokens = tokenizer(("мама", "мыла", "раму", "деревянную"))
    assert tokens == [["мама"], ["мыло"], ["рама"], ["деревянный"]]
