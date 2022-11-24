# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
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

from .completion import Completer
from .dist_context import get_default_distributed_context
from .tuner.parallel_tuner import ParallelTuner
from .utils import is_naive_data_parallel

# from .tuner.parallel_tuner import ParallelTuner


class Planner:

    def __init__(self, mode, dist_context):
        self._mode = mode
        self._dist_context = dist_context

        # NOTE: [HighOrderGrad]. There are grad ops in forward phase, and it need
        # dependency of backward-forward ops in forward completion.
        default_ctx = get_default_distributed_context()
        self._dist_context._dist_op_context = default_ctx.dist_op_context
<<<<<<< HEAD
        if not default_ctx.data_parallel:
=======
        self._dist_context.data_parallel = default_ctx.data_parallel
        if not is_naive_data_parallel(self._dist_context):
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
            # Use SSA graph for complex parallism
            self._dist_context.initialize(with_graph=True)
        else:
            # Use program for data parallel parallism
            self._dist_context.initialize(with_graph=False)

        self._completer = Completer(self._dist_context)

        self._strategy = dist_context.strategy
<<<<<<< HEAD
        # if self._strategy.auto_search:
        #     self._parallel_tuner = ParallelTuner(
        #         self._dist_context, mode=self._mode)
=======
        # set parallel tuner for auto search
        if self._strategy.auto_mode == "full":
            self._parallel_tuner = ParallelTuner(
                self._dist_context, mode=self._mode
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    @property
    def completer(self):
        return self._completer

    def plan(self):
<<<<<<< HEAD
        self._completer.complete_forward_annotation()
        # if self._strategy.auto_search:
        #     self._parallel_tuner.tune()
        # else:
        #     self._completer.complete_forward_annotation()
        # parse forward sub block
        self._dist_context.block_state.parse_forward_blocks(
            self._dist_context.serial_main_program)
=======
        if self._strategy.auto_mode == "full":
            self._parallel_tuner.tune()
        else:
            self._completer.complete_forward_annotation()
        # parse forward sub block
        self._dist_context.block_state.parse_forward_blocks(
            self._dist_context.serial_main_program
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
