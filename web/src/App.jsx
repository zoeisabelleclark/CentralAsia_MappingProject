import React, { useEffect, useMemo, useState } from "react";
import MapView from "./components/MapView";
import Methodology from "./components/Methodology";
import SidebarFooter from "./components/SidebarFooter";

const panelStyle = {
    background: "rgba(255,255,255,0.88)",
    border: "1px solid #e5e7eb",
    borderRadius: "16px",
    boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
};

const sectionTitleStyle = {
    fontSize: "0.82rem",
    fontWeight: 700,
    letterSpacing: "0.04em",
    textTransform: "uppercase",
    color: "#6b7280",
    marginBottom: "0.6rem",
};

const controlStyle = {
    width: "100%",
    padding: "0.75rem 0.9rem",
    borderRadius: "12px",
    border: "1px solid #d1d5db",
    background: "#fff",
    color: "#111827",
    outline: "none",
};

const tabButton = (active) => ({
    flex: 1,
    padding: "0.7rem 0.9rem",
    borderRadius: "12px",
    border: active ? "1px solid #111827" : "1px solid #d1d5db",
    background: active ? "#111827" : "#fff",
    color: active ? "#fff" : "#111827",
    cursor: "pointer",
    fontWeight: 600,
});

const COUNTRY_CONFIG = {
    kazakhstan: {
        label: "Kazakhstan",
        statsFile: "ethnicity_stats.json",
        statsType: "ethnicity",
        layers: [
            { value: "ethnicity", label: "Ethnicity share" },
            { value: "diversity", label: "Diversity index" },
        ],
        defaultLayer: "ethnicity",
    },
    kyrgyzstan: {
        label: "Kyrgyzstan",
        statsFile: "ethnicity_stats.json",
        statsType: "ethnicity",
        layers: [
            { value: "ethnicity", label: "Ethnicity share" },
            { value: "diversity", label: "Diversity index" },
        ],
        defaultLayer: "ethnicity",
    },
    uzbekistan: {
        label: "Uzbekistan",
        statsFile: "urban_stats.json",
        statsType: "urban",
        layers: [
            { value: "urban", label: "Urban share" },
        ],
        defaultLayer: "urban",
    },
};

export default function App() {
    const [regions, setRegions] = useState(null);
    const [statsData, setStatsData] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState("kazakhstan");
    const [selectedEthnicity, setSelectedEthnicity] = useState("dominant");
    const [viewMode, setViewMode] = useState("ethnicity");
    const [selectedRegion, setSelectedRegion] = useState(null);
    const [activePanel, setActivePanel] = useState("map");

    const countryConfig = COUNTRY_CONFIG[selectedCountry];
    const countryLabel = countryConfig.label;
    const availableLayers = countryConfig.layers;
    const statsType = countryConfig.statsType;

    useEffect(() => {
        setRegions(null);
        setStatsData([]);
        setSelectedRegion(null);

        fetch(`/data/${selectedCountry}/regions.geojson`)
            .then((res) => res.json())
            .then((data) => setRegions(data));

        fetch(`/data/${selectedCountry}/${countryConfig.statsFile}`)
            .then((res) => res.json())
            .then((data) => setStatsData(data));
    }, [selectedCountry, countryConfig.statsFile]);

    useEffect(() => {
        setViewMode(countryConfig.defaultLayer);
        setSelectedEthnicity("dominant");
        setSelectedRegion(null);
    }, [selectedCountry, countryConfig.defaultLayer]);

    const ethnicityOptions = useMemo(() => {
        if (statsType !== "ethnicity") return [];
        const values = [...new Set(statsData.map((d) => d.ethnicity).filter(Boolean))];
        return values.sort();
    }, [statsData, statsType]);

    const selectedRegionBreakdown = useMemo(() => {
        if (!selectedRegion || statsType !== "ethnicity") return [];

        return statsData
            .filter((row) => row.region_key === selectedRegion.region_key)
            .sort((a, b) => Number(b.percent) - Number(a.percent))
            .slice(0, 8);
    }, [selectedRegion, statsData, statsType]);

    return (
        <div
            style={{
                display: "grid",
                gridTemplateColumns: "360px 1fr",
                height: "100vh",
                background: "#f7f7f5",
                overflow: "hidden",
            }}
        >
            <aside
                style={{
                    padding: "1.25rem 1.25rem 2rem 1.25rem",
                    borderRight: "1px solid #e5e7eb",
                    background: "#f3f4f1",
                    overflowY: "auto",
                    height: "100vh",
                    WebkitOverflowScrolling: "touch",
                }}
            >
                <div style={{ marginBottom: "1.25rem" }}>
                    <div style={{ fontSize: "0.82rem", color: "#6b7280", marginBottom: "0.3rem" }}>
                        Mapping project
                    </div>
                    <h1 style={{ margin: 0, fontSize: "1.6rem", lineHeight: 1.1 }}>
                        Central Asia Atlas
                    </h1>
                </div>

                <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
                    <button onClick={() => setActivePanel("map")} style={tabButton(activePanel === "map")}>
                        Map
                    </button>
                    <button
                        onClick={() => setActivePanel("methodology")}
                        style={tabButton(activePanel === "methodology")}
                    >
                        Methodology
                    </button>
                </div>

                {activePanel === "map" ? (
                    <div style={{ display: "grid", gap: "1rem" }}>
                        <div style={{ ...panelStyle, padding: "1rem" }}>
                            <div style={sectionTitleStyle}>View settings</div>

                            <div style={{ marginBottom: "1rem" }}>
                                <label style={{ display: "block", fontWeight: 600, marginBottom: "0.45rem" }}>
                                    Country
                                </label>
                                <select
                                    value={selectedCountry}
                                    onChange={(e) => setSelectedCountry(e.target.value)}
                                    style={controlStyle}
                                >
                                    {Object.entries(COUNTRY_CONFIG).map(([value, config]) => (
                                        <option key={value} value={value}>
                                            {config.label}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div style={{ marginBottom: "1rem" }}>
                                <label style={{ display: "block", fontWeight: 600, marginBottom: "0.45rem" }}>
                                    Layer
                                </label>
                                <select
                                    value={viewMode}
                                    onChange={(e) => setViewMode(e.target.value)}
                                    style={controlStyle}
                                >
                                    {availableLayers.map((layer) => (
                                        <option key={layer.value} value={layer.value}>
                                            {layer.label}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {statsType === "ethnicity" && viewMode === "ethnicity" && (
                                <div>
                                    <label style={{ display: "block", fontWeight: 600, marginBottom: "0.45rem" }}>
                                        Ethnicity
                                    </label>
                                    <select
                                        value={selectedEthnicity}
                                        onChange={(e) => setSelectedEthnicity(e.target.value)}
                                        style={controlStyle}
                                    >
                                        <option value="dominant">Dominant ethnicity</option>
                                        {ethnicityOptions.map((eth) => (
                                            <option key={eth} value={eth}>
                                                {eth}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            )}
                        </div>

                        <div style={{ ...panelStyle, padding: "1rem" }}>
                            <div style={sectionTitleStyle}>Selected region</div>

                            {selectedRegion ? (
                                <div>
                                    <div style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "0.75rem" }}>
                                        {selectedRegion.region_name}
                                    </div>

                                    {statsType === "ethnicity" ? (
                                        <>
                                            <div style={{ display: "grid", gap: "0.55rem", color: "#374151" }}>
                                                <div>
                                                    <strong>Dominant ethnicity:</strong>{" "}
                                                    {selectedRegion.dominant_ethnicity || "n/a"}
                                                </div>
                                                <div>
                                                    <strong>Dominant share:</strong>{" "}
                                                    {selectedRegion.dominant_percent != null
                                                        ? `${Number(selectedRegion.dominant_percent).toFixed(1)}%`
                                                        : "n/a"}
                                                </div>
                                                <div>
                                                    <strong>Diversity index:</strong>{" "}
                                                    {selectedRegion.diversity_index != null
                                                        ? Number(selectedRegion.diversity_index).toFixed(3)
                                                        : "n/a"}
                                                </div>
                                            </div>

                                            <div style={{ marginTop: "1rem" }}>
                                                <div style={sectionTitleStyle}>Top ethnicities</div>
                                                <div style={{ display: "grid", gap: "0.45rem" }}>
                                                    {selectedRegionBreakdown.map((row) => (
                                                        <div
                                                            key={`${row.region_key}-${row.ethnicity}`}
                                                            style={{
                                                                display: "flex",
                                                                justifyContent: "space-between",
                                                                alignItems: "center",
                                                                padding: "0.55rem 0.7rem",
                                                                borderRadius: "12px",
                                                                background: "#f9fafb",
                                                                border: "1px solid #eceff3",
                                                            }}
                                                        >
                                                            <span>{row.ethnicity}</span>
                                                            <strong>{Number(row.percent).toFixed(1)}%</strong>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        </>
                                    ) : (
                                        <div style={{ display: "grid", gap: "0.55rem", color: "#374151" }}>
                                            <div>
                                                <strong>Urban share:</strong>{" "}
                                                {selectedRegion.urban_percent != null
                                                    ? `${Number(selectedRegion.urban_percent).toFixed(1)}%`
                                                    : "n/a"}
                                            </div>
                                            <div>
                                                <strong>Rural share:</strong>{" "}
                                                {selectedRegion.rural_percent != null
                                                    ? `${Number(selectedRegion.rural_percent).toFixed(1)}%`
                                                    : "n/a"}
                                            </div>
                                            <div>
                                                <strong>Urban population:</strong>{" "}
                                                {selectedRegion.urban_population != null
                                                    ? Number(selectedRegion.urban_population).toLocaleString()
                                                    : "n/a"}
                                            </div>
                                            <div>
                                                <strong>Rural population:</strong>{" "}
                                                {selectedRegion.rural_population != null
                                                    ? Number(selectedRegion.rural_population).toLocaleString()
                                                    : "n/a"}
                                            </div>
                                            <div>
                                                <strong>Total population:</strong>{" "}
                                                {selectedRegion.total_population != null
                                                    ? Number(selectedRegion.total_population).toLocaleString()
                                                    : "n/a"}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div style={{ color: "#6b7280", lineHeight: 1.6 }}>
                                    Click a region to inspect its data.
                                </div>
                            )}
                        </div>
                    </div>
                ) : (
                    <div style={{ ...panelStyle, padding: "1rem", color: "#6b7280", lineHeight: 1.6 }}>
                        Use the Methodology tab to view project notes in the main panel.
                    </div>
                )}
                {/* Footer */}
                <div
                    style={{
                        padding: "0.9rem 1.25rem",
                        borderTop: "1px solid #e5e7eb",
                        background: "#f3f4f1",
                    }}
                >
                    <SidebarFooter />
                </div>
            </aside>

            <main
                style={{
                    minWidth: 0,
                    height: "100vh",
                    overflow: "hidden",
                }}
            >
                {activePanel === "map" ? (
                    regions && (
                        <MapView
                            key={selectedCountry}
                            regions={regions}
                            statsData={statsData}
                            statsType={statsType}
                            selectedEthnicity={selectedEthnicity}
                            viewMode={viewMode}
                            onSelectRegion={setSelectedRegion}
                            selectedRegion={selectedRegion}
                            countryLabel={countryLabel}
                        />
                    )
                ) : (
                    <div
                        style={{
                            height: "100%",
                            overflowY: "auto",
                            padding: "2rem",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "flex-start",
                            WebkitOverflowScrolling: "touch",
                        }}
                    >
                        <div
                            style={{
                                background: "rgba(255,255,255,0.92)",
                                border: "1px solid #e5e7eb",
                                borderRadius: "16px",
                                boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
                                padding: "1.5rem",
                                maxWidth: "900px",
                                width: "100%",
                            }}
                        >
                            <Methodology />
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}