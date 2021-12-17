#pragma once

#include <cstdint>

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{
    // Settings for a model.
    struct ModelSettings
    {
        virtual ~ModelSettings() = 0 {}

        // Execution Timeout in milliseconds.
        int32_t TimeoutMs{ 0 }; // TODO not used

        // If true, enable tracing while running the session.
        bool EnableTracing{ false };

        // If tracing is enabled, specifies the step interval for which one trace occurs.
        int32_t TracingStepInterval{ 0 };
    };

    // Settings for a TensorFlow model.
    struct TensorFlowModelSettings final : public ModelSettings
    {
        // If true, use a new set of threads for this session rather than the global
        // pool of threads. This may be useful if you want to limit a session to a
        // background pool with fewer threads.
        bool UsePerSessionThreads{ false };

        // The execution of an individual op (for some op types) can be
        // parallelized on a pool of intra_op_parallelism_threads.
        // 0 means the system picks an appropriate number.
        int32_t NumIntraOpThreads{ 0 };

        // Nodes that perform blocking operations are enqueued on a pool of
        // inter_op_parallelism_threads available in each process.
        // 0 means the system picks an appropriate number.
        int32_t NumInterOpThreads{ 0 };
    };
}
}
}
}