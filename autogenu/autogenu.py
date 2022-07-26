import linecache
import subprocess
import platform
from enum import Enum, auto

import sympy

from autogenu import symbolic_functions as symfunc


class SolverType(Enum):
    ContinuationGMRES = auto()
    MultipleShootingCGMRES = auto()
    MSCGMRESWithInputSaturation = auto()

class AutoGenU(object):
    """ Automatic C++ code generator for the C/GMRES methods. 

        Args: 
            model_name: The name of the NMPC model. The directory having this 
                name is made and C++ source files are generated in the 
                directory.
            dimx: The dimension of the state of the NMPC model. 
            dimu: The dimension of the control input of the NMPC model. 
    """
    def __init__(self, model_name, dimx, dimu):
        assert isinstance(model_name, str), 'The frst argument must be strings!'
        assert dimx > 0, 'The second argument must be positive integer!'
        assert dimu > 0, 'The third argument must be positive integer!'
        self.__model_name = model_name
        self.__dimx = dimx        
        self.__dimu = dimu        
        self.__scalar_vars = []
        self.__array_vars = []
        self.__saturation_list = []
        self.__is_function_set = False
        self.__is_solver_type_set = False
        self.__is_solver_paramters_set = False
        self.__is_initialization_set = False
        self.__is_simulation_set = False
        self.__is_FB_epsilon_set = False

    def define_t(self):
        """ Returns symbolic scalar variable 't'.
        """
        return sympy.Symbol('t')

    def define_x(self):
        """ Returns symbolic vector variable 'x' whose size is dimx.
        """
        return sympy.symbols('x[0:%d]' %(self.__dimx))

    def define_u(self):
        """ Returns symbolic vector variable 'u' whose size is dimu.
        """
        return sympy.symbols('u[0:%d]' %(self.__dimu))

    def define_scalar_var(self, scalar_var_name):
        """ Returns symbolic variable whose name is scalar_var_name. The name of 
            the variable is memorized.

            Args:
                scalar_var_name: Name of the scalar variable.
        """
        assert isinstance(scalar_var_name, str), 'The input must be strings!'
        scalar_var = sympy.Symbol(scalar_var_name)
        self.__scalar_vars.append([scalar_var, scalar_var_name, 0])
        return scalar_var

    def define_scalar_vars(self, *scalar_var_name_list):
        """ Returns symbolic variables whose names are given by 
            scalar_var_name_list. The names of the variables are memorized.

            Args:
                scalar_var_name_list: Names of the scalar variables.
        """
        scalar_vars = []
        for scalar_var_name in scalar_var_name_list:
            assert isinstance(scalar_var_name, str), 'The input must be list of strings!'
            scalar_var = sympy.Symbol(scalar_var_name)
            self.__scalar_vars.append([scalar_var, scalar_var_name, 0])
            scalar_vars.append(scalar_var)
        return scalar_vars

    def define_array_var(self, array_var_name, dim):
        """ Returns symbolic vector variable whose names is array_var_name and 
            whose dimension is dim. The names of the variable is memorized.

            Args:
                array_var_name: Name of the array variable.
                dim: Dimension of the array variable.
        """
        assert isinstance(array_var_name, str), 'The first argument must be strings!'
        assert dim > 0, 'The second argument must be positive integer!'
        array_var = sympy.symbols(array_var_name+'[0:%d]' %(dim))
        self.__array_vars.append([array_var, array_var_name, []])
        return array_var

    def set_FB_epsilon(self, FB_epsilon):
        """ Set reguralization term of the semi-smooth Fischer-Burumeister (FB) 
            method. Set the array whose size is dimension of the inequality 
            constraints considered by semi-smooth FB method.

            Args:
                FB epsilon: Array of the reguralization term. 
        """
        for eps in FB_epsilon:
            assert eps >= 0, "FB epsilon must be non-negative!"
        self.__FB_epsilon = FB_epsilon
        self.__is_FB_epsilon_set = True

    def set_scalar_var(self, scalar_var_name, scalar_value):
        """ Set the value of the scalar variable you defied. 

            Args:
                scalar_var_name: Name of the scalar variable.
                scalar_value: Value of the scalar variable.
        """
        assert isinstance(scalar_var_name, str), 'The first argument must be strings!'
        for defined_scalar_var in self.__scalar_vars:
            if scalar_var_name[0] == defined_scalar_var[1]:
                defined_scalar_var[2] = scalar_value

    def set_scalar_vars(self, *scalar_var_name_and_value_list):
        """ Set the values of the scalar variables you defied. 

            Args:
                scalar_var_name_and_value_lis: A list composed of the name of 
                the scalar variable and value of the scalar variable.
        """
        for var_name_and_value in scalar_var_name_and_value_list:
            for defined_scalar_var in self.__scalar_vars:
                if var_name_and_value[0] == defined_scalar_var[1]:
                    defined_scalar_var[2] = var_name_and_value[1]
    
    def set_array_var(self, var_name, values):
        """ Set the value of the array variable you defied. 

            Args:
                var_name: Name of the arrray variable.
                values: Values of the arry variable. The size must be the 
                    dimension of the array variable.
        """
        assert isinstance(var_name, str), 'The first argument must be strings!'
        for defined_array_var in self.__array_vars:
            if var_name == defined_array_var[1]:
                if len(defined_array_var[0]) == len(values):
                    defined_array_var[2] = values

    def set_functions(self, f, C, h, L, phi):
        """ Sets functions that defines the optimal control problem.

            Args: 
                f: The state equation. The dimension must be dimx.
                C: The equality consrtaints. If there are no equality 
                    constraints, set the empty list.
                h: The inequality consrtaints considered by semi-smooth 
                    Fischer-Burumeister method. If there are no such inequality 
                    constraints, set the empty list.
                L: The stage cost.
                phi: The terminal cost.
        """
        assert len(f) > 0 
        assert len(f) == self.__dimx, "Dimension of f must be dimx!"
        self.__f = f
        self.__dimc = len(C)
        self.__dimh = len(h)
        x = sympy.symbols('x[0:%d]' %(self.__dimx))
        u = sympy.symbols('u[0:%d]' %(self.__dimu+self.__dimc+self.__dimh))
        lmd = sympy.symbols('lmd[0:%d]' %(self.__dimx))
        hamiltonian = L + sum(lmd[i] * f[i] for i in range(self.__dimx))
        hamiltonian += sum(u[self.__dimu+i] * C[i] for i in range(self.__dimc))
        dimuc = self.__dimu + self.__dimc
        hamiltonian += sum(u[dimuc+i] * h[i] for i in range(self.__dimh))
        self.__hx = symfunc.diff_scalar_func(hamiltonian, x)
        self.__hu = symfunc.diff_scalar_func(hamiltonian, u)
        fb_eps = sympy.symbols('fb_eps[0:%d]' %(self.__dimh))
        for i in range(self.__dimh):
            self.__hu[dimuc+i] = sympy.sqrt(u[dimuc+i]**2 + h[i]**2 + fb_eps[i]) - (u[dimuc+i] - h[i])
        self.__phix = symfunc.diff_scalar_func(phi, x)
        self.__is_function_set = True

    def set_solver_type(self, solver_type):
        """ Sets solver types of the C/GMRES methods. 

            Args: 
                solver_type: The solver type. Choose from 
                SolverType.ContinuationGMRES, SolverType.MultipleShootingCGMRES, 
                and SolverType.MSCGMRESWithInputSaturation.
        """
        assert (
            solver_type == SolverType.ContinuationGMRES or 
            solver_type == SolverType.MultipleShootingCGMRES or
            solver_type == SolverType.MSCGMRESWithInputSaturation
        )
        self.__solver_type = solver_type
        self.__is_solver_type_set = True

    def set_solver_parameters(
            self, T_f, alpha, N, finite_difference_increment, zeta, kmax
        ):
        """ Sets parameters of the NMPC solvers based on the C/GMRES method. 

            Args: 
                T_f, alpha: Parameter about the length of the horizon of NMPC.
                    The length of the horzion at time t is given by 
                    T_f * (1-exp(-alpha*t)).
                N: The number of the grid for the discretization
                    of the horizon of NMPC.
                finite_difference_increment: The small positive value for 
                    finitei difference approximation used in the FD-GMRES. 
                zeta: A stabilization parameter of the C/GMRES method. It may 
                    work well if you set as zeta=1/sampling_period.
                kmax: Maximam number of the iteration of the Krylov 
                    subspace method for the linear problem. 
        """
        assert T_f > 0
        assert alpha > 0
        assert N > 0
        assert finite_difference_increment > 0
        assert zeta > 0
        assert kmax > 0
        self.__T_f = T_f
        self.__alpha = alpha
        self.__N = N
        self.__finite_difference_increment = finite_difference_increment
        self.__zeta = zeta
        self.__kmax = kmax
        self.__is_solver_paramters_set = True

    def set_initialization_parameters(
            self, solution_initial_guess, newton_residual_torelance, 
            max_newton_iteration, initial_Lagrange_multiplier=None
        ):
        """ Set parameters for the initialization of the C/GMRES solvers. 

            Args: 
                solution_initial_guess: The initial guess of the solution of the 
                    initialization. Size must be the dimu + dimensions of C and 
                    h.
                newton_residual_torelance: The residual torelance of the 
                    initialization solved by Newton's method. The Newton 
                    iteration terminates if the optimality error is smaller than 
                    this value.
                max_newton_iteration: The maximum number of the Newton iteration. 
                initial_Lagranme_multiplier: Optional parameter is you use 
                    MSCGMRESWithInputSaturation. The initial guess of the 
                    Lagrange multiplier with respect to the box constraint on 
                    the control input that is condensed.
        """
        dimuch = self.__dimu + self.__dimc + self.__dimh
        assert len(solution_initial_guess) == dimuch
        assert newton_residual_torelance > 0
        assert max_newton_iteration > 0
        self.__solution_initial_guess = solution_initial_guess 
        self.__newton_residual_torelance = newton_residual_torelance 
        self.__max_newton_iteration = max_newton_iteration 
        if initial_Lagrange_multiplier is not None:
            self.__initial_Lagrange_multiplier = initial_Lagrange_multiplier 
        self.__is_initialization_set = True

    def set_simulation_parameters(
            self, initial_time, initial_state, simulation_time, sampling_time
        ):
        """ Set parameters for numerical simulation. 

            Args: 
                initial_time: The time parameter at the beginning of the 
                    simulation. 
                initial_state: The state of the system at the beginning of the 
                    simulation. 
                simulation_time: The length of the numerical simulation. 
                sampling_time: The sampling period of the numerical simulation. 
        """
        assert len(initial_state) == self.__dimx, "The dimension of initial_state must be dimx!"
        assert simulation_time > 0
        assert sampling_time > 0
        self.__initial_time = initial_time 
        self.__initial_state = initial_state
        self.__simulation_time = simulation_time 
        self.__sampling_time = sampling_time
        self.__is_simulation_set = True

    def add_control_input_saturation(
        self, index, u_min, u_max, dummy_weight, quadratic_weight
        ):
        """ Adds the bax constraints on the control input that is condensed in 
            linear problem. 

            Args: 
                index: The index of the constrianed control input. 
                u_min: The minimum value of the constrianed control input. 
                u_max: The minimum value of the constrianed control input. 
                dummy_weight: An weight to stabilize the numerical computation.
                quadratic_weight: Weight on the constrainted control input in 
                    the dummy input in the cost function. The larger this value, 
                    the larger mergin of constraint.
        """
        assert index >= 0
        assert index < self.__dimu
        assert u_min < u_max
        assert dummy_weight >= 0 
        assert quadratic_weight >= 0 
        find_same_index = False
        for saturation in self.__saturation_list:
            if saturation[0] == index:
                find_same_index = True
                saturation[1] = u_min
                saturation[2] = u_max
                saturation[3] = dummy_weight
                saturation[4] = quadratic_weight
        if not find_same_index:
            saturation = [index, u_min, u_max, dummy_weight, quadratic_weight]
            self.__saturation_list.append(saturation)

    def generate_source_files(self, use_simplification=False, use_cse=False):
        """ Generates the C++ source file in which the equations to solve the 
            optimal control problem are described. Before call this method, 
            set_functions() must be called.

            Args: 
                use_simplification: The flag for simplification. If True, the 
                    Symbolic functions are simplified. Default is False.
                use_cse: The flag for common subexpression elimination. If True, 
                    common subexpressions are eliminated. Default is False.
        """
        assert self.__is_function_set, "Symbolic functions are not set!. Before call this method, call set_functions()"
        if self.__dimh > 0:
            assert self.__is_FB_epsilon_set, "FB epsilons are not set!"
            assert len(self.__FB_epsilon) == self.__dimh
        self.__make_model_dir()
        if use_simplification:
            symfunc.simplify(self.__f)
            symfunc.simplify(self.__hx)
            symfunc.simplify(self.__hu)
            symfunc.simplify(self.__phix)
        f_model_h = open('models/'+str(self.__model_name)+'/ocp.hpp', 'w')
        f_model_h.write(
            '#ifndef CGMRES_OCP_'+str(self.__model_name)+'__HPP_ \n'
        )
        f_model_h.write(
            '#define CGMRES_OCP_'+str(self.__model_name)+'__HPP_ \n'
        )
        f_model_h.writelines([
""" 
#define _USE_MATH_DEFINES

#include <cmath>


namespace cgmres {

// This class represents the optimal control problem (OCP)
""" 
        ])
        f_model_h.write(
            'class OCP_'+str(self.__model_name)+' {\n'
        )

        f_model_h.writelines([
""" 
public:
"""
        ])
        f_model_h.write(
            '  static constexpr int nx = '+str(self.__dimx)+';\n'
        )
        f_model_h.write(
            '  static constexpr int nu = '
            +str(self.__dimu)+';\n'
        )
        f_model_h.write(
            '  static constexpr int nc = '
            +str(self.__dimc+self.__dimh)+';\n'
        )
        f_model_h.write(
            '  static constexpr int nuc = nu + nc;\n'
        )
        f_model_h.write('\n')
        f_model_h.write('private: \n')
        f_model_h.writelines([
            '  static constexpr double '+scalar_var[1]+' = '
            +str(scalar_var[2])+';\n' for scalar_var in self.__scalar_vars
        ])
        f_model_h.write('\n')
        for array_var in self.__array_vars:
            f_model_h.write(
                '  double '+array_var[1]+'['+str(len(array_var[0]))+']'+' = {'
            )
            for i in range(len(array_var[0])-1):
                f_model_h.write(str(array_var[2][i])+', ')
            f_model_h.write(str(array_var[2][len(array_var[0])-1])+'};\n')
        if self.__dimh > 0:
            f_model_h.write(
                '  double fb_eps['+str(self.__dimh)+']'+' = {'
            )
            for i in range(self.__dimh-1):
                f_model_h.write(str(self.__FB_epsilon[i])+', ')
            f_model_h.write(str(self.__FB_epsilon[self.__dimh-1])+'};\n')
        f_model_h.writelines([
"""

public:

  // Computes the state equation f(t, x, u).
  // t : time parameter
  // x : state vector
  // u : control input vector
  // f : the value of f(t, x, u)
  void eval_f(const double t, const double* x, const double* u, 
              double* dx) const {
""" 
        ])
        self.__write_function(f_model_h, self.__f, 'dx', use_cse)
        f_model_h.writelines([
""" 
  }

  // Computes the partial derivative of terminal cost with respect to state, 
  // i.e., dphi/dx(t, x).
  // t    : time parameter
  // x    : state vector
  // phix : the value of dphi/dx(t, x)
  void eval_phix(const double t, const double* x, double* phix) const {
""" 
        ])
        self.__write_function(f_model_h, self.__phix, 'phix', use_cse)
        f_model_h.writelines([
""" 
  }

  // Computes the partial derivative of the Hamiltonian with respect to state, 
  // i.e., dH/dx(t, x, u, lmd).
  // t   : time parameter
  // x   : state vector
  // u   : control input vector
  // lmd : the Lagrange multiplier for the state equation
  // hx  : the value of dH/dx(t, x, u, lmd)
  void eval_hx(const double t, const double* x, const double* u, 
               const double* lmd, double* hx) const {
""" 
        ])
        self.__write_function(f_model_h, self.__hx, 'hx', use_cse)
        f_model_h.writelines([
""" 
  }

  // Computes the partial derivative of the Hamiltonian with respect to control 
  // input and the constraints, dH/du(t, x, u, lmd).
  // t   : time parameter
  // x   : state vector
  // u   : control input vector
  // lmd : the Lagrange multiplier for the state equation
  // hu  : the value of dH/du(t, x, u, lmd)
  void eval_hu(const double t, const double* x, const double* u, 
               const double* lmd, double* hu) const {
""" 
        ])
        self.__write_function(f_model_h, self.__hu, 'hu', use_cse)
        f_model_h.writelines([
""" 
  }
};

} // namespace cgmres


#endif // CGMRES_OCP_HPP_
""" 
        ])
        f_model_h.close()


    def generate_main(self):
        """ Generates main.cpp that defines NMPC solver, set parameters for the 
            solver, and run numerical simulation. Befire call this method,
            set_solver_type(), set_solver_parameters(), 
            set_initialization_parameters(), and set_simulation_parameters(),
            must be called!
        """
        assert self.__is_solver_type_set, "Solver type is not set! Before call this method, call set_solver_type()"
        assert self.__is_solver_paramters_set, "Solver parameters are not set! Before call this method, call set_solver_parameters()"
        assert self.__is_initialization_set, "Initialization parameters are not set! Before call this method, call set_initialization_parameters()"
        assert self.__is_simulation_set, "Simulation parameters are not set! Before call this method, call set_simulation_parameters()"
        """ Makes a directory where the C++ source files are generated.
        """
        f_main = open('models/'+str(self.__model_name)+'/main.cpp', 'w')
        f_main.write('#include "ocp.hpp"\n')
        if self.__solver_type == SolverType.ContinuationGMRES:
            f_main.write(
                '#include "cgmres/zero_horizon_ocp_solver.hpp"\n'
                '#include "cgmres/single_shooting_cgmres_solver.hpp"\n'
            )
        elif self.__solver_type == SolverType.MultipleShootingCGMRES:
            f_main.write(
                '#include "cgmres/zero_horizon_ocp_solver.hpp"\n'
                '#include "cgmres/multiple_shooting_cgmres_solver.hpp"\n'
            )
        else:
            return NotImplementedError()
        f_main.write(
            '#include "cgmres/simulator/simulator.hpp"\n'
        )
        f_main.write('#include <string>\n')
        f_main.write(
            '\n'
            'int main() {\n'
            '  // Define the optimal control problem.\n'
            '  cgmres::OCP_'+str(self.__model_name)+' ocp;\n'
            '\n'
        )
        f_main.write(
            '  // Define the horizon.\n'
            '  const double Tf = '+str(self.__T_f)+';\n'
            '  const double alpha = '+str(self.__alpha)+';\n'
            '  cgmres::Horizon horizon(Tf, alpha);\n'
            '\n'
        )
        f_main.write(
            '  // Define the solver settings.\n'
            '  cgmres::SolverSettings settings;\n'
            '  settings.dt = '+str(self.__sampling_time)+'; // sampling period \n'
            '  settings.zeta = '+str(self.__zeta)+';\n'
            '  settings.finite_difference_epsilon = '+str(self.__finite_difference_increment)+';\n'
            '  // For initialization.\n'
            '  settings.max_iter = '+str(self.__max_newton_iteration)+';\n'
            '  settings.opt_error_tol = '+str(self.__newton_residual_torelance)+';\n'
            '\n'
        )
        f_main.write('  // Define the initial time and initial state.\n')
        f_main.write('  const double t0 = '+str(self.__initial_time)+';\n')
        f_main.write(
            '  cgmres::Vector<'+str(len(self.__initial_state))+'> x0;\n'
            +'  x0 << '
        )
        for i in range(len(self.__initial_state)-1):
            f_main.write(str(self.__initial_state[i])+', ')
        f_main.write(str(self.__initial_state[-1])+';\n')
        f_main.write('\n')
        # initial guess for the initialization of the solution
        f_main.write('  // Initialize the solution of the C/GMRES method.\n')
        f_main.write('  constexpr int kmax_init = '+str(min(self.__kmax, len(self.__solution_initial_guess)))+';\n')
        f_main.write(
            '  cgmres::ZeroHorizonOCPSolver<cgmres::OCP_'+self.__model_name+', kmax_init> '
            +'initializer(ocp, settings);\n'
        )
        f_main.write(
            '  cgmres::Vector<' + str(len(self.__solution_initial_guess))+'> uc0;\n'
            +'  uc0 << '
        )
        for i in range(len(self.__solution_initial_guess)-1):
            f_main.write(str(self.__solution_initial_guess[i])+', ')
        f_main.write(str(self.__solution_initial_guess[-1])+';\n')
        f_main.write('  initializer.set_uc(uc0);\n')
        f_main.write('  initializer.solve(t0, x0);\n')
        f_main.write('\n')
        if (self.__solver_type == SolverType.MSCGMRESWithInputSaturation
            and self.__initial_Lagrange_multiplier is not None):
            f_main.write(
                '  // Set the initial guess of the lagrange multiplier '
                'for the condensed constraints with respect to the saturation '
                'on the function of the control input .\n'
                )
            f_main.write(
                '  double initial_guess_lagrange_multiplier['
                +str(len(self.__initial_Lagrange_multiplier))
                +'] = {'
            )
            for i in range(len(self.__initial_Lagrange_multiplier)-1):
                f_main.write(
                    str(self.__initial_Lagrange_multiplier[i])+', '
                )
            f_main.write(
                str(self.__initial_Lagrange_multiplier[-1])+'};\n'
            )
            f_main.write(
                '\n'+'  mpc.setInitialInputSaturationMultiplier'
                +'(initial_guess_lagrange_multiplier);'
                +'\n'
            )

        f_main.write('  // Define the C/GMRES solver.\n')
        f_main.write('  constexpr int N = '+str(self.__N)+';\n')
        f_main.write('  constexpr int kmax = '+str(min(self.__kmax, self.__N*(self.__dimu+self.__dimc)))+';\n')
        if self.__solver_type == SolverType.ContinuationGMRES:
            f_main.write(
                '  cgmres::SingleShootingCGMRESSolver<cgmres::OCP_'+self.__model_name+', N, kmax> mpc(ocp, horizon, settings);\n'
                '  mpc.set_uc(initializer.ucopt());\n'
            )
        elif self.__solver_type == SolverType.MultipleShootingCGMRES:
            f_main.write(
                '  cgmres::MultipleShootingCGMRESSolver<cgmres::OCP_'+self.__model_name+', N, kmax> mpc(ocp, horizon, settings);\n'
                '  mpc.set_uc(initializer.ucopt());\n'
                '  mpc.set_lmd(initializer.lmdopt());\n'
                '  mpc.set_x(x0);\n'
            )
        f_main.write('\n\n')
        f_main.write(
            '  // Perform a numerical simulation.\n'
            '  const double tf = '+str(self.__simulation_time)+';\n'
            '  const double dt = settings.dt;\n'
            '  const std::string save_dir_name("../simulation_result");\n'
            '  cgmres::simulation(ocp, mpc, x0, t0, tf, dt, ' 
            +"save_dir_name"+', "' +self.__model_name +'");\n\n'
            '  return 0;\n'
            '}\n'
        )
        f_main.close()
        f_pybind11 = open('models/'+str(self.__model_name)+'/python/'+str(self.__model_name)+'/ocp.cpp', 'w')
        f_pybind11.writelines([
"""
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>

#include "cgmres/types.hpp"
#include "cgmres/python/ocp.hpp"
#include "ocp.hpp"

#include <iostream>
#include <stdexcept>

namespace cgmres {
namespace python {

namespace py = pybind11;

""" 
        ])
        f_pybind11.write('DEFINE_PYBIND11_MODULE_OCP(OCP_'+str(self.__model_name)+')\n')
        f_pybind11.writelines([
"""

} // namespace python
} // namespace cgmres
""" 
        ])
        f_pybind11.close()
        f_pybind11 = open('models/'+str(self.__model_name)+'/python/'+str(self.__model_name)+'/zero_horizon_ocp_solver.cpp', 'w')
        f_pybind11.writelines([
"""
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>

#include "cgmres/zero_horizon_ocp_solver.hpp"
#include "cgmres/python/zero_horizon_ocp_solver.hpp"
#include "ocp.hpp"

#include <iostream>
#include <stdexcept>

namespace cgmres {
namespace python {

namespace py = pybind11;

""" 
        ])
        f_pybind11.write('constexpr int kmax_init = '+str(min(self.__kmax, self.__dimc+self.__dimu+self.__dimh))+';\n')
        f_pybind11.write('DEFINE_PYBIND11_MODULE_ZERO_HORIZON_OCP_SOLVER(OCP_'+str(self.__model_name)+', kmax_init)\n')
        f_pybind11.writelines([
"""

} // namespace python
} // namespace cgmres
""" 
        ])
        f_pybind11.close()
        f_pybind11 = open('models/'+str(self.__model_name)+'/python/'+str(self.__model_name)+'/single_shooting_cgmres_solver.cpp', 'w')
        f_pybind11.writelines([
"""
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>

#include "cgmres/single_shooting_cgmres_solver.hpp"
#include "cgmres/python/single_shooting_cgmres_solver.hpp"
#include "ocp.hpp"

#include <iostream>
#include <stdexcept>

namespace cgmres {
namespace python {

namespace py = pybind11;

""" 
        ])
        f_pybind11.write('constexpr int N = '+str(self.__N)+';\n')
        f_pybind11.write('constexpr int kmax = '+str(min(self.__kmax, self.__N*(self.__dimc+self.__dimu+self.__dimh)))+';\n')
        f_pybind11.write('DEFINE_PYBIND11_MODULE_SINGLE_SHOOTING_CGMRES_SOLVER(OCP_'+str(self.__model_name)+', N, kmax)\n')
        f_pybind11.writelines([
"""

} // namespace python
} // namespace cgmres
""" 
        ])
        f_pybind11.close()
        f_pybind11 = open('models/'+str(self.__model_name)+'/python/'+str(self.__model_name)+'/multiple_shooting_cgmres_solver.cpp', 'w')
        f_pybind11.writelines([
"""
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>

#include "cgmres/multiple_shooting_cgmres_solver.hpp"
#include "cgmres/python/multiple_shooting_cgmres_solver.hpp"
#include "ocp.hpp"

#include <iostream>
#include <stdexcept>

namespace cgmres {
namespace python {

namespace py = pybind11;

""" 
        ])
        f_pybind11.write('constexpr int N = '+str(self.__N)+';\n')
        f_pybind11.write('constexpr int kmax = '+str(min(self.__kmax, self.__N*(self.__dimc+self.__dimu+self.__dimh)))+';\n')
        f_pybind11.write('DEFINE_PYBIND11_MODULE_MULTIPLE_SHOOTING_CGMRES_SOLVER(OCP_'+str(self.__model_name)+', N, kmax)\n')
        f_pybind11.writelines([
"""

} // namespace python
} // namespace cgmres
""" 
        ])
        f_pybind11.close()
        f_pybind11 = open('models/'+str(self.__model_name)+'/python/'+str(self.__model_name)+'/horizon.cpp', 'w')
        f_pybind11.writelines([
"""
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>

#include "cgmres/types.hpp"
#include "cgmres/horizon.hpp"
#include "cgmres/python/horizon.hpp"

#include <iostream>
#include <stdexcept>

namespace cgmres {
namespace python {

namespace py = pybind11;

DEFINE_PYBIND11_MODULE_HORIZON()

} // namespace python
} // namespace cgmres
""" 
        ])
        f_pybind11.close()
        f_pybind11 = open('models/'+str(self.__model_name)+'/python/'+str(self.__model_name)+'/solver_settings.cpp', 'w')
        f_pybind11.writelines([
"""
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>

#include "cgmres/solver_settings.hpp"
#include "cgmres/python/solver_settings.hpp"

#include <iostream>
#include <stdexcept>


namespace cgmres {
namespace python {

namespace py = pybind11;

DEFINE_PYBIND11_MODULE_SOLVER_SETTINGS()

} // namespace python
} // namespace cgmres
""" 
        ])
        f_pybind11.close()
        f_pybind11 = open('models/'+str(self.__model_name)+'/python/'+str(self.__model_name)+'/__init__.py', 'w')
        f_pybind11.writelines([
"""
from .ocp import *
from .zero_horizon_ocp_solver import *
from .single_shooting_cgmres_solver import *
from .multiple_shooting_cgmres_solver import *
from .horizon import *
from .solver_settings import *
""" 
        ])
        f_pybind11.close()


    def generate_cmake(self):
        """ Generates CMakeLists.txt in a directory where your .ipynb files 
            locates.
        """
        f_cmake = open('models/'+str(self.__model_name)+'/CMakeLists.txt', 'w')
        f_cmake.writelines([
"""
cmake_minimum_required(VERSION 3.1)
""" 
        ])
        f_cmake.write('project('+str(self.__model_name)+' CXX)')
        f_cmake.writelines([
"""

set(CMAKE_CXX_STANDARD 17)

option(VECTORIZE "Enable -march=native" OFF)
option(BUILD_PYTHON_INTERFACE "Build Python interface" OFF)

set(CGMRES_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/../../include)

add_executable(
    ${PROJECT_NAME}
    main.cpp
)
target_include_directories(
    ${PROJECT_NAME}
    PRIVATE
    ${CGMRES_INCLUDE_DIR}
    ${CGMRES_INCLUDE_DIR}/thirdparty/eigen
)
if (VECTORIZE)
  target_compile_options(
    ${PROJECT_NAME}
    PRIVATE
    -march=native
  )
endif()

if (BUILD_PYTHON_INTERFACE)
    add_subdirectory(python/${PROJECT_NAME})
endif()
"""
            ])
        f_cmake.close()
        f_cmake_python = open('models/'+self.__model_name+'/python/'+self.__model_name+'/CMakeLists.txt', 'w')
        f_cmake_python.writelines([
"""
macro(pybind11_add_cgmres_module MODULE)
  pybind11_add_module(
    ${MODULE} 
    SHARED 
    ${MODULE}.cpp
  )
  target_include_directories(
    ${MODULE} 
    PRIVATE
    ${CGMRES_INCLUDE_DIR}
    ${CGMRES_INCLUDE_DIR}/thirdparty/eigen
    ${PROJECT_SOURCE_DIR}
  )
    if (VECTORIZE)
    target_compile_options(
        ${MODULE}
        PRIVATE
        -march=native
    )
    endif()
endmacro()

add_subdirectory(${CGMRES_INCLUDE_DIR}/thirdparty/pybind11 ${CMAKE_CURRENT_BINARY_DIR}/thirdparty/pybind11)
pybind11_add_cgmres_module(ocp)
pybind11_add_cgmres_module(solver_settings)
pybind11_add_cgmres_module(zero_horizon_ocp_solver)
pybind11_add_cgmres_module(horizon)
pybind11_add_cgmres_module(single_shooting_cgmres_solver)
pybind11_add_cgmres_module(multiple_shooting_cgmres_solver)

set(CGMRES_PYTHON_VERSION ${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR})
"""
            ])
        f_cmake_python.write(
            'set(CGMRES_PYTHON_BINDINGS_LIBDIR $ENV{HOME}/.local/lib/python${CGMRES_PYTHON_VERSION}/site-packages/cgmres/'+self.__model_name+')')
        f_cmake_python.writelines([
"""
file(GLOB PYTHON_BINDINGS_${CURRENT_MODULE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/*.cpython*)
file(GLOB PYTHON_FILES_${CURRENT_MODULE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/*.py)
install(
  FILES ${PYTHON_FILES_${CURRENT_MODULE_DIR}} ${PYTHON_BINDINGS_${CURRENT_MODULE_DIR}} 
  DESTINATION ${CGMRES_PYTHON_BINDINGS_LIBDIR}/${CURRENT_MODULE_DIR}
)
"""
            ])
        f_cmake_python.close()


    def build(self, generator='Auto', build_python_interface=False, install_python_interface=False, remove_build_dir=False):
        """ Builds execute file to run numerical simulation. 

            Args: 
                generator: An optional variable for Windows user to choose the
                    generator. If 'MSYS', then 'MSYS Makefiles' is used. If 
                    'MinGW', then 'MinGW Makefiles' is used. The default value 
                    is 'Auto' and the generator is selected automatically. If 
                    sh.exe exists in your PATH, MSYS is choosed, and otherwise 
                    MinGW is used. If different value from 'MSYS' and 'MinGW', 
                    generator is selected automatically.
                remove_build_dir: If true, the existing build directory is 
                    removed and if False, the build directory is not removed.
                    Need to be set True is you change CMake configuration, e.g., 
                    if you change the generator. The default value is False.
        """
        build_options = ['-DCMAKE_BUILD_TYPE=Release', '-DVECTORIZE=ON']
        if build_python_interface or install_python_interface:
            build_options.append('-DBUILD_PYTHON_INTERFACE=ON')
        if platform.system() == 'Windows':
            subprocess.run(
                ['mkdir', 'build'], 
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=True
            )
            if generator == 'MSYS':
                proc = subprocess.Popen(
                    ['cmake', '..', '-G', 'MSYS Makefiles', *build_options], 
                    cwd='models/'+self.__model_name+'/build', 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    shell=True
                )
                for line in iter(proc.stdout.readline, b''):
                    print(line.rstrip().decode("utf8"))
                print('\n')
            elif generator == 'MinGW':
                proc = subprocess.Popen(
                    ['cmake', '..', '-G', 'MinGW Makefiles', *build_options], 
                    cwd='models/'+self.__model_name+'/build', 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    shell=True
                )
                for line in iter(proc.stdout.readline, b''):
                    print(line.rstrip().decode("utf8"))
                print('\n')
            else:
                proc = subprocess.Popen(
                    ['where', 'sh.exe'], 
                    cwd='C:', 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    shell=True
                )
                if proc.stderr.readline() == b'':
                    proc = subprocess.Popen(
                        ['cmake', '..', '-G', 'MSYS Makefiles', *build_options], 
                        cwd='models/'+self.__model_name+'/build', 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        shell=True
                    )
                else:
                    proc = subprocess.Popen(
                        ['cmake', '..', '-G', 'MinGW Makefiles', *build_options], 
                        cwd='models/'+self.__model_name+'/build', 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        shell=True
                    )
                for line in iter(proc.stdout.readline, b''):
                    print(line.rstrip().decode("utf8"))
                print('\n')
            proc = subprocess.Popen(
                ['cmake', '--build', '.', '-j4'], 
                cwd='models/'+self.__model_name+'/build', 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                shell=True
            )
            if install_python_interface:
                proc = subprocess.Popen(
                    ['cmake', '--install', '.'], 
                    cwd='models/'+self.__model_name+'/build', 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    shell=True
                )
            for line in iter(proc.stdout.readline,b''):
                print(line.rstrip().decode("utf8"))
            print('\n')
            
        else:
            subprocess.run(
                ['mkdir', 'build'], 
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            print('build_options:', *build_options)
            proc = subprocess.Popen(
                ['cmake', '..', *build_options], 
                cwd='models/'+self.__model_name+'/build', 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT
            )
            for line in iter(proc.stdout.readline, b''):
                print(line.rstrip().decode("utf8"))
            print('\n')
            proc = subprocess.Popen(
                ['cmake', '--build', '.', '-j4'], 
                cwd='models/'+self.__model_name+'/build', 
                stdout = subprocess.PIPE, 
                stderr = subprocess.STDOUT
            )
            if install_python_interface:
                proc = subprocess.Popen(
                    ['cmake', '--install', '.'], 
                    cwd='models/'+self.__model_name+'/build', 
                    stdout = subprocess.PIPE, 
                    stderr = subprocess.STDOUT
                )
            for line in iter(proc.stdout.readline, b''):
                print(line.rstrip().decode("utf8"))
            print('\n')

    def run_simulation(self):
        """ Run numerical simulation. Call after build() succeeded.
        """
        if platform.system() == 'Windows':
            subprocess.run(
                ['rmdir', '/q', '/s', 'simulation_result'], 
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=True
            )
            subprocess.run(
                ['mkdir', 'simulation_result'], 
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=True
            )
            proc = subprocess.Popen(
                [self.__model_name+'.exe'], 
                cwd='models/'+self.__model_name+'/build', 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                shell=True
            )
            for line in iter(proc.stdout.readline, b''):
                print(line.rstrip().decode("utf8"))
        else:
            subprocess.run(
                ['rm', '-rf', 'simulation_result'], 
                cwd='models/'+self.__model_name, 
                stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE, 
                shell=True
            )
            subprocess.run(
                ['mkdir', 'simulation_result'], 
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            proc = subprocess.Popen(
                ['./'+self.__model_name], 
                cwd='models/'+self.__model_name+'/build', 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT
            )
            for line in iter(proc.stdout.readline, b''):
                print(line.rstrip().decode("utf8"))


    def __write_function(
            self, writable_file, function, return_value_name, use_cse
        ):
        """ Write input symbolic function onto writable_file. The function's 
            return value name must be set. use_cse is optional.

            Args: 
                writable_file: A writable file, i.e., a file streaming that is 
                    already opened as writing mode.
                function: A symbolic function wrote onto the writable_file.
                return_value_name: The name of the return value.
                use_cse: If true, common subexpression elimination is used. If 
                    False, it is not used.
        """
        if use_cse:
            func_cse = sympy.cse(function)
            for i in range(len(func_cse[0])):
                cse_exp, cse_rhs = func_cse[0][i]
                writable_file.write(
                    '  double '+sympy.ccode(cse_exp)
                    +' = '+sympy.ccode(cse_rhs)+';\n'
                )
            for i in range(len(func_cse[1])):
                writable_file.write(
                    '  '+return_value_name+'[%d] = '%i
                    +sympy.ccode(func_cse[1][i])+';\n'
                )
        else:
            writable_file.writelines(
                ['  '+return_value_name+'[%d] = '%i
                +sympy.ccode(function[i])+';\n' for i in range(len(function))]
            )

    def __make_model_dir(self):
        """ Makes a directory where the C source files of OCP models are 
            generated.
        """
        if platform.system() == 'Windows':
            subprocess.run(
                ['mkdir', 'models'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=True
            )
            subprocess.run(
                ['mkdir', self.__model_name], 
                cwd='models', 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=True
            )
            subprocess.run(
                ['mkdir', '-p', 'python/'+self.__model_name], 
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=True
            )
        else:
            subprocess.run(
                ['mkdir', 'models'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            subprocess.run(
                ['mkdir', self.__model_name], 
                cwd='models',
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            subprocess.run(
                ['mkdir', '-p', 'python/'+self.__model_name], 
                cwd='models/'+self.__model_name,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )

    def __remove_build_dir(self):
        """ Removes a build directory. This function is mainly for Windows 
            users with MSYS.
        """
        if platform.system() == 'Windows':
            subprocess.run(
                ['rmdir', '/q', '/s', 'build'], 
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=True
            )
        else:
            subprocess.run(
                ['rm', '-r', 'build'],
                cwd='models/'+self.__model_name, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )