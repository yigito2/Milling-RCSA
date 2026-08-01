import numpy as np


def couple(
    Hcc,
    Hcb,
    Hbc,
    Hbb,
    Hspindle
):

    nf = Hcc.shape[0]

    Htool = np.zeros_like(Hcc)

    for i in range(nf):

        Htool[i] = (
            Hcc[i]
            - Hcb[i]
            @ np.linalg.inv(
                Hbb[i] + Hspindle[i]
            )
            @ Hbc[i]
        )

    return Htool