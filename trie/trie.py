from typing import Iterable
import itertools



class TrieNode:
    def __init__(self, value: str, parent: 'TrieNode | None' = None):
        self._children: dict[str, TrieNode] = {}
        self._insertions_count = 0
        self._value = value
        self._parent = parent

    @property
    def word(self) -> str:
        return ''.join(n._value for n in self._bottom_up_traversal())[::-1]

    def insert(self, word: str, multiplier: int = 1) -> None:
        if not isinstance(word, str):
            raise ValueError("Can insert only single word")

        if not word:
            return

        child = self._children.setdefault(word[0], TrieNode(word[0], self))
        if len(word) == 1:
            child._insertions_count += multiplier
        else:
            child.insert(word[1:], multiplier)

    def complete(self, prefix_groups: list[str] | str) -> Iterable[str]:
        return self._flatten_nodes(self._complete(prefix_groups))

    def _complete(self, prefix_groups: list[str] | str) -> Iterable['TrieNode']:
        if not prefix_groups:
            yield from self._iter_word_nodes()
            return

        for letter in prefix_groups[0]:
            child = self._children.get(letter)
            if child is not None:
                yield from child._complete(prefix_groups[1:])

    def _bottom_up_traversal(self) -> Iterable['TrieNode']:
        current = self
        while current is not None:
            yield current
            current = current._parent

    def _flatten_nodes(self, nodes: Iterable['TrieNode']) -> Iterable[str]:
        return (node.word for node in sorted(nodes, key=lambda node: -node._insertions_count))

    def _iter_word_nodes(self) -> Iterable['TrieNode']:
        if self._insertions_count:
            yield self

        for child in self._children.values():
            yield from child._iter_word_nodes()

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
