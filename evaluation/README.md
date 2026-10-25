# Evaluation

Our evaluation is split into two parts:

| Folder | What it contains |
|---|---|
| `automatic/` | Scripts that score generated portfolios against the real ones (`BERTScore_and_ROUGE.py`) |
| `manual/` | The rating rubric (`metrics.md`) and the filled-in human ratings, one file per sample |

## Automatic

Text-similarity scores between the generated and real portfolio, this uses BERTScore and ROUGE score. 

The script compares `data/portfolios/<id>.html` (real) with `output/html/<id>_output.html` (generated) and saves the scores to `automatic/results/<id>_scores.txt`.

```
pip install -r evaluation/automatic/requirements.txt
python evaluation/automatic/BERTScore_and_ROUGE.py 0007 0012   # score specific samples
python evaluation/automatic/BERTScore_and_ROUGE.py --all       # score every sample with both files
```

Add `--diff` to also print a line-by-line text diff. The first run downloads the BERTScore model (about 600 MB). If a results file has a `WARNINGS` section, read it: it usually means the real portfolio's saved HTML is missing its content.

## Manual

Our group members rate each generated portfolio from 1 to 6 on several metrics. 