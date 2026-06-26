import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

const TOKEN_KEY = "cb_token";
export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (t) => (t ? localStorage.setItem(TOKEN_KEY, t) : localStorage.removeItem(TOKEN_KEY));

const client = axios.create({ baseURL: API, withCredentials: true });
client.interceptors.request.use((config) => {
  const t = getToken();
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

const data = (p) => p.then((r) => r.data);

export const api = {
  // auth
  register: (body) => data(client.post("/auth/register", body)),
  login: (body) => data(client.post("/auth/login", body)),
  googleSession: (session_id) => data(client.post("/auth/google/session", { session_id })),
  me: () => data(client.get("/auth/me")),
  logout: () => data(client.post("/auth/logout")),
  registerBusiness: () => data(client.post("/auth/register-business")),
  // places
  getPlaces: (params = {}) => data(client.get("/places", { params })),
  getPlace: (id) => data(client.get(`/places/${id}`)),
  getCities: () => data(client.get("/places/cities")),
  getReviews: (id) => data(client.get(`/places/${id}/reviews`)),
  addReview: (id, body) => data(client.post(`/places/${id}/reviews`, body)),
  // favorites
  getFavorites: () => data(client.get("/favorites")),
  getFavoriteIds: () => data(client.get("/favorites/ids")),
  addFavorite: (id) => data(client.post(`/favorites/${id}`)),
  removeFavorite: (id) => data(client.delete(`/favorites/${id}`)),
  // chat
  chat: (body) => data(client.post("/chat/message", body)),
  getConversations: () => data(client.get("/chat/conversations")),
  getConversation: (id) => data(client.get(`/chat/conversations/${id}`)),
  deleteConversation: (id) => data(client.delete(`/chat/conversations/${id}`)),
  // trips
  generateTrip: (body) => data(client.post("/trips/generate", body)),
  getTrips: () => data(client.get("/trips")),
  saveTrip: (body) => data(client.post("/trips", body)),
  deleteTrip: (id) => data(client.delete(`/trips/${id}`)),
  // budgets
  getBudgets: () => data(client.get("/budgets")),
  createBudget: (body) => data(client.post("/budgets", body)),
  updateBudget: (id, body) => data(client.put(`/budgets/${id}`, body)),
  deleteBudget: (id) => data(client.delete(`/budgets/${id}`)),
  // weather
  getWeather: (params = {}) => data(client.get("/weather", { params })),
  // emergency
  getEmergencyNumbers: () => data(client.get("/emergency/numbers")),
  getEmergencyNearby: (lat, lon, type) => data(client.get("/emergency/nearby", { params: { lat, lon, type } })),
  getGuidanceAll: () => data(client.get("/emergency/guidance-all")),
  // nepal
  nepalFestivals: () => data(client.get("/nepal/festivals")),
  nepalTreks: () => data(client.get("/nepal/treks")),
  nepalUnesco: () => data(client.get("/nepal/unesco")),
  nepalTransport: () => data(client.get("/nepal/transport")),
  nepalInfo: () => data(client.get("/nepal/info")),
  // vision
  analyzeImage: (image_base64, note) => data(client.post("/vision/analyze", { image_base64, note })),
  // profile
  getProfile: () => data(client.get("/profile")),
  updateProfile: (body) => data(client.put("/profile", body)),
  // admin
  adminStats: () => data(client.get("/admin/stats")),
  adminUsers: () => data(client.get("/admin/users")),
  adminSetRole: (uid, role) => data(client.put(`/admin/users/${uid}/role`, { role })),
  adminCreatePlace: (body) => data(client.post("/admin/places", body)),
  adminDeletePlace: (id) => data(client.delete(`/admin/places/${id}`)),
  adminReviews: () => data(client.get("/admin/reviews")),
  adminDeleteReview: (id) => data(client.delete(`/admin/reviews/${id}`)),
  // business
  bizClaim: (place_id) => data(client.post("/business/claim", { place_id })),
  bizListings: () => data(client.get("/business/listings")),
  bizUpdateListing: (id, body) => data(client.put(`/business/listings/${id}`, body)),
  bizReviews: () => data(client.get("/business/reviews")),
  bizReply: (rid, reply) => data(client.post(`/business/reviews/${rid}/reply`, { reply })),
};
