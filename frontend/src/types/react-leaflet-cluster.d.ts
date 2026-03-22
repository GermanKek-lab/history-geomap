declare module "react-leaflet-cluster" {
  import type { ReactNode } from "react";

  type Props = {
    children?: ReactNode;
    chunkedLoading?: boolean;
  };

  export default function MarkerClusterGroup(props: Props): JSX.Element;
}
