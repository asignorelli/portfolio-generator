# Evaluation

Our evaluation is split into two parts:

| Folder | What it contains |
|---|---|
| `automatic/` | Scripts that score generated portfolios against the real ones (`BERTScore_and_ROUGE.py`) |
| `manual/` | The rating rubric (`metrics.md`) and the filled-in human ratings, one file per sample |

## Automatic

Text-similarity scores between the generated and real portfolio, this uses BERTScore and ROUGE score. 

## Manual

Our group members rate each generated portfolio from 1 to 6 on several metrics. 