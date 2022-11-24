/* Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.

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

#include "paddle/phi/core/dense_tensor.h"
#include "paddle/phi/core/sparse_coo_tensor.h"
#include "paddle/phi/kernels/empty_kernel.h"

namespace phi {
namespace sparse {

template <typename T, typename Context>
<<<<<<< HEAD
void CoalesceKernel(const Context& dev_ctx,
                    const SparseCooTensor& x,
                    SparseCooTensor* out);

template <typename T, typename Context>
SparseCooTensor Coalesce(const Context& dev_ctx, const SparseCooTensor& x) {
  SparseCooTensor coo;
  CoalesceKernel<T, Context>(dev_ctx, x, &coo);
=======
void CoalesceCooKernel(const Context& dev_ctx,
                       const SparseCooTensor& x,
                       SparseCooTensor* out);

template <typename T, typename Context>
SparseCooTensor CoalesceCoo(const Context& dev_ctx, const SparseCooTensor& x) {
  SparseCooTensor coo;
  CoalesceCooKernel<T, Context>(dev_ctx, x, &coo);
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
  return coo;
}

}  // namespace sparse
}  // namespace phi
