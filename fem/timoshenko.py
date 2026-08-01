import numpy as np


def timoshenko_stiffness(E, G, I, A, L, ks=6/7):
    """
    2-node Timoshenko beam stiffness matrix
    DOF:
    [w1, theta1, w2, theta2]
    """

    phi = 12 * E * I / (ks * G * A * L**2)

    c = E * I / ((1 + phi) * L**3)

    K = c * np.array([
        [12,               6*L,         -12,               6*L],
        [6*L, (4+phi)*L**2, -6*L, (2-phi)*L**2],
        [-12,             -6*L,          12,             -6*L],
        [6*L, (2-phi)*L**2, -6*L, (4+phi)*L**2]
    ])

    return K


def timoshenko_mass(rho, A, L):
    """
    Consistent mass matrix
    """

    return rho * A * L / 420 * np.array([
        [156,        22*L,      54,      -13*L],
        [22*L,   4*L**2,   13*L,    -3*L**2],
        [54,         13*L,     156,      -22*L],
        [-13*L, -3*L**2, -22*L,    4*L**2]
    ])


def rotary_inertia(rho, I, L):
    """
    Rotary inertia matrix
    """

    return rho * I * L / 30 * np.array([
        [0, 0, 0, 0],
        [0, 4, 0, -1],
        [0, 0, 0, 0],
        [0, -1, 0, 4]
    ])
