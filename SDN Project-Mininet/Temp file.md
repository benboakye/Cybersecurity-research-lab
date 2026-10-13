echo "=== Ubuntu Version ==="
lsb_release -a

echo "=== CPU ==="
nproc

echo "=== Memory ==="
free -h

echo "=== Disk Space ==="
df -h /

echo "=== Network Interfaces ==="
ip -br addr

echo "=== Internet Connectivity ==="
ping -c 4 8.8.8.8

echo "=== Virtualization Support ==="
sudo ip netns add sdn-test &&
sudo ip netns delete sdn-test
