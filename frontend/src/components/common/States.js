import { Loader2, Inbox, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Spinner({ className = "h-5 w-5" }) {
  return <Loader2 className={`animate-spin ${className}`} />;
}

export function PageLoader({ label = "Loading…" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-24 text-muted-foreground">
      <Loader2 className="h-7 w-7 animate-spin text-accent" />
      <p className="text-sm">{label}</p>
    </div>
  );
}

export function EmptyState({ icon: Icon = Inbox, title, description, action, testid }) {
  return (
    <div data-testid={testid} className="flex flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-border bg-card/50 py-16 px-6 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-muted text-muted-foreground">
        <Icon className="h-6 w-6" />
      </div>
      <div>
        <h3 className="font-display font-semibold text-base">{title}</h3>
        {description && <p className="mt-1 text-sm text-muted-foreground max-w-sm">{description}</p>}
      </div>
      {action}
    </div>
  );
}

export function ErrorState({ onRetry, message = "Something went wrong." }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-destructive/10 text-destructive">
        <AlertTriangle className="h-6 w-6" />
      </div>
      <p className="text-sm text-muted-foreground">{message}</p>
      {onRetry && <Button variant="outline" size="sm" onClick={onRetry}>Try again</Button>}
    </div>
  );
}
