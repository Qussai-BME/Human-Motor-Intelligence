"""Factual benchmark table, figure, and report asset generation."""

from __future__ import annotations

import csv
from dataclasses import asdict
import html
import json
from pathlib import Path
from typing import Any

from research_core.benchmarks.engine import BenchmarkResult
from research_core.contracts.base import json_safe


class ReportAssetError(RuntimeError):
    """Raised when report assets cannot be generated from a valid benchmark result."""


def _safe_filename(value: str) -> str:
    return "".join(character if character.isalnum() or character in {"-", "_"} else "-" for character in value)


def _summary_rows(result: BenchmarkResult) -> list[dict[str, Any]]:
    return [
        {
            "benchmark_id": result.benchmark_id,
            "protocol_id": result.protocol_id,
            "dataset_id": result.dataset_id,
            "metric_name": result.metric_name,
            "model_id": summary.model_id,
            "subject_count": summary.subject_count,
            "mean": summary.mean,
            "standard_deviation": summary.standard_deviation,
        }
        for summary in result.summaries
    ]


def _markdown_table(rows: list[dict[str, Any]]) -> str:
    header = "| Model | N subjects | Mean | Standard deviation |\n|---|---:|---:|---:|\n"
    lines: list[str] = []
    for row in rows:
        deviation = "" if row["standard_deviation"] is None else f"{row['standard_deviation']:.6g}"
        lines.append(
            f"| `{row['model_id']}` | {row['subject_count']} | {row['mean']:.6g} | {deviation} |\n"
        )
    return header + "".join(lines)


def _latex_table(rows: list[dict[str, Any]], result: BenchmarkResult) -> str:
    lines = [
        "\\begin{table}[htbp]",
        "\\centering",
        f"\\caption{{Subject-level descriptive summary for {result.metric_name} under protocol {result.protocol_id}.}}",
        f"\\label{{tab:{_safe_filename(result.benchmark_id)}}}",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Model & Subjects & Mean & Standard deviation \\\\",
        "\\midrule",
    ]
    for row in rows:
        deviation = "--" if row["standard_deviation"] is None else f"{row['standard_deviation']:.6g}"
        lines.append(f"{row['model_id']} & {row['subject_count']} & {row['mean']:.6g} & {deviation} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}", ""])
    return "\n".join(lines)


def _svg_bar_figure(rows: list[dict[str, Any]], result: BenchmarkResult) -> str:
    """Render a self-contained vector figure without a plotting dependency."""
    if not rows:
        raise ReportAssetError("cannot render a figure without summary rows")
    width, height = 900, 480
    left, right, top, bottom = 110, 40, 55, 100
    plot_width = width - left - right
    plot_height = height - top - bottom
    values = [float(row["mean"]) for row in rows]
    lower = min(0.0, min(values))
    upper = max(values)
    if upper == lower:
        upper = lower + 1.0
    padding = (upper - lower) * 0.08
    lower -= padding
    upper += padding
    scale = plot_height / (upper - lower)
    zero_y = top + (upper - 0.0) * scale
    zero_y = min(top + plot_height, max(top, zero_y))
    bar_slot = plot_width / len(rows)
    bar_width = min(110, bar_slot * 0.55)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{left}" y="28" font-family="Arial, sans-serif" font-size="18" font-weight="700">{html.escape(result.metric_name)} — {html.escape(result.protocol_id)}</text>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#1f2937" stroke-width="1"/>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#1f2937" stroke-width="1"/>',
        f'<line x1="{left}" y1="{zero_y:.2f}" x2="{left + plot_width}" y2="{zero_y:.2f}" stroke="#9ca3af" stroke-width="1" stroke-dasharray="4 4"/>',
    ]
    for tick in range(6):
        value = lower + (upper - lower) * tick / 5
        y = top + (upper - value) * scale
        parts.extend(
            [
                f'<line x1="{left - 6}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="#1f2937" stroke-width="1"/>',
                f'<text x="{left - 12}" y="{y + 4:.2f}" text-anchor="end" font-family="Arial, sans-serif" font-size="12">{value:.4g}</text>',
            ]
        )
    for index, row in enumerate(rows):
        center = left + bar_slot * (index + 0.5)
        value = float(row["mean"])
        value_y = top + (upper - value) * scale
        y = min(value_y, zero_y)
        bar_height = max(1.0, abs(zero_y - value_y))
        parts.extend(
            [
                f'<rect x="{center - bar_width / 2:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" fill="#1d4ed8"/>',
                f'<text x="{center:.2f}" y="{value_y - 8 if value >= 0 else value_y + 18:.2f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">{value:.6g}</text>',
                f'<text x="{center:.2f}" y="{top + plot_height + 24}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">{html.escape(str(row["model_id"]))}</text>',
                f'<text x="{center:.2f}" y="{top + plot_height + 42}" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#4b5563">n={row["subject_count"]}</text>',
            ]
        )
    parts.extend(
        [
            f'<text x="{left + plot_width / 2:.2f}" y="{height - 20}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Model</text>',
            f'<text transform="translate(24 {top + plot_height / 2:.2f}) rotate(-90)" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">{html.escape(result.metric_name)}</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def write_benchmark_assets(result: BenchmarkResult, output_dir: str | Path) -> dict[str, Path]:
    """Write factual assets derived solely from a validated `BenchmarkResult`."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    stem = _safe_filename(result.benchmark_id)
    rows = _summary_rows(result)
    paths = {
        "json": root / f"{stem}.json",
        "csv": root / f"{stem}.csv",
        "markdown": root / f"{stem}.md",
        "latex": root / f"{stem}.tex",
        "svg": root / f"{stem}.svg",
        "caption": root / f"{stem}.caption.txt",
    }
    paths["json"].write_text(
        json.dumps(json_safe(result.to_dict()), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with paths["csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    markdown = "\n".join(
        [
            f"# Benchmark Asset — {result.benchmark_id}",
            "",
            f"**Protocol:** `{result.protocol_id}`  ",
            f"**Dataset:** `{result.dataset_id}`  ",
            f"**Metric:** `{result.metric_name}`",
            "",
            "## Subject-Level Descriptive Summary",
            "",
            _markdown_table(rows),
            "## Comparison Notes",
            "",
            *[f"- {note}" for note in result.comparison_notes],
            "",
            "## Statistics",
            "",
            "```json",
            json.dumps(result.statistics, indent=2, sort_keys=True),
            "```",
            "",
            "> This asset is a factual rendering of registered subject-level values. It does not establish a scientific conclusion without protocol review and appropriate analysis.",
            "",
        ]
    )
    paths["markdown"].write_text(markdown, encoding="utf-8")
    paths["latex"].write_text(_latex_table(rows, result), encoding="utf-8")
    paths["svg"].write_text(_svg_bar_figure(rows, result), encoding="utf-8")
    caption = (
        f"Subject-level descriptive {result.metric_name} values by model for dataset {result.dataset_id} "
        f"under protocol {result.protocol_id}. Bars show the mean across the displayed number of subjects; "
        "the figure does not imply a statistical conclusion."
    )
    paths["caption"].write_text(caption + "\n", encoding="utf-8")
    return paths
