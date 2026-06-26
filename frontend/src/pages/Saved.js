import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { Bookmark, CalendarRange, Trash2, MapPin, Compass } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { PlaceCard } from "@/components/PlaceCard";
import { EmptyState, PageLoader } from "@/components/common/States";
import { formatNPR } from "@/lib/ui";

export default function Saved() {
  const qc = useQueryClient();
  const { data: favorites, isLoading: lf } = useQuery({ queryKey: ["favorites"], queryFn: api.getFavorites });
  const { data: favIds } = useQuery({ queryKey: ["favIds"], queryFn: api.getFavoriteIds });
  const { data: trips, isLoading: lt } = useQuery({ queryKey: ["trips"], queryFn: api.getTrips });

  const removeFav = async (id) => {
    await api.removeFavorite(id); toast("Removed");
    qc.invalidateQueries({ queryKey: ["favorites"] }); qc.invalidateQueries({ queryKey: ["favIds"] });
  };
  const delTrip = async (id) => {
    await api.deleteTrip(id); toast("Trip deleted");
    qc.invalidateQueries({ queryKey: ["trips"] });
  };

  return (
    <div className="max-w-[1100px] px-4 sm:px-6 lg:px-8 py-6">
      <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
        <Bookmark className="h-6 w-6 text-accent" /> Saved
      </h1>

      <Tabs defaultValue="places" className="mt-4">
        <TabsList>
          <TabsTrigger value="places" data-testid="saved-tab-places">Favorites ({favorites?.length || 0})</TabsTrigger>
          <TabsTrigger value="trips" data-testid="saved-tab-trips">Trips ({trips?.length || 0})</TabsTrigger>
        </TabsList>

        <TabsContent value="places" className="pt-4">
          {lf ? <PageLoader /> : (favorites || []).length === 0 ? (
            <EmptyState icon={Bookmark} title="No saved places yet"
              description="Tap the heart on any place to save it here."
              action={<Link to="/explore"><Button className="gap-1.5"><Compass className="h-4 w-4" /> Explore places</Button></Link>}
              testid="saved-empty" />
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {favorites.map((p) => <PlaceCard key={p.id} place={p} isFavorite={(favIds || []).includes(p.id)} onToggleFavorite={removeFav} />)}
            </div>
          )}
        </TabsContent>

        <TabsContent value="trips" className="pt-4">
          {lt ? <PageLoader /> : (trips || []).length === 0 ? (
            <EmptyState icon={CalendarRange} title="No saved trips"
              description="Generate an itinerary in the Trip Planner and save it."
              action={<Link to="/planner"><Button className="gap-1.5"><CalendarRange className="h-4 w-4" /> Plan a trip</Button></Link>} />
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {trips.map((t) => (
                <Card key={t.id} className="p-4">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="font-display font-semibold">{t.title}</h3>
                      <div className="mt-1 flex flex-wrap gap-1.5">
                        <Badge variant="secondary" className="gap-1"><MapPin className="h-3 w-3" />{t.city}</Badge>
                        <Badge variant="secondary">{t.days} days</Badge>
                        {t.estimated_cost_npr != null && <Badge variant="secondary">~{formatNPR(t.estimated_cost_npr)}</Badge>}
                      </div>
                    </div>
                    <button onClick={() => delTrip(t.id)} className="rounded-lg p-1.5 text-muted-foreground hover:text-destructive"><Trash2 className="h-4 w-4" /></button>
                  </div>
                  <p className="mt-2 text-sm text-muted-foreground line-clamp-2">{t.summary}</p>
                  <div className="mt-3 space-y-1">
                    {(t.itinerary || []).slice(0, 3).map((d) => (
                      <p key={d.day} className="text-xs text-muted-foreground"><b className="text-foreground">Day {d.day}:</b> {d.theme}</p>
                    ))}
                  </div>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
