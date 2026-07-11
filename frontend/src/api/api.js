// frontend/src/api/api.js
import client from "./client";

export async function getFactories() {
  const { data } = await client.get("/factories/");
  return data;
}

export async function getMachines() {
  const { data } = await client.get("/machines/");
  return data;
}

export async function getDashboardOverview() {
  const { data } = await client.get("/dashboard/overview");
  return data;
}

export async function predictFailure(payload) {
  const { data } = await client.post("/predict/failure", payload);
  return data;
}