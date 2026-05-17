import React from "react";

export default function Methodology() {
    return (
        <div style={{ padding: "1rem", lineHeight: 1.6, paddingBottom: "2rem" }}>
            <h2>Methodology</h2>

            <p>
                This map shows regional data across Central Asia using level-1
                administrative boundaries.
            </p>
            <hr></hr>
            <h3>Current Coverage</h3>
            <p>Urban/rural population and density are available for all five Central Asian countries. Ethnicity and diversity index layers are currently only available for Kazakhstan and Kyrgyzstan due to data avilability.</p>
            <hr></hr>
            <h3>Data sources</h3>
            <p>
                <b>Kazakhstan</b>: March 2026 regional ethnicity counts and 2025 rural/urban populations from <a href="https://stat.gov.kz/en/industries/social-statistics/demography/spreadsheets/?year=&name=38041&period=&type=">the Kazakh bureau of national statistics</a>  and
                Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/kz">Simple Maps</a>
            </p>


            <p>
                <b>Kyrgyzstan</b>: 2020-2024 regional ethnicity counts and rural/urban population from the appendix of the <a href="https://www.stat.gov.kg/ru/publications/demograficheskij-ezhegodnik-kyrgyzskoj-respubliki/">2025 demographic yearbook</a> and Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/kg">Simple Maps</a>
            </p>



            <p>
                <b>Uzbekistan</b>: 2023 rural/urban population from <a href="https://stat.uz/en/official-statistics/demography">Uzbek national statistics site</a> and Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/uz">Simple Maps</a>
            </p>

            <p>
                <b>Tajikistan</b>: 2020 rural/urban population from the <a href="https://www.stat.tj/en/population-and-housing-census/">census</a> and Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/tj">Simple Maps</a>
            </p>

            <p>
                <b>Turkmenistan</b>: 2022 rural/urban population from the <a href="https://www.stat.gov.tm/en/population-census">census</a> and Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/tj">Simple Maps</a>
            </p>
            <hr></hr>
            <h3>Definitions</h3>
            <p>
                <strong>Dominant ethnicity:</strong> the ethnic group with the largest recorded
                population in a region.
            </p>
            <p>
                <strong>Diversity index:</strong> the Shannon diversity measure calculated from
                the population shares of ethnic groups within each region. Higher values indicate
                a more mixed ethnic composition.
            </p>
            <hr></hr>
            <h3>Caveats</h3>
            <ul>
                <li>Results depend on the regional categories and naming conventions used in the source tables.</li>
                <li>Not every country publishes the same categories of data which is why some metrics are only available in some countries</li>
                <li>Crosswalk mappings may simplify or harmonize source geography to match the boundary dataset.</li>
                <li>Ethnicity is not the same as language, nationality, or identity in all contexts.</li>
            </ul>
            <hr></hr>
            <h3>Processing steps</h3>
            <ol>
                <li>Reshaped the original tables from wide format into long format.</li>
                <li>Cleaned region names and standardized text encoding issues.</li>
                <li>Mapped source region names to boundary regions using a crosswalk.</li>
                <li>Joined statistical counts to level-1 regional boundaries.</li>
                <li>Computed within-region shares.</li>
            </ol>
        </div>
    );
}