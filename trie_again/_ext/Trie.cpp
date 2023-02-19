#include "Trie.h"
#include <string>
#include <stack>
#include <list>
#include <algorithm>
#include <iostream>

#include <locale>
#include <codecvt>

std::wstring_convert<std::codecvt_utf8_utf16<wchar_t> > converter;

std::wstring TrieNode::convert(const std::string &word) const
{
    return converter.from_bytes(word);
}

std::string TrieNode::reconvert(const std::wstring &word) const
{
    return converter.to_bytes(word);
}

std::wstring TrieNode::bottom_up_traversal() const
{
    std::wstring result;
    auto current = this;
    while (current && current->letter)
    {
        result.push_back(current->letter);
        current = current->parent;
    }

    std::reverse(result.begin(), result.end());
    return result;
}

std::list<const TrieNode *> TrieNode::word_nodes() const
{
    std::list<const TrieNode *> result;
    std::stack<const TrieNode *> dfs;
    dfs.push(this);
    while (!dfs.empty())
    {
        auto node = dfs.top();
        dfs.pop();
        if (node->insertion_count)
        {
            result.push_back(node);
        }

        for (auto child : node->children)
        {
            dfs.push(child.second);
        }
    }

    return result;
}

TrieNode::TrieNode(wchar_t letter, TrieNode *parent)
    : letter(letter), parent(parent), insertion_count(0), children()
{
    this->word = this->bottom_up_traversal();
}

TrieNode::~TrieNode()
{
    for (auto child : children)
    {
        delete child.second;
    }
}

void TrieNode::insert(const std::string &word_utf8, int multiplier)
{
    auto word = this->convert(word_utf8);
    if (word.empty())
    {
        return;
    }

    auto current = this;
    for (int i = 0; i < word.size(); i++)
    {
        if (!current->children.count(word[i]))
        {
            current->children[word[i]] = new TrieNode(word[i], current);
        }

        current = current->children[word[i]];
    }

    current->insertion_count += multiplier;
}

int TrieNode::count(const std::string &word_utf8) const
{
    auto word = this->convert(word_utf8);
    auto current = this;
    for (int i = 0; i < word.size(); i++)
    {
        if (!current->children.count(word[i]))
        {
            return 0;
        }

        current = current->children.at(word[i]);
    }

    return current->insertion_count;
}

inline std::list<std::string> TrieNode::unwrap_words(const std::list<const TrieNode *> &candidates) const
{
    std::list<const TrieNode *> word_nodes;
    for (auto candidate : candidates)
    {
        auto words = candidate->word_nodes();
        word_nodes.insert(word_nodes.end(), words.begin(), words.end());
    }

    std::list<std::string> result;
    word_nodes.sort([](auto a, auto b)
                    { return a->insertion_count > b->insertion_count; });

    for (auto node : word_nodes)
    {
        result.push_back(this->reconvert(node->word));
    }

    return result;
}

std::list<std::string> TrieNode::complete(const std::string &prefix) const
{
    std::list<std::string> result;

    auto current = this;
    for (int i = 0; i < prefix.size(); i++)
    {
        if (!current->children.count(prefix[i]))
        {
            return result;
        }

        current = current->children.at(prefix[i]);
    }

    return this->unwrap_words({current});
}

std::list<std::string> TrieNode::ambiguous_complete(const std::list<std::string> &prefix_groups) const
{
    std::list<const TrieNode *> candidates = {this};
    for (auto gr : prefix_groups)
    {
        std::wstring group = this->convert(gr);
        std::list<const TrieNode *> new_candidates;
        for (int i = 0; i < group.size(); i++)
        {
            for (auto candidate : candidates)
            {
                if (candidate->children.count(group[i]))
                {
                    new_candidates.push_back(candidate->children.at(group[i]));
                }
            }
        }
        candidates = std::move(new_candidates);
    }

    return this->unwrap_words(candidates);
}

Trie::Trie() : TrieNode(0) {}

void Trie::extend(const std::list<std::string> &words, std::list<int> multipliers)
{
    if (multipliers.size() != words.size())
    {
        throw std::invalid_argument("words and multipliers must have the same size");
    }

    auto word = words.begin();
    auto mp = multipliers.begin();
    for (; word != words.end(); word++, mp++)
    {
        this->insert(*word, *mp);
    }
}
