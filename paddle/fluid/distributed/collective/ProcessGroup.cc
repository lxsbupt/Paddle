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

#include "paddle/fluid/distributed/collective/ProcessGroup.h"

namespace paddle {
namespace distributed {

ProcessGroup::Task::Task(int rank, CommType comm_type, bool sync_op)
    : rank_(rank), comm_type_(comm_type), sync_op_(sync_op) {}

ProcessGroup::Task::~Task() = default;

bool ProcessGroup::Task::IsCompleted() {
  std::lock_guard<std::mutex> lock(mutex_);
  return is_completed_;
}

bool ProcessGroup::Task::Wait(std::chrono::milliseconds timeout) {
  return false;
}

void ProcessGroup::Task::Synchronize() {}

<<<<<<< HEAD
ProcessGroup::ProcessGroup(int rank,
                           int size,
                           const platform::Place& place,
                           int gid)
    : rank_(rank), size_(size), place_(place), gid_(gid) {
=======
void ProcessGroup::Task::UpdateWaitChain(const phi::DeviceContext& ctx) {}

ProcessGroup::ProcessGroup(int rank, int size, int gid)
    : rank_(rank), size_(size), gid_(gid) {
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
  if (gid != IGNORE_ID) {
    auto map = ProcessGroupMapFromGid::getInstance();
    map->insert(gid_, this);
  }
}

// TODO(sunyilun): methods below will be removed later
ProcessGroup::Task::Task(int rank,
                         const std::vector<phi::DenseTensor>& inputs,
                         CommType comm_type)
    : rank_(rank), comm_type_(comm_type) {}

ProcessGroup::Task::Task(int rank,
                         const std::vector<phi::DenseTensor>& inputs,
                         CommType comm_type,
                         bool sync_op)
    : rank_(rank), comm_type_(comm_type), sync_op_(sync_op) {}

ProcessGroupIdMap& ProcessGroupIdMap::GetInstance() {
  static ProcessGroupIdMap instance;
  return instance;
}

}  //  namespace distributed
}  //  namespace paddle
