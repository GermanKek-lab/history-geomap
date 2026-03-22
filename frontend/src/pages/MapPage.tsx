import { Grid, Stack, Text } from "@mantine/core";
import { useEffect, useState } from "react";
import { listEvents, mapEvents } from "../api/events";
import { EventFilters } from "../components/EventFilters";
import { EventTable } from "../components/EventTable";
import { MapPanel } from "../components/MapPanel";
import { PageHeader } from "../components/PageHeader";
import type { EventFilters as EventFiltersType, EventItem, GeoJsonFeatureCollection } from "../types/api";

export function MapPage() {
  const [filters, setFilters] = useState<EventFiltersType>({});
  const [events, setEvents] = useState<EventItem[]>([]);
  const [geojson, setGeojson] = useState<GeoJsonFeatureCollection | null>(null);

  useEffect(() => {
    void Promise.all([listEvents(filters), mapEvents(filters)]).then(([eventsResult, mapResult]) => {
      setEvents(eventsResult);
      setGeojson(mapResult);
    });
  }, [filters]);

  return (
    <Stack gap="lg">
      <PageHeader
        title="Карта событий"
        subtitle="Интерактивная карта с фильтрами по времени, типу события, документу и уровню уверенности. В popup отображается краткая карточка события."
      />
      <div className="filter-card">
        <EventFilters filters={filters} onChange={setFilters} showDocumentId />
      </div>
      <Grid>
        <Grid.Col span={{ base: 12, xl: 8 }}>
          <MapPanel geojson={geojson} />
        </Grid.Col>
        <Grid.Col span={{ base: 12, xl: 4 }}>
          <div className="side-list">
            <Text fw={700} mb="sm">
              Отфильтрованные события
            </Text>
            <EventTable events={events.slice(0, 12)} />
          </div>
        </Grid.Col>
      </Grid>
    </Stack>
  );
}
