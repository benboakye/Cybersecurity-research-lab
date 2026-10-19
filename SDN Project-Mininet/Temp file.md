sed -i 's/NORTHBRIDGE CAPITAL/CPQCtech Solution/g' improved_app/crypto_inventory_scanner.py

python improved_app/crypto_inventory_scanner.py sample_data --source-dir legacy_app | sed -n '1,13p'
