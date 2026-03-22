from __future__ import annotations

from geoalchemy2.elements import WKTElement


def make_point(latitude: float | None, longitude: float | None) -> WKTElement | None:
    if latitude is None or longitude is None:
        return None
    return WKTElement(f"POINT({longitude} {latitude})", srid=4326)
