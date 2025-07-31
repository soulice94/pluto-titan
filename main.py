from ollama import generate
from ollama import GenerateResponse
import pymupdf

def main():
    try:
        doc = pymupdf.open("edc.pdf")
        auth_status = doc.authenticate("a")
        print("Authentication status:", auth_status)
        pdf_text_content = ''
        page_number = 1
        for page in doc:
            print('Page number:', page_number)
            text = page.get_text()
            # print(text)
            if page_number == 3 or page_number == 4:
                pdf_text_content += text
            page_number += 1
        doc.close()
        generated: GenerateResponse = generate(
            model="deepseek-r1:14b",
            prompt=("In the next text, after 'Listado de transacciones' extract all"
                    "the transactions and their details, the fields should be 'Concepto' (concept of the transaction),)"
                    "monto (amount of the transaction), when you have this extract, group by 'Concepto' and sum the 'monto'"
                    "for each 'Concepto'. As a result, just return each 'Concepto' with its total 'monto' and nothing else. ") + pdf_text_content,
        )
        print(generated.response)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
