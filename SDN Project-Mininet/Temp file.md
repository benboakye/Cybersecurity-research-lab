python - <<'PY'
from pqc_app.docuseal_pqc import (
    generate_signing_keypair,
    sign_document,
    verify_document
)

signer, public_key = generate_signing_keypair()

original = b"Loan Amount: $10,000"
tampered = b"Loan Amount: $90,000"

signature = sign_document(signer, original)

print("Algorithm: ML-DSA-65")
print("Original document valid:",
      verify_document(public_key, original, signature))
print("Tampered document valid:",
      verify_document(public_key, tampered, signature))
PY
