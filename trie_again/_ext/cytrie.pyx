# cython: language_level=3

from Trie cimport Trie

cdef class CyTrie:
    cdef Trie c_trie;

    def __cinit__(self):
        self.c_trie = Trie()


    def insert(self, word: str, multiplier: int = 1):
        word_bytes = word.encode('utf8')
        self.c_trie.insert(word_bytes, multiplier)

    def count(self, word: str) -> int:
        word_bytes = word.encode('utf8')
        return self.c_trie.count(word_bytes)

    def complete(self, word: 'str | list[str]') -> 'Iterable[str]':
        if isinstance(word, str):
            word_bytes = word.encode('utf8')
            results = self.c_trie.complete(word_bytes)
        else:
            results = self.c_trie.ambiguous_complete([w.encode('utf8') for w in word])

        yield from [w.decode() for w in results]

    def extend(self, words: list[str], multipliers: 'list[int] | None' = None):
        words_bytes = [word.encode('utf8') for word in words]
        if multipliers is None:
            self.c_trie.extend(words_bytes, [1 for _ in range(len(words_bytes))])
        else:
            self.c_trie.extend(words_bytes, multipliers)

    def __iter__(self) -> "Iterable[str]":
        return iter(self.complete(""))

    def __contains__(self, word: str) -> bool:
        return bool(self.count(word))

    def __len__(self) -> int:
        return len(list(self.complete("")))
