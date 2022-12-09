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

#ifdef PADDLE_WITH_XPU
#include <string>
#include <unordered_map>
#include <unordered_set>
#include "paddle/phi/backends/xpu/xpu_op_list.h"

namespace phi {
namespace backends {
namespace xpu {

XPUOpMap& get_kl2_ops() {
  // KL2支持的op，通过op_name, data_type, place来索引
  static XPUOpMap s_xpu2_kernels{
      {"abs", XPUKernelSet({phi::DataType::FLOAT32})},
      {"abs_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"adadelta", XPUKernelSet({phi::DataType::FLOAT32})},
      {"adamw", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"adam", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"arg_max", XPUKernelSet({phi::DataType::FLOAT32})},
      {"argsort_grad",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::FLOAT32})},
      {"argsort",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::FLOAT32})},
      {"assign",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT64,
                     phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::BOOL})},
      {"assign_value", XPUKernelSet({phi::DataType::FLOAT32})},
      {"batch_norm_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"batch_norm", XPUKernelSet({phi::DataType::FLOAT32})},
      {"bmm", XPUKernelSet({phi::DataType::FLOAT32})},
      {"bmm_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"bce_loss_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"bce_loss", XPUKernelSet({phi::DataType::FLOAT32})},
      {"beam_search",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT64,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"beam_search_decode",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT64,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"bilinear_interp_v2", XPUKernelSet({phi::DataType::FLOAT32})},
      {"bilinear_interp_v2_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"broadcast", XPUKernelSet({phi::DataType::FLOAT32})},
      {"c_allgather",
       XPUKernelSet({phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32,
                     phi::DataType::FLOAT64,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"c_allreduce_sum",
       XPUKernelSet({phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32,
                     phi::DataType::INT32})},
      {"c_embedding", XPUKernelSet({phi::DataType::FLOAT32})},
      {"c_identity",
       XPUKernelSet({phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32,
                     phi::DataType::FLOAT64,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"c_sync_calc_stream", XPUKernelSet({phi::DataType::FLOAT32})},
      {"c_sync_comm_stream", XPUKernelSet({phi::DataType::FLOAT32})},
      {"cast",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT64,
                     phi::DataType::BOOL,
                     phi::DataType::UINT8,
                     phi::DataType::INT64,
                     phi::DataType::INT32})},
      {"check_finite_and_unscale",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"clip", XPUKernelSet({phi::DataType::FLOAT32})},
      {"clip_by_norm", XPUKernelSet({phi::DataType::FLOAT32})},
      {"coalesce_tensor",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"concat_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"concat",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT64})},
      {"conv2d_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"conv2d",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"conv3d_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"conv3d",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"conv2d_transpose_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"conv2d_transpose", XPUKernelSet({phi::DataType::FLOAT32})},
      {"cumsum",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"deformable_conv_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"deformable_conv", XPUKernelSet({phi::DataType::FLOAT32})},
      {"depthwise_conv2d_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"depthwise_conv2d", XPUKernelSet({phi::DataType::FLOAT32})},
      {"dropout_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"dropout",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_add_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_add",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_div_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_div",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_floordiv",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_max_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_max",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_min_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_min",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_mul_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_mul",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_pow",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_sub_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"elementwise_sub",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT64})},
      {"elementwise_mod",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT64,
                     phi::DataType::INT32})},
      {"empty",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT16,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32,
                     phi::DataType::FLOAT64})},
      {"embedding_sparse_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"equal",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT32})},
      {"exp_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"exp", XPUKernelSet({phi::DataType::FLOAT32})},
      {"expand_as_v2",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"expand_v2",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"fill_any_like",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"fill_constant",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT16,
                     phi::DataType::UINT8,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT64,
                     phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::COMPLEX64,
                     phi::DataType::COMPLEX128})},
      {"flatten2_grad",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT8,
                     phi::DataType::FLOAT32})},
      {"flatten2",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT8,
                     phi::DataType::FLOAT32})},
      {"flatten_contiguous_range_grad",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT8,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"flatten_contiguous_range",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT8,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"flatten_grad",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT8,
                     phi::DataType::FLOAT32})},
      {"flatten",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::INT8,
                     phi::DataType::FLOAT32})},
      {"unfold",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"unfold_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"floor", XPUKernelSet({phi::DataType::FLOAT32})},
      {"gather_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"gather_nd",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::FLOAT32})},
      {"gather",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"gaussian_random", XPUKernelSet({phi::DataType::FLOAT32})},
      {"gelu_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"gelu", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"generate_proposals_v2", XPUKernelSet({phi::DataType::FLOAT32})},
      {"grad_add",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"greater_equal",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT32})},
      {"greater_than",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT32})},
      {"grid_sampler", XPUKernelSet({phi::DataType::FLOAT32})},
      {"hard_sigmoid_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"hard_sigmoid", XPUKernelSet({phi::DataType::FLOAT32})},
      {"hard_swish_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"hard_swish", XPUKernelSet({phi::DataType::FLOAT32})},
      {"huber_loss_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"huber_loss", XPUKernelSet({phi::DataType::FLOAT32})},
      {"kldiv_loss", XPUKernelSet({phi::DataType::FLOAT32})},
      {"kldiv_loss_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"iou_similarity", XPUKernelSet({phi::DataType::FLOAT32})},
      {"index_select",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"instance_norm", XPUKernelSet({phi::DataType::FLOAT32})},
      {"instance_norm_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"label_smooth", XPUKernelSet({phi::DataType::FLOAT32})},
      {"lamb", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"lars_momentum",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"layer_norm_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"layer_norm",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"leaky_relu_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"leaky_relu", XPUKernelSet({phi::DataType::FLOAT32})},
      {"less_equal",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT32})},
      {"less_than",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT32})},
      {"load", XPUKernelSet({phi::DataType::FLOAT32})},
      {"load_combine",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT64,
                     phi::DataType::INT8,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"log", XPUKernelSet({phi::DataType::FLOAT32})},
      {"log_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"log_softmax", XPUKernelSet({phi::DataType::FLOAT32})},
      {"log_softmax_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"lookup_table_v2_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"lookup_table_v2", XPUKernelSet({phi::DataType::FLOAT32})},
      {"masked_select",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"masked_select_grad",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"matmul_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"matmul_v2_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"matmul_v2",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"matmul",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"mean_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"mean", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"merged_momentum",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"mish_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"mish", XPUKernelSet({phi::DataType::FLOAT32})},
      {"momentum",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"mul", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"mul_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"nearest_interp_v2", XPUKernelSet({phi::DataType::FLOAT32})},
      {"nearest_interp_v2_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"not_equal",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT32})},
      {"one_hot", XPUKernelSet({phi::DataType::INT32, phi::DataType::INT64})},
      {"one_hot_v2",
       XPUKernelSet({phi::DataType::INT32, phi::DataType::INT64})},
      {"p_norm", XPUKernelSet({phi::DataType::FLOAT32})},
      {"p_norm_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"pad3d_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"pad3d", XPUKernelSet({phi::DataType::FLOAT32})},
      {"pool2d_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"pool2d",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"pow", XPUKernelSet({phi::DataType::FLOAT32})},
      {"pow_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"pow2_decay_with_linear_warmup", XPUKernelSet({phi::DataType::FLOAT32})},
      {"prior_box", XPUKernelSet({phi::DataType::FLOAT32})},
      {"range", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::INT64})},
      {"reciprocal", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reciprocal_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"reduce_max_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reduce_max", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reduce_mean_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reduce_mean", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reduce_min", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reduce_prod", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reduce_sum_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"reduce_sum", XPUKernelSet({phi::DataType::FLOAT32})},
      {"relu6", XPUKernelSet({phi::DataType::FLOAT32})},
      {"relu6_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"relu_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"relu", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"reshape2_grad",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT32})},
      {"reshape2",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT32})},
      {"resnet_unit",
       XPUKernelSet({phi::DataType::FLOAT16, phi::DataType::FLOAT32})},
      {"resnet_unit_grad",
       XPUKernelSet({phi::DataType::FLOAT16, phi::DataType::FLOAT32})},
      {"rmsprop", XPUKernelSet({phi::DataType::FLOAT32})},
      {"rnn", XPUKernelSet({phi::DataType::FLOAT32})},
      {"rnn_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"roi_align", XPUKernelSet({phi::DataType::FLOAT32})},
      {"roi_align_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"roll", XPUKernelSet({phi::DataType::FLOAT32})},
      {"roll_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"scale",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT64})},
      {"scatter",
       XPUKernelSet({phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::FLOAT32})},
      {"sampling_id",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT64})},
      {"set_value",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::FLOAT16,
                     phi::DataType::FLOAT32})},
      {"set_value_grad",
       XPUKernelSet({phi::DataType::FLOAT16, phi::DataType::FLOAT32})},
      {"sgd", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"sgd_dense_param_sparse_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"silu_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"silu", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"sigmoid_cross_entropy_with_logits_grad",
       XPUKernelSet({phi::DataType::FLOAT32})},
      {"sigmoid_cross_entropy_with_logits",
       XPUKernelSet({phi::DataType::FLOAT32})},
      {"shape", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::INT64})},
      {"sigmoid", XPUKernelSet({phi::DataType::FLOAT32})},
      {"sigmoid_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"sign", XPUKernelSet({phi::DataType::FLOAT32})},
      {"slice_grad",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT32})},
      {"slice",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT32,
                     phi::DataType::INT64})},
      {"softmax",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"softmax_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"softmax_with_cross_entropy_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"softmax_with_cross_entropy",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"softplus", XPUKernelSet({phi::DataType::FLOAT32})},
      {"softplus_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"split",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT32})},
      {"split_with_num",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT32})},
      {"sqrt", XPUKernelSet({phi::DataType::FLOAT32})},
      {"sqrt_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"square_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"square",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"squeeze2_grad",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32})},
      {"squeeze2",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32})},
      {"squeeze_grad",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32})},
      {"squeeze",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32})},
      {"stack",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::INT64,
                     phi::DataType::INT32})},
      {"stack_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::INT32})},
      {"strided_slice",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT16,
                     phi::DataType::INT32})},
      {"strided_slice_grad",
       XPUKernelSet({phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16,
                     phi::DataType::INT16,
                     phi::DataType::INT32})},
      {"sum", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"swish", XPUKernelSet({phi::DataType::FLOAT32})},
      {"swish_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"tanh_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"tanh", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"temporal_shift", XPUKernelSet({phi::DataType::FLOAT32})},
      {"temporal_shift_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"tril_triu",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::INT32})},
      {"tril_triu_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::INT32})},
      {"tile",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT32})},
      {"tile_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"transpose2_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"transpose2",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"transpose_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"transpose",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"truncated_gaussian_random", XPUKernelSet({phi::DataType::FLOAT32})},
      {"top_k", XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"top_k_v2", XPUKernelSet({phi::DataType::FLOAT32})},
      {"update_loss_scaling",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"uniform_random", XPUKernelSet({phi::DataType::FLOAT32})},
      {"unsqueeze2_grad",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16})},
      {"unsqueeze2",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32,
                     phi::DataType::FLOAT16})},
      {"unsqueeze_grad",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32})},
      {"unsqueeze",
       XPUKernelSet({phi::DataType::FLOAT64,
                     phi::DataType::INT64,
                     phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::INT8,
                     phi::DataType::UINT8,
                     phi::DataType::FLOAT32})},
      {"warpctc_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"warpctc", XPUKernelSet({phi::DataType::FLOAT32})},
      {"where_index",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::BOOL,
                     phi::DataType::FLOAT32})},
      {"where",
       XPUKernelSet({phi::DataType::INT32,
                     phi::DataType::INT64,
                     phi::DataType::FLOAT32})},

      // AddMore
      {"sequence_conv", XPUKernelSet({phi::DataType::FLOAT32})},
      {"sequence_conv_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"sequence_unpad", XPUKernelSet({phi::DataType::FLOAT32})},
      // Fused op
      {"resnet_basic_block_grad", XPUKernelSet({phi::DataType::FLOAT32})},
      {"resnet_basic_block", XPUKernelSet({phi::DataType::FLOAT32})},
      {"fused_gemm_epilogue",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"fused_gemm_epilogue_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"fused_attention",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"fused_attention_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"fused_feedforward",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
      {"fused_feedforward_grad",
       XPUKernelSet({phi::DataType::FLOAT32, phi::DataType::FLOAT16})},
  };

  return s_xpu2_kernels;
}

}  // namespace xpu
}  // namespace backends
}  // namespace phi
#endif
