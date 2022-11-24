#   Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
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

import unittest
import numpy as np

import paddle.fluid as fluid
import paddle.fluid.layers as layers
import paddle.fluid.core as core
import gradient_checker
import paddle

from decorator_helper import prog_scope


class TestInstanceNormDoubleGradCheck(unittest.TestCase):

    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed()
            shape = [2, 3, 4, 5]
            dtype = "float32"
            eps = 0.005
            atol = 1e-4
            x = layers.create_parameter(dtype=dtype, shape=shape, name='x')
            z = fluid.layers.instance_norm(input=x)
            x_arr = np.random.uniform(-1, 1, shape).astype(dtype)
<<<<<<< HEAD
            gradient_checker.double_grad_check([x],
                                               z,
                                               x_init=x_arr,
                                               atol=atol,
                                               place=place,
                                               eps=eps)
=======
            gradient_checker.double_grad_check(
                [x], z, x_init=x_arr, atol=atol, place=place, eps=eps
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    def test_grad(self):
        paddle.enable_static()
        places = [fluid.CPUPlace()]
        if core.is_compiled_with_cuda():
            places.append(fluid.CUDAPlace(0))
        for p in places:
            self.func(p)


class TestInstanceNormDoubleGradCheckWithoutParamBias(
<<<<<<< HEAD
        TestInstanceNormDoubleGradCheck):

    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed()
            shape = [2, 3, 4, 5]
            dtype = "float32"
            eps = 0.005
            atol = 1e-4
            x = layers.create_parameter(dtype=dtype, shape=shape, name='x')
            z = fluid.layers.instance_norm(input=x,
                                           param_attr=False,
                                           bias_attr=False)
            x_arr = np.random.uniform(-1, 1, shape).astype(dtype)
            gradient_checker.double_grad_check([x],
                                               z,
                                               x_init=x_arr,
                                               atol=atol,
                                               place=place,
                                               eps=eps)


class TestInstanceNormDoubleGradEagerCheck(unittest.TestCase):

    def instance_norm_wrapper(self, x):
        return paddle.nn.functional.instance_norm(x[0])

=======
    TestInstanceNormDoubleGradCheck
):
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed()
            shape = [2, 3, 4, 5]
            dtype = "float32"
            eps = 0.005
            atol = 1e-4
            x = layers.create_parameter(dtype=dtype, shape=shape, name='x')
<<<<<<< HEAD
            z = paddle.nn.functional.instance_norm(x)
            x_arr = np.random.uniform(-1, 1, shape).astype(dtype)
            # check for static mode
            gradient_checker.double_grad_check([x],
                                               z,
                                               x_init=x_arr,
                                               atol=atol,
                                               place=place,
                                               eps=eps)
            # check for eager mode
            gradient_checker.double_grad_check_for_dygraph(
                self.instance_norm_wrapper, [x],
                z,
                x_init=x_arr,
                atol=atol,
                place=place)

    def test_grad(self):
        paddle.enable_static()
        places = [fluid.CPUPlace()]
        if core.is_compiled_with_cuda():
            places.append(fluid.CUDAPlace(0))
        for p in places:
            self.func(p)


class TestInstanceNormDoubleGradEagerCheckWithParams(
        TestInstanceNormDoubleGradEagerCheck):

    def instance_norm_wrapper(self, x):
        instance_norm = paddle.nn.InstanceNorm2D(3)
        return instance_norm(x[0])

    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed()
            shape = [2, 3, 4, 5]
            dtype = "float32"
            eps = 0.005
            atol = 1e-4
            x = layers.create_parameter(dtype=dtype, shape=shape, name='x')
            z = paddle.nn.InstanceNorm2D(3)(x)
            x_arr = np.random.uniform(-1, 1, shape).astype(dtype)
            # check for static mode
            gradient_checker.double_grad_check([x],
                                               z,
                                               x_init=x_arr,
                                               atol=atol,
                                               place=place,
                                               eps=eps)
            # check for eager mode
            gradient_checker.double_grad_check_for_dygraph(
                self.instance_norm_wrapper, [x],
                z,
                x_init=x_arr,
                atol=atol,
                place=place)
=======
            z = fluid.layers.instance_norm(
                input=x, param_attr=False, bias_attr=False
            )
            x_arr = np.random.uniform(-1, 1, shape).astype(dtype)
            gradient_checker.double_grad_check(
                [x], z, x_init=x_arr, atol=atol, place=place, eps=eps
            )


class TestInstanceNormDoubleGradEagerCheck(unittest.TestCase):
    def instance_norm_wrapper(self, x):
        return paddle.nn.functional.instance_norm(x[0])

    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed()
            shape = [2, 3, 4, 5]
            dtype = "float32"
            eps = 0.005
            atol = 1e-4
            x = layers.create_parameter(dtype=dtype, shape=shape, name='x')
            z = paddle.nn.functional.instance_norm(x)
            x_arr = np.random.uniform(-1, 1, shape).astype(dtype)
            # check for static mode
            gradient_checker.double_grad_check(
                [x], z, x_init=x_arr, atol=atol, place=place, eps=eps
            )
            # check for eager mode
            gradient_checker.double_grad_check_for_dygraph(
                self.instance_norm_wrapper,
                [x],
                z,
                x_init=x_arr,
                atol=atol,
                place=place,
            )

    def test_grad(self):
        paddle.enable_static()
        places = [fluid.CPUPlace()]
        if core.is_compiled_with_cuda():
            places.append(fluid.CUDAPlace(0))
        for p in places:
            self.func(p)


class TestInstanceNormDoubleGradEagerCheckWithParams(
    TestInstanceNormDoubleGradEagerCheck
):
    def instance_norm_wrapper(self, x):
        instance_norm = paddle.nn.InstanceNorm2D(3)
        return instance_norm(x[0])

    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed()
            shape = [2, 3, 4, 5]
            dtype = "float32"
            eps = 0.005
            atol = 1e-4
            x = layers.create_parameter(dtype=dtype, shape=shape, name='x')
            z = paddle.nn.InstanceNorm2D(3)(x)
            x_arr = np.random.uniform(-1, 1, shape).astype(dtype)
            # check for static mode
            gradient_checker.double_grad_check(
                [x], z, x_init=x_arr, atol=atol, place=place, eps=eps
            )
            # check for eager mode
            gradient_checker.double_grad_check_for_dygraph(
                self.instance_norm_wrapper,
                [x],
                z,
                x_init=x_arr,
                atol=atol,
                place=place,
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f


class TestBatchNormDoubleGradCheck(unittest.TestCase):

    def setUp(self):
        self.init_test()

    def init_test(self):
        self.data_layout = 'NCHW'
        self.use_global_stats = False
        self.shape = [2, 3, 4, 5]
        self.channel_index = 1

    def batch_norm_wrapper(self, x):
        batch_norm = paddle.nn.BatchNorm2D(
            self.shape[self.channel_index],
            data_format=self.data_layout,
            use_global_stats=self.use_global_stats,
        )
        return batch_norm(x[0])

    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed()
            dtype = "float32"
            eps = 0.005
            atol = 1e-4
            x = layers.create_parameter(dtype=dtype, shape=self.shape, name='x')
<<<<<<< HEAD
            z = fluid.layers.batch_norm(input=x,
                                        data_layout=self.data_layout,
                                        use_global_stats=self.use_global_stats)
            x_arr = np.random.uniform(-1, 1, self.shape).astype(dtype)
            gradient_checker.double_grad_check([x],
                                               z,
                                               x_init=x_arr,
                                               atol=atol,
                                               place=place,
                                               eps=eps)
=======
            z = fluid.layers.batch_norm(
                input=x,
                data_layout=self.data_layout,
                use_global_stats=self.use_global_stats,
            )
            x_arr = np.random.uniform(-1, 1, self.shape).astype(dtype)
            gradient_checker.double_grad_check(
                [x], z, x_init=x_arr, atol=atol, place=place, eps=eps
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
            gradient_checker.double_grad_check_for_dygraph(
                self.batch_norm_wrapper,
                [x],
                z,
                x_init=x_arr,
                atol=atol,
                place=place,
            )

    def test_grad(self):
        paddle.enable_static()
        places = [fluid.CPUPlace()]
        if core.is_compiled_with_cuda():
            places.append(fluid.CUDAPlace(0))
        for p in places:
            self.func(p)


class TestBatchNormDoubleGradCheckCase1(TestBatchNormDoubleGradCheck):

    def init_test(self):
        self.data_layout = 'NHWC'
        self.use_global_stats = False
        self.shape = [2, 3, 4, 5]
        self.channel_index = 3


class TestBatchNormDoubleGradCheckCase2(TestBatchNormDoubleGradCheck):

    def init_test(self):
        self.data_layout = 'NCHW'
        self.use_global_stats = True
        self.shape = [2, 3, 4, 5]
        self.channel_index = 1


class TestBatchNormDoubleGradCheckCase3(TestBatchNormDoubleGradCheck):

    def init_test(self):
        self.data_layout = 'NHWC'
        self.use_global_stats = True
        self.shape = [2, 3, 4, 5]
        self.channel_index = 3


class TestBatchNormDoubleGradCheckCase4(TestBatchNormDoubleGradCheck):

    def init_test(self):
        self.data_layout = 'NCHW'
        self.use_global_stats = False
        self.shape = [2, 2, 3, 4, 5]
        self.channel_index = 1

    def batch_norm_wrapper(self, x):
        batch_norm = paddle.nn.BatchNorm3D(
            self.shape[self.channel_index],
            data_format=self.data_layout,
            use_global_stats=self.use_global_stats,
        )
        return batch_norm(x[0])


class TestBatchNormDoubleGradCheckCase5(TestBatchNormDoubleGradCheck):

    @prog_scope()
    def func(self, place):
        prog = fluid.Program()
        with fluid.program_guard(prog):
            np.random.seed(37)
            dtype = "float32"
            eps = 0.005
            atol = 2e-4
<<<<<<< HEAD
            chn = self.shape[1] if self.data_layout == 'NCHW' else self.shape[-1]
            x = layers.create_parameter(dtype=dtype, shape=self.shape, name='x')
            z = fluid.layers.batch_norm(input=x,
                                        data_layout=self.data_layout,
                                        use_global_stats=self.use_global_stats)
=======
            chn = (
                self.shape[1] if self.data_layout == 'NCHW' else self.shape[-1]
            )
            x = layers.create_parameter(dtype=dtype, shape=self.shape, name='x')
            z = fluid.layers.batch_norm(
                input=x,
                data_layout=self.data_layout,
                use_global_stats=self.use_global_stats,
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
            x_arr = np.random.uniform(-1, 1, self.shape).astype(dtype)
            w, b = prog.global_block().all_parameters()[1:3]
            w_arr = np.ones(chn).astype(dtype)
            b_arr = np.zeros(chn).astype(dtype)
<<<<<<< HEAD
            gradient_checker.double_grad_check([x, w, b],
                                               z,
                                               x_init=[x_arr, w_arr, b_arr],
                                               atol=atol,
                                               place=place,
                                               eps=eps)
=======
            gradient_checker.double_grad_check(
                [x, w, b],
                z,
                x_init=[x_arr, w_arr, b_arr],
                atol=atol,
                place=place,
                eps=eps,
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f


class TestBatchNormDoubleGradCheckCase6(TestBatchNormDoubleGradCheckCase5):

    def init_test(self):
        self.data_layout = 'NCHW'
        self.use_global_stats = True
        self.shape = [2, 3, 4, 5]
        self.channel_index = 1


if __name__ == "__main__":
    unittest.main()
