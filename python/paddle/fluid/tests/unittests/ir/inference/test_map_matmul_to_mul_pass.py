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

from auto_scan_test import PassAutoScanTest, IgnoreReasons
from program_config import TensorConfig, ProgramConfig, OpConfig
import unittest

import hypothesis.strategies as st


class TestMapMatmulToMulPass(PassAutoScanTest):
    r"""
    x_var    y_var(persistable)
      \       /
        matmul
    """

    def sample_predictor_configs(self, program_config):
        # cpu
        config = self.create_inference_config(use_gpu=False)
        yield config, [
            "mul",
        ], (1e-5, 1e-5)

        # for gpu
        config = self.create_inference_config(use_gpu=True)
        yield config, [
            "mul",
        ], (1e-5, 1e-5)

        # TRT
        # config = self.create_trt_inference_config()
        # config.enable_tensorrt_engine(
        #     max_batch_size=10,
        #     workspace_size=10240,
        #     min_subgraph_size=0,
        #     precision_mode=paddle_infer.PrecisionType.Float32,
        #     use_static=False,
        #     use_calib_mode=False)
        # yield config, ["mul", ], (1e-5, 1e-5)

    def add_ignore_pass_case(self):
        # Here we put some skip rules to avoid known bugs
        def teller1(program_config, predictor_config):
            if predictor_config.use_gpu():
                # On 3080, the results of MatMul and Mul are different
                return True

            if predictor_config.tensorrt_engine_enabled():
                # On 3080, the results of MatMul and Mul are different
                return True

                x_shape = list(program_config.inputs["matmul_x"].shape)
                if len(x_shape) > 5:
                    return True
            return False

        self.add_ignore_check_case(
            teller1,
            IgnoreReasons.PASS_ACCURACY_ERROR,
            "The pass error on TRT while shape of mul_x > 5.",
        )

    def sample_program_config(self, draw):
        # 1. Generate shape and attr of matmul
        x_shape = draw(
<<<<<<< HEAD
            st.lists(st.integers(min_value=1, max_value=8),
                     min_size=2,
                     max_size=5))
        y_shape = draw(
            st.lists(st.integers(min_value=1, max_value=8),
                     min_size=2,
                     max_size=2))
=======
            st.lists(
                st.integers(min_value=1, max_value=8), min_size=2, max_size=5
            )
        )
        y_shape = draw(
            st.lists(
                st.integers(min_value=1, max_value=8), min_size=2, max_size=2
            )
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        y_shape[0] = x_shape[-1]
        alpha = 1.0
        transpose_X = False
        transpose_Y = False

        matmul_op = OpConfig(
            "matmul",
<<<<<<< HEAD
            inputs={
                "X": ["matmul_x"],
                "Y": ["matmul_y"]
            },
=======
            inputs={"X": ["matmul_x"], "Y": ["matmul_y"]},
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
            outputs={"Out": ["matmul_out"]},
            alpha=alpha,
            transpose_X=transpose_X,
            transpose_Y=transpose_Y,
            fused_reshape_X=[],
            fused_reshape_Y=[],
            fused_transpose_X=[],
            fused_transpose_Y=[],
            fused_reshape_Out=[],
            fused_transpose_Out=[],
        )

        ops = [
            matmul_op,
        ]
        weights = {
            "matmul_y": TensorConfig(shape=y_shape),
        }
        inputs = {
            "matmul_x": TensorConfig(shape=x_shape),
        }
        program_config = ProgramConfig(
            ops=ops,
            weights=weights,
            inputs=inputs,
            outputs=ops[-1].outputs["Out"],
        )
        return program_config

    def test(self):
<<<<<<< HEAD
        self.run_and_statis(quant=False,
                            max_examples=100,
                            passes=["gpu_cpu_map_matmul_to_mul_pass"],
                            max_duration=180)
=======
        self.run_and_statis(
            quant=False,
            max_examples=100,
            passes=["gpu_cpu_map_matmul_to_mul_pass"],
            max_duration=180,
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f


if __name__ == "__main__":
    unittest.main()
