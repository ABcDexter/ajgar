#############################################################################################################################
# Generate Lissajous figures
#
# Equations:
#   x = A * sin(a * t + delta)
#   y = B * sin(b * t)
#
# This script supports interactive mode and CLI. Use `--a` and `--b` to supply
# integer values (single, comma separated, hyphen ranges or colon ranges).
#############################################################################################################################
from __future__ import annotations

import argparse
import math
import os
from typing import List

import numpy as np
import matplotlib.pyplot as plt


#############
# Constants #
#############
DEFAULT_NPOINTS = 2000
DEFAULT_DPI = 150

####################
# Helper Functions #
####################
def parse_sequence(s: str) -> List[int]:
    """Parse a string describing a sequence of integer values.

    Supported formats:
      - single integer: "3"
      - comma separated: "1,2,3"
      - hyphen range inclusive: "1-5" -> [1,2,3,4,5]
      - colon range like start:stop:step (all integers): "1:7:2" -> [1,3,5]
    """
    s = s.strip()
    if not s:
        return []
    if "," in s:
        parts = [p.strip() for p in s.split(",") if p.strip()]
        return [int(p) for p in parts]
    if ":" in s:
        parts = [int(p) for p in s.split(":")]
        if len(parts) == 2:
            start, stop = parts
            return list(range(start, stop + 1))
        elif len(parts) == 3:
            start, stop, step = parts
            return list(range(start, stop + 1, step))
    if "-" in s:
        a, b = [int(p.strip()) for p in s.split("-", 1)]
        if a <= b:
            return list(range(a, b + 1))
        else:
            return list(range(a, b - 1, -1))
    return [int(s)]


def lcm(a: int, b: int) -> int:
    '''Compute least common multiple of a and b.'''
    return abs(a * b) // math.gcd(a, b) if a and b else 0


def _safe_filename(a: int, b: int, A: float, B: float, delta: float) -> str:
    """Return a filesystem-safe filename for a given parameter set.

    Replace dots in `delta` with 'p' to avoid ambiguous filenames.
    """
    d = str(delta).replace('.', 'p')
    return f"lissajous_a{a}_b{b}_A{A}_B{B}_d{d}.png".replace(' ', '_')


def generate_and_plot(A: float, B: float, a: int, b: int, delta: float, npoints: int, out_dir: str | None, show: bool, dpi: int):
    '''
    Generate a Lissajous figure for the given parameters and either save it or show it.
    '''
    # Choose t-range so the curve completes if a and b are integers
    if isinstance(a, int) and isinstance(b, int) and a > 0 and b > 0:
        period_multiplier = lcm(a, b) if lcm(a, b) > 0 else 1
        t_max = 2 * math.pi * period_multiplier
    else:
        t_max = 2 * math.pi

    t = np.linspace(0, t_max, npoints)
    x = A * np.sin(a * t + delta)
    y = B * np.sin(b * t)

    plt.figure(figsize=(6, 6))
    plt.plot(x, y, lw=1)
    plt.title(f"Lissajous: a={a}, b={b}, A={A}, B={B}, delta={delta}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, ls=':', alpha=0.4)

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, _safe_filename(a, b, A, B, delta))
        plt.savefig(out_path, dpi=dpi, bbox_inches='tight')
        print(f"Saved {out_path}")

    if show:
        plt.show()
    else:
        plt.close()


def prompt_for_values(prompt: str) -> List[int]:
    '''
    Prompt the user for a sequence of integer values until valid input is provided.
    '''
    s = input(prompt).strip()
    return parse_sequence(s)


def main():
    '''
    Main function to parse arguments and generate Lissajous figures.
    '''
    parser = argparse.ArgumentParser(description="Generate Lissajous figures for given a,b values.")
    parser.add_argument('--A', type=float, default=1.0, help='Amplitude A (x)')
    parser.add_argument('--B', type=float, default=1.0, help='Amplitude B (y)')
    parser.add_argument('--delta', type=float, default=0.0, help='Phase delta (radians)')
    parser.add_argument('--a', type=str, default='', help="Values for a (e.g. '1', '1,2,3', '1-5', or '1:7:2')")
    parser.add_argument('--b', type=str, default='', help="Values for b (same formats as a)")
    parser.add_argument('--npoints', type=int, default=2000, help='Number of points in param t')
    parser.add_argument('--out-dir', type=str, default=None, help='Directory to save PNG files (if omitted images are shown)')
    parser.add_argument('--no-show', action='store_true', help='Do not display figures interactively')
    parser.add_argument('--dpi', type=int, default=150, help='Output image dpi')

    args = parser.parse_args()

    A = args.A
    B = args.B
    delta = args.delta
    npoints = args.npoints
    out_dir = args.out_dir
    show = not args.no_show

    
    a_values = parse_sequence(args.a) if args.a else prompt_for_values("Enter values for 'a' (e.g. 1,2 or 1-5 or 1:7:2): ")

    b_values = parse_sequence(args.b) if args.b else prompt_for_values("Enter values for 'b' (e.g. 1,2 or 1-5 or 1:7:2): ")

    if not a_values or not b_values:
        print("No a or b values provided; exiting!!!")
        return

    for a in a_values:
        for b in b_values:
            generate_and_plot(A, B, int(a), int(b), float(delta), npoints, out_dir, show, args.dpi)


if __name__ == '__main__':
    main()
