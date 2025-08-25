from executor import Executor


async def run(file_uuid: str):
    try:
        prompt = (
            "In the next text, after 'Listado de transacciones' extract all"
            "the transactions and their details, the fields should be 'Merchant' (concept of the transaction), "
            "Amount (amount of the transaction), don't group by 'Merchant', just return all the transactions. "
            "As a result, just return each 'Merchant' with its total 'Amount', please don't use '$' at the beginning of the amount and don't group by merchant,"
            "you need to return every transaction."
            "Finally return the results as a csv format, for the first column use 'Merchant', don't add "
            "any kind of of formatting for example ** neither the beginning nor the end of the text."
            "For the second column just use 'Amount'."
        )
        extractor_params = {
            "file_name": f"temp_pdfs/{file_uuid}.pdf",
            "pages_to_extract": [3, 4],  # Specify the pages you want to extract
            "password": "a",  # If the PDF is password protected, provide the password here
        }

        filter_params = {"prompt": prompt}

        executor = Executor(extractor_params, filter_params)
        result = await executor.execute()
        return result
    except Exception as e:
        print(f"Error: {e}")
