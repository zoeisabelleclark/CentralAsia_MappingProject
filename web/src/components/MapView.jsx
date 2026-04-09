import React from "react";
import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import Legend from "./Legend";

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
    layer.on({
        mouseover: (e) => {
            e.target.setStyle({
                weight: 2,
                color: "#000",
                fillOpacity: 0.9,
            });
        },
        mouseout: (e) => {
            e.target.setStyle({
                weight: 1,
                color: "white",
                fillOpacity: 0.8,
            });
        }
    });

    const props = feature.properties;
    layer.bindPopup(`
    <strong>${props.region_name}</strong><br/>
    ${props.dominant_ethnicity}<br/>
    ${props.dominant_percent?.toFixed(1)}%
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
            <Legend></Legend>
        </div>
    );
}