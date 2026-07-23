import json

import pytest

from scripts.chunk_text import (
    build_chunk_records,
    chunk_text_file,
    clean_text,
    split_text,
)

def test_clean_text_removes_extra_blank_lines():
    text = "hello\n\n\n\nworld    test"
    cleaned = clean_text(text)

    assert cleaned == "hello\n\nworld test"

def test_split_text_with_overlap():
    text = "abcdefghij"

    chunks = split_text(text, chunk_size=4, chunk_overlap=1)

    assert chunks == ["abcd", "defg", "ghij"]

def test_split_empty_text_returns_empty_list():
    chunks = split_text("  ", chunk_size=4, chunk_overlap=1)

    assert chunks == []

def test_split_text_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        split_text("hello world",chunk_size=5, chunk_overlap=5)

def test_build_chunk_records():
    text = "abcdefghij"

    records = build_chunk_records(
        text=text,
        source_file="sample.txt",
        chunk_size=4,
        chunk_overlap=1,
    )

    assert len(records) == 3
    assert records[0]["chunk_id"] == 1
    assert records[0]["source_file"] == "sample.txt"
    assert records[0]["text"] == "abcd"
    assert records[0]["char_count"] == 4

def test_chunk_text_file_saves_json(tmp_path):
    input_path = tmp_path / "sample.txt"
    output_dir = tmp_path / "chunks"

    input_path.write_text("abcdefghij",encoding="utf-8")

    output_path = chunk_text_file(
        input_path=input_path,
        output_dir=output_dir,
        chunk_size=4,
        chunk_overlap=1,
    )

    assert output_path.exists()
    records = json.loads(output_path.read_text(encoding="utf-8"))

    assert len(records) == 3
    assert records[0]["text"] == "abcd"
    assert records[1]["text"] == "defg"
    assert records[2]["text"] == "ghij"

def test_chunk_text_file_missing_input(tmp_path):
    missing_path = tmp_path / "missing.txt"
    output_dir = tmp_path / "chunks"

    with pytest.raises(FileNotFoundError):
        chunk_text_file(
            input_path=missing_path,
            output_dir=output_dir,
            chunk_size=4,
            chunk_overlap=1,
        )

