# Local Topical-Chat annotation sample

The project uses Topical-Chat as an approved candidate source for a small,
human-written conversation evaluation sample. It is a human-human,
knowledge-grounded corpus with existing sentiment and turn-quality annotations.
Those source annotations do **not** provide query expansions or the project's
L1/L2 topic labels, so the blank annotation fields must be completed by a human
reviewer before the sample is used as evaluation data.

## Prepare the local preview

From the repository root, run:

```powershell
python code/backend/evaluation/prepare_topicalchat_sample.py
```

This downloads the official `test_freq` split in memory and writes eight whole
conversations to `code/backend/evaluation/local_data/topicalchat_preview.json`.
Change the sample size with `--limit N`. The output is ignored by Git. Keep it
local; do not commit or push raw conversation text. A deterministic seed is
recorded in the output. Conversation-level IDs remain intact so that later
splits can keep all turns from one conversation together.

## Manual annotation fields

For each task, complete the standalone rewrite, whether intent was preserved,
whether unsupported details were added, whether the turn is ambiguous, and the
project's L1/L2 labels. Review the full conversation context before labeling.
Do not treat Topical-Chat's sentiment or turn-quality fields as labels for this
project.

## Source and license

- Dataset: [Topical-Chat](https://github.com/alexa/Topical-Chat)
- Source split: `conversations/test_freq.json`
- Data license: [Community Data License Agreement - Sharing v1.0](https://github.com/alexa/Topical-Chat/blob/master/DATALICENSE)
- Paper: Gopalakrishnan et al., *Topical-Chat: Towards Knowledge-Grounded Open-Domain Conversations*, Interspeech 2019, [DOI](https://doi.org/10.21437/Interspeech.2019-3079).

The dataset repository requires attribution and licensing notices if data is
published. The local preview is excluded from Git; check license obligations
again before distributing any copied or annotated data.
