import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_ui_components_import():
    from ui.components import render_header, render_sidebar
    assert callable(render_header)
    assert callable(render_sidebar)


def test_ui_styles_import():
    from ui.styles import apply_custom_styles, CUSTOM_CSS
    assert callable(apply_custom_styles)
    assert isinstance(CUSTOM_CSS, str)
    assert "<style>" in CUSTOM_CSS
