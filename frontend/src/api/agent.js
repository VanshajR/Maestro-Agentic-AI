import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 60000
});

export const executeAgent = async (payload) => {
  const endpoint = import.meta.env.VITE_AGENT_ENDPOINT || '/agent/execute';
  const { data } = await client.post(endpoint, payload);
  return data;
};

export const planAgent = async (payload) => {
  const endpoint = import.meta.env.VITE_PLAN_ENDPOINT || '/agent/plan';
  const { data } = await client.post(endpoint, payload);
  return data;
};
