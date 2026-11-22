# NeuroAnalytics

Streamlit workspace for reviewing one child's MRI studies across dates. TypeSafe AI JEV reads the full set of written reports in one request and uses earlier reports as context to answer the selected questions about the latest study and OpenAI prepares a separate draft for clinician review from the dated JEV results.

## Run locally

Requires Python 3.11 or newer. From the repository folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Add your TypeSafe AI and OpenAI keys to .env.
.\.venv\Scripts\python -m streamlit run app.py --server.address 127.0.0.1
```

1. Enter each study date and attach de-identified written material or an annotated MRI figure. Written material can be a text-based PDF or UTF-8 TXT file. For scanned PDFs, verify the OCR text before uploading it as TXT.
2. Review the seven questions from `AnalyzeDecision.py`. Four require the upper-row Panel B figure referenced by their prompts. The three diagnosis-status questions use the written material. Remove questions, add custom written-report questions with answer choices, or restore the original bank.
3. Run JEV to view answers and image annotations for the latest study. The app selects the newest study date and asks you to choose the latest study if dates tie. Only the latest study's image is used. Review the results before generating the OpenAI draft.

TypeSafe receives the applicable source material and questions. OpenAI receives question labels, dated results, source types and study IDs. Use approved de-identified material and keep the local server private. Review image annotations and the summary against the source material with the care team.

The question bank edits and results live in the current Streamlit session.
