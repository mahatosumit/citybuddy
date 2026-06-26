import { NavLink, Link } from "react-router-dom";
import { Mountain, LogOut, LogIn } from "lucide-react";
import { cn } from "@/lib/utils";
import { PRIMARY_NAV, SECONDARY_NAV, ROLE_NAV, initials } from "@/lib/ui";
import { useT } from "@/lib/i18n";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";

function NavItem({ item, t }) {
  const Icon = item.icon;
  return (
    <NavLink to={item.to} end={item.to === "/"} data-testid={item.testid}
      className={({ isActive }) => cn(
        "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors focus-ring",
        isActive ? "bg-secondary text-secondary-foreground" : "text-muted-foreground hover:bg-muted hover:text-foreground",
        item.danger && "hover:text-destructive")}>
      {({ isActive }) => (
        <>
          <span className={cn("absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 rounded-r-full bg-accent transition-opacity", isActive ? "opacity-100" : "opacity-0")} />
          <Icon className={cn("h-[18px] w-[18px] shrink-0", item.danger && "text-destructive")} />
          <span>{t(item.labelKey)}</span>
        </>
      )}
    </NavLink>
  );
}

export function Sidebar() {
  const t = useT();
  const { user, logout } = useAuth();
  const roleItem = user && ROLE_NAV[user.role];

  return (
    <aside data-testid="app-sidebar" className="hidden lg:flex fixed inset-y-0 left-0 z-40 w-[280px] xl:w-[300px] flex-col border-r border-border bg-card">
      <Link to="/" className="flex items-center gap-2.5 px-5 h-16 border-b border-border focus-ring">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground"><Mountain className="h-5 w-5" /></div>
        <div className="leading-tight">
          <div className="font-display font-semibold text-[15px]">CityBuddy</div>
          <div className="text-[11px] text-muted-foreground">{t("brand.tagline")}</div>
        </div>
      </Link>

      <nav className="flex-1 overflow-y-auto no-scrollbar px-3 py-4 space-y-1">
        {PRIMARY_NAV.map((it) => <NavItem key={it.to} item={it} t={t} />)}
        <div className="px-3 pt-5 pb-2 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">{t("nav.more")}</div>
        {SECONDARY_NAV.map((it) => <NavItem key={it.to} item={it} t={t} />)}
        {roleItem && <NavItem item={roleItem} t={t} />}
      </nav>

      <div className="border-t border-border p-3">
        {user ? (
          <div className="flex items-center gap-2">
            <NavLink to="/profile" data-testid="nav-profile" className="flex flex-1 items-center gap-3 rounded-xl px-2 py-2 text-sm font-medium hover:bg-muted transition-colors min-w-0">
              {user.picture ? <img src={user.picture} alt="" className="h-8 w-8 rounded-full object-cover" /> :
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-accent text-accent-foreground text-xs font-semibold">{initials(user.name)}</div>}
              <div className="min-w-0">
                <div className="truncate text-[13px] font-medium">{user.name}</div>
                <div className="truncate text-[11px] text-muted-foreground capitalize">{user.role}</div>
              </div>
            </NavLink>
            <Button variant="ghost" size="icon" onClick={logout} data-testid="logout-btn" aria-label="Log out"><LogOut className="h-4 w-4" /></Button>
          </div>
        ) : (
          <Link to="/login"><Button className="w-full gap-2" data-testid="sidebar-signin"><LogIn className="h-4 w-4" /> {t("common.signin")}</Button></Link>
        )}
      </div>
    </aside>
  );
}
