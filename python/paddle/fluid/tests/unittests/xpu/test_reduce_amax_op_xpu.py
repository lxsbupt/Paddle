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

sys.path.append("..")

import paddle
<<<<<<< HEAD
from op_test_xpu import XPUOpTest
from xpu.get_test_cover_info import (
    create_test_class,
    get_xpu_op_support_types,
    XPUOpTestWrapper,
)
=======
from op_test import OpTest
from op_test_xpu import XPUOpTest
from xpu.get_test_cover_info import create_test_class, get_xpu_op_support_types, XPUOpTestWrapper
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

paddle.enable_static()


class XPUTestReduceAmaxOp(XPUOpTestWrapper):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def __init__(self):
        self.op_name = 'reduce_amax'

    class XPUTestReduceAmaxBase(XPUOpTest):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        def setUp(self):
            self.place = paddle.XPUPlace(0)
            self.set_case()

        def set_case(self):
            self.op_type = 'reduce_amax'
            self.shape = (20, 10)
<<<<<<< HEAD
            self.attrs = {'use_xpu': True, 'keep_dim': False, 'dim': (1,)}
=======
            self.attrs = {'use_xpu': True, 'keep_dim': False, 'dim': (1, )}
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

            self.inputs = {
                'X': np.random.randint(0, 100, self.shape).astype("float32")
            }

            expect_intput = self.inputs['X']
            self.outputs = {
<<<<<<< HEAD
                'Out': np.amax(
                    expect_intput,
                    axis=self.attrs['dim'],
                    keepdims=self.attrs['keep_dim'],
                )
=======
                'Out':
                np.amax(expect_intput,
                        axis=self.attrs['dim'],
                        keepdims=self.attrs['keep_dim'])
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            }

        def test_check_output(self):
            self.check_output_with_place(self.place)


support_types = get_xpu_op_support_types('reduce_amax')
for stype in support_types:
    create_test_class(globals(), XPUTestReduceAmaxOp, stype)

if __name__ == '__main__':
    unittest.main()
