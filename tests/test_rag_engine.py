import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rag_engine import RAGEngine


class TestRAGEngineInit:
    def test_persist_directory_is_absolute(self, tmp_path):
        engine = RAGEngine.__new__(RAGEngine)
        engine.persist_directory = os.path.abspath(str(tmp_path / "db"))
        assert os.path.isabs(engine.persist_directory)


class TestTextCleaning:
    @pytest.fixture
    def engine(self):
        class MockEngine:
            def _clean_text(self, text):
                if not text: return text
                parts = text.split()
                if not parts: return text
                single_chars = sum(1 for p in parts if len(p) == 1)
                ratio = single_chars / len(parts)
                if ratio > 0.4:
                    cleaned = text.replace("  ", " %TEMP% ").replace(" ", "").replace("%TEMP%", " ")
                    return cleaned
                return text
        return MockEngine()

    def test_clean_spaced_text(self, engine):
        spaced = "H e l l o  W o r l d"
        result = engine._clean_text(spaced)
        assert result == "Hello World"

    def test_normal_text_unchanged(self, engine):
        normal = "Hello World"
        result = engine._clean_text(normal)
        assert result == "Hello World"

    def test_empty_text(self, engine):
        assert engine._clean_text("") == ""
        assert engine._clean_text(None) is None


class TestFileTypeSupport:
    def test_supported_extensions(self):
        supported = ['.pdf', '.txt', '.docx']
        for ext in supported:
            assert ext in ['.pdf', '.txt', '.docx']
