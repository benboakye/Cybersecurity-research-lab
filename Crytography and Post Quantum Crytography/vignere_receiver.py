import socket

KEY = "RELATIONS"
PORT = 5001


def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_index = 0

    key = key.upper()

    for char in ciphertext:

        if char.isalpha():
            # Convert ciphertext letter to number 0-25
            c = ord(char.upper()) - ord('A')

            # Get corresponding key character
            key_char = key[key_index % len(key)]

            # Convert key character to number 0-25
            k = ord(key_char) - ord('A')

            # Vigenere decryption formula
            p = (c - k) % 26

            # Convert number back to letter
            plaintext += chr(p + ord('A'))

            # Move to next key character
            key_index += 1

        else:
            # Preserve spaces and other non-alphabetic characters
            plaintext += char

    return plaintext


def main():
    print("=== Vigenere Receiver ===")
    print(f"Waiting for connection on port {PORT}...\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        # Allow the port to be reused quickly after restarting
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Listen on all network interfaces
        server.bind(("0.0.0.0", PORT))

        # Allow one incoming connection
        server.listen(1)

        conn, addr = server.accept()

        with conn:
            print(f"Connected by: {addr[0]}:{addr[1]}")

            data = conn.recv(4096)

            if not data:
                print("No data received.")
                return

            ciphertext = data.decode("utf-8")

            decrypted_message = vigenere_decrypt(
                ciphertext,
                KEY
            )

            print("\n--- Vigenere Decryption ---")
            print("Received Encrypted Message :", ciphertext)
            print("Decryption Key             :", KEY)
            print("Decrypted Message          :", decrypted_message)


if __name__ == "__main__":
    main()
