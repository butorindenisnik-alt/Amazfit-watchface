# EcoTech Balance 2 v1.0.5 — apply reviewed pixel-art changes to v1.0.4.
# This delta updates only the visual layer; Zepp sensor/shortcut implementation is retained.
from pathlib import Path
import runpy, json, zlib, base64, hashlib
s = runpy.run_path('scripts/build_ecotech_v104.py')['s']
print('BASE source digest', hashlib.sha256(s.encode('utf-8')).hexdigest(), 'lines',len(s.splitlines()))
ops=json.loads(zlib.decompress(base64.b64decode(Path('scripts/ecotech_v105.delta.b64').read_text(encoding='ascii'))))
lines=s.splitlines(keepends=True)
for start,end,new_lines in reversed(ops):
    lines[start:end]=new_lines
s=''.join(lines)
print('FINAL source digest', hashlib.sha256(s.encode('utf-8')).hexdigest())
assert all(k in s for k in ['fade=Image.new', 'def cubic(', 'Clear mini-excavator', "version={'code':6,'name':'1.0.5'}"]), 'Visual patch did not land'
exec(compile(s, 'ecotech_v105_source.py', 'exec'))
