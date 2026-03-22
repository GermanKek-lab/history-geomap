from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.db.session import SessionLocal  # noqa: E402
from app.services.query_service import QueryService  # noqa: E402


def convert_csv_to_geojson(csv_path: Path, output_path: Path) -> None:
    features: list[dict[str, object]] = []
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            latitude = row.get("latitude")
            longitude = row.get("longitude")
            if not latitude or not longitude:
                continue
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(longitude), float(latitude)],
                    },
                    "properties": row,
                }
            )

    output_path.write_text(json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"GeoJSON сохранен в {output_path}")


def export_document_csv(document_id: int, output_path: Path) -> None:
    with SessionLocal() as session:
        content = QueryService(session).export_document_csv(document_id)
        if content is None:
            raise SystemExit(f"Не найден документ {document_id} или у него нет событий.")
        output_path.write_text(content, encoding="utf-8")
        print(f"CSV сохранен в {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Экспорт CSV и конвертация CSV -> GeoJSON.")
    parser.add_argument("--document-id", type=int, help="ID документа для экспорта CSV из БД.")
    parser.add_argument("--output", type=Path, help="Путь для выходного CSV.")
    parser.add_argument("--from-csv", type=Path, help="Готовый CSV-файл для конвертации в GeoJSON.")
    parser.add_argument("--geojson-output", type=Path, help="Путь для выходного GeoJSON.")
    args = parser.parse_args()

    if args.document_id and args.output:
        export_document_csv(args.document_id, args.output)

    if args.from_csv and args.geojson_output:
        convert_csv_to_geojson(args.from_csv, args.geojson_output)

    if not ((args.document_id and args.output) or (args.from_csv and args.geojson_output)):
        parser.error("Нужно указать либо --document-id + --output, либо --from-csv + --geojson-output.")


if __name__ == "__main__":
    main()
