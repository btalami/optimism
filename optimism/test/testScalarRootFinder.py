from sys import float_info
from scipy.optimize import minimize_scalar, root_scalar # for comparison
from scipy.optimize import OptimizeResult

from optimism.JaxConfig import *
from optimism import ScalarRootFind
from optimism.test import TestFixture


def f(x): return x**3 - 4.0


class RtsafeFixture(TestFixture.TestFixture):

    def setUp(self):
        self.settings = ScalarRootFind.get_settings()

        self.rootGuess = 1e-5
        self.rootExpected = np.cbrt(4.0)


        # this shows that a scipy root finder takes longer
        # sp_opts = {'xtol': self.settings.x_tol, 'maxiter': self.settings.max_iters}
        # result = root_scalar(f, method='brentq', bracket=self.rootBracket)
        # self.scipy_function_calls = result.function_calls
        # self.scipy_iterations = result.iterations
        # print('scipy root ', result.root)
        # print('scipy fevals ', result.function_calls)
        # print('scipy iterations ', result.iterations)
        

    def test_rtsafe(self):
        rootBracket = np.array([float_info.epsilon, 100.0])
        root = ScalarRootFind.rtsafe(f, self.rootGuess, rootBracket, self.settings)
        self.assertNear(root, self.rootExpected, 13)

        
    def test_rtsafe_jits(self):
        rtsafe_jit = jit(ScalarRootFind.rtsafe, static_argnums=(0,3))
        rootBracket = np.array([float_info.epsilon, 100.0])
        root = rtsafe_jit(f, self.rootGuess, rootBracket, self.settings)
        self.assertNear(root, self.rootExpected, 13)


    def test_unbracketed_root_gives_nan(self):
        rootBracket = np.array([2.0, 100.0])
        root = ScalarRootFind.rtsafe(f, self.rootGuess, rootBracket, self.settings)
        self.assertTrue(np.isnan(root))

        
    def test_converged_with_terrible_guess(self):
        rootBracket = np.array([float_info.epsilon, 200.0])
        root = ScalarRootFind.rtsafe(f, 199.0, rootBracket, self.settings)
        self.assertNear(root, self.rootExpected, 13)

        
if __name__ == '__main__':
    TestFixture.unittest.main()
