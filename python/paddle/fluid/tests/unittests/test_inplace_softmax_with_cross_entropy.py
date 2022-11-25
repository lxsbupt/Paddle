# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
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

import paddle.fluid as fluid
import numpy as np
import unittest


class TestSoftmaxWithXe(unittest.TestCase):

    def setUp(self):
        self.initParameter()
<<<<<<< HEAD
        self.m, self.n = np.random.random_integers(
            low=100, high=2000, size=[2]
        ).astype('int64')
=======
        self.m, self.n = np.random.random_integers(low=100, high=2000,
                                                   size=[2]).astype('int64')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

    def initParameter(self):
        self.dtype = 'float32'
        self.soft_label = False

    def softmax_with_xe(
        self, x, y, place, inplace=True, numeric_stable_mode=True
    ):
        m, n = x.shape
        with fluid.program_guard(fluid.Program(), fluid.Program()):
            with fluid.scope_guard(fluid.Scope()):
<<<<<<< HEAD
                x_d = fluid.layers.data(
                    name='x',
                    shape=[m, n],
                    dtype=self.dtype,
                    append_batch_size=False,
                )
=======
                x_d = fluid.layers.data(name='x',
                                        shape=[m, n],
                                        dtype=self.dtype,
                                        append_batch_size=False)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                y_d = fluid.layers.data(
                    name='y',
                    shape=[m, 1] if not self.soft_label else [m, n],
                    dtype='int64' if not self.soft_label else self.dtype,
                    append_batch_size=False,
                )
                z_d, s_d = fluid.layers.softmax_with_cross_entropy(
                    x_d,
                    y_d,
                    soft_label=self.soft_label,
                    return_softmax=True,
                    numeric_stable_mode=numeric_stable_mode,
                )

                exe = fluid.Executor(place)

                exe.run(fluid.default_startup_program())

                build_strategy = fluid.BuildStrategy()
                build_strategy.enable_inplace = inplace
                prog = fluid.CompiledProgram(
<<<<<<< HEAD
                    fluid.default_main_program()
                ).with_data_parallel(
                    build_strategy=build_strategy, places=place
                )
=======
                    fluid.default_main_program()).with_data_parallel(
                        build_strategy=build_strategy, places=place)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

                fetch_list = [z_d.name, s_d.name]

                print('Inplace is {}'.format("ON" if inplace else "OFF"))

<<<<<<< HEAD
                z, s = exe.run(
                    prog, feed={x_d.name: x, y_d.name: y}, fetch_list=fetch_list
                )
=======
                z, s = exe.run(prog,
                               feed={
                                   x_d.name: x,
                                   y_d.name: y
                               },
                               fetch_list=fetch_list)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
                return z, s

    def main_with_place(self, place):
        x = np.random.random(size=[self.m, self.n]).astype(self.dtype)
        x_range = [(-30, 30), (10, 20), (-1, 1), (2, 3), (0, 0.3), (-200, -100)]

        for a, b in x_range:
            x = ((b - a) * x + a).astype(self.dtype)
            if not self.soft_label:
<<<<<<< HEAD
                y = np.random.random_integers(
                    size=[self.m, 1], low=0, high=self.n - 1
                ).astype('int64')
            else:
                y = np.random.random(size=[self.m, self.n]).astype(self.dtype)
                norm_y = np.broadcast_to(
                    np.reshape(np.sum(y, axis=1), [-1, 1]), y.shape
                )
                y = y / norm_y

            z1, s1 = self.softmax_with_xe(
                x, y, place, inplace=False, numeric_stable_mode=False
            )
            z2, s2 = self.softmax_with_xe(
                x, y, place, inplace=True, numeric_stable_mode=False
            )
=======
                y = np.random.random_integers(size=[self.m, 1],
                                              low=0,
                                              high=self.n - 1).astype('int64')
            else:
                y = np.random.random(size=[self.m, self.n]).astype(self.dtype)
                norm_y = np.broadcast_to(np.reshape(np.sum(y, axis=1), [-1, 1]),
                                         y.shape)
                y = y / norm_y

            z1, s1 = self.softmax_with_xe(x,
                                          y,
                                          place,
                                          inplace=False,
                                          numeric_stable_mode=False)
            z2, s2 = self.softmax_with_xe(x,
                                          y,
                                          place,
                                          inplace=True,
                                          numeric_stable_mode=False)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            self.assertTrue((z1 == z2).all())
            self.assertTrue((s1 == s2).all())

<<<<<<< HEAD
            z1, s1 = self.softmax_with_xe(
                x, y, place, inplace=False, numeric_stable_mode=True
            )
            z2, s2 = self.softmax_with_xe(
                x, y, place, inplace=True, numeric_stable_mode=True
            )
=======
            z1, s1 = self.softmax_with_xe(x,
                                          y,
                                          place,
                                          inplace=False,
                                          numeric_stable_mode=True)
            z2, s2 = self.softmax_with_xe(x,
                                          y,
                                          place,
                                          inplace=True,
                                          numeric_stable_mode=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            self.assertTrue((z1 == z2).all())
            self.assertTrue((s1 == s2).all())

    def test_main(self):
        self.main_with_place(fluid.CPUPlace())
        if fluid.core.is_compiled_with_cuda():
            self.main_with_place(fluid.CUDAPlace(0))


class TestSoftmaxWithXe1(TestSoftmaxWithXe):

    def initParameter(self):
        self.dtype = 'float32'
        self.soft_label = True


class TestSoftmaxWithXe2(TestSoftmaxWithXe):

    def initParameter(self):
        self.dtype = 'float64'
        self.soft_label = False


class TestSoftmaxWithXe3(TestSoftmaxWithXe):

    def initParameter(self):
        self.dtype = 'float64'
        self.soft_label = True


if __name__ == '__main__':
    unittest.main()
