"""Scores generated portfolios against the real ones with ROUGE and BERTScore.

Reference: data/portfolios/<id>.html            (the person's real portfolio)
Candidate: output/html/<id>_output.html         (the portfolio Claude generated)
Results:   evaluation/automatic/results/<id>_scores.txt

Usage (from anywhere in the repo):
    python evaluation/automatic/BERTScore_and_ROUGE.py 0007 0012
    python evaluation/automatic/BERTScore_and_ROUGE.py --all
    python evaluation/automatic/BERTScore_and_ROUGE.py 0007 --diff
"""

import argparse
import difflib
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from rouge_score import rouge_scorer
from bert_score import BERTScorer

REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_DIR = REPO_ROOT / "data" / "portfolios"
CANDIDATE_DIR = REPO_ROOT / "output" / "html"
RESULTS_DIR = REPO_ROOT / "evaluation" / "automatic" / "results"

# Longformer reads up to 4096 tokens. roberta-base stops at 512, which would
# only score the top of a full portfolio page.
DEFAULT_MODEL = "allenai/longformer-base-4096"

# A real portfolio with less text than this was probably rendered by JavaScript,
# so the saved source doesn't contain the page content.
MIN_REFERENCE_WORDS = 50

BLOCK_TAGS = [
    "p", "div", "section", "article", "header", "footer", "nav", "main", "aside",
    "h1", "h2", "h3", "h4", "h5", "h6", "li", "ul", "ol", "table", "tr", "td", "th",
    "br", "hr", "blockquote", "pre", "form", "figure", "figcaption", "dd", "dt",
]


def extract_clean_text_lines(html_content):
    """Parses HTML, removes non-visible elements, and returns a list of clean, stripped text lines."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Strip out non-visible elements
    for element in soup(["script", "style", "head", "title", "meta", "noscript", "svg", "template"]):
        element.extract()

    # Put each block element on its own line, so the diff lines up with what's on screen
    for element in soup.find_all(BLOCK_TAGS):
        element.insert_before("\n")
        element.insert_after("\n")

    # The space separator stops inline elements (links, bold text) from merging into one word
    text = soup.get_text(" ")
    clean_lines = []
    for line in text.splitlines():
        cleaned = " ".join(line.split())
        if cleaned:
            clean_lines.append(cleaned)
    return clean_lines


def print_diff(ref_lines, cand_lines):
    print("=" * 60)
    print(" TEXT DIFFERENCES (Reference [-] vs Candidate [+]) ")
    print("=" * 60)

    has_differences = False
    for line in difflib.ndiff(ref_lines, cand_lines):
        if line.startswith("- ") or line.startswith("+ "):
            has_differences = True
            print(line)
        elif line.startswith("? "):
            print(f"  {line.strip()}")  # Intra-line tweaks pointer

    if not has_differences:
        print("Text content matches exactly!")
    print()


def evaluate_sample(sample_id, bert_scorer, show_diff=False):
    """Scores one sample, prints the results, and saves them to the results folder."""
    ref_path = REFERENCE_DIR / f"{sample_id}.html"
    cand_path = CANDIDATE_DIR / f"{sample_id}_output.html"
    for path in (ref_path, cand_path):
        if not path.exists():
            print(f"[{sample_id}] Skipped: missing {path.relative_to(REPO_ROOT).as_posix()}")
            return False

    ref_lines = extract_clean_text_lines(ref_path.read_text(encoding="utf-8", errors="replace"))
    cand_lines = extract_clean_text_lines(cand_path.read_text(encoding="utf-8", errors="replace"))

    # Convert to single strings for NLP metrics (ROUGE / BERTScore)
    ref_string = " ".join(ref_lines)
    cand_string = " ".join(cand_lines)

    warnings = []
    ref_words = len(ref_string.split())
    if ref_words < MIN_REFERENCE_WORDS:
        warnings.append(
            f"Reference has only {ref_words} words of text. The site may be rendered by JavaScript; "
            "re-save it from DevTools (right-click <html> > Copy > Copy outerHTML)."
        )

    max_tokens = bert_scorer._tokenizer.model_max_length
    for name, text in (("Reference", ref_string), ("Candidate", cand_string)):
        n_tokens = len(bert_scorer._tokenizer.encode(text))
        if n_tokens > max_tokens:
            warnings.append(f"{name} is {n_tokens} tokens; BERTScore only reads the first {max_tokens}.")

    if show_diff:
        print_diff(ref_lines, cand_lines)

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rouge_results = scorer.score(ref_string, cand_string)
    if ref_string and cand_string:
        P, R, F1 = (t.item() for t in bert_scorer.score([cand_string], [ref_string]))
    else:
        # bert-score crashes on empty text, and there is nothing to compare anyway
        P = R = F1 = 0.0
        warnings.append("One of the pages has no visible text, so BERTScore was set to 0.")

    lines = [
        f"PAIR: {sample_id}",
        f"REFERENCE: {ref_path.relative_to(REPO_ROOT).as_posix()} ({ref_words} words)",
        f"CANDIDATE: {cand_path.relative_to(REPO_ROOT).as_posix()} ({len(cand_string.split())} words)",
        f"BERTSCORE_MODEL: {bert_scorer.model_type}",
        "",
        "[ROUGE]",
    ]
    for metric, values in rouge_results.items():
        lines.append(
            f"{metric}: precision={values.precision:.4f} recall={values.recall:.4f} f1={values.fmeasure:.4f}"
        )
    lines += [
        "",
        "[BERTScore]",
        f"bertscore: precision={P:.4f} recall={R:.4f} f1={F1:.4f}",
    ]
    if warnings:
        lines += ["", "WARNINGS:"] + [f"- {w}" for w in warnings]

    report = "\n".join(lines) + "\n"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / f"{sample_id}_scores.txt"
    out_path.write_text(report, encoding="utf-8")

    print("=" * 60)
    print(report, end="")
    print(f"Saved to {out_path.relative_to(REPO_ROOT).as_posix()}")
    print("=" * 60)
    return True


def find_all_sample_ids():
    """Sample IDs that have both a real portfolio and a generated one."""
    reference_ids = {p.stem for p in REFERENCE_DIR.glob("*.html")}
    candidate_ids = {p.stem.removesuffix("_output") for p in CANDIDATE_DIR.glob("*_output.html")}
    return sorted(reference_ids & candidate_ids)


def main():
    parser = argparse.ArgumentParser(description="Score generated portfolios with ROUGE and BERTScore.")
    parser.add_argument("sample_ids", nargs="*", help="4-digit sample IDs to score, e.g. 0007 0012")
    parser.add_argument("--all", action="store_true", help="score every sample that has both HTML files")
    parser.add_argument("--diff", action="store_true", help="also print a line-by-line text diff")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"BERTScore model (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    sample_ids = find_all_sample_ids() if args.all else [s.zfill(4) for s in args.sample_ids]
    if not sample_ids:
        parser.error("give one or more sample IDs, or use --all")

    print(f"Loading BERTScore model {args.model} (the first run downloads it)...")
    bert_scorer = BERTScorer(model_type=args.model, lang="en")
    # Some tokenizers (like Longformer's) report a huge placeholder max length, which
    # crashes bert-score. Cap it at what the model can actually read.
    model_limit = bert_scorer._model.config.max_position_embeddings - 2
    bert_scorer._tokenizer.model_max_length = min(bert_scorer._tokenizer.model_max_length, model_limit)

    scored = sum(evaluate_sample(s, bert_scorer, args.diff) for s in sample_ids)
    print(f"Scored {scored} of {len(sample_ids)} samples.")
    return 0 if scored == len(sample_ids) else 1


if __name__ == "__main__":
    sys.exit(main())
