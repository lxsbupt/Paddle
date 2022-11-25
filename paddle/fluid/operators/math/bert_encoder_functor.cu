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

#include <algorithm>
#include <type_traits>

#include "paddle/fluid/framework/tensor.h"
#include "paddle/fluid/framework/tensor_util.h"
#include "paddle/fluid/operators/math/bert_encoder_functor.h"
#include "paddle/fluid/platform/enforce.h"
#include "paddle/phi/kernels/funcs/blas/blas.h"
#include "paddle/phi/kernels/funcs/math_cuda_utils.h"

namespace paddle {
namespace operators {
namespace math {

// NOTE(chenfeiyu): explicitly use operator+ for float2
// since float2 is not in namespace phi::funcs, ADL won't help
using phi::funcs::operator+;

template <typename T>
__device__ __forceinline__ T local_rsqrt(T num) {
  return rsqrt(static_cast<float>(num));
}
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
__device__ __forceinline__ half local_rsqrt(half num) { return hrsqrt(num); }
#endif

template <typename T, int TPB>
__device__ inline void LayerNormSmall(T val,
                                      const phi::funcs::kvp<T> &thread_data,
                                      const int ld,
                                      const int idx,
<<<<<<< HEAD
                                      const T *bias,
                                      const T *scale,
=======
                                      const float *bias,
                                      const float *scale,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                      T *output,
                                      T eps) {
  using BlockReduce = cub::BlockReduce<phi::funcs::kvp<T>, TPB>;
  __shared__ typename BlockReduce::TempStorage temp_storage;
  __shared__ T mu;      // mean
  __shared__ T rsigma;  // 1 / std.dev.

  const auto sum_kv = BlockReduce(temp_storage).Reduce(thread_data, cub::Sum());

  if (threadIdx.x == 0) {
    mu = sum_kv.key;
    rsigma = local_rsqrt(sum_kv.value - mu * mu + eps);
  }
  __syncthreads();

  if (threadIdx.x < ld) {
    const T g(scale[threadIdx.x]);
    const T b(bias[threadIdx.x]);
    output[idx] = g * (val - mu) * rsigma + b;
  }
}

template <typename T, int TPB>
__device__ inline void LayerNorm(const phi::funcs::kvp<T> &thread_data,
                                 const int ld,
                                 const int offset,
<<<<<<< HEAD
                                 const T *bias,
                                 const T *scale,
=======
                                 const float *bias,
                                 const float *scale,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                 T *output,
                                 T eps) {
  using BlockReduce = cub::BlockReduce<phi::funcs::kvp<T>, TPB>;
  __shared__ typename BlockReduce::TempStorage temp_storage;
  __shared__ T mu;      // mean
  __shared__ T rsigma;  // 1 / std.dev.

  const auto sum_kv = BlockReduce(temp_storage).Reduce(thread_data, cub::Sum());

  if (threadIdx.x == 0) {
    mu = sum_kv.key;
    rsigma = local_rsqrt(sum_kv.value - mu * mu + eps);
  }
  __syncthreads();

  for (int i = threadIdx.x; i < ld; i += TPB) {
    const int idx = offset + i;
    const T val = output[idx];
    const T g(scale[i]);
    const T b(bias[i]);
    output[idx] = g * (val - mu) * rsigma + b;
  }
}

template <typename T, typename T2, int TPB>
__device__ inline void LayerNorm2(const phi::funcs::kvp<T> &thread_data,
                                  const int ld,
                                  const int offset,
<<<<<<< HEAD
                                  const T2 *bias,
                                  const T2 *scale,
=======
                                  const float2 *bias,
                                  const float2 *scale,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                  T2 *output,
                                  T eps) {
  using BlockReduce = cub::BlockReduce<phi::funcs::kvp<T>, TPB>;
  __shared__ typename BlockReduce::TempStorage temp_storage;
  __shared__ T mu;      // mean
  __shared__ T rsigma;  // 1 / std.dev.

  const auto sum_kv = BlockReduce(temp_storage).Reduce(thread_data, cub::Sum());

  if (threadIdx.x == 0) {
    mu = sum_kv.key;
    rsigma = local_rsqrt(sum_kv.value - mu * mu + eps);
  }
  __syncthreads();

  for (int i = threadIdx.x; i < ld; i += TPB) {
    const int idx = offset + i;
    T2 val = output[idx];
    const T2 g = scale[i];
    const T2 b = bias[i];
    val.x = T(g.x) * (val.x - mu) * rsigma + T(b.x);
    val.y = T(g.y) * (val.y - mu) * rsigma + T(b.y);
    output[idx] = val;
  }
}

template <typename T, unsigned TPB>
__global__ void EmbEltwiseLayernormKernel(int hidden,
                                          const int64_t *ids,
<<<<<<< HEAD
                                          const T *scale,
                                          const T *bias,
                                          const int64_t *embs,
                                          T *output,
                                          T eps,
=======
                                          const float *scale,
                                          const float *bias,
                                          const int64_t *embs,
                                          T *output,
                                          float eps,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                          int input_num) {
  cub::Sum pair_sum;
  // blockIdx.x: position in the sequence
  // blockIdx.y: batch
  // gridDim.x: Seq
  // gridDim.y: Batch

  extern __shared__ int64_t array_id[];

  const T rhidden = T(1.f) / T(hidden);
  const int64_t seq_pos = blockIdx.y + blockIdx.x * gridDim.y;
  if (threadIdx.x == 0) {
    for (int i = 0; i < input_num; ++i) {
      const int64_t *ids_p = reinterpret_cast<const int64_t *>(ids[i]);
      array_id[i] = ids_p[seq_pos];
    }
  }
  __syncthreads();

  const int64_t out_offset = seq_pos * hidden;

  phi::funcs::kvp<T> thread_data(0, 0);

#pragma unroll
  for (int it = threadIdx.x; it < hidden; it += TPB) {
    T val = 0;
    for (int i = 0; i < input_num; ++i) {
      val += reinterpret_cast<const T *>(embs[i])[array_id[i] * hidden + it];
    }

    output[out_offset + it] = val;
    const T rhiddenval = rhidden * val;
    thread_data =
        pair_sum(thread_data, phi::funcs::kvp<T>(rhiddenval, rhiddenval * val));
  }
  LayerNorm<T, TPB>(thread_data, hidden, out_offset, bias, scale, output, eps);
}

// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#ifndef __HIPCC__  // @{ Half kernel: EmbEltwiseLayernormKernel
template <>
__global__ void EmbEltwiseLayernormKernel<half, 256>(int hidden,
                                                     const int64_t *ids,
<<<<<<< HEAD
                                                     const half *scale,
                                                     const half *bias,
                                                     const int64_t *embs,
                                                     half *output,
                                                     half eps,
=======
                                                     const float *scale,
                                                     const float *bias,
                                                     const int64_t *embs,
                                                     half *output,
                                                     float eps,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                                     int input_num) {
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
  cub::Sum pair_sum;
  // blockIdx.x: position in the sequence
  // blockIdx.y: batch
  // gridDim.x: Seq
  // gridDim.y: Batch

  extern __shared__ int64_t array_id[];

  const half rhidden = half(1.f) / half(hidden);
  const int64_t seq_pos = blockIdx.y + blockIdx.x * gridDim.y;
  if (threadIdx.x == 0) {
    for (int i = 0; i < input_num; ++i) {
      const int64_t *ids_p = reinterpret_cast<const int64_t *>(ids[i]);
      array_id[i] = ids_p[seq_pos];
    }
  }
  __syncthreads();

  const int64_t out_offset = seq_pos * hidden;

  phi::funcs::kvp<half> thread_data(0, 0);

#pragma unroll
  for (int it = threadIdx.x; it < hidden; it += 256) {
    half val = 0;
    for (int i = 0; i < input_num; ++i) {
      val += reinterpret_cast<const half *>(embs[i])[array_id[i] * hidden + it];
    }

    output[out_offset + it] = val;
    const half rhiddenval = rhidden * val;
    thread_data = pair_sum(thread_data,
                           phi::funcs::kvp<half>(rhiddenval, rhiddenval * val));
  }
  LayerNorm<half, 256>(
      thread_data, hidden, out_offset, bias, scale, output, eps);
#endif
}
#endif  // @} End Half kernel: EmbEltwiseLayernormKernel

template <typename T>
void EmbEltwiseLayerNormFunctor<T>::operator()(int batch,
                                               int seq_len,
                                               int hidden,
                                               const int64_t *ids,
<<<<<<< HEAD
                                               const T *scale,
                                               const T *bias,
=======
                                               const float *scale,
                                               const float *bias,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                               const int64_t *embs,
                                               T *output,
                                               float eps,
                                               int input_num,
                                               gpuStream_t stream) {
  const unsigned tpb = 256;
  const dim3 grid(seq_len, batch, 1);
  const dim3 block(tpb, 1, 1);
  int shared_bytes = input_num * sizeof(int64_t);
  EmbEltwiseLayernormKernel<T, tpb><<<grid, block, shared_bytes, stream>>>(
      hidden, ids, scale, bias, embs, output, eps, input_num);
}

template class EmbEltwiseLayerNormFunctor<float>;

// device function 'operator()' is not supportted until cuda 10.0
// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#if defined(PADDLE_WITH_CUDA) && CUDA_VERSION >= 10000
template class EmbEltwiseLayerNormFunctor<half>;
#endif

template <typename T>
__global__ void SoftmaxKernelWithEltadd(T *qk_buf_,
                                        const T *bias_qk_,
                                        const int batch_size,
                                        const int head_num,
                                        const int seq_len,
                                        const unsigned mask) {
  int qk_offset = blockIdx.x * seq_len;
  assert(blockDim.x % 32 == 0);

  float tmp = threadIdx.x < seq_len
                  ? static_cast<float>(qk_buf_[threadIdx.x + qk_offset] +
                                       bias_qk_[threadIdx.x + qk_offset])
                  : -1e20f;
  float max_val = phi::funcs::blockReduceMax<float>(tmp, mask);

  float qk_tmp = threadIdx.x < seq_len ? __expf(tmp - max_val) : 0.0f;
  float sum_val = phi::funcs::blockReduceSum<float>(qk_tmp, mask);

  if (threadIdx.x < seq_len)
    qk_buf_[threadIdx.x + qk_offset] = (T)(qk_tmp / sum_val);
}

// HIP defined __HIP_NO_HALF_CONVERSIONS__
#ifndef __HIPCC__  // @{ Half kernel: SoftmaxKernelWithEltadd
template <>
__global__ void SoftmaxKernelWithEltadd<half>(half *qk_buf_,
                                              const half *bias_qk_,
                                              const int batch_size,
                                              const int head_num,
                                              const int seq_len,
                                              const unsigned mask) {
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
  int qk_offset = blockIdx.x * seq_len;
  assert(blockDim.x % 32 == 0);

  float tmp = threadIdx.x < seq_len
                  ? static_cast<float>(qk_buf_[threadIdx.x + qk_offset] +
                                       bias_qk_[threadIdx.x + qk_offset])
                  : -1e20f;
  float max_val = phi::funcs::blockReduceMax<float>(tmp, mask);

  float qk_tmp = threadIdx.x < seq_len ? __expf(tmp - max_val) : 0.0f;
  float sum_val = phi::funcs::blockReduceSum<float>(qk_tmp, mask);

  if (threadIdx.x < seq_len)
    qk_buf_[threadIdx.x + qk_offset] = (half)(qk_tmp / sum_val);
#endif
}
#endif  // @} End Half kernel: SoftmaxKernelWithEltadd

template <typename T>
__global__ void SoftmaxKernelWithEltadd2(T *qk_buf_,
                                         const T *bias_qk_,
                                         const int batch_size,
                                         const int head_num,
                                         const int seq_len,
                                         const unsigned mask) {
  int qk_offset = blockIdx.x * seq_len;
  int idx = threadIdx.x;
  assert(blockDim.x % 32 == 0);

  float2 tmp = idx < seq_len
                   ? phi::funcs::ToFloat2<T>(qk_buf_[idx + qk_offset] +
                                             bias_qk_[idx + qk_offset])
                   : make_float2(-1e20f, -1e20f);
  float max_val = phi::funcs::blockReduceMax<float>(max(tmp.x, tmp.y), mask);
  float2 qk_tmp = idx < seq_len ? make_float2(__expf(tmp.x - max_val),
                                              __expf(tmp.y - max_val))
                                : make_float2(0.f, 0.f);
  float sum_val =
      phi::funcs::blockReduceSum<float>(qk_tmp.x + qk_tmp.y, mask) + 1e-6f;

  if (idx < seq_len) {
    qk_buf_[idx + qk_offset] =
        phi::funcs::FloatsToPair<T>(qk_tmp.x / sum_val, qk_tmp.y / sum_val);
  }
}

template <>
__global__ void SoftmaxKernelWithEltadd2<half2>(half2 *qk_buf_,
                                                const half2 *bias_qk_,
                                                const int batch_size,
                                                const int head_num,
                                                const int seq_len,
                                                const unsigned mask) {
// operator "+" of half only suppotted after cuda version 10.0
// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#if defined(PADDLE_WITH_CUDA) && \
    (CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__) && CUDA_VERSION >= 10000)
  int qk_offset = blockIdx.x * seq_len;
  int idx = threadIdx.x;
  assert(blockDim.x % 32 == 0);

  float2 tmp = idx < seq_len
                   ? phi::funcs::ToFloat2<half2>(qk_buf_[idx + qk_offset] +
                                                 bias_qk_[idx + qk_offset])
                   : make_float2(-1e20f, -1e20f);
  float max_val = phi::funcs::blockReduceMax<float>(max(tmp.x, tmp.y), mask);
  float2 qk_tmp = idx < seq_len ? make_float2(__expf(tmp.x - max_val),
                                              __expf(tmp.y - max_val))
                                : make_float2(0.f, 0.f);
  float sum_val =
      phi::funcs::blockReduceSum<float>(qk_tmp.x + qk_tmp.y, mask) + 1e-6f;

  if (idx < seq_len) {
    qk_buf_[idx + qk_offset] =
        phi::funcs::FloatsToPair<half2>(qk_tmp.x / sum_val, qk_tmp.y / sum_val);
  }
#endif
}

template <typename T>
__global__ void SoftmaxKernelWithEltaddForLarge(T *qk_buf,
                                                const T *bias_qk,
                                                const int batch_size,
                                                const int head_num,
                                                const int seq_len,
                                                const unsigned mask) {
  int qk_offset = blockIdx.x * seq_len;
  assert(blockDim.x % 32 == 0);

  T stride_max = -1e20f;
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    stride_max = qk_buf[threadIdx.x + i + qk_offset] +
                             bias_qk[threadIdx.x + i + qk_offset] >
                         stride_max
                     ? qk_buf[threadIdx.x + i + qk_offset] +
                           bias_qk[threadIdx.x + i + qk_offset]
                     : stride_max;
  }
  T max_val = phi::funcs::blockReduceMax<T>(stride_max, mask);

  T stride_sum = 0.f;
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    stride_sum += __expf(qk_buf[threadIdx.x + i + qk_offset] +
                         bias_qk[threadIdx.x + i + qk_offset] - max_val);
  }
  T sum_val = phi::funcs::blockReduceSum<T>(stride_sum, mask);

  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    qk_buf[threadIdx.x + i + qk_offset] =
        (T)(__expf(qk_buf[threadIdx.x + i + qk_offset] +
                   bias_qk[threadIdx.x + i + qk_offset] - max_val) /
            sum_val);
  }
}

// HIP defined __HIP_NO_HALF_CONVERSIONS__
#ifndef __HIPCC__  // @{ Half kernel: SoftmaxKernelWithEltadd
template <>
__global__ void SoftmaxKernelWithEltaddForLarge(half *qk_buf,
                                                const half *bias_qk,
                                                const int batch_size,
                                                const int head_num,
                                                const int seq_len,
                                                const unsigned mask) {
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
  int qk_offset = blockIdx.x * seq_len;
  assert(blockDim.x % 32 == 0);

  float stride_max = -1e20f;
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float tmp = static_cast<float>(qk_buf[threadIdx.x + i + qk_offset] +
                                   bias_qk[threadIdx.x + i + qk_offset]);
    stride_max = tmp > stride_max ? tmp : stride_max;
  }
  float max_val = phi::funcs::blockReduceMax<float>(stride_max, mask);

  float stride_sum = 0.f;
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float tmp = static_cast<float>(qk_buf[threadIdx.x + i + qk_offset] +
                                   bias_qk[threadIdx.x + i + qk_offset]);
    stride_sum += __expf(tmp - max_val);
  }
  float sum_val = phi::funcs::blockReduceSum<float>(stride_sum, mask);

  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float tmp =
        __expf(static_cast<float>(qk_buf[threadIdx.x + i + qk_offset] +
                                  bias_qk[threadIdx.x + i + qk_offset]) -
               max_val);
    qk_buf[threadIdx.x + i + qk_offset] = (half)(tmp / sum_val);
  }
#endif
}
#endif  // @} End Half kernel: SoftmaxKernelWithEltadd

template <typename T>
__global__ void SoftmaxKernelWithEltaddForLarge2(T *qk_buf_,
                                                 const T *bias_qk_,
                                                 const int batch_size,
                                                 const int head_num,
                                                 const int seq_len,
                                                 const unsigned mask) {
  int qk_offset = blockIdx.x * seq_len;
  assert(blockDim.x % 32 == 0);

  float2 stride_max = make_float2(-1e20f, -1e20f);
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float2 cur = phi::funcs::ToFloat2<T>(qk_buf_[threadIdx.x + i + qk_offset] +
                                         bias_qk_[threadIdx.x + i + qk_offset]);
    stride_max.x = max(stride_max.x, cur.x);
    stride_max.y = max(stride_max.y, cur.y);
  }
  float max_val =
      phi::funcs::blockReduceMax<float>(max(stride_max.x, stride_max.y), mask);

  float2 stride_sum = make_float2(0.f, 0.f);
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float2 cur = phi::funcs::ToFloat2<T>(qk_buf_[threadIdx.x + i + qk_offset] +
                                         bias_qk_[threadIdx.x + i + qk_offset]);
    stride_sum.x += __expf(cur.x - max_val);
    stride_sum.y += __expf(cur.y - max_val);
  }

  float sum_val =
      phi::funcs::blockReduceSum<float>(stride_sum.x + stride_sum.y, mask) +
      1e-6f;

  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float2 cur = phi::funcs::ToFloat2<T>(qk_buf_[threadIdx.x + i + qk_offset] +
                                         bias_qk_[threadIdx.x + i + qk_offset]);
    qk_buf_[threadIdx.x + i + qk_offset] = phi::funcs::FloatsToPair<T>(
        __expf(cur.x - max_val) / sum_val, __expf(cur.y - max_val) / sum_val);
  }
}

template <>
__global__ void SoftmaxKernelWithEltaddForLarge2(half2 *qk_buf_,
                                                 const half2 *bias_qk_,
                                                 const int batch_size,
                                                 const int head_num,
                                                 const int seq_len,
                                                 const unsigned mask) {
// operator "+" of half only suppotted after cuda version 10.0
// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#if defined(PADDLE_WITH_CUDA) && \
    (CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__) && CUDA_VERSION >= 10000)

  int qk_offset = blockIdx.x * seq_len;
  assert(blockDim.x % 32 == 0);

  float2 stride_max = make_float2(-1e20f, -1e20f);
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float2 cur =
        phi::funcs::ToFloat2<half2>(qk_buf_[threadIdx.x + i + qk_offset] +
                                    bias_qk_[threadIdx.x + i + qk_offset]);
    stride_max.x = max(stride_max.x, cur.x);
    stride_max.y = max(stride_max.y, cur.y);
  }
  float max_val =
      phi::funcs::blockReduceMax<float>(max(stride_max.x, stride_max.y), mask);

  float2 stride_sum = make_float2(0.f, 0.f);
  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float2 cur =
        phi::funcs::ToFloat2<half2>(qk_buf_[threadIdx.x + i + qk_offset] +
                                    bias_qk_[threadIdx.x + i + qk_offset]);
    stride_sum.x += __expf(cur.x - max_val);
    stride_sum.y += __expf(cur.y - max_val);
  }

  float sum_val =
      phi::funcs::blockReduceSum<float>(stride_sum.x + stride_sum.y, mask) +
      1e-6f;

  for (int i = 0; threadIdx.x + i < seq_len; i += blockDim.x) {
    float2 cur =
        phi::funcs::ToFloat2<half2>(qk_buf_[threadIdx.x + i + qk_offset] +
                                    bias_qk_[threadIdx.x + i + qk_offset]);
    qk_buf_[threadIdx.x + i + qk_offset] = phi::funcs::FloatsToPair<half2>(
        __expf(cur.x - max_val) / sum_val, __expf(cur.y - max_val) / sum_val);
  }
#endif
}

template <typename T>
<<<<<<< HEAD
inline __device__ T ldg(const T *val) {
  return __ldg(val);
}

template <typename T>
inline __device__ T hexp2(T a) {
  return h2exp(a);
}

template <typename T_IN, typename T_OUT>
inline __device__ T_OUT type2type2(T_IN a);

template <>
inline __device__ half2 type2type2(half a) {
  return __half2half2(a);
}

template <typename T>
inline __device__ T float2type2(float a);

template <>
inline __device__ half2 float2type2(float a) {
  return __float2half2_rn(a);
}

template <typename T>
inline __device__ T hmul2(T a, T b) {
  return __hmul2(a, b);
}

template <typename T>
inline __device__ T hsub2(T a, T b) {
  return __hsub2(a, b);
}

template <typename T>
inline __device__ T hadd2(T a, T b) {
  return __hadd2(a, b);
}

template <typename T, int NUM>
__inline__ __device__ T warpReduceSumV2(T *val) {
#pragma unroll
  for (int i = 0; i < NUM; i++) {
#pragma unroll
    for (int mask = 16; mask > 0; mask >>= 1)
      val[i] += __shfl_xor_sync(FINAL_MASK, val[i], mask, 32);
  }
  return (T)(0.0f);
}

template <typename T, int NUM>
__inline__ __device__ T blockReduceSumV2(T *val) {
  static __shared__ T shared[NUM][33];
  int lane = threadIdx.x & 0x1f;
  int wid = threadIdx.x >> 5;

  warpReduceSumV2<T, NUM>(val);

  if (lane == 0) {
#pragma unroll
    for (int i = 0; i < NUM; i++) {
      shared[i][wid] = val[i];
    }
  }

  __syncthreads();

  bool is_mask = threadIdx.x < (blockDim.x / 32.f);
#pragma unroll
  for (int i = 0; i < NUM; i++) {
    val[i] = is_mask ? shared[i][lane] : (T)(0.0f);
  }
  warpReduceSumV2<T, NUM>(val);
  return (T)0.0f;
}

template <typename T, int NUM>
__inline__ __device__ T warpReduceMaxV2(T *val) {
#pragma unroll
  for (int i = 0; i < NUM; i++) {
#pragma unroll
    for (int mask = 16; mask > 0; mask >>= 1)
      val[i] = max(val[i], __shfl_xor_sync(FINAL_MASK, val[i], mask, 32));
  }
  return (T)(0.0f);
}

template <typename T, int NUM>
__inline__ __device__ T blockReduceMaxV2(T *val) {
  static __shared__ T shared[32][NUM];
  int lane = threadIdx.x & 0x1f;  // in-warp idx
  int wid = threadIdx.x >> 5;     // warp idx

  warpReduceMaxV2<T, NUM>(val);  // get maxx in each warp

  if (lane == 0) {
#pragma unroll
    for (int i = 0; i < NUM; i++) {
      shared[wid][i] = val[i];
    }
  }

  __syncthreads();

  // Modify from blockDim.x << 5 to blockDim.x / 32. to prevent
  // blockDim.x is not divided by 32
  bool is_mask = threadIdx.x < (blockDim.x / 32.f);
#pragma unroll
  for (int i = 0; i < NUM; i++) {
    val[i] = is_mask ? shared[lane][i] : (T)-1e20f;
  }
  warpReduceMaxV2<T, NUM>(val);

  return (T)0.0f;
}

template <typename T, int ITEMS_PER_THREAD, int NUM>
__global__ void softmax_kernel_with_mask(T *qk_buf_,
                                         const T *attr_mask,
                                         const int batch_size,
                                         const int head_num,
                                         const int seq_len) {
  using T2 = half2;
  T2 *qk_buf_half2 = reinterpret_cast<T2 *>(qk_buf_);
  const T2 *attr_mask_half2 = (const T2 *)attr_mask;

  for (int seq_id = blockIdx.x; seq_id < seq_len; seq_id += gridDim.x * NUM) {
    T2 data[NUM][ITEMS_PER_THREAD];

    int qk_offset[NUM];

    __shared__ float s_sum[NUM], s_max[NUM];
    float local_max[NUM];
#pragma unroll
    for (int j = 0; j < NUM; j++) {
      local_max[j] = -1e20f;
    }

    for (int i = 0;
         blockDim.x * i + threadIdx.x < (seq_len / 2) && i < ITEMS_PER_THREAD;
         i++) {
      int mask_offset[NUM];
#pragma unroll
      for (int j = 0; j < NUM; j++) {
        qk_offset[j] = ((blockIdx.y * head_num + blockIdx.z) * seq_len +
                        seq_id + j * gridDim.x) *
                           (seq_len / 2) +
                       blockDim.x * i + threadIdx.x;
        mask_offset[j] =
            (blockIdx.y * seq_len + seq_id + j * gridDim.x) * (seq_len / 2) +
            blockDim.x * i + threadIdx.x;
      }

      T2 mask_val[NUM];
#pragma unroll
      for (int j = 0; j < NUM; j++) {
        mask_val[j] = ldg(&attr_mask_half2[mask_offset[j]]);
      }

      T2 qk[NUM];
#pragma unroll
      for (int j = 0; j < NUM; j++) {
        qk[j] = qk_buf_half2[qk_offset[j]];
      }

#pragma unroll
      for (int j = 0; j < NUM; j++) {
        mask_val[j] = hmul2<T2>(hsub2<T2>(float2type2<T2>(1.0f), mask_val[j]),
                                float2type2<T2>(-10000.0f));
      }

#pragma unroll
      for (int j = 0; j < NUM; j++) {
        data[j][i] = hadd2<T2>(qk[j], mask_val[j]);
        local_max[j] = fmax(local_max[j],
                            fmax(static_cast<float>(data[j][i].x),
                                 static_cast<float>(data[j][i].y)));
      }
    }

    if (blockDim.x <= 32) {
      warpReduceMaxV2<float, NUM>(local_max);
    } else {
      blockReduceMaxV2<float, NUM>(local_max);
    }

    if (threadIdx.x == 0) {
#pragma unroll
      for (int j = 0; j < NUM; j++) {
        s_max[j] = local_max[j];
      }
    }
    __syncthreads();

    float local_sum[NUM];
#pragma unroll
    for (int j = 0; j < NUM; j++) {
      local_sum[j] = {0.f};
    }

    for (int i = 0;
         blockDim.x * i + threadIdx.x < (seq_len / 2) && i < ITEMS_PER_THREAD;
         i++) {
#pragma unroll
      for (int j = 0; j < NUM; j++) {
        data[j][i] =
            hexp2<T2>(hsub2<T2>(data[j][i], float2type2<T2>(s_max[j])));
      }

#pragma unroll
      for (int j = 0; j < NUM; j++) {
        local_sum[j] += static_cast<float>(data[j][i].x + data[j][i].y);
      }
    }

    if (blockDim.x <= 32) {
      warpReduceSumV2<float, NUM>(local_sum);
    } else {
      blockReduceSumV2<float, NUM>(local_sum);
    }

    if (threadIdx.x == 0) {
#pragma unroll
      for (int j = 0; j < NUM; j++) {
        s_sum[j] = __fdividef(1.0f, local_sum[j] + 1e-6f);
      }
    }
    __syncthreads();

    for (int i = 0;
         blockDim.x * i + threadIdx.x < (seq_len / 2) && i < ITEMS_PER_THREAD;
         i++) {
#pragma unroll
      for (int j = 0; j < NUM; j++) {
        qk_offset[j] = ((blockIdx.y * head_num + blockIdx.z) * seq_len +
                        seq_id + j * gridDim.x) *
                           (seq_len / 2) +
                       blockDim.x * i + threadIdx.x;
      }

#pragma unroll
      for (int j = 0; j < NUM; j++) {
        qk_buf_half2[qk_offset[j]] =
            hmul2<T2>(data[j][i], float2type2<T2>(s_sum[j]));
      }
    }
  }
}

#define SOFTMAX_KERNEL_WITH_MASK(REPEAT_THREAD)                         \
  do {                                                                  \
    block.x /= REPEAT_THREAD;                                           \
    grid.x /= 4;                                                        \
    constexpr int NUM = 4;                                              \
    softmax_kernel_with_mask<half, REPEAT_THREAD, NUM>                  \
        <<<grid, block, 0, stream>>>(reinterpret_cast<half *>(qk_buf_), \
                                     (const half *)bias_qk,             \
                                     batch_size,                        \
                                     head_num,                          \
                                     seq_len);                          \
  } while (0)

template <typename T>
=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
inline void MatMulWithHeadQK(const phi::GPUContext &context,
                             int head_num,
                             int seq_len,
                             int size_per_head,
                             int batch_size,
                             bool q_trans,
                             bool k_trans,
                             T *q_buf_,
                             T *k_buf_,
                             T *qk_buf_,
                             const T *bias_qk,
<<<<<<< HEAD
                             bool bias_is_mask,
=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                             T alpha,
                             T beta) {
  CBLAS_TRANSPOSE transA = !q_trans ? CblasNoTrans : CblasTrans;
  CBLAS_TRANSPOSE transB = !k_trans ? CblasNoTrans : CblasTrans;

  typedef typename CUDATypeTraits<T>::TYPE run_type;
  auto blas = phi::funcs::GetBlas<phi::GPUContext, run_type>(context);
  auto stream = context.stream();

  blas.BatchedGEMM(transA,
                   transB,
                   seq_len,
                   seq_len,
                   size_per_head,
                   static_cast<run_type>(alpha),
                   reinterpret_cast<run_type *>(q_buf_),
                   reinterpret_cast<run_type *>(k_buf_),
                   static_cast<run_type>(beta),
                   reinterpret_cast<run_type *>(qk_buf_),
                   batch_size * head_num,
                   seq_len * size_per_head,
                   seq_len * size_per_head);

  if (seq_len <= 1024) {
    int grid = batch_size * head_num * seq_len;
    int block = seq_len;

    // Align block to 32, also limit seq_len to max block size.
    if (seq_len % 2 == 0) {
      block = (seq_len <= 64) ? 32 : ((seq_len + 63) / 64) * 32;
      if (std::is_same<T, float>::value) {
        SoftmaxKernelWithEltadd2<float2><<<grid, block, 0, stream>>>(
            reinterpret_cast<float2 *>(qk_buf_),
            reinterpret_cast<const float2 *>(bias_qk),
            batch_size,
            head_num,
            seq_len / 2,
            FINAL_MASK);
      } else {
<<<<<<< HEAD
        if (bias_is_mask) {
#if defined(__HIPCC__) || (defined(__CUDA_ARCH__) && __CUDA_ARCH__ < 700)
          PADDLE_ENFORCE_EQ(bias_is_mask,
                            false,
                            platform::errors::InvalidArgument(
                                "QK_bias is mask can't be supported on rocm or "
                                "cuda_arch<700"));
#else
          dim3 grid(seq_len, batch_size, head_num);
          dim3 block((seq_len / 2 + 31) / 32 * 32);
          SOFTMAX_KERNEL_WITH_MASK(1);
#endif
        } else {
          SoftmaxKernelWithEltadd2<__half2><<<grid, block, 0, stream>>>(
              reinterpret_cast<__half2 *>(qk_buf_),
              reinterpret_cast<const __half2 *>(bias_qk),
              batch_size,
              head_num,
              seq_len / 2,
              FINAL_MASK);
        }
=======
        SoftmaxKernelWithEltadd2<__half2><<<grid, block, 0, stream>>>(
            reinterpret_cast<__half2 *>(qk_buf_),
            reinterpret_cast<const __half2 *>(bias_qk),
            batch_size,
            head_num,
            seq_len / 2,
            FINAL_MASK);
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
      }
    } else {
      block = (seq_len <= 32) ? 32 : ((seq_len + 31) / 32) * 32;
      SoftmaxKernelWithEltadd<T><<<grid, block, 0, stream>>>(
          qk_buf_, bias_qk, batch_size, head_num, seq_len, FINAL_MASK);
    }
  } else {
    int grid = batch_size * head_num * seq_len;
    int block = 512;
    if (seq_len % 2 == 0) {
      if (std::is_same<T, float>::value) {
        SoftmaxKernelWithEltaddForLarge2<float2><<<grid, block, 0, stream>>>(
            reinterpret_cast<float2 *>(qk_buf_),
            reinterpret_cast<const float2 *>(bias_qk),
            batch_size,
            head_num,
            seq_len / 2,
            FINAL_MASK);
      } else {
<<<<<<< HEAD
        if (bias_is_mask) {
#if defined(__HIPCC__) || (defined(__CUDA_ARCH__) && __CUDA_ARCH__ < 700)
          PADDLE_ENFORCE_EQ(bias_is_mask,
                            false,
                            platform::errors::InvalidArgument(
                                "QK_bias is mask can't be supported on rocm or "
                                "cuda_arch<700"));
#else
          dim3 grid(seq_len, batch_size, head_num);
          dim3 block((seq_len / 2 + 31) / 32 * 32);
          if (block.x > 0 && block.x <= 1024) {
            SOFTMAX_KERNEL_WITH_MASK(1);
          } else if (block.x <= 2048) {
            SOFTMAX_KERNEL_WITH_MASK(2);
          } else if (block.x <= 4096) {
            SOFTMAX_KERNEL_WITH_MASK(4);
          } else {
            PADDLE_THROW(platform::errors::InvalidArgument(
                "Cannot support the length of attention > 8192."));
          }
#endif
        } else {
          SoftmaxKernelWithEltaddForLarge2<__half2><<<grid, block, 0, stream>>>(
              reinterpret_cast<__half2 *>(qk_buf_),
              reinterpret_cast<const __half2 *>(bias_qk),
              batch_size,
              head_num,
              seq_len / 2,
              FINAL_MASK);
        }
=======
        SoftmaxKernelWithEltaddForLarge2<__half2><<<grid, block, 0, stream>>>(
            reinterpret_cast<__half2 *>(qk_buf_),
            reinterpret_cast<const __half2 *>(bias_qk),
            batch_size,
            head_num,
            seq_len / 2,
            FINAL_MASK);
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
      }
    } else {
      SoftmaxKernelWithEltaddForLarge<T><<<grid, block, 0, stream>>>(
          qk_buf_, bias_qk, batch_size, head_num, seq_len, FINAL_MASK);
    }
  }
}

template <typename T>
inline void MatMulWithHeadQKV(const phi::GPUContext &context,
                              int head_num,
                              int seq_len,
                              int size_per_head,
                              int batch_size,
                              bool qk_trans,
                              bool v_trans,
                              T *v_buf_,
                              const T *qk_buf_,
                              T *dst,
                              T alpha,
                              T beta) {
  int m = batch_size * seq_len;
  int k = head_num * size_per_head;

  typedef typename CUDATypeTraits<T>::TYPE run_type;
  auto blas = phi::funcs::GetBlas<phi::GPUContext, run_type>(context);
  auto stream = context.stream();
  CBLAS_TRANSPOSE transA = !qk_trans ? CblasNoTrans : CblasTrans;
  CBLAS_TRANSPOSE transB = !v_trans ? CblasNoTrans : CblasTrans;

  blas.BatchedGEMM(transA,
                   transB,
                   seq_len,
                   size_per_head,
                   seq_len,
                   static_cast<run_type>(alpha),
                   reinterpret_cast<const run_type *>(qk_buf_),
                   reinterpret_cast<run_type *>(v_buf_),
                   static_cast<run_type>(beta),
                   reinterpret_cast<run_type *>(dst),
                   batch_size * head_num,
                   seq_len * seq_len,
                   seq_len * size_per_head);
}

template <typename T>
void MultiHeadGPUComputeFunctor<T>::operator()(const phi::GPUContext &dev_ctx,
                                               int batch,
                                               int seq_len,
                                               int head_num,
                                               int head_size,
                                               T *qkptr,
                                               const T *bias_qk_ptr,
<<<<<<< HEAD
                                               bool bias_is_mask,
=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                               T *tptr,
                                               T alpha,
                                               T beta) {
  auto stream = dev_ctx.stream();
  const int tsize = batch * head_num * seq_len * head_size;

  T *qptr = tptr;
  T *kptr = qptr + tsize;
  T *vptr = kptr + tsize;
  // batch gemm stride, softmaxwithscale.
  MatMulWithHeadQK<T>(dev_ctx,
                      head_num,
                      seq_len,
                      head_size,
                      batch,
                      false,
                      true,
                      qptr,
                      kptr,
                      qkptr,
                      bias_qk_ptr,
<<<<<<< HEAD
                      bias_is_mask,
=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                      alpha,
                      beta);
  // batch gemm stride, transpose.
  MatMulWithHeadQKV<T>(dev_ctx,
                       head_num,
                       seq_len,
                       head_size,
                       batch,
                       false,
                       false,
                       vptr,
                       qkptr,
                       tptr,
                       T(1.0),
                       beta);
}

template class MultiHeadGPUComputeFunctor<float>;

// device function 'operator()' is not supportted until cuda 10.0
// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#if defined(PADDLE_WITH_CUDA) && CUDA_VERSION >= 10000
template class MultiHeadGPUComputeFunctor<half>;
#endif

template <typename T, unsigned TPB>
__global__ void SkipLayerNormSmallKernel(int num,
                                         int hidden,
                                         const T *input1,
                                         const T *input2,
                                         T *output,
<<<<<<< HEAD
                                         const T *scale,
                                         const T *bias,
                                         T eps) {
=======
                                         const float *scale,
                                         const float *bias,
                                         float eps) {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
  const T rld = T(1) / T(hidden);
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<T> thread_data(0, 0);
  const int idx = offset + threadIdx.x;
  T val = 0;
  if (threadIdx.x < hidden) {
    val = input1[idx] + input2[idx];
    const T rldval = rld * val;
    thread_data =
        pair_sum(thread_data, phi::funcs::kvp<T>(rldval, rldval * val));
  }
  LayerNormSmall<T, TPB>(
      val, thread_data, hidden, idx, bias, scale, output, eps);
}

// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#ifndef __HIPCC__  // @{ Half kernel: SkipLayerNormSmallKernel
template <>
__global__ void SkipLayerNormSmallKernel<half, 32>(int num,
                                                   int hidden,
                                                   const half *input1,
                                                   const half *input2,
                                                   half *output,
<<<<<<< HEAD
                                                   const half *scale,
                                                   const half *bias,
                                                   half eps) {
=======
                                                   const float *scale,
                                                   const float *bias,
                                                   float eps) {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
  const half rld = half(1) / half(hidden);
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<half> thread_data(0, 0);
  const int idx = offset + threadIdx.x;
  half val = 0;
  if (threadIdx.x < hidden) {
    val = input1[idx] + input2[idx];
    const half rldval = rld * val;
    thread_data =
        pair_sum(thread_data, phi::funcs::kvp<half>(rldval, rldval * val));
  }
  LayerNormSmall<half, 32>(
      val, thread_data, hidden, idx, bias, scale, output, eps);
#endif
}

template <>
__global__ void SkipLayerNormSmallKernel<half, 128>(int num,
                                                    int hidden,
                                                    const half *input1,
                                                    const half *input2,
                                                    half *output,
<<<<<<< HEAD
                                                    const half *scale,
                                                    const half *bias,
                                                    half eps) {
=======
                                                    const float *scale,
                                                    const float *bias,
                                                    float eps) {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
  const half rld = half(1) / half(hidden);
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<half> thread_data(0, 0);
  const int idx = offset + threadIdx.x;
  half val = 0;
  if (threadIdx.x < hidden) {
    val = input1[idx] + input2[idx];
    const half rldval = rld * val;
    thread_data =
        pair_sum(thread_data, phi::funcs::kvp<half>(rldval, rldval * val));
  }
  LayerNormSmall<half, 128>(
      val, thread_data, hidden, idx, bias, scale, output, eps);
#endif
}

template <>
__global__ void SkipLayerNormSmallKernel<half, 384>(int num,
                                                    int hidden,
                                                    const half *input1,
                                                    const half *input2,
                                                    half *output,
<<<<<<< HEAD
                                                    const half *scale,
                                                    const half *bias,
                                                    half eps) {
=======
                                                    const float *scale,
                                                    const float *bias,
                                                    float eps) {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
  const half rld = half(1) / half(hidden);
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<half> thread_data(0, 0);
  const int idx = offset + threadIdx.x;
  half val = 0;
  if (threadIdx.x < hidden) {
    val = input1[idx] + input2[idx];
    const half rldval = rld * val;
    thread_data =
        pair_sum(thread_data, phi::funcs::kvp<half>(rldval, rldval * val));
  }
  LayerNormSmall<half, 384>(
      val, thread_data, hidden, idx, bias, scale, output, eps);
#endif
}
#endif  // @} End Half kernel: SkipLayerNormSmallKernel

template <typename T, unsigned TPB>
__global__ void SkipLayerNormKernel(int num,
                                    int hidden,
                                    const T *input1,
                                    const T *input2,
                                    T *output,
<<<<<<< HEAD
                                    const T *scale,
                                    const T *bias,
                                    T eps) {
=======
                                    const float *scale,
                                    const float *bias,
                                    float eps) {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
  const T rld = T(1) / T(hidden);
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<T> thread_data(0, 0);

  for (int it = threadIdx.x; it < hidden; it += TPB) {
    const int idx = offset + it;
    const T val = input1[idx] + input2[idx];
    const T rldval = rld * val;
    thread_data =
        pair_sum(thread_data, phi::funcs::kvp<T>(rldval, rldval * val));
    output[idx] = val;
  }
  LayerNorm<T, TPB>(thread_data, hidden, offset, bias, scale, output, eps);
}

// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#ifndef __HIPCC__  // @{ Half kernel: SkipLayerNormKernel
template <>
__global__ void SkipLayerNormKernel<half, 256>(int num,
                                               int hidden,
                                               const half *input1,
                                               const half *input2,
                                               half *output,
<<<<<<< HEAD
                                               const half *scale,
                                               const half *bias,
                                               half eps) {
=======
                                               const float *scale,
                                               const float *bias,
                                               float eps) {
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__)
  const half rld = half(1) / half(hidden);
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<half> thread_data(0, 0);

  for (int it = threadIdx.x; it < hidden; it += 256) {
    const int idx = offset + it;
    const half val = input1[idx] + input2[idx];
    const half rldval = rld * val;
    thread_data =
        pair_sum(thread_data, phi::funcs::kvp<half>(rldval, rldval * val));
    output[idx] = val;
  }
  LayerNorm<half, 256>(thread_data, hidden, offset, bias, scale, output, eps);
#endif
}
#endif  // @} End Half kernel: SkipLayerNormKernel

template <typename T, typename T2, unsigned TPB>
__global__ void SkipLayerNormKernel2(int num,
                                     int hidden,
                                     const T2 *input1,
                                     const T2 *input2,
                                     T2 *output,
<<<<<<< HEAD
                                     const T2 *scale,
                                     const T2 *bias,
=======
                                     const float2 *scale,
                                     const float2 *bias,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                     float eps) {
  const T rld = T(0.5f / hidden);  // because hidden is hidden/2
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<T> thread_data(0, 0);

  for (int it = threadIdx.x; it < hidden; it += TPB) {
    const int idx = offset + it;
    const T2 val2 = input1[idx] + input2[idx];
    thread_data = pair_sum(
        thread_data,
        phi::funcs::kvp<T>(rld * (val2.x + val2.y),
                           rld * val2.x * val2.x + rld * val2.y * val2.y));
    output[idx] = val2;
  }
  LayerNorm2<T, T2, TPB>(thread_data, hidden, offset, bias, scale, output, eps);
}

// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#ifndef __HIPCC__  // @{ Half kernel: SkipLayerNormKernel2
template <>
__global__ void SkipLayerNormKernel2<half, half2, 256>(int num,
                                                       int hidden,
                                                       const half2 *input1,
                                                       const half2 *input2,
                                                       half2 *output,
<<<<<<< HEAD
                                                       const half2 *scale,
                                                       const half2 *bias,
=======
                                                       const float2 *scale,
                                                       const float2 *bias,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                                       float eps) {
// operator "+" of half only suppotted after cuda version 10.0
#if CUDA_ARCH_FP16_SUPPORTED(__CUDA_ARCH__) && CUDA_VERSION >= 10000
  const half rld = half(0.5f / hidden);  // because hidden is hidden/2
  const int offset = blockIdx.x * hidden;
  cub::Sum pair_sum;
  phi::funcs::kvp<half> thread_data(0, 0);

  for (int it = threadIdx.x; it < hidden; it += 256) {
    const int idx = offset + it;
    const half2 val2 = input1[idx] + input2[idx];
    thread_data = pair_sum(
        thread_data,
        phi::funcs::kvp<half>(rld * (val2.x + val2.y),
                              rld * val2.x * val2.x + rld * val2.y * val2.y));
    output[idx] = val2;
  }
  LayerNorm2<half, half2, 256>(
      thread_data, hidden, offset, bias, scale, output, eps);
#endif
}
#endif  // @} End Half kernel: SkipLayerNormKernel2

template <typename T>
void SkipLayerNormFunctor<T>::operator()(const int num,
                                         const int hidden,
                                         const T *input1,
                                         const T *input2,
<<<<<<< HEAD
                                         const T *scale,
                                         const T *bias,
                                         T *output,
                                         float eps,
=======
                                         const float *scale,
                                         const float *bias,
                                         T *output,
                                         T eps,
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                                         gpuStream_t stream) {
  int block = num / hidden;
  if (hidden <= 32) {
    const int threads = 32;
    SkipLayerNormSmallKernel<T, threads><<<block, threads, 0, stream>>>(
        num, hidden, input1, input2, output, scale, bias, eps);
  } else if (hidden <= 128) {
    const int threads = 128;
    SkipLayerNormSmallKernel<T, threads><<<block, threads, 0, stream>>>(
        num, hidden, input1, input2, output, scale, bias, eps);
  } else if (hidden == 384) {
    const int threads = 384;
    SkipLayerNormSmallKernel<T, threads><<<block, threads, 0, stream>>>(
        num, hidden, input1, input2, output, scale, bias, eps);
  } else {
    const int threads = 256;
    if (hidden % 2 == 0) {
      if (std::is_same<T, float>::value) {
        SkipLayerNormKernel2<float, float2, threads>
            <<<block, threads, 0, stream>>>(
                num,
                hidden / 2,
                reinterpret_cast<const float2 *>(input1),
                reinterpret_cast<const float2 *>(input2),
                reinterpret_cast<float2 *>(output),
                reinterpret_cast<const float2 *>(scale),
                reinterpret_cast<const float2 *>(bias),
                eps);
// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#ifndef __HIPCC__
      } else if (std::is_same<T, __half>::value) {
        SkipLayerNormKernel2<__half, __half2, threads>
            <<<block, threads, 0, stream>>>(
                num,
                hidden / 2,
                reinterpret_cast<const __half2 *>(input1),
                reinterpret_cast<const __half2 *>(input2),
                reinterpret_cast<__half2 *>(output),
<<<<<<< HEAD
                reinterpret_cast<const __half2 *>(scale),
                reinterpret_cast<const __half2 *>(bias),
=======
                reinterpret_cast<const float2 *>(scale),
                reinterpret_cast<const float2 *>(bias),
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                eps);
#endif
      } else {
        assert(false);
        // should not be here
      }
    } else {
      SkipLayerNormKernel<T, threads><<<block, threads, 0, stream>>>(
          num, hidden, input1, input2, output, scale, bias, eps);
    }
  }
}

template class SkipLayerNormFunctor<float>;

// device function 'operator()' is not supportted until cuda 10.0
// HIP defined __HIP_NO_HALF_CONVERSIONS__ in hip.cmake
#if defined(PADDLE_WITH_CUDA) && CUDA_VERSION >= 10000
template class SkipLayerNormFunctor<half>;
#endif

}  // namespace math
}  // namespace operators
}  // namespace paddle
