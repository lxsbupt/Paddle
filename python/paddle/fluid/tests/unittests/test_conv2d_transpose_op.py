#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
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

import os
import unittest
import numpy as np

import paddle
import paddle.nn as nn

paddle.enable_static()
import paddle.fluid.core as core
import paddle.fluid as fluid
from paddle.fluid import Program, program_guard
from test_attribute_var import UnittestBase
from op_test import OpTest


def conv2dtranspose_forward_naive(input_, filter_, attrs):
    padding_algorithm = attrs['padding_algorithm']
    if padding_algorithm not in ["SAME", "VALID", "EXPLICIT"]:
        raise ValueError(
            "Unknown Attr(padding_algorithm): '%s'. "
            "It can only be 'SAME' or 'VALID'." % str(padding_algorithm)
        )

    if attrs['data_format'] == 'NHWC':
        input_ = np.transpose(input_, [0, 3, 1, 2])
    in_n, in_c, in_h, in_w = input_.shape
    f_c, f_out_c, f_h, f_w = filter_.shape
    groups = attrs['groups']
    assert in_c == f_c
    out_c = f_out_c * groups
    sub_in_c = in_c // groups

    stride, pad, dilations = (
        attrs['strides'],
        attrs['paddings'],
        attrs['dilations'],
    )

    # update pad and dilation
    def _get_padding_with_SAME(input_shape, kernel_size, kernel_stride):
        padding = []
<<<<<<< HEAD
        for input_size, filter_size, stride_size in zip(input_shape,
                                                        kernel_size,
                                                        kernel_stride):
            out_size = int((input_size + stride_size - 1) / stride_size)
            pad_sum = np.max(
                ((out_size - 1) * stride_size + filter_size - input_size, 0))
=======
        for input_size, filter_size, stride_size in zip(
            input_shape, kernel_size, kernel_stride
        ):
            out_size = int((input_size + stride_size - 1) / stride_size)
            pad_sum = np.max(
                ((out_size - 1) * stride_size + filter_size - input_size, 0)
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
            pad_0 = int(pad_sum / 2)
            pad_1 = int(pad_sum - pad_0)
            padding.append(pad_0)
            padding.append(pad_1)
        return padding

    ksize = filter_.shape[2:4]
    if padding_algorithm == "VALID":
        pad = [0, 0, 0, 0]
    elif padding_algorithm == "SAME":
        dilations = [1, 1]
        input_data_shape = input_.shape[2:4]
        pad = _get_padding_with_SAME(input_data_shape, ksize, stride)

    pad_h_0, pad_h_1 = pad[0], pad[0]
    pad_w_0, pad_w_1 = pad[1], pad[1]
    if len(pad) == 4:
        pad_h_0, pad_h_1 = pad[0], pad[1]
        pad_w_0, pad_w_1 = pad[2], pad[3]

    d_bolck_h = dilations[0] * (f_h - 1) + 1
    d_bolck_w = dilations[1] * (f_w - 1) + 1
    out_h = (in_h - 1) * stride[0] + d_bolck_h
    out_w = (in_w - 1) * stride[1] + d_bolck_w
    if 'output_size' in attrs:
        output_size = attrs['output_size']
        out_h = output_size[0] + pad_h_0 + pad_h_1
        out_w = output_size[1] + pad_w_0 + pad_w_1
    out_pad_h = 0
    out_pad_w = 0
    if 'output_padding' in attrs:
        out_pad_h = attrs['output_padding'][0]
        out_pad_w = attrs['output_padding'][1]
<<<<<<< HEAD
    out = np.zeros((in_n, out_c, out_h + out_pad_h, out_w + out_pad_w),
                   dtype=input_.dtype)
=======
    out = np.zeros(
        (in_n, out_c, out_h + out_pad_h, out_w + out_pad_w), dtype=input_.dtype
    )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    for n in range(in_n):
        for i in range(in_h):
            for j in range(in_w):
                for g in range(groups):
                    input_masked = input_[
                        n, g * sub_in_c : (g + 1) * sub_in_c, i, j
                    ]  # (c)
                    input_masked = np.reshape(input_masked, (sub_in_c, 1, 1))
                    input_masked = np.tile(input_masked, (1, f_h, f_w))

                    for k in range(f_out_c):
                        tmp_out = np.sum(
                            input_masked
                            * filter_[
                                g * sub_in_c : (g + 1) * sub_in_c, k, :, :
                            ],
                            axis=0,
                        )
                        i1, i2 = i * stride[0], i * stride[0] + d_bolck_h
                        j1, j2 = j * stride[1], j * stride[1] + d_bolck_w
<<<<<<< HEAD
                        out[n, g * f_out_c + k, i1:i2:dilations[0],
                            j1:j2:dilations[1]] += tmp_out

    out = out[:, :, pad_h_0:out_h - pad_h_1 + out_pad_h,
              pad_w_0:out_w - pad_w_1 + out_pad_w]
=======
                        out[
                            n,
                            g * f_out_c + k,
                            i1 : i2 : dilations[0],
                            j1 : j2 : dilations[1],
                        ] += tmp_out

    out = out[
        :,
        :,
        pad_h_0 : out_h - pad_h_1 + out_pad_h,
        pad_w_0 : out_w - pad_w_1 + out_pad_w,
    ]
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    if attrs['data_format'] == 'NHWC':
        out = np.transpose(out, [0, 2, 3, 1])
    return out


class TestConv2DTransposeOp(OpTest):

    def setUp(self):
        # init as conv transpose
        self.dtype = np.float32 if core.is_compiled_with_rocm() else np.float64
        self.need_check_grad = True
        self.is_test = False
        self.use_cudnn = False
        self.use_mkldnn = False
        self.output_size = None
        self.output_padding = []
        self.data_format = "NCHW"
        self.pad = [0, 0]
        self.padding_algorithm = "EXPLICIT"
        self.init_op_type()
        self.init_test_case()

        input_ = np.random.random(self.input_size).astype(self.dtype)
        filter_ = np.random.random(self.filter_size).astype(self.dtype)

        self.inputs = {'Input': input_, 'Filter': filter_}
        self.attrs = {
            'strides': self.stride,
            'paddings': self.pad,
            'padding_algorithm': self.padding_algorithm,
            'groups': self.groups,
            'dilations': self.dilations,
            'use_cudnn': self.use_cudnn,
            'is_test': self.is_test,
            'use_mkldnn': self.use_mkldnn,
            'data_format': self.data_format,
        }
        if self.output_size is not None:
            self.attrs['output_size'] = self.output_size

        if len(self.output_padding) > 0:
            self.attrs['output_padding'] = self.output_padding

        output = conv2dtranspose_forward_naive(
            input_, filter_, self.attrs
        ).astype(self.dtype)

        self.outputs = {'Output': output}

    def test_check_output(self):
        # TODO(wangzhongpu): support mkldnn op in dygraph mode
        if self.use_cudnn:
            place = core.CUDAPlace(0)
            self.check_output_with_place(
                place, atol=1e-5, check_dygraph=(not self.use_mkldnn)
            )
        else:
            self.check_output(check_dygraph=(not self.use_mkldnn))

    def test_check_grad_no_input(self):
        if self.need_check_grad:
            if self.use_cudnn:
                place = core.CUDAPlace(0)
<<<<<<< HEAD
                self.check_grad_with_place(place, ['Filter'],
                                           'Output',
                                           max_relative_error=0.02,
                                           no_grad_set=set(['Input']))
            else:
                self.check_grad(['Filter'],
                                'Output',
                                no_grad_set=set(['Input']))
=======
                self.check_grad_with_place(
                    place,
                    ['Filter'],
                    'Output',
                    max_relative_error=0.02,
                    no_grad_set=set(['Input']),
                )
            else:
                self.check_grad(
                    ['Filter'], 'Output', no_grad_set=set(['Input'])
                )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    def test_check_grad_no_filter(self):
        if self.need_check_grad:
            if self.use_cudnn:
                place = core.CUDAPlace(0)
<<<<<<< HEAD
                self.check_grad_with_place(place, ['Input'],
                                           'Output',
                                           no_grad_set=set(['Filter']))
            else:
                self.check_grad(['Input'],
                                'Output',
                                no_grad_set=set(['Filter']))
=======
                self.check_grad_with_place(
                    place, ['Input'], 'Output', no_grad_set=set(['Filter'])
                )
            else:
                self.check_grad(
                    ['Input'], 'Output', no_grad_set=set(['Filter'])
                )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    def test_check_grad(self):
        if self.need_check_grad:
            if self.use_cudnn:
                place = core.CUDAPlace(0)
<<<<<<< HEAD
                self.check_grad_with_place(place,
                                           set(['Input', 'Filter']),
                                           'Output',
                                           max_relative_error=0.02)
            else:
                self.check_grad(set(['Input', 'Filter']),
                                'Output',
                                max_relative_error=0.02)
=======
                self.check_grad_with_place(
                    place,
                    set(['Input', 'Filter']),
                    'Output',
                    max_relative_error=0.02,
                )
            else:
                self.check_grad(
                    set(['Input', 'Filter']), 'Output', max_relative_error=0.02
                )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    def init_test_case(self):
        self.pad = [0, 0]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]

    def init_op_type(self):
        self.op_type = "conv2d_transpose"


class TestWithSymmetricPad(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]


class TestWithAsymmetricPad(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 0, 1, 2]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]


class TestWithSAMEPad(TestConv2DTransposeOp):

    def init_test_case(self):
        self.stride = [2, 1]
        self.dilations = [1, 2]
        self.groups = 1
        self.input_size = [2, 3, 6, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 4, 3]
        self.padding_algorithm = 'SAME'


class TestWithVALIDPad(TestConv2DTransposeOp):

    def init_test_case(self):
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]
        self.padding_algorithm = 'VALID'


class TestWithGroups(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 2
        self.input_size = [2, 4, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 3, 3, 3]


class TestWithStride(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [2, 2]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]


class TestWithDilation(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [2, 2]
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]


class TestWithEvenUpsample(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [2, 2]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.output_size = [14, 14]
        self.input_size = [2, 3, 7, 7]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 5, 5]


class TestWithEvenUpsampleOutputPadding(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [2, 2]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.output_padding = [1, 1]
        self.input_size = [2, 3, 7, 7]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 5, 5]


class Test_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [0, 0]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


class TestWithSymmetricPad_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


class TestWithAsymmetricPad_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 0, 1, 2]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


class TestWithGroups_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 2
        self.input_size = [2, 5, 5, 4]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 3, 3, 3]
        self.data_format = 'NHWC'


class TestWithStride_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [2, 2]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 5, 5, 3]  # NCHW
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


class TestWithDilation_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [2, 2]
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


class TestWithEvenUpsample_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [2, 2]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.output_size = [14, 14]
        self.input_size = [2, 7, 7, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 5, 5]
        self.data_format = 'NHWC'


class TestWithEvenUpsample_NHWC_output_padding(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [2, 2]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.output_padding = [1, 1]
        self.input_size = [2, 7, 7, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 5, 5]
        self.data_format = 'NHWC'


# ------------ test_cudnn ------------
@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNN(TestConv2DTransposeOp):

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithSymmetricPad(TestWithSymmetricPad):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithAsymmetricPad(TestWithAsymmetricPad):

    def init_test_case(self):
        self.pad = [1, 0, 1, 2]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithSAMEPad(TestWithSAMEPad):

    def init_test_case(self):
        self.pad = [1, 0, 1, 2]
        self.stride = [1, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithVALIDPad(TestWithVALIDPad):

    def init_test_case(self):
        self.pad = [1, 0, 1, 2]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithStride(TestWithStride):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithGroups(TestWithGroups):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 2
        self.input_size = [2, 4, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 3, 3, 3]

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


# ------------ test_cudnn ------------
@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithEvenUpsample(TestWithEvenUpsample):

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


# Please Don't remove the following code.
# Currently, CI use cudnn V5.0 which not support dilation conv.
# class TestCUDNNWithDilation(TestWithDilation):
#     def init_test_case(self):
#         self.pad = [1, 1]
#         self.stride = [2, 2]
#         self.dilations = [2, 2]
#         self.input_size = [2, 3, 5, 5]  # NCHW
#         f_c = self.input_size[1]
#         self.filter_size = [f_c, 6, 3, 3]
#
#     def init_op_type(self):
#         self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNN_NHWC(TestConv2DTransposeOp):

    def init_test_case(self):
        self.pad = [0, 0]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithSymmetricPad_NHWC(TestWithSymmetricPad):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithAsymmetricPad_NHWC(TestWithSymmetricPad):

    def init_test_case(self):
        self.pad = [1, 0, 2, 3]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithStride_NHWC(TestWithStride):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithGroups_NHWC(TestWithGroups):

    def init_test_case(self):
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 2
        self.input_size = [2, 5, 5, 4]  # NCHW
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 3, 3, 3]
        self.data_format = 'NHWC'

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithEvenUpsample_NHWC(TestWithEvenUpsample):

    def init_test_case(self):
        self.pad = [2, 2]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.output_size = [14, 14]
        self.input_size = [2, 7, 7, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 5, 5]
        self.data_format = 'NHWC'

    def init_op_type(self):
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNN_FP16(TestConv2DTransposeOp):

    def init_test_case(self):
        self.dtype = np.float16
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 3, 5, 5]  # NCHW
        f_c = self.input_size[1]
        self.filter_size = [f_c, 6, 3, 3]

    def init_op_type(self):
        self.need_check_grad = False
        self.use_cudnn = True
        self.op_type = "conv2d_transpose"

    def test_check_output(self):
        if self.use_cudnn:
            place = core.CUDAPlace(0)
            self.check_output_with_place(
                place, atol=0.02, check_dygraph=(not self.use_mkldnn)
            )
        else:
            self.check_output(check_dygraph=(not self.use_mkldnn))


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNN_NHWC_FP16(TestCUDNN_FP16):

    def init_test_case(self):
        self.dtype = np.float16
        self.pad = [0, 0]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 1
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithSymmetricPad_NHWC_FP16(TestCUDNN_FP16):

    def init_test_case(self):
        self.dtype = np.float16
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithAsymmetricPad_NHWC_FP16(TestCUDNN_FP16):

    def init_test_case(self):
        self.dtype = np.float16
        self.pad = [1, 0, 2, 3]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithStride_NHWC_FP16(TestCUDNN_FP16):

    def init_test_case(self):
        self.dtype = np.float16
        self.pad = [1, 1]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.input_size = [2, 5, 5, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 3, 3]
        self.data_format = 'NHWC'


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithGroups_NHWC_FP16(TestCUDNN_FP16):

    def init_test_case(self):
        self.dtype = np.float16
        self.pad = [1, 1]
        self.stride = [1, 1]
        self.dilations = [1, 1]
        self.groups = 2
        self.input_size = [2, 5, 5, 4]  # NCHW
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 3, 3, 3]
        self.data_format = 'NHWC'


@unittest.skipIf(
    not core.is_compiled_with_cuda(), "core is not compiled with CUDA"
)
class TestCUDNNWithEvenUpsample_NHWC_FP16(TestCUDNN_FP16):

    def init_test_case(self):
        self.dtype = np.float16
        self.pad = [2, 2]
        self.stride = [2, 2]
        self.groups = 1
        self.dilations = [1, 1]
        self.output_size = [14, 14]
        self.input_size = [2, 7, 7, 3]  # NHWC
        f_c = self.input_size[-1]
        self.filter_size = [f_c, 6, 5, 5]
        self.data_format = 'NHWC'


class TestConv2DTransposeAPI(unittest.TestCase):

    def test_case1(self):
<<<<<<< HEAD
        data1 = fluid.layers.data(name='data1',
                                  shape=[3, 5, 5],
                                  dtype='float32')
        data2 = fluid.layers.data(name='data2',
                                  shape=[5, 5, 3],
                                  dtype='float32')
        out1 = fluid.layers.conv2d_transpose(input=data1,
                                             groups=1,
                                             num_filters=6,
                                             filter_size=3,
                                             data_format='NCHW')
        out2 = fluid.layers.conv2d_transpose(input=data2,
                                             groups=1,
                                             num_filters=6,
                                             filter_size=3,
                                             data_format='NHWC')
        out3 = fluid.layers.conv2d_transpose(input=data1,
                                             groups=1,
                                             num_filters=6,
                                             filter_size=3,
                                             padding=[[0, 0], [1, 1], [1, 1],
                                                      [0, 0]],
                                             data_format='NHWC')
        out4 = fluid.layers.conv2d_transpose(input=data1,
                                             groups=3,
                                             num_filters=6,
                                             filter_size=3,
                                             padding=[[0, 0], [0, 0], [2, 1],
                                                      [0, 0]],
                                             data_format='NCHW')
        out5 = fluid.layers.conv2d_transpose(input=data2,
                                             groups=1,
                                             num_filters=6,
                                             filter_size=3,
                                             padding='SAME',
                                             data_format='NCHW')
        out6 = fluid.layers.conv2d_transpose(input=data1,
                                             groups=1,
                                             num_filters=6,
                                             filter_size=3,
                                             padding='VALID',
                                             data_format='NHWC')
        out7 = fluid.layers.conv2d_transpose(input=data1,
                                             groups=1,
                                             num_filters=6,
                                             output_size=[7, 7],
                                             padding=[0, 0],
                                             data_format='NHWC')
=======
        data1 = fluid.layers.data(
            name='data1', shape=[3, 5, 5], dtype='float32'
        )
        data2 = fluid.layers.data(
            name='data2', shape=[5, 5, 3], dtype='float32'
        )
        out1 = paddle.static.nn.conv2d_transpose(
            input=data1,
            groups=1,
            num_filters=6,
            filter_size=3,
            data_format='NCHW',
        )
        out2 = paddle.static.nn.conv2d_transpose(
            input=data2,
            groups=1,
            num_filters=6,
            filter_size=3,
            data_format='NHWC',
        )
        out3 = paddle.static.nn.conv2d_transpose(
            input=data1,
            groups=1,
            num_filters=6,
            filter_size=3,
            padding=[[0, 0], [1, 1], [1, 1], [0, 0]],
            data_format='NHWC',
        )
        out4 = paddle.static.nn.conv2d_transpose(
            input=data1,
            groups=3,
            num_filters=6,
            filter_size=3,
            padding=[[0, 0], [0, 0], [2, 1], [0, 0]],
            data_format='NCHW',
        )
        out5 = paddle.static.nn.conv2d_transpose(
            input=data2,
            groups=1,
            num_filters=6,
            filter_size=3,
            padding='SAME',
            data_format='NCHW',
        )
        out6 = paddle.static.nn.conv2d_transpose(
            input=data1,
            groups=1,
            num_filters=6,
            filter_size=3,
            padding='VALID',
            data_format='NHWC',
        )
        out7 = paddle.static.nn.conv2d_transpose(
            input=data1,
            groups=1,
            num_filters=6,
            output_size=[7, 7],
            padding=[0, 0],
            data_format='NHWC',
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        data1_np = np.random.random((2, 3, 5, 5)).astype("float32")
        data2_np = np.random.random((2, 5, 5, 3)).astype("float32")

        if core.is_compiled_with_cuda():
            place = core.CUDAPlace(0)
        else:
            place = core.CPUPlace()
        exe = fluid.Executor(place)
        exe.run(fluid.default_startup_program())
<<<<<<< HEAD
        results = exe.run(fluid.default_main_program(),
                          feed={
                              "data1": data1_np,
                              "data2": data2_np
                          },
                          fetch_list=[out1, out2, out3, out4, out5, out6, out7],
                          return_numpy=True)
=======
        results = exe.run(
            fluid.default_main_program(),
            feed={"data1": data1_np, "data2": data2_np},
            fetch_list=[out1, out2, out3, out4, out5, out6, out7],
            return_numpy=True,
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        self.assertIsNotNone(results[0])
        self.assertIsNotNone(results[1])
        self.assertIsNotNone(results[2])
        self.assertIsNotNone(results[3])
        self.assertIsNotNone(results[4])
        self.assertIsNotNone(results[5])
        self.assertIsNotNone(results[6])


class TestConv2DTransposeOpException(unittest.TestCase):

    def test_exception(self):
        data = fluid.layers.data(name='data', shape=[3, 5, 5], dtype="float32")

        def attr_data_format():
<<<<<<< HEAD
            out = fluid.layers.conv2d_transpose(input=data,
                                                groups=1,
                                                num_filters=6,
                                                filter_size=3,
                                                data_format="NCDHW")
=======
            out = paddle.static.nn.conv2d_transpose(
                input=data,
                groups=1,
                num_filters=6,
                filter_size=3,
                data_format="NCDHW",
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        self.assertRaises(ValueError, attr_data_format)

        def attr_padding_str():
<<<<<<< HEAD
            out = fluid.layers.conv2d_transpose(input=data,
                                                groups=1,
                                                num_filters=6,
                                                filter_size=3,
                                                padding='Vald')
=======
            out = paddle.static.nn.conv2d_transpose(
                input=data,
                groups=1,
                num_filters=6,
                filter_size=3,
                padding='Vald',
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        self.assertRaises(ValueError, attr_padding_str)

        def attr_padding_list():
<<<<<<< HEAD
            out = fluid.layers.conv2d_transpose(input=data,
                                                groups=1,
                                                num_filters=6,
                                                filter_size=3,
                                                padding=[[1, 1], [1, 1], [0, 0],
                                                         [0, 0]])
=======
            out = paddle.static.nn.conv2d_transpose(
                input=data,
                groups=1,
                num_filters=6,
                filter_size=3,
                padding=[[1, 1], [1, 1], [0, 0], [0, 0]],
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        self.assertRaises(ValueError, attr_padding_list)

        def attr_padding_with_data_format():
<<<<<<< HEAD
            out = fluid.layers.conv2d_transpose(input=data,
                                                groups=1,
                                                num_filters=6,
                                                filter_size=3,
                                                padding=[[1, 1], [0, 0], [0, 0],
                                                         [1, 1]],
                                                data_format='NHWC')

        self.assertRaises(ValueError, attr_padding_with_data_format)

        error_input = fluid.layers.data(name='error_data',
                                        shape=[1],
                                        dtype="float32")

        def error_input_size():
            out = fluid.layers.conv2d_transpose(input=error_input,
                                                groups=1,
                                                num_filters=6,
                                                filter_size=3)
=======
            out = paddle.static.nn.conv2d_transpose(
                input=data,
                groups=1,
                num_filters=6,
                filter_size=3,
                padding=[[1, 1], [0, 0], [0, 0], [1, 1]],
                data_format='NHWC',
            )

        self.assertRaises(ValueError, attr_padding_with_data_format)

        error_input = fluid.layers.data(
            name='error_data', shape=[1], dtype="float32"
        )

        def error_input_size():
            out = paddle.static.nn.conv2d_transpose(
                input=error_input, groups=1, num_filters=6, filter_size=3
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        self.assertRaises(ValueError, error_input_size)

        def error_groups():
<<<<<<< HEAD
            out = fluid.layers.conv2d_transpose(input=data,
                                                groups=0,
                                                num_filters=6,
                                                filter_size=3,
                                                data_format='NHWC')
=======
            out = paddle.static.nn.conv2d_transpose(
                input=data,
                groups=0,
                num_filters=6,
                filter_size=3,
                data_format='NHWC',
            )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

        self.assertRaises(ValueError, error_groups)


class TestConv2DTransposeRepr(unittest.TestCase):

    def test_case(self):
        paddle.disable_static()
        x_var = paddle.uniform((2, 4, 8, 8), dtype='float32', min=-1.0, max=1.0)
        conv = nn.Conv2DTranspose(4, 6, (3, 3), output_padding=1, stride=2)
        print(conv)
        y_var = conv(x_var)
        y_np = y_var.numpy()
        self.assertIsNotNone(y_np)
        paddle.enable_static()


class TestTensorOutputSize1(UnittestBase):
    def init_info(self):
        self.shapes = [[2, 3, 8, 8]]
        self.save_path = os.path.join(self.temp_dir.name, self.path_prefix())

    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size1'

    def var_prefix(self):
        return "Vars["

    def call_func(self, x):
        w_var = paddle.randn((3, 6, 3, 3), dtype='float32')
        output_size = paddle.assign([17])
        out = paddle.paddle.nn.functional.conv2d_transpose(
            x, w_var, stride=2, output_size=output_size
        )
        return out

    def test_static(self):
        main_prog = Program()
        starup_prog = Program()
        with program_guard(main_prog, starup_prog):
            fc = paddle.nn.Linear(8, 8)
            x = paddle.randn([2, 3, 8, 8])
            x.stop_gradient = False
            feat = fc(x)
            out = self.call_func(feat)

            sgd = paddle.optimizer.SGD()
            sgd.minimize(paddle.mean(out))
            self.assertTrue(self.var_prefix() in str(main_prog))

            exe = paddle.static.Executor()
            exe.run(starup_prog)
            res = exe.run(fetch_list=[feat, out])
            np.testing.assert_allclose(res[1].shape, (2, 6, 17, 17))

            paddle.static.save_inference_model(
                self.save_path, [x], [feat, out], exe
            )
            # Test for Inference Predictor
            infer_outs = self.infer_prog()
            np.testing.assert_allclose(infer_outs[1].shape, (2, 6, 17, 17))


class TestTensorOutputSize2(TestTensorOutputSize1):
    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size2'

    def call_func(self, x):
        w_var = paddle.randn((3, 6, 3, 3), dtype='float32')
        output_size = [17, paddle.assign([17])]
        out = paddle.paddle.nn.functional.conv2d_transpose(
            x, w_var, stride=2, output_size=output_size
        )
        return out


class TestTensorOutputSize3(TestTensorOutputSize1):
    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size3'

    def call_func(self, x):
        w_var = paddle.randn((3, 6, 3, 3), dtype='float32')
        output_size = paddle.assign([17])
        out = paddle.static.nn.conv2d_transpose(
            x, num_filters=6, output_size=output_size, filter_size=3, stride=2
        )
        return out


class TestTensorOutputSize4(TestTensorOutputSize1):
    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size4'

    def call_func(self, x):
        output_size = [17, paddle.assign([17])]
        out = paddle.static.nn.conv2d_transpose(
            x, num_filters=6, output_size=output_size, filter_size=3, stride=2
        )
        return out


class TestTensorOutputSize5(TestTensorOutputSize1):
    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size5'

    def call_func(self, x):
        w_var = paddle.randn((3, 6, 3, 3), dtype='float32')
        output_size = [17, paddle.assign([17])]
        conv2d_trans = paddle.fluid.dygraph.Conv2DTranspose(
            num_channels=3,
            num_filters=6,
            filter_size=3,
            output_size=output_size,
            stride=2,
        )
        out = conv2d_trans(x)
        return out


class TestTensorOutputSize6(TestTensorOutputSize1):
    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size6'

    def var_prefix(self):
        return "Var["

    def call_func(self, x):
        w_var = paddle.randn((3, 6, 3, 3), dtype='float32')
        output_size = paddle.assign([17, 17])
        conv2d_trans = paddle.fluid.dygraph.Conv2DTranspose(
            num_channels=3,
            num_filters=6,
            filter_size=3,
            output_size=output_size,
            stride=2,
        )
        out = conv2d_trans(x)
        return out


class TestTensorOutputSize7(TestTensorOutputSize1):
    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size7'

    def var_prefix(self):
        return ""

    def call_func(self, x):
        w_var = paddle.randn((3, 6, 3, 3), dtype='float32')
        output_size = 17
        conv2d_trans = paddle.fluid.dygraph.Conv2DTranspose(
            num_channels=3,
            num_filters=6,
            filter_size=3,
            output_size=output_size,
            stride=2,
        )
        out = conv2d_trans(x)
        return out


class TestTensorOutputSize8(TestTensorOutputSize1):
    def path_prefix(self):
        return 'conv2d_transpose_tensor_output_size8'

    def var_prefix(self):
        return ""

    def call_func(self, x):
        w_var = paddle.randn((3, 6, 3, 3), dtype='float32')
        output_size = [17, 17]
        conv2d_trans = paddle.fluid.dygraph.Conv2DTranspose(
            num_channels=3,
            num_filters=6,
            filter_size=3,
            output_size=output_size,
            stride=2,
        )
        out = conv2d_trans(x)
        return out


if __name__ == '__main__':
    unittest.main()
