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

#include "paddle/fluid/operators/beam_search_decode_op.h"
<<<<<<< HEAD
#include <string>
#include "paddle/fluid/framework/op_registry.h"
=======

#include <string>

#include "paddle/fluid/framework/convert_utils.h"
#include "paddle/fluid/platform/device_context.h"

namespace paddle {
namespace framework {
class InferShapeContext;
class OpDesc;
class Scope;
template <typename T>
class EmptyGradOpMaker;
}  // namespace framework
namespace imperative {
class OpBase;
}  // namespace imperative
}  // namespace paddle
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

namespace paddle {
namespace operators {

<<<<<<< HEAD
class BeamSearchDecodeOp : public framework::OperatorWithKernel {
 public:
  using framework::OperatorWithKernel::OperatorWithKernel;

  void InferShape(framework::InferShapeContext *ctx) const override {
    for (const std::string &arg : std::vector<std::string>({"Ids", "Scores"})) {
      OP_INOUT_CHECK(ctx->HasInput(arg), "Input", arg, "BeamSeachDecode");
    }
    for (const std::string &arg :
         std::vector<std::string>({"SentenceIds", "SentenceScores"})) {
      OP_INOUT_CHECK(ctx->HasOutput(arg), "Output", arg, "BeamSeachDecode");
    }
=======
struct BeamSearchDecodeFunctor {
  BeamSearchDecodeFunctor(const LoDTensorArray& step_ids,
                          const LoDTensorArray& step_scores,
                          LoDTensor* id_tensor,
                          LoDTensor* score_tensor,
                          size_t beam_size,
                          int end_id)
      : beam_size_(beam_size),
        end_id_(end_id),
        step_ids_origin_(step_ids),
        step_scores_origin_(step_scores),
        id_tensor_(id_tensor),
        score_tensor_(score_tensor) {
    tensor_on_gpu_ = false;
    tensor_on_npu_ = false;
    // First make a copy of GPU data on CPU
    if (platform::is_gpu_place(step_ids_origin_[0].place()) ||
        platform::is_npu_place(step_ids_origin_[0].place())) {
      if (platform::is_gpu_place(step_ids_origin_[0].place())) {
        tensor_on_gpu_ = true;
      } else {
        tensor_on_npu_ = true;
      }
      platform::DeviceContextPool& pool =
          platform::DeviceContextPool::Instance();
      auto* dev_ctx = pool.Get(step_ids_origin_[0].place());
      // Copy all tensors in the input tensor array
      for (auto& step_id : step_ids_origin_) {
        framework::LoDTensor out;
        if (step_id.numel() > 0) {
          if (tensor_on_gpu_) {
            dev_ctx->Wait();
          }
          framework::TensorCopy(step_id, platform::CPUPlace(), *dev_ctx, &out);
          dev_ctx->Wait();
        }

        out.set_lod(step_id.lod());
        step_ids_.push_back(out);
      }
    }
    if (platform::is_gpu_place(step_scores_origin_[0].place()) ||
        platform::is_npu_place(step_scores_origin_[0].place())) {
      if (platform::is_gpu_place(step_scores_origin_[0].place())) {
        tensor_on_gpu_ = true;
      } else {
        tensor_on_npu_ = true;
      }
      platform::DeviceContextPool& pool =
          platform::DeviceContextPool::Instance();
      auto* dev_ctx = pool.Get(step_scores_origin_[0].place());
      // Copy all tensors in the input tensor array
      for (auto& step_score : step_scores_origin_) {
        framework::LoDTensor out;
        if (step_score.numel() > 0) {
          if (tensor_on_gpu_) {
            dev_ctx->Wait();
          }
          framework::TensorCopy(
              step_score, platform::CPUPlace(), *dev_ctx, &out);
          dev_ctx->Wait();
        }

        out.set_lod(step_score.lod());
        step_scores_.push_back(out);
      }
    }
  }

  template <typename T>
  void apply() const;

  bool tensor_on_gpu_;
  bool tensor_on_npu_;
  size_t beam_size_;
  int end_id_;
  // TODO(Superjomn) Here might result serious performance issue in the
  // concurrency
  // scenarios.
  const LoDTensorArray& step_ids_origin_;
  const LoDTensorArray& step_scores_origin_;
  LoDTensorArray step_ids_ = LoDTensorArray();
  LoDTensorArray step_scores_ = LoDTensorArray();
  LoDTensor* id_tensor_;
  LoDTensor* score_tensor_;
};

template <typename T>
void BeamSearchDecodeFunctor::apply() const {
  BeamSearchDecoder<T> beam_search_decoder(beam_size_, end_id_);
  // Check if the tensor is on GPU or NPU. If so, use the CPU copy instead
  if (tensor_on_gpu_ || tensor_on_npu_) {
    beam_search_decoder.Backtrace(
        step_ids_, step_scores_, id_tensor_, score_tensor_);
  } else {
    beam_search_decoder.Backtrace(
        step_ids_origin_, step_scores_origin_, id_tensor_, score_tensor_);
  }
}

template <>
void BeamSearchDecodeFunctor::apply<bool>() const {
  PADDLE_THROW(platform::errors::InvalidArgument(
      "beam search decode op does not support bool!"));
}

class BeamSearchDecodeOp : public framework::OperatorBase {
 public:
  BeamSearchDecodeOp(const std::string& type,
                     const framework::VariableNameMap& inputs,
                     const framework::VariableNameMap& outputs,
                     const framework::AttributeMap& attrs)
      : OperatorBase(type, inputs, outputs, attrs) {}

 private:
  void RunImpl(const framework::Scope& scope,
               const platform::Place& dev_place) const override {
    platform::DeviceContextPool& pool = platform::DeviceContextPool::Instance();
    auto& dev_ctx = *pool.Get(dev_place);

    framework::RuntimeContext run_ctx(Inputs(), Outputs(), scope);
    framework::ExecutionContext ctx(*this, scope, dev_ctx, run_ctx);

    const LoDTensorArray* ids = ctx.Input<LoDTensorArray>("Ids");
    const LoDTensorArray* scores = ctx.Input<LoDTensorArray>("Scores");
    const size_t step_num = ids->size();
    PADDLE_ENFORCE_GT(
        step_num,
        0UL,
        platform::errors::InvalidArgument(
            "beam search steps, which is the"
            "size of Input(Ids) LoDTensorArray. beam search steps should "
            "be larger than 0, but received %d. ",
            step_num));
    const size_t source_num = ids->at(0).lod().at(0).size() - 1;
    PADDLE_ENFORCE_GT(
        source_num,
        0UL,
        platform::errors::InvalidArgument(
            "source_num is the sequence number of the"
            "first decoding step, indicating by Input(Ids)[0].lod[0].size. "
            "The number of source_num should be larger than"
            "0, but received %d. ",
            source_num));

    for (size_t i = 0; i < step_num; ++i) {
      PADDLE_ENFORCE_EQ(
          ids->at(i).lod().size(),
          2UL,
          platform::errors::InvalidArgument(
              "For the i step in beam search steps,"
              "the size of Input(Ids)[i].lod() should larger than 2,"
              "but received %d. ",
              ids->at(i).lod().size()));
    }

    size_t beam_size = ctx.Attr<int>("beam_size");
    int end_id = ctx.Attr<int>("end_id");

    // prepare output
    LoDTensor* sentenceIds = ctx.Output<LoDTensor>("SentenceIds");
    LoDTensor* sentenceScores = ctx.Output<LoDTensor>("SentenceScores");

    framework::VisitDataType(
        framework::TransToProtoVarType(scores->at(0).dtype()),
        BeamSearchDecodeFunctor(
            *ids, *scores, sentenceIds, sentenceScores, beam_size, end_id));
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
  }
};

class BeamSearchDecodeOpProtoMaker : public framework::OpProtoAndCheckerMaker {
 public:
  void Make() override {
    AddInput("Ids",
             "(LodTensorArray)"
             "The LodTensorArray containing the selected ids of all steps");
    AddInput("Scores",
             "(LodTensorArray)"
             "The LodTensorArray containing the selected scores of all steps");
    AddOutput(
        "SentenceIds",
        "(LodTensor)"
        "An LodTensor containing all generated id sequences for all source "
        "sentences");
    AddOutput(
        "SentenceScores",
        "(LodTensor)"
        "An LodTensor containing scores corresponding to Output(SentenceIds)");
    AddAttr<int>("beam_size", "beam size for beam search");
    AddAttr<int>("end_id",
                 "the token id which indicates the end of a sequence");
    AddComment(R"DOC(
Beam Search Decode Operator. This Operator constructs the full hypotheses for
each source sentence by walking back along the LoDTensorArray Input(ids)
whose lods can be used to restore the path in the beam search tree.

The Output(SentenceIds) and Output(SentenceScores) separately contain the
generated id sequences and the corresponding scores. The shapes and lods of the
two LodTensor are same. The lod level is 2 and the two levels separately
indicate how many hypotheses each source sentence has and how many ids each
hypothesis has.
)DOC");
  }
};

/*class BeamSearchDecodeInferShape : public framework::InferShapeBase {
 public:
  void operator()(framework::InferShapeContext* context) const override {
    OP_INOUT_CHECK(
        context->HasInput("Ids"), "Input", "Ids", "BeamSearchDecode");
    OP_INOUT_CHECK(
        context->HasInput("Scores"), "Input", "Scores", "BeamSearchDecode");
    OP_INOUT_CHECK(context->HasOutput("SentenceIds"),
                   "Output",
                   "SentenceIds",
                   "BeamSearchDecode");
    OP_INOUT_CHECK(context->HasOutput("SentenceScores"),
                   "Output",
                   "SentenceScores",
                   "BeamSearchDecode");
  }
};*/

class BeamSearchDecodeInferVarType : public framework::VarTypeInference {
 public:
<<<<<<< HEAD
  void operator()(framework::InferVarTypeContext *ctx) const override {
=======
  void operator()(framework::InferVarTypeContext* ctx) const override {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    ctx->SetOutputType("SentenceIds",
                       framework::proto::VarType::LOD_TENSOR,
                       framework::ALL_ELEMENTS);
    ctx->SetOutputType("SentenceScores",
                       framework::proto::VarType::LOD_TENSOR,
                       framework::ALL_ELEMENTS);
  }
};

}  // namespace operators
}  // namespace paddle

<<<<<<< HEAD
namespace ops = paddle::operators;
REGISTER_OPERATOR(beam_search_decode,
                  paddle::operators::BeamSearchDecodeOp,
                  paddle::operators::BeamSearchDecodeOpProtoMaker,
                  paddle::operators::BeamSearchDecodeInferVarType);

REGISTER_OP_CPU_KERNEL(
    beam_search_decode,
    ops::BeamSearchDecodeOpKernel<phi::CPUContext, float>,
    ops::BeamSearchDecodeOpKernel<phi::CPUContext, double>,
    ops::BeamSearchDecodeOpKernel<phi::CPUContext, paddle::platform::float16>,
    ops::BeamSearchDecodeOpKernel<phi::CPUContext, int>,
    ops::BeamSearchDecodeOpKernel<phi::CPUContext, int64_t>);
=======
REGISTER_OPERATOR(
    beam_search_decode,
    paddle::operators::BeamSearchDecodeOp,
    paddle::operators::BeamSearchDecodeOpProtoMaker,
    paddle::operators::BeamSearchDecodeInferShape,
    paddle::operators::BeamSearchDecodeInferVarType,
    paddle::framework::EmptyGradOpMaker<paddle::framework::OpDesc>,
    paddle::framework::EmptyGradOpMaker<paddle::imperative::OpBase>);
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
