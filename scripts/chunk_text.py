import argparse
import json
import re
from pathlib import Path

def clean_text(text:str) -> str:
    """
        简单清洗文本：
        1. 统一换行
        2. 去掉过多空白
        3. 保留基本可读性
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def split_text(text:str,chunk_size:int = 500,chunk_overlap:int = 50) -> list[str]:
    """
       按字符长度切分文本，并保留一定 overlap。
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size,len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - chunk_overlap

    return chunks

def build_chunk_records(
        text:str,
        source_file:str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
) -> list[dict]:
    chunks = split_text(
        text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    records = []

    for index, chunk in enumerate(chunks, start=1):
        records.append(
            {
                "chunk_id": index,
                "source_file": source_file,
                "text": chunk,
                "char_count": len(chunk),
            }
        )

    return records

def chunk_text_file(
        input_path:Path,
        output_dir:Path,
        chunk_size:int = 500,
        chunk_overlap:int = 50,
)-> Path:
    if not input_path.exists():
        raise FileNotFoundError(f"Input text file not found:{input_path}")
    text = input_path.read_text(encoding="utf-8")

    records = build_chunk_records(
        text=text,
        source_file=input_path.name,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    output_dir.mkdir(parents=True,exist_ok=True)

    output_path = output_dir / f"{input_path.stem}_chunks.json"

    output_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_path

def main():
    parser = argparse.ArgumentParser(description="Split extraced text into chunks.")
    parser.add_argument("input_path",help="Path to the extracted .txt file.")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="chunks",
        help="Directory to save chunk JSON files."
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Maximum character length of each chunk.",
    )
    parser.add_argument(
        "--chunk_overlap",
        type=int,
        default=50,
        help="Character overlap between adjacent chunks.",
    )

    args = parser.parse_args()

    output_path = chunk_text_file(
        input_path=Path(args.input_path),
        output_dir=Path(args.output_dir),
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )

    print(f"chunks saved to:{output_path}")

if __name__ == "__main__":
    main()