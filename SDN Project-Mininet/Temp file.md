python - <<'PY'
import os
from cryptography.exceptions import InvalidTag
from crypto_common import derive_aes_key, seal_document, open_document

document = b"Loan Amount: $10,000"
aes_key = derive_aes_key(os.urandom(32))

envelope = seal_document(document, aes_key)
print("Original decrypts:",
      open_document(envelope, aes_key) == document)

tampered = bytearray(envelope)
tampered[-1] ^= 1

try:
    open_document(bytes(tampered), aes_key)
    print("Tampered ciphertext: ACCEPTED")
except InvalidTag:
    print("Tampered ciphertext: REJECTED")
PY
