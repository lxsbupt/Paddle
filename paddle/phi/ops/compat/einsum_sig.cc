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

#include "paddle/phi/core/compat/op_utils.h"

namespace phi {

KernelSignature EinsumOpArgumentMapping(const ArgumentMappingContext& ctx) {
<<<<<<< HEAD
  return KernelSignature("einsum_raw",
                         {"Operands"},
                         {"equation"},
                         {"Out", "InnerCache", "XShape"});
=======
  if (ctx.OutputSize("XShape") > 0 && ctx.OutputSize("InnerCache") > 0) {
    return KernelSignature("einsum_raw",
                           {"Operands"},
                           {"equation"},
                           {"Out", "InnerCache", "XShape"});
  } else {
    return KernelSignature("einsum", {"Operands"}, {"equation"}, {"Out"});
  }
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
}

KernelSignature EinsumGradOpArgumentMapping(const ArgumentMappingContext& ctx) {
  return KernelSignature("einsum_grad",
                         {"Operands", "InnerCache", "Out@GRAD"},
                         {"equation"},
                         {"Operands@GRAD"});
}
}  // namespace phi

PD_REGISTER_ARG_MAPPING_FN(einsum, phi::EinsumOpArgumentMapping);
PD_REGISTER_ARG_MAPPING_FN(einsum_grad, phi::EinsumGradOpArgumentMapping);
