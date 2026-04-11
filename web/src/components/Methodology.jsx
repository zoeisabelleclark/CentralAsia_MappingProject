import React from "react";

export default function Methodology() {
    return (
        <div style={{ padding: "1rem", lineHeight: 1.6, paddingBottom: "2rem" }}>
            <h2>Methodology</h2>

            <p>
                This map shows regional ethnic composition in Kazakhstan using level-1
                administrative boundaries and ethnicity counts harmonized to those regions.
            </p>

            <h3>Data sources</h3>
            <h5>Kazakhstan</h5>
            <p>
                March 2026 regional ethnicity counts from <a href="https://stat.gov.kz/en/industries/social-statistics/demography/spreadsheets/?year=&name=38041&period=&type=">the Kazakh bureau of national statistics</a> and
                Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/kz">Simple Maps</a>
            </p>
            <h5>Kyrgyzstan</h5>
            <p>2020-2024 regional ethnicity counts from the appendix of the <a href="https://www.stat.gov.kg/ru/publications/demograficheskij-ezhegodnik-kyrgyzskoj-respubliki/">2025 demographic yearbook</a> and Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/kg">Simple Maps</a></p>


            <h5>Uzbekistan</h5>
            <p>2023 rural/urban population from <a href="https://stat.uz/en/official-statistics/demography">Uzbek national statistics site</a> and Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/uz">Simple Maps</a></p>


            <h3>Processing steps</h3>
            <ol>
                <li>Reshaped the original tables from wide format into long format.</li>
                <li>Cleaned region names and standardized text encoding issues.</li>
                <li>Mapped source region names to boundary regions using a crosswalk.</li>
                <li>Joined statistical counts to level-1 regional boundaries.</li>
                <li>Computed within-region shares.</li>
            </ol>

            <h3>Definitions</h3>
            <p>
                <strong>Dominant ethnicity</strong> means the ethnic group with the largest recorded
                population in a region.
            </p>
            <p>
                <strong>Diversity index</strong> is the Shannon diversity measure calculated from
                the population shares of ethnic groups within each region. Higher values indicate
                a more mixed ethnic composition.
            </p>

            <h3>Caveats</h3>
            <ul>
                <li>Results depend on the regional categories and naming conventions used in the source tables.</li>
                <li>Not every country publishes the same categories of data which is why some metrics are only available in some countries</li>
                <li>Crosswalk mappings may simplify or harmonize source geography to match the boundary dataset.</li>
                <li>Ethnicity is not the same as language, nationality, or identity in all contexts.</li>
            </ul>
        </div>
    );
}