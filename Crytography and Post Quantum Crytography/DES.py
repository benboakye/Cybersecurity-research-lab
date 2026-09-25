import socket
import secrets

PORT = 5002
BLOCK_SIZE = 8


# =========================================================
# DES TABLES
# =========================================================

# Initial Permutation
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]


# Final Permutation
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]


# Expansion permutation: 32 bits -> 48 bits
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]


# Permutation after S-box substitution
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]


# Permuted Choice 1
# Removes 8 parity bits:
# 64-bit supplied key -> 56 effective key bits
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,

    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]


# Permuted Choice 2
# 56-bit combined key halves -> 48-bit round key
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,

    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]


# Number of left shifts performed in each DES round
SHIFTS = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]


# =========================================================
# DES S-BOXES
# Each S-box maps 6 input bits to 4 output bits
# =========================================================

S_BOXES = [

    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8,
         3, 10, 6, 12, 5, 9, 0, 7],

        [0, 15, 7, 4, 14, 2, 13, 1,
         10, 6, 12, 11, 9, 5, 3, 8],

        [4, 1, 14, 8, 13, 6, 2, 11,
         15, 12, 9, 7, 3, 10, 5, 0],

        [15, 12, 8, 2, 4, 9, 1, 7,
         5, 11, 3, 14, 10, 0, 6, 13]
    ],

    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4,
         9, 7, 2, 13, 12, 0, 5, 10],

        [3, 13, 4, 7, 15, 2, 8, 14,
         12, 0, 1, 10, 6, 9, 11, 5],

        [0, 14, 7, 11, 10, 4, 13, 1,
         5, 8, 12, 6, 9, 3, 2, 15],

        [13, 8, 10, 1, 3, 15, 4, 2,
         11, 6, 7, 12, 0, 5, 14, 9]
    ],

    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5,
         1, 13, 12, 7, 11, 4, 2, 8],

        [13, 7, 0, 9, 3, 4, 6, 10,
         2, 8, 5, 14, 12, 11, 15, 1],

        [13, 6, 4, 9, 8, 15, 3, 0,
         11, 1, 2, 12, 5, 10, 14, 7],

        [1, 10, 13, 0, 6, 9, 8, 7,
         4, 15, 14, 3, 11, 5, 2, 12]
    ],

    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10,
         1, 2, 8, 5, 11, 12, 4, 15],

        [13, 8, 11, 5, 6, 15, 0, 3,
         4, 7, 2, 12, 1, 10, 14, 9],

        [10, 6, 9, 0, 12, 11, 7, 13,
         15, 1, 3, 14, 5, 2, 8, 4],

        [3, 15, 0, 6, 10, 1, 13, 8,
         9, 4, 5, 11, 12, 7, 2, 14]
    ],

    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6,
         8, 5, 3, 15, 13, 0, 14, 9],

        [14, 11, 2, 12, 4, 7, 13, 1,
         5, 0, 15, 10, 3, 9, 8, 6],

        [4, 2, 1, 11, 10, 13, 7, 8,
         15, 9, 12, 5, 6, 3, 0, 14],

        [11, 8, 12, 7, 1, 14, 2, 13,
         6, 15, 0, 9, 10, 4, 5, 3]
    ],

    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8,
         0, 13, 3, 4, 14, 7, 5, 11],

        [10, 15, 4, 2, 7, 12, 9, 5,
         6, 1, 13, 14, 0, 11, 3, 8],

        [9, 14, 15, 5, 2, 8, 12, 3,
         7, 0, 4, 10, 1, 13, 11, 6],

        [4, 3, 2, 12, 9, 5, 15, 10,
         11, 14, 1, 7, 6, 0, 8, 13]
    ],

    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13,
         3, 12, 9, 7, 5, 10, 6, 1],

        [13, 0, 11, 7, 4, 9, 1, 10,
         14, 3, 5, 12, 2, 15, 8, 6],

        [1, 4, 11, 13, 12, 3, 7, 14,
         10, 15, 6, 8, 0, 5, 9, 2],

        [6, 11, 13, 8, 1, 4, 10, 7,
         9, 5, 0, 15, 14, 2, 3, 12]
    ],

    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1,
         10, 9, 3, 14, 5, 0, 12, 7],

        [1, 15, 13, 8, 10, 3, 7, 4,
         12, 5, 6, 11, 0, 14, 9, 2],

        [7, 11, 4, 1, 9, 12, 14, 2,
         0, 6, 10, 13, 15, 3, 5, 8],

        [2, 1, 14, 7, 4, 10, 8, 13,
         15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def bytes_to_bits(data):
    """Convert bytes to a string of binary bits."""
    return ''.join(f'{byte:08b}' for byte in data)


def bits_to_bytes(bits):
    """Convert binary bit string back to bytes."""
    return bytes(
        int(bits[i:i + 8], 2)
        for i in range(0, len(bits), 8)
    )


def permute(bits, table):
    """Rearrange bits according to a DES permutation table."""
    return ''.join(bits[position - 1] for position in table)


def xor_bits(a, b):
    """XOR two equal-length binary strings."""
    return ''.join(
        '0' if bit1 == bit2 else '1'
        for bit1, bit2 in zip(a, b)
    )


def left_rotate(bits, amount):
    """Circular left shift."""
    return bits[amount:] + bits[:amount]


def group_bits(bits, group=8):
    """Format binary output for easier reading."""
    return ' '.join(
        bits[i:i + group]
        for i in range(0, len(bits), group)
    )


# =========================================================
# DES KEY SCHEDULE
# =========================================================

def generate_round_keys(key_bits):
    """
    Generate sixteen 48-bit DES round keys
    from the supplied 64-bit key.
    """

    # PC-1 reduces the supplied 64-bit representation
    # to the 56 effective DES key bits.
    key_56 = permute(key_bits, PC1)

    left = key_56[:28]
    right = key_56[28:]

    round_keys = []

    for shift in SHIFTS:
        left = left_rotate(left, shift)
        right = left_rotate(right, shift)

        combined = left + right

        # PC-2 produces the 48-bit round key
        round_key = permute(combined, PC2)

        round_keys.append(round_key)

    return round_keys


# =========================================================
# DES FEISTEL FUNCTION
# =========================================================

def feistel_function(right_half, round_key):
    """
    DES F-function:
    1. Expand 32 bits to 48 bits
    2. XOR with round key
    3. Pass through eight S-boxes
    4. Apply P permutation
    """

    expanded = permute(right_half, E)

    mixed = xor_bits(expanded, round_key)

    sbox_output = ""

    sbox1_input = None
    sbox1_output = None

    for box_number in range(8):

        start = box_number * 6
        six_bits = mixed[start:start + 6]

        # Row = first and last bit
        row_bits = six_bits[0] + six_bits[5]
        row = int(row_bits, 2)

        # Column = middle four bits
        column_bits = six_bits[1:5]
        column = int(column_bits, 2)

        value = S_BOXES[box_number][row][column]

        four_bits = f'{value:04b}'

        # Capture S-box 1 input/output for lab display
        if box_number == 0:
            sbox1_input = six_bits
            sbox1_output = four_bits

        sbox_output += four_bits

    result = permute(sbox_output, P)

    return result, sbox1_input, sbox1_output


# =========================================================
# ENCRYPT ONE 64-BIT DES BLOCK
# =========================================================

def des_encrypt_block(block_bytes, key_bytes):
    block_bits = bytes_to_bits(block_bytes)
    key_bits = bytes_to_bits(key_bytes)

    # Step 1: Initial Permutation
    initial_permutation = permute(block_bits, IP)

    left = initial_permutation[:32]
    right = initial_permutation[32:]

    round_keys = generate_round_keys(key_bits)

    first_sbox1_input = None
    first_sbox1_output = None

    # Step 2: Sixteen Feistel rounds
    for round_number in range(16):

        f_output, s1_input, s1_output = feistel_function(
            right,
            round_keys[round_number]
        )

        if round_number == 0:
            first_sbox1_input = s1_input
            first_sbox1_output = s1_output

        new_right = xor_bits(left, f_output)

        left = right
        right = new_right

    # DES swaps halves before final permutation
    combined = right + left

    # Step 3: Final Permutation
    final_permutation = permute(combined, FP)

    ciphertext_block = bits_to_bytes(final_permutation)

    trace = {
        "initial_permutation": initial_permutation,
        "sbox1_input": first_sbox1_input,
        "sbox1_output": first_sbox1_output,
        "final_permutation": final_permutation
    }

    return ciphertext_block, trace


# =========================================================
# PADDING
# =========================================================

def pkcs5_pad(data):
    """
    DES uses an 8-byte block.
    PKCS#5 padding fills the final incomplete block.
    """

    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)

    return data + bytes(
        [padding_length] * padding_length
    )


# =========================================================
# ENCRYPT COMPLETE MESSAGE
# =========================================================

def des_encrypt_message(plaintext, key_bytes):

    plaintext_bytes = plaintext.encode("utf-8")

    padded_data = pkcs5_pad(plaintext_bytes)

    ciphertext = b""

    first_block_trace = None

    for block_start in range(0, len(padded_data), BLOCK_SIZE):

        block = padded_data[
            block_start:block_start + BLOCK_SIZE
        ]

        encrypted_block, trace = des_encrypt_block(
            block,
            key_bytes
        )

        ciphertext += encrypted_block

        # We only need one example of the internal
        # DES stages for the required lab display.
        if first_block_trace is None:
            first_block_trace = trace

    return ciphertext, first_block_trace


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("=== DES Sender ===\n")

    plaintext = input(
        'Enter the message "No body can see me": '
    )

    receiver_ip = input(
        "Enter VM2 Receiver IP address: "
    )

    # Generate an 8-byte (64-bit stored) DES key.
    # DES uses 56 effective key bits after PC-1.
    key_bytes = secrets.token_bytes(8)

    ciphertext, trace = des_encrypt_message(
        plaintext,
        key_bytes
    )

    key_hex = key_bytes.hex().upper()
    ciphertext_hex = ciphertext.hex().upper()

    print("\n--- DES Encryption ---")

    print("Plaintext:")
    print(plaintext)

    print("\nDES Key (Hex):")
    print(key_hex)

    print("\nDES Key (64-bit representation):")
    print(
        group_bits(
            bytes_to_bits(key_bytes)
        )
    )

    print("\nInitial Permutation - First 64-bit Block:")
    print(
        group_bits(
            trace["initial_permutation"]
        )
    )

    print("\nRound 1 - S-box 1 Input (6 bits):")
    print(trace["sbox1_input"])

    print("\nRound 1 - S-box 1 Output (4 bits):")
    print(trace["sbox1_output"])

    print("\nFinal Permutation - First 64-bit Block:")
    print(
        group_bits(
            trace["final_permutation"]
        )
    )

    print("\nCiphertext (Hex):")
    print(ciphertext_hex)

    print("\nIMPORTANT:")
    print(
        "Copy the DES Key shown above. "
        "VM2 must use exactly the same key."
    )

    input(
        "\nStart the DES receiver on VM2 using this key, "
        "then press ENTER here to send the ciphertext..."
    )

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.connect(
                (receiver_ip, PORT)
            )

            sock.sendall(ciphertext)

            print(
                f"\nCiphertext successfully sent "
                f"to {receiver_ip}:{PORT}"
            )

    except ConnectionRefusedError:

        print("\nConnection refused.")
        print(
            "Make sure des_receiver.py "
            "is running on VM2."
        )

    except OSError as error:

        print(
            f"\nNetwork error: {error}"
        )


if __name__ == "__main__":
    main()