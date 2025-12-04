from __future__ import annotations

from typing import List

from .domain import PipelineConfig, TransformationConfig
from .readers import SourceReaderResolver
from .transforms import FilterTransform, RecordTransform, SortTransform
from .writers import DestinationWriterResolver


class TransformationBuilder:
    def build(self, config: TransformationConfig) -> List[RecordTransform]:
        transforms: List[RecordTransform] = []
        if config.score_filter:
            transforms.append(FilterTransform(config.score_filter))
        if config.sort_and_limit:
            transforms.append(SortTransform(config.sort_and_limit))
        return transforms


class StudentPipelineService:
    def __init__(
        self,
        reader_resolver: SourceReaderResolver,
        writer_resolver: DestinationWriterResolver,
        transformation_builder: TransformationBuilder,
    ) -> None:
        self._reader_resolver = reader_resolver
        self._writer_resolver = writer_resolver
        self._transformation_builder = transformation_builder

    def execute(self, config: PipelineConfig) -> List[str]:
        reader = self._reader_resolver.resolve(config.source)
        records = reader.read(config.source)

        steps = self._transformation_builder.build(config.transformations)
        for transform in steps:
            records = transform.apply(records)

        writer = self._writer_resolver.resolve(config.destination)
        writer.write(config.destination, records)
        return [
            f"Loaded {len(records)} records.",
            f"Written output with {writer.__class__.__name__}.",
        ]
