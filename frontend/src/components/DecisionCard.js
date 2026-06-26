import { Lightbulb, MapPin, CheckCircle2, Utensils, Hotel, Footprints, Banknote } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatNPR } from "@/lib/ui";

const ICONS = {
  place: MapPin, tip: Lightbulb, step: CheckCircle2, restaurant: Utensils,
  hotel: Hotel, activity: Footprints, food: Utensils, transport: Footprints,
  attraction: MapPin,
};

export function DecisionCard({ rec, index }) {
  const Icon = ICONS[rec.type] || Lightbulb;
  return (
    <Card
      data-testid="decision-card"
      className="flex gap-3 border-border bg-card p-3.5 border-l-4 border-l-[hsl(var(--route))] card-hover"
    >
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[hsl(var(--route))]/12 text-[hsl(var(--route))]">
        <Icon className="h-[18px] w-[18px]" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-2">
          <h4 className="font-display font-semibold text-sm leading-snug">{rec.title}</h4>
          {rec.cost_npr !== null && rec.cost_npr !== undefined && (
            <Badge variant="secondary" className="shrink-0 gap-1 text-[11px]">
              <Banknote className="h-3 w-3" /> {formatNPR(rec.cost_npr)}
            </Badge>
          )}
        </div>
        <p className="mt-1 text-[13px] leading-relaxed text-muted-foreground">{rec.detail}</p>
      </div>
    </Card>
  );
}
