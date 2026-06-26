import { createContext, useContext, useEffect, useState, useCallback } from "react";

// ---- Translations (EN / NE). Falls back to EN, then the key itself. ----
export const STRINGS = {
  en: {
    "brand.tagline": "Your AI Companion for Nepal",
    "nav.home": "Home", "nav.chat": "CityBrain", "nav.explore": "Explore",
    "nav.planner": "Trip Planner", "nav.weather": "Weather", "nav.budget": "Budget",
    "nav.camera": "Camera AI", "nav.nepal": "Nepal Intel", "nav.saved": "Saved",
    "nav.emergency": "Emergency", "nav.profile": "Profile", "nav.admin": "Admin",
    "nav.business": "Business", "nav.more": "More",
    "common.signin": "Sign in", "common.signup": "Sign up", "common.logout": "Log out",
    "common.loading": "Loading\u2026", "common.save": "Save", "common.search": "Search",
    "common.seeAll": "See all", "common.new": "New", "common.delete": "Delete", "common.free": "Free",
    "auth.welcome": "Welcome back", "auth.create": "Create your account",
    "auth.email": "Email", "auth.password": "Password", "auth.name": "Name",
    "auth.google": "Continue with Google", "auth.or": "or",
    "auth.haveAccount": "Already have an account?", "auth.noAccount": "Don't have an account?",
    "auth.loginCta": "Log in", "auth.signupCta": "Sign up",
    "auth.gate": "Sign in to use this feature",
    "home.heroTitle": "Your AI Companion for Nepal",
    "home.heroSub": "Maps, trip planning, weather, budgets, emergencies and deep local knowledge \u2014 unified into one intelligent companion that reasons before it recommends.",
    "home.askCity": "Ask CityBrain", "home.exploreNepal": "Explore Nepal",
    "home.help": "What can I help with?", "home.byCity": "Explore by city", "home.topRated": "Top rated in Nepal",
    "chat.title": "CityBrain", "chat.sub": "Multi-agent AI that reasons over Nepal",
    "chat.placeholder": "Ask CityBrain anything about Nepal\u2026",
    "chat.greeting": "Namaste! I'm CityBrain", "chat.why": "Why this & how I decided",
    "explore.searchPh": "Search places, food, temples\u2026", "explore.nearMe": "Near me",
    "explore.all": "All", "explore.attractions": "Attractions", "explore.food": "Food",
    "explore.hotels": "Hotels", "explore.events": "Events", "explore.empty": "No places found",
    "planner.title": "AI Trip Planner", "planner.generate": "Generate Itinerary", "planner.saveTrip": "Save trip",
    "weather.title": "Weather across Nepal", "budget.title": "Budget Planner",
    "emergency.title": "Emergency Mode", "camera.title": "Camera AI",
    "nepal.title": "Nepal Intelligence", "saved.title": "Saved", "profile.title": "Profile",
  },
  ne: {
    "brand.tagline": "\u0928\u0947\u092a\u093e\u0932\u0915\u093e \u0932\u093e\u0917\u093f \u0924\u092a\u093e\u0908\u0915\u094b AI \u0938\u093e\u0925\u0940",
    "nav.home": "\u0917\u0943\u0939", "nav.chat": "\u0938\u093f\u091f\u0940\u092c\u094d\u0930\u0947\u0928", "nav.explore": "\u0905\u0928\u094d\u0935\u0947\u0937\u0923",
    "nav.planner": "\u092f\u093e\u0924\u094d\u0930\u093e \u092f\u094b\u091c\u0928\u093e", "nav.weather": "\u092e\u094c\u0938\u092e", "nav.budget": "\u092c\u091c\u0947\u091f",
    "nav.camera": "\u0915\u094d\u092f\u093e\u092e\u0947\u0930\u093e AI", "nav.nepal": "\u0928\u0947\u092a\u093e\u0932 \u091c\u093e\u0928\u0915\u093e\u0930\u0940", "nav.saved": "\u0938\u0947\u092d \u0917\u0930\u093f\u090f\u0915\u094b",
    "nav.emergency": "\u0906\u092a\u0924\u094d\u0915\u093e\u0932\u0940\u0928", "nav.profile": "\u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932", "nav.admin": "\u090f\u0921\u092e\u093f\u0928",
    "nav.business": "\u0935\u094d\u092f\u0935\u0938\u093e\u092f", "nav.more": "\u0925\u092a",
    "common.signin": "\u0938\u093e\u0907\u0928 \u0907\u0928", "common.signup": "\u0926\u0930\u094d\u0924\u093e", "common.logout": "\u0932\u0917\u0906\u0909\u091f",
    "common.loading": "\u0932\u094b\u0921 \u0939\u0941\u0901\u0926\u0948\u2026", "common.save": "\u0938\u0947\u092d", "common.search": "\u0916\u094b\u091c",
    "common.seeAll": "\u0938\u092c\u0948 \u0939\u0947\u0930\u094d\u0928\u0941\u0939\u094b\u0938\u094d", "common.new": "\u0928\u092f\u093e\u0901", "common.delete": "\u092e\u0947\u091f\u093e\u0909\u0928\u0941\u0939\u094b\u0938\u094d", "common.free": "\u0928\u093f\u0903\u0936\u0941\u0932\u094d\u0915",
    "auth.welcome": "\u092a\u0941\u0928\u0903 \u0938\u094d\u0935\u093e\u0917\u0924 \u091b", "auth.create": "\u0906\u092b\u094d\u0928\u094b \u0916\u093e\u0924\u093e \u092c\u0928\u093e\u0909\u0928\u0941\u0939\u094b\u0938\u094d",
    "auth.email": "\u0907\u092e\u0947\u0932", "auth.password": "\u092a\u093e\u0938\u0935\u0930\u094d\u0921", "auth.name": "\u0928\u093e\u092e",
    "auth.google": "Google \u092e\u093e\u0930\u094d\u092b\u0924 \u091c\u093e\u0930\u0940 \u0930\u093e\u0916\u094d\u0928\u0941\u0939\u094b\u0938\u094d", "auth.or": "\u0935\u093e",
    "auth.haveAccount": "\u092a\u0939\u093f\u0932\u0947\u0926\u0947\u0916\u093f \u0916\u093e\u0924\u093e \u091b?", "auth.noAccount": "\u0916\u093e\u0924\u093e \u091b\u0948\u0928?",
    "auth.loginCta": "\u0932\u0917 \u0907\u0928", "auth.signupCta": "\u0926\u0930\u094d\u0924\u093e",
    "auth.gate": "\u092f\u094b \u0938\u0941\u0935\u093f\u0927\u093e \u092a\u094d\u0930\u092f\u094b\u0917 \u0917\u0930\u094d\u0928 \u0938\u093e\u0907\u0928 \u0907\u0928 \u0917\u0930\u094d\u0928\u0941\u0939\u094b\u0938\u094d",
    "home.heroTitle": "\u0928\u0947\u092a\u093e\u0932\u0915\u093e \u0932\u093e\u0917\u093f \u0924\u092a\u093e\u0908\u0915\u094b AI \u0938\u093e\u0925\u0940",
    "home.heroSub": "\u0928\u0915\u094d\u0938\u093e, \u092f\u093e\u0924\u094d\u0930\u093e \u092f\u094b\u091c\u0928\u093e, \u092e\u094c\u0938\u092e, \u092c\u091c\u0947\u091f \u0930 \u0938\u094d\u0925\u093e\u0928\u0940\u092f \u091c\u094d\u091e\u093e\u0928 \u090f\u0909\u091f\u0948 \u092c\u0941\u0926\u094d\u0927\u093f\u092e\u093e\u0928\u094d \u0938\u093e\u0925\u0940\u092e\u093e\u0964",
    "home.askCity": "\u0938\u093f\u091f\u0940\u092c\u094d\u0930\u0947\u0928\u0932\u093e\u0908 \u0938\u094b\u0927\u094d\u0928\u0941\u0939\u094b\u0938\u094d", "home.exploreNepal": "\u0928\u0947\u092a\u093e\u0932 \u0905\u0928\u094d\u0935\u0947\u0937\u0923",
    "home.help": "\u092e \u0915\u0938\u0930\u0940 \u0938\u0939\u092f\u094b\u0917 \u0917\u0930\u0942\u0901?", "home.byCity": "\u0936\u0939\u0930 \u0905\u0928\u0941\u0938\u093e\u0930 \u0905\u0928\u094d\u0935\u0947\u0937\u0923", "home.topRated": "\u0928\u0947\u092a\u093e\u0932\u092e\u093e \u0936\u0940\u0930\u094d\u0937 \u0930\u0947\u091f\u093f\u0919",
    "chat.title": "\u0938\u093f\u091f\u0940\u092c\u094d\u0930\u0947\u0928", "chat.sub": "\u0928\u0947\u092a\u093e\u0932\u092c\u093e\u0930\u0947 \u0924\u0930\u094d\u0915 \u0917\u0930\u094d\u0928\u0947 AI",
    "chat.placeholder": "\u0928\u0947\u092a\u093e\u0932\u092c\u093e\u0930\u0947 \u0915\u0947\u0939\u0940 \u092a\u0928\u093f \u0938\u094b\u0927\u094d\u0928\u0941\u0939\u094b\u0938\u094d\u2026",
    "chat.greeting": "\u0928\u092e\u0938\u094d\u0924\u0947! \u092e \u0938\u093f\u091f\u0940\u092c\u094d\u0930\u0947\u0928 \u0939\u0942\u0901", "chat.why": "\u0915\u093f\u0928 \u0930 \u0915\u0938\u0930\u0940 \u0928\u093f\u0930\u094d\u0923\u092f \u0917\u0930\u0947\u0902",
    "explore.searchPh": "\u0938\u094d\u0925\u093e\u0928, \u0916\u093e\u0928\u093e, \u092e\u0928\u094d\u0926\u093f\u0930 \u0916\u094b\u091c\u094d\u0928\u0941\u0939\u094b\u0938\u094d\u2026", "explore.nearMe": "\u0928\u091c\u093f\u0915",
    "explore.all": "\u0938\u092c\u0948", "explore.attractions": "\u0906\u0915\u0930\u094d\u0937\u0923", "explore.food": "\u0916\u093e\u0928\u093e",
    "explore.hotels": "\u0939\u094b\u091f\u0932", "explore.events": "\u0915\u093e\u0930\u094d\u092f\u0915\u094d\u0930\u092e", "explore.empty": "\u0915\u0941\u0928\u0948 \u0938\u094d\u0925\u093e\u0928 \u092b\u0947\u0932\u093e \u092a\u0930\u0947\u0928",
    "planner.title": "AI \u092f\u093e\u0924\u094d\u0930\u093e \u092f\u094b\u091c\u0928\u093e\u0915\u093e\u0930", "planner.generate": "\u092f\u093e\u0924\u094d\u0930\u093e\u0935\u093f\u0935\u0930\u0923 \u092c\u0928\u093e\u0909\u0928\u0941\u0939\u094b\u0938\u094d", "planner.saveTrip": "\u092f\u093e\u0924\u094d\u0930\u093e \u0938\u0947\u092d",
    "weather.title": "\u0928\u0947\u092a\u093e\u0932\u092d\u0930\u093f\u0915\u094b \u092e\u094c\u0938\u092e", "budget.title": "\u092c\u091c\u0947\u091f \u092f\u094b\u091c\u0928\u093e",
    "emergency.title": "\u0906\u092a\u0924\u094d\u0915\u093e\u0932\u0940\u0928 \u092e\u094b\u0921", "camera.title": "\u0915\u094d\u092f\u093e\u092e\u0947\u0930\u093e AI",
    "nepal.title": "\u0928\u0947\u092a\u093e\u0932 \u091c\u093e\u0928\u0915\u093e\u0930\u0940", "saved.title": "\u0938\u0947\u092d \u0917\u0930\u093f\u090f\u0915\u094b", "profile.title": "\u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932",
  },
};

const LanguageContext = createContext({ lang: "en", setLang: () => {}, t: (k) => k });

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => localStorage.getItem("cb_lang") || "en");
  useEffect(() => { localStorage.setItem("cb_lang", lang); }, [lang]);
  const t = useCallback((key) => (STRINGS[lang] && STRINGS[lang][key]) || STRINGS.en[key] || key, [lang]);
  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>{children}</LanguageContext.Provider>
  );
}

export const useLanguage = () => useContext(LanguageContext);
export const useT = () => useContext(LanguageContext).t;
