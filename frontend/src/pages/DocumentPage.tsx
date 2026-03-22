import { useState } from "react";
import { useParams } from "react-router-dom";
import { Alert, Badge, Button, Card, Group, Grid, Loader, Stack, Tabs, Text, Textarea } from "@mantine/core";
import { extractDocument, getCsvExportUrl, getDocument, getDocumentEvents, getJsonExportUrl } from "../api/documents";
import { EventTable } from "../components/EventTable";
import { PageHeader } from "../components/PageHeader";
import { TimelineView } from "../components/TimelineView";
import { useAsyncData } from "../hooks/useAsyncData";

export function DocumentPage() {
  const params = useParams();
  const documentId = Number(params.id);
  const [extractMessage, setExtractMessage] = useState<string | null>(null);
  const [extractError, setExtractError] = useState<string | null>(null);
  const [extracting, setExtracting] = useState(false);

  const documentQuery = useAsyncData(() => getDocument(documentId), [documentId]);
  const eventsQuery = useAsyncData(() => getDocumentEvents(documentId), [documentId]);

  const runPipeline = async () => {
    setExtracting(true);
    setExtractMessage(null);
    setExtractError(null);
    try {
      const result = await extractDocument(documentId);
      documentQuery.setData(await getDocument(documentId));
      eventsQuery.setData(await getDocumentEvents(documentId));
      setExtractMessage(`Готово: чанков ${result.chunks_created}, событий ${result.events_created}.`);
    } catch (err) {
      setExtractError(err instanceof Error ? err.message : "Pipeline завершился с ошибкой.");
    } finally {
      setExtracting(false);
    }
  };

  const document = documentQuery.data;
  const events = eventsQuery.data ?? [];

  return (
    <Stack gap="lg">
      <PageHeader
        title={document?.filename || "Документ"}
        subtitle="Исходный текст, кнопка запуска extraction pipeline, таблица событий и timeline для ручной проверки результата."
        action={
          <Group>
            <Button component="a" href={getCsvExportUrl(documentId)} variant="default">
              Экспорт CSV
            </Button>
            <Button component="a" href={getJsonExportUrl(documentId)} variant="default">
              Экспорт JSON
            </Button>
            <Button color="accent" loading={extracting} onClick={runPipeline}>
              Извлечь события
            </Button>
          </Group>
        }
      />

      {documentQuery.loading ? <Loader /> : null}
      {document ? (
        <>
          <Group>
            <Badge color="accent">{document.format}</Badge>
            <Badge color="tide" variant="light">
              {document.processing_status}
            </Badge>
            <Badge color="accent" variant="light">
              Событий: {document.events_count}
            </Badge>
          </Group>

          {extractMessage ? <Alert color="tide">{extractMessage}</Alert> : null}
          {extractError ? <Alert color="accent">{extractError}</Alert> : null}
          {document.last_error ? <Alert color="accent">{document.last_error}</Alert> : null}

          <Tabs defaultValue="text">
            <Tabs.List>
              <Tabs.Tab value="text">Текст</Tabs.Tab>
              <Tabs.Tab value="events">Таблица событий</Tabs.Tab>
              <Tabs.Tab value="timeline">Timeline</Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel value="text" pt="md">
              <Card className="feature-card" radius="lg">
                <Textarea value={document.original_text} readOnly minRows={18} autosize />
              </Card>
            </Tabs.Panel>

            <Tabs.Panel value="events" pt="md">
              <Card className="feature-card" radius="lg">
                <EventTable events={events} />
              </Card>
            </Tabs.Panel>

            <Tabs.Panel value="timeline" pt="md">
              <Grid>
                <Grid.Col span={{ base: 12, lg: 8 }}>
                  <TimelineView events={events} />
                </Grid.Col>
                <Grid.Col span={{ base: 12, lg: 4 }}>
                  <Card className="feature-card" radius="lg">
                    <Stack gap="sm">
                      <Text fw={700}>Сводка документа</Text>
                      <Text size="sm">Чанков: {document.chunks_count}</Text>
                      <Text size="sm">Событий: {events.length}</Text>
                      <Text size="sm">Проверено вручную: {events.filter((event) => event.is_reviewed).length}</Text>
                    </Stack>
                  </Card>
                </Grid.Col>
              </Grid>
            </Tabs.Panel>
          </Tabs>
        </>
      ) : null}
    </Stack>
  );
}
