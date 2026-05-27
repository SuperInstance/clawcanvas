"""Canvas class — the drawing surface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from clawcanvas.color import Color
from clawcanvas.shapes import Shape


@dataclass
class Canvas:
    """A drawing surface with a pixel grid, background, and shape list."""

    width: int
    height: int
    background: Color = field(default_factory=lambda: Color(255, 255, 255))

    _shapes: list[Shape] = field(default_factory=list, init=False, repr=False)
    _grid: list[list[Color]] | None = field(default=None, init=False, repr=False)

    # --- shape management ---------------------------------------------

    def add(self, shape: Shape) -> None:
        """Add a shape to the canvas."""
        self._shapes.append(shape)

    def remove(self, shape: Shape) -> bool:
        """Remove a shape. Returns True if found."""
        try:
            self._shapes.remove(shape)
            return True
        except ValueError:
            return False

    def clear(self) -> None:
        """Remove all shapes."""
        self._shapes.clear()
        self._grid = None

    @property
    def shapes(self) -> list[Shape]:
        return list(self._shapes)

    # --- pixel grid (rasterizer) --------------------------------------

    def _ensure_grid(self) -> list[list[Color]]:
        if self._grid is None:
            self._grid = [
                [self.background for _ in range(self.width)]
                for _ in range(self.height)
            ]
        return self._grid

    def rasterize(self) -> list[list[Color]]:
        """Rasterize all shapes onto the pixel grid. Returns grid[row][col]."""
        grid = self._ensure_grid()
        # Start fresh each rasterize
        for y in range(self.height):
            for x in range(self.width):
                grid[y][x] = self.background
        for shape in self._shapes:
            shape.rasterize(grid, self.width, self.height)
        return grid

    def get_pixel(self, x: int, y: int) -> Color:
        """Get pixel color at (x, y). Rasterizes if needed."""
        if self._grid is None:
            self.rasterize()
        assert self._grid is not None
        if 0 <= x < self.width and 0 <= y < self.height:
            return self._grid[y][x]
        raise IndexError(f"Pixel ({x}, {y}) out of bounds for {self.width}x{self.height} canvas")

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        """Directly set a pixel color."""
        grid = self._ensure_grid()
        if 0 <= x < self.width and 0 <= y < self.height:
            grid[y][x] = color
        else:
            raise IndexError(f"Pixel ({x}, {y}) out of bounds for {self.width}x{self.height} canvas")

    def __repr__(self) -> str:
        return f"Canvas({self.width}x{self.height}, {len(self._shapes)} shapes)"
