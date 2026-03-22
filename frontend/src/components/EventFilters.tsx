import { Button, Grid, NumberInput, Select, TextInput } from "@mantine/core";
import { listDocuments } from "../api/documents";
import { useAsyncData } from "../hooks/useAsyncData";
import type { EventFilters as EventFiltersType } from "../types/api";
import { eventTypeOptions } from "../constants/eventTypes";

type Props = {
  filters: EventFiltersType;
  onChange: (filters: EventFiltersType) => void;
  showDocumentId?: boolean;
};

function toOptionalNumber(value: string | number) {
  if (value === "" || value === null || value === undefined) {
    return undefined;
  }
  return Number(value);
}

export function EventFilters({ filters, onChange, showDocumentId = false }: Props) {
  const { data: documents } = useAsyncData(listDocuments, []);
  const documentsList = documents ?? [];
  const documentOptions = documentsList
    .slice()
    .sort((left, right) => left.filename.localeCompare(right.filename, "ru"))
    .map((document) => ({ value: String(document.id), label: document.filename }));

  return (
    <Grid>
      {showDocumentId ? (
        <Grid.Col span={{ base: 12, md: 2 }}>
          <Select
            searchable
            label="Документ"
            placeholder="Выберите файл"
            data={documentOptions}
            value={filters.document_id ? String(filters.document_id) : null}
            onChange={(value) => onChange({ ...filters, document_id: value ? Number(value) : undefined })}
          />
        </Grid.Col>
      ) : null}
      <Grid.Col span={{ base: 12, md: 2 }}>
        <NumberInput
          label="Год от"
          value={filters.year_from}
          onChange={(value) => onChange({ ...filters, year_from: toOptionalNumber(value) })}
        />
      </Grid.Col>
      <Grid.Col span={{ base: 12, md: 2 }}>
        <NumberInput
          label="Год до"
          value={filters.year_to}
          onChange={(value) => onChange({ ...filters, year_to: toOptionalNumber(value) })}
        />
      </Grid.Col>
      <Grid.Col span={{ base: 12, md: 3 }}>
        <Select
          label="Тип события"
          data={eventTypeOptions}
          value={filters.event_type || ""}
          onChange={(value) => onChange({ ...filters, event_type: value || undefined })}
        />
      </Grid.Col>
      <Grid.Col span={{ base: 12, md: 2 }}>
        <NumberInput
          label="Мин. уверенность"
          min={0}
          max={1}
          step={0.05}
          decimalScale={2}
          value={filters.min_confidence}
          onChange={(value) => onChange({ ...filters, min_confidence: toOptionalNumber(value) })}
        />
      </Grid.Col>
      <Grid.Col span={{ base: 12, md: 3 }}>
        <TextInput
          label="Топоним"
          value={filters.place_query || ""}
          onChange={(event) => onChange({ ...filters, place_query: event.currentTarget.value || undefined })}
        />
      </Grid.Col>
      <Grid.Col span={12}>
        <Button variant="subtle" color="tide" onClick={() => onChange({})}>
          Сбросить фильтры
        </Button>
      </Grid.Col>
    </Grid>
  );
}
