#ifndef CGMRES__OCP_CARTPOLE_EXTERNAL_REFERENCE_HPP_ 
#define CGMRES__OCP_CARTPOLE_EXTERNAL_REFERENCE_HPP_
 
#define _USE_MATH_DEFINES

#include <cmath>
#include <array>
#include <iostream>
#include <memory>

#include "cgmres/types.hpp"

namespace cgmres {

/// 
/// @class OCP_cartpoleExternalReference
/// @brief Definition of the optimal control problem (OCP) of cartpoleExternalReference.
/// 
class OCP_cartpoleExternalReference { 
public:
 
  ///
  /// @brief Dimension of the state. 
  ///
  static constexpr int nx = 4;
 
  ///
  /// @brief Dimension of the control input. 
  ///
  static constexpr int nu = 1;
 
  ///
  /// @brief Dimension of the equality constraints. 
  ///
  static constexpr int nc = 0;
 
  ///
  /// @brief Dimension of the Fischer-Burmeister function (already counded in nc). 
  ///
  static constexpr int nh = 0;
 
  ///
  /// @brief Dimension of the concatenation of the control input and equality constraints. 
  ///
  static constexpr int nuc = nu + nc;
 
  ///
  /// @brief Dimension of the bound constraints on the control input. 
  ///
  static constexpr int nub = 1;

  double m_c = 2;
  double m_p = 0.2;
  double l = 0.5;
  double g = 9.80665;

  std::array<double, 4> q = {2.5, 10, 0.01, 0.01};
  std::array<double, 4> q_terminal = {2.5, 10, 0.01, 0.01};
  std::array<double, 4> x_ref = {0, M_PI, 0, 0};
  std::array<double, 1> r = {1};

  static constexpr std::array<int, nub> ubound_indices = {0};
  std::array<double, nub> umin = {-15.0};
  std::array<double, nub> umax = {15.0};
  std::array<double, nub> dummy_weight = {0.1};

  void disp(std::ostream& os) const {
    os << "OCP_cartpoleExternalReference:" << std::endl;
    os << "  nx:  " << nx << std::endl;
    os << "  nu:  " << nu << std::endl;
    os << "  nc:  " << nc << std::endl;
    os << "  nh:  " << nh << std::endl;
    os << "  nuc: " << nuc << std::endl;
    os << "  nub: " << nub << std::endl;
    os << std::endl;
    os << "  m_c: " << m_c << std::endl;
    os << "  m_p: " << m_p << std::endl;
    os << "  l: " << l << std::endl;
    os << "  g: " << g << std::endl;
    os << std::endl;
    Eigen::IOFormat fmt(4, 0, ", ", "", "[", "]");
    Eigen::IOFormat intfmt(1, 0, ", ", "", "[", "]");
    os << "  q: " << Map<const VectorX>(q.data(), q.size()).transpose().format(fmt) << std::endl;
    os << "  q_terminal: " << Map<const VectorX>(q_terminal.data(), q_terminal.size()).transpose().format(fmt) << std::endl;
    os << "  x_ref: " << Map<const VectorX>(x_ref.data(), x_ref.size()).transpose().format(fmt) << std::endl;
    os << "  r: " << Map<const VectorX>(r.data(), r.size()).transpose().format(fmt) << std::endl;
    os << std::endl;
    os << "  ubound_indices: " << Map<const VectorXi>(ubound_indices.data(), ubound_indices.size()).transpose().format(intfmt) << std::endl;
    os << "  umin: " << Map<const VectorX>(umin.data(), umin.size()).transpose().format(fmt) << std::endl;
    os << "  umax: " << Map<const VectorX>(umax.data(), umax.size()).transpose().format(fmt) << std::endl;
    os << "  dummy_weight: " << Map<const VectorX>(dummy_weight.data(), dummy_weight.size()).transpose().format(fmt) << std::endl;
  }

  friend std::ostream& operator<<(std::ostream& os, const OCP_cartpoleExternalReference& ocp) { 
    ocp.disp(os);
    return os;
  }

  struct ExternalReference {
    double cart_position = 0.0;
  };
  std::shared_ptr<ExternalReference> external_reference = nullptr;

  ///
  /// @brief Synchrozies the internal parameters of this OCP with the external references.
  ///
  void synchronize() {
    if (external_reference != nullptr) {
      x_ref[0] = external_reference->cart_position;
    }
  }

  ///
  /// @brief Computes the state equation dx = f(t, x, u).
  /// @param[in] t Time.
  /// @param[in] x State.
  /// @param[in] u Control input.
  /// @param[out] dx Evaluated value of the state equation.
  ///
  void eval_f(const double t, const double* x, const double* u, 
              double* dx) const {
    const double x0 = sin(x[1]);
    const double x1 = 1.0/(m_c + m_p*pow(x0, 2));
    const double x2 = cos(x[1]);
    const double x3 = l*pow(x[1], 2);
    const double x4 = m_p*x0;
    dx[0] = x[2];
    dx[1] = x[3];
    dx[2] = x1*(u[0] + x4*(g*x2 + x3));
    dx[3] = x1*(-g*x0*(m_c + m_p) - u[0]*x2 - x2*x3*x4)/l;
 
  }

  ///
  /// @brief Computes the partial derivative of terminal cost with respect to state, 
  /// i.e., phix = dphi/dx(t, x).
  /// @param[in] t Time.
  /// @param[in] x State.
  /// @param[out] phix Evaluated value of the partial derivative of terminal cost.
  ///
  void eval_phix(const double t, const double* x, double* phix) const {
    phix[0] = (1.0/2.0)*q_terminal[0]*(2*x[0] - 2*x_ref[0]);
    phix[1] = (1.0/2.0)*q_terminal[1]*(2*x[1] - 2*x_ref[1]);
    phix[2] = (1.0/2.0)*q_terminal[2]*(2*x[2] - 2*x_ref[2]);
    phix[3] = (1.0/2.0)*q_terminal[3]*(2*x[3] - 2*x_ref[3]);
 
  }

  ///
  /// @brief Computes the partial derivative of the Hamiltonian with respect to state, 
  /// i.e., hx = dH/dx(t, x, u, lmd).
  /// @param[in] t Time.
  /// @param[in] x State.
  /// @param[in] u Concatenatin of the control input and Lagrange multiplier with respect to the equality constraints. 
  /// @param[in] lmd Costate. 
  /// @param[out] hx Evaluated value of the partial derivative of the Hamiltonian.
  ///
  void eval_hx(const double t, const double* x, const double* u, 
               const double* lmd, double* hx) const {
    const double x0 = 2*x[1];
    const double x1 = sin(x[1]);
    const double x2 = cos(x[1]);
    const double x3 = g*x2;
    const double x4 = pow(x[1], 2);
    const double x5 = l*x4;
    const double x6 = m_p*(x3 + x5);
    const double x7 = pow(x1, 2);
    const double x8 = m_c + m_p*x7;
    const double x9 = m_p*x1;
    const double x10 = x2*x9;
    const double x11 = 2*x10/pow(x8, 2);
    const double x12 = 1.0/x8;
    const double x13 = g*x1;
    const double x14 = m_c + m_p;
    const double x15 = lmd[3]/l;
    hx[0] = (1.0/2.0)*q[0]*(2*x[0] - 2*x_ref[0]);
    hx[1] = -lmd[2]*x11*(u[0] + x1*x6) + lmd[2]*x12*(x2*x6 + x9*(2*l*x[1] - x13)) + (1.0/2.0)*q[1]*(x0 - 2*x_ref[1]) - x11*x15*(-u[0]*x2 - x10*x5 - x13*x14) + x12*x15*(l*m_p*x4*x7 - l*x0*x10 - m_p*pow(x2, 2)*x5 + u[0]*x1 - x14*x3);
    hx[2] = lmd[0] + (1.0/2.0)*q[2]*(2*x[2] - 2*x_ref[2]);
    hx[3] = lmd[1] + (1.0/2.0)*q[3]*(2*x[3] - 2*x_ref[3]);
 
  }

  ///
  /// @brief Computes the partial derivative of the Hamiltonian with respect to control input and the equality constraints, 
  /// i.e., hu = dH/du(t, x, u, lmd).
  /// @param[in] t Time.
  /// @param[in] x State.
  /// @param[in] u Concatenatin of the control input and Lagrange multiplier with respect to the equality constraints. 
  /// @param[in] lmd Costate. 
  /// @param[out] hu Evaluated value of the partial derivative of the Hamiltonian.
  ///
  void eval_hu(const double t, const double* x, const double* u, 
               const double* lmd, double* hu) const {
    const double x0 = 1.0/(m_c + m_p*pow(sin(x[1]), 2));
    hu[0] = lmd[2]*x0 + r[0]*u[0] - lmd[3]*x0*cos(x[1])/l;
 
  }
};

} // namespace cgmres

#endif // CGMRES_OCP_HPP_
