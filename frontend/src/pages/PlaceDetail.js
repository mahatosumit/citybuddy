import { useParams, Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Star, Heart, MapPin, Clock, ArrowLeft, MessageSquare, Send } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { MapView } from "@/components/MapView";
import { PlaceCard } from "@/components/PlaceCard";
import { PageLoader } from "@/components/common/States";
import { typeMeta, formatNPR } from "@/lib/ui";

export default function PlaceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [name, setName] = useState("");

  const { data: place, isLoading } = useQuery({ queryKey: ["place", id], queryFn: () => api.getPlace(id) });
  const { data: reviews } = useQuery({ queryKey: ["reviews", id], queryFn: () => api.getReviews(id) });
  const { data: favIds } = useQuery({ queryKey: ["favIds"], queryFn: api.getFavoriteIds });

  if (isLoading || !place) return <PageLoader label="Loading place…" />;
  const meta = typeMeta(place.type);
  const TypeIcon = meta.icon;
  const isFav = (favIds || []).includes(place.id);

  const toggleFav = async () => {
    try {
      if (isFav) { await api.removeFavorite(place.id); toast("Removed from saved"); }
      else { await api.addFavorite(place.id); toast.success("Saved to favorites"); }
      qc.invalidateQueries({ queryKey: ["favIds"] });
    } catch { toast.error("Could not update"); }
  };

  const submitReview = async () => {
    if (!comment.trim()) return toast.error("Please write a short review");
    try {
      await api.addReview(place.id, { rating, comment, user_name: name || "Traveler" });
      toast.success("Review posted");
      setComment(""); setName("");
      qc.invalidateQueries({ queryKey: ["reviews", id] });
      qc.invalidateQueries({ queryKey: ["place", id] });
    } catch { toast.error("Could not post review"); }
  };

  return (
    <div className="max-w-[1100px] px-4 sm:px-6 lg:px-8 py-5">
      <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="gap-1.5 mb-3 -ml-2">
        <ArrowLeft className="h-4 w-4" /> Back
      </Button>

      <div className="relative overflow-hidden rounded-2xl">
        <img src={place.image_url} alt={place.name} className="h-56 sm:h-72 w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/55 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-5 text-white">
          <Badge className="gap-1 border-0 bg-white/20 text-white backdrop-blur mb-2">
            <TypeIcon className="h-3 w-3" /> {meta.label}
          </Badge>
          <h1 className="font-display text-2xl sm:text-3xl font-semibold">{place.name}</h1>
          <p className="mt-1 flex items-center gap-3 text-sm text-white/90">
            <span className="flex items-center gap-1"><MapPin className="h-4 w-4" />{place.city}, {place.region}</span>
            <span className="flex items-center gap-1"><Star className="h-4 w-4 fill-accent text-accent" />{place.rating}</span>
          </p>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <span className="text-xl font-semibold">{formatNPR(place.price_npr)}{place.type === "hotel" && place.price_npr > 0 && <span className="text-sm font-normal text-muted-foreground">/night</span>}</span>
        <div className="ml-auto flex gap-2">
          <Button variant={isFav ? "default" : "outline"} onClick={toggleFav} data-testid="place-detail-save" className="gap-1.5">
            <Heart className={`h-4 w-4 ${isFav ? "fill-current" : ""}`} /> {isFav ? "Saved" : "Save"}
          </Button>
          <Link to="/chat"><Button variant="outline" className="gap-1.5"><MessageSquare className="h-4 w-4" /> Ask CityBrain</Button></Link>
        </div>
      </div>

      <div className="mt-5 grid gap-5 lg:grid-cols-[1fr_360px]">
        <div>
          <Tabs defaultValue="overview" data-testid="place-tabs">
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="reviews">Reviews ({reviews?.length || 0})</TabsTrigger>
            </TabsList>
            <TabsContent value="overview" className="space-y-4 pt-3">
              <p className="text-[15px] leading-relaxed text-muted-foreground">{place.description}</p>
              <div className="grid grid-cols-2 gap-3">
                <Card className="p-3"><p className="flex items-center gap-1.5 text-xs text-muted-foreground"><Clock className="h-3.5 w-3.5" /> Hours</p><p className="mt-1 text-sm font-medium">{place.hours || "—"}</p></Card>
                <Card className="p-3"><p className="flex items-center gap-1.5 text-xs text-muted-foreground"><MapPin className="h-3.5 w-3.5" /> Address</p><p className="mt-1 text-sm font-medium">{place.address}</p></Card>
              </div>
              {place.tags?.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {place.tags.map((t) => <Badge key={t} variant="secondary" className="text-[11px] capitalize">{t}</Badge>)}
                </div>
              )}
            </TabsContent>
            <TabsContent value="reviews" className="space-y-4 pt-3">
              <Card className="p-4 space-y-3">
                <p className="text-sm font-medium">Write a review</p>
                <div className="flex items-center gap-1">
                  {[1,2,3,4,5].map((n) => (
                    <button key={n} onClick={() => setRating(n)} data-testid={`star-${n}`}>
                      <Star className={`h-6 w-6 ${n <= rating ? "fill-accent text-accent" : "text-muted-foreground"}`} />
                    </button>
                  ))}
                </div>
                <Input placeholder="Your name (optional)" value={name} onChange={(e) => setName(e.target.value)} />
                <Textarea data-testid="review-input" placeholder="Share your experience…" value={comment} onChange={(e) => setComment(e.target.value)} />
                <Button onClick={submitReview} data-testid="review-submit" className="gap-1.5"><Send className="h-4 w-4" /> Post review</Button>
              </Card>
              {(reviews || []).length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-6">No reviews yet. Be the first!</p>
              ) : (reviews || []).map((r) => (
                <Card key={r.id} className="p-3.5">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-sm">{r.user_name}</span>
                    <span className="flex items-center gap-0.5 text-sm"><Star className="h-3.5 w-3.5 fill-accent text-accent" />{r.rating}</span>
                  </div>
                  <p className="mt-1.5 text-sm text-muted-foreground">{r.comment}</p>
                </Card>
              ))}
            </TabsContent>
          </Tabs>
        </div>

        <div className="space-y-4">
          <Card className="overflow-hidden h-56">
            <MapView places={[place]} center={[place.lat, place.lon]} zoom={14} />
          </Card>
        </div>
      </div>

      {place.nearby?.length > 0 && (
        <section className="mt-8">
          <h2 className="text-lg font-semibold mb-3">Nearby in {place.city}</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {place.nearby.slice(0, 4).map((p) => <PlaceCard key={p.id} place={p} />)}
          </div>
        </section>
      )}
    </div>
  );
}
