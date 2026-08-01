import pandas as pd
import numpy as np

def load_spindle_frf(csv_file):

    df = pd.read_csv(csv_file)

    freq = df["freq"].values

    H = (
        df["re"].values
        + 1j * df["im"].values
    )

    Hsp = np.zeros(
        (len(freq), 2, 2),
        dtype=complex
    )

    Hsp[:,0,0] = H
    Hsp[:,1,1] = H

    return freq, Hsp