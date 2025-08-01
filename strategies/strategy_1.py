from executor import Executor

async def run():
    try:
        prompt = ("In the next text, after 'Listado de transacciones' extract all"
                    "the transactions and their details, the fields should be 'Concepto' (concept of the transaction), "
                    "monto (amount of the transaction), don't group by 'Concepto', just return all the transactions. "
                    "As a result, just return each 'Concepto' with its total 'monto' and nothing else."
                    "Finally return the results as a csv format, for the first column use 'Concepto', don't add "
                    "any kind of of formatting for example ** neither the beginning nor the end of the text."
                    "For the second column just use 'monto'.")
        extractor_params = {
            'file_name': 'pdfs/stori.pdf',
            'pages_to_extract': [3, 4],  # Specify the pages you want to extract
            'password': 'a'  # If the PDF is password protected, provide the password here
        }

        filter_params = {
            'prompt': prompt
        }

        executor = Executor(extractor_params, filter_params)
        result = await executor.execute()
        return result
    except Exception as e:
        print(f"Error: {e}")