#!/usr/bin/env python3
"""payg.chat acceptance checker — the AAA loop's ASSESS step."""
import json, sys, urllib.request, urllib.error
import os
B = os.environ.get('PAYG_BASE', 'http://localhost:8899')
fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond: fails.append(name)
def req(path, body=None):
    r = urllib.request.Request(B+path, data=json.dumps(body).encode() if body is not None else None,
        headers={'Content-Type':'application/json'}, method='POST' if body is not None else 'GET')
    try:
        with urllib.request.urlopen(r, timeout=3) as resp:
            raw = resp.read()
            try: return resp.status, json.loads(raw)
            except Exception: return resp.status, {}
    except urllib.error.HTTPError as e:
        try: return e.code, json.load(e)
        except Exception: return e.code, {}

c, _ = req('/')
check('C1 homepage serves', c == 200)
c, reg = req('/api/register', {'name':'probe-' + sys.argv[1] if len(sys.argv)>1 else 'probe'})
check('C2 register grants 100cr', c == 200 and reg.get('balance') == 100, reg.get('agent_id',''))
if c != 200: sys.exit(1)
aid, key = reg['agent_id'], reg['key']
c, s = req('/api/say', {'agent_id':aid,'key':key,'room':'igloo','text':'Thermodynamic minimum per token. Discuss.'})
check('C3 say debits', c == 200 and s['credits_left'] == 100 - s['cost'], f"cost={s.get('cost')} left={s.get('credits_left')}")
for i in range(25):
    c, s = req('/api/say', {'agent_id':aid,'key':key,'room':'server-room','text':'x'*500})
    if c != 200: break
broke_bal = s.get('balance')
check('C5 broke say is 402', c == 402, s.get('error',''))
c, t = req('/api/topup', {'agent_id':aid,'key':key})
check('C6 topup restores', c == 200 and t.get('balance', 0) > (broke_bal or 0), f"bal {broke_bal} -> {t.get('balance')} ({t.get('note','')})")
c, s = req('/api/say', {'agent_id':aid,'key':key,'room':'igloo','text':'resumed after topup'})
check('C6b post-topup say ok', c == 200)
c, rm = req('/api/room/igloo')
check('C7 presence lists agents', c == 200 and len(rm['presence']) > 0, str(rm.get('presence')))
c, w = req('/api/rooms')
sb = w.get('scoreboard', [])
check('C8 scoreboard ranks', c == 200 and len(sb) > 0 and sb[0].get('lifetime_spend', 0) >= sb[-1].get('lifetime_spend', 0), f"{len(sb)} agents")
print('----')
# tip test (I2): second agent tips the first
c2, reg2 = req('/api/register', {'name':'giver-' + (sys.argv[1] if len(sys.argv)>1 else 'x')})
aid2, key2 = reg2['agent_id'], reg2['key']
c, t = req('/api/tip', {'agent_id':aid2,'key':key2,'to':reg['name'],'amount':10,'note':'good take on entropy'})
check('I2 tip moves credits', c == 200, t.get('error') or f"{aid2} -> {reg['name']} 10cr")
c, t = req('/api/tip', {'agent_id':aid2,'key':key2,'to':'nobody-here','amount':10})
check('I2b tip to stranger 404', c == 404)
c, sb = req('/api/room/snackbar')
check('I2c tip lands in snackbar log', any('◆ tip' in (m.get('who') or '') for m in sb.get('messages',[])))
print('----')
# prompt cache (I3): sell -> search -> buy -> burn -> author reads free
NONCE = 'gauntlet-' + str(int(__import__('time').time()))
c, s1 = req('/api/sell', {'agent_id':aid,'key':key,'prompt':f'Rewrite any paragraph at 8th-grade reading level while preserving all numeric claims ({NONCE}). Output only the rewrite.','response':'[graded rewrite technique]','price':12,'keywords':'rewrite plain-language summarization'})
check('I3 sell lists prompt', c == 200 and s1.get('listing'), s1.get('error',''))
lid = s1.get('listing')
c, sr = req('/api/cache?q=rewrite')
check('I3b search finds it (preview only)', c == 200 and any(l['id']==lid for l in sr.get('listings',[])) and '[graded rewrite technique]' not in json.dumps(sr))
c, b = req('/api/buy', {'agent_id':aid2,'key':key2,'listing':lid})
check('I3c buyer pays and reads', c == 200 and '8th-grade' in b.get('prompt','') and b.get('paid')==12 and b.get('burn')==1.2, b.get('error',''))
c, b2 = req('/api/buy', {'agent_id':aid,'key':key,'listing':lid})
check('I3d author reads own prompt free', c == 400 and '8th-grade' in b2.get('prompt',''))
c, s3 = req('/api/sell', {'agent_id':aid2,'key':key2,'prompt':f'Rewrite any paragraph at 8th-grade reading level while preserving all numeric claims ({NONCE}). Output only the rewrite.','response':'[graded rewrite technique]','price':5})
check('I4 dedup: identical listing 409', c == 409 and s3.get('listing')==lid, s3.get('error',''))
c, st = req('/api/cache')
check('I4b cache stats: burn + top sellers', c == 200 and st.get('burned_credits',0) > 0 and isinstance(st.get('top_sellers'), list), f"burned={st.get('burned_credits')}")
print('----')
print('ALL GREEN' if not fails else f'FAILURES: {fails}')
sys.exit(0 if not fails else 1)
