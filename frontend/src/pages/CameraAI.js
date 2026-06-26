import { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Camera, Upload, Sparkles, MapPin, Lightbulb, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/common/States";

export default function CameraAI() {
  const [preview, setPreview] = useState(null);
  const [b64, setB64] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileRef = useRef(null);

  const onFile = (file) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => { setPreview(reader.result); setB64(reader.result); setResult(null); };
    reader.readAsDataURL(file);
  };

  const analyze = async () => {
    if (!b64) return;
    setLoading(true);
    try {
      const res = await api.analyzeImage(b64, "Identify this and tell me about it in the context of Nepal.");
      setResult(res);
    } catch { toast.error("Could not analyze image. Try another photo."); }
    setLoading(false);
  };

  const reset = () => { setPreview(null); setB64(null); setResult(null); };
  const confColor = { high: "text-[hsl(var(--route))]", medium: "text-accent", low: "text-muted-foreground" };

  return (
    <div className="max-w-[900px] px-4 sm:px-6 lg:px-8 py-6">
      <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
        <Camera className="h-6 w-6 text-accent" /> Camera AI
      </h1>
      <p className="mt-1 text-sm text-muted-foreground">Snap or upload a temple, dish, signboard or scenery — CityBrain identifies it with local context.</p>

      <div className="mt-5 grid gap-5 lg:grid-cols-2">
        <div>
          <input ref={fileRef} type="file" accept="image/*" capture="environment" className="hidden"
            data-testid="camera-file" onChange={(e) => onFile(e.target.files?.[0])} />
          {!preview ? (
            <button onClick={() => fileRef.current?.click()} data-testid="camera-upload"
              className="flex aspect-[4/3] w-full flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed border-border bg-card hover:border-accent/50 hover:bg-muted/40 transition-colors">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-accent/15 text-accent"><Upload className="h-7 w-7" /></div>
              <p className="font-medium">Tap to upload or take a photo</p>
              <p className="text-xs text-muted-foreground">JPG / PNG · landmarks, food, signboards</p>
            </button>
          ) : (
            <div className="space-y-3">
              <div className="relative overflow-hidden rounded-2xl">
                <img src={preview} alt="preview" className="aspect-[4/3] w-full object-cover" />
              </div>
              <div className="flex gap-2">
                <Button onClick={analyze} disabled={loading} data-testid="camera-analyze" className="flex-1 gap-2">
                  {loading ? <Spinner /> : <Sparkles className="h-4 w-4" />} {loading ? "Analyzing…" : "Analyze with AI"}
                </Button>
                <Button variant="outline" onClick={reset} className="gap-1.5"><RefreshCw className="h-4 w-4" /> New</Button>
              </div>
            </div>
          )}
        </div>

        <div>
          {!result && !loading && (
            <Card className="flex h-full min-h-[240px] flex-col items-center justify-center gap-2 p-6 text-center text-muted-foreground">
              <Sparkles className="h-8 w-8 text-accent/60" />
              <p className="text-sm">Your AI identification will appear here.</p>
            </Card>
          )}
          {loading && (
            <Card className="flex h-full min-h-[240px] flex-col items-center justify-center gap-3 p-6 text-muted-foreground">
              <Spinner className="h-7 w-7" /> <p className="text-sm">CityBrain Vision is looking…</p>
            </Card>
          )}
          {result && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
              <Card data-testid="camera-result" className="p-4 border-l-4 border-l-accent">
                <div className="flex items-start justify-between gap-2">
                  <h3 className="font-display font-semibold text-lg">{result.identification}</h3>
                  {result.confidence && <Badge variant="secondary" className={`shrink-0 capitalize ${confColor[result.confidence] || ""}`}>{result.confidence}</Badge>}
                </div>
                <div className="mt-1 flex flex-wrap gap-1.5">
                  {result.category && <Badge variant="outline" className="text-[11px] capitalize">{result.category}</Badge>}
                  {result.is_nepal && <Badge variant="outline" className="gap-1 text-[11px]"><MapPin className="h-3 w-3 text-accent" /> Nepal</Badge>}
                </div>
                {result.facts?.length > 0 && (
                  <ul className="mt-3 space-y-1.5 text-sm text-muted-foreground">
                    {result.facts.map((f, i) => <li key={i} className="flex gap-2"><span className="text-accent">•</span>{f}</li>)}
                  </ul>
                )}
                {result.traveler_tip && (
                  <div className="mt-3 flex items-start gap-2 rounded-lg bg-secondary p-2.5 text-sm">
                    <Lightbulb className="h-4 w-4 shrink-0 text-accent mt-0.5" /><span>{result.traveler_tip}</span>
                  </div>
                )}
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
