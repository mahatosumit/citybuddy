import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { User, Save, Globe } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useLanguage } from "@/lib/i18n";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PageLoader } from "@/components/common/States";

const CITIES = ["Kathmandu", "Pokhara", "Bhaktapur", "Lalitpur", "Chitwan", "Lumbini", "Mustang", "Ilam", "Dharan"];
const INTERESTS = ["culture", "nature", "food", "adventure", "spiritual", "shopping", "photography", "trekking"];

export default function Profile() {
  const qc = useQueryClient();
  const { lang, setLang } = useLanguage();
  const { data: profile, isLoading } = useQuery({ queryKey: ["profile"], queryFn: api.getProfile });
  const [name, setName] = useState("");
  const [homeCity, setHomeCity] = useState("Kathmandu");
  const [interests, setInterests] = useState([]);

  useEffect(() => {
    if (profile) {
      setName(profile.name || "");
      setHomeCity(profile.home_city || "Kathmandu");
      setInterests(profile.preferences?.interests || []);
    }
  }, [profile]);

  const save = useMutation({
    mutationFn: () => api.updateProfile({ name, home_city: homeCity, language: lang, preferences: { ...(profile?.preferences || {}), interests } }),
    onSuccess: () => { toast.success("Profile saved"); qc.invalidateQueries({ queryKey: ["profile"] }); },
    onError: () => toast.error("Could not save profile"),
  });

  const toggle = (i) => setInterests((p) => p.includes(i) ? p.filter((x) => x !== i) : [...p, i]);
  if (isLoading) return <PageLoader />;

  return (
    <div className="max-w-[700px] px-4 sm:px-6 lg:px-8 py-6">
      <h1 className="font-display text-2xl font-semibold flex items-center gap-2"><User className="h-6 w-6 text-accent" /> Profile</h1>
      <p className="mt-1 text-sm text-muted-foreground">CityBrain personalizes recommendations using your preferences.</p>

      <Card className="mt-5 p-5 space-y-5">
        <div className="flex items-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-accent text-accent-foreground text-lg font-semibold">
            {(name || "DT").split(" ").map((w) => w[0]).slice(0, 2).join("").toUpperCase()}
          </div>
          <div className="flex-1">
            <label className="text-xs font-medium text-muted-foreground">Name</label>
            <Input value={name} onChange={(e) => setName(e.target.value)} data-testid="profile-name" className="mt-1" />
          </div>
        </div>

        <div>
          <label className="text-xs font-medium text-muted-foreground">Home / base city</label>
          <Select value={homeCity} onValueChange={setHomeCity}>
            <SelectTrigger className="mt-1" data-testid="profile-city"><SelectValue /></SelectTrigger>
            <SelectContent>{CITIES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
          </Select>
        </div>

        <div>
          <label className="text-xs font-medium text-muted-foreground">Interests</label>
          <div className="mt-1.5 flex flex-wrap gap-2">
            {INTERESTS.map((i) => (
              <button key={i} onClick={() => toggle(i)}
                className={`rounded-full border px-3 py-1.5 text-xs font-medium capitalize transition-colors ${interests.includes(i) ? "border-accent bg-accent/15 text-accent" : "border-border bg-card text-muted-foreground hover:bg-muted"}`}>
                {i}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5"><Globe className="h-3.5 w-3.5" /> AI response language</label>
          <div className="mt-1.5 flex gap-2">
            <Button variant={lang === "en" ? "default" : "outline"} size="sm" onClick={() => setLang("en")}>English</Button>
            <Button variant={lang === "ne" ? "default" : "outline"} size="sm" onClick={() => setLang("ne")}>नेपाली</Button>
          </div>
        </div>

        <Button onClick={() => save.mutate()} disabled={save.isPending} data-testid="profile-save" className="gap-1.5">
          <Save className="h-4 w-4" /> Save profile
        </Button>
      </Card>
    </div>
  );
}
