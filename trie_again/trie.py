import itertools
from functools import cached_property
from typing import Iterable, Optional


class TrieNode:
    def __init__(self, value: str, parent: "TrieNode | None" = None):
        self._children: dict[str, TrieNode] = {}
        self._insertion_count = 0
        self._value = value
        self._parent = parent

    def __repr__(self):
        return f"TrieNode<{self._value}>"  # pragma: no cover

    @cached_property
    def word(self) -> str:
        return "".join(n._value for n in self._bottom_up_traversal())[::-1]

    def _bottom_up_traversal(self) -> Iterable["TrieNode"]:
        current: "TrieNode | None" = self
        while current is not None:
            yield current
            current = current._parent

    @property
    def word_nodes(self) -> Iterable["TrieNode"]:
        result = []
        dfs = [self]
        while dfs:
            node = dfs.pop()
            if node._insertion_count:
                result.append(node)

            for child in node._children.values():
                dfs.append(child)

        return result


class Trie:
    def __init__(self):
        self._root = TrieNode("")

    def extend(
        self, words: Iterable[str], multipliers: Optional[Iterable[int]] = None
    ) -> None:
        if multipliers is None:
            multipliers = itertools.cycle([1])

        for word, multiplier in zip(words, multipliers):
            self.insert(word, multiplier)

    def insert(self, word: str, multiplier: int = 1) -> None:
        if not isinstance(word, str):  # pragma: no cover
            raise ValueError("Can insert only single word")

        if not word:  # pragma: no cover
            return

        current = self._root
        for letter in word:
            if letter not in current._children:
                current._children[letter] = TrieNode(letter, current)

            current = current._children[letter]

        current._insertion_count += multiplier

    def count(self, word: str) -> int:
        current = self._root
        for letter in word:
            if letter not in current._children:
                return 0

            current = current._children[letter]

        return current._insertion_count

    def complete(self, prefix_groups: "list[str] | str") -> Iterable[str]:
        candidates = [self._root]
        for group in prefix_groups:
            new_candidates = []
            for each in candidates:
                for letter in group:
                    if letter in each._children:
                        new_candidates.append(each._children[letter])

            candidates = new_candidates

        return self._flatten_nodes([node for c in candidates for node in c.word_nodes])

    def _flatten_nodes(self, nodes: Iterable["TrieNode"]) -> Iterable[str]:
        return (
            node.word for node in sorted(nodes, key=lambda node: -node._insertion_count)
        )

    def __iter__(self) -> Iterable[str]:
        return self._flatten_nodes(self._root.word_nodes)

    def __contains__(self, word: str) -> bool:
        return bool(self.count(word))

    def __len__(self) -> int:
        return len(list(self._root.word_nodes))
