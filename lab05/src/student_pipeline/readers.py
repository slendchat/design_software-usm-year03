from __future__ import annotations

import json
import random
import string
import urllib.request
from pathlib import Path
from typing import Iterable, List, Protocol

from .domain import (
    FileSourceDefinition,
    HttpSourceDefinition,
    RandomSourceDefinition,
    SourceDefinition,
    StudentRecord,
)


class SourceReader(Protocol):
    def supports(self, source: SourceDefinition) -> bool:
        ...

    def read(self, source: SourceDefinition) -> List[StudentRecord]:
        ...


def _dict_to_record(raw: dict) -> StudentRecord:
    return StudentRecord(
        student_id=str(raw.get("student_id", raw.get("id", "unknown"))),
        full_name=str(raw.get("full_name", raw.get("name", "Unknown Student"))),
        group=str(raw.get("group", raw.get("group_name", "N/A"))),
        average_score=float(raw.get("average_score", raw.get("score", 0.0))),
        credits=int(raw.get("credits", raw.get("credit_count", 0))),
    )


class FileSourceReader:
    def supports(self, source: SourceDefinition) -> bool:
        return isinstance(source, FileSourceDefinition)

    def read(self, source: SourceDefinition) -> List[StudentRecord]:
        assert isinstance(source, FileSourceDefinition)
        path = Path(source.path)
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return [_dict_to_record(item) for item in payload]


class HttpSourceReader:
    def supports(self, source: SourceDefinition) -> bool:
        return isinstance(source, HttpSourceDefinition)

    def read(self, source: SourceDefinition) -> List[StudentRecord]:
        assert isinstance(source, HttpSourceDefinition)
        request = urllib.request.Request(source.url, method="GET")
        with urllib.request.urlopen(request, timeout=source.timeout_seconds) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return [_dict_to_record(item) for item in payload]


class RandomSourceReader:
    def __init__(self) -> None:
        self._random = random.Random()

    def supports(self, source: SourceDefinition) -> bool:
        return isinstance(source, RandomSourceDefinition)

    def read(self, source: SourceDefinition) -> List[StudentRecord]:
        assert isinstance(source, RandomSourceDefinition)
        ret: List[StudentRecord] = []
        for index in range(source.count):
            record = StudentRecord(
                student_id=f"R{index:03}",
                full_name=self._generate_name(),
                group=self._random.choice(["CS-01", "CS-02", "ENG-01", "MATH-99"]),
                average_score=round(self._random.uniform(5.0, 10.0), 2),
                credits=self._random.randint(10, 60),
            )
            ret.append(record)
        return ret

    def _generate_name(self) -> str:
        first = "".join(
            self._random.choice(string.ascii_letters) for _ in range(5)
        ).capitalize()
        last = "".join(
            self._random.choice(string.ascii_letters) for _ in range(7)
        ).capitalize()
        return f"{first} {last}"


class SourceReaderResolver:
    def __init__(self, readers: Iterable[SourceReader]) -> None:
        self._readers = list(readers)

    def resolve(self, source: SourceDefinition) -> SourceReader:
        for reader in self._readers:
            if reader.supports(source):
                return reader
        raise ValueError(f"No reader registered for {type(source)!r}")
