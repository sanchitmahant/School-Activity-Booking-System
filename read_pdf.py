import PyPDF2

pdf_path = "CN7021 ASWE 2025-26 Coursework Brief.pdf"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    print(f"Number of pages: {len(reader.pages)}\n")
    print("="*80)
    
    for page_num, page in enumerate(reader.pages, 1):
        print(f"\n--- PAGE {page_num} ---\n")
        text = page.extract_text()
        print(text)
        print("\n" + "="*80)
