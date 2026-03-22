import { Card, Stack, Text } from "@mantine/core";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import { formatEventTypeLabel } from "../constants/eventTypes";
import type { GeoJsonFeatureCollection } from "../types/api";

type Props = {
  geojson: GeoJsonFeatureCollection | null;
};

export function MapPanel({ geojson }: Props) {
  const features = geojson?.features ?? [];

  return (
    <Card className="feature-card" padding="sm" radius="lg">
      {features.length ? (
        <MapContainer center={[55.751244, 37.618423]} zoom={5} className="map-container">
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MarkerClusterGroup chunkedLoading>
            {features.map((feature) => (
              <Marker
                key={feature.properties.id}
                position={[feature.geometry.coordinates[1], feature.geometry.coordinates[0]]}
              >
                <Popup>
                  <Stack gap={4}>
                    <Text fw={700}>{feature.properties.place_name_normalized || feature.properties.place_name_raw}</Text>
                    <Text size="sm" c="accent.7">
                      {formatEventTypeLabel(feature.properties.event_type)}
                    </Text>
                    <Text size="sm">{feature.properties.description}</Text>
                    <Text size="xs" c="dimmed">
                      {feature.properties.time_normalized_start || feature.properties.time_raw}
                    </Text>
                  </Stack>
                </Popup>
              </Marker>
            ))}
          </MarkerClusterGroup>
        </MapContainer>
      ) : (
        <Text c="dimmed">События с координатами пока не найдены.</Text>
      )}
    </Card>
  );
}
