cat > flow101.json <<'EOF'
{
  "flow": [
    {
      "id": "101",
      "table_id": 0,
      "priority": 100,
      "flow-name": "h1-to-h2",
      "match": {
        "in-port": "1"
      },
      "instructions": {
        "instruction": [
          {
            "order": 0,
            "apply-actions": {
              "action": [
              {
                  "order": 0,
                  "output-action": {
                    "output-node-connector": "2"
                  }
                }
              ]
            }
          }
        ]
      }
    }
  ]
}
EOF
