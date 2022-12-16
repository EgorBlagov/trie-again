import pytest
from trie import Trie


@pytest.fixture()
def ca_words():
    return ["cat", "car", "cartoon", "carate"]


@pytest.fixture()
def ta_words():
    return ["tabla", "table", "taboo"]


@pytest.fixture()
def words(ta_words, ca_words):
    return ta_words + ca_words


@pytest.fixture()
def trie(words):
    result = Trie()
    for word in words:
        result.insert(word)

    return result


class TestTrie:
    def test_find(self, words, trie):
        for word in words:
            assert word in trie

        assert "rofl" not in trie

    def test_prefix_not_in_trie(self, trie):
        assert "ca" not in trie

    def test_len(self, words, trie):
        assert len(trie) == len(words)

    def test_iter(self, trie, words):
        assert sorted(trie) == sorted(words)

    def test_complete(self, ca_words, ta_words, trie):
        assert list(trie.complete("cat")) == ["cat"]
        assert list(trie.complete("car")) == ["car", "cartoon", "carate"]
        assert list(trie.complete("ca")) == ca_words
        assert list(trie.complete("ta")) == ta_words

    @pytest.mark.parametrize(
        ("words", "expected"),
        [
            (["cat"] * 3 + ["car"] * 1 + ["cartoon"] * 2, ["cat", "cartoon", "car"]),
            (["cat"] * 2 + ["car"] * 1 + ["cartoon"] * 3, ["cartoon", "cat", "car"]),
            (["cat"] * 2 + ["car"] * 3 + ["cartoon"] * 1, ["car", "cat", "cartoon"]),
        ],
    )
    def test_sorted_by_use(self, trie, expected):
        assert list(trie) == expected
        assert list(trie.complete("ca")) == expected

    @pytest.mark.parametrize("words", [["cat"] * 3 + ["car"] * 1 + ["cartoon"] * 2])
    def test_query_count(self, trie):
        assert trie.count("cat") == 3
        assert trie.count("car") == 1
        assert trie.count("cartoon") == 2
        assert trie.count("carate") == 0
        assert trie.count("ca") == 0

    @pytest.mark.parametrize(
        ("input_groups", "expected"),
        [
            (["cv", "as", "rt"], ["car", "cartoon", "carate", "cat"]),
            (["atc", "atc", "atc"], ["cat"]),
            (["c", "a", "r"], ["car", "cartoon", "carate"]),
            (["ct", "a", "tb"], ["cat", "tabla", "table", "taboo"]),
        ],
    )
    def test_ambiguous_completion(self, trie, input_groups, expected):
        assert list(trie.complete(input_groups)) == expected

    @pytest.mark.parametrize(
        ("words", "input_groups", "expected"), [(["cat"] * 3 + ["car"], ["cv", "as", "rt"], ["cat", "car"])]
    )
    def test_ambiguous_completion_sorted_by_use(self, trie, input_groups, expected):
        assert list(trie.complete(input_groups)) == expected
