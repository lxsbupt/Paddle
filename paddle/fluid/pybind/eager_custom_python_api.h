// Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#pragma once

#include <iostream>

<<<<<<< HEAD
#include "paddle/fluid/eager/to_static/run_program_op_func.h"
=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
#include "paddle/phi/core/enforce.h"

namespace paddle {
namespace pybind {
<<<<<<< HEAD

static PyObject *eager_api_run_program(PyObject *self,
                                       PyObject *args,
                                       PyObject *kwargs) {
  PyThreadState *tstate = nullptr;
  try {
    auto X = GetTensorListFromArgs("run_program", "X", args, 0, false);
    auto Params = GetTensorListFromArgs("run_program", "Params", args, 1, true);
    auto Out = GetTensorPtrListFromArgs("run_program", "Out", args, 2, false);
    auto OutScope =
        GetScopePtrListFromArgs("run_program", "OutScope", args, 3, false);
    auto DOut = GetTensorPtrListFromArgs("run_program", "DOut", args, 4, true);
    framework::AttributeMap attrs;
    // TODO(zengjinle): support CUDA Graph on eager mode
    ConstructAttrMapFromPyArgs(
        "run_program", args, 6, PyTuple_GET_SIZE(args), attrs);

    tstate = PyEval_SaveThread();
    run_program_dygraph_function(X, Params, Out, OutScope, DOut, attrs);
    PyEval_RestoreThread(tstate);
    tstate = nullptr;
    Py_RETURN_NONE;
=======

static PyObject *eager_api_linear(PyObject *self,
                                  PyObject *args,
                                  PyObject *kwargs) {
  PyThreadState *tstate = nullptr;
  try {
    auto x = GetTensorFromArgs("linear", "X", args, 0, false);
    auto weight = GetTensorFromArgs("linear", "weight", args, 1, false);
    auto bias = GetTensorFromArgs("linear", "Bias", args, 2, true);
    tstate = PyEval_SaveThread();
    if (bias.initialized()) {
      auto mm_out = matmul_ad_func(x, weight, false, false);
      auto out = add_ad_func(mm_out, bias);
      PyEval_RestoreThread(tstate);
      tstate = nullptr;
      return ToPyObject(out);
    } else {
      auto mm_out = matmul_ad_func(x, weight, false, false);
      PyEval_RestoreThread(tstate);
      tstate = nullptr;
      return ToPyObject(mm_out);
    }
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
  } catch (paddle::platform::EnforceNotMet &exception) {
    if (tstate) {
      PyEval_RestoreThread(tstate);
    }
    std::ostringstream sout;
    sout << exception.what();
<<<<<<< HEAD
    sout << "  [operator < run_program > error]";
=======
    sout << "  [operator < linear > error]";
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    exception.set_error_str(sout.str());
    ThrowExceptionToPython(std::current_exception());
    return nullptr;
  } catch (...) {
    if (tstate) {
      PyEval_RestoreThread(tstate);
    }
    ThrowExceptionToPython(std::current_exception());
    return nullptr;
  }
}

<<<<<<< HEAD
static PyMethodDef CustomEagerMethods[] = {
    {"run_program",
     (PyCFunction)(void (*)(void))eager_api_run_program,
=======
static PyMethodDef CustomEagerFinalStateMethods[] = {
    {"linear",
     (PyCFunction)(void (*)(void))eager_api_linear,
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
     METH_VARARGS | METH_KEYWORDS,
     "C++ interface function for run_program in dygraph."},
    {nullptr, nullptr, 0, nullptr}};

}  // namespace pybind
}  // namespace paddle
