# Dataset — Real-Time Query Expansion & Topic Tagging

Fully synthetic dataset of multi-turn conversations, generated and annotated using the Groq API (`llama-4-scout-17b-16e-instruct` / `llama-3.3-70b-versatile`). No manual annotation was performed.

---

## Files

| File | Description | Rows |
|---|---|---|
| `merged_conversations.csv` | One row per full conversation | 277 |
| `turns_dataset.csv` | One row per user turn — BERT training-ready | 2,046 |

---

## How it was generated

Three separate generation runs (with slightly different prompts and model versions) produced raw CSV files that were merged and deduplicated using `merge_and_dedup.ipynb`.

**Deduplication was done at two levels:**

1. **Conversation level** — each conversation fingerprinted by its first 3 user queries (lowercased). Exact fingerprint matches across runs are collapsed, keeping the version from the highest-priority source.
2. **Turn level** — exact string match on `user_query`, then bigram BLEU ≥ 0.85 within the same topic label to remove near-paraphrase duplicates.

Raw counts: 344 conversations → **277 unique**. Turn-level: 2,770 → **2,046 unique**.

---

## Conversation-level schema (`merged_conversations.csv`)

| Field | Type | Description |
|---|---|---|
| `conversation_id` | string | Unique ID, e.g. `conv_0042_politics_india` |
| `topic_l1` | string | High-level domain label |
| `topic_l2` | string | Sub-domain label |
| `seed_entity` | string | Entity used to seed generation, e.g. `Narendra Modi` |
| `turns` | JSON array | Full 20-message conversation `[{role, text}, ...]` |
| `user_queries` | list[str] | All 10 raw user messages |
| `expanded_queries` | list[str] | Self-contained rewrites of each user turn |
| `named_entities` | list[list] | Entities per user turn (PERSON, GPE, ORG, EVENT) |
| `needs_expansion` | list[bool] | Whether each turn required expansion |
| `created_at` | string | ISO timestamp |

---

## Turn-level schema (`turns_dataset.csv`)

One row per user turn — directly usable for BERT fine-tuning.

| Field | Type | Description |
|---|---|---|
| `conversation_id` | string | Parent conversation ID |
| `topic_l1` | string | Coarse domain |
| `topic_l2` | string | Fine-grained sub-topic |
| `label` | string | Combined label for training, e.g. `Politics_India` |
| `turn_index` | int | Turn number within conversation (1–10) |
| `user_query` | string | Raw user message |
| `expanded_query` | string | Self-contained rewrite — **model input** |
| `named_entities` | JSON list | Named entities in this turn |
| `needs_expansion` | bool | Whether expansion changed the raw query |

---

## Size & splits

| Split | Conversations | User turns |
|---|---|---|
| Train (80%) | 221 | 1,636 |
| Test (20%) | 56 | 410 |
| **Total** | **277** | **2,046** |

The train/test split is stratified by `topic_l1` to preserve class balance.

---

## Label distribution

### L1 (conversations)

| Domain | Conversations |
|---|---|
| Politics | 62 |
| Sports | 62 |
| Technology | 53 |
| Entertainment | 34 |
| Health | 28 |
| History | 14 |
| Geography | 13 |
| General | 11 |

### L2 (turns in `turns_dataset.csv`)

| Label | Turns | | Label | Turns |
|---|---|---|---|---|
| Technology_AI | 201 | | Technology_Gadgets | 69 |
| Politics_India | 179 | | History_World Wars | 67 |
| Politics_USA | 176 | | Health_Mental Health | 59 |
| Sports_Cricket | 156 | | Geography_Countries | 59 |
| Entertainment_Hollywood | 146 | | Health_Nutrition | 58 |
| Sports_Tennis | 145 | | Sports_Olympics | 54 |
| Technology_Space | 120 | | Geography_Cities | 37 |
| Entertainment_Bollywood | 105 | | History_India | 36 |
| Politics_UK | 101 | | | |
| Health_Fitness | 94 | | | |
| Sports_Football | 93 | | **Total** | **2,046** |
| General_General | 91 | | | |

---

## Expansion statistics

Of the 2,046 user turns:

| | Count | % |
|---|---|---|
| Required expansion (`needs_expansion=True`) | 1,619 | 79.1% |
| Already self-contained | 427 | 20.9% |

The high expansion rate reflects the dataset design: conversations intentionally include pronoun references (`his/her/their`), elliptical follow-ups (`what about uk?`), resumptions (`back, so what were we saying?`), and topic switches.

---

## Seed pairs used for generation

34 `(topic_l1, topic_l2, entity)` seeds, repeated across runs to reach the target volume:

| Domain | Entity examples |
|---|---|
| Politics / India | Narendra Modi, Rahul Gandhi, Manmohan Singh |
| Politics / UK | Rishi Sunak, Boris Johnson |
| Politics / USA | Joe Biden, Donald Trump, Barack Obama |
| Sports / Cricket | Virat Kohli, MS Dhoni, Rohit Sharma |
| Sports / Football | Lionel Messi, Cristiano Ronaldo |
| Sports / Tennis | Novak Djokovic, Rafael Nadal |
| Sports / Olympics | Neeraj Chopra |
| Technology / AI | OpenAI, Geoffrey Hinton, Google DeepMind |
| Technology / Space | ISRO, SpaceX |
| Technology / Gadgets | Apple iPhone |
| Entertainment / Bollywood | Shah Rukh Khan, Aamir Khan |
| Entertainment / Hollywood | Christopher Nolan, Marvel Studios |
| Health / Nutrition | Intermittent fasting |
| Health / Mental Health | Anxiety |
| Health / Fitness | Yoga |
| History / India | Mahatma Gandhi |
| History / World Wars | World War II |
| Geography / Countries | India |
| Geography / Cities | Paris |
| General | *(open-ended small talk)* |

---

## Generation prompts summary

**Stage 1** seeds the LLM with topic + entity and requires the conversation to include: direct questions, pronoun references, elliptical follow-ups, at least one interruption (`brb`, `wait`), a resumption, a topic switch, and a multi-entity comparison.

**Stage 2** runs a separate LLM call over the full conversation and outputs a JSON array with one annotation object per user turn, covering `expanded_query`, `topic_l1`, `topic_l2`, `named_entities`, and `needs_expansion`.

**Stage 3** runs automated Python checks (turn count, JSON validity, alternation, label allowlist) and rejects any conversation that fails a single check. Expected pass rate was ~85–90%.
