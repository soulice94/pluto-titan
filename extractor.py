import pymupdf

class PDFExtractor:
    def __init__(self, file_name, pages_to_extract, password=None):
        self.file_name = file_name
        self.pages_to_extract = pages_to_extract
        self.doc = None
        self.password = password

    def open(self):
        self.doc = pymupdf.open(self.file_name)
        if self.password:
            auth_status = self.doc.authenticate(self.password)
            if not auth_status:
                raise ValueError("Authentication failed with the provided password.")
    
    def close(self):
        if self.doc:
            self.doc.close()


    def extract_text(self):
        self.open()
        pdf_text_content = ''
        page_number = 1
        for page in self.doc:
            if page_number in self.pages_to_extract:
                text = page.get_text()
                pdf_text_content += text
            page_number += 1
        self.close()

        return pdf_text_content
