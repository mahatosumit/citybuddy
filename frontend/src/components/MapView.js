import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Link } from "react-router-dom";
import { renderToStaticMarkup } from "react-dom/server";
import { typeMeta, formatNPR } from "@/lib/ui";

function makeIcon(type, active) {
  const meta = typeMeta(type);
  const Icon = meta.icon;
  const svg = renderToStaticMarkup(<Icon size={15} color="#fff" />);
  return L.divIcon({
    className: `cb-pin ${active ? "cb-pin-active" : ""}`,
    html: `<div class="cb-pin-inner" style="background:${meta.color}">${svg}</div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 28],
    popupAnchor: [0, -28],
  });
}

function Recenter({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) map.flyTo(center, zoom || map.getZoom(), { duration: 0.6 });
  }, [center, zoom, map]);
  return null;
}

export function MapView({ places = [], center = [27.7172, 85.324], zoom = 7,
                          selectedId, onSelect, height = "100%" }) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      scrollWheelZoom
      style={{ height, width: "100%" }}
      data-testid="explore-map"
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Recenter center={center} zoom={zoom} />
      {places.filter((p) => p.lat && p.lon).map((p) => (
        <Marker
          key={p.id}
          position={[p.lat, p.lon]}
          icon={makeIcon(p.type, selectedId === p.id)}
          eventHandlers={{ click: () => onSelect && onSelect(p.id) }}
        >
          <Popup>
            <div className="min-w-[170px]">
              <img src={p.image_url} alt={p.name} className="h-20 w-full rounded-md object-cover mb-1.5" />
              <div className="font-semibold text-[13px] leading-tight">{p.name}</div>
              <div className="text-[11px] text-gray-500">{p.city} · {typeMeta(p.type).label}</div>
              <div className="mt-1 flex items-center justify-between">
                <span className="text-[12px] font-medium">{formatNPR(p.price_npr)}</span>
                <Link to={`/place/${p.id}`} className="text-[12px] font-semibold text-[#0EA5A4]">View →</Link>
              </div>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
