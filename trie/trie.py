from typing import Iterable
import itertools

TTrieEntryResult = tuple["TrieNode", str]


class TrieNode:
    def __init__(self, value: str):
        self._children: dict[str, TrieNode] = {}
        self._insertions_count = 0
        self._value = value

    def insert(self, word: str, multiplier: int = 1) -> None:
        if not isinstance(word, str):
            raise ValueError("Can insert only single word")

        if not word:
            return

        child = self._children.setdefault(word[0], TrieNode(word[0]))
        if len(word) == 1:
            child._insertions_count += multiplier
        else:
            child.insert(word[1:], multiplier)

    def complete(self, prefix: str) -> Iterable[str]:
        return self.complete_ambiguous(prefix)

    def _flatten_nodes(self, nodes: Iterable[TTrieEntryResult]) -> Iterable[str]:
        return (word for _, word in sorted(nodes, key=lambda entry: -entry[0]._insertions_count))

    def complete_ambiguous(self, prefix_groups: list[str]) -> Iterable[str]:
        return self._flatten_nodes(self._complete_ambiguous(prefix_groups))

    def _complete_ambiguous(self, prefix_groups: list[str]) -> Iterable[TTrieEntryResult]:
        if not prefix_groups:
            yield from self._iter_word_nodes()
            return

        for letter in prefix_groups[0]:
            child = self._children.get(letter)
            if child is not None:
                for node, suffix in child._complete_ambiguous(prefix_groups[1:]):
                    yield node, self._value + suffix

    def _iter_word_nodes(self) -> Iterable[TTrieEntryResult]:
        if self._insertions_count:
            yield self, self._value

        for child in self._children.values():
            for node, suffix in child._iter_word_nodes():
                yield node, self._value + suffix

    def __iter__(self) -> Iterable[str]:
        return self._flatten_nodes(self._iter_word_nodes())

    def __contains__(self, word: str) -> bool:
        return not word or (word[1:] in self._children.get(word[0], ()))

    def __len__(self) -> int:
        return len(list(self._iter_word_nodes()))


class Trie(TrieNode):
    def __init__(self):
        super().__init__("")

    def extend(self, words: Iterable[str], multipliers: Iterable[int] | None = None) -> None:
        if multipliers is None:
            multipliers = itertools.cycle([1])

        for word, multiplier in zip(words, multipliers):
            self.insert(word, multiplier)
