import { Cloud, CloudRain, CloudSnow, Sun, CloudLightning, CloudFog, Wind, Droplets } from "lucide-react";

export function weatherIcon(condition = "", cls = "h-6 w-6") {
  const c = condition.toLowerCase();
  if (c.includes("thunder")) return <CloudLightning className={cls} />;
  if (c.includes("snow")) return <CloudSnow className={cls} />;
  if (c.includes("rain") || c.includes("drizzle") || c.includes("shower")) return <CloudRain className={cls} />;
  if (c.includes("fog")) return <CloudFog className={cls} />;
  if (c.includes("clear")) return <Sun className={cls} />;
  return <Cloud className={cls} />;
}

export function CurrentWeather({ data, city }) {
  if (!data) return null;
  const c = data.current;
  return (
    <div data-testid="weather-now" className="rounded-2xl border border-border bg-card p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">{city}</p>
          <div className="mt-1 flex items-end gap-1">
            <span className="font-display text-5xl font-semibold">{Math.round(c.temp_c)}°</span>
            <span className="mb-2 text-sm text-muted-foreground">C</span>
          </div>
          <p className="mt-1 text-sm font-medium">{c.condition}</p>
        </div>
        <div className="text-accent">{weatherIcon(c.condition, "h-16 w-16")}</div>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-2 text-center">
        <div className="rounded-xl bg-muted/60 py-2">
          <p className="text-[11px] text-muted-foreground">Feels like</p>
          <p className="font-semibold">{Math.round(c.feels_like_c)}°</p>
        </div>
        <div className="rounded-xl bg-muted/60 py-2">
          <p className="flex items-center justify-center gap-1 text-[11px] text-muted-foreground"><Droplets className="h-3 w-3" />Humidity</p>
          <p className="font-semibold">{c.humidity}%</p>
        </div>
        <div className="rounded-xl bg-muted/60 py-2">
          <p className="flex items-center justify-center gap-1 text-[11px] text-muted-foreground"><Wind className="h-3 w-3" />Wind</p>
          <p className="font-semibold">{Math.round(c.wind_kmh)} km/h</p>
        </div>
      </div>
    </div>
  );
}

export function ForecastStrip({ forecast = [] }) {
  return (
    <div data-testid="weather-forecast" className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
      {forecast.map((d) => (
        <div key={d.date} className="rounded-xl border border-border bg-card p-3">
          <p className="text-xs font-medium text-muted-foreground">
            {new Date(d.date).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" })}
          </p>
          <div className="my-2 text-accent">{weatherIcon(d.condition, "h-7 w-7")}</div>
          <p className="text-xs text-muted-foreground line-clamp-1">{d.condition}</p>
          <div className="mt-1.5 flex items-center justify-between text-sm">
            <span className="font-semibold">{Math.round(d.max)}°</span>
            <span className="text-muted-foreground">{Math.round(d.min)}°</span>
          </div>
          {d.precip_prob != null && (
            <p className="mt-1 flex items-center gap-1 text-[11px] text-[hsl(var(--route))]">
              <Droplets className="h-3 w-3" /> {d.precip_prob}%
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
