import { useState, useRef, useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Sparkles, ShieldAlert, Globe, Cpu, Plus, History, Trash2, MessageSquare } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useLanguage } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { DecisionCard } from "@/components/DecisionCard";

const SUGGESTIONS = [
  "Plan a 2-day budget trip in Pokhara under NPR 5000",
  "What should I do in Kathmandu today given the weather?",
  "Best momo spots in Thamel",
  "Is it safe to drive to Mustang in monsoon?",
  "Explain Nepali temple etiquette",
];

const CONF = { high: { v: 100, t: "High" }, medium: { v: 66, t: "Medium" }, low: { v: 33, t: "Low" } };

function AgentChips({ agents = [] }) {
  if (!agents.length) return null;
  return (
    <div className="mt-3 flex flex-wrap gap-1.5">
      {agents.map((a) => (
        <Badge key={a} data-testid="agent-chip" variant="secondary" className="gap-1 text-[11px]">
          <Cpu className="h-3 w-3 text-[hsl(var(--route))]" /> {a.replace("Agent", "")}
        </Badge>
      ))}
    </div>
  );
}

function AssistantMessage({ data }) {
  const conf = CONF[data.confidence] || CONF.medium;
  return (
    <div className="space-y-3">
      <Card className="border-l-4 border-l-[hsl(var(--route))] bg-card p-4">
        <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{data.summary}</p>
        <AgentChips agents={data.agents_used} />
      </Card>

      {data.recommendations?.length > 0 && (
        <div className="space-y-2">
          {data.recommendations.map((r, i) => <DecisionCard key={i} rec={r} index={i} />)}
        </div>
      )}

      {data.safety_notes?.length > 0 && (
        <Card className="border-destructive/30 bg-destructive/5 p-3.5">
          <div className="flex items-center gap-2 text-destructive font-medium text-sm">
            <ShieldAlert className="h-4 w-4" /> Safety notes
          </div>
          <ul className="mt-2 space-y-1.5 text-[13px] text-muted-foreground">
            {data.safety_notes.map((s, i) => <li key={i} className="flex gap-2"><span className="text-destructive">•</span>{s}</li>)}
          </ul>
        </Card>
      )}

      {(data.reasoning || data.nepal_context) && (
        <Accordion type="single" collapsible className="rounded-xl border border-border bg-card px-3">
          <AccordionItem value="why" className="border-0" data-testid="why-this-accordion">
            <AccordionTrigger className="text-sm hover:no-underline py-3">
              <span className="flex items-center gap-2"><Sparkles className="h-4 w-4 text-accent" /> Why this & how I decided</span>
            </AccordionTrigger>
            <AccordionContent className="space-y-3 pb-4">
              {data.reasoning && <p className="text-[13px] leading-relaxed text-muted-foreground">{data.reasoning}</p>}
              {data.nepal_context && (
                <div className="flex items-start gap-2 rounded-lg bg-secondary p-2.5 text-[13px]">
                  <Globe className="h-4 w-4 shrink-0 text-[hsl(var(--route))] mt-0.5" />
                  <span>{data.nepal_context}</span>
                </div>
              )}
              <div data-testid="confidence-meter" className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">Confidence</span>
                <div className="h-1.5 flex-1 rounded-full bg-muted overflow-hidden">
                  <div className="h-full rounded-full bg-[hsl(var(--route))]" style={{ width: `${conf.v}%` }} />
                </div>
                <span className="text-xs font-medium">{conf.t}</span>
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      )}
    </div>
  );
}

function Thinking() {
  const agents = ["Routing", "Weather", "Places", "Budget", "Local Knowledge"];
  return (
    <Card className="border-l-4 border-l-[hsl(var(--route))] p-4">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span className="flex gap-1">
          <span className="h-2 w-2 rounded-full bg-[hsl(var(--route))] animate-bounce" style={{ animationDelay: "0ms" }} />
          <span className="h-2 w-2 rounded-full bg-[hsl(var(--route))] animate-bounce" style={{ animationDelay: "150ms" }} />
          <span className="h-2 w-2 rounded-full bg-[hsl(var(--route))] animate-bounce" style={{ animationDelay: "300ms" }} />
        </span>
        CityBrain is reasoning across agents…
      </div>
      <div className="mt-3 flex flex-wrap gap-1.5">
        {agents.map((a, i) => (
          <motion.div key={a} initial={{ opacity: 0.3 }} animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}>
            <Badge variant="secondary" className="gap-1 text-[11px]"><Cpu className="h-3 w-3" /> {a}</Badge>
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

export default function Chat() {
  const { lang } = useLanguage();
  const qc = useQueryClient();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [convId, setConvId] = useState(null);
  const endRef = useRef(null);

  const { data: conversations } = useQuery({ queryKey: ["conversations"], queryFn: api.getConversations });

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const mutation = useMutation({
    mutationFn: (msg) => api.chat({ message: msg, conversation_id: convId, context: { language: lang } }),
    onSuccess: (res) => {
      setConvId(res.conversation_id);
      setMessages((m) => [...m, { role: "assistant", data: res.response }]);
      qc.invalidateQueries({ queryKey: ["conversations"] });
    },
    onError: () => {
      toast.error("CityBrain couldn't respond. Please try again.");
      setMessages((m) => [...m, { role: "error" }]);
    },
  });

  const send = (text) => {
    const msg = (text ?? input).trim();
    if (!msg || mutation.isPending) return;
    setMessages((m) => [...m, { role: "user", content: msg }]);
    setInput("");
    mutation.mutate(msg);
  };

  const loadConversation = async (id) => {
    const res = await api.getConversation(id);
    setConvId(id);
    setMessages(res.messages.map((m) => m.role === "assistant"
      ? { role: "assistant", data: m.data }
      : { role: "user", content: m.content }));
  };

  const newChat = () => { setConvId(null); setMessages([]); };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex items-center justify-between border-b border-border px-4 sm:px-6 py-3">
        <div>
          <h1 className="font-display font-semibold text-lg flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-accent" /> CityBrain
          </h1>
          <p className="text-xs text-muted-foreground">Multi-agent AI that reasons over Nepal</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={newChat} data-testid="new-chat-btn" className="gap-1.5">
            <Plus className="h-4 w-4" /> New
          </Button>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" data-testid="history-btn"><History className="h-4 w-4" /></Button>
            </SheetTrigger>
            <SheetContent>
              <SheetHeader><SheetTitle>Chat history</SheetTitle></SheetHeader>
              <div className="mt-4 space-y-1">
                {(conversations || []).length === 0 && <p className="text-sm text-muted-foreground">No conversations yet.</p>}
                {(conversations || []).map((c) => (
                  <div key={c.id} className="flex items-center gap-1">
                    <button onClick={() => loadConversation(c.id)}
                      className="flex-1 truncate rounded-lg px-3 py-2 text-left text-sm hover:bg-muted transition-colors">
                      <MessageSquare className="inline h-3.5 w-3.5 mr-2 text-muted-foreground" />{c.title}
                    </button>
                    <button onClick={async () => { await api.deleteConversation(c.id); qc.invalidateQueries({ queryKey: ["conversations"] }); if (c.id === convId) newChat(); }}
                      className="rounded-lg p-2 text-muted-foreground hover:text-destructive"><Trash2 className="h-3.5 w-3.5" /></button>
                  </div>
                ))}
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-5">
        <div className="mx-auto max-w-3xl space-y-5">
          {messages.length === 0 && (
            <div className="pt-6">
              <div className="rounded-2xl border border-border bg-card p-6 text-center">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-accent/15 text-accent">
                  <Sparkles className="h-6 w-6" />
                </div>
                <h2 className="mt-3 font-display font-semibold text-lg">Namaste! I'm CityBrain 🇳🇵</h2>
                <p className="mt-1 text-sm text-muted-foreground max-w-md mx-auto">
                  Ask me anything about traveling, eating, staying or staying safe in Nepal. I combine
                  weather, places, budget and local knowledge to give real decisions.
                </p>
              </div>
              <div className="mt-4 flex flex-wrap gap-2 justify-center">
                {SUGGESTIONS.map((s) => (
                  <button key={s} data-testid="suggestion-chip" onClick={() => send(s)}
                    className="rounded-full border border-border bg-card px-3.5 py-2 text-[13px] hover:bg-muted hover:border-accent/40 transition-colors">
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          <AnimatePresence>
            {messages.map((m, i) => (
              <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
                {m.role === "user" && (
                  <div className="flex justify-end">
                    <div className="max-w-[85%] rounded-2xl rounded-br-md bg-primary px-4 py-2.5 text-primary-foreground text-[15px]">
                      {m.content}
                    </div>
                  </div>
                )}
                {m.role === "assistant" && <AssistantMessage data={m.data} />}
                {m.role === "error" && (
                  <Card className="border-destructive/30 bg-destructive/5 p-3.5 text-sm text-destructive">
                    CityBrain hit an error. Please try again.
                  </Card>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {mutation.isPending && <Thinking />}
          <div ref={endRef} />
        </div>
      </div>

      <div className="sticky bottom-0 border-t border-border bg-background/95 backdrop-blur p-3 sm:p-4">
        <div className="mx-auto max-w-3xl flex items-end gap-2">
          <Textarea
            data-testid="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            placeholder="Ask CityBrain anything about Nepal…"
            rows={1}
            className="min-h-[48px] max-h-32 resize-none rounded-xl"
          />
          <Button data-testid="chat-send" size="icon" className="h-12 w-12 shrink-0 rounded-xl active:scale-95"
            onClick={() => send()} disabled={mutation.isPending || !input.trim()}>
            <Send className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </div>
  );
}
