import { Link } from "react-router-dom";
import { Star, Heart, MapPin } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { typeMeta, formatNPR } from "@/lib/ui";

export function PlaceCard({ place, isFavorite, onToggleFavorite, compact }) {
  const meta = typeMeta(place.type);
  const TypeIcon = meta.icon;
  return (
    <Card
      data-testid="place-card"
      className={cn("group overflow-hidden border-border bg-card card-hover", compact ? "flex" : "")}
    >
      <Link to={`/place/${place.id}`} className={cn("block relative overflow-hidden", compact ? "w-32 shrink-0" : "")}>
        <div className={cn("overflow-hidden bg-muted", compact ? "h-full" : "aspect-[16/10]")}>
          <img
            src={place.image_url}
            alt={place.name}
            loading="lazy"
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
        </div>
        {!compact && (
          <Badge className="absolute left-3 top-3 gap-1 border-0 bg-background/85 text-foreground backdrop-blur">
            <TypeIcon className="h-3 w-3" style={{ color: meta.color }} />
            {meta.label}
          </Badge>
        )}
      </Link>

      <div className={cn("p-3.5", compact && "flex-1")}>
        <div className="flex items-start justify-between gap-2">
          <Link to={`/place/${place.id}`} className="min-w-0 focus-ring">
            <h3 className="font-display font-semibold text-[15px] leading-snug truncate">{place.name}</h3>
            <p className="mt-0.5 flex items-center gap-1 text-xs text-muted-foreground">
              <MapPin className="h-3 w-3" /> {place.city}
            </p>
          </Link>
          {onToggleFavorite && (
            <button
              data-testid="place-card-save"
              aria-label="Save place"
              onClick={(e) => { e.preventDefault(); onToggleFavorite(place.id); }}
              className="shrink-0 rounded-full p-1.5 hover:bg-muted transition-colors focus-ring"
            >
              <Heart className={cn("h-[18px] w-[18px] transition-colors",
                isFavorite ? "fill-accent text-accent" : "text-muted-foreground")} />
            </button>
          )}
        </div>

        {!compact && (
          <p className="mt-2 text-xs text-muted-foreground line-clamp-2">{place.description}</p>
        )}

        <div className="mt-3 flex items-center justify-between">
          <span className="inline-flex items-center gap-1 text-sm font-medium">
            <Star className="h-3.5 w-3.5 fill-accent text-accent" /> {place.rating}
          </span>
          <span className="text-sm font-semibold">
            {place.type === "hotel" && place.price_npr > 0 ? (
              <>{formatNPR(place.price_npr)}<span className="text-xs font-normal text-muted-foreground">/night</span></>
            ) : formatNPR(place.price_npr)}
          </span>
        </div>
      </div>
    </Card>
  );
}
