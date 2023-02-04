import pytest


@pytest.fixture()
def ca_words():
    return ["cat", "car", "cartoon", "carate"]


@pytest.fixture()
def ta_words():
    return ["tabla", "table", "taboo"]


@pytest.fixture()
def words(ta_words, ca_words):
    return ta_words + ca_words


def test_find(words, trie):
    for word in words:
        assert word in trie

    assert "rofl" not in trie


def test_prefix_not_in_trie(trie):
    assert "ca" not in trie


def test_len(words, trie):
    assert len(trie) == len(words)


def test_iter(trie, words):
    assert sorted(trie) == sorted(words)


def test_complete(ca_words, ta_words, trie):
    assert list(trie.complete("cat")) == ["cat"]
    assert sorted(trie.complete("car")) == sorted(["car", "cartoon", "carate"])
    assert sorted(trie.complete("ca")) == sorted(ca_words)
    assert sorted(trie.complete("ta")) == sorted(ta_words)


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["cat"] * 3 + ["car"] * 1 + ["cartoon"] * 2, ["cat", "cartoon", "car"]),
        (["cat"] * 2 + ["car"] * 1 + ["cartoon"] * 3, ["cartoon", "cat", "car"]),
        (["cat"] * 2 + ["car"] * 3 + ["cartoon"] * 1, ["car", "cat", "cartoon"]),
    ],
)
def test_sorted_by_use(trie, expected):
    assert list(trie) == expected
    assert list(trie.complete("ca")) == expected


@pytest.mark.parametrize("words", [["cat"] * 3 + ["car"] * 1 + ["cartoon"] * 2])
def test_query_count(trie):
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
def test_ambiguous_completion(trie, input_groups, expected):
    assert sorted(trie.complete(input_groups)) == sorted(expected)


@pytest.mark.parametrize(
    ("words", "input_groups", "expected"),
    [(["cat"] * 3 + ["car"], ["cv", "as", "rt"], ["cat", "car"])],
)
def test_ambiguous_completion_sorted_by_use(trie, input_groups, expected):
    assert list(trie.complete(input_groups)) == expected
