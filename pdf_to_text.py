from pypdf import PdfReader
import pdfplumber
import pdb


from pathlib import Path

# Get the current working directory
current_directory = Path.cwd()
print(f"Current working directory: {current_directory}")

# clean the output directory
file_to_rem = Path(current_directory / "source_text/output.txt")
if file_to_rem.exists():
    file_to_rem.unlink()

# Define a relative path to a file or directory
relative_path = Path("source_pdf/input.pdf")
# Join the current directory with the relative path to create an absolute path
absolute_path = current_directory / relative_path

def extractor_w_pypdf(input_path):
    reader = PdfReader(absolute_path)
    number_of_pages = len(reader.pages)

    # save to a text file for later use
    # copy the path where the script and pdf is placed
    with open((current_directory / Path("source_text/output.txt")), "x") as file1:
        for page_num in range(number_of_pages):
            page = reader.pages[page_num]
            text = page.extract_text()        
            file1.writelines(text)
            continue
    file1.close()

def extractor_w_pdfplumber(input_path):
    with open((current_directory / Path("source_text/output.txt")), "x") as file1:
        with pdfplumber.open(absolute_path) as pdf:
            page_length = len(pdf.pages)
            for page_num in range(page_length):
                page = pdf.pages[page_num]
                text = page.extract_text(layout=True)
                file1.writelines(text)
                continue
    # file1.close()



# extractor_w_pypdf(absolute_path)
extractor_w_pdfplumber(absolute_path)