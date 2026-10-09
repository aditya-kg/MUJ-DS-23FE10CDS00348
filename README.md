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

## Live demo

[Open the Streamlit app](https://muj-ds-23fe10cds00348.streamlit.app/)

## Training program

This repository accompanies training in **Natural Language Processing (NLP)**. Its focus includes conversational language processing, query expansion, named entity recognition, text classification, and the practical stages of building an NLP pipeline. Course assignments, notebooks, learning resources, and presentations can be added to their matching folders as the program progresses.

## Project overview

**Real-Time Query Expansion and Topic Tagging** is an NLP tool that takes a message from a conversation, uses the surrounding context to rewrite it as a clearer, standalone query, then assigns it a broad topic and a subtopic.

For example, after someone mentions India’s prime minister, the tool could turn **“What are his duties?”** into **“What are Narendra Modi’s duties as Prime Minister of India?”**, then label it **Politics → India**.

The app can also generate a brief reply to each new message using the conversation and the model’s general knowledge. It does not retrieve live information, so answers about current events may be outdated. Query expansion and topic tagging remain the core project features.

The college repository brings together the Streamlit application and the backend research pipeline. The backend contains dataset preparation and deduplication notebooks, classifier training and inference notebooks, generated datasets, model documentation, and a project report. The live app is deployed from this repository.

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

The project application and backend pipeline in this college repository originated in these personal repositories. I copied and organized the relevant project files here as the official college submission; this repository is a separate project copy, not a fork or submodule, and the source repositories retain their own histories.

- Frontend: [Real-Time-Query_Expansion_amd_Topic-Tagging](https://github.com/aditya-kg/Real-Time-Query_Expansion_amd_Topic-Tagging) → [`code/frontend/`](code/frontend/)
- Backend: [Real-Time-Query_Expansion_amd_Topic-Tagging_backend_pipeline](https://github.com/aditya-kg/Real-Time-Query_Expansion_amd_Topic-Tagging_backend_pipeline) → [`code/backend/`](code/backend/)

## Improvements in the college repository

The college version builds on those source projects with an integrated, deployed Streamlit app and project-specific improvements, including:

- Short contextual model replies returned in the same Groq request as query expansion.
- More reliable structured response parsing and a clarification path for ambiguous messages.
- L1/L2 topic consistency, so the subtopic is selected from the predicted topic's valid choices.
- Interruption handling that skips Groq for common fillers while still processing valid short questions.
- Expanded quick inputs and sample conversations across several topics. Sample conversations use their earlier turns as context and process only the final user message.
- A human-conversation evaluation workflow with a schema, split and scoring scripts; downloaded preview data stays local.

The live app uses the frontend in this repository, while the backend datasets, notebooks, and evaluation materials remain available for the college project and further development.

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

The app is deployed at [muj-ds-23fe10cds00348.streamlit.app](https://muj-ds-23fe10cds00348.streamlit.app/).

## Academic use

This repository organizes the capstone and related coursework for academic review. Original project files and their existing license are retained where provided. Review the license and dataset documentation in the source folders before reusing or redistributing project materials.
