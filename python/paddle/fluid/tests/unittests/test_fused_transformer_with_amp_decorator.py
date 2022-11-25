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

import paddle
import paddle.nn as nn
<<<<<<< HEAD
from paddle.incubate.nn.layer.fused_transformer import (
    FusedMultiHeadAttention,
    FusedFeedForward,
)
=======
from paddle.incubate.nn.layer.fused_transformer import FusedMultiHeadAttention, FusedFeedForward
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
import unittest


class PreModel(nn.Layer):
<<<<<<< HEAD
    def __init__(self):
        super().__init__()
=======

    def __init__(self):
        super(PreModel, self).__init__()
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        self.attn = FusedMultiHeadAttention(
            embed_dim=1024,
            num_heads=16,
            normalize_before=False,
        )
<<<<<<< HEAD
        self.ffn = FusedFeedForward(
            d_model=1024, dim_feedforward=4096, normalize_before=False
        )
=======
        self.ffn = FusedFeedForward(d_model=1024,
                                    dim_feedforward=4096,
                                    normalize_before=False)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

    def forward(self, x):
        x = self.attn(x)
        x = self.ffn(x)


class PostModel(nn.Layer):
<<<<<<< HEAD
    def __init__(self):
        super().__init__()
=======

    def __init__(self):
        super(PostModel, self).__init__()
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
        self.attn = FusedMultiHeadAttention(
            embed_dim=1024,
            num_heads=16,
            normalize_before=True,
        )
<<<<<<< HEAD
        self.ffn = FusedFeedForward(
            d_model=1024, dim_feedforward=4096, normalize_before=True
        )
=======
        self.ffn = FusedFeedForward(d_model=1024,
                                    dim_feedforward=4096,
                                    normalize_before=True)
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e

    def forward(self, x):
        x = self.attn(x)
        x = self.ffn(x)


class TestFusedTransformerWithAmpDecorator(unittest.TestCase):
<<<<<<< HEAD
=======

>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
    def get_model(self):
        self.pre_model = PreModel()
        self.post_model = PostModel()

    def test_run(self):
        self.get_model()
<<<<<<< HEAD
        pre_model = paddle.amp.decorate(
            models=self.pre_model, level='O2', save_dtype='float32'
        )
        post_model = paddle.amp.decorate(
            models=self.post_model, level='O2', save_dtype='float32'
        )
=======
        pre_model = paddle.amp.decorate(models=self.pre_model,
                                        level='O2',
                                        save_dtype='float32')
        post_model = paddle.amp.decorate(models=self.post_model,
                                         level='O2',
                                         save_dtype='float32')
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e


if __name__ == "__main__":
    unittest.main()
