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

<<<<<<< HEAD
=======
from __future__ import print_function

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
import numpy as np
import unittest
import sys

sys.path.append("..")
from op_test import OpTest, skip_check_grad_ci
import paddle
import paddle.fluid as fluid
from paddle.fluid import Program, program_guard
import paddle.fluid.core as core

paddle.enable_static()
SEED = 2022


class TestElementwiseMinOp(OpTest):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def setUp(self):
        self.set_mlu()
        self.op_type = "elementwise_min"
        self.init_dtype()
        self.init_input_output()
        self.inputs = {
            'X': OpTest.np_dtype_to_fluid_dtype(self.x),
<<<<<<< HEAD
            'Y': OpTest.np_dtype_to_fluid_dtype(self.y),
=======
            'Y': OpTest.np_dtype_to_fluid_dtype(self.y)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        }
        self.outputs = {'Out': self.out}
        self.attrs = {'axis': self.axis}

    def set_mlu(self):
        self.__class__.use_mlu = True
        self.place = paddle.device.MLUPlace(0)

    def init_input_output(self):
        # If x and y have the same value, the min() is not differentiable.
        # So we generate test data by the following method
        # to avoid them being too close to each other.
        self.x = np.random.uniform(0.1, 1, [13, 17]).astype(self.dtype)
        self.sgn = np.random.choice([-1, 1], [13, 17]).astype(self.dtype)
        self.y = self.x + self.sgn * np.random.uniform(0.1, 1, [13, 17]).astype(
<<<<<<< HEAD
            self.dtype
        )
=======
            self.dtype)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        self.out = np.minimum(self.x, self.y)
        self.axis = -1

    def init_dtype(self):
        self.dtype = np.float32

    def test_check_output(self):
        self.check_output_with_place(self.place)

    def test_check_grad_normal(self):
        if self.dtype == np.float16:
<<<<<<< HEAD
            self.check_grad_with_place(
                self.place, ['X', 'Y'], 'Out', max_relative_error=0.5
            )
=======
            self.check_grad_with_place(self.place, ['X', 'Y'],
                                       'Out',
                                       max_relative_error=0.5)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        else:
            self.check_grad_with_place(
                self.place,
                ['X', 'Y'],
                'Out',
            )

    def test_check_grad_ingore_x(self):
        if self.dtype == np.float16:
<<<<<<< HEAD
            self.check_grad_with_place(
                self.place,
                ['Y'],
                'Out',
                no_grad_set=set("X"),
                max_relative_error=0.9,
            )
=======
            self.check_grad_with_place(self.place, ['Y'],
                                       'Out',
                                       no_grad_set=set("X"),
                                       max_relative_error=0.9)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        else:
            self.check_grad_with_place(
                self.place,
                ['Y'],
                'Out',
                no_grad_set=set("X"),
            )

    def test_check_grad_ingore_y(self):
        if self.dtype == np.float16:
<<<<<<< HEAD
            self.check_grad_with_place(
                self.place,
                ['X'],
                'Out',
                no_grad_set=set("Y"),
                max_relative_error=0.1,
            )
=======
            self.check_grad_with_place(self.place, ['X'],
                                       'Out',
                                       no_grad_set=set("Y"),
                                       max_relative_error=0.1)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        else:
            self.check_grad_with_place(
                self.place,
                ['X'],
                'Out',
                no_grad_set=set("Y"),
            )


class TestElementwiseMinOpFp16(TestElementwiseMinOp):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def init_dtype(self):
        self.dtype = np.float16


class TestElementwiseMinOp_Vector(TestElementwiseMinOp):
<<<<<<< HEAD
    def init_input_output(self):
        self.x = np.random.uniform(1, 2, (100,)).astype(self.dtype)
        self.sgn = np.random.choice([-1, 1], (100,)).astype(self.dtype)
        self.y = self.x + self.sgn * np.random.uniform(0.1, 1, (100,)).astype(
            self.dtype
        )
=======

    def init_input_output(self):
        self.x = np.random.uniform(1, 2, (100, )).astype(self.dtype)
        self.sgn = np.random.choice([-1, 1], (100, )).astype(self.dtype)
        self.y = self.x + self.sgn * np.random.uniform(0.1, 1, (100, )).astype(
            self.dtype)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        self.out = np.minimum(self.x, self.y)
        self.axis = -1


class TestElementwiseMinOpFp16_Vector(TestElementwiseMinOp_Vector):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def init_dtype(self):
        self.dtype = np.float16


@skip_check_grad_ci(
<<<<<<< HEAD
    reason="[skip shape check] Use y_shape(1) to test broadcast."
)
class TestElementwiseMinOp_scalar(TestElementwiseMinOp):
=======
    reason="[skip shape check] Use y_shape(1) to test broadcast.")
class TestElementwiseMinOp_scalar(TestElementwiseMinOp):

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def init_input_output(self):
        self.x = np.random.random_integers(-5, 5, [10, 3, 4]).astype(self.dtype)
        self.y = np.array([0.5]).astype(self.dtype)
        self.out = np.minimum(self.x, self.y)
        self.axis = -1


@skip_check_grad_ci(
<<<<<<< HEAD
    reason="[skip shape check] Use y_shape(1) to test broadcast."
)
class TestElementwiseMinOpFp16_scalar(TestElementwiseMinOp_scalar):
=======
    reason="[skip shape check] Use y_shape(1) to test broadcast.")
class TestElementwiseMinOpFp16_scalar(TestElementwiseMinOp_scalar):

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def init_dtype(self):
        self.dtype = np.float16


class TestElementwiseMinOp_broadcast(TestElementwiseMinOp):
<<<<<<< HEAD
    def init_input_output(self):
        self.x = np.random.uniform(0.5, 1, (2, 3, 100)).astype(self.dtype)
        self.sgn = np.random.choice([-1, 1], (100,)).astype(self.dtype)
        self.y = self.x[0, 0, :] + self.sgn * np.random.uniform(
            1, 2, (100,)
        ).astype(self.dtype)
=======

    def init_input_output(self):
        self.x = np.random.uniform(0.5, 1, (2, 3, 100)).astype(self.dtype)
        self.sgn = np.random.choice([-1, 1], (100, )).astype(self.dtype)
        self.y = self.x[0, 0, :] + self.sgn * \
            np.random.uniform(1, 2, (100, )).astype(self.dtype)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        self.out = np.minimum(self.x, self.y.reshape(1, 1, 100))
        self.axis = -1


class TestElementwiseMinOpFp16_broadcast(TestElementwiseMinOp_broadcast):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def init_dtype(self):
        self.dtype = np.float16


class TestElementwiseMinOpNet(unittest.TestCase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def _test(self, run_mlu=True):
        main_prog = paddle.static.Program()
        startup_prog = paddle.static.Program()
        main_prog.random_seed = SEED
        startup_prog.random_seed = SEED
        np.random.seed(SEED)

        a_np = np.random.random(size=(32, 32)).astype('float32')
        b_np = np.random.random(size=(32, 32)).astype('float32')
        label_np = np.random.randint(2, size=(32, 1)).astype('int64')

        with paddle.static.program_guard(main_prog, startup_prog):
            a = paddle.static.data(name="a", shape=[32, 32], dtype='float32')
            b = paddle.static.data(name="b", shape=[32, 32], dtype='float32')
<<<<<<< HEAD
            label = paddle.static.data(
                name="label", shape=[32, 1], dtype='int64'
            )
=======
            label = paddle.static.data(name="label",
                                       shape=[32, 1],
                                       dtype='int64')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            c = paddle.minimum(a, b)

            fc_1 = fluid.layers.fc(input=c, size=128)
            prediction = fluid.layers.fc(input=fc_1, size=2, act='softmax')

            cost = fluid.layers.cross_entropy(input=prediction, label=label)
            loss = fluid.layers.reduce_mean(cost)
            sgd = fluid.optimizer.SGD(learning_rate=0.01)
            sgd.minimize(loss)

        if run_mlu:
            place = paddle.device.MLUPlace(0)
        else:
            place = paddle.CPUPlace()

        exe = paddle.static.Executor(place)
        exe.run(startup_prog)

        print("Start run on {}".format(place))
        for epoch in range(100):

<<<<<<< HEAD
            pred_res, loss_res = exe.run(
                main_prog,
                feed={"a": a_np, "b": b_np, "label": label_np},
                fetch_list=[prediction, loss],
            )
            if epoch % 10 == 0:
                print(
                    "Epoch {} | Prediction[0]: {}, Loss: {}".format(
                        epoch, pred_res[0], loss_res
                    )
                )
=======
            pred_res, loss_res = exe.run(main_prog,
                                         feed={
                                             "a": a_np,
                                             "b": b_np,
                                             "label": label_np
                                         },
                                         fetch_list=[prediction, loss])
            if epoch % 10 == 0:
                print("Epoch {} | Prediction[0]: {}, Loss: {}".format(
                    epoch, pred_res[0], loss_res))
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

        return pred_res, loss_res

    def test_mlu(self):
        cpu_pred, cpu_loss = self._test(False)
        mlu_pred, mlu_loss = self._test(True)

<<<<<<< HEAD
        np.testing.assert_allclose(mlu_pred, cpu_pred, rtol=1e-6)
        np.testing.assert_allclose(mlu_loss, cpu_loss)
=======
        self.assertTrue(np.allclose(mlu_pred, cpu_pred))
        self.assertTrue(np.allclose(mlu_loss, cpu_loss))
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e


if __name__ == '__main__':
    unittest.main()
