from PyPDF2 import PdfReader


def extract_text_from_pdf(file):
    """
    Extracts text from uploaded PDF resume.
    Works for Streamlit upload or FastAPI file input.
    """

    try:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # fallback check
        if not text.strip():
            return " "

        return text

    except Exception as e:
        print("PDF extraction error:", e)
        return " "