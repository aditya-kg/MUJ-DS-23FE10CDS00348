# MUJ NLP Project Repository

**Student:** Aditya Kumar Guru  
**Student ID:** 23FE10CDS00348

This repository is the college submission workspace for an NLP project on real-time query expansion and hierarchical topic tagging. It brings the project application and its backend pipeline together under one repository and provides space for course assignments, notebooks, resources, and presentations.

## Capstone project

The system expands context-dependent user messages into self-contained queries and assigns hierarchical topic labels. The application and backend pipeline are organized under [`code/`](code/); project notes, results, and setup documentation are in [`capstone/`](capstone/).

## Source repositories

The code in this college repository was copied from the following original project repositories and organized here for the course submission. These are source links; this repository is a separate submission copy, not a fork or submodule. The originals remain the source repositories for their respective project histories.

- Frontend application: [Real-Time-Query_Expansion_amd_Topic-Tagging](https://github.com/aditya-kg/Real-Time-Query_Expansion_amd_Topic-Tagging) → [`code/frontend/`](code/frontend/)
- Backend pipeline: [Real-Time-Query_Expansion_amd_Topic-Tagging_backend_pipeline](https://github.com/aditya-kg/Real-Time-Query_Expansion_amd_Topic-Tagging_backend_pipeline) → [`code/backend/`](code/backend/)

## Repository layout

```text
.
├── README.md
├── assignments/
├── notebooks/
├── code/
│   ├── backend/       # Dataset, training, and inference pipeline
│   └── frontend/      # Streamlit application
├── resources/
├── presentations/
├── capstone/
│   ├── README.md
│   ├── screenshots/
│   ├── results/
│   └── installation.md
└── .gitignore
```

## Getting started

See [`capstone/installation.md`](capstone/installation.md) for setup notes. The frontend application has its own dependency file at [`code/frontend/requirements.txt`](code/frontend/requirements.txt). Keep API keys and local credentials out of Git; use environment variables or Streamlit secrets locally.

## Academic use

This repository is intended to organize and present the project for coursework. Original project files and their existing licenses are retained where provided. Please review the license and dataset documentation in the relevant source folders before redistributing their contents.
