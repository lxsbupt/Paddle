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
<<<<<<< HEAD

=======
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
import paddle
import paddle.static
from paddle.fluid.tests.unittests.ipu.op_test_ipu import IPUOpTest


class TestBase(IPUOpTest):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def setUp(self):
        self.set_atol()
        self.set_training()
        self.set_feed()
        self.set_op_attrs()

    def set_op_attrs(self):
        self.attrs = {}

    def set_feed(self):
        data = np.random.uniform(size=[32, 100])
        self.feed_fp32 = {'x': data.astype(np.float32)}
        self.feed_fp16 = {'x': data.astype(np.float16)}
        self.feed_shape = [x.shape for x in self.feed_fp32.values()]
        self.feed_list = list(self.feed_fp32.keys())

    @IPUOpTest.static_graph
    def build_model(self):
<<<<<<< HEAD
        x = paddle.static.data(
            name=self.feed_list[0], shape=self.feed_shape[0], dtype='float32'
        )
=======
        x = paddle.static.data(name=self.feed_list[0],
                               shape=self.feed_shape[0],
                               dtype='float32')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        x = paddle.static.nn.data_norm(input=x, **self.attrs)
        self.fetch_list = [x.name]

    def run_model(self, exec_mode):
        self.run_op_test(exec_mode)

    def test(self):
        for m in IPUOpTest.ExecutionMode:
            if not self.skip_mode(m):
                self.build_model()
                self.run_model(m)
        self.check()


class TestCase1(TestBase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def set_op_attrs(self):
        self.attrs = {"in_place": True}

    @IPUOpTest.static_graph
    def build_model(self):
<<<<<<< HEAD
        x = paddle.static.data(
            name=self.feed_list[0], shape=self.feed_shape[0], dtype='float32'
        )
=======
        x = paddle.static.data(name=self.feed_list[0],
                               shape=self.feed_shape[0],
                               dtype='float32')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        x = paddle.static.nn.data_norm(input=x, **self.attrs)
        x = x + 1
        self.fetch_list = [x.name]


@unittest.skip("Do not support in_place=True when test single data_norm Op")
class TestCase2(TestBase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def set_op_attrs(self):
        self.attrs = {"in_place": True}


class TestCase3(TestBase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def set_op_attrs(self):
        self.attrs = {"data_layout": "NHWC"}


class TestCase4(TestBase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def set_op_attrs(self):
        self.attrs = {"epsilon": 0.001}


class TestCase5(TestBase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def set_op_attrs(self):
        self.attrs = {"do_model_average_for_mean_and_var": True}


class TestCase6(TestBase):
    # If enable_scale_and_shift=True, it requires to set values of scale and bias in `param_attr`
    def set_op_attrs(self):
        self.attrs = {
<<<<<<< HEAD
            "param_attr": {"scale_w": 0.5, "bias": 0.1},
            "enable_scale_and_shift": True,
=======
            "param_attr": {
                "scale_w": 0.5,
                "bias": 0.1
            },
            "enable_scale_and_shift": True
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        }


class TestCase7(TestBase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def set_op_attrs(self):
        self.attrs = {
            "param_attr": {
                "batch_size": 1e3,
                "batch_sum": 0.1,
                "batch_square": 1e3,
                "scale_w": 0.5,
<<<<<<< HEAD
                "bias": 0.1,
            },
            "enable_scale_and_shift": True,
=======
                "bias": 0.1
            },
            "enable_scale_and_shift": True
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        }


if __name__ == "__main__":
    unittest.main()
