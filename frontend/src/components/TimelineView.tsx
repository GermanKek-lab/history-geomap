import { Badge, Card, Group, Stack, Text } from "@mantine/core";
import { formatEventTypeLabel } from "../constants/eventTypes";
import type { EventItem } from "../types/api";

type Props = {
  events: EventItem[];
};

export function TimelineView({ events }: Props) {
  return (
    <Stack gap="sm">
      {events.map((event) => (
        <Card key={event.id} className="timeline-card" radius="lg">
          <Group justify="space-between" align="flex-start">
            <div>
              <Text fw={700}>{event.time_normalized_start || event.time_raw}</Text>
              <Text c="dimmed" size="sm">
                {event.place_name_normalized || event.place_name_raw}
              </Text>
            </div>
            <Badge color="accent" variant="light">
              {formatEventTypeLabel(event.event_type)}
            </Badge>
          </Group>
          <Text mt="sm">{event.description}</Text>
        </Card>
      ))}
    </Stack>
  );
}
