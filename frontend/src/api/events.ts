import type { EventFilters, EventItem, EventStats, GeoJsonFeatureCollection } from "../types/api";
import { buildQuery, request } from "./client";

export function listEvents(filters: EventFilters = {}) {
  return request<EventItem[]>(`/api/events${buildQuery(filters as Record<string, string | number | undefined>)}`);
}

export function mapEvents(filters: EventFilters = {}) {
  return request<GeoJsonFeatureCollection>(`/api/events/map${buildQuery(filters as Record<string, string | number | undefined>)}`);
}

export function updateEvent(id: number, payload: Partial<EventItem>) {
  return request<EventItem>(`/api/events/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function getEventStats() {
  return request<EventStats>("/api/events/stats");
}
