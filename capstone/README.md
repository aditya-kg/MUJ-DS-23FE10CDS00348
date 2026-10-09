# Capstone: Real-Time Query Expansion and Topic Tagging

This capstone combines the Streamlit frontend and NLP backend pipeline copied from the two source repositories listed in the [root README](../README.md).

## Project summary

The pipeline uses conversation context to expand implicit or abbreviated user queries, then assigns hierarchical topic labels. The project includes dataset preparation, model training and inference notebooks, model and dataset documentation, and the Streamlit application.

## Project contents

- Application: [`../code/frontend/`](../code/frontend/)
- Backend, datasets, notebooks, and pipeline documentation: [`../code/backend/`](../code/backend/)
- Setup notes: [`installation.md`](installation.md)
- Screenshots: [`screenshots/`](screenshots/)
- Results: [`results/`](results/)

The backend repository includes a project document and additional dataset/model documentation. Refer to those files for methodology and detailed results.
# Short conversational replies

The frontend returns a brief reply for new messages. Query expansion and reply generation share one Groq request, with replies limited to three short sentences and 50 words. Interruption messages use a built-in response without calling Groq. Replies use conversation context and general model knowledge; they are not backed by live retrieval.
