import React from "react";
import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function getFillColor(feature) {
    const pct = feature?.properties?.dominant_percent ?? 0;
    if (pct > 75) return "#0f172a";
    if (pct > 50) return "#334155";
    if (pct > 25) return "#64748b";
    if (pct > 10) return "#94a3b8";
    return "#cbd5e1";
}

function style(feature) {
    return {
        fillColor: getFillColor(feature),
        weight: 1,
        opacity: 1,
        color: "white",
        fillOpacity: 0.8,
    };
}

function onEachFeature(feature, layer) {
    const props = feature.properties || {};
    const name = props.region_name || "Unknown region";
    const ethnicity = props.dominant_ethnicity || "No data";
    const percent =
        props.dominant_percent != null
            ? `${Number(props.dominant_percent).toFixed(1)}%`
            : "n/a";

    layer.bindPopup(`
    <strong>${name}</strong><br/>
    Dominant ethnicity: ${ethnicity}<br/>
    Percent: ${percent}
  `);
}

export default function MapView() {
    const [regions, setRegions] = useState(null);

    useEffect(() => {
        fetch("/data/regions.geojson")
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`Failed to load GeoJSON: ${res.status}`);
                }
                return res.json();
            })
            .then((data) => setRegions(data))
            .catch((err) => console.error(err));
    }, []);

    return (
        <div style={{ height: "80vh", width: "100%" }}>
            <MapContainer
                center={[48, 68]}
                zoom={5}
                scrollWheelZoom={true}
                style={{ height: "100%", width: "100%" }}
            >
                <TileLayer
                    attribution="&copy; OpenStreetMap contributors"
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {regions && (
                    <GeoJSON
                        data={regions}
                        style={style}
                        onEachFeature={onEachFeature}
                    />
                )}
            </MapContainer>
        </div>
    );
}