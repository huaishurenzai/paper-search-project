from pathlib import Path

import pytest

from scripts.extract_pdf_text import extract_text_from_pdf,save_text

def test_extract_text_from_missing_pdf():
    missing_pdf = Path("not_exists.pdf")

    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(missing_pdf)

def test_save_text(tmp_path):
    output_path = tmp_path / "output.txt"

    save_text("hello pdf",output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "hello pdf"