# Methodology

## Project scope
This project maps regional ethnic composition in Kazakhstan at the level-1 administrative unit.

## Data inputs
- 2026 Regional ethnicity counts from 'https://stat.gov.kz/en/industries/social-statistics/demography/' 
- Level-1 administrative boundaries in GeoJSON format from 'https://simplemaps.com/gis/country/kz'

## Data reshaping
The original ethnicity data was published in a wide table format with regions as columns and ethnicities as rows. This table was transformed into long format so that each row represents one ethnicity in one region.

## Harmonization
Region names in the ethnicity table and boundary dataset did not always match exactly. A manual crosswalk was created to align source region names to standardized boundary region keys.

## Derived measures
### Dominant ethnicity
The ethnic group with the highest recorded population in each region.

### Ethnicity share
The share of the regional total population accounted for by each ethnic group.

### Diversity index
Shannon diversity:
H = -sum(p_i * ln(p_i))
where p_i is the share of each ethnic group in the region.

## Caveats
- Administrative boundaries and statistical reporting categories may change over time.
- Crosswalk decisions can affect comparability.
- Ethnicity should not be interpreted as a direct substitute for language use.


## Update process
- Update join_boundaries.py
- rerun: python scripts/join_boundaries.py
- copy outputs:  cp data/processed/regions.geojson web/public/data/regions.geojson
cp data/processed/ethnicity_stats.json web/public/data/ethnicity_stats.json
- replace App.jsx
- replace MapView.jsx
- update Methodology.jsx
- run: cd web
npm run dev
- test: dominant mode, specific ethnicity mode, diversity mode, click region, methodology toggle