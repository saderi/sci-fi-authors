# Science fiction authors world map

An interactive choropleth map of science fiction authors born in 1800 or later, shaded by number of authors per country. Switch between **Born in** and **Lived in**, and filter by birth era. Each author links to their English Wikipedia article or official website.

Built with AI (Claude, by Anthropic). Data is from Wikidata and may contain errors.

## Data

- 3,557 authors, from Wikidata: people with occupation "science fiction writer", or writers with the genre "science fiction".
- Only authors with an English Wikipedia article or an official website are kept.
- **Born in** is the present-day country of the birthplace. **Lived in** is the recorded country of residence, falling back to citizenship. Both are one country per author.
- Not a complete census: English-language writers are over-represented, and Wikidata tags can be missing or wrong.

## Files

| File | Purpose |
|---|---|
| `index.html` | The built page (self-contained apart from three CDN scripts). This is what GitHub Pages serves. |
| `template.html` | Page source with `__DATA__` and `__NAMES__` placeholders. Edit this, not `index.html`. |
| `authors_wd.csv` | The data: name, birth year, born/lived ISO3 country codes, Wikipedia URL, website. |
| `country_names.json` | ISO 3166-1 alpha-3 code to country name. |
| `fetch_wikidata.py` | Pulls the data from Wikidata and writes `authors_wd.csv`. |
| `build.py` | Validates the CSV and writes `index.html` from the template. |
| `queries/` | The SPARQL queries behind the data. |

## Rebuild

Python 3, standard library only.

```
python3 fetch_wikidata.py   # about 11 minutes: Wikidata rate-limits to 1 query per minute
python3 build.py            # writes index.html
```

`fetch_wikidata.py` caches each birth-year range in `cache_*.json` (git-ignored), so a failed run resumes. Delete the cache files to refresh the data.

## Notes

- The map uses Plotly 2.35.2 (`plotly-geo-assets.js` bundles the country outlines). If it fails to load, the ranking and author lists still work.
- Counts are binned (1, 2-4, 5-9, 10-24, 25-49, 50-99, 100-249, 250+) because the United States dwarfs every other country.
- Known issues: two duplicate names (Jonathan Blum, Michael Shea); historical states without ISO codes fall back to citizenship.

## Licence

MIT for the code. Data derived from Wikidata (CC0).
