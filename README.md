# ClawCanvas

A canvas/drawing abstraction for programmatic art and visualization. Pure Python, no external dependencies.

## Features

- **Canvas** — pixel grid with configurable size and background color
- **Shapes** — Rectangle, Circle, Line, Triangle, Polygon with fill & stroke
- **Color** — RGB with alpha, hex parsing, named colors, HSL, blending, linear gradients
- **Text** — built-in 5×7 monospace bitmap font with scaling, alignment, and word wrapping
- **Export** — SVG, ASCII art, and JSON canvas formats
- **Zero dependencies** — uses only dataclasses, type hints, and the standard library

## Installation

```bash
pip install clawcanvas
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from clawcanvas import Canvas, Color, Rectangle, Circle, Line, SVGExporter

# Create a canvas
canvas = Canvas(200, 200, background=Color(20, 20, 30))

# Add shapes
canvas.add(Rectangle(x=10, y=10, w=80, h=60, fill=Color(255, 80, 80)))
canvas.add(Circle(cx=150, cy=100, radius=40, fill=Color.from_name("skyblue")))
canvas.add(Line(x0=10, y0=180, x1=190, y1=180, stroke=Color(200, 200, 200)))

# Export to SVG
svg = SVGExporter(pixel_scale=1.0).export(canvas)
print(svg)
```

## Colors

```python
from clawcanvas import Color

# Constructors
c1 = Color(255, 128, 0)                  # RGB
c2 = Color.from_hex("#ff8800")            # Hex string
c3 = Color.from_name("coral")             # Named CSS color
c4 = Color.from_hsl(30, 1.0, 0.5)        # HSL

# Operations
blended = c1.blend(c2, factor=0.5)       # Alpha blend
with_alpha = c1.with_alpha(0.7)           # Set transparency
lum = c1.luminance()                      # Perceived brightness 0-1

# Gradients
from clawcanvas.color import LinearGradient
grad = LinearGradient(0, 0, 100, 0, [
    (0.0, Color(255, 0, 0)),
    (0.5, Color(255, 255, 0)),
    (1.0, Color(0, 255, 0)),
])
mid_color = grad.color_at(0.5)
```

## Text Rendering

```python
from clawcanvas import Canvas, TextRenderer, Color
from clawcanvas.canvas import Canvas

canvas = Canvas(100, 20, background=Color(0, 0, 0))
tr = TextRenderer(scale=2, color=Color(255, 255, 255))
grid = canvas.rasterize()
tr.render(grid, "Hello!", 2, 2, canvas.width, canvas.height)

# Word wrapping
lines = tr.wrap_text("The quick brown fox jumps over the lazy dog", 60)
```

## Export Formats

```python
from clawcanvas import Canvas, SVGExporter, ASCIIExporter, JSONExporter

canvas = Canvas(40, 20)
# ... add shapes ...

# SVG
svg = SVGExporter(pixel_scale=10.0).export(canvas)
SVGExporter().export_to_file(canvas, "output.svg")

# ASCII art
ascii_art = ASCIIExporter().export(canvas)

# JSON (portable canvas format)
json_str = JSONExporter().export(canvas)
JSONExporter().export_to_file(canvas, "output.json")
```

## Running Tests

```bash
python -m pytest tests/ -q
```

## License

MIT
