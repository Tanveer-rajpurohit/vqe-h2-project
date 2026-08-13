from qiskit.quantum_info import SparsePauliOp

# H2 qubit Hamiltonian: STO-3G basis, bond length 0.735 Angstrom, Jordan-Wigner mapping.
# These coefficients come from the molecule's classical Hartree-Fock calculation
# (the same numbers PySCF + Qiskit Nature would produce)
pauli_strings = ["IIII", "IIIZ", "IIZI", "IZII", "ZIII", "IIZZ", "IZIZ", "ZIIZ","YYYY", "XXYY", "YYXX", "XXXX", "IZZI", "ZIZI", "ZZII"]
coeffs = [-0.81054798, 0.17218393, -0.22575349, 0.17218393, -0.22575349, 0.12091263, 0.16892754, 0.16614543, 0.0452328, 0.0452328, 0.0452328, 0.0452328, 0.16614543, 0.17464343, 0.12091263]

hamiltonian = SparsePauliOp(pauli_strings, coeffs=coeffs)

print("Number of qubits required:", hamiltonian.num_qubits)
print("\nQubit Hamiltonian (Pauli terms):")
print(hamiltonian)