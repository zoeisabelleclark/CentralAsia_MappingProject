import React, { useEffect, useMemo, useRef } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function getPercentColor(value) {
    if (value > 75) return "#0f172a";
    if (value > 50) return "#334155";
    if (value > 25) return "#64748b";
    if (value > 10) return "#94a3b8";
    return "#cbd5e1";
}

function getUrbanColor(value) {
    if (value > 80) return "#0f172a";
    if (value > 60) return "#334155";
    if (value > 40) return "#64748b";
    if (value > 20) return "#94a3b8";
    return "#cbd5e1";
}

function getDiversityColor(value) {
    if (value > 1.2) return "#0f172a";
    if (value > 1.0) return "#334155";
    if (value > 0.8) return "#64748b";
    if (value > 0.5) return "#94a3b8";
    return "#cbd5e1";
}

function LegendRow({ color, label }) {
    return (
        <div
            style={{
                display: "grid",
                gridTemplateColumns: "16px 1fr",
                gap: "0.65rem",
                alignItems: "center",
            }}
        >
            <div
                style={{
                    width: "16px",
                    height: "16px",
                    borderRadius: "4px",
                    background: color,
                    border: "1px solid rgba(17, 24, 39, 0.08)",
                }}
            />
            <div style={{ fontSize: "0.92rem", color: "#374151" }}>{label}</div>
        </div>
    );
}

function Legend({ viewMode, selectedEthnicity }) {
    let title = "";
    let rows = [];

    if (viewMode === "diversity") {
        title = "Shannon diversity index";
        rows = [
            { color: "#0f172a", label: "1.2+" },
            { color: "#334155", label: "1.0–1.2" },
            { color: "#64748b", label: "0.8–1.0" },
            { color: "#94a3b8", label: "0.5–0.8" },
            { color: "#cbd5e1", label: "< 0.5" },
        ];
    } else if (viewMode === "urban") {
        title = "Urban population share";
        rows = [
            { color: "#0f172a", label: "80%+" },
            { color: "#334155", label: "60–80%" },
            { color: "#64748b", label: "40–60%" },
            { color: "#94a3b8", label: "20–40%" },
            { color: "#cbd5e1", label: "< 20%" },
        ];
    } else {
        title =
            selectedEthnicity === "dominant"
                ? "Dominant ethnicity share"
                : `${selectedEthnicity} share`;

        rows = [
            { color: "#0f172a", label: "75%+" },
            { color: "#334155", label: "50–75%" },
            { color: "#64748b", label: "25–50%" },
            { color: "#94a3b8", label: "10–25%" },
            { color: "#cbd5e1", label: "< 10%" },
        ];
    }

    return (
        <div
            style={{
                position: "absolute",
                bottom: "24px",
                right: "24px",
                zIndex: 1000,
                background: "rgba(255,255,255,0.92)",
                backdropFilter: "blur(10px)",
                border: "1px solid #e5e7eb",
                borderRadius: "16px",
                padding: "0.95rem 1rem",
                boxShadow: "0 10px 24px rgba(15, 23, 42, 0.12)",
                minWidth: "210px",
            }}
        >
            <div
                style={{
                    fontSize: "0.78rem",
                    fontWeight: 700,
                    textTransform: "uppercase",
                    letterSpacing: "0.04em",
                    color: "#6b7280",
                    marginBottom: "0.5rem",
                }}
            >
                Legend
            </div>

            <div style={{ fontWeight: 700, marginBottom: "0.75rem", lineHeight: 1.3 }}>
                {title}
            </div>

            <div style={{ display: "grid", gap: "0.45rem" }}>
                {rows.map((row) => (
                    <LegendRow key={row.label} color={row.color} label={row.label} />
                ))}
            </div>
        </div>
    );
}

function FitToData({ regions }) {
    const map = useMap();

    useEffect(() => {
        if (!regions || !regions.features || regions.features.length === 0) return;

        const layer = L.geoJSON(regions);
        const bounds = layer.getBounds();

        if (bounds.isValid()) {
            map.fitBounds(bounds, { padding: [20, 20] });
        }
    }, [regions, map]);

    return null;
}

export default function MapView({
    regions,
    ethnicityStats,
    urbanStats,
    selectedEthnicity,
    viewMode,
    onSelectRegion,
    selectedRegion,
}) {
    const geoJsonRef = useRef(null);

    const ethnicityLookup = useMemo(() => {
        const lookup = {};
        for (const row of ethnicityStats) {
            const regionKey = row.region_key;
            const ethnicity = row.ethnicity;
            const percent = Number(row.percent);

            if (!lookup[regionKey]) lookup[regionKey] = {};
            lookup[regionKey][ethnicity] = percent;
        }
        return lookup;
    }, [ethnicityStats]);

    function getFeatureValue(feature) {
        const props = feature.properties || {};
        const regionKey = props.region_key;

        if (viewMode === "diversity") {
            return Number(props.diversity_index || 0);
        }

        if (viewMode === "urban") {
            return Number(props.urban_percent || 0);
        }

        if (selectedEthnicity === "dominant") {
            return Number(props.dominant_percent || 0);
        }

        return Number(ethnicityLookup?.[regionKey]?.[selectedEthnicity] || 0);
    }

    function getBaseStyle(feature) {
        const props = feature.properties || {};
        const isSelected = selectedRegion?.region_key === props.region_key;
        const value = getFeatureValue(feature);

        let fillColor = "#cbd5e1";

        if (viewMode === "diversity") {
            fillColor = getDiversityColor(value);
        } else if (viewMode === "urban") {
            fillColor = getUrbanColor(value);
        } else {
            fillColor = getPercentColor(value);
        }

        return {
            fillColor,
            weight: isSelected ? 3 : 1.2,
            opacity: 1,
            color: isSelected ? "#111827" : "#ffffff",
            fillOpacity: 0.84,
        };
    }

    function getHoverStyle(feature) {
        const props = feature.properties || {};
        const isSelected = selectedRegion?.region_key === props.region_key;
        const base = getBaseStyle(feature);

        return {
            ...base,
            weight: isSelected ? 3 : 2.2,
            color: "#111827",
            fillColor: base.fillColor,
            fillOpacity: base.fillOpacity,
        };
    }

    function style(feature) {
        return getBaseStyle(feature);
    }

    function onEachFeature(feature, layer) {
        const props = feature.properties || {};
        const regionKey = props.region_key;

        layer.on({
            mouseover: (e) => {
                e.target.setStyle(getHoverStyle(feature));
                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                    e.target.bringToFront();
                }
            },
            mouseout: (e) => {
                if (geoJsonRef.current) {
                    geoJsonRef.current.resetStyle(e.target);
                }

                const isSelected = selectedRegion?.region_key === props.region_key;
                if (isSelected) {
                    e.target.setStyle(getBaseStyle(feature));
                }
            },
            click: () => {
                onSelectRegion(props);
            },
        });

        let body = "";

        if (viewMode === "diversity") {
            body = `Diversity index: ${props.diversity_index != null ? Number(props.diversity_index).toFixed(3) : "n/a"
                }`;
        } else if (viewMode === "urban") {
            body = `
        Urban share: ${props.urban_percent != null ? Number(props.urban_percent).toFixed(1) + "%" : "n/a"
                }<br/>
        Rural share: ${props.rural_percent != null ? Number(props.rural_percent).toFixed(1) + "%" : "n/a"
                }
      `;
        } else if (selectedEthnicity === "dominant") {
            body = `Dominant ethnicity: ${props.dominant_ethnicity || "n/a"}<br/>
              Share: ${props.dominant_percent != null
                    ? Number(props.dominant_percent).toFixed(1) + "%"
                    : "n/a"
                }`;
        } else {
            const pct = ethnicityLookup?.[regionKey]?.[selectedEthnicity];
            body = `${selectedEthnicity}: ${pct != null ? Number(pct).toFixed(1) + "%" : "0.0%"}`;
        }

        layer.bindPopup(`
      <div style="min-width: 180px; line-height: 1.5;">
        <div style="font-weight: 700; margin-bottom: 6px;">
          ${props.region_name || "Unknown region"}
        </div>
        <div style="color: #374151;">
          ${body}
        </div>
      </div>
    `);
    }

    return (
        <div style={{ position: "relative", height: "100%", width: "100%" }}>
            <MapContainer
                center={[43, 64]}
                zoom={5}
                scrollWheelZoom={true}
                style={{ height: "100%", width: "100%" }}
            >
                <FitToData regions={regions} />
                <TileLayer
                    attribution="&copy; OpenStreetMap contributors"
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <GeoJSON
                    key={`${viewMode}-${selectedEthnicity}-${selectedRegion?.region_key || "none"}`}
                    ref={geoJsonRef}
                    data={regions}
                    style={style}
                    onEachFeature={onEachFeature}
                />
            </MapContainer>

            <Legend viewMode={viewMode} selectedEthnicity={selectedEthnicity} />
        </div>
    );
}