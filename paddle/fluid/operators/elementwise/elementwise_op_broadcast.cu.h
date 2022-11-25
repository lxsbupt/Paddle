// Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.1 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.1
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include "paddle/fluid/operators/elementwise/elementwise_op_impl.cu.h"

namespace paddle {
namespace operators {

template <ElementwiseType ET,
          typename InT,
          typename OutT,
          typename Functor,
          int NumOuts = 1>
void LaunchElementwiseCudaKernel(
    const KPDevice &ctx,
<<<<<<< HEAD
    const std::vector<const phi::DenseTensor *> &ins,
    std::vector<phi::DenseTensor *> *outs,
=======
    const std::vector<const framework::Tensor *> &ins,
    std::vector<framework::Tensor *> *outs,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    int axis,
    Functor func) {
  std::vector<const phi::DenseTensor *> pt_inputs;
  std::vector<phi::DenseTensor *> pt_outputs;
  // TODO(YuanRisheng) *_tmp for cache DenseTensor, because the temporary
  // DenseTensor obj
  // generated by MakePhiDenseTensor can be destroyed when exits loop. *_tmp
  // can be deleted
  // when DenseTensor support copy constructor.
  std::vector<std::unique_ptr<phi::DenseTensor>> pt_inputs_tmp;
  std::vector<std::unique_ptr<phi::DenseTensor>> pt_outputs_tmp;
  for (auto in : ins) {
    pt_inputs_tmp.emplace_back(
        std::move(paddle::experimental::MakePhiDenseTensor(*in)));
  }
  for (auto out : *outs) {
    pt_outputs_tmp.emplace_back(
        std::move(paddle::experimental::MakePhiDenseTensor(*out)));
  }
  for (int i = 0; i < pt_inputs_tmp.size(); i++) {
    pt_inputs.push_back(pt_inputs_tmp[i].get());
  }
  for (int i = 0; i < pt_outputs_tmp.size(); i++) {
    pt_outputs.push_back(pt_outputs_tmp[i].get());
  }
  phi::funcs::BroadcastKernel<ET, InT, OutT, Functor, NumOuts>(
      ctx, pt_inputs, &pt_outputs, axis, func);
}

}  // namespace operators
}  // namespace paddle
