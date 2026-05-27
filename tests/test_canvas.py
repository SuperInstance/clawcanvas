"""Tests for clawcanvas.canvas."""

import pytest
from clawcanvas.canvas import Canvas
from clawcanvas.color import Color
from clawcanvas.shapes import Rectangle, Circle


class TestCanvas:
    def test_create(self):
        c = Canvas(10, 20)
        assert c.width == 10 and c.height == 20
        assert c.background == Color(255, 255, 255)

    def test_create_custom_bg(self):
        c = Canvas(10, 10, background=Color(0, 0, 0))
        assert c.background == Color(0, 0, 0)

    def test_add_shape(self):
        c = Canvas(10, 10)
        r = Rectangle(x=0, y=0, w=5, h=5, fill=Color(255, 0, 0))
        c.add(r)
        assert len(c.shapes) == 1

    def test_remove_shape(self):
        c = Canvas(10, 10)
        r = Rectangle(x=0, y=0, w=5, h=5)
        c.add(r)
        assert c.remove(r)
        assert len(c.shapes) == 0

    def test_remove_missing(self):
        c = Canvas(10, 10)
        r = Rectangle()
        assert not c.remove(r)

    def test_clear(self):
        c = Canvas(10, 10)
        c.add(Rectangle())
        c.clear()
        assert len(c.shapes) == 0

    def test_rasterize_background(self):
        c = Canvas(5, 5, background=Color(100, 100, 100))
        grid = c.rasterize()
        assert all(grid[y][x] == Color(100, 100, 100) for y in range(5) for x in range(5))

    def test_rasterize_fill(self):
        c = Canvas(10, 10, background=Color(0, 0, 0))
        c.add(Rectangle(x=2, y=2, w=3, h=3, fill=Color(255, 255, 255)))
        grid = c.rasterize()
        assert grid[3][3] == Color(255, 255, 255)
        assert grid[0][0] == Color(0, 0, 0)

    def test_get_pixel(self):
        c = Canvas(10, 10)
        c.add(Rectangle(x=0, y=0, w=10, h=10, fill=Color(0, 255, 0)))
        c.rasterize()
        assert c.get_pixel(5, 5) == Color(0, 255, 0)

    def test_get_pixel_out_of_bounds(self):
        c = Canvas(5, 5)
        with pytest.raises(IndexError):
            c.get_pixel(10, 10)

    def test_set_pixel(self):
        c = Canvas(5, 5)
        c.set_pixel(2, 3, Color(255, 0, 0))
        assert c.get_pixel(2, 3) == Color(255, 0, 0)

    def test_set_pixel_out_of_bounds(self):
        c = Canvas(5, 5)
        with pytest.raises(IndexError):
            c.set_pixel(10, 10, Color())

    def test_shapes_copy(self):
        c = Canvas(5, 5)
        c.add(Rectangle())
        shapes = c.shapes
        shapes.clear()
        assert len(c.shapes) == 1  # returned copy, not internal list

    def test_repr(self):
        c = Canvas(10, 20)
        assert "10x20" in repr(c)
