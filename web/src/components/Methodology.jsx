import React from "react";

export default function Methodology() {
    return (
        <div style={{ padding: "1rem", lineHeight: 1.6 }}>
            <h2>Methodology</h2>

            <p>
                This map shows regional ethnic composition in Kazakhstan using level-1
                administrative boundaries and ethnicity counts harmonized to those regions.
            </p>

            <h3>Data sources</h3>
            <p>
                2026 Regional ethnicity counts from <a href="https://stat.gov.kz/en/industries/social-statistics/demography/">the Kazakh government statistic website</a> and
                Level-1 administrative boundaries in GeoJSON format from <a href="https://simplemaps.com/gis/country/kz">Simple Maps</a>
            </p>

            <h3>Processing steps</h3>
            <ol>
                <li>Reshaped the original ethnicity table from wide format into long format.</li>
                <li>Cleaned region names and standardized text encoding issues.</li>
                <li>Mapped source region names to boundary regions using a crosswalk.</li>
                <li>Joined ethnicity counts to level-1 regional boundaries.</li>
                <li>Computed within-region ethnicity shares.</li>
                <li>Calculated dominant ethnicity and Shannon diversity index for each region.</li>
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
                <li>Crosswalk mappings may simplify or harmonize source geography to match the boundary dataset.</li>
                <li>Ethnicity is not the same as language, nationality, or identity in all contexts.</li>
            </ul>
        </div>
    );
}