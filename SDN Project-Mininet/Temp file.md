sh ovs-ofctl -O OpenFlow13 dump-flows s1


sudo mn -c
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6653 --switch ovsk,protocols=OpenFlow13
