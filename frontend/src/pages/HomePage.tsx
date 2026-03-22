import { useNavigate } from "react-router-dom";
import { Card, Grid, Group, List, Stack, Text, ThemeIcon } from "@mantine/core";
import { IconMap2, IconRoute2, IconTimeline } from "@tabler/icons-react";
import { UploadPanel } from "../components/UploadPanel";
import { PageHeader } from "../components/PageHeader";
import { useAsyncData } from "../hooks/useAsyncData";
import { getEventStats } from "../api/events";

export function HomePage() {
  const navigate = useNavigate();
  const { data: stats } = useAsyncData(getEventStats, []);

  return (
    <Stack gap="xl">
      <PageHeader
        title="ИИ-карта исторических событий"
        subtitle="GeoAutoMap принимает исторический текст, извлекает события, нормализует время и место, а затем показывает результат в таблице, timeline и на карте."
      />

      <Grid>
        <Grid.Col span={{ base: 12, lg: 7 }}>
          <UploadPanel onUploaded={(document) => navigate(`/documents/${document.id}`)} />
        </Grid.Col>
        <Grid.Col span={{ base: 12, lg: 5 }}>
          <Card className="hero-card" radius="lg" padding="xl">
            <Stack gap="lg">
              <Text className="hero-metric">{stats?.total_events ?? 0}</Text>
              <Text size="sm" c="dimmed">
                уже извлеченных событий в базе. Система рассчитана на хроники, мемуары, описания кампаний и другие исторические источники.
              </Text>
              <List
                spacing="sm"
                icon={
                  <ThemeIcon color="accent" variant="light" radius="xl">
                    <IconMap2 size={16} />
                  </ThemeIcon>
                }
              >
                <List.Item>Парсинг `txt`, `docx`, `md`, `html`, `pdf`</List.Item>
                <List.Item icon={<ThemeIcon color="tide" variant="light" radius="xl"><IconTimeline size={16} /></ThemeIcon>}>
                  Нормализация дат от точной даты до расплывчатых эпох
                </List.Item>
                <List.Item icon={<ThemeIcon color="accent" variant="light" radius="xl"><IconRoute2 size={16} /></ThemeIcon>}>
                  Ручная проверка результата и экспорт в CSV / GeoJSON
                </List.Item>
              </List>
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>
    </Stack>
  );
}
