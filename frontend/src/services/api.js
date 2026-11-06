
const BASE = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/+$/, "");

async function req(path, options = {}) {
  const url = `${BASE}${path}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  const text = await response.text();

  if (!response.ok) {
    throw new Error(
      `HTTP ${response.status} | ${url}\n${text}`
    );
  }

  if (response.status === 204) return null;

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(
      `Expected JSON but received HTML/text.\nURL: ${url}\nResponse: ${text.slice(0, 300)}`
    );
  }
}

// Dashboard
export const getDashboard = () => req("/api/dashboard");

// Claims
export const getClaims = () => req("/api/claims");

export const getClaim = (id) =>
  req(`/api/claims/${encodeURIComponent(id)}`);

export const createClaim = (data) =>
  req("/api/claims", {
    method: "POST",
    body: JSON.stringify(data),
  });

export const evaluateClaim = (id) =>
  req(`/api/claims/${encodeURIComponent(id)}/evaluate`, {
    method: "POST",
  });

// Investigations
export const getInvestigations = () =>
  req("/api/investigations");

// Pool
export const getPool = () =>
  req("/api/pool");

// Settlement ledger
export const getLedger = () =>
  req("/api/settlements/ledger");
