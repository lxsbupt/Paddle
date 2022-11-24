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
from __future__ import print_function

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
import numpy as np
import unittest
import sys

sys.path.append("..")
from op_test import OpTest
import paddle
import paddle.fluid as fluid

SEED = 2022
paddle.enable_static()


class TestLabelSmoothOp(OpTest):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def init_dtype(self):
        self.dtype = np.float32

    def config(self):
        self.op_type = "label_smooth"
        self.place = paddle.MLUPlace(0)
        self.__class__.use_mlu = True
        self.__class__.no_need_check_grad = True
        self.epsilon = 0.1
        batch_size, self.label_dim = 10, 12
        np.random.seed(SEED)
        self.label = np.zeros((batch_size, self.label_dim)).astype(self.dtype)
        nonzero_index = np.random.randint(self.label_dim, size=(batch_size))
        self.label[np.arange(batch_size), nonzero_index] = 1

    def setUp(self):
        self.init_dtype()
        self.config()
        smoothed_label = (
<<<<<<< HEAD
            1 - self.epsilon) * self.label + self.epsilon / self.label_dim
=======
            1 - self.epsilon
        ) * self.label + self.epsilon / self.label_dim
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        smoothed_label = smoothed_label.astype(self.dtype)
        self.inputs = {'X': self.label}
        self.attrs = {'epsilon': self.epsilon}
        self.outputs = {'Out': smoothed_label}

    def test_check_output(self):
        self.check_output_with_place(self.place)


class TestLabelSmoothOpWithPriorDist(TestLabelSmoothOp):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def setUp(self):
        self.init_dtype()
        self.config()
        dist = np.random.random((1, self.label_dim)).astype(self.dtype)
        smoothed_label = (1 - self.epsilon) * self.label + self.epsilon * dist
        smoothed_label = smoothed_label.astype(self.dtype)
        self.inputs = {'X': self.label, 'PriorDist': dist}
        self.attrs = {'epsilon': self.epsilon}
        self.outputs = {'Out': smoothed_label}


class TestLabelSmoothOp3D(TestLabelSmoothOp):
<<<<<<< HEAD

    def setUp(self):
        super(TestLabelSmoothOp3D, self).setUp()
        self.inputs['X'] = self.inputs['X'].reshape(
            [2, -1, self.inputs['X'].shape[-1]])
        self.outputs['Out'] = self.outputs['Out'].reshape(
            self.inputs['X'].shape)


class TestLabelSmoothOpWithPriorDist3D(TestLabelSmoothOpWithPriorDist):

    def setUp(self):
        super(TestLabelSmoothOpWithPriorDist3D, self).setUp()
        self.inputs['X'] = self.inputs['X'].reshape(
            [2, -1, self.inputs['X'].shape[-1]])
        self.outputs['Out'] = self.outputs['Out'].reshape(
            self.inputs['X'].shape)


class TestLabelSmoothOpFP16(TestLabelSmoothOp):

=======
    def setUp(self):
        super().setUp()
        self.inputs['X'] = self.inputs['X'].reshape(
            [2, -1, self.inputs['X'].shape[-1]]
        )
        self.outputs['Out'] = self.outputs['Out'].reshape(
            self.inputs['X'].shape
        )


class TestLabelSmoothOpWithPriorDist3D(TestLabelSmoothOpWithPriorDist):
    def setUp(self):
        super().setUp()
        self.inputs['X'] = self.inputs['X'].reshape(
            [2, -1, self.inputs['X'].shape[-1]]
        )
        self.outputs['Out'] = self.outputs['Out'].reshape(
            self.inputs['X'].shape
        )


class TestLabelSmoothOpFP16(TestLabelSmoothOp):
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def init_dtype(self):
        self.dtype = np.float16


class TestLabelSmoothOpWithPriorDistFP16(TestLabelSmoothOpWithPriorDist):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def init_dtype(self):
        self.dtype = np.float16


class TestLabelSmoothOp3DFP16(TestLabelSmoothOp3D):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def init_dtype(self):
        self.dtype = np.float16


class TestLabelSmoothOpWithPriorDist3DFP16(TestLabelSmoothOpWithPriorDist3D):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def init_dtype(self):
        self.dtype = np.float16


if __name__ == '__main__':
    unittest.main()
