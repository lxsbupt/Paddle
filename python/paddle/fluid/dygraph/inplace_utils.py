#   Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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

from ..wrapped_decorator import wrap_decorator
from ..framework import _non_static_mode
import warnings
import paddle
from paddle import _C_ops, _legacy_C_ops


# NOTE(pangyoki): The Inplace APIs with underline(`_`) is only valid for the method of calling `_C_ops`
# in dygraph mode. If static mode is used, the inplace mechanism will not be used, and the static method
# of the original API will be called.
def _inplace_apis_in_dygraph_only_(func):

    def __impl__(*args, **kwargs):
        if not _non_static_mode():
            origin_api_name = func.__name__[:-1]
            warnings.warn(
<<<<<<< HEAD
                "In static mode, {}() is the same as {}() and does not perform inplace operation.".format(
                    func.__name__, origin_api_name
                )
            )
=======
                "In static mode, {}() is the same as {}() and does not perform inplace operation."
                .format(func.__name__, origin_api_name))
>>>>>>> e170b253fc2cfc81aeb39c17a0fffc8e08311f1e
            origin_func = "{}.{}".format(func.__module__, origin_api_name)
            return eval(origin_func)(*args, **kwargs)
        return func(*args, **kwargs)

    return __impl__


inplace_apis_in_dygraph_only = wrap_decorator(_inplace_apis_in_dygraph_only_)
