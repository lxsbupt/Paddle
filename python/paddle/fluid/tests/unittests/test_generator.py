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
"""Test cloud role maker."""

import unittest
import paddle
import paddle.fluid.generator as generator


class TestGenerator(unittest.TestCase):
    """
    Test cases for cpu generator.
    """

    def test_basic_generator(self):
        """Test basic generator."""
        gen = generator.Generator()
        gen.manual_seed(123123143)
        st = gen.get_state()
        gen.set_state(st)
        gen.random()

    def test_basic_generator_error(self):
        if paddle.fluid.core.is_compiled_with_cuda():
<<<<<<< HEAD
            self.assertRaises(
                ValueError, generator.Generator, place=paddle.CUDAPlace(0)
            )
=======
            self.assertRaises(ValueError,
                              generator.Generator,
                              place=paddle.CUDAPlace(0))
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e


if __name__ == "__main__":
    unittest.main()
