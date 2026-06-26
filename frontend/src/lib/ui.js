import {
  MessageSquare, Map, CalendarRange, CloudSun, Wallet, Camera,
  Mountain, ShieldAlert, Bookmark, User, Home, Hotel, UtensilsCrossed,
  Landmark, PartyPopper, MapPin, LayoutDashboard, Store,
} from "lucide-react";

export const PRIMARY_NAV = [
  { to: "/", labelKey: "nav.home", icon: Home, testid: "nav-home" },
  { to: "/chat", labelKey: "nav.chat", icon: MessageSquare, testid: "nav-chat" },
  { to: "/explore", labelKey: "nav.explore", icon: Map, testid: "nav-explore" },
  { to: "/planner", labelKey: "nav.planner", icon: CalendarRange, testid: "nav-planner" },
  { to: "/weather", labelKey: "nav.weather", icon: CloudSun, testid: "nav-weather" },
  { to: "/budget", labelKey: "nav.budget", icon: Wallet, testid: "nav-budget" },
];

export const SECONDARY_NAV = [
  { to: "/camera", labelKey: "nav.camera", icon: Camera, testid: "nav-camera" },
  { to: "/nepal", labelKey: "nav.nepal", icon: Mountain, testid: "nav-nepal" },
  { to: "/saved", labelKey: "nav.saved", icon: Bookmark, testid: "nav-saved" },
  { to: "/emergency", labelKey: "nav.emergency", icon: ShieldAlert, testid: "nav-emergency", danger: true },
];

export const ROLE_NAV = {
  admin: { to: "/admin", labelKey: "nav.admin", icon: LayoutDashboard, testid: "nav-admin" },
  business: { to: "/business", labelKey: "nav.business", icon: Store, testid: "nav-business" },
};

export const BOTTOM_NAV = [
  { to: "/chat", labelKey: "nav.chat", icon: MessageSquare, testid: "tab-chat" },
  { to: "/explore", labelKey: "nav.explore", icon: Map, testid: "tab-explore" },
  { to: "/planner", labelKey: "nav.planner", icon: CalendarRange, testid: "tab-planner" },
  { to: "/saved", labelKey: "nav.saved", icon: Bookmark, testid: "tab-saved" },
  { to: "/profile", labelKey: "nav.profile", icon: User, testid: "tab-profile" },
];

export const TYPE_META = {
  hotel: { icon: Hotel, color: "#1E2A5A", label: "Hotel" },
  restaurant: { icon: UtensilsCrossed, color: "#F59E0B", label: "Restaurant" },
  attraction: { icon: Landmark, color: "#0EA5A4", label: "Attraction" },
  event: { icon: PartyPopper, color: "#DC2626", label: "Event" },
  default: { icon: MapPin, color: "#0EA5A4", label: "Place" },
};
export const typeMeta = (t) => TYPE_META[t] || TYPE_META.default;

export function formatNPR(n) {
  if (n === 0) return "Free";
  if (n === null || n === undefined || n === "") return "";
  const num = Number(n);
  if (Number.isNaN(num)) return "";
  return "Rs " + num.toLocaleString("en-IN");
}

export function initials(name = "") {
  return name.split(" ").map((w) => w[0]).slice(0, 2).join("").toUpperCase();
}
