#  Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
import paddle
import paddle.nn.functional as F
import paddle.static
from paddle.fluid.tests.unittests.ipu.op_test_ipu import IPUOpTest


class TestBase(IPUOpTest):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def setUp(self):
        self.set_atol()
        self.set_training()
        self.set_data_feed()
        self.set_feed_attr()
        self.set_op_attrs()

    def set_data_feed(self):
        data = np.random.uniform(size=[1, 3, 10, 10])
        self.feed_fp32 = {'x': data.astype(np.float32)}
        self.feed_fp16 = {'x': data.astype(np.float16)}
        self.feed_list = list(self.feed_fp32.keys())

    def set_feed_attr(self):
        self.feed_shape = [x.shape for x in self.feed_fp32.values()]
        self.feed_list = list(self.feed_fp32.keys())
        self.feed_dtype = [x.dtype for x in self.feed_fp32.values()]

    def set_op_attrs(self):
        self.attrs = {}

    @IPUOpTest.static_graph
    def build_model(self):
<<<<<<< HEAD
        x = paddle.static.data(name=self.feed_list[0],
                               shape=self.feed_shape[0],
                               dtype='float32')
=======
        x = paddle.static.data(
            name=self.feed_list[0], shape=self.feed_shape[0], dtype='float32'
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        array = np.random.uniform(size=[1]).astype(np.float32)
        result1 = paddle.zeros(shape=[1], dtype='float32')
        weight = paddle.assign(array, result1)
        out = F.prelu(x, weight=weight, **self.attrs)
        self.fetch_list = [out.name]

    def run_model(self, exec_mode):
        ipu_strategy = paddle.static.IpuStrategy()
        ipu_strategy.set_graph_config(is_training=self.is_training)
        self.run_op_test(exec_mode, ipu_strategy=ipu_strategy)

    def test(self):
        for m in IPUOpTest.ExecutionMode:
            if not self.skip_mode(m):
                self.build_model()
                self.run_model(m)
        self.check()


class TestCase1(TestBase):
<<<<<<< HEAD

    @IPUOpTest.static_graph
    def build_model(self):
        x = paddle.static.data(name=self.feed_list[0],
                               shape=self.feed_shape[0],
                               dtype='float32')
=======
    @IPUOpTest.static_graph
    def build_model(self):
        x = paddle.static.data(
            name=self.feed_list[0], shape=self.feed_shape[0], dtype='float32'
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        array = np.random.uniform(size=[3]).astype(np.float32)
        result1 = paddle.zeros(shape=[3], dtype='float32')
        weight = paddle.assign(array, result1)
        out = F.prelu(x, weight=weight, **self.attrs)
        self.fetch_list = [out.name]


if __name__ == "__main__":
    unittest.main()
