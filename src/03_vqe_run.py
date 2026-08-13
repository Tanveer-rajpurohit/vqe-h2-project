import numpy as np
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import n_local
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA


# --- rebuild the Hamiltonian (this is the ELECTRONIC part only) ---
pauli_strings = ["IIII", "IIIZ", "IIZI", "IZII", "ZIII", "IIZZ", "IZIZ", "ZIIZ", "YYYY", "XXYY", "YYXX", "XXXX", "IZZI", "ZIZI", "ZZII"]
coeffs = [-0.81054798, 0.17218393, -0.22575349, 0.17218393, -0.22575349, 0.12091263, 0.16892754, 0.16614543, 0.0452328, 0.0452328, 0.0452328, 0.0452328, 0.16614543, 0.17464343, 0.12091263]
hamiltonian = SparsePauliOp(pauli_strings, coeffs=coeffs)

NUCLEAR_REPULSION = 1 / 1.3892 # ~0.71968 Hartree

ansatz = n_local(
    num_qubits=4,
    rotation_blocks=["ry", "rz"],
    entanglement_blocks="cz",
    entanglement="linear",
    reps=2,
)

energy_history = []
def store_energy(eval_count, params, mean, std):
    energy_history.append(mean)

estimator = StatevectorEstimator()
optimizer = COBYLA(maxiter=300)

np.random.seed(42)
initial_point = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)

vqe = VQE(estimator, ansatz, optimizer, initial_point=initial_point, callback=store_energy)
result = vqe.compute_minimum_eigenvalue(hamiltonian)

electronic_energy = result.eigenvalue.real
total_energy = electronic_energy + NUCLEAR_REPULSION

print("VQE electronic ground state energy:", electronic_energy, "Hartree")
print("Nuclear repulsion energy:", NUCLEAR_REPULSION, "Hartree")
print("VQE TOTAL molecular energy:", total_energy, "Hartree")
print("Known exact total energy (reference):    -1.137270 Hartree")
print("Difference from exact:", abs(total_energy - (-1.137270)), "Hartree")
print("Number of optimizer iterations:", len(energy_history))