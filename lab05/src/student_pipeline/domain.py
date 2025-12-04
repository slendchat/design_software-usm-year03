from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Set, Union


@dataclass
class StudentRecord:
    student_id: str
    full_name: str
    group: str
    average_score: float
    credits: int


@dataclass
class ScoreFilterParams:
    min_score: float
    max_score: float
    ignored_groups: Set[str] = field(default_factory=set)


@dataclass
class SortParams:
    primary: str = "average_score"
    descending: bool = True
    limit: Optional[int] = None


@dataclass
class TransformationConfig:
    score_filter: Optional[ScoreFilterParams] = None
    sort_and_limit: Optional[SortParams] = None


@dataclass
class FileSourceDefinition:
    path: str


@dataclass
class HttpSourceDefinition:
    url: str
    timeout_seconds: float = 5.0


@dataclass
class RandomSourceDefinition:
    count: int = 10


SourceDefinition = Union[
    FileSourceDefinition,
    HttpSourceDefinition,
    RandomSourceDefinition,
]


@dataclass
class JsonFormatContext:
    path: str
    indent: int = 2


@dataclass
class CsvFormatContext:
    path: str
    separator: str = ","


@dataclass
class PlainTextFormatContext:
    path: str


DestinationFormat = Union[
    JsonFormatContext,
    CsvFormatContext,
    PlainTextFormatContext,
]


@dataclass
class PipelineConfig:
    source: SourceDefinition
    destination: DestinationFormat
    transformations: TransformationConfig = field(
        default_factory=TransformationConfig
    )
