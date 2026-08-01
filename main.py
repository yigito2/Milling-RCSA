from fem.beam2d import ToolBeam
from rcsa.coupling import couple
from data.spindle_model import spindle_frf

import matplotlib

print("Backend =", matplotlib.get_backend())


tool_no_rot = ToolBeam(
    D=0.012,
    L=0.08,
    E=600e9,
    rho=14500,
    n_elem=20,
    use_rotary=False
)

tool_rot = ToolBeam(
    D=0.012,
    L=0.08,
    E=600e9,
    rho=14500,
    n_elem=20,
    use_rotary=True
)

fn_no = tool_no_rot.natural_frequencies(6)
fn_rot = tool_rot.natural_frequencies(6)

print()
print("ROTARY INERTIA COMPARISON")
print("-"*80)

for i in range(6):

    diff_hz = fn_rot[i] - fn_no[i]
    diff_pct = 100 * diff_hz / fn_no[i]

    print(
        f"Mode {i+1:>2} | "
        f"No RI = {fn_no[i]:10.2f} Hz | "
        f"With RI = {fn_rot[i]:10.2f} Hz | "
        f"Δ = {diff_hz:8.2f} Hz | "
        f"{diff_pct:8.4f}%"
    )

print("Before mode plots")

tool_rot.plot_mode(1)
tool_rot.plot_mode(2)
tool_rot.plot_mode(3)

print("After mode plots")

import numpy as np
import matplotlib.pyplot as plt

freq = np.linspace(
    1,
    30000,
    3000
)

Gxx = tool_rot.frf(freq)

plt.figure(figsize=(10,5))

plt.semilogy(
    freq,
    np.abs(Gxx)
)

plt.grid(True)

plt.xlabel("Frequency [Hz]")
plt.ylabel("|Gxx| [m/N]")

plt.title("Tool Tip FRF")

plt.show()

print(hasattr(tool_rot, "frf"))

freq = np.linspace(1, 30000, 500)

Gxx = tool_rot.frf(freq)

print("FRF shape:", Gxx.shape)
print("Max receptance:", np.max(np.abs(Gxx)))

import matplotlib.pyplot as plt

plt.plot([1,2,3],[1,4,9])
plt.show()

import matplotlib.pyplot as plt

plt.figure()

plt.plot(
    [0, 1, 2, 3],
    [0, 1, 0, 1]
)

plt.grid(True)

plt.show()

Hcc, Hcb, Hbc, Hbb = tool_rot.receptance_blocks(freq)

print()
print("Hcc shape :", Hcc.shape)
print("Hcb shape :", Hcb.shape)
print("Hbc shape :", Hbc.shape)
print("Hbb shape :", Hbb.shape)


freq = np.linspace(
    1,
    5000,
    500
)

Hcc, Hcb, Hbc, Hbb = (
    tool_rot.receptance_blocks(freq)
)

print()
print("Hcc:", Hcc.shape)
print("Hcb:", Hcb.shape)
print("Hbc:", Hbc.shape)
print("Hbb:", Hbb.shape)

Hsp = spindle_frf(freq)

Htool = couple(
    Hcc,
    Hcb,
    Hbc,
    Hbb,
    Hsp
)

Gxx = Htool[:,0,0]

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

plt.semilogy(
    freq,
    np.abs(Gxx)
)

plt.grid(True)

plt.xlabel("Frequency [Hz]")
plt.ylabel("|Gxx|")

plt.title(
    "RCSA Coupled Tool Tip FRF"
)

plt.show()

Hsp = spindle_frf(freq)

Htool = couple(
    Hcc,
    Hcb,
    Hbc,
    Hbb,
    Hsp
)

print()
print("Htool:", Htool.shape)

Gxx = Htool[:,0,0]

print(
    "Max coupled receptance:",
    np.max(np.abs(Gxx))
)