const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function login(email: string, password: string) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Invalid credentials");
  }
  const data = await res.json();
  localStorage.setItem("access_token", data.access_token);
  return data;
}

export async function signup(name: string, email: string, password: string) {
  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Signup failed");
  }
}

export function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "/login";
}

export function getToken() {
  return localStorage.getItem("access_token");
}