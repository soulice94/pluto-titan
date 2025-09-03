# Pluto Titan: PDF Transaction Extractor API

Pluto Titan is a FastAPI-based service for extracting and classifying transaction data from PDF bank statements using custom strategies and merchant grouping logic.

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
- `pdfs/`, `temp_pdfs/`: PDF storage folders

## Setup
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or if using uv
   uv pip install -r requirements.txt
   ```
   Additional dependencies (for merchant classification):
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


