import { Outlet, useLocation } from "react-router-dom";
import { Sidebar } from "@/components/layout/Sidebar";
import { BottomNav } from "@/components/layout/BottomNav";
import { TopBar } from "@/components/layout/TopBar";

export function AppShell() {
  const location = useLocation();
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className="lg:pl-[280px] xl:pl-[300px] flex flex-col min-h-screen">
        <TopBar />
        <main
          key={location.pathname}
          className="flex-1 pb-[calc(env(safe-area-inset-bottom)+76px)] lg:pb-0"
        >
          <Outlet />
        </main>
      </div>
      <BottomNav />
    </div>
  );
}
