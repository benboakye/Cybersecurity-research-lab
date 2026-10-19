python - <<'PY'
import os
from cryptography.exceptions import InvalidTag
from crypto_common import derive_aes_key, seal_document, open_document

document = b"Confidential Loan Agreement"

correct_key = derive_aes_key(os.urandom(32))
wrong_key = derive_aes_key(os.urandom(32))

envelope = seal_document(document, correct_key)

print("Correct key decrypts:",
      open_document(envelope, correct_key) == document)

try:
    open_document(envelope, wrong_key)
    print("Wrong key: ACCEPTED")
except InvalidTag:
    print("Wrong key: REJECTED")
PY
