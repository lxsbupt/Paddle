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

import unittest

import numpy as np
import paddle
import scipy.special
import scipy.stats
from paddle.distribution import kl

import config
import mock_data as mock
import parameterize as param

np.random.seed(2022)
paddle.seed(2022)
paddle.set_default_dtype('float64')


@param.place(config.DEVICES)
<<<<<<< HEAD
@param.parameterize_cls((param.TEST_CASE_NAME, 'a1', 'b1', 'a2', 'b2'), [
    ('test_regular_input', 6.0 * np.random.random(
        (4, 5)) + 1e-4, 6.0 * np.random.random(
            (4, 5)) + 1e-4, 6.0 * np.random.random(
                (4, 5)) + 1e-4, 6.0 * np.random.random((4, 5)) + 1e-4),
])
=======
@param.parameterize_cls(
    (param.TEST_CASE_NAME, 'a1', 'b1', 'a2', 'b2'),
    [
        (
            'test_regular_input',
            6.0 * np.random.random((4, 5)) + 1e-4,
            6.0 * np.random.random((4, 5)) + 1e-4,
            6.0 * np.random.random((4, 5)) + 1e-4,
            6.0 * np.random.random((4, 5)) + 1e-4,
        ),
    ],
)
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
class TestKLBetaBeta(unittest.TestCase):

    def setUp(self):
<<<<<<< HEAD
        self.p = paddle.distribution.Beta(paddle.to_tensor(self.a1),
                                          paddle.to_tensor(self.b1))
        self.q = paddle.distribution.Beta(paddle.to_tensor(self.a2),
                                          paddle.to_tensor(self.b2))
=======
        self.p = paddle.distribution.Beta(
            paddle.to_tensor(self.a1), paddle.to_tensor(self.b1)
        )
        self.q = paddle.distribution.Beta(
            paddle.to_tensor(self.a2), paddle.to_tensor(self.b2)
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f

    def test_kl_divergence(self):
        with paddle.fluid.dygraph.guard(self.place):
            np.testing.assert_allclose(
                paddle.distribution.kl_divergence(self.p, self.q),
                self.scipy_kl_beta_beta(self.a1, self.b1, self.a2, self.b2),
                rtol=config.RTOL.get(str(self.a1.dtype)),
                atol=config.ATOL.get(str(self.a1.dtype)),
            )

    def scipy_kl_beta_beta(self, a1, b1, a2, b2):
        return (
            scipy.special.betaln(a2, b2)
            - scipy.special.betaln(a1, b1)
            + (a1 - a2) * scipy.special.digamma(a1)
            + (b1 - b2) * scipy.special.digamma(b1)
            + (a2 - a1 + b2 - b1) * scipy.special.digamma(a1 + b1)
        )


@param.place(config.DEVICES)
<<<<<<< HEAD
@param.param_cls((param.TEST_CASE_NAME, 'conc1', 'conc2'), [
    ('test-regular-input', np.random.random(
        (5, 7, 8, 10)), np.random.random((5, 7, 8, 10))),
])
=======
@param.param_cls(
    (param.TEST_CASE_NAME, 'conc1', 'conc2'),
    [
        (
            'test-regular-input',
            np.random.random((5, 7, 8, 10)),
            np.random.random((5, 7, 8, 10)),
        ),
    ],
)
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
class TestKLDirichletDirichlet(unittest.TestCase):

    def setUp(self):
        self.p = paddle.distribution.Dirichlet(paddle.to_tensor(self.conc1))
        self.q = paddle.distribution.Dirichlet(paddle.to_tensor(self.conc2))

    def test_kl_divergence(self):
        with paddle.fluid.dygraph.guard(self.place):
            np.testing.assert_allclose(
                paddle.distribution.kl_divergence(self.p, self.q),
                self.scipy_kl_diric_diric(self.conc1, self.conc2),
                rtol=config.RTOL.get(str(self.conc1.dtype)),
                atol=config.ATOL.get(str(self.conc1.dtype)),
            )

    def scipy_kl_diric_diric(self, conc1, conc2):
        return (
<<<<<<< HEAD
            scipy.special.gammaln(np.sum(conc1, -1)) -
            scipy.special.gammaln(np.sum(conc2, -1)) - np.sum(
                scipy.special.gammaln(conc1) - scipy.special.gammaln(conc2), -1)
            + np.sum(
                (conc1 - conc2) *
                (scipy.special.digamma(conc1) -
                 scipy.special.digamma(np.sum(conc1, -1, keepdims=True))), -1))
=======
            scipy.special.gammaln(np.sum(conc1, -1))
            - scipy.special.gammaln(np.sum(conc2, -1))
            - np.sum(
                scipy.special.gammaln(conc1) - scipy.special.gammaln(conc2), -1
            )
            + np.sum(
                (conc1 - conc2)
                * (
                    scipy.special.digamma(conc1)
                    - scipy.special.digamma(np.sum(conc1, -1, keepdims=True))
                ),
                -1,
            )
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f


class DummyDistribution(paddle.distribution.Distribution):
    pass


@param.place(config.DEVICES)
@param.param_cls(
    (param.TEST_CASE_NAME, 'p', 'q'),
    [('test-unregister', DummyDistribution(), DummyDistribution)],
)
class TestDispatch(unittest.TestCase):

    def test_dispatch_with_unregister(self):
        with self.assertRaises(NotImplementedError):
            paddle.distribution.kl_divergence(self.p, self.q)


@param.place(config.DEVICES)
@param.param_cls(
    (param.TEST_CASE_NAME, 'p', 'q'),
<<<<<<< HEAD
    [('test-diff-dist', mock.Exponential(paddle.rand((100, 200, 100)) + 1.0),
      mock.Exponential(paddle.rand((100, 200, 100)) + 2.0)),
     ('test-same-dist', mock.Exponential(
         paddle.to_tensor(1.0)), mock.Exponential(paddle.to_tensor(1.0)))])
=======
    [
        (
            'test-diff-dist',
            mock.Exponential(paddle.rand((100, 200, 100)) + 1.0),
            mock.Exponential(paddle.rand((100, 200, 100)) + 2.0),
        ),
        (
            'test-same-dist',
            mock.Exponential(paddle.to_tensor(1.0)),
            mock.Exponential(paddle.to_tensor(1.0)),
        ),
    ],
)
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
class TestKLExpfamilyExpFamily(unittest.TestCase):

    def test_kl_expfamily_expfamily(self):
<<<<<<< HEAD
        np.testing.assert_allclose(paddle.distribution.kl_divergence(
            self.p, self.q),
                                   kl._kl_expfamily_expfamily(self.p, self.q),
                                   rtol=config.RTOL.get(config.DEFAULT_DTYPE),
                                   atol=config.ATOL.get(config.DEFAULT_DTYPE))
=======
        np.testing.assert_allclose(
            paddle.distribution.kl_divergence(self.p, self.q),
            kl._kl_expfamily_expfamily(self.p, self.q),
            rtol=config.RTOL.get(config.DEFAULT_DTYPE),
            atol=config.ATOL.get(config.DEFAULT_DTYPE),
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f


if __name__ == '__main__':
    unittest.main()
