import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import eigh

from fem.timoshenko import (
    timoshenko_stiffness,
    timoshenko_mass,
    rotary_inertia
)


class ToolBeam:

    def __init__(
        self,
        D,
        L,
        E,
        rho,
        nu=0.22,
        n_elem=20,
        ks=6/7,
        use_rotary=True
    ):

        self.D = D
        self.L = L
        self.E = E
        self.rho = rho
        self.nu = nu

        self.G = E / (2 * (1 + nu))

        self.n_elem = n_elem
        self.ks = ks
        self.use_rotary = use_rotary

        self.A = np.pi * D**2 / 4
        self.I = np.pi * D**4 / 64

        self.build()

    def build(self):

        n_node = self.n_elem + 1

        self.n_node = n_node
        self.ndof = 2 * n_node

        K = np.zeros((self.ndof, self.ndof))
        M = np.zeros((self.ndof, self.ndof))

        Le = self.L / self.n_elem

        for e in range(self.n_elem):

            Ke = timoshenko_stiffness(
                self.E,
                self.G,
                self.I,
                self.A,
                Le,
                self.ks
            )

            Me = timoshenko_mass(
                self.rho,
                self.A,
                Le
            )

            if self.use_rotary:
                Me += rotary_inertia(
                    self.rho,
                    self.I,
                    Le
                )

            idx = [2*e, 2*e+1, 2*e+2, 2*e+3]

            K[np.ix_(idx, idx)] += Ke
            M[np.ix_(idx, idx)] += Me

        self.K = K
        self.M = M

    def apply_clamped_boundary(self):

        fixed = [0, 1]

        free = np.setdiff1d(
            np.arange(self.ndof),
            fixed
        )

        Kf = self.K[np.ix_(free, free)]
        Mf = self.M[np.ix_(free, free)]

        return Kf, Mf, free

    def natural_frequencies(self, n_modes=6):

        Kf, Mf, _ = self.apply_clamped_boundary()

        eigvals, _ = eigh(Kf, Mf)

        eigvals = eigvals[eigvals > 0]

        fn = np.sqrt(eigvals) / (2*np.pi)

        return fn[:n_modes]

    def modal_solution(self):

        Kf, Mf, free = self.apply_clamped_boundary()

        eigvals, eigvecs = eigh(Kf, Mf)

        mask = eigvals > 0

        eigvals = eigvals[mask]
        eigvecs = eigvecs[:, mask]

        fn = np.sqrt(eigvals) / (2*np.pi)

        return fn, eigvecs, free

    

    def plot_mode(self, mode_number):

        print(f"Plotting mode {mode_number}")

        fn, eigvecs, free = self.modal_solution()

        mode = mode_number - 1

        full_mode = np.zeros(self.ndof)

        full_mode[free] = eigvecs[:, mode]

        displacement = full_mode[0::2]

        displacement /= np.max(np.abs(displacement))

        x = np.linspace(
            0,
            self.L,
            len(displacement)
        )

        plt.figure(figsize=(8, 4))
        plt.plot(x, displacement, marker="o")
        plt.grid(True)

        plt.xlabel("Length [m]")
        plt.ylabel("Normalized displacement")


        plt.title(
            f"Mode {mode_number} - {fn[mode]:.1f} Hz"
        )
        plt.savefig(f"mode_{mode_number}.png")

        plt.show()

        print("Mode frequency:", fn[mode])

        print("Max displacement:", np.max(np.abs(displacement)))

    def receptance_blocks(self, freq):

        alpha = 0.0
        beta = 1e-7

        nf = len(freq)

        C = alpha * self.M + beta * self.K

        interface = [0, 1]

        tip = [
            self.ndof - 2,
            self.ndof - 1
        ]

        Hcc = np.zeros((nf, 2, 2), dtype=complex)
        Hcb = np.zeros((nf, 2, 2), dtype=complex)
        Hbc = np.zeros((nf, 2, 2), dtype=complex)
        Hbb = np.zeros((nf, 2, 2), dtype=complex)

        for i, f in enumerate(freq):

            w = 2 * np.pi * f

            D = (
                self.K
                - w**2 * self.M
                + 1j * w * C
            )

            H = np.linalg.inv(D)

            Hcc[i] = H[np.ix_(tip, tip)]

            Hcb[i] = H[np.ix_(tip, interface)]

            Hbc[i] = H[np.ix_(interface, tip)]

            Hbb[i] = H[np.ix_(interface, interface)]

        return Hcc, Hcb, Hbc, Hbb

        


        

    def frf(self, freq):

        Kf, Mf, free = self.apply_clamped_boundary()

        alpha = 0.0
        beta = 1e-7

        Cf = alpha * Mf + beta * Kf

        tip_disp = len(free) - 2

        Gxx = np.zeros(
            len(freq),
            dtype=complex
        )

        for i, f in enumerate(freq):

            w = 2 * np.pi * f

            D = (
                Kf
                - w**2 * Mf
                + 1j * w * Cf
            )

            H = np.linalg.inv(D)

            Gxx[i] = H[
                tip_disp,
                tip_disp
            ]

        return Gxx
    def receptance_blocks(self, freq):

        alpha = 0.0
        beta = 1e-7

        nf = len(freq)

        C = alpha * self.M + beta * self.K

        interface = [0, 1]

        tip = [
            self.ndof - 2,
            self.ndof - 1
        ]

        Hcc = np.zeros((nf, 2, 2), dtype=complex)
        Hcb = np.zeros((nf, 2, 2), dtype=complex)
        Hbc = np.zeros((nf, 2, 2), dtype=complex)
        Hbb = np.zeros((nf, 2, 2), dtype=complex)

        for i, f in enumerate(freq):

            w = 2 * np.pi * f

            D = (
                self.K
                - w**2 * self.M
                + 1j * w * C
            )

            H = np.linalg.inv(D)

            Hcc[i] = H[np.ix_(tip, tip)]
            Hcb[i] = H[np.ix_(tip, interface)]
            Hbc[i] = H[np.ix_(interface, tip)]
            Hbb[i] = H[np.ix_(interface, interface)]

        return Hcc, Hcb, Hbc, Hbb
