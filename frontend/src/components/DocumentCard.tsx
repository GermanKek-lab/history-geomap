import { Badge, Button, Card, Group, Stack, Text } from "@mantine/core";
import { Link } from "react-router-dom";
import type { DocumentItem } from "../types/api";

type Props = {
  document: DocumentItem;
};

export function DocumentCard({ document }: Props) {
  return (
    <Card className="feature-card" radius="lg" padding="lg">
      <Stack gap="sm">
        <Group justify="space-between">
          <Badge color="accent" variant="light">
            {document.format.toUpperCase()}
          </Badge>
          <Badge color={document.processing_status === "completed" ? "tide" : "accent"} variant="dot">
            {document.processing_status}
          </Badge>
        </Group>
        <div>
          <Text fw={700}>{document.filename}</Text>
          <Text size="sm" c="dimmed">
            Источник: {document.source_type} | событий: {document.events_count} | чанков: {document.chunks_count}
          </Text>
        </div>
        {document.last_error ? (
          <Text size="sm" c="accent.6">
            Последняя ошибка: {document.last_error}
          </Text>
        ) : null}
        <Button component={Link} to={`/documents/${document.id}`} color="tide">
          Открыть документ
        </Button>
      </Stack>
    </Card>
  );
}
