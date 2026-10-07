# Installation and setup

## Frontend application

1. Use Python 3.10 or a compatible version, then create and activate a virtual environment.
2. Install the application dependencies:

   ```bash
   pip install -r code/frontend/requirements.txt
   ```

3. Configure required credentials locally. The frontend README documents the expected Groq and Hugging Face values. Keep these in environment variables or `code/frontend/.streamlit/secrets.toml`; do not commit real credentials.
4. Start the app from the repository root:

   ```bash
   streamlit run code/frontend/app.py
   ```

## Backend notebooks

The backend notebooks and their individual setup notes are in [`../code/backend/`](../code/backend/). Install the Python packages listed in the backend README and model documentation. Some notebooks need external API credentials or access to hosted Hugging Face models; configure those locally before running them.

The backend source folder also includes generated datasets, project documentation, and demonstration recordings. Review the dataset README and source repository license before reusing or redistributing those materials.
