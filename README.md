# SentiLingo — Multilingual Customer Sentiment Analysis Platform

> DEPI (Digital Egypt Pioneers Initiative) Round 5 · Microsoft Machine Learning track · Graduation Project

SentiLingo classifies customer feedback written in **Arabic (MSA and Egyptian dialect)**, **English** and **Franco-Arabic** as **Negative**, **Neutral** or **Positive**, with a confidence score. It compares a classical NLP baseline with deep-learning and pretrained Transformer models, tracks every experiment in MLflow, and can optionally serve the best model from an Azure Machine Learning endpoint.

| | |
|---|---|
| **Status** | Kick-off (19 Oct 2026): documentation Parts 1–3 delivered |
| **Repository** | https://github.com/AhmedMoenes/SentiLingo |
| **Documentation** | [Project Documentation — Parts 1–3 (PDF)](docs/SentiLingo_Project_Documentation_Parts_1-3.pdf) |
| **Next milestone** | MS1: dataset v1 and EDA (25 Oct 2026) |
| **Final presentation** | 4 Dec 2026 |

## Problem statement

A company receives customer feedback in natural-language text and needs to automatically identify whether feedback expresses positive, negative, or other predefined sentiment categories.

## Approach

| Stage | What we build |
|---|---|
| Data | A unified multilingual dataset built from public review and tweet corpora, mapped to 3 classes, de-duplicated, with frozen stratified splits |
| Preprocessing | Configurable cleaning, Arabic normalisation, tokenisation that keeps negation words |
| Baseline | TF-IDF with word and character n-grams, plus Naive Bayes and Logistic Regression |
| Advanced models | BiLSTM and fine-tuned Hugging Face Transformers (multilingual and Arabic) |
| Evaluation | Accuracy, precision, recall, F1 (macro and per class), confusion matrix, per-language slices, error analysis |
| MLOps | MLflow experiment tracking and model registry |
| Extension | Azure ML managed online endpoint and a Streamlit demo |

## Deliverables checklist

- [ ] D1 Dataset and data card
- [ ] D2 NLP preprocessing pipeline
- [ ] D3 Classical baseline (TF-IDF + n-grams, NB / LR)
- [ ] D4 Deep-learning / pretrained model (BiLSTM, Transformer)
- [ ] D5 Model comparison
- [ ] D6 MLflow experiment tracking
- [ ] D7 Error analysis
- [ ] D8 Sample predictions
- [ ] D9 README
- [ ] D10 *(optional)* Azure ML endpoint and demo app
- [x] Project documentation, Parts 1–3

## Roadmap

| Milestone | Target date | Exit criteria |
|---|---|---|
| MS0 | 19 Oct 2026 | Kick-off: documentation Parts 1–3 and GitHub repository |
| MS1 | 25 Oct 2026 | Dataset v1, frozen splits, data card, EDA |
| MS2 | 1 Nov 2026 | Preprocessing pipeline and NB / LR baselines in MLflow |
| MS3 | 15 Nov 2026 | BiLSTM and fine-tuned Transformer trained |
| MS4 | 22 Nov 2026 | Model comparison, error analysis, sample predictions, best model registered |
| MS5 | 29 Nov 2026 | *(optional)* Azure ML endpoint and demo app |
| MS6 | 4 Dec 2026 | Final presentation |

## Team

- احمد مؤنس احمد عبدالفتاح
- نوران ناصر جلال سيد
- محمد محمود محمد عبدلله عياد
- احمد اشرف سامى فريد
- رضوه أشرف جمعه مهدي

Responsibilities for each work area will be agreed at the first sprint planning meeting.

## Repository structure

```text
.
├── app/            # Streamlit demo and serving code (planned)
├── data/           # Download scripts and data card; raw/processed data is git-ignored
├── docs/
│   ├── SentiLingo_Project_Documentation_Parts_1-3.pdf
│   ├── meetings/   # Sprint meeting notes
│   └── source/     # HTML sources and build script for the documentation PDF
├── notebooks/      # EDA and experiment notebooks
├── src/            # Reusable pipeline code: data, preprocessing, features, models, evaluation
└── tests/          # Unit tests
```

## Rebuilding the documentation PDF

The PDF is generated from the HTML files in `docs/source/parts/`. Team names, dates and the schedule are in `docs/source/project.json`.

```bash
git clone https://github.com/AhmedMoenes/SentiLingo.git
cd SentiLingo
pip install pymupdf
python docs/source/build_pdf.py
```

The script needs Google Chrome or Microsoft Edge, which it runs headless to print the PDF. Set `CHROME_PATH` if the browser is installed in a non-standard location.

## Data and licences

Only public datasets are used. Raw third-party data is never committed. Each source's licence and terms are recorded in the data card, and some sources allow non-commercial or research use only.

## Acknowledgements

Built as a graduation project of the Digital Egypt Pioneers Initiative (DEPI), Ministry of Communications and Information Technology, Egypt.
