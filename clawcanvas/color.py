"""Color representation with RGB, hex, named colors, blending, and gradients."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterator, Sequence

# 140 CSS named colors
NAMED_COLORS: dict[str, tuple[int, int, int]] = {
    "white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0),
    "green": (0, 128, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
    "cyan": (0, 255, 255), "magenta": (255, 0, 255), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "orange": (255, 165, 0), "pink": (255, 192, 203),
    "purple": (128, 0, 128), "brown": (165, 42, 42), "navy": (0, 0, 128),
    "teal": (0, 128, 128), "maroon": (128, 0, 0), "olive": (128, 128, 0),
    "lime": (0, 255, 0), "aqua": (0, 255, 255), "silver": (192, 192, 192),
    "gold": (255, 215, 0), "coral": (255, 127, 80), "salmon": (250, 128, 114),
    "khaki": (240, 230, 140), "violet": (238, 130, 238), "indigo": (75, 0, 130),
    "beige": (245, 245, 220), "ivory": (255, 255, 240), "plum": (221, 160, 221),
    "orchid": (218, 112, 214), "tomato": (255, 99, 71), "turquoise": (64, 224, 208),
    "sienna": (160, 82, 45), "chocolate": (210, 105, 30), "tan": (210, 180, 140),
    "wheat": (245, 222, 179), "linen": (250, 240, 230), "snow": (255, 250, 250),
    "azure": (240, 255, 255), "lavender": (230, 230, 250), "crimson": (220, 20, 60),
    "darkblue": (0, 0, 139), "darkgreen": (0, 100, 0), "darkred": (139, 0, 0),
    "darkgray": (169, 169, 169), "lightgray": (211, 211, 211),
    "darkgrey": (169, 169, 169), "lightgrey": (211, 211, 211),
    "darkcyan": (0, 139, 139), "darkmagenta": (139, 0, 139),
    "darkorange": (255, 140, 0), "darkviolet": (148, 0, 211),
    "lightblue": (173, 216, 230), "lightgreen": (144, 238, 144),
    "lightyellow": (255, 255, 224), "lightpink": (255, 182, 193),
    "lightsalmon": (255, 160, 122), "lightcoral": (240, 128, 128),
    "steelblue": (70, 130, 180), "royalblue": (65, 105, 225),
    "midnightblue": (25, 25, 112), "dodgerblue": (30, 144, 255),
    "skyblue": (135, 206, 235), "deepskyblue": (0, 191, 255),
    "firebrick": (178, 34, 34), "forestgreen": (34, 139, 34),
    "seagreen": (46, 139, 87), "springgreen": (0, 255, 127),
    "hotpink": (255, 105, 180), "deeppink": (255, 20, 147),
    "peru": (205, 133, 63), "rosybrown": (188, 143, 143),
    "slategray": (112, 128, 144), "slategrey": (112, 128, 144),
    "darkslategray": (47, 79, 79), "darkslategrey": (47, 79, 79),
}


def named_colors() -> dict[str, "Color"]:
    """Return a dict of named Color objects."""
    return {name: Color(r, g, b) for name, (r, g, b) in NAMED_COLORS.items()}


def _clamp(v: int) -> int:
    return max(0, min(255, v))


@dataclass(frozen=True, slots=True)
class Color:
    """Immutable RGB color with alpha."""

    r: int = 0
    g: int = 0
    b: int = 0
    a: float = 1.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "r", _clamp(self.r))
        object.__setattr__(self, "g", _clamp(self.g))
        object.__setattr__(self, "b", _clamp(self.b))
        object.__setattr__(self, "a", max(0.0, min(1.0, self.a)))

    # --- constructors --------------------------------------------------

    @classmethod
    def from_hex(cls, hex_str: str) -> Color:
        """Create from '#RRGGBB' or '#RGB' or 'RRGGBB'."""
        h = hex_str.lstrip("#")
        if len(h) == 3:
            h = h[0] * 2 + h[1] * 2 + h[2] * 2
        if len(h) != 6:
            raise ValueError(f"Invalid hex color: {hex_str!r}")
        return cls(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    @classmethod
    def from_name(cls, name: str) -> Color:
        name_lower = name.lower().replace(" ", "")
        if name_lower not in NAMED_COLORS:
            raise ValueError(f"Unknown color name: {name!r}")
        r, g, b = NAMED_COLORS[name_lower]
        return cls(r, g, b)

    @classmethod
    def from_hsl(cls, h: float, s: float, l: float) -> Color:
        """HSL where h in [0,360], s,l in [0,1]."""
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2
        if h < 60:
            r1, g1, b1 = c, x, 0
        elif h < 120:
            r1, g1, b1 = x, c, 0
        elif h < 180:
            r1, g1, b1 = 0, c, x
        elif h < 240:
            r1, g1, b1 = 0, x, c
        elif h < 300:
            r1, g1, b1 = x, 0, c
        else:
            r1, g1, b1 = c, 0, x
        return cls(
            round((r1 + m) * 255),
            round((g1 + m) * 255),
            round((b1 + m) * 255),
        )

    # --- conversions ---------------------------------------------------

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_hex_alpha(self) -> str:
        a_byte = round(self.a * 255)
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{a_byte:02x}"

    def to_rgb_tuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    def to_rgba_tuple(self) -> tuple[int, int, int, float]:
        return (self.r, self.g, self.b, self.a)

    # --- operations ----------------------------------------------------

    def blend(self, other: Color, factor: float = 0.5) -> Color:
        """Alpha-blend with another color. factor=0 → self, factor=1 → other."""
        f = max(0.0, min(1.0, factor))
        return Color(
            round(self.r * (1 - f) + other.r * f),
            round(self.g * (1 - f) + other.g * f),
            round(self.b * (1 - f) + other.b * f),
            self.a * (1 - f) + other.a * f,
        )

    def with_alpha(self, a: float) -> Color:
        return Color(self.r, self.g, self.b, a)

    def luminance(self) -> float:
        """Perceived luminance in [0, 1]."""
        return (0.299 * self.r + 0.587 * self.g + 0.114 * self.b) / 255

    def __repr__(self) -> str:
        if self.a < 1.0:
            return f"Color({self.r}, {self.g}, {self.b}, a={self.a:.2f})"
        return f"Color({self.r}, {self.g}, {self.b})"


class LinearGradient:
    """Multi-stop linear gradient between two points."""

    def __init__(
        self,
        x0: float, y0: float,
        x1: float, y1: float,
        stops: Sequence[tuple[float, Color]],
    ) -> None:
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        # Always sorted by position
        self.stops = sorted(stops, key=lambda s: s[0])
        if not self.stops:
            raise ValueError("Gradient needs at least one stop")

    def color_at(self, t: float) -> Color:
        """Sample color at position t ∈ [0, 1] along the gradient."""
        t = max(0.0, min(1.0, t))
        if len(self.stops) == 1:
            return self.stops[0][1]
        # Find surrounding stops
        for i in range(len(self.stops) - 1):
            t0, c0 = self.stops[i]
            t1, c1 = self.stops[i + 1]
            if t <= t1:
                local = (t - t0) / (t1 - t0) if t1 != t0 else 0.0
                return c0.blend(c1, local)
        return self.stops[-1][1]

    def samples(self, n: int = 10) -> list[Color]:
        """Return n evenly-spaced samples along the gradient."""
        return [self.color_at(i / (n - 1)) for i in range(n)]

    def __repr__(self) -> str:
        return f"LinearGradient(({self.x0},{self.y0})→({self.x1},{self.y1}), {len(self.stops)} stops)"
