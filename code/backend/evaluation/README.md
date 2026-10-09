# Human conversation evaluation

This folder contains the local workflow for evaluating the NLP pipeline on human-written conversations with human-checked labels. **No human conversation data is included yet.** Do not download or copy a dataset here until its source, license, privacy terms, and intended use have been approved.

## Workflow

1. Obtain approval for the source and terms before adding any records. Prefer consented, de-identified conversations. Do not include names, contact details, account identifiers, or other personal data unless explicitly approved.
2. Annotate complete conversations using [`conversation.schema.json`](conversation.schema.json). Include topic labels and whether a user turn genuinely needs clarification. Record a human reference expansion where a clear expansion is possible.
3. Save one JSON object per conversation in a local `human_conversations.jsonl` file. Keep all turns from a conversation in the same record.
4. Create a deterministic development/held-out split by conversation:

   ```bash
   python code/backend/evaluation/split_conversations.py \
     --input code/backend/evaluation/human_conversations.jsonl \
     --output-dir code/backend/evaluation/splits
   ```

   The split script never separates turns from the same conversation. Use the development split for prompt or threshold changes; reserve `held_out_test.jsonl` for the final evaluation.
5. Run the app on the held-out conversations and have a reviewer score whether each expansion preserves intent, adds unsupported details, and handles ambiguity correctly. Store predictions and reviews in the shape described in the schema.
6. Score the held-out annotations:

   ```bash
   python code/backend/evaluation/score_holdout.py \
     --gold code/backend/evaluation/splits/held_out_test.jsonl \
     --predictions code/backend/evaluation/held_out_predictions.jsonl
   ```

The scorer reports L1/L2 accuracy and macro-F1, clarification precision/recall/F1, and human-reviewed expansion faithfulness and unsupported-detail rates. It compares topic labels only; it does not use exact string matching for paraphrased expansions.

## Annotation guidance

- Write natural conversations without templated prompts. Keep each conversation self-contained and preserve the full turn order.
- Label every user turn with one L1 and one valid L2 topic. Use `General > General` for small talk or interruptions.
- Mark `needs_clarification` only when the conversation does not support a single safe interpretation. Provide the clarification question a person should ask.
- For clear turns, write one acceptable standalone reference expansion. Preserve the speaker's intent and do not add facts absent from the conversation.
- Review model outputs independently of the gold labels. `intent_preserved` should be true only when meaning is retained; `unsupported_details` should be true when the model adds an ungrounded person, fact, or relationship.
- Keep the held-out set untouched while changing prompts, rules, or models. If it is used for tuning, create a new held-out set before reporting final results.

Human records and predictions should remain local until approval explicitly covers any sharing or publication.
## Approved real-conversation sample

The evaluation workflow now includes an optional local preview from Topical-Chat, an openly released human-human conversation dataset. See [TOPICAL_CHAT_SAMPLE.md](TOPICAL_CHAT_SAMPLE.md) for its source, license, and annotation guidance.

Prepare the preview from the repository root:

```powershell
python code/backend/evaluation/prepare_topicalchat_sample.py
```

By default, the script samples eight complete conversations from the source `test_freq` split and writes `local_data/topicalchat_preview.json`. The `local_data/` directory is ignored by Git, so raw conversation text stays local. Do not commit or push that preview.

The sample is not a completed gold evaluation set yet. It contains the source dataset's own sentiment and turn-quality fields, but still needs human labels for standalone rewrites, intent preservation, unsupported details, ambiguity, and this project's L1/L2 topic hierarchy. Keep every turn from a conversation in the same evaluation split to avoid conversation leakage.

