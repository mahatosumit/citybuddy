import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "next-themes";
import { Toaster } from "@/components/ui/sonner";
import { LanguageProvider } from "@/lib/i18n";
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

function App() {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
      <LanguageProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<AppShell />}>
              <Route path="/" element={<Home />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="/explore" element={<Explore />} />
              <Route path="/place/:id" element={<PlaceDetail />} />
              <Route path="/planner" element={<Planner />} />
              <Route path="/weather" element={<Weather />} />
              <Route path="/budget" element={<Budget />} />
              <Route path="/emergency" element={<Emergency />} />
              <Route path="/camera" element={<CameraAI />} />
              <Route path="/nepal" element={<Nepal />} />
              <Route path="/saved" element={<Saved />} />
              <Route path="/profile" element={<Profile />} />
            </Route>
          </Routes>
        </BrowserRouter>
        <Toaster position="top-center" richColors />
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
