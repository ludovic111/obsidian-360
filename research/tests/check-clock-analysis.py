#!/usr/bin/env python3
"""Check clock-bracket analysis against a synthetic independent time scale."""
import copy,importlib.util,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('clock',root/'tools/measure-clock-drift.py');clock=importlib.util.module_from_spec(spec);spec.loader.exec_module(clock)
base={'state':'succeeded','transport_code':0,'identity':{'clocksource':'timebase','timebase_frequencies':{'cpu0':50000000}},'samples':[]}
# Actual local instants are bracketed, not assumed equal to packet midpoints.
for local,delay in [(10_000_000_000,1_000_000),(70_000_000_000,3_000_000)]:
 remote=local*9975//10000
 base['samples'].append({'host_send_monotonic_ns':local-delay,'host_receive_monotonic_ns':local+delay,'host_send_wall_ns':local-delay,'host_receive_wall_ns':local+delay,'console':{'raw_ns':remote,'monotonic_ns':remote,'wall_ns':remote}})
r=clock.analyze(base);low,high=r['effective_timebase_hz_bounds'];assert low<=49875000<=high and high<50000000
cases=1
for change in ('incomplete','transport','missing_sample','negative_rtt','backwards_host','backwards_remote'):
 data=copy.deepcopy(base)
 if change=='incomplete':data['state']='running'
 if change=='transport':data['transport_code']=255
 if change=='missing_sample':data['samples']=data['samples'][:1]
 if change=='negative_rtt':data['samples'][0]['host_receive_monotonic_ns']=0
 if change=='backwards_host':data['samples'][1]['host_send_monotonic_ns']=0
 if change=='backwards_remote':data['samples'][1]['console']['raw_ns']=0
 try:clock.analyze(data)
 except ValueError:cases+=1
 else:raise AssertionError(change)
# The active kernel conversion may differ from the immutable firmware DT.
corrected=copy.deepcopy(base)
corrected['identity']['cpuinfo_timebase_hz']=49875000
for row in corrected['samples']:
 midpoint=(row['host_send_monotonic_ns']+row['host_receive_monotonic_ns'])//2
 for field in ('raw_ns','monotonic_ns','wall_ns'):row['console'][field]=midpoint
r=clock.analyze(corrected)
assert r['advertised_timebase_hz']==50000000 and r['conversion_timebase_hz']==49875000
assert r['effective_timebase_hz_bounds'][0]<=49875000<=r['effective_timebase_hz_bounds'][1]<50000000
cases+=1
for invalid in (0,-1,True,'49875000'):
 data=copy.deepcopy(corrected);data['identity']['cpuinfo_timebase_hz']=invalid
 try:clock.analyze(data)
 except ValueError:cases+=1
 else:raise AssertionError('Invalid active frequency accepted')
data=copy.deepcopy(corrected);data['identity']['cpuinfo_timebase_hz']=None
assert 'effective_timebase_hz_bounds' not in clock.analyze(data);cases+=1
print(json.dumps({'passed':True,'cases':cases,'scope':'Synthetic known rate plus malformed/incomplete observations; no console access'}))
