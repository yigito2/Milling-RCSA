import numpy as np


def spindle_frf(freq):

    m = 5.0

    fn = 800

    zeta = 0.03

    wn = 2 * np.pi * fn

    k = m * wn**2
    c = 2 * zeta * m * wn

    Hs = np.zeros(
        (len(freq), 2, 2),
        dtype=complex
    )

    for i, f in enumerate(freq):

        w = 2 * np.pi * f

        H = 1 / (
            k
            - m * w**2
            + 1j * c * w
        )

        Hs[i,0,0] = H
        Hs[i,1,1] = H

    return Hs