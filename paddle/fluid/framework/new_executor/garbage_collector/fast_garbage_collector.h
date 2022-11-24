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
#pragma once

#include "paddle/fluid/framework/new_executor/garbage_collector/garbage_collector.h"

namespace paddle {
namespace framework {

class InterpreterCoreFastGarbageCollector
    : public InterpreterCoreGarbageCollector {
 public:
<<<<<<< HEAD
  void Add(Variable* var) override;
  void Add(Variable* var,
           platform::DeviceEvent* event,
           const platform::DeviceContext* ctx) override;
=======
  void Add(Variable* var, const Instruction& instr) override;
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

 private:
  void Add(Variable* var);
  void Add(Garbage garbage);
};
}  // namespace framework
}  // namespace paddle
