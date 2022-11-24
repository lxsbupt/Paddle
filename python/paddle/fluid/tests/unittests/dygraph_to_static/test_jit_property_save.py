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
import numpy
=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
import unittest
import paddle


class TestPropertySave(unittest.TestCase):
<<<<<<< HEAD
    """test jit property save
    """
=======
    """test jit property save"""
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    def setUp(self):
        a = paddle.framework.core.Property()
        a.set_float('a', 1.0)
        a.set_floats('b', [1.02, 2.3, 4.23])

        b = paddle.framework.core.Property()
        b.parse_from_string(a.serialize_to_string())

        self.a = a
        self.b = b

    def test_property_save(self):
        self.assertEqual(self.a.get_float('a'), self.b.get_float('a'))
        self.assertEqual(self.a.get_float(0), 1.0)

    def test_size(self):
        self.assertEqual(self.b.size(), 2)
        self.assertEqual(self.a.size(), 2)

    def test_load_float(self):
        with self.assertRaises(ValueError):
            self.a.get_float(1)

<<<<<<< HEAD
    def test_set_float_wo_name(self):
        """test save without name
        """
        a = paddle.framework.core.Property()
        a.set_float(10.0)
        self.assertEqual(a.get_float(0), 10.0)

    def test_set(self):
        """test propety set.
        """
        try:
            a = paddle.framework.core.Property()
            a.set_float(10.0)
            a.set_float('float', 10.0)
            a.set_floats([5.0, 4.0, 3.0])
            a.set_floats('floats', [5.0, 4.0, 3.0])
            a.set_int(5)
            a.set_int('int', 5)
            a.set_ints([1, 2, 3])
            a.set_ints('ints', [1, 2, 3])
            a.set_string("hello")
            a.set_string("str", "hello")
            a.set_strings(["1", "2", "3"])
=======
    def test_set(self):
        """test propety set."""
        try:
            a = paddle.framework.core.Property()
            a.set_float('float', 10.0)
            a.set_floats('floats', [5.0, 4.0, 3.0])
            a.set_int('int', 5)
            a.set_ints('ints', [1, 2, 3])
            a.set_string("str", "hello")
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
            a.set_strings('strs', ["1", "2", "3"])
        except Exception as e:
            self.assertEqual(False, True)


if __name__ == '__main__':
    unittest.main()
