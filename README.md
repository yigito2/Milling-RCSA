# Milling-RCSA

> Python-based engineering framework for tool dynamics, receptance coupling, chatter prediction and future 5-axis compensation.

docs/images/project-roadmap.png

---

## Features

### Current

- Timoshenko Beam FEM
- Consistent Mass Matrix
- Rotary Inertia
- Modal Analysis
- Tool Tip FRF
- Receptance Blocks

### Planned

- RCSA Coupling
- Experimental Spindle FRF Import
- Stability Lobe Diagrams
- Bi-Planar 4x4 Beam Model
- 3D 6x6 Beam Model
- 6x6 RCSA
- 5-Axis Deflection Compensation

---

## Project Structure

```text
milling_rcsa/
│
├── config/
├── data/
├── docs/
│   └── images/
├── fem/
│   ├── timoshenko.py
│   └── beam2d.py
├── modal/
├── rcsa/
├── plots/
├── main.py
└── requirements.txt