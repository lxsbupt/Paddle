/* Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */

#include "paddle/fluid/operators/collective/c_allreduce_op.h"

namespace paddle {
namespace framework {
class OpDesc;
template <typename T>
class EmptyGradOpMaker;
}  // namespace framework
namespace imperative {
class OpBase;
}  // namespace imperative
}  // namespace paddle

namespace paddle {
namespace operators {

class CAllReduceMaxOpMaker : public CAllReduceOpMaker {
 protected:
  std::string GetName() const override { return "Max"; }
};

DECLARE_INPLACE_OP_INFERER(AllreduceMaxInplaceInferer, {"X", "Out"});

}  // namespace operators
}  // namespace paddle

namespace ops = paddle::operators;
namespace plat = paddle::platform;

<<<<<<< HEAD
REGISTER_OPERATOR(
    c_allreduce_max,
    ops::CAllReduceOp,
    ops::CAllReduceMaxOpMaker,
    paddle::framework::EmptyGradOpMaker<paddle::framework::OpDesc>,
    paddle::framework::EmptyGradOpMaker<paddle::imperative::OpBase>,
    ops::AllreduceMaxInplaceInferer)
=======
REGISTER_OP_WITHOUT_GRADIENT(c_allreduce_max,
                             ops::CAllReduceOp,
                             ops::CAllReduceMaxOpMaker,
                             ops::AllreduceMaxInplaceInferer)
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

REGISTER_OP_CPU_KERNEL(c_allreduce_max,
                       ops::CAllReduceOpCPUKernel<ops::kRedMax, float>,
                       ops::CAllReduceOpCPUKernel<ops::kRedMax, double>,
                       ops::CAllReduceOpCPUKernel<ops::kRedMax, int>,
                       ops::CAllReduceOpCPUKernel<ops::kRedMax, int64_t>,
                       ops::CAllReduceOpCPUKernel<ops::kRedMax, plat::float16>);
