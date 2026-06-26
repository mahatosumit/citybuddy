import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Moon, Sun, Mountain, ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLanguage } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export function TopBar() {
  const { theme, setTheme } = useTheme();
  const { lang, setLang } = useLanguage();
  const [mounted, setMounted] = useState(false);
  const location = useLocation();
  useEffect(() => setMounted(true), []);

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-border bg-background/90 backdrop-blur supports-[backdrop-filter]:bg-background/70 px-4 sm:px-6">
      {/* mobile brand */}
      <Link to="/" className="flex items-center gap-2 lg:hidden focus-ring">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Mountain className="h-4 w-4" />
        </div>
        <span className="font-display font-semibold">CityBuddy</span>
      </Link>

      <div className="ml-auto flex items-center gap-2">
        <Link to="/emergency" className="hidden sm:block">
          <Button
            variant="outline"
            size="sm"
            data-testid="topbar-emergency"
            className={cn("gap-1.5 border-destructive/30 text-destructive hover:bg-destructive/10",
              location.pathname === "/emergency" && "bg-destructive/10")}
          >
            <ShieldAlert className="h-4 w-4" /> SOS
          </Button>
        </Link>

        <div className="flex items-center rounded-lg border border-border bg-card p-0.5">
          <button
            data-testid="language-toggle"
            onClick={() => setLang(lang === "en" ? "ne" : "en")}
            className="px-2.5 py-1 text-xs font-semibold rounded-md hover:bg-muted transition-colors"
            aria-label="Toggle AI response language"
            title={lang === "en" ? "AI replies in English" : "AI जवाफ नेपालीमा"}
          >
            {lang === "en" ? "EN" : "ने"}
          </button>
        </div>

        <Button
          variant="ghost"
          size="icon"
          data-testid="theme-toggle"
          aria-label="Toggle theme"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {mounted && theme === "dark" ? <Sun className="h-[18px] w-[18px]" /> : <Moon className="h-[18px] w-[18px]" />}
        </Button>
      </div>
    </header>
  );
}
