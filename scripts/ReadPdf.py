import os
import glob
from pypdf import PdfReader


def get_pdf_file(file_path: str) -> list:
    """
    Get all PDF files from the specified file path

    Args:
        file_path(str): The directory path containing the PDF files.

    Returns:
        list: A list containing the paths of all the PDF files in the directory.

    """
    pdf_files = []
    try:
        pdf_files = glob.glob(os.path.join(file_path, "*.pdf"))
    except Exception as e:
        print(f"Error getting PDF files from '{file_path}': {str(e)}")
    return pdf_files


def read_multiple_pdf(file_path: str) -> list:
    """
    Read multiple PDF files from the specifies file path and extract the text from each page.

    Args:
        file_path(str): The directory path containing the PDF files.

    Returns:
        list: A list containing the extracted text from each page of the PDF files.
    """
    data = []
    pdf_files = get_pdf_file(file_path)
    for file in pdf_files:
        try:
            with open(file, "rb") as f:
                pdf_reader = PdfReader(f)
                count = len(pdf_reader.pages)
                for i in range(count):
                    page = pdf_reader.pages[i]
                    data.append(page.extract_text())
        except Exception as e:
            print(f"Error Reading file '{file}': {str(e)}")
    return data


def read_single_pdf(file_path: str) -> str:
    """
    Read a single PDF file and extract the text from each page.

    Args:
        file_path(str): The path of the PDF file.

    Returns:
        str: A str containing the extracted text from each page of the PDF file.
    """
    data = []
    try:
        with open(file_path, "rb") as f:
            pdf_reader = PdfReader(f)
            count = len(pdf_reader.pages)
            for i in range(count):
                page = pdf_reader.pages[i]
                data.append(page.extract_text())
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
    return str(" ".join(data))
