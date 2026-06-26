import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { api, setToken } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { PageLoader } from "@/components/common/States";

export default function AuthCallback() {
  const navigate = useNavigate();
  const { applyGoogleUser } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    if (hasProcessed.current) return;
    hasProcessed.current = true;
    const hash = window.location.hash || "";
    const match = hash.match(/session_id=([^&]+)/);
    const sessionId = match ? decodeURIComponent(match[1]) : null;
    (async () => {
      if (!sessionId) { navigate("/login", { replace: true }); return; }
      try {
        const res = await api.googleSession(sessionId);
        applyGoogleUser(res.user, res.token);
        // clear the hash and go to the app
        window.history.replaceState(null, "", window.location.origin + "/");
        navigate("/chat", { replace: true });
      } catch (e) {
        navigate("/login", { replace: true });
      }
    })();
  }, [navigate, applyGoogleUser]);

  return <PageLoader label="Signing you in\u2026" />;
}
