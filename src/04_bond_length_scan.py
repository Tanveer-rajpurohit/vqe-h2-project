import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import n_local
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA

pauli_strings = ["IIII", "IIIZ", "IIZI", "IZII", "ZIII", "IIZZ", "IZIZ", "ZIIZ", "YYYY", "XXYY", "YYXX", "XXXX", "IZZI", "ZIZI", "ZZII"]
coeffs = [-0.81054798, 0.17218393, -0.22575349, 0.17218393, -0.22575349, 0.12091263, 0.16892754, 0.16614543, 0.0452328, 0.0452328, 0.0452328, 0.0452328, 0.16614543, 0.17464343, 0.12091263]
hamiltonian = SparsePauliOp(pauli_strings, coeffs=coeffs)
NUCLEAR_REPULSION = 1 / 1.3892

ansatz = n_local(
    num_qubits=4,
    rotation_blocks=["ry", "rz"],
    entanglement_blocks="cz",
    entanglement="linear",
    reps=2,
)

energy_history = []
def store_energy(eval_count, params, mean, std):
    energy_history.append(mean + NUCLEAR_REPULSION) 

estimator = StatevectorEstimator()
optimizer = COBYLA(maxiter=300)

np.random.seed(42)
initial_point = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)

vqe = VQE(estimator, ansatz, optimizer, initial_point=initial_point, callback=store_energy)
result = vqe.compute_minimum_eigenvalue(hamiltonian)

final_total_energy = result.eigenvalue.real + NUCLEAR_REPULSION
exact_energy = -1.137270


plt.figure(figsize=(8, 5))
plt.plot(range(1, len(energy_history) + 1), energy_history, label="VQE energy per iteration")
plt.axhline(y=exact_energy, color="red", linestyle="--", label=f"Exact ground state ({exact_energy} Ha)")
plt.xlabel("Optimizer iteration")
plt.ylabel("Total molecular energy (Hartree)")
plt.title("VQE Convergence for H$_2$ Ground State Energy")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("results/convergence_plot.png", dpi=150)


plt.figure(figsize=(5, 5))
labels = ["VQE (this project)", "Exact (reference)"]
values = [final_total_energy, exact_energy]
colors = ["#1f77b4", "#d62728"]
bars = plt.bar(labels, values, color=colors)
plt.ylabel("Total molecular energy (Hartree)")
plt.title("VQE vs Exact Ground State Energy (H$_2$)")
plt.grid(True, axis="y", alpha=0.3)
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, val - 0.05, f"{val:.4f}",
              ha="center", va="top", color="white", fontweight="bold")
plt.tight_layout()
plt.savefig("results/comparison_bar_chart.png", dpi=150)
print("Bar chart saved to results/comparison_bar_chart.png")

print("Final VQE total energy:", final_total_energy, "Hartree")
print("Exact reference energy:", exact_energy, "Hartree")
print("Absolute error:", abs(final_total_energy - exact_energy), "Hartree")
print("Plot saved to results/convergence_plot.png")