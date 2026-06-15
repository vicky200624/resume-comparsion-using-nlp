#!/usr/bin/env bash

# Start FastAPI in the background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Give the server 10 seconds to load AI models safely
sleep 10

# Start Streamlit and disable strict domain blocking
streamlit run streamlit_app.py --server.port 10000 --server.address 0.0.0.0 --server.enableXsrfProtection false --server.enableCORS false