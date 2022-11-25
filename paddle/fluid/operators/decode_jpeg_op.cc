// Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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

#include <fstream>
#include <string>
#include <vector>

#include "paddle/fluid/framework/generator.h"
#include "paddle/fluid/framework/infershape_utils.h"
#include "paddle/fluid/framework/op_registry.h"
#include "paddle/fluid/framework/operator.h"
#include "paddle/fluid/platform/enforce.h"
#include "paddle/phi/core/infermeta_utils.h"
#include "paddle/phi/infermeta/unary.h"

namespace paddle {
namespace operators {

class DecodeJpegOp : public framework::OperatorWithKernel {
 public:
  using framework::OperatorWithKernel::OperatorWithKernel;

 protected:
  framework::OpKernelType GetExpectedKernelType(
      const framework::ExecutionContext& ctx) const override {
    return framework::OpKernelType(
        OperatorWithKernel::IndicateVarDataType(ctx, "X"), ctx.GetPlace());
  }

  framework::OpKernelType GetKernelTypeForVar(
      const std::string& var_name,
<<<<<<< HEAD
      const phi::DenseTensor& tensor,
      const framework::OpKernelType& expected_kernel_type) const override {
=======
      const framework::Tensor& tensor,
      const framework::OpKernelType& expected_kernel_type) const {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    if (var_name == "X") {
      return expected_kernel_type;
    }

    return framework::OpKernelType(
        framework::TransToProtoVarType(tensor.dtype()),
        tensor.place(),
        tensor.layout());
  }
};

class DecodeJpegOpMaker : public framework::OpProtoAndCheckerMaker {
 public:
  void Make() override {
    AddInput("X",
             "A one dimensional uint8 tensor containing the raw bytes "
             "of the JPEG image. It is a tensor with rank 1.");
    AddOutput("Out", "The output tensor of DecodeJpeg op");
    AddComment(R"DOC(
This operator decodes a JPEG image into a 3 dimensional RGB Tensor
or 1 dimensional Gray Tensor. Optionally converts the image to the
desired format. The values of the output tensor are uint8 between 0
and 255.
)DOC");
    AddAttr<std::string>(
        "mode",
        "(string, default \"unchanged\"), The read mode used "
        "for optionally converting the image, can be \"unchanged\" "
        ",\"gray\" , \"rgb\" .")
        .SetDefault("unchanged");
  }
};

}  // namespace operators
}  // namespace paddle

namespace ops = paddle::operators;
DECLARE_INFER_SHAPE_FUNCTOR(decode_jpeg,
                            DecodeJpegInferShapeFunctor,
                            PD_INFER_META(phi::DecodeJpegInferMeta));

REGISTER_OPERATOR(
    decode_jpeg,
    ops::DecodeJpegOp,
    ops::DecodeJpegOpMaker,
    paddle::framework::EmptyGradOpMaker<paddle::framework::OpDesc>,
    paddle::framework::EmptyGradOpMaker<paddle::imperative::OpBase>,
    DecodeJpegInferShapeFunctor)
