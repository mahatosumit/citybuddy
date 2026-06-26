import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

const client = axios.create({
  baseURL: API,
  headers: { "Content-Type": "application/json", "X-User-Id": "demo-user" },
});

const data = (p) => p.then((r) => r.data);

export const api = {
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
  getTrip: (id) => data(client.get(`/trips/${id}`)),
  deleteTrip: (id) => data(client.delete(`/trips/${id}`)),
  // budgets
  getBudgets: () => data(client.get("/budgets")),
  createBudget: (body) => data(client.post("/budgets", body)),
  updateBudget: (id, body) => data(client.put(`/budgets/${id}`, body)),
  deleteBudget: (id) => data(client.delete(`/budgets/${id}`)),
  // weather
  getWeather: (params = {}) => data(client.get("/weather", { params })),
  getWeatherCities: () => data(client.get("/weather/cities")),
  // emergency
  getEmergencyNumbers: () => data(client.get("/emergency/numbers")),
  getEmergencyNearby: (lat, lon, type) =>
    data(client.get("/emergency/nearby", { params: { lat, lon, type } })),
  getGuidance: (type) => data(client.get("/emergency/guidance", { params: { type } })),
  getGuidanceAll: () => data(client.get("/emergency/guidance-all")),
  // nepal
  nepalOverview: () => data(client.get("/nepal/overview")),
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
};
