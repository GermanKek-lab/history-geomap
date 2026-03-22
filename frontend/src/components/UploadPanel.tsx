import { useState } from "react";
import { Alert, Button, Card, FileInput, Group, Stack, Tabs, Text, TextInput, Textarea } from "@mantine/core";
import { IconUpload, IconFileText } from "@tabler/icons-react";
import { uploadDocument } from "../api/documents";
import type { DocumentDetail } from "../types/api";

type Props = {
  onUploaded?: (document: DocumentDetail) => void;
};

export function UploadPanel({ onUploaded }: Props) {
  const [mode, setMode] = useState<string>("file");
  const [file, setFile] = useState<File | null>(null);
  const [manualText, setManualText] = useState("");
  const [manualFilename, setManualFilename] = useState("manual_demo.txt");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const created = await uploadDocument({
        file: mode === "file" ? file : undefined,
        manualText: mode === "text" ? manualText : undefined,
        manualFilename: mode === "text" ? manualFilename : undefined,
      });
      setMessage(`Документ «${created.filename}» загружен.`);
      onUploaded?.(created);
      setFile(null);
      if (mode === "text") {
        setManualText("");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось загрузить документ.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="feature-card" padding="lg" radius="lg">
      <Stack>
        <Group justify="space-between">
          <div>
            <Text fw={700}>Загрузка исторического источника</Text>
            <Text c="dimmed" size="sm">
              Поддерживаются `txt`, `docx`, `md`, `html`, `pdf`, а также ручной ввод. Имя документа должно быть уникальным.
            </Text>
          </div>
          <IconUpload size={20} />
        </Group>

        <Tabs value={mode} onChange={(value) => setMode(value || "file")}>
          <Tabs.List>
            <Tabs.Tab value="file">Файл</Tabs.Tab>
            <Tabs.Tab value="text">Вставить текст</Tabs.Tab>
          </Tabs.List>

          <Tabs.Panel value="file" pt="md">
            <Stack>
              <FileInput
                label="Файл источника"
                placeholder="Выберите документ"
                value={file}
                onChange={setFile}
                accept=".txt,.docx,.md,.html,.pdf"
              />
            </Stack>
          </Tabs.Panel>

          <Tabs.Panel value="text" pt="md">
            <Stack>
              <TextInput
                label="Имя документа"
                value={manualFilename}
                onChange={(event) => setManualFilename(event.currentTarget.value)}
                leftSection={<IconFileText size={16} />}
              />
              <Textarea
                label="Исторический текст"
                minRows={10}
                placeholder="Вставьте хронику, мемуар или описание кампании"
                value={manualText}
                onChange={(event) => setManualText(event.currentTarget.value)}
              />
            </Stack>
          </Tabs.Panel>
        </Tabs>

        <Group justify="space-between">
          <Text size="sm" c="dimmed">
            После загрузки документ можно сразу отправить в extraction pipeline.
          </Text>
          <Button loading={loading} onClick={submit} color="accent">
            Загрузить
          </Button>
        </Group>

        {message ? <Alert color="tide">{message}</Alert> : null}
        {error ? <Alert color="accent">{error}</Alert> : null}
      </Stack>
    </Card>
  );
}
