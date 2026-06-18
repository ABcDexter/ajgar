#!/usr/bin/env python3
#############################################################################################################################
# Draw hydrogen-like atomic orbitals (|psi|^2) for given quantum numbers n, l, m.
#
# Features:
# - Compute analytic hydrogenic radial functions R_{n,l}(r) (atomic units, a0=1)
# - Use spherical harmonics from scipy to build psi(r,theta,phi)
# - Render either a 2D slice (imshow + contour) or a 3D scatter of points above a threshold
#
# Requirements:
#   python -m pip install --user numpy scipy matplotlib
#
# Examples:
#   # 2D slice at z=0 for 2p (n=2,l=1,m=0)
#   python scripts/orbitals.py --n 2 --l 1 --m 0 --mode slice --slice-z 0 --grid 300 --out orb_2p_z0.png
#
#   # 3D scatter for 3d (n=3,l=2,m=1)
#   python scripts/orbitals.py --n 3 --l 2 --m 1 --mode scatter --grid 80 --threshold 0.02 --out-dir figures
#
#############################################################################################################################

from __future__ import annotations

###########
# Imports #
###########
import argparse
import math
import os
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)
#from scipy.special import sph_harm, genlaguerre, factorial
from scipy.special import sph_harm_y as sph_harm
from scipy.special import genlaguerre


#############
# Constants #
#############
A0 = 1.0  # Bohr radius in atomic units (use 1 for hydrogenic shapes)


####################
# Helper Functions #
####################

def factorial(n: int) -> int:
    """Compute factorial of n (non-negative integer)."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def radial_R(n: int, l: int, r: np.ndarray, a0: float = A0) -> np.ndarray:
    """
    Compute hydrogenic radial wavefunction R_{n,l}(r) (real) in atomic units.

    Uses the standard analytic expression with generalized Laguerre polynomials.
    Returns values with the Condon-Shortley phase convention consistent with scipy's sph_harm.
    """
    # safety
    if n <= l:
        raise ValueError("Quantum number n must be > l")

    rho = 2.0 * r / (n * a0)

    # normalization constant
    prefactor = np.sqrt((2.0 / (n * a0)) ** 3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))

    # Associated Laguerre polynomial L_{n-l-1}^{2l+1}(rho)
    L = genlaguerre(n - l - 1, 2 * l + 1)(rho)

    R = prefactor * rho ** l * np.exp(-rho / 2.0) * L
    return R


def psi_complex(n: int, l: int, m: int, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """
    Compute complex wavefunction psi on Cartesian grid arrays x,y,z.

    Returns complex-valued psi array with the same shape as inputs.
    """
    # convert to spherical coords
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    # avoid division by zero in theta computation
    theta = np.arccos(np.where(r > 0, z / r, 1.0))  # polar angle [0,pi]
    phi = np.arctan2(y, x)  # azimuth [ -pi, pi ]

    # radial part
    R = radial_R(n, l, r)

    # spherical harmonic (complex)
    Y = sph_harm(m, l, phi, theta)

    psi = R * Y
    return psi


def make_grid(grid: int, rmax: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create a cubic grid centered at origin with side length 2*rmax and `grid` points per axis."""
    xs = np.linspace(-rmax, rmax, grid)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing='xy')
    return X, Y, Z


#################
# Plotting Code #
#################
def plot_slice(n: int, l: int, m: int, grid: int=200, rmax: float=20.0, z0: float=0.0, out: str | None=None) -> None:
    '''create 2D grid on plane z = z0'''
    xs = np.linspace(-rmax, rmax, grid)
    X, Y = np.meshgrid(xs, xs, indexing='xy')
    Z = np.full_like(X, z0)

    psi = psi_complex(n, l, m, X, Y, Z)
    density = np.real(psi * np.conjugate(psi))

    plt.figure(figsize=(6, 5))
    im = plt.imshow(density, extent=[-rmax, rmax, -rmax, rmax], origin='lower', cmap='inferno')
    plt.colorbar(im, label=r'$|\psi|^2$')
    plt.title(f"Orbital n={n}, l={l}, m={m}  (slice z={z0})")
    plt.xlabel('x (a.u.)')
    plt.ylabel('y (a.u.)')
    if out:
        plt.savefig(out, dpi=150, bbox_inches='tight')
        print(f"Saved slice image to {out}")
    else:
        plt.show()


def plot_scatter(n: int, l: int, m: int, grid: int=200, rmax: float=20.0, threshold: float=0.02, out_dir: str | None=None) -> None:
    '''create 3D grid and scatter points above threshold'''
    X, Y, Z = make_grid(grid, rmax)
    psi = psi_complex(n, l, m, X, Y, Z)
    density = np.real(psi * np.conjugate(psi))

    dmax = density.max()
    if dmax <= 0:
        raise RuntimeError("Computed density is zero everywhere; check quantum numbers or grid.")

    mask = density >= (threshold * dmax)
    xs = X[mask]
    ys = Y[mask]
    zs = Z[mask]
    vals = density[mask]

    print(f"Selected {vals.size} points (threshold {threshold} of max) out of {density.size} grid points")

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection='3d')
    p = ax.scatter(xs, ys, zs, c=vals, cmap='inferno', s=1, alpha=0.6)
    ax.set_xlim(-rmax, rmax)
    ax.set_ylim(-rmax, rmax)
    ax.set_zlim(-rmax, rmax)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    fig.colorbar(p, label=r'$|\psi|^2$')
    ax.set_title(f"Orbital n={n}, l={l}, m={m} (scatter threshold {threshold})")

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"orbital_n{n}_l{l}_m{m}.png")
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        print(f"Saved scatter image to {out_path}")
    else:
        plt.show()


#################
# main function #
#################
def main() -> None:
    parser = argparse.ArgumentParser(description='Render hydrogen-like atomic orbitals (|psi|^2).')
    parser.add_argument('--n', type=int, required=True, help='Principal quantum number n (integer >=1)')
    parser.add_argument('--l', type=int, required=True, help='Azimuthal quantum number l (0 <= l < n)')
    parser.add_argument('--m', type=int, required=True, help='Magnetic quantum number m (-l <= m <= l)')
    
    args = parser.parse_args()

    # Validate quantum numbers
    if args.n <= 0:
        raise SystemExit('n must be >= 1')
    if args.l < 0 or args.l >= args.n:
        raise SystemExit('l must satisfy 0 <= l < n')
    if abs(args.m) > args.l:
        raise SystemExit('m must satisfy -l <= m <= l')

    plot_slice(args.n, args.l, args.m)


if __name__ == '__main__':
    main()
