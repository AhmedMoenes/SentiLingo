# SentiLingo — Multilingual Customer Sentiment Analysis Platform

> DEPI (Digital Egypt Pioneers Initiative) Round 5 · Microsoft Machine Learning track · Graduation project

SentiLingo is a five-week capstone project that will classify customer feedback written in **English**, **Modern Standard Arabic (MSA)**, and **Egyptian Arabic** as **Negative**, **Neutral**, or **Positive**. The project compares credible classical text-classification baselines with a multilingual Transformer and delivers a local Streamlit demonstration.

| | |
|---|---|
| **Current status** | Planning and design package in progress; implementation has not started |
| **Planning date** | 2 November 2026 |
| **Final presentation** | 4 December 2026 |
| **Repository** | https://github.com/AhmedMoenes/SentiLingo |
| **Documentation** | [Project documentation PDF](docs/SentiLingo_Project_Documentation_Parts_1-4.pdf) |

## Problem statement

Companies receive customer feedback through reviews, surveys, support channels, and social media. Manually categorising multilingual feedback is slow and inconsistent. SentiLingo will provide a reproducible sentiment-analysis workflow for English, MSA, and Egyptian Arabic, while reporting results separately for each language variety.

## Approved scope

| Area | Current decision |
|---|---|
| Languages | English, MSA, and Egyptian Arabic |
| Labels | Negative, Neutral, and Positive |
| Classical comparison | Dummy classifier, Multinomial Naive Bayes, Logistic Regression, and Linear SVM |
| Text representations | Word TF-IDF, character TF-IDF, and their combination |
| Required advanced model | XLM-R Base |
| Controlled comparisons | MARBERT if the core schedule is healthy; BiLSTM only if required by the instructor |
| Model-selection metric | Mean of the per-language macro-F1 scores on validation data |
| Final evaluation | One evaluation on the frozen test set after the full configuration is locked |
| User interface | Local Streamlit application with single-text and CSV prediction |
| Deployment | Local-first; FastAPI, Docker, and Azure are stretch goals |
| Compute | Local CPU for data/classical work, RTX 4050 for smoke tests and inference, hosted GPU for main Transformer runs |

Franco-Arabic and other Arabic dialects are outside the core release. Mixed Arabic-English text may be inspected as an edge case, but performance outside the three supported varieties will not be claimed.

## Five-week delivery plan

| Week | Dates | Required outcome |
|---|---|---|
| Week 1 | 2–8 Nov | Approved planning package, dataset sources, licences, label mapping, common schema, and sample audit |
| Week 2 | 9–15 Nov | Dataset v1, frozen splits, data card, preprocessing, and classical baselines |
| Week 3 | 16–22 Nov | XLM-R trained and evaluated on validation data; optional comparison attempted only if safe |
| Week 4 | 23–29 Nov | Model locked, frozen-test evaluation, error analysis, and reliable local Streamlit demo |
| Week 5 | 30 Nov–4 Dec | Documentation, model card, presentation PDF, video demonstration, rehearsal, and delivery |

## Deliverables

- [x] Project Planning
- [x] Stakeholder Analysis and role-based RACI
- [x] Database Design - minimal experiment and model registry
- [ ] UI/UX Design
- [ ] Dataset source register, licence review, label mapping, and data card
- [ ] Reproducible preprocessing and frozen train/validation/test splits
- [ ] Dummy, Naive Bayes, Logistic Regression, and Linear SVM baselines
- [ ] XLM-R advanced model and controlled optional comparison
- [ ] Validation leaderboard and final test report
- [ ] Error analysis and representative predictions
- [ ] Streamlit application and clean-environment test
- [ ] README, model card, final documentation, presentation PDF, and video demonstration

## Team

- احمد مؤنس احمد عبدالفتاح
- نوران ناصر جلال سيد
- محمد محمود محمد عبدلله عياد
- احمد اشرف سامى فريد
- رضوه أشرف جمعه مهدي

Work ownership will be recorded in the project plan and GitHub issues. Each deliverable should have one owner, one reviewer, and visible evidence of completion.

## Planned repository structure

```text
.
├── app/            # Streamlit interface
├── data/           # Source register, download instructions, schema and data card
├── docs/           # Planning, design, reports, presentation material and meeting records
├── notebooks/      # Exploration and controlled experiments
├── src/            # Reusable data, feature, model and evaluation modules
└── tests/          # Automated checks for preprocessing, data leakage and prediction behaviour
```

The application and model implementation folders currently contain placeholders. Source code will be added only after the planning, dataset, and interface contracts are approved.

## Working rules

- Raw third-party datasets, credentials, model weights, and generated experiment artefacts are not committed.
- Every dataset must have a recorded source, licence, intended use, and label-mapping decision.
- All models use the same frozen data splits and comparable evaluation policy.
- Validation data selects models and hyperparameters; the test set is evaluated once after locking the configuration.
- Reported results must identify the data version, model configuration, seed, hardware, duration, and metric definitions.
- Optional features are stopped when they threaten the core demonstration, documentation, or rehearsal.

## Rebuilding the documentation PDF

The documentation is generated from the HTML sources in `docs/source/parts/`. Team names, dates, tasks, and milestones are stored in `docs/source/project.json`.

```bash
python docs/source/build_pdf.py
```

The build script uses Google Chrome or Microsoft Edge in headless mode and PyMuPDF to generate the PDF and resolve its table of contents.

## Current limitations

- No trained model, dataset build, or application is committed yet.
- Dataset selection and licensing still require approval.
- The exact submission deadline, and whether Azure or BiLSTM is mandatory, still require instructor confirmation.
- Performance claims will not be made until reproducible evaluation results exist.

## Acknowledgements

Built as a graduation project for the Digital Egypt Pioneers Initiative, Ministry of Communications and Information Technology, Egypt.
