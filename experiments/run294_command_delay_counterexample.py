"""Dependency-free counterexample: hidden command delay breaks a Markov predictor.

Toy reference-tracking channel only; NOT an identified PX4 model.
"""

def step(p, v, r_prev):
    return (p + v, 0.5 * v + 0.5 * r_prev)

def run():
    x = (0.0, 0.0)
    current_reference = 0.0
    plus = step(*x, +1.0)
    minus = step(*x, -1.0)
    assert plus == (0.0, 0.5)
    assert minus == (0.0, -0.5)
    assert plus != minus
    minimum_radius = abs(plus[1] - minus[1]) / 2
    assert minimum_radius == 0.5
    assert step(*x, +1.0) == plus
    assert step(*x, -1.0) == minus
    print("PASS: hidden delay yields distinct successors; minimum velocity residual radius=0.5")

if __name__ == "__main__":
    run()
