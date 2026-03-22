import type { ReactNode } from "react";
import { AppShell, Burger, Button, Group, Stack, Text } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link, NavLink, useLocation } from "react-router-dom";

const items = [
  { to: "/", label: "Главная" },
  { to: "/documents", label: "Документы" },
  { to: "/map", label: "Карта" },
  { to: "/review", label: "Проверка" },
  { to: "/stats", label: "Статистика" },
];

type Props = {
  children: ReactNode;
};

export function AppLayout({ children }: Props) {
  const [opened, { toggle }] = useDisclosure(false);
  const location = useLocation();

  const nav = (
    <Stack gap="xs">
      {items.map((item) => (
        <Button
          key={item.to}
          component={NavLink}
          to={item.to}
          variant={location.pathname === item.to ? "filled" : "subtle"}
          color={location.pathname === item.to ? "accent" : "tide"}
          justify="flex-start"
        >
          {item.label}
        </Button>
      ))}
    </Stack>
  );

  return (
    <AppShell
      padding="lg"
      navbar={{ width: 240, breakpoint: "sm", collapsed: { mobile: !opened, desktop: false } }}
      header={{ height: 72 }}
    >
      <AppShell.Header className="header-shell">
        <Group justify="space-between" align="center" h="100%" px="md">
          <Group>
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
            <div>
              <Text component={Link} to="/" className="brand-title">
                GeoAutoMap
              </Text>
              <Text size="xs" c="dimmed">
                Исторические события, карта, ручная проверка
              </Text>
            </div>
          </Group>
          <Button component={Link} to="/map" variant="filled" color="accent">
            Открыть карту
          </Button>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md" className="sidebar-shell">
        {nav}
      </AppShell.Navbar>

      <AppShell.Main>
        <div className="page-shell">{children}</div>
      </AppShell.Main>
    </AppShell>
  );
}
