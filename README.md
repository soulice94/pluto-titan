## Run the app locally

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

launchctl setenv OLLAMA_NUM_PARALLEL 4
