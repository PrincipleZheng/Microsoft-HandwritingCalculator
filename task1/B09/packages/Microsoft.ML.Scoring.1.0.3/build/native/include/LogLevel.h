#pragma once

#include "SonomaServingApi.h"

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{
/// Log levels supported by MLScoring Logger.
enum class LogLevel
{
    Debug,
    Info,
    Warning,
    Error,
};

/// Sets the minimum log level for emitted logging messages.
/// @param minimumLogLevel The minimum log level.
SONOMASERVING_API
void SetMinimumLogLevel(LogLevel minimumLogLevel);
}
}
}
}