import difflib 
from bs4 import BeautifulSoup 
from rouge_score import rouge_scorer 
from bert_score import score as bert_score 

def extract_clean_text_lines(html_content): 

    """Parses HTML, removes boilerplate, and returns a list of clean, stripped text lines.""" 
    soup = BeautifulSoup(html_content, 'html.parser') 

    # Strip out non-visible elements 
    for element in soup(["script", "style", "head", "title", "meta"]): 
        element.extract() 

    # Extract line by line to preserve structure for the diff 
    text = soup.get_text() 
    clean_lines = [] 
    for line in text.splitlines(): 
        cleaned = line.strip() 
        if cleaned: 
            clean_lines.append(cleaned) 
    return clean_lines 

def evaluate_and_diff_html(html_candidate, html_reference): 
    # 1. Clean HTML and prepare text structures 
    cand_lines = extract_clean_text_lines(html_candidate) 
    ref_lines = extract_clean_text_lines(html_reference) 

    # Convert to single strings for NLP metrics (ROUGE / BERTScore) 
    cand_string = " ".join(cand_lines) 
    ref_string = " ".join(ref_lines) 

    # 2. Print Content Differences 
    print("=" * 60) 
    print(" TEXT DIFFERENCES (Reference [-] vs Candidate [+]) ") 
    print("=" * 60) 

    diff = difflib.ndiff(ref_lines, cand_lines) 
    has_differences = False 

    for line in diff: 
        # Check if line indicates a difference 
        if line.startswith('- ') or line.startswith('+ '): 
            has_differences = True 
            print(line) 

        elif line.startswith('? '): 
            print(f"  {line.strip()}") # Intra-line tweaks pointer 

    if not has_differences: 
        print("Text content matches exactly!") 

    print("\n" + "=" * 60) 
    print(" EVALUATION SCORES ") 
    print("=" * 60) 

    # 3. Compute and Print ROUGE Scores 
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True) 
    rouge_results = scorer.score(ref_string, cand_string) 

    print("[ROUGE Metrics]") 
    for metric, values in rouge_results.items(): 
        print(f"  {metric.upper():<7} -> Precision: {values.precision:.4f} | Recall: {values.recall:.4f} | F1: {values.fmeasure:.4f}") 

    # 4. Compute and Print BERTScores 
    # Using 'roberta-base' as a fast, reliable baseline 
    P, R, F1 = bert_score([cand_string], [ref_string], lang="en", model_type="roberta-base", verbose=False) 

    print("\n[BERTScore Metric]") 
    print(f"  Precision: {P.item():.4f}") 
    print(f"  Recall:    {R.item():.4f}") 
    print(f"  F1-Score:  {F1.item():.4f}") 
    print("=" * 60) 

# Example Usage: 
html_ref = """ 
<div> 
    <h1>Project Overview</h1> 

    <p>The primary target is to extract textual elements safely.</p> 

    <p>Ensure to filter scripts.</p> 

</div> 

""" 
html_cand = """ 

<div> 

    <h1>Project Overview</h1> 

    <p>The main goal is to safely extract textual elements.</p> 

    <!-- Notice 'Ensure to filter scripts' is missing here --> 

</div> 

""" 

evaluate_and_diff_html(html_cand, html_ref) 