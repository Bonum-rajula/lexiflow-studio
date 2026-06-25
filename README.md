# LexiFlow Studio

Frontend UI for LexiFlow AI – an autonomous multi‑agent RAG system.

## Setup

1. Clone the repo.
2. Create a conda environment: `conda create -n lexiflow-studio python=3.11`
3. Activate: `conda activate lexiflow-studio`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and set `API_BASE_URL` to your backend URL.
6. Run the app: `streamlit run src/app.py`