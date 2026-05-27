"""Tests for clawcanvas.text."""

import pytest
from clawcanvas.color import Color
from clawcanvas.text import TextRenderer
from clawcanvas.canvas import Canvas


def _make_grid(w: int = 50, h: int = 20) -> list[list[Color]]:
    bg = Color(0, 0, 0)
    return [[bg for _ in range(w)] for _ in range(h)]


class TestTextRenderer:
    def test_render_single_char(self):
        grid = _make_grid(20, 20)
        tr = TextRenderer(color=Color(255, 255, 255))
        tr.render(grid, "A", 0, 0, 20, 20)
        # Should have some lit pixels
        lit = sum(1 for y in range(20) for x in range(20) if grid[y][x] == Color(255, 255, 255))
        assert lit > 0

    def test_render_space(self):
        grid = _make_grid(20, 20)
        tr = TextRenderer(color=Color(255, 255, 255))
        tr.render(grid, " ", 0, 0, 20, 20)
        # Space has no lit pixels
        lit = sum(1 for y in range(20) for x in range(20) if grid[y][x] == Color(255, 255, 255))
        assert lit == 0

    def test_measure(self):
        tr = TextRenderer(scale=1)
        w, h = tr.measure("Hi")
        assert w > 0 and h > 0

    def test_measure_empty(self):
        tr = TextRenderer()
        assert tr.measure("") == (0, 0)

    def test_measure_multiline(self):
        tr = TextRenderer()
        w, h = tr.measure("AB\nC")
        assert h > TextRenderer.char_height()

    def test_wrap_text(self):
        tr = TextRenderer(scale=1)
        lines = tr.wrap_text("hello world this is a test", 80)
        assert len(lines) >= 1
        for line in lines:
            assert len(line) <= 80 // (TextRenderer.char_width() + 1)

    def test_wrap_long_word(self):
        tr = TextRenderer()
        lines = tr.wrap_text("abcdefghij", 30)
        assert len(lines) >= 1

    def test_scale(self):
        tr1 = TextRenderer(scale=1)
        tr2 = TextRenderer(scale=2)
        w1, h1 = tr1.measure("A")
        w2, h2 = tr2.measure("A")
        assert w2 > w1 and h2 > h1

    def test_alignment(self):
        grid = _make_grid(50, 20)
        tr = TextRenderer(color=Color(255, 255, 255))
        # Should not crash with any alignment
        tr.render(grid, "Hi", 25, 0, 50, 20, align="left")
        tr.render(grid, "Hi", 25, 0, 50, 20, align="center")
        tr.render(grid, "Hi", 25, 0, 50, 20, align="right")

    def test_unknown_char(self):
        grid = _make_grid(20, 20)
        tr = TextRenderer(color=Color(255, 255, 255))
        # Should not crash on unknown char
        tr.render(grid, "\x01", 0, 0, 20, 20)

    def test_char_dimensions(self):
        assert TextRenderer.char_width() == 5
        assert TextRenderer.char_height() == 7
