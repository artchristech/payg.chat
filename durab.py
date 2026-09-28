import json, urllib.request
B='http://localhost:8899'
def req(path, body=None):
    r = urllib.request.Request(B+path, data=json.dumps(body).encode() if body is not None else None,
        headers={'Content-Type':'application/json'}, method='POST' if body is not None else 'GET')
    with urllib.request.urlopen(r, timeout=3) as resp:
        return json.loads(resp.read())
reg = req('/api/register', {'name':'durab'})
print('registered:', reg['agent_id'], 'balance', reg['balance'])
print('tip sent:', req('/api/tip', {'agent_id':reg['agent_id'],'key':reg['key'],'to':'durab2','amount':7}) if False else 'skip')
# write a marker: a tip needs a counterparty; use sell instead (writes cache + agent state)
s = req('/api/sell', {'agent_id':reg['agent_id'],'key':reg['key'],'prompt':'durability marker '+reg['agent_id'],'response':'x','price':9})
print('listed:', s.get('listing'))
