"""Tests for clawcanvas.color."""

import pytest
from clawcanvas.color import Color, LinearGradient, NAMED_COLORS, named_colors


class TestColor:
    def test_default(self):
        c = Color()
        assert c.r == 0 and c.g == 0 and c.b == 0 and c.a == 1.0

    def test_clamp(self):
        c = Color(300, -10, 128)
        assert c.r == 255 and c.g == 0 and c.b == 128

    def test_alpha_clamp(self):
        c = Color(0, 0, 0, 2.0)
        assert c.a == 1.0
        c2 = Color(0, 0, 0, -1.0)
        assert c2.a == 0.0

    def test_from_hex_6(self):
        c = Color.from_hex("#FF8800")
        assert c.r == 255 and c.g == 136 and c.b == 0

    def test_from_hex_no_hash(self):
        c = Color.from_hex("FF8800")
        assert c.r == 255 and c.g == 136 and c.b == 0

    def test_from_hex_3(self):
        c = Color.from_hex("#F80")
        assert c.r == 255 and c.g == 136 and c.b == 0

    def test_from_hex_invalid(self):
        with pytest.raises(ValueError):
            Color.from_hex("#ZZ")

    def test_from_name(self):
        c = Color.from_name("red")
        assert c.r == 255 and c.g == 0 and c.b == 0

    def test_from_name_case_insensitive(self):
        c = Color.from_name("RED")
        assert c.r == 255

    def test_from_name_unknown(self):
        with pytest.raises(ValueError):
            Color.from_name("nonexistent")

    def test_from_hsl_red(self):
        c = Color.from_hsl(0, 1.0, 0.5)
        assert c.r == 255 and c.g == 0 and c.b == 0

    def test_from_hsl_green(self):
        c = Color.from_hsl(120, 1.0, 0.5)
        assert c.r == 0 and c.g == 255 and c.b == 0

    def test_to_hex(self):
        c = Color(255, 136, 0)
        assert c.to_hex() == "#ff8800"

    def test_to_hex_alpha(self):
        c = Color(0, 0, 0, 0.5)
        assert c.to_hex_alpha() == "#00000080"

    def test_to_rgb_tuple(self):
        c = Color(10, 20, 30)
        assert c.to_rgb_tuple() == (10, 20, 30)

    def test_blend_equal(self):
        a = Color(0, 0, 0)
        b = Color(255, 255, 255)
        mid = a.blend(b, 0.5)
        assert mid.r == 128 and mid.g == 128 and mid.b == 128

    def test_blend_zero(self):
        a = Color(100, 200, 50)
        b = Color(0, 0, 0)
        result = a.blend(b, 0.0)
        assert result.r == 100 and result.g == 200

    def test_with_alpha(self):
        c = Color(255, 0, 0).with_alpha(0.5)
        assert c.a == 0.5 and c.r == 255

    def test_luminance(self):
        assert Color(255, 255, 255).luminance() == pytest.approx(1.0)
        assert Color(0, 0, 0).luminance() == pytest.approx(0.0)

    def test_frozen(self):
        c = Color(1, 2, 3)
        with pytest.raises(AttributeError):
            c.r = 5  # type: ignore

    def test_repr(self):
        assert "Color(255, 0, 0)" in repr(Color(255, 0, 0))


class TestNamedColors:
    def test_dict_has_common_colors(self):
        nc = named_colors()
        assert "red" in nc
        assert "blue" in nc
        assert isinstance(nc["red"], Color)

    def test_named_colors_count(self):
        assert len(NAMED_COLORS) >= 30


class TestLinearGradient:
    def test_two_stops(self):
        g = LinearGradient(0, 0, 100, 0, [(0.0, Color(0, 0, 0)), (1.0, Color(255, 255, 255))])
        assert g.color_at(0.0) == Color(0, 0, 0)
        assert g.color_at(1.0).r == 255

    def test_samples(self):
        g = LinearGradient(0, 0, 1, 0, [(0.0, Color(0, 0, 0)), (1.0, Color(255, 0, 0))])
        samples = g.samples(5)
        assert len(samples) == 5

    def test_empty_stops_error(self):
        with pytest.raises(ValueError):
            LinearGradient(0, 0, 1, 1, [])

    def test_repr(self):
        g = LinearGradient(0, 0, 1, 1, [(0.0, Color())])
        assert "LinearGradient" in repr(g)
