import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { MantineProvider, createTheme } from "@mantine/core";
import "@mantine/core/styles.css";
import "leaflet/dist/leaflet.css";
import "./styles/global.css";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
import App from "./App";

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

const theme = createTheme({
  colors: {
    gray: ["#ffffff", "#f8f9fb", "#e5e7eb", "#d1d5db", "#9ca3af", "#6b7280", "#4b5563", "#374151", "#1f2937", "#111827"],
    accent: ["#f4efe8", "#ece3d7", "#dfcfbc", "#d1baa0", "#c2a684", "#b29268", "#8b6f47", "#775f3c", "#624f31", "#4e3f27"],
    tide: ["#edf4f5", "#ddebed", "#c6dde0", "#adcdd1", "#8fbabf", "#71a5ab", "#2f5d62", "#284f53", "#213f43", "#1a3134"],
  },
  black: "#1f2937",
  white: "#ffffff",
  primaryColor: "accent",
  primaryShade: 6,
  defaultRadius: "md",
  fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  headings: {
    fontFamily: '"Lora", "Georgia", serif',
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <MantineProvider theme={theme}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </MantineProvider>
  </React.StrictMode>,
);
