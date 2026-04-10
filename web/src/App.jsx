import React, { useEffect, useMemo, useState } from "react";
import MapView from "./components/MapView";
import Methodology from "./components/Methodology";

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

export default function App() {
    const [regions, setRegions] = useState(null);
    const [ethnicityStats, setEthnicityStats] = useState([]);
    const [selectedEthnicity, setSelectedEthnicity] = useState("dominant");
    const [viewMode, setViewMode] = useState("ethnicity");
    const [selectedRegion, setSelectedRegion] = useState(null);
    const [activePanel, setActivePanel] = useState("map");

    useEffect(() => {
        fetch("/data/kyrgyzstan/regions.geojson")
            .then((res) => res.json())
            .then((data) => setRegions(data));

        fetch("/data/kyrgyzstan/ethnicity_stats.json")
            .then((res) => res.json())
            .then((data) => setEthnicityStats(data));
    }, []);

    const ethnicityOptions = useMemo(() => {
        const values = [...new Set(ethnicityStats.map((d) => d.ethnicity).filter(Boolean))];
        return values.sort();
    }, [ethnicityStats]);

    const selectedRegionBreakdown = useMemo(() => {
        if (!selectedRegion) return [];

        return ethnicityStats
            .filter((row) => row.region_key === selectedRegion.region_key)
            .sort((a, b) => Number(b.percent) - Number(a.percent))
            .slice(0, 8);
    }, [selectedRegion, ethnicityStats]);

    return (
        <div
            style={{
                display: "grid",
                gridTemplateColumns: "360px 1fr",
                minHeight: "100vh",
                background: "#f7f7f5",
            }}
        >
            <aside
                style={{
                    padding: "1.25rem",
                    borderRight: "1px solid #e5e7eb",
                    background: "#f3f4f1",
                }}
            >
                <div style={{ marginBottom: "1.25rem" }}>
                    <div style={{ fontSize: "0.82rem", color: "#6b7280", marginBottom: "0.3rem" }}>
                        Central Asia Mapping Project
                    </div>
                    <h1 style={{ margin: 0, fontSize: "1.6rem", lineHeight: 1.1 }}>
                        Kazakhstan Ethnicity Explorer
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
                                    Layer
                                </label>
                                <select
                                    value={viewMode}
                                    onChange={(e) => setViewMode(e.target.value)}
                                    style={controlStyle}
                                >
                                    <option value="ethnicity">Ethnicity share</option>
                                    <option value="diversity">Diversity index</option>
                                </select>
                            </div>

                            {viewMode === "ethnicity" && (
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
                                </div>
                            ) : (
                                <div style={{ color: "#6b7280", lineHeight: 1.6 }}>
                                    Click a region to inspect its ethnic composition and diversity.
                                </div>
                            )}
                        </div>
                    </div>
                ) : (
                    <div style={{ ...panelStyle, padding: "0.5rem" }}>
                        Overarching strategy and rationale of the research project and methods/data used.
                    </div>
                )}
            </aside>

            <main style={{ minWidth: 0 }}>
                {activePanel === "map" ? (
                    regions && (
                        <MapView
                            regions={regions}
                            ethnicityStats={ethnicityStats}
                            selectedEthnicity={selectedEthnicity}
                            viewMode={viewMode}
                            onSelectRegion={setSelectedRegion}
                            selectedRegion={selectedRegion}
                        />
                    )
                ) : (
                    <div style={{ padding: "2rem" }}>
                        <div style={{ ...panelStyle, padding: "1.5rem", maxWidth: "900px" }}>
                            <Methodology />
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}