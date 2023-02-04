import pytest
import json
import os


@pytest.fixture(
    params=[
        "en_cleaned.json",
    ]
)
def words(request):
    with open(os.path.join(os.path.dirname(__file__), request.param)) as f:
        result = json.load(f)
    items = list(result.items())
    return dict(items[: len(items) // 5])


@pytest.mark.benchmark
def test_completion(trie, words, benchmark):
    @benchmark
    def complete():
        for word in words:
            for i in range(1, len(word)):
                trie.complete(word[:i])
