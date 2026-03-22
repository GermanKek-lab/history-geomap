import { Card, Group, Progress, Stack, Text } from "@mantine/core";
import type { EventStatsBucket } from "../types/api";

type Props = {
  title: string;
  items: EventStatsBucket[];
  labelFormatter?: (label: string) => string;
};

export function StatsBars({ title, items, labelFormatter }: Props) {
  const max = items[0]?.count || 1;

  return (
    <Card className="feature-card" radius="lg" padding="lg">
      <Stack>
        <Text fw={700}>{title}</Text>
        {items.map((item) => (
          <div key={item.label}>
            <Group justify="space-between">
              <Text size="sm">{labelFormatter ? labelFormatter(item.label) : item.label}</Text>
              <Text size="sm" fw={700}>
                {item.count}
              </Text>
            </Group>
            <Progress value={(item.count / max) * 100} color="accent" radius="xl" />
          </div>
        ))}
      </Stack>
    </Card>
  );
}
