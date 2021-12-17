#pragma once

#include "SonomaServingApi.h"

#include "DataType.h"

#include <memory>
#include <string>
#include <vector>

namespace tensorflow
{
class Tensor;
}

namespace Microsoft
{
namespace ML
{
namespace Scoring
{
namespace Native
{
class TensorImpl;
class TensorFlowModel;
class OnnxModel;

// The Tensor vector interface allows constructing Tensor objects from vectors of common types,
// as well as retrieving the content of the Tensor as a vector.
#define TENSOR_TYPE_INTERFACE(TypeName) \
    SONOMASERVING_API Tensor(const std::vector<TypeName>& src); \
    SONOMASERVING_API Tensor(const std::vector<TypeName>& src, const std::vector<int64_t>& shape); \
    SONOMASERVING_API Tensor(const TypeName& src); \
    SONOMASERVING_API void CopyTo(std::vector<TypeName>& dst) const; \
    SONOMASERVING_API void CopyTo(std::vector<TypeName>& dst, int64_t src_idx, int64_t size) const; \
    SONOMASERVING_API void CastTo(std::vector<TypeName>& dst) const; \
    SONOMASERVING_API void CastTo(std::vector<TypeName>& dst, int64_t src_idx, int64_t size) const; \
    SONOMASERVING_API void GetData(const TypeName*& data) const; \

/// Tensors are multi-dimensional objects that have a specific type. For example:
/// 0-dimensional: scalar
/// 1-dimensional: vector
/// 2-dimensional: matrix
/// n-dimensiona: tensor
/// Tensors are fundamental data units that are used for passing the inputs and receiving outputs from the models.
class Tensor final
{
    friend class TensorFlowModel;
    friend class OnnxModel;

public:
    /// Parses the given string as a tensor of the given type.
    /// @param src String to parse.
    /// @param type Optionally, type of the tensor to assume when parsing. If not provided, attempt is made to infer
    /// the type from the string.
    ///  @returns On success, the tensor parsed from the string.
    /// @throws std::rutime_error if src could not be parsed as a valid tensor.
    SONOMASERVING_API static Tensor Parse(const std::string& src, DataType type = DataType::DATA_TYPE_INVALID);

    /// Destructor.
    SONOMASERVING_API ~Tensor();

    TENSOR_TYPE_INTERFACE(float)
    TENSOR_TYPE_INTERFACE(double)
    TENSOR_TYPE_INTERFACE(int8_t)
    TENSOR_TYPE_INTERFACE(int16_t)
    TENSOR_TYPE_INTERFACE(int32_t)
    TENSOR_TYPE_INTERFACE(int64_t)
    TENSOR_TYPE_INTERFACE(uint8_t)
    TENSOR_TYPE_INTERFACE(uint16_t)
    TENSOR_TYPE_INTERFACE(std::string)
    TENSOR_TYPE_INTERFACE(bool)


    /// @returns Total number of values in the tensor, regardless of its shape.
    SONOMASERVING_API int32_t GetSize() const;


    /// @returns Data type of the tensor.
    SONOMASERVING_API DataType GetDataType() const;


    /// @returns Shape of the tensor.
    SONOMASERVING_API const std::vector<int64_t>& GetShape() const;


    /// @returns Text representation of the tensor.
    SONOMASERVING_API std::string ToString() const;


    /// Checks if the tensor is equal to the other tensor.
    /// The tensors are considered equal if their data type, shape and content are equal.
    /// The content of tensors is compared element-wise using operator ==, which may not be desirable for
    /// tensors of floating-point types.
    /// @param other The tensor to compare this tensor with.
    /// @returns True if the tensors are equal, false otherwise.
    SONOMASERVING_API bool Equals(const Tensor& other) const;


    /// Checks if the tensor is equal to the other tensor.
    /// The tensors are considered equal if their data type, shape and content are equal.
    /// For tensors of floating-point types, the given precision is used for comparing the corresponding elements.
    /// @param other The tensor to compare this tensor with.
    /// @param precision Precision to use for comparing elements of the the floating-point type tensors. The parameter
    /// is ignored for other tensor types.
    /// @returns True if the tensors are equal, false otherwise.
    SONOMASERVING_API bool Equals(const Tensor& other, float precision) const;

private:
    /// Constructor. Creates a Sonoma tensor from a TensorFlow tensor. Should be used only by TensorFlow models.
    /// @param src TensorFlow tensor to create a Sonoma tensor from.
    explicit Tensor(const tensorflow::Tensor& src);
    explicit Tensor(const TensorImpl& src);


    /// Returns the Tensor's representation as TensorFlow tensor. Should be used only by TensorFlow models.
    /// @returns Internal representation of the Tensor.
    const tensorflow::Tensor& GetTensorFlowTensor() const;


    // Pointer to the internal implementation.
    std::shared_ptr<TensorImpl> m_impl;
};

}
}
}
}