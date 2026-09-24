import fitz  # PyMuPDF
import sys
import os

pdf_path = "test_broken.pdf"
if not os.path.exists(pdf_path):
    print("PDF not found!")
    sys.exit(1)

doc = fitz.open(pdf_path)
print(f"Total Pages: {len(doc)}")

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    image_list = page.get_images(full=True)
    print(f"\nPage {page_num + 1}:")
    print(f"  Images: {len(image_list)}")
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_w = base_image["width"]
        image_h = base_image["height"]
        print(f"    Image {img_index}: {image_w}x{image_h} ({base_image['ext']})")
