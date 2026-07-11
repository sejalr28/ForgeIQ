// frontend/src/api/client.js
import axios from "axios";

// In development, requests go through the Vite dev proxy (see vite.config.js)
// at the same origin under /api, avoiding the need for CORS headers on the API.
// In production, point VITE_API_BASE_URL at the deployed API's absolute URL.
const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";

const client = axios.create({
    baseURL,
    timeout: 15000,
});

export default client;