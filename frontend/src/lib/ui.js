import {
  MessageSquare, Map, CalendarRange, CloudSun, Wallet, Camera,
  Mountain, ShieldAlert, Bookmark, User, Home, Hotel, UtensilsCrossed,
  Landmark, PartyPopper, MapPin,
} from "lucide-react";

// Primary + secondary navigation (shared by sidebar + bottom tabs)
export const PRIMARY_NAV = [
  { to: "/", label: "Home", icon: Home, testid: "nav-home" },
  { to: "/chat", label: "CityBrain", icon: MessageSquare, testid: "nav-chat" },
  { to: "/explore", label: "Explore", icon: Map, testid: "nav-explore" },
  { to: "/planner", label: "Trip Planner", icon: CalendarRange, testid: "nav-planner" },
  { to: "/weather", label: "Weather", icon: CloudSun, testid: "nav-weather" },
  { to: "/budget", label: "Budget", icon: Wallet, testid: "nav-budget" },
];

export const SECONDARY_NAV = [
  { to: "/camera", label: "Camera AI", icon: Camera, testid: "nav-camera" },
  { to: "/nepal", label: "Nepal Intel", icon: Mountain, testid: "nav-nepal" },
  { to: "/saved", label: "Saved", icon: Bookmark, testid: "nav-saved" },
  { to: "/emergency", label: "Emergency", icon: ShieldAlert, testid: "nav-emergency", danger: true },
];

export const BOTTOM_NAV = [
  { to: "/chat", label: "CityBrain", icon: MessageSquare, testid: "tab-chat" },
  { to: "/explore", label: "Explore", icon: Map, testid: "tab-explore" },
  { to: "/planner", label: "Planner", icon: CalendarRange, testid: "tab-planner" },
  { to: "/saved", label: "Saved", icon: Bookmark, testid: "tab-saved" },
  { to: "/profile", label: "Profile", icon: User, testid: "tab-profile" },
];

// place type -> icon + color (matches map pin colors)
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
