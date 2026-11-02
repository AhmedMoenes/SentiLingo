# SentiLingo UI UX Design

## Decision

SentiLingo will use a multi-page local Streamlit dashboard. The dashboard provides analysis, batch processing, session analytics, model evidence, experiment traceability, and help without adding authentication or persistent customer-message history.

## Information architecture

| Page | Primary purpose | Core release |
|---|---|---|
| Overview | Explain the product, show the current session and direct users to the correct workflow | Yes |
| Analyze Text | Predict one English, MSA, or Egyptian Arabic message | Yes |
| Analyze CSV | Validate a file, choose the text column, preview rows, run batch prediction, and export | Yes |
| Results | Explore the current batch by sentiment and language and download the enriched CSV | Yes |
| Model Performance | Show validation and locked-test evidence without mixing the two | Yes |
| Experiment Registry | Read-only traceability from model artefact to run, dataset, configuration, and metrics | Yes, after registry persistence is available |
| Help and Limitations | Explain labels, supported language varieties, privacy, file requirements, and known limitations | Yes |

The dashboard does not include user accounts, role administration, or persistent prediction history. “History” means model experiment history from the approved registry, not stored customer messages.

## Primary workflows

### Single text

1. Open Analyze Text.
2. Enter a message or choose a labelled example.
3. The interface validates that the text is not empty.
4. Run analysis.
5. Review sentiment, confidence estimate, detected variety, and the limitation notice.
6. Open Model Performance when evaluation evidence is needed.

### CSV batch

1. Open Analyze CSV and select a CSV file.
2. Choose the text column and preview validation results.
3. Resolve missing-column, empty-row, encoding, or unsupported-file errors.
4. Run batch analysis.
5. Open Results to filter the current session and download an enriched CSV.

### Evaluator review

1. Open Overview to understand the supported workflow.
2. Review Model Performance and confirm validation data selected the model.
3. Open Experiment Registry and trace the selected artefact to its dataset, run, configuration, and metrics.
4. Review Help and Limitations before interpreting predictions.

## Interaction and privacy rules

- Prediction text is processed in memory and is not added to the registry.
- Validation errors are shown next to the affected control and never rely on colour alone.
- Arabic content is right-to-left while navigation, identifiers, numbers, and English content remain readable.
- Confidence is presented as a model estimate, not a guarantee.
- Empty, loading, success, partial-success, and failure states are designed before implementation.
- The interface remains usable by keyboard and at narrow browser widths.
- Charts never display invented model scores; placeholders remain clearly marked until reproducible results exist.

## Scope consequence

The multi-page architecture improves portfolio value and separates user goals, but it creates more navigation, shared state, integration tests, and presentation rehearsal than a two-tab interface. The team must build the prediction contract first and stop visual extras if they threaten model evaluation, documentation, or the offline demonstration.
