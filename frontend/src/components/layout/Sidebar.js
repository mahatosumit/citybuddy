import { NavLink, Link } from "react-router-dom";
import { Mountain } from "lucide-react";
import { cn } from "@/lib/utils";
import { PRIMARY_NAV, SECONDARY_NAV } from "@/lib/ui";

function NavItem({ item }) {
  const Icon = item.icon;
  return (
    <NavLink
      to={item.to}
      end={item.to === "/"}
      data-testid={item.testid}
      className={({ isActive }) =>
        cn(
          "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
          "focus-ring",
          isActive
            ? "bg-secondary text-secondary-foreground"
            : "text-muted-foreground hover:bg-muted hover:text-foreground",
          item.danger && "hover:text-destructive"
        )
      }
    >
      {({ isActive }) => (
        <>
          <span
            className={cn(
              "absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 rounded-r-full bg-accent transition-opacity",
              isActive ? "opacity-100" : "opacity-0"
            )}
          />
          <Icon className={cn("h-[18px] w-[18px] shrink-0", item.danger && "text-destructive")} />
          <span>{item.label}</span>
        </>
      )}
    </NavLink>
  );
}

export function Sidebar() {
  return (
    <aside
      data-testid="app-sidebar"
      className="hidden lg:flex fixed inset-y-0 left-0 z-40 w-[280px] xl:w-[300px] flex-col border-r border-border bg-card"
    >
      <Link to="/" className="flex items-center gap-2.5 px-5 h-16 border-b border-border focus-ring">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
          <Mountain className="h-5 w-5" />
        </div>
        <div className="leading-tight">
          <div className="font-display font-semibold text-[15px]">CityBuddy</div>
          <div className="text-[11px] text-muted-foreground">Your AI Companion for Nepal</div>
        </div>
      </Link>

      <nav className="flex-1 overflow-y-auto no-scrollbar px-3 py-4 space-y-1">
        {PRIMARY_NAV.map((it) => <NavItem key={it.to} item={it} />)}
        <div className="px-3 pt-5 pb-2 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
          More
        </div>
        {SECONDARY_NAV.map((it) => <NavItem key={it.to} item={it} />)}
      </nav>

      <div className="border-t border-border p-3">
        <NavLink
          to="/profile"
          data-testid="nav-profile"
          className={({ isActive }) =>
            cn("flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors focus-ring",
              isActive ? "bg-secondary text-secondary-foreground" : "text-muted-foreground hover:bg-muted hover:text-foreground")
          }
        >
          <div className="flex h-7 w-7 items-center justify-center rounded-full bg-accent text-accent-foreground text-xs font-semibold">
            DT
          </div>
          <span>Demo Traveler</span>
        </NavLink>
      </div>
    </aside>
  );
}
