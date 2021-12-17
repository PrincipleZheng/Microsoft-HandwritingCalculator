#pragma once

#include <limits>
#include <string>

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{

/// Object IDs are used to identify objects whose lifetime is managed by MLScoring.
/// They can be used to precisely tell MLScoring what object needs to be accessed.
class ObjectId final
{
public:
    /// A pre-defined value for the version field that indicates 'whatever latest version is avaliable'.
    static const int32_t c_latestVersion = std::numeric_limits<int32_t>::max();

    /// Constructs an ID with an empty object name and latest version.
    ObjectId()
        : m_name(), m_version(c_latestVersion)
    {
    }


    /// Constructs an ID for the latest version of the object with the given name.
    /// @param name Name of the object.
    ObjectId(const std::string& name)
        : m_name(name), m_version(c_latestVersion)
    {
    }


    /// Constructs an ID for the object with the given name and version.
    /// @param name Name of the object.
    /// @param version Version of the object.
    ObjectId(const std::string& name, int32_t version)
        : m_name(name), m_version(version)
    {
    }


    /// @returns Name of the object the ID refers to.
    const std::string& GetName() const
    {
        return m_name;
    }


    /// @returns Version of the object the ID refers to.
    int32_t GetVersion() const
    {
        return m_version;
    }

private:
    // Name of the object.
    std::string m_name;

    // Version of the object.
    int32_t m_version;
};

/// Checks if one ID is smaller than the other ID. Orders by name ACC and then version DESC.
/// @param a First ID.
/// @param b Second ID.
/// @returns True if ID a is 'less' than ID b.
inline bool operator <(const ObjectId& a, const ObjectId& b)
{
    return (a.GetName() == b.GetName()) ? (a.GetVersion() > b.GetVersion()) : (a.GetName() < b.GetName());
}


/// Appends the human-readable representation of the ObjectId to the provided stream.
/// @param out Stream to output the ObjectId representation to.
/// @param id Id to output.
/// @returns The instance of the stream that has representation of the ObjectId appended to it.
inline std::ostream& operator <<(std::ostream& out, const ObjectId& id)
{
    if (id.GetVersion() != ObjectId::c_latestVersion)
    {
        out << "(" << id.GetName() << "," << id.GetVersion() << ")";
    }
    else
    {
        out << "(" << id.GetName() << ",Latest)";
    }
    return out;
}

}
}
}
}