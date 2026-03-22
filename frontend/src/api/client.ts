const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function buildQuery(params?: Record<string, string | number | undefined>) {
  if (!params) {
    return "";
  }

  const search = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      search.set(key, String(value));
    }
  });
  const query = search.toString();
  return query ? `?${query}` : "";
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Ошибка запроса ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function fileUrl(path: string) {
  return `${API_BASE_URL}${path}`;
}

export { API_BASE_URL, buildQuery };
