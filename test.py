import os
import pydocx

root_dir = os.path.dirname(__file__)

def filepath(filename):
    return os.path.join(root_dir, filename)    

def docx2html(path):
    return pydocx.Docx2Html(path).parsed

def docx2markdown(path):
    return pydocx.Docx2Markdown(path, True).parsed

def main():
    print docx2markdown("table.docx")

if __name__ == '__main__':
    main()
