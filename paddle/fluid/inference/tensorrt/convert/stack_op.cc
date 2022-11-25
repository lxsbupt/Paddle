/* Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */

#include "paddle/fluid/inference/tensorrt/convert/op_converter.h"
#include "paddle/fluid/inference/tensorrt/plugin/stack_op_plugin.h"

namespace paddle {
namespace framework {
class Scope;
namespace proto {
class OpDesc;
}  // namespace proto
}  // namespace framework
}  // namespace paddle

namespace paddle {
namespace inference {
namespace tensorrt {

/*
 * Stack converter from fluid to tensorRT.
 */
class StackOpConverter : public OpConverter {
 public:
  void operator()(const framework::proto::OpDesc& op,
                  const framework::Scope& scope,
                  bool test_mode) override {
    VLOG(4) << "convert fluid stack op to tensorrt stack layer";

    framework::OpDesc op_desc(op, nullptr);
    auto input = op_desc.Input("X");
    int input_num = input.size();
    std::vector<nvinfer1::ITensor*> inputs;

    for (int i = 0; i < input_num; ++i) {
      inputs.push_back(engine_->GetITensor(input[i]));
      if (op_desc.HasAttr("out_threshold")) {
        float out_scale =
            PADDLE_GET_CONST(float, op_desc.GetAttr("out_threshold"));
        engine_->SetTensorDynamicRange(inputs[i], out_scale);
      }
    }

    int axis = PADDLE_GET_CONST(int, op_desc.GetAttr("axis"));
<<<<<<< HEAD
    int output_rank = inputs[0]->getDimensions().nbDims + 1;
=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    if (axis < 0) {
      axis = axis + output_rank;
    }
    // Now, axis is relative to output_rank.

    auto* shape_tensor = Shape(inputs[0]);
    std::vector<nvinfer1::ITensor*> shape_tensor_vec;
    for (int i = 0; i < output_rank; i++) {
      if (i < axis) {
        shape_tensor_vec.push_back(GetEleTensorOfShape(shape_tensor, i));
      } else if (i > axis) {
        shape_tensor_vec.push_back(GetEleTensorOfShape(shape_tensor, i - 1));
      } else {
        shape_tensor_vec.push_back(Add1DConstantLayer(1));
      }
    }
    auto* after_shape_tensor = Concat(shape_tensor_vec);

    for (int i = 0; i < input_num; ++i) {
      auto* reshape_layer = TRT_ENGINE_ADD_LAYER(engine_, Shuffle, *inputs[i]);
      reshape_layer->setInput(1, *after_shape_tensor);
      inputs[i] = reshape_layer->getOutput(0);
    }

    auto* layer = TRT_ENGINE_ADD_LAYER(
        engine_, Concatenation, inputs.data(), inputs.size());
    layer->setAxis(axis);

<<<<<<< HEAD
=======
    nvinfer1::ILayer* layer = nullptr;
#if IS_TRT_VERSION_GE(6000)
    bool with_fp16 = engine_->WithFp16() && !engine_->disable_trt_plugin_fp16();
    plugin::StackPluginDynamic* plugin =
        new plugin::StackPluginDynamic(axis, input_num, with_fp16);
    layer = engine_->AddDynamicPlugin(inputs, input_num, plugin);
    PADDLE_ENFORCE_NOT_NULL(
        layer,
        platform::errors::InvalidArgument(
            "trt stack layer in converter could not be created."));
#else
    PADDLE_THROW(platform::errors::Fatal(
        "You are running the TRT Dynamic Shape mode, need to confirm that "
        "your TRT version is no less than 6.0"));
#endif
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    auto output_name = op_desc.Output("Y").front();
    RreplenishLayerAndOutput(layer, "stack", {output_name}, test_mode);
  }
};

}  // namespace tensorrt
}  // namespace inference
}  // namespace paddle

REGISTER_TRT_OP_CONVERTER(stack, StackOpConverter);
