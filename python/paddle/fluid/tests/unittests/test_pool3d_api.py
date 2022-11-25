#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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
import unittest
import numpy as np
import paddle.fluid as fluid
import paddle.fluid.core as core
from paddle.fluid.framework import _test_eager_guard
from paddle.nn.functional import avg_pool3d, max_pool3d
from paddle.fluid.framework import _test_eager_guard
from test_pool3d_op import (
    avg_pool3D_forward_naive,
    max_pool3D_forward_naive,
    pool3D_forward_naive,
)


class TestPool3D_API(unittest.TestCase):

    def setUp(self):
        np.random.seed(123)
        self.places = [fluid.CPUPlace()]
        if core.is_compiled_with_cuda():
            self.places.append(fluid.CUDAPlace(0))

    def check_avg_static_results(self, place):
        with fluid.program_guard(fluid.Program(), fluid.Program()):
<<<<<<< HEAD
            input = fluid.data(
                name="input", shape=[2, 3, 32, 32, 32], dtype="float32"
            )
            result = avg_pool3d(input, kernel_size=2, stride=2, padding=0)

            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='avg',
            )
=======
            input = fluid.data(name="input",
                               shape=[2, 3, 32, 32, 32],
                               dtype="float32")
            result = avg_pool3d(input, kernel_size=2, stride=2, padding=0)

            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='avg')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            exe = fluid.Executor(place)
            fetches = exe.run(
                fluid.default_main_program(),
                feed={"input": input_np},
                fetch_list=[result],
            )
            np.testing.assert_allclose(fetches[0], result_np, rtol=1e-05)

    def check_avg_dygraph_results(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
            result = avg_pool3d(input, kernel_size=2, stride=2, padding="SAME")

<<<<<<< HEAD
            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='avg',
                padding_algorithm="SAME",
            )
=======
            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='avg',
                                             padding_algorithm="SAME")
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

<<<<<<< HEAD
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(
                kernel_size=2, stride=None, padding="SAME"
            )
=======
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(kernel_size=2,
                                                      stride=None,
                                                      padding="SAME")
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = avg_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_avg_dygraph_padding_results(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
<<<<<<< HEAD
            result = avg_pool3d(
                input,
                kernel_size=2,
                stride=2,
                padding=1,
                ceil_mode=False,
                exclusive=True,
            )

            result_np = avg_pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[1, 1, 1],
                ceil_mode=False,
                exclusive=False,
            )
=======
            result = avg_pool3d(input,
                                kernel_size=2,
                                stride=2,
                                padding=1,
                                ceil_mode=False,
                                exclusive=True)

            result_np = avg_pool3D_forward_naive(input_np,
                                                 ksize=[2, 2, 2],
                                                 strides=[2, 2, 2],
                                                 paddings=[1, 1, 1],
                                                 ceil_mode=False,
                                                 exclusive=False)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

<<<<<<< HEAD
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(
                kernel_size=2,
                stride=None,
                padding=1,
                ceil_mode=False,
                exclusive=True,
            )
=======
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(kernel_size=2,
                                                      stride=None,
                                                      padding=1,
                                                      ceil_mode=False,
                                                      exclusive=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = avg_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_avg_dygraph_ceilmode_results(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
<<<<<<< HEAD
            result = avg_pool3d(
                input, kernel_size=2, stride=2, padding=0, ceil_mode=True
            )

            result_np = avg_pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                ceil_mode=True,
            )
=======
            result = avg_pool3d(input,
                                kernel_size=2,
                                stride=2,
                                padding=0,
                                ceil_mode=True)

            result_np = avg_pool3D_forward_naive(input_np,
                                                 ksize=[2, 2, 2],
                                                 strides=[2, 2, 2],
                                                 paddings=[0, 0, 0],
                                                 ceil_mode=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

<<<<<<< HEAD
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(
                kernel_size=2, stride=None, padding=0, ceil_mode=True
            )
=======
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(kernel_size=2,
                                                      stride=None,
                                                      padding=0,
                                                      ceil_mode=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = avg_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_max_static_results(self, place):
        with fluid.program_guard(fluid.Program(), fluid.Program()):
<<<<<<< HEAD
            input = fluid.data(
                name="input", shape=[2, 3, 32, 32, 32], dtype="float32"
            )
            result = max_pool3d(input, kernel_size=2, stride=2, padding=0)

            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='max',
            )
=======
            input = fluid.data(name="input",
                               shape=[2, 3, 32, 32, 32],
                               dtype="float32")
            result = max_pool3d(input, kernel_size=2, stride=2, padding=0)

            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='max')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            exe = fluid.Executor(place)
            fetches = exe.run(
                fluid.default_main_program(),
                feed={"input": input_np},
                fetch_list=[result],
            )
            np.testing.assert_allclose(fetches[0], result_np, rtol=1e-05)

    def check_max_dygraph_results(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
            result = max_pool3d(input, kernel_size=2, stride=2, padding=0)

<<<<<<< HEAD
            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='max',
            )

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(
                kernel_size=2, stride=None, padding=0
            )
=======
            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='max')

            self.assertTrue(np.allclose(result.numpy(), result_np))
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(kernel_size=2,
                                                      stride=None,
                                                      padding=0)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = max_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_max_dygraph_ndhwc_results(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(
<<<<<<< HEAD
                np.transpose(input_np, [0, 2, 3, 4, 1])
            )
            result = max_pool3d(
                input,
                kernel_size=2,
                stride=2,
                padding=0,
                data_format="NDHWC",
                return_mask=False,
            )

            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='max',
            )

            np.testing.assert_allclose(
                np.transpose(result.numpy(), [0, 4, 1, 2, 3]),
                result_np,
                rtol=1e-05,
            )
=======
                np.transpose(input_np, [0, 2, 3, 4, 1]))
            result = max_pool3d(input,
                                kernel_size=2,
                                stride=2,
                                padding=0,
                                data_format="NDHWC",
                                return_mask=False)

            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='max')

            self.assertTrue(
                np.allclose(np.transpose(result.numpy(), [0, 4, 1, 2, 3]),
                            result_np))
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

    def check_max_dygraph_ceilmode_results(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
<<<<<<< HEAD
            result = max_pool3d(
                input, kernel_size=2, stride=2, padding=0, ceil_mode=True
            )

            result_np = max_pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                ceil_mode=True,
            )
=======
            result = max_pool3d(input,
                                kernel_size=2,
                                stride=2,
                                padding=0,
                                ceil_mode=True)

            result_np = max_pool3D_forward_naive(input_np,
                                                 ksize=[2, 2, 2],
                                                 strides=[2, 2, 2],
                                                 paddings=[0, 0, 0],
                                                 ceil_mode=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

<<<<<<< HEAD
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(
                kernel_size=2, stride=None, padding=0, ceil_mode=True
            )
=======
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(kernel_size=2,
                                                      stride=None,
                                                      padding=0,
                                                      ceil_mode=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = max_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_max_dygraph_padding_results(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
<<<<<<< HEAD
            result = max_pool3d(
                input, kernel_size=2, stride=2, padding=1, ceil_mode=False
            )

            result_np = max_pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[1, 1, 1],
                ceil_mode=False,
            )
=======
            result = max_pool3d(input,
                                kernel_size=2,
                                stride=2,
                                padding=1,
                                ceil_mode=False)

            result_np = max_pool3D_forward_naive(input_np,
                                                 ksize=[2, 2, 2],
                                                 strides=[2, 2, 2],
                                                 paddings=[1, 1, 1],
                                                 ceil_mode=False)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

<<<<<<< HEAD
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(
                kernel_size=2, stride=None, padding=1, ceil_mode=False
            )
=======
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(kernel_size=2,
                                                      stride=None,
                                                      padding=1,
                                                      ceil_mode=False)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = max_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_max_dygraph_stride_is_none(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
<<<<<<< HEAD
            result, indices = max_pool3d(
                input,
                kernel_size=2,
                stride=None,
                padding="SAME",
                return_mask=True,
            )

            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='max',
                padding_algorithm="SAME",
            )

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(
                kernel_size=2, stride=2, padding=0
            )
=======
            result, indices = max_pool3d(input,
                                         kernel_size=2,
                                         stride=None,
                                         padding="SAME",
                                         return_mask=True)

            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='max',
                                             padding_algorithm="SAME")

            self.assertTrue(np.allclose(result.numpy(), result_np))
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(kernel_size=2,
                                                      stride=2,
                                                      padding=0)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = max_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_max_dygraph_padding(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
            padding = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
            result = max_pool3d(input, kernel_size=2, stride=2, padding=padding)

<<<<<<< HEAD
            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='max',
            )

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(
                kernel_size=2, stride=2, padding=0
            )
=======
            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='max')

            self.assertTrue(np.allclose(result.numpy(), result_np))
            max_pool3d_dg = paddle.nn.layer.MaxPool3D(kernel_size=2,
                                                      stride=2,
                                                      padding=0)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = max_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

            padding = [0, 0, 0, 0, 0, 0]
            result = max_pool3d(input, kernel_size=2, stride=2, padding=padding)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

    def check_avg_divisor(self, place):
        with fluid.dygraph.guard(place):
            input_np = np.random.random([2, 3, 32, 32, 32]).astype("float32")
            input = fluid.dygraph.to_variable(input_np)
            padding = 0
<<<<<<< HEAD
            result = avg_pool3d(
                input,
                kernel_size=2,
                stride=2,
                padding=padding,
                divisor_override=8,
            )

            result_np = pool3D_forward_naive(
                input_np,
                ksize=[2, 2, 2],
                strides=[2, 2, 2],
                paddings=[0, 0, 0],
                pool_type='avg',
            )

            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(
                kernel_size=2, stride=2, padding=0
            )
=======
            result = avg_pool3d(input,
                                kernel_size=2,
                                stride=2,
                                padding=padding,
                                divisor_override=8)

            result_np = pool3D_forward_naive(input_np,
                                             ksize=[2, 2, 2],
                                             strides=[2, 2, 2],
                                             paddings=[0, 0, 0],
                                             pool_type='avg')

            self.assertTrue(np.allclose(result.numpy(), result_np))
            avg_pool3d_dg = paddle.nn.layer.AvgPool3D(kernel_size=2,
                                                      stride=2,
                                                      padding=0)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            result = avg_pool3d_dg(input)
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)

            padding = [0, 0, 0, 0, 0, 0]
<<<<<<< HEAD
            result = avg_pool3d(
                input,
                kernel_size=2,
                stride=2,
                padding=padding,
                divisor_override=8,
            )
            np.testing.assert_allclose(result.numpy(), result_np, rtol=1e-05)
=======
            result = avg_pool3d(input,
                                kernel_size=2,
                                stride=2,
                                padding=padding,
                                divisor_override=8)
            self.assertTrue(np.allclose(result.numpy(), result_np))
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

    def test_pool3d(self):
        for place in self.places:

            self.check_max_dygraph_results(place)
            self.check_avg_dygraph_results(place)
            self.check_max_static_results(place)
            self.check_avg_static_results(place)
            self.check_max_dygraph_stride_is_none(place)
            self.check_max_dygraph_padding(place)
            self.check_avg_divisor(place)
            self.check_max_dygraph_ndhwc_results(place)
            self.check_max_dygraph_ceilmode_results(place)

    def test_dygraph_api(self):
        with _test_eager_guard():
            self.test_pool3d()


class TestPool3DError_API(unittest.TestCase):

    def test_error_api(self):

        def run1():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                padding = [[0, 1], [0, 0], [0, 0], [0, 0], [0, 0]]
                res_pd = avg_pool3d(
                    input_pd, kernel_size=2, stride=2, padding=padding
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                padding = [[0, 1], [0, 0], [0, 0], [0, 0], [0, 0]]
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding=padding)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run1)

        def run2():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                padding = [[0, 1], [0, 0], [0, 0], [0, 0], [0, 0]]
                res_pd = avg_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding=padding,
                    data_format='NCDHW',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                padding = [[0, 1], [0, 0], [0, 0], [0, 0], [0, 0]]
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding=padding,
                                    data_format='NCDHW')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run2)

        def run3():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                padding = [[0, 1], [0, 0], [0, 0], [0, 0], [0, 0]]
                res_pd = avg_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding=padding,
                    data_format='NDHWC',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                padding = [[0, 1], [0, 0], [0, 0], [0, 0], [0, 0]]
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding=padding,
                                    data_format='NDHWC')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run3)

        def run4():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding=0,
                    data_format='NNNN',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding=0,
                                    data_format='NNNN')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run4)

        def run5():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding=0,
                    data_format='NNNN',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding=0,
                                    data_format='NNNN')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run5)

        def run6():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding="padding",
                    data_format='NNNN',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding="padding",
                                    data_format='NNNN')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run6)

        def run7():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding="padding",
                    data_format='NNNN',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding="padding",
                                    data_format='NNNN')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run7)

        def run8():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding="VALID",
                    ceil_mode=True,
                    data_format='NNNN',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding="VALID",
                                    ceil_mode=True,
                                    data_format='NNNN')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run8)

        def run9():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding="VALID",
                    ceil_mode=True,
                    data_format='NNNN',
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding="VALID",
                                    ceil_mode=True,
                                    data_format='NNNN')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run9)

        def run10():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=2,
                    padding=0,
                    data_format='NDHWC',
                    return_mask=True,
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = max_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=2,
                                    padding=0,
                                    data_format='NDHWC',
                                    return_mask=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run10)

        def run_kernel_out_of_range():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(
                    input_pd,
                    kernel_size=-1,
                    stride=2,
                    padding="VALID",
                    ceil_mode=True,
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=-1,
                                    stride=2,
                                    padding="VALID",
                                    ceil_mode=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run_kernel_out_of_range)

        def run_size_out_of_range():
            with fluid.dygraph.guard():
                input_np = np.random.uniform(-1, 1, [2, 3, 32, 32, 32]).astype(
<<<<<<< HEAD
                    np.float32
                )
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(
                    input_pd,
                    kernel_size=2,
                    stride=0,
                    padding="VALID",
                    ceil_mode=True,
                )
=======
                    np.float32)
                input_pd = fluid.dygraph.to_variable(input_np)
                res_pd = avg_pool3d(input_pd,
                                    kernel_size=2,
                                    stride=0,
                                    padding="VALID",
                                    ceil_mode=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        self.assertRaises(ValueError, run_size_out_of_range)

    def test_dygraph_api(self):
        with _test_eager_guard():
            self.test_error_api()


if __name__ == '__main__':
    unittest.main()
