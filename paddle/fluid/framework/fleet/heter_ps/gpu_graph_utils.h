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
#include <algorithm>
#include <vector>
#include <random>
#include <time.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <stdio.h>
#include "paddle/fluid/platform/enforce.h"

namespace paddle {
namespace framework {

/**
 * @brief wrapper of the std::default_random_engine each construction will have different seeds.
 */
struct random_engine_wrapper_t {
    std::default_random_engine engine;
    random_engine_wrapper_t() {
        timespec tp;
        clock_gettime(CLOCK_REALTIME, &tp);
        static std::atomic<unsigned long> x(static_cast<unsigned long>(1));
        std::seed_seq sseq = {x++, x++, x++,
            (unsigned long)(tp.tv_sec * 1e9 + tp.tv_nsec)};
        engine.seed(sseq);
    }
};

/**
 * @brief Get a n-size vector<int>, but its element has unique shuffled int value (from 0 to n-1).
 * @param n vector size
 * @return the shuffled vector.
 */
inline std::vector<int> shuffle_int_vector(int n) {
    random_engine_wrapper_t random_engine_wrapper;
    std::vector<int> ret(n);
    int i = 0;

    for (auto & e : ret) {
        e = i++;
    }
    std::shuffle(ret.begin(), ret.end(), random_engine_wrapper.engine);
    return std::move(ret);
}

#define CUDA_CHECK(cmd)                                                       \
  do {                                                                        \
    cudaError_t e = cmd;                                                      \
    CHECK(e == cudaSuccess) << "Cuda failure " << __FILE__ << ":" << __LINE__ \
                            << " " << cudaGetErrorString(e) << std::endl;     \
  } while (0)

class CudaDeviceRestorer {
 public:
  CudaDeviceRestorer() { cudaGetDevice(&dev_); }
  ~CudaDeviceRestorer() { cudaSetDevice(dev_); }

 private:
  int dev_;
};

inline void debug_gpu_memory_info(int gpu_id, const char* desc) {
  CudaDeviceRestorer r;

  size_t avail{0};
  size_t total{0};
  cudaSetDevice(gpu_id);
  auto err = cudaMemGetInfo(&avail, &total);
  PADDLE_ENFORCE_EQ(
      err,
      cudaSuccess,
      platform::errors::InvalidArgument("cudaMemGetInfo failed!"));
  VLOG(0) << "updatex gpu memory on device " << gpu_id << ", "
          << "avail=" << avail / 1024.0 / 1024.0 / 1024.0 << "g, "
          << "total=" << total / 1024.0 / 1024.0 / 1024.0 << "g, "
          << "use_rate=" << (total - avail) / double(total) << "%, "
          << "desc=" << desc;
}

inline void debug_gpu_memory_info(const char* desc) {
  CudaDeviceRestorer r;

  int device_num = 0;
  auto err = cudaGetDeviceCount(&device_num);
  PADDLE_ENFORCE_EQ(
      err,
      cudaSuccess,
      platform::errors::InvalidArgument("cudaGetDeviceCount failed!"));

  size_t avail{0};
  size_t total{0};
  for (int i = 0; i < device_num; ++i) {
    cudaSetDevice(i);
    auto err = cudaMemGetInfo(&avail, &total);
    PADDLE_ENFORCE_EQ(
        err,
        cudaSuccess,
        platform::errors::InvalidArgument("cudaMemGetInfo failed!"));
    VLOG(0) << "update gpu memory on device " << i << ", "
            << "avail=" << avail / 1024.0 / 1024.0 / 1024.0 << "g, "
            << "total=" << total / 1024.0 / 1024.0 / 1024.0 << "g, "
            << "use_rate=" << (total - avail) / double(total) << "%, "
            << "desc=" << desc;
  }
}

};  // namespace framework
};  // namespace paddle
