import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { CalendarRange, Sparkles, Save, Clock, Banknote, Lightbulb, ShieldAlert, Wand2 } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useLanguage } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PageLoader } from "@/components/common/States";
import { formatNPR } from "@/lib/ui";

const CITIES = ["Kathmandu", "Pokhara", "Bhaktapur", "Lalitpur", "Chitwan", "Lumbini", "Mustang", "Ilam", "Dharan", "Janakpur"];
const INTERESTS = ["heritage", "nature", "food", "adventure", "spiritual", "shopping", "photography", "trekking"];

export default function Planner() {
  const { lang } = useLanguage();
  const [city, setCity] = useState("Pokhara");
  const [days, setDays] = useState(2);
  const [budget, setBudget] = useState("");
  const [interests, setInterests] = useState(["nature", "food"]);
  const [trip, setTrip] = useState(null);

  const gen = useMutation({
    mutationFn: () => api.generateTrip({ city, days: Number(days), budget_npr: budget ? Number(budget) : null, interests, language: lang }),
    onSuccess: (d) => { setTrip(d); toast.success("Itinerary ready!"); },
    onError: () => toast.error("Could not generate itinerary. Try again."),
  });

  const save = useMutation({
    mutationFn: () => api.saveTrip({
      title: trip.title, city: trip.city, days: trip.days, summary: trip.summary,
      estimated_cost_npr: trip.estimated_cost_npr, itinerary: trip.itinerary,
      tips: trip.tips || [], safety_notes: trip.safety_notes || [],
    }),
    onSuccess: () => toast.success("Trip saved to your collection"),
    onError: () => toast.error("Could not save trip"),
  });

  const toggleInterest = (i) => setInterests((prev) => prev.includes(i) ? prev.filter((x) => x !== i) : [...prev, i]);

  return (
    <div className="max-w-[1100px] px-4 sm:px-6 lg:px-8 py-6">
      <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
        <CalendarRange className="h-6 w-6 text-accent" /> AI Trip Planner
      </h1>
      <p className="mt-1 text-sm text-muted-foreground">CityBrain builds a realistic, budget-aware itinerary grounded in real places & weather.</p>

      <Card className="mt-5 p-4 sm:p-5">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <label className="text-xs font-medium text-muted-foreground">Destination</label>
            <Select value={city} onValueChange={setCity}>
              <SelectTrigger className="mt-1" data-testid="planner-city"><SelectValue /></SelectTrigger>
              <SelectContent>{CITIES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-xs font-medium text-muted-foreground">Days</label>
            <Select value={String(days)} onValueChange={(v) => setDays(Number(v))}>
              <SelectTrigger className="mt-1" data-testid="planner-days"><SelectValue /></SelectTrigger>
              <SelectContent>{[1,2,3,4,5,6,7].map((d) => <SelectItem key={d} value={String(d)}>{d} day{d>1?"s":""}</SelectItem>)}</SelectContent>
            </Select>
          </div>
          <div className="sm:col-span-2">
            <label className="text-xs font-medium text-muted-foreground">Total budget (NPR, optional)</label>
            <Input data-testid="planner-budget" type="number" value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="e.g. 8000" className="mt-1" />
          </div>
        </div>
        <div className="mt-4">
          <label className="text-xs font-medium text-muted-foreground">Interests</label>
          <div className="mt-1.5 flex flex-wrap gap-2">
            {INTERESTS.map((i) => (
              <button key={i} onClick={() => toggleInterest(i)}
                className={`rounded-full border px-3 py-1.5 text-xs font-medium capitalize transition-colors ${interests.includes(i) ? "border-accent bg-accent/15 text-accent" : "border-border bg-card text-muted-foreground hover:bg-muted"}`}>
                {i}
              </button>
            ))}
          </div>
        </div>
        <Button data-testid="planner-generate" className="mt-5 gap-2" onClick={() => gen.mutate()} disabled={gen.isPending}>
          <Wand2 className="h-4 w-4" /> {gen.isPending ? "Generating…" : "Generate Itinerary"}
        </Button>
      </Card>

      {gen.isPending && <PageLoader label="CityBrain is crafting your itinerary… this can take ~30s" />}

      {trip && !gen.isPending && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-6">
          <Card className="p-5 border-l-4 border-l-accent">
            <div className="flex items-start justify-between gap-3 flex-wrap">
              <div>
                <h2 className="font-display text-xl font-semibold">{trip.title}</h2>
                <p className="mt-1 text-sm text-muted-foreground max-w-xl">{trip.summary}</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  <Badge variant="secondary" className="gap-1">{trip.city}</Badge>
                  <Badge variant="secondary" className="gap-1"><CalendarRange className="h-3 w-3" />{trip.days} days</Badge>
                  {trip.estimated_cost_npr != null && <Badge variant="secondary" className="gap-1"><Banknote className="h-3 w-3" />~{formatNPR(trip.estimated_cost_npr)}</Badge>}
                </div>
              </div>
              <Button data-testid="itinerary-save" onClick={() => save.mutate()} disabled={save.isPending} className="gap-1.5">
                <Save className="h-4 w-4" /> Save trip
              </Button>
            </div>
          </Card>

          <div className="mt-4 space-y-4">
            {(trip.itinerary || []).map((day) => (
              <Card key={day.day} data-testid="itinerary-day" className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground text-sm font-semibold">{day.day}</div>
                  <h3 className="font-display font-semibold">{day.theme}</h3>
                </div>
                <div className="space-y-3 border-l-2 border-dashed border-border ml-4 pl-5">
                  {(day.stops || []).map((s, i) => (
                    <div key={i} className="relative">
                      <span className="absolute -left-[27px] top-1 h-3 w-3 rounded-full bg-accent ring-4 ring-background" />
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <p className="flex items-center gap-1.5 text-xs text-muted-foreground"><Clock className="h-3 w-3" />{s.time}</p>
                          <p className="font-medium text-sm mt-0.5">{s.title}</p>
                          <p className="text-[13px] text-muted-foreground mt-0.5">{s.detail}</p>
                        </div>
                        {s.cost_npr != null && <Badge variant="outline" className="shrink-0 text-[11px]">{formatNPR(s.cost_npr)}</Badge>}
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            ))}
          </div>

          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            {trip.tips?.length > 0 && (
              <Card className="p-4">
                <p className="flex items-center gap-1.5 font-medium text-sm"><Lightbulb className="h-4 w-4 text-accent" /> Tips</p>
                <ul className="mt-2 space-y-1.5 text-[13px] text-muted-foreground">
                  {trip.tips.map((t, i) => <li key={i} className="flex gap-2"><span className="text-accent">•</span>{t}</li>)}
                </ul>
              </Card>
            )}
            {trip.safety_notes?.length > 0 && (
              <Card className="p-4 border-destructive/30 bg-destructive/5">
                <p className="flex items-center gap-1.5 font-medium text-sm text-destructive"><ShieldAlert className="h-4 w-4" /> Safety</p>
                <ul className="mt-2 space-y-1.5 text-[13px] text-muted-foreground">
                  {trip.safety_notes.map((t, i) => <li key={i} className="flex gap-2"><span className="text-destructive">•</span>{t}</li>)}
                </ul>
              </Card>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}
