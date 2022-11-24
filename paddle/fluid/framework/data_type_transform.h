/* Copyright (c) 2016 PaddlePaddle Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */

#pragma once

#include <utility>

#include "paddle/fluid/framework/op_kernel_type.h"
#include "paddle/fluid/framework/tensor.h"
#include "paddle/fluid/framework/variable.h"
#include "paddle/fluid/platform/device_context.h"

namespace paddle {
namespace framework {

class OpKernelType;

using KernelTypePair = std::pair<OpKernelType, OpKernelType>;

void TransDataType(const OpKernelType& kernel_type_for_var,
                   const OpKernelType& expected_kernel_type,
<<<<<<< HEAD
                   const Tensor& in,
                   Tensor* out);
void TransDataType(const Tensor& in,
=======
                   const phi::DenseTensor& in,
                   phi::DenseTensor* out);
void TransDataType(const phi::DenseTensor& in,
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
                   const paddle::framework::proto::VarType::Type& type,
                   phi::DenseTensor* out);

/**
 * Transform complex gradient to real data type.
 *
 * If complex type promotion occurred in forward op, the grad output of
 * this op is complex data type, but the input variable may be real type,
 * in this case the grad input need to be cast to type same with input,
 * this casting executed at the end of grad op.
 *
 * note: call this function need to ensure that dst_type is real and
 * src_type is complex
 */
void TransComplexToReal(const proto::VarType::Type& dst_type,
                        const proto::VarType::Type& src_type,
<<<<<<< HEAD
                        const Tensor& in,
                        Tensor* out);
=======
                        const phi::DenseTensor& in,
                        phi::DenseTensor* out);
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

}  // namespace framework
}  // namespace paddle
