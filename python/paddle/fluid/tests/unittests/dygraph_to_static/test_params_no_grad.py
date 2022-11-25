# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import paddle
import paddle.nn as nn
import paddle.distributed as dist

import unittest


class Net(nn.Layer):
<<<<<<< HEAD
    def __init__(self):
        super().__init__()
=======

    def __init__(self):
        super(Net, self).__init__()
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        self.emb1 = nn.Embedding(100, 16)
        self.emb2 = nn.Embedding(100, 16)

    def forward(self, ids):
        feat1 = self.emb1(ids)
        feat1.stop_gradient = True  # here

        feat2 = self.emb2(ids)

        out = feat1 + feat2
        out = paddle.mean(out)
        return out


def train():
    paddle.distributed.init_parallel_env()
    net = Net()
    net = paddle.jit.to_static(net)

    sgd = paddle.optimizer.SGD(learning_rate=0.1, parameters=net.parameters())
    dp_net = paddle.DataParallel(net)
    for i in range(4):
        x = paddle.randint(low=0, high=100, shape=[4, 10])
        loss = dp_net(x)
        loss.backward()
        sgd.step()
        loss.clear_gradient()
        print(loss)


class TestParamsNoGrad(unittest.TestCase):
<<<<<<< HEAD
    def test_two_card(self):
        if (
            paddle.is_compiled_with_cuda()
            and len(paddle.static.cuda_places()) > 1
        ):
=======

    def test_two_card(self):
        if paddle.is_compiled_with_cuda() and len(
                paddle.static.cuda_places()) > 1:
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            dist.spawn(train, nprocs=2, gpus='0,1')


if __name__ == '__main__':
    unittest.main()
