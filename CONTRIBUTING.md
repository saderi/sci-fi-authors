# Contributing

Thanks for helping improve the map. Corrections and ideas are welcome.

## Fixing an author's data

The data comes from Wikidata, so most fixes belong there, not here:

- **Wrong or missing birth country, residence or citizenship:** edit the person's item on [wikidata.org](https://www.wikidata.org/) (properties P19 place of birth, P551 residence, P27 citizenship). The fix reaches the map the next time the data is rebuilt.
- **Author missing from the map:** check that their Wikidata item has occupation "science fiction writer" (Q18844224), or occupation "writer" with genre "science fiction" (P136 = Q24925), plus an English Wikipedia article or an official website (P856).
- **Something wrong that Wikidata can't fix** (a bad link, a display bug, a wrong country code): open an issue.

## Reporting a problem

[Open an issue](https://github.com/saderi/sci-fi-authors/issues) with the author or country involved, what you expected, and what the page shows. For a display bug, include your browser and a screenshot.

## Changing the code

1. Fork the repo and create a branch.
2. Edit `template.html` (page), `build.py` (validation and build) or `fetch_wikidata.py` (data). Do not edit `index.html` by hand; it is generated.
3. Run `python3 build.py` and open `index.html` in a browser. Check the map draws, both "Born in" and "Lived in" views, and the era filters.
4. Open a pull request describing what changed and why.

Python 3 with the standard library only. Please don't add dependencies for small changes.

## Refreshing the data

`python3 fetch_wikidata.py` then `python3 build.py`. Wikidata rate-limits to about one query per minute, so a full fetch takes around 11 minutes. Delete the `cache_*.json` files first to force a fresh pull. Commit `authors_wd.csv` and `index.html` together.

## Notes

- This project was built with AI assistance, so double-check changes that touch data rules (country codes, the "lived in" fallback to citizenship).
- By contributing you agree your changes are released under the MIT licence.
