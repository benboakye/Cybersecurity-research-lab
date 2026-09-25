import socket

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


# Expansion permutation
# Expands 32 bits to 48 bits
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


# Permutation performed after S-box substitution
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
# Converts the supplied 64-bit key representation
# into the 56 effective DES key bits
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
# Produces each 48-bit DES round key
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


# Left rotations for the sixteen rounds
SHIFTS = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]


# =========================================================
# DES S-BOXES
# Each S-box converts 6 input bits to 4 output bits
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
    """
    Convert bytes into a binary string.
    Each byte becomes 8 bits.
    """
    return ''.join(
        f'{byte:08b}'
        for byte in data
    )


def bits_to_bytes(bits):
    """
    Convert a binary string back into bytes.
    """
    return bytes(
        int(bits[i:i + 8], 2)
        for i in range(0, len(bits), 8)
    )


def permute(bits, table):
    """
    Rearrange bits according to the specified DES table.
    """
    return ''.join(
        bits[position - 1]
        for position in table
    )


def xor_bits(a, b):
    """
    Perform bit-by-bit XOR.
    """
    return ''.join(
        '0' if bit1 == bit2 else '1'
        for bit1, bit2 in zip(a, b)
    )


def left_rotate(bits, amount):
    """
    Circular left rotation.
    """
    return bits[amount:] + bits[:amount]


# =========================================================
# DES KEY SCHEDULE
# =========================================================

def generate_round_keys(key_bits):
    """
    Generate the sixteen 48-bit DES round keys.
    """

    # Remove the parity positions:
    # 64-bit representation -> 56 effective key bits
    key_56 = permute(key_bits, PC1)

    left = key_56[:28]
    right = key_56[28:]

    round_keys = []

    for shift in SHIFTS:

        left = left_rotate(left, shift)
        right = left_rotate(right, shift)

        combined = left + right

        round_key = permute(
            combined,
            PC2
        )

        round_keys.append(
            round_key
        )

    return round_keys


# =========================================================
# DES FEISTEL FUNCTION
# =========================================================

def feistel_function(right_half, round_key):
    """
    Perform the DES F-function.

    Steps:
    1. Expand right half from 32 to 48 bits.
    2. XOR it with the 48-bit round key.
    3. Pass the result through eight S-boxes.
    4. Apply the P permutation.
    """

    # Expand 32 bits to 48 bits
    expanded = permute(
        right_half,
        E
    )

    # XOR with round key
    mixed = xor_bits(
        expanded,
        round_key
    )

    sbox_output = ""

    # Process eight groups of six bits
    for box_number in range(8):

        start = box_number * 6

        six_bits = mixed[
            start:start + 6
        ]

        # First and last bits determine the row
        row_bits = (
            six_bits[0] +
            six_bits[5]
        )

        row = int(
            row_bits,
            2
        )

        # Middle four bits determine the column
        column_bits = six_bits[1:5]

        column = int(
            column_bits,
            2
        )

        value = S_BOXES[
            box_number
        ][row][column]

        four_bits = f'{value:04b}'

        sbox_output += four_bits

    # Final permutation inside the F-function
    result = permute(
        sbox_output,
        P
    )

    return result


# =========================================================
# DES BLOCK DECRYPTION
# =========================================================

def des_decrypt_block(ciphertext_block, key_bytes):
    """
    Decrypt one 8-byte / 64-bit DES ciphertext block.

    The DES encryption and decryption structures are
    essentially the same.

    The key difference is that decryption applies the
    sixteen round keys in reverse order.
    """

    ciphertext_bits = bytes_to_bits(
        ciphertext_block
    )

    key_bits = bytes_to_bits(
        key_bytes
    )

    # Step 1: Initial Permutation
    permuted_block = permute(
        ciphertext_bits,
        IP
    )

    # Divide into two 32-bit halves
    left = permuted_block[:32]
    right = permuted_block[32:]

    # Generate all sixteen round keys
    round_keys = generate_round_keys(
        key_bits
    )

    # IMPORTANT:
    # Reverse key order for DES decryption
    round_keys = round_keys[::-1]

    # Perform sixteen Feistel rounds
    for round_key in round_keys:

        f_output = feistel_function(
            right,
            round_key
        )

        new_right = xor_bits(
            left,
            f_output
        )

        left = right
        right = new_right

    # DES swaps the two halves
    combined = right + left

    # Apply final permutation
    plaintext_bits = permute(
        combined,
        FP
    )

    return bits_to_bytes(
        plaintext_bits
    )


# =========================================================
# COMPLETE MESSAGE DECRYPTION
# =========================================================

def des_decrypt_message(ciphertext, key_bytes):
    """
    Decrypt the complete ciphertext in 8-byte blocks.
    """

    plaintext = b""

    for start in range(
        0,
        len(ciphertext),
        BLOCK_SIZE
    ):

        block = ciphertext[
            start:start + BLOCK_SIZE
        ]

        decrypted_block = des_decrypt_block(
            block,
            key_bytes
        )

        plaintext += decrypted_block

    return plaintext


# =========================================================
# REMOVE PKCS#5 PADDING
# =========================================================

def pkcs5_unpad(data):
    """
    Remove the PKCS#5 padding that was added by
    the sender before DES encryption.
    """

    if not data:
        raise ValueError(
            "No decrypted data was produced."
        )

    padding_length = data[-1]

    if (
        padding_length < 1 or
        padding_length > BLOCK_SIZE
    ):
        raise ValueError(
            "Invalid PKCS#5 padding length."
        )

    expected_padding = bytes(
        [padding_length] *
        padding_length
    )

    actual_padding = data[
        -padding_length:
    ]

    if actual_padding != expected_padding:
        raise ValueError(
            "Invalid PKCS#5 padding bytes."
        )

    return data[
        :-padding_length
    ]


# =========================================================
# MAIN RECEIVER PROGRAM
# =========================================================

def main():

    print("=" * 50)
    print("DES RECEIVER - VM2")
    print("=" * 50)

    # -----------------------------------------------------
    # Obtain the shared DES key
    # -----------------------------------------------------

    key_hex = input(
        "\nEnter shared DES Key (Hex): "
    ).strip()

    try:

        key_bytes = bytes.fromhex(
            key_hex
        )

    except ValueError:

        print(
            "\nERROR: The DES key must contain "
            "valid hexadecimal characters."
        )

        return

    if len(key_bytes) != 8:

        print(
            "\nERROR: The DES key must be "
            "exactly 8 bytes."
        )

        print(
            "That means exactly "
            "16 hexadecimal characters."
        )

        return

    # -----------------------------------------------------
    # Start TCP server
    # -----------------------------------------------------

    print(
        f"\nWaiting for connection "
        f"on TCP port {PORT}..."
    )

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as server:

        # Allow quick reuse of the port
        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        # Listen on every network interface
        server.bind(
            ("0.0.0.0", PORT)
        )

        server.listen(1)

        # Wait until VM1 connects
        conn, addr = server.accept()

        with conn:

            print(
                f"\nConnected by "
                f"{addr[0]}:{addr[1]}"
            )

            chunks = []

            # Receive all ciphertext
            while True:

                data = conn.recv(4096)

                if not data:
                    break

                chunks.append(data)

            ciphertext = b"".join(
                chunks
            )

    # -----------------------------------------------------
    # Display received data
    # -----------------------------------------------------

    print("\n" + "=" * 50)
    print("DES DECRYPTION RESULTS")
    print("=" * 50)

    print(
        "\nReceived Ciphertext (Hex):"
    )

    print(
        ciphertext.hex().upper()
    )

    print(
        "\nShared DES Key (Hex):"
    )

    print(
        key_hex.upper()
    )

    # -----------------------------------------------------
    # Decrypt ciphertext
    # -----------------------------------------------------

    try:

        padded_plaintext = des_decrypt_message(
            ciphertext,
            key_bytes
        )

        plaintext_bytes = pkcs5_unpad(
            padded_plaintext
        )

        plaintext = plaintext_bytes.decode(
            "utf-8"
        )

    except Exception as error:

        print(
            f"\nDecryption Error: {error}"
        )

        return

    # -----------------------------------------------------
    # Display final plaintext
    # -----------------------------------------------------

    print(
        "\nDecrypted Message:"
    )

    print(
        plaintext
    )

    print("\n" + "=" * 50)

    print(
        "DES decryption completed successfully."
    )

    print("=" * 50)


if __name__ == "__main__":
    main()
