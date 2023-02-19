#ifndef TRIE_H
#define TRIE_H

#include <string>
#include <list>
#include <unordered_map>

class TrieNode
{
private:
    wchar_t letter;
    int insertion_count;
    std::unordered_map<wchar_t, TrieNode *> children;
    TrieNode *parent;
    std::wstring word;

    std::wstring bottom_up_traversal() const;

    std::list<const TrieNode *> word_nodes() const;
    inline std::wstring convert(const std::string &word) const;
    inline std::string reconvert(const std::wstring &word) const;
    inline std::list<std::string> unwrap_words(const std::list<const TrieNode *> &nodes) const;

public:
    TrieNode(wchar_t letter, TrieNode *parent = nullptr);
    ~TrieNode();
    void insert(const std::string &word, int multiplier = 1);
    int count(const std::string &word) const;
    std::list<std::string> complete(const std::string &prefix) const;
    std::list<std::string> ambiguous_complete(const std::list<std::string> &prefix_groups) const;
};

class Trie : public TrieNode
{
public:
    Trie();
    void extend(const std::list<std::string> &words, std::list<int> multipliers);
};

#endif
