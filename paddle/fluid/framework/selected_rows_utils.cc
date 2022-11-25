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

#include "paddle/fluid/framework/selected_rows_utils.h"

#include "paddle/phi/core/serialization.h"

namespace paddle {
namespace framework {

void SerializeToStream(std::ostream& os,
                       const phi::SelectedRows& selected_rows,
                       const platform::DeviceContext& dev_ctx) {
  phi::SerializeToStream(os, selected_rows, dev_ctx);
}

void SerializeToStream(std::ostream& os,
                       const phi::SelectedRows& selected_rows) {
  platform::DeviceContextPool& pool = platform::DeviceContextPool::Instance();
  const platform::DeviceContext* dev_ctx;
  auto place = selected_rows.place();
  dev_ctx = pool.Get(place);
  phi::SerializeToStream(os, selected_rows, *dev_ctx);
}

void DeserializeFromStream(std::istream& is, phi::SelectedRows* selected_rows) {
  platform::DeviceContextPool& pool = platform::DeviceContextPool::Instance();
  const platform::DeviceContext* dev_ctx;
  dev_ctx = pool.Get(platform::CPUPlace());
  phi::DeserializeFromStream(is, selected_rows, *dev_ctx);
}

void DeserializeFromStream(std::istream& is,
                           phi::SelectedRows* selected_rows,
                           const platform::DeviceContext& dev_ctx) {
<<<<<<< HEAD
  phi::DeserializeFromStream(is, selected_rows, dev_ctx);
=======
  {
    // the 1st field, unit32_t version for SelectedRows
    uint32_t version;
    is.read(reinterpret_cast<char*>(&version), sizeof(version));
    PADDLE_ENFORCE_EQ(version,
                      0U,
                      platform::errors::InvalidArgument(
                          "Only version 0 SelectedRows is supported."));
  }
  {
    // the 2st field, rows information
    uint64_t size;
    is.read(reinterpret_cast<char*>(&size), sizeof(size));
    auto& rows = *selected_rows->mutable_rows();
    rows.resize(size);
    for (uint64_t i = 0; i < size; ++i) {
      is.read(reinterpret_cast<char*>(&rows[i]), sizeof(int64_t));
    }
  }
  {
    // the 3st field, the height of the SelectedRows
    int64_t height;
    is.read(reinterpret_cast<char*>(&height), sizeof(int64_t));
    selected_rows->set_height(height);
  }
  // the 4st field, tensor which contains the data
  TensorFromStream(is, selected_rows->mutable_value(), dev_ctx);
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
}

}  // namespace framework
}  // namespace paddle
