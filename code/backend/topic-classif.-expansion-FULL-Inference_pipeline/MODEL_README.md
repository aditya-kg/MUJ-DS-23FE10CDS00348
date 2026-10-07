# Model — DistilBERT Topic Classifiers

Two fine-tuned DistilBERT classifiers for hierarchical topic classification of conversational queries.

**HuggingFace:**
- L1 classifier → [`Adignite/query-topic-l1-classifier`](https://huggingface.co/Adignite/query-topic-l1-classifier/tree/main)
- L2 classifier → [`Adignite/query-topic-l2-classifier`](https://huggingface.co/Adignite/query-topic-l2-classifier)

---

## Architecture

| Property | Value |
|---|---|
| Base model | `distilbert-base-uncased` |
| Task | Sequence classification |
| Input | `expanded_query` (self-contained rewrite of user message) |
| L1 output | 8 coarse domain classes |
| L2 output | 19 fine-grained sub-topic classes |
| Max input length | 128 tokens |

**Why DistilBERT?** 40% smaller and 60% faster than BERT-base while retaining 97% of its performance. The classification task here (~1,600 training examples, 8–19 classes) does not justify the overhead of RoBERTa or BERT-large. DistilBERT is also better suited to the real-time inference pipeline target.

The two classifiers are trained independently with separate classification heads — L1 optimises for coarse domain boundaries, L2 for fine-grained sub-topic discrimination. A single multi-output model was not used because the two label spaces have different feature requirements.

---

## Training configuration

| Hyperparameter | Value |
|---|---|
| Learning rate | 2e-5 |
| Batch size | 32 |
| Max epochs | 8 |
| Warmup ratio | 0.1 |
| Weight decay | 0.01 |
| Early stopping patience | 3 epochs |
| Best model metric | F1 Weighted |
| Train / test split | 80 / 20 (stratified by L1) |
| Train samples | 1,636 |
| Test samples | 410 |
| Seed | 42 |
| Precision | fp16 (GPU) |

---

## Evaluation results

### L1 Classifier (8 classes)

| Metric | Value |
|---|---|
| Loss | 0.3587 |
| Accuracy | **95.85%** |
| F1 Macro | 94.07% |
| F1 Weighted | **95.97%** |

**Per-class breakdown (test set, n=410):**

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Entertainment | 1.00 | 0.96 | 0.98 | 50 |
| General | 0.68 | 0.94 | 0.79 | 18 |
| Geography | 1.00 | 0.84 | 0.91 | 19 |
| Health | 0.98 | 1.00 | 0.99 | 42 |
| History | 1.00 | 0.90 | 0.95 | 21 |
| Politics | 0.97 | 0.93 | 0.95 | 92 |
| Sports | 0.98 | 0.98 | 0.98 | 90 |
| Technology | 0.96 | 0.99 | 0.97 | 78 |
| **weighted avg** | **0.96** | **0.96** | **0.96** | **410** |

The `General` class has the lowest F1 (0.79) — expected, since it covers small talk and interruptions that share surface-level vocabulary with other domains. Precision is 0.68, meaning some `General` turns are being tagged as domain-specific.

---

### L2 Classifier (19 classes)

| Metric | Value |
|---|---|
| Loss | 0.3731 |
| Accuracy | **94.88%** |
| F1 Macro | 94.76% |
| F1 Weighted | **94.95%** |

**Per-class breakdown (test set, n=410):**

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| AI | 0.93 | 1.00 | 0.97 | 42 |
| Bollywood | 1.00 | 0.96 | 0.98 | 23 |
| Cities | 1.00 | 1.00 | 1.00 | 5 |
| Countries | 0.92 | 0.86 | 0.89 | 14 |
| Cricket | 0.82 | 1.00 | 0.90 | 23 |
| Fitness | 0.95 | 1.00 | 0.97 | 19 |
| Football | 1.00 | 1.00 | 1.00 | 19 |
| Gadgets | 1.00 | 0.90 | 0.95 | 10 |
| General | 0.74 | 0.94 | 0.83 | 18 |
| Hollywood | 1.00 | 0.96 | 0.98 | 27 |
| India | 0.93 | 0.98 | 0.95 | 41 |
| Mental Health | 1.00 | 1.00 | 1.00 | 11 |
| Nutrition | 1.00 | 0.92 | 0.96 | 12 |
| Olympics | 1.00 | 0.80 | 0.89 | 10 |
| Space | 1.00 | 0.96 | 0.98 | 26 |
| Tennis | 1.00 | 0.92 | 0.96 | 38 |
| UK | 1.00 | 0.87 | 0.93 | 15 |
| USA | 0.95 | 0.93 | 0.94 | 41 |
| World Wars | 1.00 | 0.88 | 0.93 | 16 |
| **weighted avg** | **0.95** | **0.95** | **0.95** | **410** |

Strong across the board. The weakest classes are `General` (F1 0.83) and `Cricket` (precision 0.82 — some Cricket turns are pulled toward other Sports sub-topics). `Cities`, `Football`, and `Mental Health` hit perfect F1.

---

## Usage

```python
from transformers import pipeline

clf_l1 = pipeline("text-classification", model="Adignite/query-topic-l1-classifier")
clf_l2 = pipeline("text-classification", model="Adignite/query-topic-l2-classifier")

queries = [
    "who is the prime minister of india?",
    "what are Virat Kohli's achievements in test cricket?",
    "how does OpenAI's GPT model work?",
    "what are the health benefits of yoga?",
    "brb",
]

for q in queries:
    l1 = clf_l1(q)[0]
    l2 = clf_l2(q)[0]
    print(f"{q[:55]:<55}  {l1['label']} ({l1['score']:.2f})  →  {l2['label']} ({l2['score']:.2f})")
```

Example output:
```
who is the prime minister of india?                      Politics (0.97)  →  India (0.95)
what are Virat Kohli's achievements in test cricket?     Sports (0.99)    →  Cricket (0.94)
how does OpenAI's GPT model work?                        Technology (0.98) →  AI (0.96)
what are the health benefits of yoga?                    Health (0.99)    →  Fitness (0.97)
brb                                                      General (0.91)   →  General (0.89)
```

> **Note:** The classifiers are trained on `expanded_query` (self-contained rewrites), not raw user messages. For best results in a conversation context, run the expansion pipeline first and classify the expanded output.

---

## Label maps

### L1
`Entertainment · General · Geography · Health · History · Politics · Sports · Technology`

### L2
`AI · Bollywood · Cities · Countries · Cricket · Fitness · Football · Gadgets · General · Hollywood · India · Mental Health · Nutrition · Olympics · Space · Tennis · UK · USA · World Wars`

---

## Training notebook

See `bert_classifier.ipynb` for the full training code including dataset loading, label encoding, `TopicDataset` class, `Trainer` setup, per-class evaluation, and HuggingFace Hub push.
