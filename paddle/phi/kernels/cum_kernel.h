// Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

<<<<<<< HEAD
#include "paddle/phi/common/scalar.h"
=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
#include "paddle/phi/core/dense_tensor.h"

namespace phi {

template <typename T, typename Context>
void CumsumKernel(const Context& dev_ctx,
                  const DenseTensor& x,
<<<<<<< HEAD
                  const Scalar& axis,
=======
                  int axis,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                  bool flatten,
                  bool exclusive,
                  bool reverse,
                  DenseTensor* out);

template <typename T, typename Context>
void LogcumsumexpKernel(const Context& dev_ctx,
                        const DenseTensor& x,
                        int axis,
                        bool flatten,
                        bool exclusive,
                        bool reverse,
                        DenseTensor* out);

}  // namespace phi
