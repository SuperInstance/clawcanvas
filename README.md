<<<<<<< HEAD
# ClawCanvas — Programmatic Art & Visualization

**A canvas/drawing abstraction for programmatic art, diagrams, and visualization. Pure Python, zero external dependencies.**

## What This Gives You

- **Shape primitives** — Rectangle, Circle, Line, Triangle, Polygon with fill, stroke, and opacity
- **Color system** — RGB/RGBA colors, named colors, gradient support
- **Text rendering** — positioned text with font size and color
- **Canvas compositing** — layer shapes and text on a configurable canvas
- **Multi-format export** — SVG, ASCII art, and JSON output

## Quick Start

```bash
pip install clawcanvas
```

```python
from clawcanvas import Canvas, Color, Rectangle, Circle, Line, TextRenderer
from clawcanvas import SVGExporter, ASCIIExporter

# Create a canvas
canvas = Canvas(width=800, height=600, background=Color(0x1a, 0x1a, 0x2e))

# Draw shapes
canvas.add(Rectangle(x=100, y=100, width=200, height=150, fill=Color(0x00, 0x80, 0xff)))
canvas.add(Circle(cx=400, cy=300, radius=80, fill=Color(0xff, 0x00, 0x80), opacity=0.7))
canvas.add(Line(x1=0, y1=0, x2=800, y2=600, stroke=Color(0xff, 0xff, 0xff)))

# Add text
renderer = TextRenderer()
canvas.add(renderer.render("Fleet Dashboard", x=300, y=50, size=24, color=Color(0xff, 0xff, 0xff)))

# Export
canvas.export(SVGExporter(), "dashboard.svg")
canvas.export(ASCIIExporter(), "dashboard.txt")
```

## API Reference

### Shapes
`Rectangle(x, y, width, height, fill, stroke, opacity)` · `Circle(cx, cy, radius, ...)` · `Line(x1, y1, x2, y2, stroke)` · `Triangle(points, ...)` · `Polygon(points, ...)`

### `Canvas(width, height, background)`
`add(shape)` · `export(exporter, path)`

### `Color(r, g, b, a=255)` / `named_colors`
### `TextRenderer` — `render(text, x, y, size, color)`
### Exporters — `SVGExporter`, `ASCIIExporter`, `JSONExporter`

## How It Fits

The visualization tool for the [SuperInstance fleet](https://github.com/SuperInstance). Used for fleet dashboards, architecture diagrams, and agent-generated art.

- **[cocapn-benchmark](https://github.com/SuperInstance/cocapn-benchmark)** — Uses ClawCanvas for performance charts
- **[agent-grid](https://github.com/SuperInstance/agent-grid)** — Grid interface visualization
- **[ccc-os](https://github.com/SuperInstance/ccc-os)** — Fleet monitoring dashboards

## Testing

```bash
pytest tests/
```
=======
# clawcanvas

**Programmatic canvas for art and visualization** — shapes, colors, text, and export to SVG/ASCII/JSON. Pure Python, zero dependencies.

## What This Gives You

- **Shapes** — Rectangle, Circle, Line, Triangle, Polygon with fill & stroke
- **Colors** — RGB/alpha, hex parsing, named colors, HSL, blending, linear gradients
- **Text** — built-in 5×7 bitmap font with scaling, alignment, and word wrapping
- **Export** — SVG, ASCII art, and JSON canvas formats
- **Zero dependencies** — dataclasses + stdlib only
>>>>>>> 53235cb628037d5b45eac6b4849f21a15d8ad085

## Installation

```bash
pip install clawcanvas
```

<<<<<<< HEAD
Python 3.10+. MIT license.
=======
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
>>>>>>> 53235cb628037d5b45eac6b4849f21a15d8ad085
