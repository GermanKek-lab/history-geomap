import { Button, Group, Modal, NumberInput, Select, Stack, Textarea, TextInput } from "@mantine/core";
import { useEffect, useState } from "react";
import { eventTypeLabels } from "../constants/eventTypes";
import type { EventItem } from "../types/api";

type Props = {
  opened: boolean;
  event: EventItem | null;
  onClose: () => void;
  onSave: (payload: Partial<EventItem>) => Promise<void>;
};

const eventTypes = [
  "battle",
  "march",
  "treaty",
  "political_event",
  "biography_event",
  "movement",
  "memoir_reference",
  "other",
];

export function EventEditorModal({ opened, event, onClose, onSave }: Props) {
  const [form, setForm] = useState<Partial<EventItem>>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setForm(event || {});
  }, [event]);

  const submit = async () => {
    setLoading(true);
    try {
      await onSave(form);
      onClose();
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title="Ручная проверка события" size="lg">
      <Stack>
        <TextInput
          label="Дата в источнике"
          value={form.time_raw || ""}
          onChange={(eventValue) => setForm({ ...form, time_raw: eventValue.currentTarget.value })}
        />
        <TextInput
          label="Период"
          value={form.period_label || ""}
          onChange={(eventValue) => setForm({ ...form, period_label: eventValue.currentTarget.value })}
        />
        <TextInput
          label="Место"
          value={form.place_name_raw || ""}
          onChange={(eventValue) => setForm({ ...form, place_name_raw: eventValue.currentTarget.value })}
        />
        <Select
          label="Тип события"
          value={form.event_type || "other"}
          data={eventTypes.map((value) => ({ value, label: eventTypeLabels[value] }))}
          onChange={(value) => setForm({ ...form, event_type: value || "other" })}
        />
        <TextInput
          label="Действие"
          value={form.action || ""}
          onChange={(eventValue) => setForm({ ...form, action: eventValue.currentTarget.value })}
        />
        <Textarea
          label="Описание"
          minRows={3}
          value={form.description || ""}
          onChange={(eventValue) => setForm({ ...form, description: eventValue.currentTarget.value })}
        />
        <Textarea
          label="Фрагмент источника"
          minRows={4}
          value={form.source_fragment || ""}
          onChange={(eventValue) => setForm({ ...form, source_fragment: eventValue.currentTarget.value })}
        />
        <Group grow>
          <NumberInput
            label="Широта"
            decimalScale={6}
            value={form.latitude ?? undefined}
            onChange={(value) => setForm({ ...form, latitude: Number(value) || null })}
          />
          <NumberInput
            label="Долгота"
            decimalScale={6}
            value={form.longitude ?? undefined}
            onChange={(value) => setForm({ ...form, longitude: Number(value) || null })}
          />
        </Group>
        <NumberInput
          label="Уверенность"
          min={0}
          max={1}
          step={0.05}
          decimalScale={2}
          value={form.confidence ?? undefined}
          onChange={(value) => setForm({ ...form, confidence: Number(value) || 0 })}
        />
        <Textarea
          label="Комментарий проверяющего"
          minRows={2}
          value={form.reviewer_comment || ""}
          onChange={(eventValue) => setForm({ ...form, reviewer_comment: eventValue.currentTarget.value, is_reviewed: true })}
        />
        <Group justify="flex-end">
          <Button variant="default" onClick={onClose}>
            Отмена
          </Button>
          <Button loading={loading} color="accent" onClick={submit}>
            Сохранить
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
}
