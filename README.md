# VQE for H2 Ground State Energy

Capstone project for Quantum Computing, Uka Tarsadia University (2026). This computes the ground-state energy of a hydrogen molecule (H2) using the Variational Quantum Eigensolver (VQE) algorithm on a simulated quantum computer, and checks the result against the exact, classically-known answer.

## Why this project

A molecule's ground-state energy is the lowest possible energy its electrons can settle into at a given bond distance. For most molecules, computing this exactly gets exponentially harder as the molecule grows, which is one of the main reasons quantum computers are expected to eventually help with chemistry simulation. H2 is the smallest molecule with a real chemical bond, and its exact ground-state energy is already known from classical chemistry — about -1.137 Hartree at its natural bond length of 0.735 Angstrom. That makes it the standard first test case: if a quantum method can't reproduce a known answer, it isn't ready to be trusted on molecules where the answer isn't known in advance.

This project builds that pipeline from scratch: turn the molecule into a form a quantum circuit can work with, build a small parameterized circuit that represents a guess at the ground state, and let a classical optimizer tune that guess until the measured energy stops improving.

## What's in this repo

```
vqe-h2-project/
├── src/
│   ├── 01_hamiltonian.py       builds H2's qubit Hamiltonian
│   ├── 02_ansatz.py            builds the parameterized circuit (ansatz)
│   ├── 03_vqe_run.py           runs the VQE optimization loop
│   └── 04_bond_length_scan.py  plots convergence and the final energy comparison
├── results/                    saved plots from running the scripts above
├── paper/                      LaTeX source for the written report
└── requirements.txt
```

## How it works, briefly

1. **Hamiltonian** (`01_hamiltonian.py`) — PySCF works out H2's electronic structure using the sto-3g basis set, and a Jordan-Wigner mapping turns that into a Hamiltonian written in terms of qubits: a weighted sum of Pauli operators. That's the object VQE tries to minimize the energy of. For H2 in this basis, this comes out to 4 qubits.
2. **Ansatz** (`02_ansatz.py`) — a hardware-efficient parameterized circuit (24 tunable parameters) representing a flexible guess at what the ground state might look like.
3. **VQE loop** (`03_vqe_run.py`) — the circuit's energy is measured, a classical optimizer (COBYLA) nudges the parameters to lower it, and this repeats for up to 300 iterations or until it stops improving.
4. **Evaluation** (`04_bond_length_scan.py`) — plots the energy dropping over the optimization run, and a bar chart comparing the final VQE result against the exact answer, computed classically since H2 is small enough to solve exactly.

## Setup

```
python -m venv venv
```

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

Then:
```
pip install -r requirements.txt
```

`pyscf` is a compiled chemistry library and occasionally fails to build on native Windows. If that happens, WSL or a conda environment usually resolves it.

## Running it

Run the scripts in order:

```
python src/01_hamiltonian.py
python src/02_ansatz.py
python src/03_vqe_run.py
python src/04_bond_length_scan.py
```

Each one prints its own output; the last one saves plots to `results/`.

## Results

At the equilibrium bond length (0.735 Angstrom):

| | Energy (Hartree) |
|---|---|
| VQE (this project) | -1.11712 |
| Exact (classical reference) | -1.13727 |
| Absolute error | 0.02015 |

The gap comes from using a generic hardware-efficient ansatz with a fixed iteration budget, rather than a chemistry-specific ansatz like UCCSD, which would close more of it at the cost of a larger circuit. Quantum chemists generally define "chemical accuracy" as being within about 0.0016 Hartree of the exact answer — this result doesn't reach that bar, but it wasn't tuned to; a UCCSD ansatz and a larger iteration budget would be the natural next step for closing it further.

See `results/convergence_plot.png` for how the energy drops over the optimization run, and `results/comparison_bar_chart.png` for the final VQE-vs-exact comparison.

## Author

Tanveer Singh, B.Tech Computer Science Engineering, Uka Tarsadia University.