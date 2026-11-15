"""Validate the author CSV and write index.html from template.html.
Usage: python3 build.py [authors_wd.csv]   (Python 3, standard library only)"""
import json, collections, csv, sys
src = sys.argv[1] if len(sys.argv) > 1 else 'authors_wd.csv'
rows = list(csv.reader(open(src, encoding='utf-8')))[1:]
assert all(len(r) == 6 for r in rows), [r for r in rows if len(r) != 6][:5]
dup = [n for n, c in collections.Counter(r[0] for r in rows).items() if c > 1]; print('duplicate names', len(dup), dup[:10])
assert all(1800 <= int(r[1]) <= 2005 for r in rows)
iso = json.load(open('country_names.json', encoding='utf-8'))
over = {'USA':'United States','GBR':'United Kingdom','RUS':'Russia','KOR':'South Korea','TWN':'Taiwan','IRN':'Iran','SYR':'Syria','BOL':'Bolivia','CZE':'Czechia','VNM':'Vietnam','HKG':'Hong Kong'}
codes = sorted({c for r in rows for c in r[2:4]})
bad = [c for c in codes if c not in iso]; assert not bad, ('add these codes to country_names.json', bad)
nm = {c: over.get(c, iso[c]) for c in codes}
b = collections.Counter(r[2] for r in rows); l = collections.Counter(r[3] for r in rows)
print(len(rows), 'authors', len(codes), 'codes'); print('born', b.most_common(12)); print('lived', l.most_common(12))
print('moved', sum(r[2] != r[3] for r in rows), '| with wikipedia', sum(bool(r[4]) for r in rows))
WP = 'https://en.wikipedia.org/wiki/'
def line(r):
    link = r[4][len(WP):] if r[4].startswith(WP) else (r[4] or r[5])
    link = link.replace(';', '%3B').replace('`', '%60').replace('\n', '')
    return ';'.join(r[:4] + [link])
h = open('template.html', encoding='utf-8').read().replace('__DATA__', '\n'.join(line(r) for r in rows)).replace('__NAMES__', json.dumps(nm, ensure_ascii=False))
open('index.html', 'w', encoding='utf-8').write(h)
