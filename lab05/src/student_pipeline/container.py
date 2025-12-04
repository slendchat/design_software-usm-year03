from __future__ import annotations

from typing import Any, Callable, Dict, TypeVar

from .pipeline import StudentPipelineService, TransformationBuilder
from .readers import (
    FileSourceReader,
    HttpSourceReader,
    RandomSourceReader,
    SourceReaderResolver,
)
from .writers import (
    CsvDestinationWriter,
    DestinationWriterResolver,
    JsonDestinationWriter,
    PlainTextDestinationWriter,
)

T = TypeVar("T")


class ServiceContainer:
    def __init__(self) -> None:
        self._factories: Dict[str, Callable[["ServiceContainer"], Any]] = {}
        self._singletons: Dict[str, Any] = {}

    def register_singleton(
        self, key: str, factory: Callable[["ServiceContainer"], T]
    ) -> None:
        self._factories[key] = factory

    def resolve(self, key: str) -> Any:
        if key in self._singletons:
            return self._singletons[key]
        if key not in self._factories:
            raise KeyError(f"Service {key} not registered")
        instance = self._factories[key](self)
        self._singletons[key] = instance
        return instance


def build_default_container() -> ServiceContainer:
    container = ServiceContainer()

    container.register_singleton(
        "file_reader", lambda _: FileSourceReader()
    )
    container.register_singleton(
        "http_reader", lambda _: HttpSourceReader()
    )
    container.register_singleton(
        "random_reader", lambda _: RandomSourceReader()
    )
    container.register_singleton(
        "reader_resolver",
        lambda c: SourceReaderResolver(
            [
                c.resolve("file_reader"),
                c.resolve("http_reader"),
                c.resolve("random_reader"),
            ]
        ),
    )

    container.register_singleton(
        "json_writer", lambda _: JsonDestinationWriter()
    )
    container.register_singleton(
        "csv_writer", lambda _: CsvDestinationWriter()
    )
    container.register_singleton(
        "text_writer", lambda _: PlainTextDestinationWriter()
    )
    container.register_singleton(
        "writer_resolver",
        lambda c: DestinationWriterResolver(
            [
                c.resolve("json_writer"),
                c.resolve("csv_writer"),
                c.resolve("text_writer"),
            ]
        ),
    )

    container.register_singleton(
        "transformation_builder", lambda _: TransformationBuilder()
    )
    container.register_singleton(
        "pipeline_service",
        lambda c: StudentPipelineService(
            reader_resolver=c.resolve("reader_resolver"),
            writer_resolver=c.resolve("writer_resolver"),
            transformation_builder=c.resolve("transformation_builder"),
        ),
    )
    return container
