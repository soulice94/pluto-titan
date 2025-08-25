from extractor import PDFExtractor
from filter import Filter


class Executor:
    def __init__(self, extractor_params, filter_params):
        self.extractor = PDFExtractor(**extractor_params)
        self.filter_params = filter_params

    async def execute(self):
        extracted_text = self.extractor.extract_text()
        refined_text = await Filter(extracted_text, **self.filter_params).refine()
        return refined_text
