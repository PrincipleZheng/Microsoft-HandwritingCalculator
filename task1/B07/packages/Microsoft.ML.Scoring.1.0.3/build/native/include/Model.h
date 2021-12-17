#pragma once

#include "DataType.h"
#include "ObjectId.h"
#include "Tensor.h"

#include <string>
#include <unordered_map>

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{
    class Vocabulary;

    /// Contains data type for each input/output.
    typedef std::unordered_map<std::string, DataType> InputOutputTypeMap;

    /// Abstract class representing a model.
    /// Derived classes should implement details of actually loading and running a model.
    class Model
    {
    public:
        /// Constructor.
        Model() = default;


        /// Destructor.
        virtual ~Model() = 0
        {
        }


        /// @returns ID of the model.
        virtual const ObjectId& GetId() const = 0;


        /// Runs the model.
        /// @param inputs      List of (name, Tensor) pairs to provide as inputs to the model.
        /// @param outputNames List of names of outputs to return after the model is run.
        /// @param outputs     List to populate with outputs after the model is run.
        ///                    The order of returned items will match the order of outputNames list.
        /// @throws std::runtime_error Thrown when the model could not be run.
        virtual void Run(const std::vector<std::pair<std::string, Tensor>>& inputs,
                         const std::vector<std::string>& outputNames,
                         std::vector<Tensor>& outputs) = 0;


        /// @returns Map from valid input names to their type.
        virtual const InputOutputTypeMap& GetInputTypeMap() const = 0;


        /// @returns Map from valid output names to their type.
        virtual const InputOutputTypeMap& GetOutputTypeMap() const = 0;


        /// Gets a summary of model run traces.
        /// @returns The summary.
        virtual std::string GetRunTraceSummary() const = 0;


        /// Gets a vocabulary asset.
        /// @param name The vocabulary name.
        /// @returns The vocabulary asset.
        virtual std::shared_ptr<Vocabulary> GetVocabulary(const std::string& vocabularyName) const = 0;


        /// Copy constructor. Deleted.
        Model(const Model& other) = delete;


        /// Assignment operator. Deleted.
        Model& operator=(const Model& other) = delete;
    };
}
}
}
}