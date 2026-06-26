import { useState, useMemo, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Search, LocateFixed, List, Map as MapIcon, SlidersHorizontal } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { Badge } from "@/components/ui/badge";
import { PlaceCard } from "@/components/PlaceCard";
import { MapView } from "@/components/MapView";
import { PageLoader, EmptyState } from "@/components/common/States";
import { typeMeta } from "@/lib/ui";

const TYPES = [
  { v: "", label: "All" },
  { v: "attraction", label: "Attractions" },
  { v: "restaurant", label: "Food" },
  { v: "hotel", label: "Hotels" },
  { v: "event", label: "Events" },
];

export default function Explore() {
  const [params, setParams] = useSearchParams();
  const qc = useQueryClient();
  const [type, setType] = useState("");
  const [city, setCity] = useState(params.get("city") || "");
  const [q, setQ] = useState("");
  const [coords, setCoords] = useState(null);
  const [selected, setSelected] = useState(null);
  const [mobileView, setMobileView] = useState("list");

  const queryParams = useMemo(() => {
    const p = { limit: 80 };
    if (type) p.type = type;
    if (city) p.city = city;
    if (q) p.q = q;
    if (coords) { p.lat = coords[0]; p.lon = coords[1]; p.radius_km = 30; }
    return p;
  }, [type, city, q, coords]);

  const { data: places, isLoading } = useQuery({
    queryKey: ["places", queryParams],
    queryFn: () => api.getPlaces(queryParams),
  });
  const { data: cities } = useQuery({ queryKey: ["cities"], queryFn: api.getCities });
  const { data: favIds } = useQuery({ queryKey: ["favIds"], queryFn: api.getFavoriteIds });

  useEffect(() => { setCity(params.get("city") || ""); }, [params]);

  const toggleFav = async (id) => {
    const isFav = (favIds || []).includes(id);
    try {
      if (isFav) { await api.removeFavorite(id); toast("Removed from saved"); }
      else { await api.addFavorite(id); toast.success("Saved to favorites"); }
      qc.invalidateQueries({ queryKey: ["favIds"] });
      qc.invalidateQueries({ queryKey: ["favorites"] });
    } catch { toast.error("Could not update favorite"); }
  };

  const nearMe = () => {
    if (!navigator.geolocation) return toast.error("Geolocation not supported");
    navigator.geolocation.getCurrentPosition(
      (pos) => { setCoords([pos.coords.latitude, pos.coords.longitude]); setCity(""); toast.success("Showing places near you"); },
      () => toast.error("Location permission denied. Showing Nepal-wide."),
    );
  };

  const list = places || [];
  const mapCenter = coords || (list[0] ? [list[0].lat, list[0].lon] : [27.7172, 85.324]);
  const selectedPlace = list.find((p) => p.id === selected);
  const mapPlaces = selectedPlace ? list : list;

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {/* Controls */}
      <div className="border-b border-border px-4 sm:px-6 py-3 space-y-3">
        <div className="flex items-center gap-2">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input data-testid="explore-search" value={q} onChange={(e) => setQ(e.target.value)}
              placeholder="Search places, food, temples…" className="pl-9" />
          </div>
          <Button variant={coords ? "default" : "outline"} size="sm" onClick={nearMe} data-testid="filter-near-me" className="gap-1.5 shrink-0">
            <LocateFixed className="h-4 w-4" /> <span className="hidden sm:inline">Near me</span>
          </Button>
          <div className="lg:hidden">
            <ToggleGroup type="single" value={mobileView} onValueChange={(v) => v && setMobileView(v)} className="border border-border rounded-lg">
              <ToggleGroupItem value="list" data-testid="view-list" className="px-2.5"><List className="h-4 w-4" /></ToggleGroupItem>
              <ToggleGroupItem value="map" data-testid="view-map" className="px-2.5"><MapIcon className="h-4 w-4" /></ToggleGroupItem>
            </ToggleGroup>
          </div>
        </div>
        <div className="flex gap-2 overflow-x-auto no-scrollbar">
          {TYPES.map((t) => (
            <button key={t.v} data-testid="filter-chip" onClick={() => setType(t.v)}
              className={`rounded-full border px-3 py-1.5 text-xs font-medium whitespace-nowrap transition-colors ${type === t.v ? "border-accent bg-accent/15 text-accent" : "border-border bg-card text-muted-foreground hover:bg-muted"}`}>
              {t.label}
            </button>
          ))}
          <div className="mx-1 w-px bg-border" />
          {(cities || []).map((c) => (
            <button key={c.city} onClick={() => { setCity(city === c.city ? "" : c.city); setCoords(null); }}
              className={`rounded-full border px-3 py-1.5 text-xs font-medium whitespace-nowrap transition-colors ${city === c.city ? "border-primary bg-secondary text-secondary-foreground" : "border-border bg-card text-muted-foreground hover:bg-muted"}`}>
              {c.city}
            </button>
          ))}
        </div>
      </div>

      {/* Body */}
      <div className="flex-1 min-h-0 lg:grid lg:grid-cols-[minmax(380px,420px)_1fr]">
        {/* List */}
        <div data-testid="explore-list" className={`overflow-y-auto p-4 ${mobileView === "map" ? "hidden lg:block" : ""}`}>
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm text-muted-foreground">
              {isLoading ? "Searching…" : `${list.length} place${list.length !== 1 ? "s" : ""}`}
              {coords && <Badge variant="secondary" className="ml-2 text-[11px]">Near you</Badge>}
            </p>
          </div>
          {isLoading ? <PageLoader /> : list.length === 0 ? (
            <EmptyState title="No places found" description="Try a different filter, city, or search term." testid="explore-empty" />
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-3">
              {list.map((p) => (
                <div key={p.id} onMouseEnter={() => setSelected(p.id)}>
                  <PlaceCard place={p} isFavorite={(favIds || []).includes(p.id)} onToggleFavorite={toggleFav} />
                </div>
              ))}
            </div>
          )}
        </div>
        {/* Map */}
        <div className={`relative ${mobileView === "list" ? "hidden lg:block" : ""} h-full min-h-[300px]`}>
          <MapView places={mapPlaces} center={mapCenter} zoom={coords ? 12 : city ? 12 : 7}
            selectedId={selected} onSelect={setSelected} />
        </div>
      </div>
    </div>
  );
}
