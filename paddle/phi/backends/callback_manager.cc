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

#include "paddle/phi/backends/callback_manager.h"

#include <ThreadPool.h>

#include "paddle/fluid/platform/device/device_wrapper.h"
<<<<<<< HEAD
#include "paddle/fluid/platform/enforce.h"
#include "paddle/phi/backends/device_guard.h"
=======
#include "paddle/phi/backends/device_guard.h"
#include "paddle/phi/core/enforce.h"
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

namespace phi {

CallbackManager::CallbackManager(stream::Stream *stream)
    : stream_(stream), thread_pool_(new ::ThreadPool(1)) {}

void CallbackManager::AddCallback(std::function<void()> callback) const {
  auto *callback_func = new std::function<void()>(std::move(callback));
  auto *func = new std::function<void()>([this, callback_func] {
    std::lock_guard<std::mutex> lock(mtx_);
    last_future_ = thread_pool_->enqueue([callback_func] {
      std::unique_ptr<std::function<void()>> releaser(callback_func);
      (*callback_func)();
    });
  });
  phi::DeviceGuard guard(stream_->GetPlace());
  phi::DeviceManager::GetDeviceWithPlace(stream_->GetPlace())
      ->AddCallback(stream_, func);
}

void CallbackManager::Wait() const {
  phi::DeviceGuard guard(stream_->GetPlace());
  phi::DeviceManager::GetDeviceWithPlace(stream_->GetPlace())
      ->SynchronizeStream(stream_);

  {
    std::lock_guard<std::mutex> lock(mtx_);
    if (last_future_.valid()) {
      last_future_.wait();
    }
  }
}

}  // namespace phi
