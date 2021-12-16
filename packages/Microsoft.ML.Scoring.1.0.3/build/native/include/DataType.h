#pragma once

#include <ostream>

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{
    // TODO this should be generated so it will be consistent with DataType.proto
    enum class DataType
    {
        DATA_TYPE_INVALID = 0,
        DATA_TYPE_FLOAT = 1,
        DATA_TYPE_DOUBLE = 2,
        DATA_TYPE_INT32 = 3,
        DATA_TYPE_UINT8 = 4,
        DATA_TYPE_INT16 = 5,
        DATA_TYPE_INT8 = 6,
        DATA_TYPE_STRING = 7,
        DATA_TYPE_INT64 = 9,
        DATA_TYPE_BOOL = 10,
        DATA_TYPE_UINT16 = 17
    };

    inline std::ostream& operator<<(std::ostream& os, const DataType& dataType)
    {
        return os << "Native::DataType (" << static_cast<int>(dataType) << ")";
    }
}
}
}
}