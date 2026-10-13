sh ovs-ofctl -O OpenFlow13 dump-flows s1


sudo mn -c
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6653 --switch ovsk,protocols=OpenFlow13


curl -i -u admin:admin \
-H "Accept: application/yang-data+json" \
"http://127.0.0.1:8181/rests/data/opendaylight-inventory:nodes?content=nonconfig"


curl -i -u admin:admin -X PUT \
"http://127.0.0.1:8181/rests/data/opendaylight-inventory:nodes/node=openflow%3A1/table=0/flow=101" \
-H "Content-Type: application/yang-data+json" \
-d '{
  "flow": [{
    "id": "101",
    "table_id": 0,
    "priority": 100,
    "flow-name": "h1-to-h2",
    "match": {
      "in-port": "1"
    },
    "instructions": {
      "instruction": [{
        "order": 0,
        "apply-actions": {
          "action": [{
            "order": 0,
            "output-action": {
              "output-node-connector": "2"
            }
          }]
        }
      }]
    }
  }]
}'
