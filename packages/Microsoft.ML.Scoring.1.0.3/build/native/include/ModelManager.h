#pragma once

#include "SonomaServingApi.h"

#include "Model.h"
#include "ObjectId.h"
#include "ModelSettings.h"

#include <memory>
#include <string>
#include <utility>

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{

/// ModelManager acts as a Facade for loading and running all models.
/// This class is thread-safe - models can be loaded, unloaded and retrieved without any external synchronization.
class ModelManager
{
public:
    /// Constructor.
    ModelManager() = default;

    /// Copy constructor. Deleted.
    /// @param other The ModelManager to copy from.
    ModelManager(const ModelManager& other) = delete;


    /// Assignment operator. Deleted.
    /// @param other The ModelManager to assign from.
    ModelManager& operator=(const ModelManager& other) = delete;


    /// Destructor
    virtual ~ModelManager() = 0
    {
    }


    /// Loads and initializes the model, so that it is ready to be run.
    /// @param id ID of the model to initialize.
    /// @throws std::runtime_error Thrown when the model could not be initialized.
    virtual void InitModel(const ObjectId& id) = 0;


    /// Loads and initializes the model, so that it is ready to be run.
    /// @param id ID of the model to initialize.
    /// @param settings Settings for model to be initialized.
    /// @throws std::runtime_error Thrown when the model could not be initialized.
    virtual void InitModel(const ObjectId& id, const ModelSettings& settings) = 0;


    /// Gets the model with the given ID.
    /// @param id ID of the model to get.
    /// @returns Pointer to the model with the given ID or nullptr if the model with the given ID is not currently
    /// initialized.
    virtual std::shared_ptr<Model> GetModel(const ObjectId& id) const = 0;


    /// Unloads the model with the given ID.
    /// @param id ID of the model to unload.
    virtual void UnloadModel(const ObjectId& id) = 0;
};

/// The different object source types.
enum class ObjectSourceType
{
    /// Represents objects in a hierarchical directory structure on the filesystem.
    filesystem,
    /// Represents objects in a flat directory structure on the filesystem.
    flatFilesystem,
};

/// Creates a model manager instance.
/// @param sourceType The object source type.
/// @param sourcePath The object source path.
/// @returns Pointer to a model manager.
SONOMASERVING_API
std::unique_ptr<ModelManager> CreateModelManager(ObjectSourceType sourceType, const std::string& sourcePath);
}
}
}
}