from pypdf import PdfReader
import pdfplumber
from pathlib import Path

class PdfExtractor:
    def __init__(self, input_file_name):
        self.__current_directory = Path.cwd()
        self.__input_pdf_path = self.__current_directory / Path(f"source_pdf/{input_file_name}")

    def clear_files_if_exists(self):
        file_to_rem = Path(self.__current_directory / "source_text/output.txt")
        if file_to_rem.exists():
            file_to_rem.unlink()

    def extractor_w_pypdf(self):
        reader = PdfReader(self.__input_pdf_path)
        number_of_pages = len(reader.pages)

        # save to a text file for later use
        # copy the path where the script and pdf is placed
        with open((self.__current_directory / Path("source_text/output.txt")), "x") as file1:
            for page_num in range(number_of_pages):
                page = reader.pages[page_num]
                text = page.extract_text()        
                file1.writelines(text)
                continue
        file1.close()

    def extractor_w_pdfplumber(self):
        with open((self.__current_directory / Path("source_text/output.txt")), "x") as file1:
            with pdfplumber.open(self.__input_pdf_path) as pdf:
                page_length = len(pdf.pages)
                for page_num in range(page_length):
                    page = pdf.pages[page_num]
                    text = page.extract_text(layout=True)
                    file1.writelines(text)
                    continue
    
    def run(self):
        self.clear_files_if_exists()
        self.extractor_w_pypdf()
        # self.extractor_w_pdfplumber()


pdf = PdfExtractor('input.pdf').run()