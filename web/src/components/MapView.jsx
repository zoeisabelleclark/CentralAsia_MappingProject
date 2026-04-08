import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import regions from "../data/regions.geojson";

function getFillColor(feature) {
    const pct = feature.properties.percent ?? 0;
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
    const name = feature.properties.region_name || "Unknown region";
    const language = feature.properties.ethnicities || "No data";
    const percent = feature.properties.percent ?? "n/a";

    layer.bindPopup(`
    <strong>${name}</strong><br/>
    Dominant language: ${language}<br/>
    Percent: ${percent}
  `);
}

export default function MapView() {
    return (
        <MapContainer
            center={[43.5, 68.0]}
            zoom={4}
            scrollWheelZoom={true}
            className="h-full w-full"
        >
            <TileLayer
                attribution='&copy; OpenStreetMap contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <GeoJSON data={regions} style={style} onEachFeature={onEachFeature} />
        </MapContainer>
    );
}