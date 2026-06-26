import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { Mountain, Mail, Lock, User as UserIcon, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "@/lib/auth";
import { useT } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";

export default function Login() {
  const t = useT();
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register, loginWithGoogle } = useAuth();
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const from = location.state?.from || "/chat";

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      if (mode === "login") { await login(email, password); toast.success("Welcome back!"); }
      else { await register(email, password, name); toast.success("Account created!"); }
      navigate(from, { replace: true });
    } catch (err) {
      const msg = err?.response?.data?.detail || "Authentication failed";
      toast.error(typeof msg === "string" ? msg : "Authentication failed");
    } finally { setBusy(false); }
  };

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-background">
      {/* Brand panel */}
      <div className="relative hidden lg:block">
        <img src="https://images.pexels.com/photos/25490311/pexels-photo-25490311.jpeg?auto=compress&cs=tinysrgb&w=1400" alt="Nepal" className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/40 to-black/30" />
        <div className="absolute bottom-0 p-10 text-white">
          <div className="flex items-center gap-2.5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/15 backdrop-blur"><Mountain className="h-5 w-5" /></div>
            <span className="font-display text-xl font-semibold">CityBuddy</span>
          </div>
          <h2 className="mt-5 font-display text-3xl font-semibold max-w-md text-balance">{t("home.heroTitle")}</h2>
          <p className="mt-2 text-white/80 max-w-md">{t("home.heroSub")}</p>
        </div>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center p-6">
        <Card className="w-full max-w-md p-7">
          <Link to="/" className="flex items-center gap-2 lg:hidden mb-5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground"><Mountain className="h-5 w-5" /></div>
            <span className="font-display font-semibold">CityBuddy</span>
          </Link>
          <h1 className="font-display text-2xl font-semibold">{mode === "login" ? t("auth.welcome") : t("auth.create")}</h1>
          <p className="mt-1 text-sm text-muted-foreground">{t("brand.tagline")}</p>

          <Button variant="outline" className="mt-5 w-full gap-2" onClick={loginWithGoogle} data-testid="google-login">
            <svg className="h-4 w-4" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.84 14.1a6.6 6.6 0 0 1 0-4.2V7.06H2.18a11 11 0 0 0 0 9.88l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38z"/></svg>
            {t("auth.google")}
          </Button>

          <div className="my-5 flex items-center gap-3 text-xs text-muted-foreground">
            <div className="h-px flex-1 bg-border" /> {t("auth.or")} <div className="h-px flex-1 bg-border" />
          </div>

          <form onSubmit={submit} className="space-y-3">
            {mode === "signup" && (
              <div className="relative">
                <UserIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input value={name} onChange={(e) => setName(e.target.value)} placeholder={t("auth.name")} className="pl-9" data-testid="auth-name" />
              </div>
            )}
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder={t("auth.email")} className="pl-9" data-testid="auth-email" />
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder={t("auth.password")} className="pl-9" data-testid="auth-password" />
            </div>
            <Button type="submit" className="w-full" disabled={busy} data-testid="auth-submit">
              {busy && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
              {mode === "login" ? t("auth.loginCta") : t("auth.signupCta")}
            </Button>
          </form>

          <p className="mt-4 text-center text-sm text-muted-foreground">
            {mode === "login" ? t("auth.noAccount") : t("auth.haveAccount")}{" "}
            <button onClick={() => setMode(mode === "login" ? "signup" : "login")} className="font-medium text-accent hover:underline" data-testid="auth-toggle">
              {mode === "login" ? t("auth.signupCta") : t("auth.loginCta")}
            </button>
          </p>
        </Card>
      </div>
    </div>
  );
}
