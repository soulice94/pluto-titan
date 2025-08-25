from executor import Executor


async def run(file_uuid: str):
    try:
        prompt = (
            "In the next text in spanish, after 'FLUJO DE CUENTA' extract all "
            "the transactions and their details, the fields should be 'Merchant' (in the data received is called comercio o comision), "
            "amount (in the data described is called monto en MXN), don't group by 'Merchant', just return all the transactions. "
            "When an amount is negative is a valid transaction, when an amount is positive you should ignore it. "
            "As a result, just return each 'Merchant' with its total 'amount', with amount transform it to a positive value. "
            "Also for the amount don't add the dollar sign at the beginning since is causing noise. "
            "Finally return the results as a csv format, for the first column use 'Merchant', don't add "
            "any kind of of formatting for example ** neither the beginning nor the end of the text. "
            "For the second column just use 'Amount'. Also: the final result should be bare text, dont add any "
            "kind of formatting like adding '```' or any other character, just the text itself."
        )
        extractor_params = {
            "file_name": f"temp_pdfs/{file_uuid}.pdf",
            "pages_to_extract": [3, 4],  # Specify the pages you want to extract
        }

        filter_params = {"prompt": prompt}

        executor = Executor(extractor_params, filter_params)
        result = await executor.execute()
        return result
    except Exception as e:
        print(f"Error: {e}")
