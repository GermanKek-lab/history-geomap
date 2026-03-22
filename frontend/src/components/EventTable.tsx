import { ActionIcon, Badge, ScrollArea, Table, Text } from "@mantine/core";
import { IconPencil } from "@tabler/icons-react";
import { formatEventTypeLabel } from "../constants/eventTypes";
import type { EventItem } from "../types/api";

type Props = {
  events: EventItem[];
  onEdit?: (event: EventItem) => void;
};

export function EventTable({ events, onEdit }: Props) {
  if (!events.length) {
    return (
      <Text c="dimmed" size="sm">
        События пока не извлечены.
      </Text>
    );
  }

  return (
    <ScrollArea>
      <Table striped highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Дата</Table.Th>
            <Table.Th>Место</Table.Th>
            <Table.Th>Тип</Table.Th>
            <Table.Th>Описание</Table.Th>
            <Table.Th>Confidence</Table.Th>
            <Table.Th />
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {events.map((event) => (
            <Table.Tr key={event.id}>
              <Table.Td>{event.time_normalized_start || event.time_raw}</Table.Td>
              <Table.Td>{event.place_name_normalized || event.place_name_raw}</Table.Td>
              <Table.Td>
                <Badge color="accent" variant="light">
                  {formatEventTypeLabel(event.event_type)}
                </Badge>
              </Table.Td>
              <Table.Td>{event.description}</Table.Td>
              <Table.Td>{event.confidence.toFixed(2)}</Table.Td>
              <Table.Td>
                {onEdit ? (
                  <ActionIcon variant="subtle" color="tide" onClick={() => onEdit(event)}>
                    <IconPencil size={16} />
                  </ActionIcon>
                ) : null}
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </ScrollArea>
  );
}
