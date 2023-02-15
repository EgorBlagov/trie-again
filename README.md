# Trie Again: Python Trie implementation optimized for T9 completion


## Installation

```bash

pip install trie-again

# in some cases you might want to adjust your compiler (the same is applicable for `poetry install`)
CC='gcc' CFLAGS='-march=native' pip install trie-again

```

## Usage

```python

# create an instance
from trie_again import Trie

# if you want to use faster version
from trie_again import CyTrie

trie = Trie()

# insert a single word
trie.insert('boy')

# insert a list of words
trie.extend(['bondage', 'coverage'])

# insert a list of words with multipliers (useful when parsing json)
data = {
    'bondage': 10,
    'coverage': 20,
}
trie.extend(data.keys(), data.values())

# check key in trie
print('bondage' in trie)
# True

# list all keys, sorted by usage
print(list(trie))
# ['coverage', 'bondage', 'boy']

# complete simple, sorted by usage
print(list(trie.complete('b')))
# ['bondage', 'boy']
```

## T9 Like completion

```python

# complete with t9 like approach
print(list(trie.complete(['bc', 'o', 'vn'])))
# ['coverage', 'bondage']

```

### How it works?

```

b o y
b o n d a g e
c o v e r a g e
^ ^ ^
1 2 3

```

We use these groups to complete: `bc`, `o`, `vn`. It means that at position 1 it the letter may be `b` or `c`, at position 2 only `o`, at position 3 `v` or `n`.

## Test

```bash

# test behavior
poetry run pytest

# test performance
poetry run pytest --benchmark

```

## Dev

```bash

# very start (adjust compiler options if needed)
poetry install

# install pre commit
poetry run pre-commit install

# lint
poetry run black .
poetry run flake8 .
poetry run mypy .

# coverage
poetry run coverage run -m pytest && poetry run coverage report -m

# build package: limiting to sdist to compile it on install
poetry build -f sdist
```

## Read an article about the trie, friends!

https://blagovdaryu.hashnode.dev/ok-lets-trie-t9-in-python
