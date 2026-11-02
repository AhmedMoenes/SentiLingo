# SentiLingo Database Design

## Decision

SentiLingo uses a minimal experiment and model registry. The logical schema is vendor-neutral; SQLite is the preferred local implementation if persistence is added. The registry stores reproducibility metadata and references to generated files. It does not store raw customer feedback, user accounts, credentials, or prediction history.

## Tables

| Table | Purpose | Main relationships |
|---|---|---|
| `dataset_versions` | Identifies prepared data, frozen splits, provenance, label policy, counts, and checksum | One dataset version has many experiment runs |
| `experiment_runs` | Records model configuration, features, parameters, seed, code revision, environment, hardware, timing, and status | Belongs to one dataset version; has many metrics and artifacts |
| `metric_results` | Stores validation or test measurements by language and label scope | Belongs to one experiment run |
| `artifacts` | References models, tokenizers, confusion matrices, error analyses, sample predictions, and reports | Belongs to one experiment run |

## Core integrity rules

1. Every experiment references exactly one immutable dataset version.
2. Completed runs are append-only evidence; corrections create a new run.
3. Metrics are unique for each run, split, language scope, label scope, and metric name.
4. Only a model artifact can be selected for the local-demo release, and only one model is selected at a time.
5. Test metrics are recorded only after the configuration is locked.
6. Raw feedback and personal data are not persisted by the registry.

## Physical implementation

SQLite fits the local-first demonstration because it is zero-cost, portable, easy to back up, and sufficient for the expected single-team write pattern. Foreign keys must be enabled. Database files and model artifacts are generated outputs and are not committed. Schema documentation and reviewer-friendly CSV or JSON exports are committed.

## Alternatives not selected

- **No database:** simpler, but weaker for audit queries, integrity constraints, and demonstrating database-design knowledge.
- **Full application database:** accounts, authentication, prediction history, and analytics would create excessive scope for five weeks.
- **Cloud-managed database:** adds cost, credentials, networking, and presentation risk without helping the required offline demo.
- **Model binaries inside the database:** makes backups and transfers unnecessarily heavy; the registry stores file locations and checksums instead.

The complete data dictionary, ER model, lifecycle, security decisions, and acceptance checklist are in the project documentation PDF.
