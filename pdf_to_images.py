# pyrefly: ignore [missing-import]
import fitz  # PyMuPDF
import sys
import os

pdf_path = "test_fixed.pdf"
out_dir = r"C:\Users\aarya\.gemini\antigravity-ide\brain\502865c1-e33b-4ac2-bf0d-8a3f1108fce8"

if not os.path.exists(pdf_path):
    print(f"PDF not found at {pdf_path}")
    sys.exit(1)

doc = fitz.open(pdf_path)
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    output_filename = os.path.join(out_dir, f"fixed_pdf_page_{page_num + 1}.png")
    pix.save(output_filename)
    print(f"Saved {output_filename}")
