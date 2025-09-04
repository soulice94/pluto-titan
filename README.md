# Pluto Titan: PDF Transaction Extractor API

Pluto Titan is a FastAPI-based service for extracting and classifying transaction data from PDF bank statements using custom strategies and merchant grouping logic.

## Explaining Pluto Titan
I write this backend as part of a proof of concept for the scopes for using LLMS to extract data from bank statements. The idea is to have a backend that can handle different types of bank statements (in this case, credit card statements) and extract the relevant transaction data using AI-powered strategies. For achieve this I use FastAPI for building the API, PyMuPDF for PDF text extraction, and fuzzy matching techniques for merchant classification (but for the final use I don't integrate it but it helps me to introduce me into Data Science). The project is designed to be extensible, allowing for the 
addition of new extraction strategies and customization of prompts for improved accuracy.

## Implementation Details
The implementation of Pluto Titan involves several key components:

1. **FastAPI**: The web framework used to build the API, providing a simple and efficient way to handle HTTP requests and responses.
2. **PyMuPDF**: A library for extracting text from PDF documents, enabling the extraction of transaction data from bank statements.
3. **Ollama**: A local LLM server that allows to run LLMs locally and use them for text extraction and processing.
4. **DeepSeek**: A LLM model for general proposes, in this case I use it for text extraction and processing.
5. **GPT-OSS**: A open-source LLM model that can be used for various text processing tasks.
6. **Fuzzy Matching**: Techniques used to group similar merchants based on their names, improving the accuracy of merchant classification.

The project is structured to allow for easy extension and modification, making it adaptable to different types of bank statements and extraction requirements.

## Creating a new strategy
To create a new strategy for extracting transactions from a different type of bank statement, follow these steps:
1. **Define the Strategy**: Identify the unique characteristics of the bank statement format and determine how to extract the relevant transaction data.
2. **Implement the Strategy**: Create a new Python file in the `strategies/` folder, implementing the extraction logic using PyMuPDF and any necessary text processing techniques.
3. **Integrate with the API**: Update the `executor.py` file to include the new strategy, allowing it to be selected via the API.
4. **Test the Strategy**: Upload sample bank statements and verify that the extraction works as expected.

The most important part is to define the prompts correctly, as they will determine the accuracy of the extraction. You can customize the prompts in the strategy file to better suit the specific format of the bank statement.

## Features
- Upload PDF bank statements and extract transaction data using AI-powered strategies
- Filter and refine extracted data with custom prompts
- Group merchants using fuzzy matching
- Async processing for efficient handling of large files

## Project Structure
- `main.py`: FastAPI app and API endpoints
- `extractor.py`: PDF text extraction logic
- `filter.py`: AI-based filtering and refinement
- `executor.py`: Orchestrates extraction and filtering
- `classifier.py`: Groups merchants using fuzzy matching
- `strategies/`: Contains extraction strategies for different PDF formats
- `temp_pdfs/`: PDF storage folders

## Setup
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or if using uv
   uv pip install -r requirements.txt
   ```
   Additional dependencies (for merchant classification, optional):
   ```bash
   pip install fuzzywuzzy python-levenshtein
   ```
2. **Set Ollama for multi-threading (if using Ollama locally)**
   ```bash
   launchctl setenv OLLAMA_NUM_PARALLEL 4
   ```
3. **Run the API locally**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## About running the project
You need to setup correctly in IPs in the `main.py` file for CORS to work properly. If you don't set it you won't be able to access the API from the Pluto frontend application.

## API Endpoints
### 1. Health Check
- `GET /`
  - Returns a welcome message.

### 2. Upload PDF
- `POST /file/upload/`
  - Uploads a PDF file and returns a UUID for further processing.
  - **Request:** multipart/form-data with file
  - **Response:** `{ "file_name": ..., "file_uuid": ... }`

### 3. Extract Transactions (Filter)
- `POST /file/filter/`
  - Executes a strategy to extract transactions from the uploaded PDF.
  - **Request:** `{ "file_uuid": "...", "strategy": "1" | "2" }`
  - **Response:** `{ "result": ... }`

#### Strategies
- **Strategy 1:** Extracts transactions after 'Listado de transacciones' (pages 3-4) (Plata Card)
- **Strategy 2:** Extracts transactions after 'FLUJO DE CUENTA' (pages 3-4, Spanish, ignores positive amounts) (Stori Card)

### 4. Merchant Classification
- `POST /merchants/classify-simple/`
  - Groups similar merchants using fuzzy matching.
  - **Request:**
    ```json
   	{
		"merchants": [
			"Uber",
			"Uber Eats",
			"Uber Eats 1",
			"La comer",
			"la comer de mexico"
		],
		"similarity_threshold": 0.8
	}
    ```
  - **Response:**
    ```json
    {
        "groups": [
            {
                "group_name": "uber",
                "merchants": [
                    "Uber"
                ],
                "count": 1
            },
            {
                "group_name": "uber eats",
                "merchants": [
                    "Uber Eats",
                    "Uber Eats 1"
                ],
                "count": 2
            },
            {
                "group_name": "la comer",
                "merchants": [
                    "La comer"
                ],
                "count": 1
            },
            {
                "group_name": "la comer de mexico",
                "merchants": [
                    "la comer de mexico"
                ],
                "count": 1
            }
        ],
        "total_groups": 4,
        "total_merchants": 5
    }
    ```

## Customization
- Add new strategies in the `strategies/` folder for different PDF formats / Cards statements.
- Adjust prompts in `filter.py` or strategy files for improved extraction.


