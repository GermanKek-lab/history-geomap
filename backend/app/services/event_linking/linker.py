from __future__ import annotations

from collections import OrderedDict


class EventLinker:
    def deduplicate(self, events: list[dict[str, object]]) -> list[dict[str, object]]:
        unique: OrderedDict[tuple[object, ...], dict[str, object]] = OrderedDict()
        for event in events:
            key = (
                event.get("document_id"),
                event.get("time_raw"),
                event.get("place_name_normalized") or event.get("place_name_raw"),
                event.get("event_type"),
                event.get("action"),
            )
            if key not in unique or float(event.get("confidence", 0.0)) > float(unique[key].get("confidence", 0.0)):
                unique[key] = event
        return list(unique.values())
