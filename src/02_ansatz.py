from qiskit.circuit.library import n_local

ansatz = n_local(
    num_qubits=4,
    rotation_blocks=["ry", "rz"],
    entanglement_blocks="cz",
    entanglement="linear",
    reps=2,
)

print("Number of qubits:", ansatz.num_qubits)
print("Number of tunable parameters:", ansatz.num_parameters)
print()
print(ansatz)