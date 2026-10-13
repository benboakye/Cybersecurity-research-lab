{
  lsb_release -d
  java -version 2>&1
  mn --version
  ovs-vsctl --version | head -n 1
} | tee ~/SDN-Project/Evidence/system-versions.txt
