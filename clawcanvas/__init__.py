"""ClawCanvas — a canvas/drawing abstraction for programmatic art and visualization."""

from clawcanvas.canvas import Canvas
from clawcanvas.color import Color, named_colors
from clawcanvas.shapes import Circle, Line, Polygon, Rectangle, Triangle
from clawcanvas.text import TextRenderer
from clawcanvas.export import SVGExporter, ASCIIExporter, JSONExporter

__version__ = "0.1.0"
__all__ = [
    "Canvas",
    "Color",
    "named_colors",
    "Rectangle",
    "Circle",
    "Line",
    "Triangle",
    "Polygon",
    "TextRenderer",
    "SVGExporter",
    "ASCIIExporter",
    "JSONExporter",
]
