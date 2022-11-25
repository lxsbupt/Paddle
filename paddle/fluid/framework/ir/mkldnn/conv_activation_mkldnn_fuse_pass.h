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

#include <string>

#include "paddle/fluid/framework/ir/fuse_pass_base.h"
#include "paddle/fluid/framework/ir/graph.h"

namespace paddle {
namespace framework {
namespace ir {

class ConvActivationMkldnnFusePass : public FusePassBase {
 public:
  ConvActivationMkldnnFusePass();
  virtual ~ConvActivationMkldnnFusePass() {}

 protected:
  void ApplyImpl(Graph *graph) const override;

  void FuseConvAct(Graph *graph,
                   const std::string &conv_type,
                   std::string &act_type) const;
<<<<<<< HEAD

  void FuseConvConcatAct(Graph *graph, std::string &act_type) const;
=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
};

}  // namespace ir
}  // namespace framework
}  // namespace paddle
