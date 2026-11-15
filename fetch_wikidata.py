"""Fetch SF authors born 1800+ from Wikidata, collapse to one row per author, write authors_wd.csv.
Python 3, standard library only. Usage: python3 fetch_wikidata.py"""
import csv, os, json, time, urllib.parse, urllib.request, collections

EP = 'https://query.wikidata.org/sparql'
UA = 'sf-authors-map/0.2 (hobby data project)'
RANGES = [(1800,1900),(1900,1920),(1920,1930),(1930,1940),(1940,1950),(1950,1960),(1960,1970),(1970,1980),(1980,1990),(1990,2006)]

Q = """
SELECT ?a ?label ?birth ?bornIso ?livedIso ?citIso ?wp ?site WHERE {
  { SELECT DISTINCT ?a ?birth WHERE {
      { ?a wdt:P106 wd:Q18844224 . }
      UNION
      { ?a wdt:P106 wd:Q36180 ; wdt:P136 wd:Q24925 . }
      ?a wdt:P31 wd:Q5 ; wdt:P569 ?birth .
      FILTER(YEAR(?birth) >= %d && YEAR(?birth) < %d)
  } }
  OPTIONAL { ?a wdt:P19/wdt:P17/wdt:P298 ?bornIso . }
  OPTIONAL { ?a wdt:P551/wdt:P17/wdt:P298 ?livedIso . }
  OPTIONAL { ?a wdt:P27/wdt:P298 ?citIso . }
  OPTIONAL { ?wp schema:about ?a ; schema:isPartOf <https://en.wikipedia.org/> . }
  OPTIONAL { ?a wdt:P856 ?site . }
  OPTIONAL { ?a rdfs:label ?label . FILTER(LANG(?label)='en') }
}
"""

def run(q):
    url = EP + '?format=json&query=' + urllib.parse.quote(q)
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/sparql-results+json'})
            return json.load(urllib.request.urlopen(req, timeout=180))['results']['bindings']
        except Exception as e:
            print('retry', i, e); time.sleep(65)
    raise SystemExit('query failed')

auth = {}
for lo, hi in RANGES:
    cf = 'cache_%d_%d.json' % (lo, hi)
    if os.path.exists(cf):
        rows = json.load(open(cf)); print(lo, hi, len(rows), 'rows (cached)', flush=True)
    else:
        rows = run(Q % (lo, hi)); json.dump(rows, open(cf, 'w')); print(lo, hi, len(rows), 'rows', flush=True)
        time.sleep(65)
    for r in rows:
        g = lambda k: r[k]['value'] if k in r else None
        d = auth.setdefault(g('a'), dict(label=None, y=None, born=collections.Counter(), lived=collections.Counter(),
                                         cit=collections.Counter(), wp=set(), site=set()))
        d['label'] = d['label'] or g('label')
        d['y'] = d['y'] or int(g('birth')[:4].lstrip('+'))
        for k, f in (('born','bornIso'),('lived','livedIso'),('cit','citIso')):
            if g(f): d[k][g(f)] += 1
        if g('wp'): d['wp'].add(g('wp'))
        if g('site'): d['site'].add(g('site'))

iso = json.load(open('country_names.json', encoding='utf-8'))
def pick(c, prefer=()):
    c = collections.Counter({k: v for k, v in c.items() if k in iso})
    for p in prefer:
        if p in c: return p
    return c.most_common(1)[0][0] if c else None

out, skipped = [], collections.Counter()
for q, d in auth.items():
    name = d['label']
    if not name or name.startswith('Q') and name[1:].isdigit(): skipped['nolabel'] += 1; continue
    wp = sorted(d['wp'])[0] if d['wp'] else ''
    site = sorted(d['site'])[0] if d['site'] else ''
    if not wp and not site: skipped['nolink'] += 1; continue
    cit = pick(d['cit'])
    born = pick(d['born'], [cit] if cit else ()) or cit
    lived = pick(d['lived'], [cit] if cit else ()) or cit or born
    if not born: skipped['nocountry'] += 1; continue
    born = born or lived
    if not (1800 <= d['y'] <= 2005): skipped['year'] += 1; continue
    out.append([name.replace(';', ',').replace('`', ''), d['y'], born, lived, wp, site])

out.sort(key=lambda r: (r[0].lower(), r[1]))
with open('authors_wd.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['name','birth_year','born_iso3','lived_iso3','wikipedia_url','website']); w.writerows(out)
print(len(auth), 'authors fetched;', len(out), 'written; skipped', dict(skipped))
