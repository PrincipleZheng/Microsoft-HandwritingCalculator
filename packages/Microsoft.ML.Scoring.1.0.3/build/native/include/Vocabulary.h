#pragma once

#include <string>

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{

/// Vocabulary containing all terms recognized by the model.
class Vocabulary
{
public:
    /// Constructor.
    Vocabulary() = default;


    /// Destructor.
    virtual ~Vocabulary() = 0
    {
    }

    /// Looks up the term in the vocabulary.
    /// @param term Term to look up.
    /// @returns Index of the term in the vocabulary, or -1 if the term was not found in the vocabulary.
    virtual int32_t GetIndex(const std::string& term) const = 0;


    /// Looks up the term for the given index in the vocabulary. Will only work if the vocabulary was initialized
    /// with the reverse lookup support.
    /// @param index Index in the vocabulary to return the term for.
    /// @param dst An object to initialize with the term's value on success.
    /// @returns True if the given index has a term in the vocabulary, false otherwise.
    virtual bool GetTerm(const int32_t index, std::string& dst) const = 0;


    /// Copy constructor. Deleted.
    Vocabulary(const Vocabulary& other) = delete;


    /// Assignment operator. Deleted.
    Vocabulary& operator=(const Vocabulary& other) = delete;
};

}
}
}
}