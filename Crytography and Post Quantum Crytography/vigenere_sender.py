import socket

PORT = 5001


def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key_index = 0

    key = key.upper()

    for char in plaintext:

        if char.isalpha():
            # Convert plaintext letter to number 0-25
            p = ord(char.upper()) - ord('A')

            # Select corresponding key character
            key_char = key[key_index % len(key)]

            # Convert key character to number 0-25
            k = ord(key_char) - ord('A')

            # Vigenere encryption formula
            c = (p + k) % 26

            # Convert encrypted value back to a letter
            ciphertext += chr(c + ord('A'))

            # Move to next key character
            key_index += 1

        else:
            # Preserve spaces and other non-alphabetic characters
            ciphertext += char

    return ciphertext


def main():
    print("=== Vigenere Sender ===\n")

    message = input(
        'Enter the message "TO BE OR NOT TO BE THAT IS THE QUESTION": '
    )

    key = input(
        'Enter the Vigenere key "RELATIONS": '
    )

    receiver_ip = input(
        "Enter VM2 Receiver IP address: "
    )

    ciphertext = vigenere_encrypt(message, key)

    print("\n--- Vigenere Encryption ---")
    print("Original Message :", message)
    print("Encryption Key   :", key)
    print("Encrypted Message:", ciphertext)

    print(f"\nConnecting to {receiver_ip}:{PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # Connect to VM2
            sock.connect((receiver_ip, PORT))

            # Send encrypted message
            sock.sendall(ciphertext.encode("utf-8"))

            print("Ciphertext successfully sent to VM2.")

    except ConnectionRefusedError:
        print("\nConnection refused.")
        print("Make sure vigenere_receiver.py is running on VM2.")

    except OSError as error:
        print(f"\nNetwork error: {error}")


if __name__ == "__main__":
    main()
