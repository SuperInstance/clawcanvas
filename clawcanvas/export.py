"""Exporters: SVG, ASCII art, and JSON canvas format."""

from __future__ import annotations

import json
from typing import Any, TextIO

from clawcanvas.canvas import Canvas
from clawcanvas.shapes import Circle, Line, Polygon, Rectangle, Shape, Triangle
from clawcanvas.color import Color
from clawcanvas.text import TextRenderer


class SVGExporter:
    """Export a Canvas to SVG."""

    def __init__(self, pixel_scale: float = 10.0) -> None:
        self.pixel_scale = pixel_scale

    def export(self, canvas: Canvas) -> str:
        s = self.pixel_scale
        w = canvas.width * s
        h = canvas.height * s
        parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">',
            f'<rect width="{w}" height="{h}" fill="{canvas.background.to_hex()}"/>',
        ]
        for shape in canvas.shapes:
            svg = self._shape_to_svg(shape, s)
            if svg:
                parts.append(svg)
        parts.append("</svg>")
        return "\n".join(parts)

    def _color_attr(self, shape: Shape) -> tuple[str, str]:
        fill = shape.fill.to_hex() if shape.fill else "none"
        stroke = shape.stroke.to_hex() if shape.stroke else "none"
        sw = shape.stroke_width * self.pixel_scale
        return fill, f'{stroke}" stroke-width="{sw}'

    def _shape_to_svg(self, shape: Shape, s: float) -> str:
        fill, stroke_str = self._color_attr(shape)

        if isinstance(shape, Rectangle):
            return (
                f'<rect x="{shape.x * s}" y="{shape.y * s}" '
                f'width="{shape.w * s}" height="{shape.h * s}" '
                f'fill="{fill}" stroke="{stroke_str}"/>'
            )
        elif isinstance(shape, Circle):
            return (
                f'<circle cx="{shape.cx * s}" cy="{shape.cy * s}" r="{shape.radius * s}" '
                f'fill="{fill}" stroke="{stroke_str}"/>'
            )
        elif isinstance(shape, Line):
            return (
                f'<line x1="{shape.x0 * s}" y1="{shape.y0 * s}" '
                f'x2="{shape.x1 * s}" y2="{shape.y1 * s}" '
                f'stroke="{shape.stroke.to_hex() if shape.stroke else "#000"}" '
                f'stroke-width="{shape.stroke_width * s}"/>'
            )
        elif isinstance(shape, Triangle):
            pts = f"{shape.x0*s},{shape.y0*s} {shape.x1*s},{shape.y1*s} {shape.x2*s},{shape.y2*s}"
            return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke_str}"/>'
        elif isinstance(shape, Polygon):
            pts = " ".join(f"{x*s},{y*s}" for x, y in shape.vertices)
            return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke_str}"/>'
        return ""

    def export_to_file(self, canvas: Canvas, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.export(canvas))


# ASCII density ramp from lightest to darkest
_ASCII_RAMP = " .:-=+*#%@"


class ASCIIExporter:
    """Export a Canvas raster to ASCII art."""

    def __init__(self, chars: str | None = None) -> None:
        self.chars = chars or _ASCII_RAMP

    def export(self, canvas: Canvas) -> str:
        grid = canvas.rasterize()
        ramp = self.chars
        lines: list[str] = []
        for row in grid:
            line_chars: list[str] = []
            for color in row:
                lum = color.luminance()
                idx = int((1 - lum) * (len(ramp) - 1))
                idx = max(0, min(len(ramp) - 1, idx))
                line_chars.append(ramp[idx])
            lines.append("".join(line_chars))
        return "\n".join(lines)

    def export_to_file(self, canvas: Canvas, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.export(canvas))


class JSONExporter:
    """Export canvas metadata + shapes to a portable JSON format."""

    def export(self, canvas: Canvas) -> str:
        data: dict[str, Any] = {
            "version": "1.0",
            "width": canvas.width,
            "height": canvas.height,
            "background": canvas.background.to_hex(),
            "shapes": [self._serialize_shape(s) for s in canvas.shapes],
        }
        return json.dumps(data, indent=2)

    def _serialize_shape(self, shape: Shape) -> dict[str, Any]:
        base: dict[str, Any] = {
            "fill": shape.fill.to_hex() if shape.fill else None,
            "stroke": shape.stroke.to_hex() if shape.stroke else None,
            "stroke_width": shape.stroke_width,
        }
        if isinstance(shape, Rectangle):
            base["type"] = "rectangle"
            base["x"], base["y"] = shape.x, shape.y
            base["w"], base["h"] = shape.w, shape.h
        elif isinstance(shape, Circle):
            base["type"] = "circle"
            base["cx"], base["cy"] = shape.cx, shape.cy
            base["radius"] = shape.radius
        elif isinstance(shape, Line):
            base["type"] = "line"
            base["x0"], base["y0"] = shape.x0, shape.y0
            base["x1"], base["y1"] = shape.x1, shape.y1
        elif isinstance(shape, Triangle):
            base["type"] = "triangle"
            base["x0"], base["y0"] = shape.x0, shape.y0
            base["x1"], base["y1"] = shape.x1, shape.y1
            base["x2"], base["y2"] = shape.x2, shape.y2
        elif isinstance(shape, Polygon):
            base["type"] = "polygon"
            base["vertices"] = list(shape.vertices)
        return base

    def export_to_file(self, canvas: Canvas, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.export(canvas))
