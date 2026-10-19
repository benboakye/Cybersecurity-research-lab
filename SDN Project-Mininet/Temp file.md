lscpu | grep -E '^(CPU\(s\)|Model name|Hypervisor vendor):'

python -m pip freeze > sample_output/environment_packages_n50.txt
