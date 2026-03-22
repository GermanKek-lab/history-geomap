export const eventTypeLabels: Record<string, string> = {
  battle: "Сражение",
  march: "Поход",
  treaty: "Договор",
  political_event: "Политическое событие",
  biography_event: "Биографическое событие",
  movement: "Перемещение",
  memoir_reference: "Мемуарное свидетельство",
  other: "Другое",
};

export const eventTypeOptions = [
  { value: "", label: "Все типы" },
  ...Object.entries(eventTypeLabels).map(([value, label]) => ({ value, label })),
];

export function formatEventTypeLabel(eventType: string) {
  return eventTypeLabels[eventType] || eventType;
}
