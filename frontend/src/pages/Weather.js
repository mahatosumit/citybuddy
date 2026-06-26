import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CloudSun } from "lucide-react";
import { api } from "@/lib/api";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { PageLoader } from "@/components/common/States";
import { CurrentWeather, ForecastStrip, weatherIcon } from "@/components/WeatherWidget";

const CITIES = ["Kathmandu", "Pokhara", "Bhaktapur", "Lalitpur", "Chitwan", "Lumbini", "Mustang", "Ilam", "Dharan", "Janakpur", "Biratnagar", "Butwal"];

export default function Weather() {
  const [city, setCity] = useState("Kathmandu");
  const { data, isLoading } = useQuery({ queryKey: ["weather", city], queryFn: () => api.getWeather({ city }) });

  return (
    <div className="max-w-[1000px] px-4 sm:px-6 lg:px-8 py-6">
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
          <CloudSun className="h-6 w-6 text-accent" /> Weather across Nepal
        </h1>
        <Select value={city} onValueChange={setCity}>
          <SelectTrigger className="w-44" data-testid="weather-city"><SelectValue /></SelectTrigger>
          <SelectContent>{CITIES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
        </Select>
      </div>

      {isLoading ? <PageLoader label="Fetching live weather…" /> : data && (
        <div className="mt-5 space-y-5">
          <div className="grid gap-4 lg:grid-cols-2">
            <CurrentWeather data={data} city={data.city} />
            <Card className="p-5">
              <h3 className="font-medium text-sm mb-3">Next hours</h3>
              <div className="flex gap-3 overflow-x-auto no-scrollbar">
                {(data.hourly || []).slice(0, 12).map((h) => (
                  <div key={h.time} className="flex flex-col items-center gap-1 rounded-xl bg-muted/50 px-3 py-2 min-w-[60px]">
                    <span className="text-[11px] text-muted-foreground">{new Date(h.time).toLocaleTimeString("en-US", { hour: "numeric" })}</span>
                    <span className="text-accent">{weatherIcon(h.condition, "h-5 w-5")}</span>
                    <span className="text-sm font-semibold">{Math.round(h.temp)}°</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
          <div>
            <h3 className="font-medium text-sm mb-3">7-day forecast</h3>
            <ForecastStrip forecast={data.forecast} />
          </div>
        </div>
      )}
    </div>
  );
}
