import cirq
import secrets

# Message to encrypt
message = "One_state"

# Simulate key generation (not real QKD)
key_length = len(message)  # Key length matches message length
key = secrets.token_bytes(key_length)

def qubit_in_basis(basis):
    """Creates a qubit in the specified basis (rectilinear or diagonal)."""
    if basis == "rect":
        return cirq.H(cirq.GridQubit(0, 0))  # Hadamard for superposition
    elif basis == "diag":
        return cirq.H(cirq.rx(0.7854).on(cirq.GridQubit(0, 0)))  # Rx for diagonal
    else:
        raise ValueError("Invalid basis")

def introduce_errors(circuit, error_rate):
    """Applies depolarizing noise to the circuit with a given error rate."""
    for moment in circuit.moments:
        new_moment = []
        for op in moment.operations:
            # Apply depolarizing channel to each operation
            new_op = cirq.depolarize(error_rate).on(*op)
            new_moment.append(new_op)
        circuit.replace(moment, new_moment)
    return circuit

# Simulate key preparation circuits (Alice's program)
alice_circuits = []
for _ in range(key_length):
    basis = secrets.choice(["rect", "diag"])  # Randomly choose basis for each key bit
    alice_circuits.append(qubit_in_basis(basis))

# Simulate Bob's basis selection (Bob's program)
bob_circuits = []
for _ in range(key_length):
    bob_circuits.append(qubit_in_basis(secrets.choice(["rect", "diag"])))

# Simulate sifting with error checking (conceptually)
sifted_key = []
for alice_circuit, bob_circuit in zip(alice_circuits, bob_circuits):
    # Discard qubits with mismatched bases
    if alice_circuit == bob_circuit:
        # Introduce errors (already in circuit due to introduce_errors)
        # Simulate measurement (extract classical bit values)
        measurement = cirq.Simulator().run(alice_circuit, repetitions=1).measurements[0][0]
        sifted_key.append(measurement)

# Convert simulated key to binary string
simulated_key_bits = "".join(["0" if result == 0 else "1" for result in sifted_key])

# Encryption with XOR (simple example)
def encrypt_message(message, key):
    encrypted_message = ""
    for char, key_bit in zip(message, simulated_key_bits):
        encrypted_message += chr(ord(char) ^ int(key_bit))
    return encrypted_message

# Decryption with XOR
def decrypt_message(encrypted_message, key):
    decrypted_message = ""
    for char, key_bit in zip(encrypted_message, simulated_key_bits):
        decrypted_message += chr(ord(char) ^ int(key_bit))
    return decrypted_message

# Test encryption and decryption
encrypted_message = encrypt_message(message, simulated_key_bits)
decrypted_message = decrypt_message(encrypted_message, simulated_key_bits)

# Verify successful decryption
if decrypted_message == message:
    print("Decryption successful! Message recovered:", decrypted_message)
else:
    print("Decryption failed. Messages don't match.")
