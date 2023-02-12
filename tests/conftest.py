import pytest
from trie_again import Trie
from trie_again.cytrie import CyTrie


def pytest_addoption(parser):
    parser.addoption(
        "--benchmark", action="store_true", default=False, help="Run benchmark tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--benchmark"):
        for item in items:
            if "benchmark" not in item.keywords:
                item.add_marker(pytest.mark.skip(reason="skip due to benchmarking"))

        return

    for item in items:
        if "benchmark" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="to benchmark add --benchmark"))


@pytest.fixture(
    params=[
        Trie,
        CyTrie,
    ]
)
def trie_impl(request):
    return request.param


@pytest.fixture()
def trie(trie_impl, words):
    result = trie_impl()
    if isinstance(words, list):
        result.extend(words)
    else:
        result.extend(list(words), list(words.values()))

    return result
