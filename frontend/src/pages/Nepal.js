import { useQuery } from "@tanstack/react-query";
import { Mountain, PartyPopper, Footprints, Landmark, Bus, Info, ShieldAlert } from "lucide-react";
import { api } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { PageLoader } from "@/components/common/States";

export default function Nepal() {
  const { data: festivals } = useQuery({ queryKey: ["festivals"], queryFn: api.nepalFestivals });
  const { data: treks } = useQuery({ queryKey: ["treks"], queryFn: api.nepalTreks });
  const { data: unesco } = useQuery({ queryKey: ["unesco"], queryFn: api.nepalUnesco });
  const { data: transport } = useQuery({ queryKey: ["transport"], queryFn: api.nepalTransport });
  const { data: info } = useQuery({ queryKey: ["nepalInfo"], queryFn: api.nepalInfo });

  return (
    <div className="max-w-[1000px] px-4 sm:px-6 lg:px-8 py-6">
      <div className="relative overflow-hidden rounded-2xl mb-5">
        <img src="https://images.pexels.com/photos/25490313/pexels-photo-25490313.jpeg?auto=compress&cs=tinysrgb&w=1400" alt="Nepal" className="h-40 w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-black/10" />
        <div className="absolute bottom-0 p-5 text-white">
          <h1 className="font-display text-2xl font-semibold flex items-center gap-2"><Mountain className="h-6 w-6" /> Nepal Intelligence</h1>
          <p className="text-sm text-white/90">Festivals, treks, heritage, transport & essentials — all in one place.</p>
        </div>
      </div>

      <Tabs defaultValue="festivals">
        <TabsList className="flex-wrap h-auto">
          <TabsTrigger value="festivals" data-testid="nepal-tab-festivals" className="gap-1.5"><PartyPopper className="h-4 w-4" /> Festivals</TabsTrigger>
          <TabsTrigger value="treks" className="gap-1.5"><Footprints className="h-4 w-4" /> Treks</TabsTrigger>
          <TabsTrigger value="heritage" className="gap-1.5"><Landmark className="h-4 w-4" /> Heritage</TabsTrigger>
          <TabsTrigger value="transport" className="gap-1.5"><Bus className="h-4 w-4" /> Transport</TabsTrigger>
          <TabsTrigger value="essentials" className="gap-1.5"><Info className="h-4 w-4" /> Essentials</TabsTrigger>
        </TabsList>

        <TabsContent value="festivals" className="pt-4">
          {!festivals ? <PageLoader /> : (
            <div className="grid gap-3 sm:grid-cols-2">
              {festivals.map((f) => (
                <Card key={f.name} className="p-4">
                  <div className="flex items-center justify-between"><h3 className="font-display font-semibold">{f.name}</h3><Badge variant="secondary">{f.period}</Badge></div>
                  <p className="mt-1.5 text-sm text-muted-foreground">{f.about}</p>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="treks" className="pt-4">
          {!treks ? <PageLoader /> : (
            <div className="grid gap-3 sm:grid-cols-2">
              {treks.map((t) => (
                <Card key={t.name} className="p-4">
                  <h3 className="font-display font-semibold">{t.name}</h3>
                  <div className="mt-2 flex flex-wrap gap-1.5 text-[11px]">
                    <Badge variant="outline">{t.days} days</Badge>
                    <Badge variant="outline">{t.difficulty}</Badge>
                    <Badge variant="outline">Max {t.max_alt}</Badge>
                  </div>
                  <p className="mt-2 text-xs text-muted-foreground">Permits: {t.permits}</p>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="heritage" className="pt-4">
          <Card className="p-4">
            <h3 className="font-display font-semibold mb-2">UNESCO World Heritage in Nepal</h3>
            <div className="flex flex-wrap gap-2">
              {(unesco || []).map((u) => <Badge key={u} variant="secondary" className="px-3 py-1.5">{u}</Badge>)}
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="transport" className="pt-4">
          <div className="space-y-3">
            {(transport || []).map((t, i) => (
              <Card key={i} className="p-4">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <h3 className="font-medium">{t.route}</h3>
                  <div className="flex gap-1.5"><Badge variant="outline">{t.mode}</Badge>{t.duration !== "-" && <Badge variant="secondary">{t.duration}</Badge>}{t.fare_npr && <Badge variant="secondary">Rs {t.fare_npr}</Badge>}</div>
                </div>
                <p className="mt-1.5 text-sm text-muted-foreground">{t.notes}</p>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="essentials" className="pt-4 space-y-4">
          {info && (
            <>
              <Accordion type="single" collapsible className="rounded-xl border border-border bg-card divide-y">
                {Object.entries(info.practical).map(([k, v]) => (
                  <AccordionItem key={k} value={k} className="border-0 px-4">
                    <AccordionTrigger className="text-sm hover:no-underline">{v.title}</AccordionTrigger>
                    <AccordionContent className="text-sm text-muted-foreground">{v.info}</AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
              <Card className="p-4 border-destructive/30 bg-destructive/5">
                <h3 className="flex items-center gap-1.5 font-medium text-destructive"><ShieldAlert className="h-4 w-4" /> Hazard awareness</h3>
                <div className="mt-2 space-y-2">
                  {Object.entries(info.safety).map(([k, steps]) => (
                    <div key={k}>
                      <p className="text-sm font-medium capitalize">{k}</p>
                      <p className="text-xs text-muted-foreground">{steps[0]}</p>
                    </div>
                  ))}
                </div>
              </Card>
            </>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
