import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Wallet, Plus, Trash2, X } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { EmptyState, PageLoader } from "@/components/common/States";
import { formatNPR } from "@/lib/ui";

const COLORS = ["#1E2A5A", "#0EA5A4", "#F59E0B", "#DC2626", "#475569", "#7C3AED"];
const CATS = ["Accommodation", "Food", "Transport", "Activities", "Shopping", "Misc"];

function BudgetCard({ b, onDelete }) {
  const spent = (b.entries || []).reduce((s, e) => s + Number(e.amount_npr || 0), 0);
  const pct = b.total_budget_npr ? Math.min(100, Math.round((spent / b.total_budget_npr) * 100)) : 0;
  const byCat = {};
  (b.entries || []).forEach((e) => { byCat[e.category] = (byCat[e.category] || 0) + Number(e.amount_npr || 0); });
  const pieData = Object.entries(byCat).map(([name, value]) => ({ name, value }));
  const over = spent > b.total_budget_npr;

  return (
    <Card className="p-4" data-testid="budget-summary">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-display font-semibold">{b.title}</h3>
          {b.city && <Badge variant="secondary" className="mt-1 text-[11px]">{b.city}</Badge>}
        </div>
        <button onClick={() => onDelete(b.id)} className="rounded-lg p-1.5 text-muted-foreground hover:text-destructive"><Trash2 className="h-4 w-4" /></button>
      </div>
      <div className="mt-3 grid grid-cols-[120px_1fr] gap-3 items-center">
        <div className="h-[120px]">
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={32} outerRadius={56} paddingAngle={2}>
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip formatter={(v) => formatNPR(v)} />
              </PieChart>
            </ResponsiveContainer>
          ) : <div className="flex h-full items-center justify-center text-xs text-muted-foreground">No entries</div>}
        </div>
        <div>
          <div className="flex items-baseline justify-between">
            <span className="text-sm text-muted-foreground">Spent</span>
            <span className={`font-semibold ${over ? "text-destructive" : ""}`}>{formatNPR(spent)}</span>
          </div>
          <Progress value={pct} className="my-2" />
          <div className="flex items-baseline justify-between text-xs text-muted-foreground">
            <span>{pct}% of budget</span>
            <span>{formatNPR(b.total_budget_npr)}</span>
          </div>
          <div className="mt-2 space-y-1">
            {Object.entries(byCat).map(([c, v], i) => (
              <div key={c} className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full" style={{ background: COLORS[i % COLORS.length] }} />{c}</span>
                <span className="font-medium">{formatNPR(v)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}

export default function Budget() {
  const qc = useQueryClient();
  const { data: budgets, isLoading } = useQuery({ queryKey: ["budgets"], queryFn: api.getBudgets });
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [city, setCity] = useState("");
  const [total, setTotal] = useState("");
  const [entries, setEntries] = useState([{ category: "Accommodation", label: "", amount_npr: "" }]);

  const create = useMutation({
    mutationFn: () => api.createBudget({
      title, city, total_budget_npr: Number(total) || 0,
      entries: entries.filter((e) => e.amount_npr).map((e) => ({ ...e, amount_npr: Number(e.amount_npr) })),
    }),
    onSuccess: () => { toast.success("Budget created"); setOpen(false); reset(); qc.invalidateQueries({ queryKey: ["budgets"] }); },
    onError: () => toast.error("Could not create budget"),
  });
  const del = useMutation({
    mutationFn: (id) => api.deleteBudget(id),
    onSuccess: () => { toast("Budget deleted"); qc.invalidateQueries({ queryKey: ["budgets"] }); },
  });

  const reset = () => { setTitle(""); setCity(""); setTotal(""); setEntries([{ category: "Accommodation", label: "", amount_npr: "" }]); };
  const updateEntry = (i, k, v) => setEntries((e) => e.map((row, idx) => idx === i ? { ...row, [k]: v } : row));

  return (
    <div className="max-w-[1000px] px-4 sm:px-6 lg:px-8 py-6">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
          <Wallet className="h-6 w-6 text-accent" /> Budget Planner
        </h1>
        <Button data-testid="budget-new" onClick={() => setOpen(!open)} className="gap-1.5">
          {open ? <X className="h-4 w-4" /> : <Plus className="h-4 w-4" />} {open ? "Close" : "New budget"}
        </Button>
      </div>

      {open && (
        <Card className="mt-4 p-4 sm:p-5 space-y-4">
          <div className="grid gap-3 sm:grid-cols-3">
            <Input placeholder="Trip title" value={title} onChange={(e) => setTitle(e.target.value)} data-testid="budget-title" />
            <Input placeholder="City (optional)" value={city} onChange={(e) => setCity(e.target.value)} />
            <Input type="number" placeholder="Total budget (NPR)" value={total} onChange={(e) => setTotal(e.target.value)} data-testid="budget-total" />
          </div>
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground">Expenses</p>
            {entries.map((e, i) => (
              <div key={i} className="grid grid-cols-[1fr_1fr_110px_auto] gap-2">
                <select value={e.category} onChange={(ev) => updateEntry(i, "category", ev.target.value)}
                  className="rounded-lg border border-input bg-background px-2 text-sm h-9">
                  {CATS.map((c) => <option key={c}>{c}</option>)}
                </select>
                <Input placeholder="Label" value={e.label} onChange={(ev) => updateEntry(i, "label", ev.target.value)} className="h-9" />
                <Input type="number" placeholder="NPR" value={e.amount_npr} onChange={(ev) => updateEntry(i, "amount_npr", ev.target.value)} className="h-9" />
                <button onClick={() => setEntries((arr) => arr.filter((_, idx) => idx !== i))} className="text-muted-foreground hover:text-destructive px-1"><X className="h-4 w-4" /></button>
              </div>
            ))}
            <Button variant="outline" size="sm" onClick={() => setEntries((e) => [...e, { category: "Food", label: "", amount_npr: "" }])} className="gap-1.5">
              <Plus className="h-3.5 w-3.5" /> Add expense
            </Button>
          </div>
          <Button data-testid="budget-create" onClick={() => create.mutate()} disabled={!title || create.isPending}>Create budget</Button>
        </Card>
      )}

      <div className="mt-5">
        {isLoading ? <PageLoader /> : (budgets || []).length === 0 ? (
          <EmptyState icon={Wallet} title="No budgets yet" description="Create a budget to track your trip expenses by category." testid="budget-empty" />
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {budgets.map((b) => <BudgetCard key={b.id} b={b} onDelete={del.mutate} />)}
          </div>
        )}
      </div>
    </div>
  );
}
