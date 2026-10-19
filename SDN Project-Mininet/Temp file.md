python - <<'PY'
from legacy_app.docuseal_classical import (
    generate_signing_keypair,
    sign_document,
    verify_document
)

private_key, public_key = generate_signing_keypair()

original = b"Loan Amount: $10,000"
tampered = b"Loan Amount: $90,000"

signature = sign_document(private_key, original)

print("Original document valid:",
      verify_document(public_key, original, signature))

print("Tampered document valid:",
      verify_document(public_key, tampered, signature))
PY
