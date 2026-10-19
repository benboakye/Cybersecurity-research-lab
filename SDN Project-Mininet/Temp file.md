cp sample_output/benchmark_results.csv sample_output/classical_baseline_ubuntu_n10.csv


bash sample_data/generate_sample_keys.sh

python legacy_app/crypto_inventory_scanner.py sample_data --source-dir legacy_app
