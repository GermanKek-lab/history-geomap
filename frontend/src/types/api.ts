export type DocumentItem = {
  id: number;
  filename: string;
  format: string;
  source_type: string;
  processing_status: string;
  last_error: string | null;
  uploaded_at: string;
  chunks_count: number;
  events_count: number;
};

export type DocumentDetail = DocumentItem & {
  storage_path: string | null;
  original_text: string;
};

export type DocumentTextResponse = {
  id: number;
  filename: string;
  text: string;
};

export type ExtractionResponse = {
  document_id: number;
  status: string;
  chunks_created: number;
  events_created: number;
  warnings: string[];
  csv_path: string | null;
  json_path: string | null;
  geojson_path: string | null;
};

export type EventItem = {
  id: number;
  document_id: number;
  chunk_id: number | null;
  time_raw: string;
  time_normalized_start: string | null;
  time_normalized_end: string | null;
  period_label: string | null;
  place_name_raw: string;
  place_name_normalized: string | null;
  latitude: number | null;
  longitude: number | null;
  event_type: string;
  action: string;
  description: string;
  confidence: number;
  source_fragment: string;
  is_reviewed: boolean;
  reviewer_comment: string | null;
  created_at: string;
  updated_at: string;
};

export type GeoJsonFeature = {
  type: "Feature";
  geometry: {
    type: "Point";
    coordinates: [number, number];
  };
  properties: EventItem;
};

export type GeoJsonFeatureCollection = {
  type: "FeatureCollection";
  features: GeoJsonFeature[];
};

export type EventStatsBucket = {
  label: string;
  count: number;
};

export type EventStats = {
  total_events: number;
  reviewed_events: number;
  without_coordinates: number;
  by_type: EventStatsBucket[];
  by_period: EventStatsBucket[];
  by_year: EventStatsBucket[];
};

export type EventFilters = {
  document_id?: number;
  year_from?: number;
  year_to?: number;
  event_type?: string;
  min_confidence?: number;
  place_query?: string;
};
