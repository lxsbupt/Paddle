#   Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
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

<<<<<<< HEAD
=======
from __future__ import print_function

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
import unittest
import numpy as np
import sys

sys.path.append('..')
from op_test import OpTest
from paddle.fluid import core
import paddle

alignment = 256
paddle.enable_static()


class TestAllocContinuousSpace(OpTest):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def setUp(self):
        self.op_type = "coalesce_tensor"
        self.dtype, self.fluid_dtype = self.init_dtype()
        attrs = self.init_attr()
        self.copy_data = attrs["copy_data"]
        self.constant = attrs["constant"]
        self.set_constant = attrs["set_constant"]
        self.Inputs = self.init_input()
        self.Outputs, self.FusedOutput = self.init_output(
<<<<<<< HEAD
            self.Inputs, self.set_constant, self.constant
        )
=======
            self.Inputs, self.set_constant, self.constant)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        self.inputs = {'Input': self.Inputs}
        self.attrs = attrs
        self.outputs = {'Output': self.Outputs, 'FusedOutput': self.FusedOutput}

    def init_dtype(self):
        return np.float32, int(core.VarDesc.VarType.FP32)

    def init_input(self):
        inputs = []
        inputs.append(("x1", np.random.random([20, 3]).astype(self.dtype)))
        inputs.append(("x2", np.random.random([20]).astype(self.dtype)))
        inputs.append(("x3", np.random.random([1]).astype(self.dtype)))
        inputs.append(("x4", np.random.random([200, 30]).astype(self.dtype)))
        inputs.append(("x5", np.random.random([30]).astype(self.dtype)))
        inputs.append(("x6", np.random.random([1]).astype(self.dtype)))
        return inputs

    def init_attr(self):
        return {
            "copy_data": True,
            "set_constant": False,
            "constant": 0.0,
<<<<<<< HEAD
            "dtype": self.fluid_dtype,
=======
            "dtype": self.fluid_dtype
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        }

    def init_output(self, input_list, set_constant, constant):
        inputs = []
        outputs = input_list

        for input in input_list:
            length = len(input[1].flatten())
            aligned_len = (length + alignment) / alignment * alignment
            out = np.zeros(int(aligned_len))
            out[0:length] = input[1].flatten()
            inputs.append(out)

        coalesce_tensor_var = np.concatenate([input for input in inputs])
        if set_constant:
            coalesce_tensor_var = np.ones((len(coalesce_tensor_var))) * constant
<<<<<<< HEAD
            outputs = [
                (out[0], np.ones(out[1].shape).astype(self.dtype) * constant)
                for out in outputs
            ]
        return outputs, coalesce_tensor_var

    def test_check_output(self):
        self.check_output_with_place(
            place=paddle.device.MLUPlace(0),
            no_check_set=["FusedOutput"],
            atol=1e-5,
        )


class TestAllocContinuousSpace2(TestAllocContinuousSpace):
=======
            outputs = [(out[0],
                        np.ones(out[1].shape).astype(self.dtype) * constant)
                       for out in outputs]
        return outputs, coalesce_tensor_var

    def test_check_output(self):
        self.check_output_with_place(place=paddle.device.MLUPlace(0),
                                     no_check_set=["FusedOutput"],
                                     atol=1e-5)


class TestAllocContinuousSpace2(TestAllocContinuousSpace):

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def init_attr(self):
        return {
            "copy_data": False,
            "set_constant": True,
            "constant": 5,
            "dtype": self.fluid_dtype,
<<<<<<< HEAD
            "user_defined_size_of_dtype": 2,
        }

    def test_check_output(self):
        self.check_output_with_place(
            place=paddle.device.MLUPlace(0),
            no_check_set=["FusedOutput"],
            atol=1e-5,
        )
=======
            "user_defined_size_of_dtype": 2
        }

    def test_check_output(self):
        self.check_output_with_place(place=paddle.device.MLUPlace(0),
                                     no_check_set=["FusedOutput"],
                                     atol=1e-5)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e


if __name__ == '__main__':
    unittest.main()
