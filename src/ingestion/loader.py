import os, re, json
from pypdf import PdfReader
from pathlib import Path
path = os.path.join(os.getcwd(), "data", "raw")
output_dir = os.path.join(os.getcwd(), "data", "processed")
def get_pdfs(path = path):
    files = list()
    if os.path.isdir(path):
        for f in os.listdir(path):
            if f.endswith(".pdf"):
                filepath = os.path.join(path,f)
                files.append(filepath)

        return files
    else : return []

def clean_pdf_text(raw_text: str) -> str:
    """Clean extracted PDF text"""
    
    # Step 1: Remove extra whitespace and newlines
    text = re.sub(r'\n\s*\n', '\n\n', raw_text)  # Multiple newlines -> double newline
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs -> single space
    
    # Step 2: Remove common PDF artifacts
    text = re.sub(r'-\n\s*', '', text)  # Hyphenated line breaks
    text = re.sub(r'\.\n\s*', '. ', text)  # Periods at line ends
    
    # Step 3: Remove page numbers/headers/footers patterns
    text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\d{1,3}\s*/\s*\d{1,3}', '', text)  # Page ranges
    
    # Step 4: Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\$\$]', ' ', text)
    
    # Step 5: Normalize whitespace again
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
def pdf_processor(pdf_path : str) -> dict:
    try:
        with open(pdf_path,'rb') as f:
            pdf_reader = PdfReader(f)

            #metadata
            metadata = pdf_reader.metadata or {}

            #extract text by page
            pages_text = []
            total_chars = 0

            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text() or ""
                    pages_text.append(text.strip())
                    total_chars += len(text)
                except Exception as e:
                    print(f"Failed to extract page {page_num}")
                    pages_text.append("")
            
            full_text = '\n\n'.join(pages_text)
            cleaned_text = clean_pdf_text(full_text)
            filename = Path(pdf_path).name
            result = {
                'success': True,
                'filename' : filename,
                'text': cleaned_text,
                'raw_length': len(full_text),
                'cleaned_length': len(cleaned_text),
                'num_pages': len(pdf_reader.pages),
                'metadata': dict(metadata)
            }
            
            out_path = os.path.join(output_dir,f"{metadata.title}.json")
            with open(out_path,'w') as f:
                json.dump(result,f,indent=2,ensure_ascii=False)
                print(f"Saved processed at {out_path}")
            return result
    except Exception as e:
        return {'success' : False,'error': str(e)}

files = get_pdfs()
res = pdf_processor(files[0])

