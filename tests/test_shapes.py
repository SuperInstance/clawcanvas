"""Tests for clawcanvas.shapes."""

import pytest
from clawcanvas.color import Color
from clawcanvas.shapes import Circle, Line, Polygon, Rectangle, Triangle
from clawcanvas.canvas import Canvas


def _make_grid(w: int = 20, h: int = 20) -> list[list[Color]]:
    bg = Color(255, 255, 255)
    return [[bg for _ in range(w)] for _ in range(h)]


class TestRectangle:
    def test_fill(self):
        grid = _make_grid(10, 10)
        r = Rectangle(x=2, y=2, w=5, h=5, fill=Color(255, 0, 0))
        r.rasterize(grid, 10, 10)
        # Interior pixel should be fill color
        assert grid[4][4] == Color(255, 0, 0)
        assert grid[0][0] == Color(255, 255, 255)  # outside

    def test_stroke(self):
        grid = _make_grid(10, 10)
        r = Rectangle(x=1, y=1, w=5, h=5, stroke=Color(0, 0, 255), stroke_width=1)
        r.rasterize(grid, 10, 10)
        assert grid[1][1] == Color(0, 0, 255)  # top-left corner

    def test_bounding_box(self):
        r = Rectangle(x=5, y=10, w=20, h=30)
        assert r.bounding_box() == (5, 10, 25, 40)

    def test_no_fill_no_stroke(self):
        grid = _make_grid(5, 5)
        r = Rectangle(x=1, y=1, w=3, h=3, fill=None, stroke=None)
        r.rasterize(grid, 5, 5)
        assert all(grid[y][x] == Color(255, 255, 255) for y in range(5) for x in range(5))


class TestCircle:
    def test_fill(self):
        grid = _make_grid(20, 20)
        c = Circle(cx=10, cy=10, radius=5, fill=Color(255, 0, 0))
        c.rasterize(grid, 20, 20)
        assert grid[10][10] == Color(255, 0, 0)  # center

    def test_bounding_box(self):
        c = Circle(cx=10, cy=10, radius=5)
        assert c.bounding_box() == (5, 5, 15, 15)


class TestLine:
    def test_horizontal(self):
        grid = _make_grid(10, 10)
        l = Line(x0=0, y0=5, x1=9, y1=5, stroke=Color(0, 0, 0))
        l.rasterize(grid, 10, 10)
        assert grid[5][0] == Color(0, 0, 0)
        assert grid[5][9] == Color(0, 0, 0)

    def test_diagonal(self):
        grid = _make_grid(10, 10)
        l = Line(x0=0, y0=0, x1=9, y1=9, stroke=Color(255, 0, 0))
        l.rasterize(grid, 10, 10)
        assert grid[0][0] == Color(255, 0, 0)
        assert grid[9][9] == Color(255, 0, 0)

    def test_no_stroke(self):
        grid = _make_grid(5, 5)
        l = Line(x0=0, y0=0, x1=4, y1=4, stroke=None)
        l.rasterize(grid, 5, 5)
        assert all(grid[y][x] == Color(255, 255, 255) for y in range(5) for x in range(5))

    def test_bounding_box(self):
        l = Line(x0=1, y0=2, x1=5, y1=8)
        assert l.bounding_box() == (1, 2, 5, 8)


class TestTriangle:
    def test_fill(self):
        grid = _make_grid(20, 20)
        t = Triangle(x0=5, y0=2, x1=15, y1=2, x2=10, y2=18, fill=Color(0, 255, 0))
        t.rasterize(grid, 20, 20)
        # Interior pixel (not on edge) should be fill
        assert grid[10][10] == Color(0, 255, 0)

    def test_bounding_box(self):
        t = Triangle(x0=1, y0=2, x1=5, y1=10, x2=8, y2=4)
        bb = t.bounding_box()
        assert bb[0] == 1 and bb[1] == 2 and bb[2] == 8 and bb[3] == 10


class TestPolygon:
    def test_fill_square(self):
        grid = _make_grid(10, 10)
        p = Polygon(
            vertices=[(2, 2), (7, 2), (7, 7), (2, 7)],
            fill=Color(100, 100, 100),
        )
        p.rasterize(grid, 10, 10)
        assert grid[4][4] == Color(100, 100, 100)

    def test_bounding_box_empty(self):
        p = Polygon()
        assert p.bounding_box() == (0, 0, 0, 0)

    def test_bounding_box(self):
        p = Polygon(vertices=[(0, 0), (10, 0), (5, 8)])
        bb = p.bounding_box()
        assert bb == (0, 0, 10, 8)

    def test_less_than_3_vertices(self):
        grid = _make_grid(5, 5)
        p = Polygon(vertices=[(0, 0), (2, 2)], fill=Color(0, 0, 0))
        p.rasterize(grid, 5, 5)
        assert all(grid[y][x] == Color(255, 255, 255) for y in range(5) for x in range(5))


class TestIntegration:
    def test_multiple_shapes(self):
        c = Canvas(20, 20, background=Color(0, 0, 0))
        c.add(Rectangle(x=0, y=0, w=20, h=20, fill=Color(0, 0, 0)))
        c.add(Circle(cx=10, cy=10, radius=5, fill=Color(255, 255, 255)))
        grid = c.rasterize()
        assert grid[10][10] == Color(255, 255, 255)
