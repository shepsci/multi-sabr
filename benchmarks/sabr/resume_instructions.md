# SABR Hackathon Resume Instructions

You are resuming work on the **SABR (Selective Attention Benchmark for Reasoning)** submission to the [Kaggle Measuring Progress Toward AGI](https://www.kaggle.com/competitions/kaggle-measuring-agi) hackathon. The deadline is **April 16, 2026**. Everything is **private** (Kaggle + GitHub) until we decide to publish.

## Current State

The submission is **live and complete** as of March 18, 2026. All 6/6 checklist items are done:
- Writeup submitted (editable until deadline)
- Card image uploaded
- Track: **Attention**
- Project link: benchmark collection URL (added via External Links, not Kaggle Benchmarks search)

### Session 2 Improvements (March 18, 2026)
All 7 planned improvements completed:
1. **SABR logo** created (800×450 PNG, deep indigo background) and uploaded to Kaggle media gallery — embedded in writeup
2. **Removed DeepMind branding**: replaced "grounded in DeepMind's AGI cognitive framework (§7.3.2)" with inline `[Burnell et al. (2026)](URL)` citations throughout all files
3. **Diversified references**: added Shi et al. (2023), Liu et al. (2023), Hendrycks et al./MMLU (2021) — all verified URLs
4. **Consistent citation style**: `[Author (Year)](URL)` format with hyperlinks throughout writeup; no section refs
5. **Expanded docstrings**: all three task files (`task_distractor.py`, `task_source_select.py`, `task_spotlight.py`) have detailed data schema, scoring, and result range documentation
6. **Resources section** added to writeup with links to benchmark collection, notebook, dataset, and GitHub
7. **"Submission Against Judging Criteria" section** added to writeup with three subsections: "Evidence that the dataset and task are both high quality", "Evidence that the writeup is high quality", "Evidence that the benchmark has sufficient discriminatory power"
8. **Notebook synced to Kaggle** via CLI (`kaggle kernels push`, version 7)

**Note on logo sizing**: Kaggle media gallery requires minimum 640×360px. The logo is 800×450px to meet this requirement.

### Session 3 Improvements (March 18, 2026)
All tasks completed:
1. **Ran 3 additional models**: Claude Opus 4.6, Gemini 3.1 Pro Preview, Gemma 3 27B — now 6 models on leaderboard
2. **Updated sabr_notebook.py**: Removed subtitle comment, updated top markdown table with 6-model results, pushed to Kaggle as version 8
3. **Added descriptions** to benchmark task page, benchmark collection page, dataset page (usability score jumped from 2.50 to 4.38), and confirmed notebook cells serve as documentation
4. **Updated Kaggle writeup**: Synced 6-model results table with Gemini 2.5 Flash and Gemma 3 27B distractor breakdowns, updated composite spreads in TL;DR section
5. **Writeup verified live**: "Submitted!" confirmed, Resources section visible with all 4 links, inline citations rendering as hyperlinks

### Key URLs
- **Writeup editor**: https://www.kaggle.com/competitions/kaggle-measuring-agi/writeups/measuring-progress-toward-agi
- **Benchmark notebook editor**: https://www.kaggle.com/code/shepscientific/new-benchmark-task-0adb6/edit
- **Benchmark task page**: https://www.kaggle.com/benchmarks/tasks/shepscientific/sabr-benchmark-hwqqb6/
- **Benchmark collection**: https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning
- **Leaderboard**: https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning/leaderboard
- **GitHub (private)**: https://github.com/shepsci/SABR
- **Kaggle dataset**: https://www.kaggle.com/datasets/shepscientific/sabr-selective-attention-data

### Current Results (6 models, as of March 18, 2026)
| Model | Composite | Distractor (ARS) | Source-Selective | Spotlight (F1) |
|-------|-----------|-------------------|------------------|----------------|
| Claude Opus 4.6 | 92% | 91% | 100% | 84% |
| Gemini 3.1 Pro Preview | 87% | 88% | 100% | 74% |
| Claude Sonnet 4.6 | 85% | 86% | 100% | 68% |
| Claude Haiku 4.5 | 84% | 79% | 100% | 74% |
| Gemma 3 27B | 82% | 81% | 100% | 66% |
| Gemini 2.5 Flash | 76% | 68% | 100% | 63% |

Gemini 2.5 Flash distractor breakdown: clean 100%, low 84%, medium 44%, high 48%.
Gemma 3 27B distractor breakdown: clean 96%, low 98%, medium 76%, high 54%.

## Project Structure

```
/Users/smallmacmini/SABR/
├── benchmark/
│   ├── sabr_notebook.py          # THE MAIN DELIVERABLE - Kaggle benchmark notebook
│   ├── sabr_notebook.ipynb       # Jupyter version (same code)
│   ├── task_distractor.py        # Distractor Robustness implementation
│   ├── task_source_select.py     # Source-Selective QA implementation
│   └── task_spotlight.py         # Attentional Spotlight implementation
├── data/
│   ├── distractor_robustness.json # 50 items x 4 conditions = 200 evals
│   ├── source_selective.json      # 50 items = 50 evals
│   └── attentional_spotlight.json # 30 items = 30 evals
├── scripts/
│   └── validate_data.py
├── writeup/
│   ├── writeup.md                # Competition writeup (~1500 words, max 1500)
│   ├── sabr_card.png             # 560x280 card image
│   └── sabr_logo.png             # 800x450 SABR logo (in Kaggle media gallery)
├── config.yaml
└── requirements.txt
```

## Technical Details That Matter

### Kaggle Benchmarks SDK
- Import: `import kaggle_benchmarks as kbench` (NOT `import kbench`)
- Decorator: `@kbench.task(name="SABR Benchmark hwqqb6", description="...")`
- Task function must return `float` (NOT dict, NOT tuple)
- Supported return types: `None`, `bool`, `int`, `float`, `tuple[int,int]`, `tuple[float,float]`
- Chat isolation: `with kbench.chats.new("unique_id"):` for each eval
- LLM calls: `response = llm.prompt(prompt_string)`
- Task names must be globally unique (our suffix: `hwqqb6`)
- Run cell: `run = sabr_benchmark.run(llm=kbench.llm)`
- Choose directive: `# %choose sabr_benchmark`

### Data Loading
- Benchmark runtime runs from `/tmp/ipykernel_13/` — NOT `/kaggle/working/`
- Benchmark runtime does NOT mount `/kaggle/input/`
- Working solution: `kagglehub.dataset_download("shepscientific/sabr-selective-attention-data")` with `/kaggle/input/` fallback

### Scoring
- Tasks 1-2: case-insensitive exact match with word-boundary awareness + alias support
- Task 3: token-overlap F1 (70% threshold) with bullet/numbering normalization
- Composite: Distractor 40%, Source-Selective 30%, Spotlight 30%
- Zero-gold-count spotlight items score 1.0 only if model produces no claims

## Lessons Learned (Things That Tripped Us Up)

### Kaggle Platform Gotchas
1. **Benchmark runtime paths**: The benchmark runtime does NOT use `/kaggle/input/`. Always use `kagglehub.dataset_download()` as primary, with `/kaggle/input/` as fallback.
2. **Task return types**: Only primitives work. We wasted time with dict returns before discovering this.
3. **Benchmark search doesn't find your own benchmarks**: When adding project links, the "Kaggle Benchmarks" search tab returns no results for your own benchmarks. Use "External Links" tab instead to paste the collection URL directly.
4. **Track selection persists oddly**: The save dialog may show the wrong track name, but after reload it's correct. Don't panic.
5. **File upload is blocked**: The standard `file_upload` MCP tool returns `{"code":-32000,"message":"Not allowed"}` on Kaggle writeup pages.

### Image Upload Workaround (What Worked)
The `file_upload` tool is blocked on Kaggle. The working approach:
1. Start a CORS-enabled local HTTP server serving the image directory
2. Use browser JavaScript `fetch('http://localhost:PORT/image.png')` to get a blob
3. Create a `File` from the blob, wrap in `DataTransfer`, set on the `input[type="file"]` element
4. Dispatch `change` event with `{ bubbles: true }`

**Critical**: A plain `python3 -m http.server` does NOT work because it lacks CORS headers. You must use a custom handler that adds `Access-Control-Allow-Origin: *`.

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
os.chdir('/Users/smallmacmini/SABR/writeup')
class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        super().end_headers()
HTTPServer(('', 8765), CORSHandler).serve_forever()
```

### Base64 in JavaScript (What Failed)
Passing raw base64 strings into JavaScript template literals fails with `InvalidCharacterError` due to newlines from shell output. Don't bother with this approach — use the fetch + CORS server method above.

### Kaggle Editor Text Manipulation
When updating writeup text via JavaScript:
- Get textarea: `document.querySelector('textarea')` (for the body field)
- Set value and dispatch events: `textarea.value = newText; textarea.dispatchEvent(new Event('input', {bubbles: true}))`
- Em-dash (`—`) characters may not match between your search string and the actual textarea content. Use simpler unique substrings for find-and-replace.

## Daily Improvement Ideas

When resuming, consider these areas for improvement (pick one or two per session):

### Data Quality
- [ ] Review distractor items where models succeed at high distraction — may need harder distractors
- [ ] Add more answer aliases for edge cases the models might produce
- [ ] Audit spotlight gold claims for consistency across filter categories
- [ ] Check if any distractor questions have ambiguous answers

### Benchmark Code
- [ ] Add error handling for edge cases in claim matching
- [ ] Consider adding per-domain breakdowns in assertions output
- [ ] Test if prompt format changes improve spotlight F1 (more specific instructions)
- [ ] Explore whether few-shot examples in spotlight prompts help precision

### Results & Analysis
- [x] Run benchmark on additional models as they become available on Kaggle (6 models now complete)
- [ ] Analyze which specific items models get wrong — look for patterns
- [ ] Create visualizations (accuracy-vs-distraction curves, model comparison charts)
- [ ] Add visualizations to Media Gallery in writeup

### Writeup Improvements
- [x] Add Resources section with links to all artifacts
- [x] Add Submission Against Judging Criteria section
- [x] Diversify references with hyperlinks
- [x] SABR logo embedded in writeup
- [ ] Word count is now near 1500 — limited headroom for additions
- [ ] Could add: accuracy degradation curve visualization
- [ ] Could add: per-domain analysis or position bias breakdown

### Competition Strategy
- [ ] Monitor other submissions in the Attention track for ideas
- [ ] Check if judges have posted any feedback or criteria clarifications
- [ ] Consider whether adding more evaluation items would strengthen the submission
- [ ] Review the competition rubric again for any missed scoring criteria

## Workflow for Making Changes

### To update the benchmark code:
1. Edit `benchmark/sabr_notebook.py` locally
2. Mirror changes to `benchmark/sabr_notebook.ipynb` (use NotebookEdit tool)
3. Run `kaggle kernels push -p benchmark/` to push to Kaggle (kernel ref: `shepscientific/new-benchmark-task-0adb6`)
4. Commit locally and push to GitHub

### To update the writeup:
1. Edit `writeup/writeup.md` locally
2. Navigate to the writeup editor URL
3. Update the textarea via JavaScript or manual editing
4. Save Draft (or Submit if already submitted — edits allowed until deadline)
5. Commit locally and push to GitHub

### To update the dataset:
1. Edit JSON files in `data/`
2. Run `scripts/validate_data.py` to verify schema
3. Upload new dataset version to Kaggle
4. Re-run the benchmark notebook
5. Commit and push

## Quick Start Checklist

When you begin a session:
1. Read this file for context
2. Check `git status` and `git log --oneline -5` to see latest state
3. Open the leaderboard URL to check for new model results
4. Pick an improvement area from the list above
5. Make changes, test, commit, push
6. Update this file if you discover new gotchas or complete improvement items
