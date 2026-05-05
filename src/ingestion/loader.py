from importlib.metadata import PathDistribution
import os
from pypdf import PdfReader
path = os.path.join(os.getcwd(),"data","raw")

def get_pdfs(path = path):
    files = list()
    if os.path.isdir(path):
        for f in os.listdir(path):
            if f.endswith("pdf"):
                filepath = os.path.join(path,f)
                files.append(filepath)

        return files
    else : return []

files = get_pdfs()
print(files)
