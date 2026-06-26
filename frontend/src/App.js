import "@/App.css";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { ThemeProvider } from "next-themes";
import { Toaster } from "@/components/ui/sonner";
import { LanguageProvider } from "@/lib/i18n";
import { AuthProvider, ProtectedRoute } from "@/lib/auth";
import { AppShell } from "@/components/layout/AppShell";

import Home from "@/pages/Home";
import Chat from "@/pages/Chat";
import Explore from "@/pages/Explore";
import PlaceDetail from "@/pages/PlaceDetail";
import Planner from "@/pages/Planner";
import Weather from "@/pages/Weather";
import Budget from "@/pages/Budget";
import Emergency from "@/pages/Emergency";
import CameraAI from "@/pages/CameraAI";
import Nepal from "@/pages/Nepal";
import Saved from "@/pages/Saved";
import Profile from "@/pages/Profile";
import Login from "@/pages/Login";
import AuthCallback from "@/pages/AuthCallback";
import Admin from "@/pages/Admin";
import Business from "@/pages/Business";

function AppRouter() {
  const location = useLocation();
  // Handle OAuth return: detect session_id in URL fragment FIRST (synchronously).
  if (location.hash?.includes("session_id=")) return <AuthCallback />;
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<AppShell />}>
        <Route path="/" element={<Home />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/explore" element={<Explore />} />
        <Route path="/place/:id" element={<PlaceDetail />} />
        <Route path="/planner" element={<Planner />} />
        <Route path="/weather" element={<Weather />} />
        <Route path="/budget" element={<ProtectedRoute><Budget /></ProtectedRoute>} />
        <Route path="/emergency" element={<Emergency />} />
        <Route path="/camera" element={<CameraAI />} />
        <Route path="/nepal" element={<Nepal />} />
        <Route path="/saved" element={<ProtectedRoute><Saved /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/admin" element={<ProtectedRoute roles={["admin"]}><Admin /></ProtectedRoute>} />
        <Route path="/business" element={<ProtectedRoute roles={["business", "admin"]}><Business /></ProtectedRoute>} />
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
      <LanguageProvider>
        <BrowserRouter>
          <AuthProvider>
            <AppRouter />
          </AuthProvider>
        </BrowserRouter>
        <Toaster position="top-center" richColors />
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
