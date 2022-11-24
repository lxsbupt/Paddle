# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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
from trt_layer_auto_scan_test import TrtLayerAutoScanTest, SkipReasons
=======
from trt_layer_auto_scan_test import TrtLayerAutoScanTest
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
from program_config import TensorConfig, ProgramConfig
import numpy as np
import paddle.inference as paddle_infer
from functools import partial
<<<<<<< HEAD
from typing import Optional, List, Callable, Dict, Any, Set
=======
from typing import List
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
import unittest


class TrtConvertSumTest(TrtLayerAutoScanTest):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    def is_program_valid(self, program_config: ProgramConfig) -> bool:
        return True

    def sample_program_configs(self):
<<<<<<< HEAD

=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        def generate_input1(batch):
            if self.dims == 4:
                return np.ones([batch, 3, 24, 24]).astype(np.float32)
            elif self.dims == 3:
                return np.ones([batch, 3, 24]).astype(np.float32)
            elif self.dims == 2:
                return np.ones([batch, 24]).astype(np.float32)
            elif self.dims == 1:
                return np.ones([24]).astype(np.float32)

        for dims in [1, 2, 3, 4]:
            for batch in [1, 4]:
                self.dims = dims
<<<<<<< HEAD
                ops_config = [{
                    "op_type": "shape",
                    "op_inputs": {
                        "Input": ["input1"]
                    },
                    "op_outputs": {
                        "Out": ["output"]
                    },
                    "op_attrs": {}
                }]
=======
                ops_config = [
                    {
                        "op_type": "shape",
                        "op_inputs": {"Input": ["input1"]},
                        "op_outputs": {"Out": ["output"]},
                        "op_attrs": {},
                    }
                ]
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
                ops = self.generate_op_config(ops_config)
                program_config = ProgramConfig(
                    ops=ops,
                    weights={},
                    inputs={
<<<<<<< HEAD
                        "input1":
                        TensorConfig(data_gen=partial(generate_input1, batch))
                    },
                    outputs=["output"])
=======
                        "input1": TensorConfig(
                            data_gen=partial(generate_input1, batch)
                        )
                    },
                    outputs=["output"],
                )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

                yield program_config

    def sample_predictor_configs(
<<<<<<< HEAD
            self, program_config) -> (paddle_infer.Config, List[int], float):

=======
        self, program_config
    ) -> (paddle_infer.Config, List[int], float):
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        def generate_dynamic_shape():
            if self.dims == 4:
                self.dynamic_shape.min_input_shape = {"input1": [1, 3, 24, 24]}
                self.dynamic_shape.max_input_shape = {"input1": [4, 3, 48, 48]}
                self.dynamic_shape.opt_input_shape = {"input1": [1, 3, 24, 24]}
            elif self.dims == 3:
                self.dynamic_shape.min_input_shape = {"input1": [1, 3, 24]}
                self.dynamic_shape.max_input_shape = {"input1": [4, 3, 48]}
                self.dynamic_shape.opt_input_shape = {"input1": [1, 3, 24]}
            elif self.dims == 2:
                self.dynamic_shape.min_input_shape = {"input1": [1, 24]}
                self.dynamic_shape.max_input_shape = {"input1": [4, 48]}
                self.dynamic_shape.opt_input_shape = {"input1": [1, 24]}
            elif self.dims == 1:
                self.dynamic_shape.min_input_shape = {"input1": [24]}
                self.dynamic_shape.max_input_shape = {"input1": [48]}
                self.dynamic_shape.opt_input_shape = {
                    "input1": [24],
                }

        def generate_trt_nodes_num(dynamic_shape):
<<<<<<< HEAD
            if (not dynamic_shape):
=======
            if not dynamic_shape:
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
                return 0, 3
            return 1, 2

        def clear_dynamic_shape():
            self.dynamic_shape.min_input_shape = {}
            self.dynamic_shape.max_input_shape = {}
            self.dynamic_shape.opt_input_shape = {}

        # for static_shape
        clear_dynamic_shape()
        self.trt_param.precision = paddle_infer.PrecisionType.Float32
        yield self.create_inference_config(), generate_trt_nodes_num(
<<<<<<< HEAD
            False), 1e-5
        self.trt_param.precision = paddle_infer.PrecisionType.Half
        yield self.create_inference_config(), generate_trt_nodes_num(
            False), 1e-5
=======
            False
        ), 1e-5
        self.trt_param.precision = paddle_infer.PrecisionType.Half
        yield self.create_inference_config(), generate_trt_nodes_num(
            False
        ), 1e-3
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        # for dynamic_shape
        generate_dynamic_shape()
        self.trt_param.precision = paddle_infer.PrecisionType.Float32
        yield self.create_inference_config(), generate_trt_nodes_num(True), 1e-5
        self.trt_param.precision = paddle_infer.PrecisionType.Half
<<<<<<< HEAD
        yield self.create_inference_config(), generate_trt_nodes_num(True), 1e-5
=======
        yield self.create_inference_config(), generate_trt_nodes_num(True), 1e-3
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    def test(self):
        self.run_test()


if __name__ == "__main__":
    unittest.main()
