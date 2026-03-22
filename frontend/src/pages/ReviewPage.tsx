import { Alert, Card, Stack } from "@mantine/core";
import { useEffect, useState } from "react";
import { listEvents, updateEvent } from "../api/events";
import { EventEditorModal } from "../components/EventEditorModal";
import { EventFilters } from "../components/EventFilters";
import { EventTable } from "../components/EventTable";
import { PageHeader } from "../components/PageHeader";
import type { EventFilters as EventFiltersType, EventItem } from "../types/api";

export function ReviewPage() {
  const [filters, setFilters] = useState<EventFiltersType>({});
  const [events, setEvents] = useState<EventItem[]>([]);
  const [selected, setSelected] = useState<EventItem | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    void listEvents(filters).then(setEvents);
  }, [filters]);

  const save = async (payload: Partial<EventItem>) => {
    if (!selected) {
      return;
    }
    const updated = await updateEvent(selected.id, payload);
    setEvents((current) => current.map((item) => (item.id === updated.id ? updated : item)));
    setMessage(`Событие ${updated.id} обновлено.`);
  };

  return (
    <Stack gap="lg">
      <PageHeader
        title="Ручная проверка"
        subtitle="Экран для исправления даты, места, типа события, уверенности и комментария проверяющего."
      />

      <div className="filter-card">
        <EventFilters filters={filters} onChange={setFilters} showDocumentId />
      </div>

      {message ? <Alert color="tide">{message}</Alert> : null}

      <Card className="feature-card" radius="lg">
        <EventTable events={events} onEdit={setSelected} />
      </Card>

      <EventEditorModal opened={Boolean(selected)} event={selected} onClose={() => setSelected(null)} onSave={save} />
    </Stack>
  );
}
