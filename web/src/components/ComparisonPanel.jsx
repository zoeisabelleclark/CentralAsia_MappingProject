import React from "react";

const cardStyle = {
    padding: "0.85rem",
    borderRadius: "12px",
    border: "1px solid #e5e7eb",
    background: "#f9fafb",
};

function MetricRow({ label, left, right }) {
    return (
        <div
            style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr 1fr",
                gap: "0.5rem",
                alignItems: "center",
                padding: "0.45rem 0",
                borderBottom: "1px solid #eef2f7",
            }}
        >
            <div style={{ color: "#6b7280", fontSize: "0.9rem" }}>{label}</div>
            <div style={{ fontWeight: 600 }}>{left}</div>
            <div style={{ fontWeight: 600 }}>{right}</div>
        </div>
    );
}

function formatNumber(value) {
    if (value == null || Number.isNaN(Number(value))) return "n/a";
    return Number(value).toLocaleString();
}

function formatPercent(value) {
    if (value == null || Number.isNaN(Number(value))) return "n/a";
    return `${Number(value).toFixed(1)}%`;
}

function formatDensity(value) {
    if (value == null || Number.isNaN(Number(value))) return "n/a";
    return `${Number(value).toFixed(1)} /km²`;
}

export default function ComparisonPanel({
    comparedRegions,
    viewMode,
    selectedEthnicity,
}) {
    const [left, right] = comparedRegions;

    if (comparedRegions.length === 0) {
        return <div style={{ color: "#6b7280" }}>No regions selected.</div>;
    }

    if (comparedRegions.length === 1) {
        return (
            <div style={{ ...cardStyle, color: "#374151" }}>
                <div style={{ fontWeight: 700, marginBottom: "0.35rem" }}>{left.region_name}</div>
                <div style={{ color: "#6b7280" }}>{left.country || "Unknown country"}</div>
                <div style={{ marginTop: "0.5rem", color: "#6b7280" }}>
                    Select one more region to compare.
                </div>
            </div>
        );
    }

    return (
        <div style={{ display: "grid", gap: "0.75rem" }}>
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "0.75rem",
                }}
            >
                <div style={cardStyle}>
                    <div style={{ fontWeight: 700 }}>{left.region_name}</div>
                    <div style={{ color: "#6b7280" }}>{left.country || "Unknown country"}</div>
                </div>

                <div style={cardStyle}>
                    <div style={{ fontWeight: 700 }}>{right.region_name}</div>
                    <div style={{ color: "#6b7280" }}>{right.country || "Unknown country"}</div>
                </div>
            </div>

            <div style={{ ...cardStyle, paddingTop: "0.25rem" }}>
                {viewMode === "urban" && (
                    <>
                        <MetricRow
                            label="Urban share"
                            left={formatPercent(left.urban_percent)}
                            right={formatPercent(right.urban_percent)}
                        />
                        <MetricRow
                            label="Rural share"
                            left={formatPercent(left.rural_percent)}
                            right={formatPercent(right.rural_percent)}
                        />
                        <MetricRow
                            label="Population"
                            left={formatNumber(left.total_population)}
                            right={formatNumber(right.total_population)}
                        />
                        <MetricRow
                            label="Density"
                            left={formatDensity(left.population_density)}
                            right={formatDensity(right.population_density)}
                        />
                    </>
                )}

                {viewMode === "density" && (
                    <>
                        <MetricRow
                            label="Density"
                            left={formatDensity(left.population_density)}
                            right={formatDensity(right.population_density)}
                        />
                        <MetricRow
                            label="Population"
                            left={formatNumber(left.total_population)}
                            right={formatNumber(right.total_population)}
                        />
                        <MetricRow
                            label="Area"
                            left={left.area_sq_km != null ? `${Number(left.area_sq_km).toFixed(0)} km²` : "n/a"}
                            right={right.area_sq_km != null ? `${Number(right.area_sq_km).toFixed(0)} km²` : "n/a"}
                        />
                    </>
                )}

                {(viewMode === "ethnicity" || viewMode === "diversity") && (
                    <>
                        <MetricRow
                            label="Dominant ethnicity"
                            left={left.dominant_ethnicity || "n/a"}
                            right={right.dominant_ethnicity || "n/a"}
                        />
                        <MetricRow
                            label="Dominant share"
                            left={formatPercent(left.dominant_percent)}
                            right={formatPercent(right.dominant_percent)}
                        />
                        <MetricRow
                            label="Diversity"
                            left={left.diversity_index != null ? Number(left.diversity_index).toFixed(3) : "n/a"}
                            right={right.diversity_index != null ? Number(right.diversity_index).toFixed(3) : "n/a"}
                        />
                        {viewMode === "ethnicity" && selectedEthnicity !== "dominant" && (
                            <MetricRow
                                label={selectedEthnicity}
                                left={"See map shading"}
                                right={"See map shading"}
                            />
                        )}
                    </>
                )}
            </div>
        </div>
    );
}