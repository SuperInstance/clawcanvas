# clawcanvas

**Programmatic canvas for art and visualization** — shapes, colors, text, and export to SVG/ASCII/JSON. Pure Python, zero dependencies.

## What This Gives You

- **Shapes** — Rectangle, Circle, Line, Triangle, Polygon with fill & stroke
- **Colors** — RGB/alpha, hex parsing, named colors, HSL, blending, linear gradients
- **Text** — built-in 5×7 bitmap font with scaling, alignment, and word wrapping
- **Export** — SVG, ASCII art, and JSON canvas formats
- **Zero dependencies** — dataclasses + stdlib only

## Installation

```bash
pip install clawcanvas
```

## Quick Start

```python
from clawcanvas import Canvas, Color, Rectangle, Circle, Line, SVGExporter

canvas = Canvas(200, 200, background=Color(20, 20, 30))
canvas.add(Rectangle(x=10, y=10, w=80, h=60, fill=Color(255, 80, 80)))
canvas.add(Circle(cx=150, cy=100, radius=40, fill=Color.from_name("skyblue")))
canvas.add(Line(x0=10, y0=180, x1=190, y1=180, stroke=Color(200, 200, 200)))

svg = SVGExporter(pixel_scale=1.0).export(canvas)
```

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## How It Fits

Visualization library for the SuperInstance ecosystem. Used in `dial-space-explorer` for tradition maps and `conservation-art` for generative pieces.

## License

MIT
