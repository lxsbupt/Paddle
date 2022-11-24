/* Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */
#pragma once
#ifndef _WIN32
<<<<<<< HEAD
#include <cuda.h>
#include <nvToolsExt.h>

#include <mutex>  // NOLINT

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
#include "paddle/phi/backends/dynload/nvtx.h"

namespace paddle {
namespace platform {
namespace dynload {

#define PLATFORM_DECLARE_DYNAMIC_LOAD_NVTX_WRAP(__name)      \
  using DynLoad__##__name = phi::dynload::DynLoad__##__name; \
  extern DynLoad__##__name __name

#define PLATFORM_NVTX_ROUTINE_EACH(__macro) \
  __macro(nvtxRangePushA);                  \
  __macro(nvtxRangePushEx);                 \
  __macro(nvtxRangePop);

PLATFORM_NVTX_ROUTINE_EACH(PLATFORM_DECLARE_DYNAMIC_LOAD_NVTX_WRAP);

#undef PLATFORM_DECLARE_DYNAMIC_LOAD_NVTX_WRAP
}  // namespace dynload
}  // namespace platform
}  // namespace paddle
#endif
