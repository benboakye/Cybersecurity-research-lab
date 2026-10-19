python - <<'PY'
import os
from cryptography.exceptions import InvalidTag
from crypto_common import derive_aes_key, seal_document, open_document

document = b"Loan Amount: $10,000"
key = derive_aes_key(os.urandom(32))

envelope = seal_document(document, key)
print("Original decrypts:", open_document(envelope, key) == document)

tampered = bytearray(envelope)
tampered[16] ^= 1  # Modify one ciphertext bit

try:
    open_document(bytes(tampered), key)
    print("Tampered ciphertext: ACCEPTED")
except InvalidTag:
    print("Tampered ciphertext: REJECTED")
PY
