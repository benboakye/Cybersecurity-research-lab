mkdir -p improved_app/test_fixtures

cat > improved_app/test_fixtures/false_positive_demo.py <<'PY'
# padding.OAEP mentioned in a comment

"""padding.PSS mentioned in documentation"""

from cryptography.hazmat.primitives.asymmetric import rsa

def create_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=3072
    )
PY
