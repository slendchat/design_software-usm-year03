from __future__ import annotations

import argparse
import sys
from typing import List

from .container import build_default_container
from .domain import (
    CsvFormatContext,
    FileSourceDefinition,
    HttpSourceDefinition,
    JsonFormatContext,
    PipelineConfig,
    PlainTextFormatContext,
    RandomSourceDefinition,
    ScoreFilterParams,
    SortParams,
    TransformationConfig,
)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Student record processing pipeline"
    )
    parser.add_argument(
        "--source",
        choices=["file", "http", "random"],
        required=True,
        help="Which reader implementation to use.",
    )
    parser.add_argument(
        "--input",
        help="Path or URL for file/http sources.",
    )
    parser.add_argument(
        "--destination",
        choices=["json", "csv", "text"],
        required=True,
        help="Which writer implementation to use.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="File path where the writer should store the result.",
    )
    parser.add_argument("--min-score", type=float, default=0.0)
    parser.add_argument("--max-score", type=float, default=10.0)
    parser.add_argument(
        "--ignored-group",
        action="append",
        default=[],
        help="Group names to skip. Can be provided multiple times.",
    )
    parser.add_argument(
        "--sort-key",
        choices=["average_score", "full_name", "credits"],
        default="average_score",
    )
    parser.add_argument(
        "--ascending", action="store_true", help="Sort ascending instead."
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Maximum number of rows."
    )
    parser.add_argument(
        "--random-count",
        type=int,
        default=10,
        help="How many records to generate when source=random.",
    )
    parser.add_argument(
        "--http-timeout",
        type=float,
        default=5.0,
        help="HTTP timeout when source=http.",
    )
    return parser.parse_args(argv)


def build_source(args: argparse.Namespace):
    if args.source == "file":
        if not args.input:
            raise ValueError("--input is required for file source")
        return FileSourceDefinition(path=args.input)
    if args.source == "http":
        if not args.input:
            raise ValueError("--input is required for http source")
        return HttpSourceDefinition(url=args.input, timeout_seconds=args.http_timeout)
    if args.source == "random":
        return RandomSourceDefinition(count=args.random_count)
    raise ValueError(f"Unknown source {args.source}")


def build_destination(args: argparse.Namespace):
    if args.destination == "json":
        return JsonFormatContext(path=args.output)
    if args.destination == "csv":
        return CsvFormatContext(path=args.output)
    if args.destination == "text":
        return PlainTextFormatContext(path=args.output)
    raise ValueError(f"Unknown destination {args.destination}")


def build_transform_config(args: argparse.Namespace) -> TransformationConfig:
    score_filter = ScoreFilterParams(
        min_score=args.min_score,
        max_score=args.max_score,
        ignored_groups=set(args.ignored_group),
    )
    sort_params = SortParams(
        primary=args.sort_key,
        descending=not args.ascending,
        limit=args.limit,
    )
    return TransformationConfig(
        score_filter=score_filter,
        sort_and_limit=sort_params,
    )


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    source = build_source(args)
    destination = build_destination(args)
    transformations = build_transform_config(args)

    pipeline_config = PipelineConfig(
        source=source,
        destination=destination,
        transformations=transformations,
    )

    container = build_default_container()
    service = container.resolve("pipeline_service")
    logs = service.execute(pipeline_config)
    for entry in logs:
        print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
