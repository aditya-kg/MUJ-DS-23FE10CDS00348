# MUJ NLP Project Repository

## Student information

| Field | Details |
| --- | --- |
| **Name** | Aditya Kumar Guru |
| **Registration Number** | 23FE10CDS00348 |
| **Branch** | Data Science |
| **Batch** | 2023–27 |
| **Section** | E |
| **GitHub Username** | [aditya-kg](https://github.com/aditya-kg) |

## Project title

**Real-Time Query Expansion and Topic Tagging**

## Training program

This repository accompanies training in **Natural Language Processing (NLP)**. Its focus includes conversational language processing, query expansion, named entity recognition, text classification, and the practical stages of building an NLP pipeline. Course assignments, notebooks, learning resources, and presentations can be added to their matching folders as the program progresses.

## Project overview

People often refer to earlier messages with pronouns, omit context, or change topics mid-conversation. This project processes each user turn in a conversation, rewrites context-dependent messages as self-contained queries, and assigns a two-level topic label such as `Politics > India` or `Sports > Cricket`.

The college repository brings together the Streamlit application and the backend research pipeline. The backend contains dataset preparation and deduplication notebooks, classifier training and inference notebooks, generated datasets, model documentation, and a project report.

## Goals and features

- **Context-aware query expansion:** Use recent conversation history to resolve references and ellipsis in a user message.
- **Hierarchical topic tagging:** Predict a broad topic and a more specific subtopic using separate L1 and L2 classifiers.
- **Entity tracking:** Use spaCy named entity recognition to maintain a register of people, places, organizations, and related entities from recent turns.
- **Interruption handling:** Detect short acknowledgements and conversational fillers, and classify them as general messages without unnecessary expansion.
- **Dataset and model workflow:** Generate and annotate conversational examples, merge and deduplicate datasets, fine-tune classifiers, and run the end-to-end inference pipeline.
- **Interactive demo:** Explore the processing flow through a Streamlit application.

## How the pipeline works

1. Keep a sliding window of recent conversation turns.
2. Extract named entities and update the entity register.
3. Detect short interruptions or small talk that do not need query expansion.
4. For other messages, use the conversation context and entity register to rewrite the message as a standalone query. The Streamlit app calls Groq for this step; the backend notebooks also document Hugging Face based inference experiments.
5. Run the expanded query through the two DistilBERT topic classifiers and return the L1 and L2 labels.

## Models and reported results

The backend documentation describes independently fine-tuned DistilBERT sequence classifiers hosted on Hugging Face. The L1 classifier predicts 8 broad domains, and the L2 classifier predicts 19 subtopics. The Streamlit app loads these classifiers from Hugging Face and uses spaCy for named entity recognition.

The model documentation reports the following evaluation results on a 410-example test split:

| Classifier | Accuracy | Macro F1 | Weighted F1 |
| --- | ---: | ---: | ---: |
| L1 topic classifier | 95.85% | 94.07% | 95.97% |
| L2 topic classifier | 94.88% | 94.76% | 94.95% |

These are results reported by the project’s model documentation; see [`MODEL_README.md`](code/backend/topic-classif.-expansion-FULL-Inference_pipeline/MODEL_README.md) for the evaluation details and per-class metrics.

## Dataset and research workflow

The backend notebooks document a multi-stage workflow:

1. Generate synthetic multi-turn conversations and annotations with an LLM.
2. Merge source dataset files and remove duplicate conversations and turns.
3. Fine-tune separate L1 and L2 DistilBERT classifiers.
4. Run the full query expansion and topic classification pipeline.

The backend README reports a merged dataset of 277 conversations and 2,046 user turns. See [`DATASET_README.md`](code/backend/Final-merged-datasets/DATASET_README.md) for dataset fields and processing notes.

## Repository contents

- [`code/frontend/`](code/frontend/) — Streamlit application, configuration, dependencies, and demo image.
- [`code/backend/`](code/backend/) — dataset creation and processing notebooks, datasets, classifier and inference notebooks, recordings, diagrams, and project documentation.
- [`assignments/`](assignments/) — course assignments.
- [`notebooks/`](notebooks/) — course notebooks.
- [`resources/`](resources/) — learning and project resources.
- [`presentations/`](presentations/) — presentation materials.
- [`capstone/`](capstone/) — capstone overview, installation notes, screenshots, and results.

## Source repositories

The project application and backend pipeline in this college repository were copied and organized from these original source repositories. This repository is a separate college submission copy, not a fork or submodule; the source repositories retain their own histories.

- Frontend: [Real-Time-Query_Expansion_amd_Topic-Tagging](https://github.com/aditya-kg/Real-Time-Query_Expansion_amd_Topic-Tagging) → [`code/frontend/`](code/frontend/)
- Backend: [Real-Time-Query_Expansion_amd_Topic-Tagging_backend_pipeline](https://github.com/aditya-kg/Real-Time-Query_Expansion_amd_Topic-Tagging_backend_pipeline) → [`code/backend/`](code/backend/)

## Setup

For the Streamlit app, install its dependencies from the repository root:

```bash
pip install -r code/frontend/requirements.txt
```

Configure `GROQ_API_KEY` and `HF_TOKEN` locally through Streamlit secrets or environment variables, then launch the app:

```bash
streamlit run code/frontend/app.py
```

Never commit real API keys or credentials. For backend notebook dependencies and model setup, see [`code/backend/README.md`](code/backend/README.md), [`capstone/installation.md`](capstone/installation.md), and the notebook-specific documentation.

The frontend README links to the [live Streamlit demo](https://gsdtepaqrm57qwsoqzz4qu.streamlit.app/).

## Academic use

This repository organizes the capstone and related coursework for academic review. Original project files and their existing license are retained where provided. Review the license and dataset documentation in the source folders before reusing or redistributing project materials.
