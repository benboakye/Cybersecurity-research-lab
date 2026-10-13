sh ovs-ofctl -O OpenFlow13 dump-flows s1


sudo mn -c
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6653 --switch ovsk,protocols=OpenFlow13


curl -i -u admin:admin \
-H "Accept: application/yang-data+json" \
"http://127.0.0.1:8181/rests/data/opendaylight-inventory:nodes?content=nonconfig"
