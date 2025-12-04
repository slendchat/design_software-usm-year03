from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol

from .domain import ScoreFilterParams, SortParams, StudentRecord


def filter_by_score(
    records: Iterable[StudentRecord], params: ScoreFilterParams
) -> List[StudentRecord]:
    ret: List[StudentRecord] = []
    ignored = {group.lower() for group in params.ignored_groups}
    for record in records:
        group = record.group.lower()
        if group in ignored:
            continue
        if record.average_score < params.min_score:
            continue
        if record.average_score > params.max_score:
            continue
        ret.append(record)
    return ret


def sort_and_limit(
    records: Iterable[StudentRecord], params: SortParams
) -> List[StudentRecord]:
    key = params.primary
    allowed_keys = {"average_score", "full_name", "credits"}
    if key not in allowed_keys:
        raise ValueError(f"Unsupported sort key {key}")
    sorted_records = sorted(
        records,
        key=lambda rec: getattr(rec, key),
        reverse=params.descending,
    )
    if params.limit is not None:
        return sorted_records[: params.limit]
    return sorted_records


class RecordTransform(Protocol):
    def apply(self, records: List[StudentRecord]) -> List[StudentRecord]:
        ...


@dataclass
class FilterTransform:
    params: ScoreFilterParams

    def apply(self, records: List[StudentRecord]) -> List[StudentRecord]:
        return filter_by_score(records, self.params)


@dataclass
class SortTransform:
    params: SortParams

    def apply(self, records: List[StudentRecord]) -> List[StudentRecord]:
        return sort_and_limit(records, self.params)
