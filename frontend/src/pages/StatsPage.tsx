import { Grid, SimpleGrid, Stack, Text } from "@mantine/core";
import { getEventStats } from "../api/events";
import { PageHeader } from "../components/PageHeader";
import { StatsBars } from "../components/StatsBars";
import { formatEventTypeLabel } from "../constants/eventTypes";
import { useAsyncData } from "../hooks/useAsyncData";

function MetricCard({ value, label }: { value: number; label: string }) {
  return (
    <div className="metric-card">
      <Text className="metric-value">{value}</Text>
      <Text c="dimmed">{label}</Text>
    </div>
  );
}

export function StatsPage() {
  const { data } = useAsyncData(getEventStats, []);

  return (
    <Stack gap="lg">
      <PageHeader
        title="Статистика"
        subtitle="Сводные показатели корпуса: число событий, доля проверенных записей, распределение по типам, периодам и годам."
      />
      <SimpleGrid cols={{ base: 1, md: 3 }}>
        <MetricCard value={data?.total_events || 0} label="Всего событий" />
        <MetricCard value={data?.reviewed_events || 0} label="Проверено вручную" />
        <MetricCard value={data?.without_coordinates || 0} label="Без координат" />
      </SimpleGrid>
      <Grid>
        <Grid.Col span={{ base: 12, xl: 4 }}>
          <StatsBars title="По типам" items={data?.by_type || []} labelFormatter={formatEventTypeLabel} />
        </Grid.Col>
        <Grid.Col span={{ base: 12, xl: 4 }}>
          <StatsBars title="По периодам" items={data?.by_period || []} />
        </Grid.Col>
        <Grid.Col span={{ base: 12, xl: 4 }}>
          <StatsBars title="По годам" items={data?.by_year || []} />
        </Grid.Col>
      </Grid>
    </Stack>
  );
}
