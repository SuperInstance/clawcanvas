"""Tests for clawcanvas.export."""

import json
import pytest
from clawcanvas.canvas import Canvas
from clawcanvas.color import Color
from clawcanvas.shapes import Circle, Line, Rectangle, Triangle, Polygon
from clawcanvas.export import SVGExporter, ASCIIExporter, JSONExporter


def _sample_canvas() -> Canvas:
    c = Canvas(20, 20, background=Color(255, 255, 255))
    c.add(Rectangle(x=2, y=2, w=10, h=10, fill=Color(255, 0, 0), stroke=Color(0, 0, 0)))
    c.add(Circle(cx=15, cy=15, radius=3, fill=Color(0, 0, 255)))
    c.add(Line(x0=0, y0=0, x1=19, y1=19, stroke=Color(0, 0, 0)))
    return c


class TestSVGExporter:
    def test_basic_export(self):
        c = _sample_canvas()
        svg = SVGExporter().export(c)
        assert "<svg" in svg
        assert "</svg>" in svg
        assert "rect" in svg
        assert "circle" in svg
        assert "line" in svg

    def test_background(self):
        c = Canvas(10, 10, background=Color(0, 0, 0))
        svg = SVGExporter().export(c)
        assert "#000000" in svg

    def test_scale(self):
        c = Canvas(10, 10)
        svg = SVGExporter(pixel_scale=20.0).export(c)
        assert 'width="200' in svg

    def test_triangle_export(self):
        c = Canvas(20, 20)
        c.add(Triangle(x0=0, y0=0, x1=10, y1=0, x2=5, y2=10, fill=Color(255, 0, 0)))
        svg = SVGExporter().export(c)
        assert "polygon" in svg

    def test_polygon_export(self):
        c = Canvas(20, 20)
        c.add(Polygon(vertices=[(0, 0), (10, 0), (10, 10), (0, 10)], fill=Color(0, 255, 0)))
        svg = SVGExporter().export(c)
        assert "polygon" in svg

    def test_export_to_file(self, tmp_path):
        c = _sample_canvas()
        path = str(tmp_path / "out.svg")
        SVGExporter().export_to_file(c, path)
        with open(path) as f:
            content = f.read()
        assert "<svg" in content


class TestASCIIExporter:
    def test_basic_export(self):
        c = Canvas(10, 5, background=Color(255, 255, 255))
        c.add(Rectangle(x=2, y=1, w=3, h=2, fill=Color(0, 0, 0)))
        ascii_art = ASCIIExporter().export(c)
        lines = ascii_art.split("\n")
        assert len(lines) == 5
        assert len(lines[0]) == 10

    def test_custom_chars(self):
        c = Canvas(5, 5, background=Color(0, 0, 0))
        result = ASCIIExporter(chars=".X").export(c)
        assert "X" in result

    def test_export_to_file(self, tmp_path):
        c = Canvas(5, 5)
        path = str(tmp_path / "out.txt")
        ASCIIExporter().export_to_file(c, path)
        with open(path) as f:
            assert len(f.read()) > 0


class TestJSONExporter:
    def test_basic_export(self):
        c = _sample_canvas()
        data = json.loads(JSONExporter().export(c))
        assert data["width"] == 20
        assert data["height"] == 20
        assert len(data["shapes"]) == 3
        assert data["background"] == "#ffffff"

    def test_shape_types(self):
        c = _sample_canvas()
        data = json.loads(JSONExporter().export(c))
        types = [s["type"] for s in data["shapes"]]
        assert "rectangle" in types
        assert "circle" in types
        assert "line" in types

    def test_no_fill_serialization(self):
        c = Canvas(10, 10)
        c.add(Rectangle(x=0, y=0, w=5, h=5, fill=None))
        data = json.loads(JSONExporter().export(c))
        assert data["shapes"][0]["fill"] is None

    def test_export_to_file(self, tmp_path):
        c = _sample_canvas()
        path = str(tmp_path / "out.json")
        JSONExporter().export_to_file(c, path)
        with open(path) as f:
            data = json.load(f)
        assert "shapes" in data

    def test_polygon_vertices(self):
        c = Canvas(20, 20)
        verts = [(0, 0), (10, 0), (10, 10)]
        c.add(Polygon(vertices=verts, fill=Color(255, 0, 0)))
        data = json.loads(JSONExporter().export(c))
        assert data["shapes"][0]["vertices"] == [list(v) for v in verts]
