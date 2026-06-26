import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import {
  MessageSquare, Map, CalendarRange, CloudSun, Camera, ShieldAlert,
  Sparkles, ArrowRight, Star, MapPin,
} from "lucide-react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { PlaceCard } from "@/components/PlaceCard";

const QUICK = [
  { to: "/chat", label: "Ask CityBrain", desc: "AI that reasons, not just searches", icon: MessageSquare, color: "hsl(var(--route))" },
  { to: "/explore", label: "Explore Map", desc: "Discover places near you", icon: Map, color: "#0EA5A4" },
  { to: "/planner", label: "Plan a Trip", desc: "AI day-by-day itineraries", icon: CalendarRange, color: "#1E2A5A" },
  { to: "/weather", label: "Weather", desc: "Live forecasts across Nepal", icon: CloudSun, color: "#F59E0B" },
  { to: "/camera", label: "Camera AI", desc: "Identify temples & food", icon: Camera, color: "#0EA5A4" },
  { to: "/emergency", label: "Emergency", desc: "Help & safety, fast", icon: ShieldAlert, color: "#DC2626" },
];

export default function Home() {
  const { data: cities } = useQuery({ queryKey: ["cities"], queryFn: api.getCities });
  const { data: featured } = useQuery({
    queryKey: ["featured"],
    queryFn: () => api.getPlaces({ sort: "rating", limit: 8 }),
  });

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="https://images.pexels.com/photos/9275921/pexels-photo-9275921.jpeg?auto=compress&cs=tinysrgb&w=1600"
            alt="Himalayas"
            className="h-full w-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/85 to-background/30" />
        </div>
        <div className="relative px-4 sm:px-6 lg:px-8 pt-16 pb-12 lg:pt-24 lg:pb-16 max-w-[1100px]">
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <Badge className="gap-1.5 bg-accent/15 text-accent border-0">
              <Sparkles className="h-3.5 w-3.5" /> Powered by CityBrain AI
            </Badge>
            <h1 className="mt-4 text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-balance">
              Your AI Companion<br />for Nepal
            </h1>
            <p className="mt-4 max-w-xl text-base sm:text-lg text-muted-foreground">
              Maps, trip planning, weather, budgets, emergencies and deep local knowledge — unified into one
              intelligent companion that <span className="text-foreground font-medium">reasons</span> before it recommends.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link to="/chat"><Button size="lg" data-testid="hero-chat-btn" className="gap-2">
                <MessageSquare className="h-4 w-4" /> Ask CityBrain
              </Button></Link>
              <Link to="/explore"><Button size="lg" variant="outline" data-testid="hero-explore-btn" className="gap-2">
                <Map className="h-4 w-4" /> Explore Nepal
              </Button></Link>
            </div>
          </motion.div>
        </div>
      </section>

      <div className="px-4 sm:px-6 lg:px-8 pb-16 space-y-12 max-w-[1200px]">
        {/* Quick actions */}
        <section>
          <h2 className="text-xl font-semibold mb-4">What can I help with?</h2>
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-3">
            {QUICK.map((q, i) => {
              const Icon = q.icon;
              return (
                <motion.div key={q.to} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.25, delay: i * 0.04 }}>
                  <Link to={q.to}>
                    <Card className="group p-4 h-full card-hover border-border" data-testid={`quick-${q.to.slice(1)}`}>
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl"
                        style={{ backgroundColor: `${q.color}1f`, color: q.color }}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <h3 className="mt-3 font-display font-semibold text-[15px] flex items-center gap-1">
                        {q.label}
                        <ArrowRight className="h-3.5 w-3.5 opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                      </h3>
                      <p className="text-xs text-muted-foreground mt-0.5">{q.desc}</p>
                    </Card>
                  </Link>
                </motion.div>
              );
            })}
          </div>
        </section>

        {/* Featured cities */}
        {cities?.length > 0 && (
          <section>
            <h2 className="text-xl font-semibold mb-4">Explore by city</h2>
            <div className="flex gap-2 overflow-x-auto no-scrollbar pb-1">
              {cities.map((c) => (
                <Link key={c.city} to={`/explore?city=${encodeURIComponent(c.city)}`}>
                  <Badge variant="secondary" className="gap-1.5 px-3 py-2 text-sm whitespace-nowrap card-hover">
                    <MapPin className="h-3.5 w-3.5 text-accent" /> {c.city}
                    <span className="text-muted-foreground">{c.count}</span>
                  </Badge>
                </Link>
              ))}
            </div>
          </section>
        )}

        {/* Featured places */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Star className="h-5 w-5 text-accent" /> Top rated in Nepal
            </h2>
            <Link to="/explore"><Button variant="ghost" size="sm" className="gap-1">See all <ArrowRight className="h-3.5 w-3.5" /></Button></Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {(featured || []).slice(0, 8).map((p) => <PlaceCard key={p.id} place={p} />)}
          </div>
        </section>
      </div>
    </div>
  );
}
