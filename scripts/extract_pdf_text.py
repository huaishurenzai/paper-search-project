import argparse
from pathlib import Path

import fitz

def extract_text_from_pdf(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found:{pdf_path}")

    text_parts = []

    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc,start=1):
            page_text = page.get_text()
            text_parts.append(f"\n\n=====Page{page_index}=====\n")
            text_parts.append(page_text)

    return "".join(text_parts)

def save_text(text:str,output_path: Path):
    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.write_text(text,encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path",help="Path to the input PDF file.")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output text file.If not provided,save to extracted_texts/{pdf_name}.txt",
    )

    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("extracted_texts") / f"{pdf_path.stem}.txt"

    text = extract_text_from_pdf(pdf_path)
    save_text(text,output_path)

    print(f"Extracted text saved to:{output_path}")

if __name__ == "__main__":
    main()