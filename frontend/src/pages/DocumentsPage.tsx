import { Grid, Stack } from "@mantine/core";
import { listDocuments } from "../api/documents";
import { DocumentCard } from "../components/DocumentCard";
import { PageHeader } from "../components/PageHeader";
import { useAsyncData } from "../hooks/useAsyncData";

export function DocumentsPage() {
  const { data, loading } = useAsyncData(listDocuments, []);
  const documents = data ?? [];

  return (
    <Stack>
      <PageHeader
        title="Документы"
        subtitle="Список загруженных источников с состоянием pipeline, количеством чанков и найденных событий."
      />
      <Grid>
        {documents.map((document) => (
          <Grid.Col key={document.id} span={{ base: 12, md: 6, xl: 4 }}>
            <DocumentCard document={document} />
          </Grid.Col>
        ))}
      </Grid>
      {!loading && !data?.length ? <div>Документов пока нет.</div> : null}
    </Stack>
  );
}
