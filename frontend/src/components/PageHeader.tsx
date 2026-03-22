import type { ReactNode } from "react";
import { Group, Stack, Text, Title } from "@mantine/core";

type Props = {
  title: string;
  subtitle: string;
  action?: ReactNode;
};

export function PageHeader({ title, subtitle, action }: Props) {
  return (
    <Group justify="space-between" align="flex-end" mb="lg">
      <Stack gap={4}>
        <Text size="xs" tt="uppercase" fw={700} c="accent.6">
          GeoAutoMap
        </Text>
        <Title order={1}>{title}</Title>
        <Text c="dimmed" maw={720}>
          {subtitle}
        </Text>
      </Stack>
      {action}
    </Group>
  );
}
