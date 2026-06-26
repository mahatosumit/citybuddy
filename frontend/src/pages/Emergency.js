import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldAlert, Phone, LocateFixed, Hospital, Shield, AlertTriangle, MapPin } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

const GUIDE_META = {
  earthquake: { label: "Earthquake", icon: AlertTriangle },
  monsoon: { label: "Monsoon", icon: AlertTriangle },
  landslide: { label: "Landslide", icon: AlertTriangle },
  altitude: { label: "Altitude", icon: AlertTriangle },
};

export default function Emergency() {
  const [coords, setCoords] = useState(null);
  const { data: numbers } = useQuery({ queryKey: ["emNumbers"], queryFn: api.getEmergencyNumbers });
  const { data: guidance } = useQuery({ queryKey: ["guidanceAll"], queryFn: api.getGuidanceAll });
  const { data: nearby } = useQuery({
    queryKey: ["emNearby", coords],
    queryFn: () => api.getEmergencyNearby(coords[0], coords[1]),
    enabled: !!coords,
  });

  const locate = () => {
    if (!navigator.geolocation) return toast.error("Geolocation not supported");
    navigator.geolocation.getCurrentPosition(
      (pos) => { setCoords([pos.coords.latitude, pos.coords.longitude]); toast.success("Finding nearest help"); },
      () => { setCoords([27.7172, 85.324]); toast("Using Kathmandu as fallback location"); },
    );
  };

  const primary = (numbers || []).filter((n) => ["Police", "Ambulance", "Fire Brigade"].includes(n.name));
  const others = (numbers || []).filter((n) => !primary.includes(n));

  return (
    <div className="max-w-[1000px] px-4 sm:px-6 lg:px-8 py-6">
      <div className="rounded-2xl border border-destructive/30 bg-destructive/5 p-4 mb-5">
        <h1 className="font-display text-2xl font-semibold flex items-center gap-2 text-destructive">
          <ShieldAlert className="h-6 w-6" /> Emergency Mode
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">Stay calm. Tap to call. Nepal emergency services & safety guidance.</p>
      </div>

      {/* Call now */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {primary.map((n) => (
          <a key={n.name} href={`tel:${n.number}`} data-testid={`emergency-call-${n.name.toLowerCase().split(" ")[0]}`}>
            <Card className="flex items-center gap-3 p-4 min-h-[64px] border-destructive/30 bg-destructive/5 hover:bg-destructive/10 transition-colors">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-destructive text-destructive-foreground">
                <Phone className="h-5 w-5" />
              </div>
              <div>
                <p className="font-display font-semibold">{n.name}</p>
                <p className="text-xl font-bold text-destructive">{n.number}</p>
              </div>
            </Card>
          </a>
        ))}
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        {others.map((n) => (
          <a key={n.name} href={`tel:${n.number}`}>
            <Badge variant="outline" className="gap-1.5 px-3 py-2 text-sm"><Phone className="h-3.5 w-3.5" />{n.name}: <b>{n.number}</b></Badge>
          </a>
        ))}
      </div>

      {/* Nearest facilities */}
      <section className="mt-6">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-lg">Nearest hospitals & police</h2>
          <Button size="sm" variant="outline" onClick={locate} data-testid="emergency-locate" className="gap-1.5">
            <LocateFixed className="h-4 w-4" /> Use my location
          </Button>
        </div>
        <div className="mt-3 grid gap-3 sm:grid-cols-2">
          {!coords && <p className="text-sm text-muted-foreground">Tap “Use my location” to find the closest facilities.</p>}
          {(nearby || []).map((f) => (
            <Card key={f.id} data-testid="emergency-nearest-hospital" className="flex items-start gap-3 p-3.5">
              <div className={`flex h-9 w-9 items-center justify-center rounded-xl ${f.type === "hospital" ? "bg-destructive/12 text-destructive" : "bg-primary/12 text-primary"}`}>
                {f.type === "hospital" ? <Hospital className="h-4.5 w-4.5" /> : <Shield className="h-4.5 w-4.5" />}
              </div>
              <div className="min-w-0 flex-1">
                <p className="font-medium text-sm">{f.name}</p>
                <p className="flex items-center gap-1 text-xs text-muted-foreground"><MapPin className="h-3 w-3" />{f.address}</p>
                <a href={`tel:${f.phone}`} className="mt-1 inline-flex items-center gap-1 text-xs font-medium text-destructive"><Phone className="h-3 w-3" />{f.phone}</a>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* Guidance */}
      <section className="mt-6" data-testid="emergency-guidance">
        <h2 className="font-semibold text-lg mb-3">Safety guidance</h2>
        {guidance && (
          <Tabs defaultValue="earthquake">
            <TabsList className="flex-wrap h-auto">
              {Object.keys(guidance).map((k) => (
                <TabsTrigger key={k} value={k} className="capitalize">{GUIDE_META[k]?.label || k}</TabsTrigger>
              ))}
            </TabsList>
            {Object.entries(guidance).map(([k, steps]) => (
              <TabsContent key={k} value={k} className="pt-3">
                <Card className="p-4">
                  <ol className="space-y-2.5">
                    {steps.map((s, i) => (
                      <li key={i} className="flex gap-3 text-sm">
                        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent/15 text-accent text-xs font-semibold">{i + 1}</span>
                        <span className="text-muted-foreground">{s}</span>
                      </li>
                    ))}
                  </ol>
                </Card>
              </TabsContent>
            ))}
          </Tabs>
        )}
      </section>
    </div>
  );
}
