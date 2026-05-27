"""Shape primitives with fill, stroke, and rasterization."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Sequence

from clawcanvas.color import Color


@dataclass
class Shape(ABC):
    """Abstract base for all shapes."""

    fill: Color | None = None
    stroke: Color | None = Color(0, 0, 0)
    stroke_width: int = 1

    @abstractmethod
    def rasterize(self, grid: list[list[Color]], width: int, height: int) -> None:
        """Draw onto a pixel grid."""
        ...

    @abstractmethod
    def bounding_box(self) -> tuple[float, float, float, float]:
        """Return (x_min, y_min, x_max, y_max)."""
        ...

    def _plot(self, grid: list[list[Color]], x: int, y: int, color: Color, width: int, height: int) -> None:
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = color


@dataclass
class Rectangle(Shape):
    """Axis-aligned rectangle."""

    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    def rasterize(self, grid: list[list[Color]], width: int, height: int) -> None:
        x0, y0 = int(self.x), int(self.y)
        x1, y1 = int(self.x + self.w), int(self.y + self.h)
        # Fill
        if self.fill is not None:
            for y in range(max(0, y0), min(height, y1)):
                for x in range(max(0, x0), min(width, x1)):
                    grid[y][x] = self.fill
        # Stroke (border) — only draw edges, don't overwrite interior fill
        if self.stroke is not None and self.stroke_width > 0:
            sw = self.stroke_width
            # Left & right edges
            for y in range(max(0, y0), min(height, y1)):
                for dx in range(sw):
                    if x0 + dx < width:
                        grid[y][x0 + dx] = self.stroke
                    if x1 - 1 - dx >= 0:
                        grid[y][x1 - 1 - dx] = self.stroke
            # Top & bottom edges (only interior between left/right stroke)
            for x in range(max(0, x0 + sw), min(width, x1 - sw)):
                for dy in range(sw):
                    if y0 + dy < height:
                        grid[y0 + dy][x] = self.stroke
                    if y1 - 1 - dy >= 0:
                        grid[y1 - 1 - dy][x] = self.stroke


@dataclass
class Circle(Shape):
    """Circle defined by center and radius."""

    cx: float = 0
    cy: float = 0
    radius: float = 0

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (
            self.cx - self.radius, self.cy - self.radius,
            self.cx + self.radius, self.cy + self.radius,
        )

    def rasterize(self, grid: list[list[Color]], width: int, height: int) -> None:
        r = self.radius
        r2 = r * r
        x0 = max(0, int(self.cx - r - 1))
        x1 = min(width, int(self.cx + r + 2))
        y0 = max(0, int(self.cy - r - 1))
        y1 = min(height, int(self.cy + r + 2))
        sw = self.stroke_width
        outer_r2 = (r + sw / 2) ** 2
        inner_r2 = (r - sw / 2) ** 2 if self.stroke_width > 0 else outer_r2

        for y in range(y0, y1):
            for x in range(x0, x1):
                dx = x - self.cx
                dy = y - self.cy
                d2 = dx * dx + dy * dy
                if self.fill is not None and d2 <= r2:
                    grid[y][x] = self.fill
                if self.stroke is not None and inner_r2 <= d2 <= outer_r2:
                    grid[y][x] = self.stroke


@dataclass
class Line(Shape):
    """Line from (x0, y0) to (x1, y1)."""

    x0: float = 0
    y0: float = 0
    x1: float = 0
    y1: float = 0

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (min(self.x0, self.x1), min(self.y0, self.y1),
                max(self.x0, self.x1), max(self.y0, self.y1))

    def rasterize(self, grid: list[list[Color]], width: int, height: int) -> None:
        if self.stroke is None:
            return
        # Bresenham's line algorithm
        x0, y0 = int(round(self.x0)), int(round(self.y0))
        x1, y1 = int(round(self.x1)), int(round(self.y1))
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        sw = self.stroke_width
        half = sw // 2

        while True:
            for oy in range(-half, half + 1):
                for ox in range(-half, half + 1):
                    self._plot(grid, x0 + ox, y0 + oy, self.stroke, width, height)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy


@dataclass
class Triangle(Shape):
    """Triangle defined by three vertices."""

    x0: float = 0
    y0: float = 0
    x1: float = 0
    y1: float = 0
    x2: float = 0
    y2: float = 0

    def bounding_box(self) -> tuple[float, float, float, float]:
        xs = [self.x0, self.x1, self.x2]
        ys = [self.y0, self.y1, self.y2]
        return (min(xs), min(ys), max(xs), max(ys))

    def rasterize(self, grid: list[list[Color]], width: int, height: int) -> None:
        # Scanline fill using edge function
        verts = [(self.x0, self.y0), (self.x1, self.y1), (self.x2, self.y2)]
        bb = self.bounding_box()
        ix0, iy0 = max(0, int(bb[0])), max(0, int(bb[1]))
        ix1, iy1 = min(width, int(bb[2]) + 1), min(height, int(bb[3]) + 1)

        def edge(ax: float, ay: float, bx: float, by: float, px: float, py: float) -> float:
            return (bx - ax) * (py - ay) - (by - ay) * (px - ax)

        area = edge(verts[0][0], verts[0][1], verts[1][0], verts[1][1], verts[2][0], verts[2][1])
        if area == 0:
            return

        for y in range(iy0, iy1):
            for x in range(ix0, ix1):
                w0 = edge(verts[1][0], verts[1][1], verts[2][0], verts[2][1], x + 0.5, y + 0.5)
                w1 = edge(verts[2][0], verts[2][1], verts[0][0], verts[0][1], x + 0.5, y + 0.5)
                w2 = edge(verts[0][0], verts[0][1], verts[1][0], verts[1][1], x + 0.5, y + 0.5)
                inside = (w0 >= 0 and w1 >= 0 and w2 >= 0) or (w0 <= 0 and w1 <= 0 and w2 <= 0)
                if inside and self.fill is not None:
                    grid[y][x] = self.fill

        # Stroke edges
        if self.stroke is not None and self.stroke_width > 0:
            Line(x0=self.x0, y0=self.y0, x1=self.x1, y1=self.y1, stroke=self.stroke, stroke_width=self.stroke_width).rasterize(grid, width, height)
            Line(x0=self.x1, y0=self.y1, x1=self.x2, y1=self.y2, stroke=self.stroke, stroke_width=self.stroke_width).rasterize(grid, width, height)
            Line(x0=self.x2, y0=self.y2, x1=self.x0, y1=self.y0, stroke=self.stroke, stroke_width=self.stroke_width).rasterize(grid, width, height)


@dataclass
class Polygon(Shape):
    """Convex or concave polygon from a list of vertices."""

    vertices: list[tuple[float, float]] = field(default_factory=list)

    def bounding_box(self) -> tuple[float, float, float, float]:
        if not self.vertices:
            return (0, 0, 0, 0)
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        return (min(xs), min(ys), max(xs), max(ys))

    def rasterize(self, grid: list[list[Color]], width: int, height: int) -> None:
        n = len(self.vertices)
        if n < 3:
            return

        bb = self.bounding_box()
        ix0, iy0 = max(0, int(bb[0])), max(0, int(bb[1]))
        ix1, iy1 = min(width, int(bb[2]) + 1), min(height, int(bb[3]) + 1)

        # Point-in-polygon using ray casting
        if self.fill is not None:
            for y in range(iy0, iy1):
                for x in range(ix0, ix1):
                    if self._point_in_polygon(x + 0.5, y + 0.5):
                        grid[y][x] = self.fill

        # Stroke edges
        if self.stroke is not None and self.stroke_width > 0:
            for i in range(n):
                x0, y0 = self.vertices[i]
                x1, y1 = self.vertices[(i + 1) % n]
                Line(x0=x0, y0=y0, x1=x1, y1=y1, stroke=self.stroke, stroke_width=self.stroke_width).rasterize(grid, width, height)

    def _point_in_polygon(self, px: float, py: float) -> bool:
        n = len(self.vertices)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]
            if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside
