python -m pip install liboqs-python

python -c "import oqs; print('KEM:', oqs.get_enabled_kem_mechanisms()); print('Signatures:', oqs.get_enabled_sig_mechanisms())"
