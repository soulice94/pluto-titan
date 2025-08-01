from executor import Executor

async def run():
    try:
        prompt  =  ("In the next text in spanish, after 'TRANSACCIONES' extract all "
                    "the transactions and their details, the fields should be 'Merchant' (concept of the transaction), "
                    "monto (amount of the transaction), don't group by 'Merchant', just return all the transactions. "
                    "The transaction have the following format: \n"
                    "Date, example: 12 JUN \n"
                    "Category, example: Gastos de viaje \n"
                    "Store/Merchant, example: Amazon \n"
                    "Amount, example: $100.00 \n"
                    "There's a few negative amounts, you have to avoid add this negative amounts to the final result. "
                    "As a result, just return each 'Merchant' with its total 'amount' and nothing else. "
                    "Finally return the results as a csv format, for the first column use 'Merchant', don't add "
                    "any kind of of formatting for example ** neither the beginning nor the end of the text. "
                    "For the second column just use 'amount'.")
        extractor_params = {
            'file_name': 'pdfs/nu.pdf',
            'pages_to_extract': [3, 4],  # Specify the pages you want to extract
        }

        filter_params = {
            'prompt': prompt
        }

        executor = Executor(extractor_params, filter_params)
        result = await executor.execute()
        return result
    except Exception as e:
        print(f"Error: {e}")