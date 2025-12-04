from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List, Protocol

from .domain import (
    CsvFormatContext,
    DestinationFormat,
    JsonFormatContext,
    PlainTextFormatContext,
    StudentRecord,
)


class DestinationWriter(Protocol):
    def supports(self, destination: DestinationFormat) -> bool:
        ...

    def write(
        self, destination: DestinationFormat, records: List[StudentRecord]
    ) -> None:
        ...


class JsonDestinationWriter:
    def supports(self, destination: DestinationFormat) -> bool:
        return isinstance(destination, JsonFormatContext)

    def write(
        self, destination: DestinationFormat, records: List[StudentRecord]
    ) -> None:
        assert isinstance(destination, JsonFormatContext)
        path = Path(destination.path)
        payload = [asdict(record) for record in records]
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=destination.indent)


class CsvDestinationWriter:
    def supports(self, destination: DestinationFormat) -> bool:
        return isinstance(destination, CsvFormatContext)

    def write(
        self, destination: DestinationFormat, records: List[StudentRecord]
    ) -> None:
        assert isinstance(destination, CsvFormatContext)
        path = Path(destination.path)
        fieldnames = [
            "student_id",
            "full_name",
            "group",
            "average_score",
            "credits",
        ]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=fieldnames, delimiter=destination.separator
            )
            writer.writeheader()
            for record in records:
                writer.writerow(asdict(record))


class PlainTextDestinationWriter:
    def supports(self, destination: DestinationFormat) -> bool:
        return isinstance(destination, PlainTextFormatContext)

    def write(
        self, destination: DestinationFormat, records: List[StudentRecord]
    ) -> None:
        assert isinstance(destination, PlainTextFormatContext)
        path = Path(destination.path)
        with path.open("w", encoding="utf-8") as handle:
            for record in records:
                line = (
                    f"{record.full_name} ({record.student_id}) "
                    f"- Group {record.group} - "
                    f"Score {record.average_score:.2f}, Credits {record.credits}"
                )
                handle.write(line + "\n")


class DestinationWriterResolver:
    def __init__(self, writers: Iterable[DestinationWriter]) -> None:
        self._writers = list(writers)

    def resolve(self, destination: DestinationFormat) -> DestinationWriter:
        for writer in self._writers:
            if writer.supports(destination):
                return writer
        raise ValueError(f"No writer registered for {type(destination)!r}")
