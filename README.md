# OSMS Mold Master Data

ETL pipeline and Excel deliverables for sole-mold master data, governed
by the **Bottoming Mold Master Data Standard v3.0/v3.1** in
[`docs/reference/`](docs/reference/) — the source of truth for naming,
hierarchy, and governance rules.

## The standard in one paragraph

Mold data has two layers. The **Mold ID** is the product definition —
`{MoldFamily}-{Type}-{Position}(-B)` with Type ∈ {OS, MS, OT}, Position
∈ {PRI, BOT, HEEL}, and `-B` marking a blocker preform (e.g.
`SA-2301-MS-PRI-B`). The **Physical Asset** is an actual mold at a
vendor (size coverage, mold set, revision, status). Governance: PRI
always exists; BOT/HEEL require PRI; OT is always PRI; every `-B` pairs
with a non-B; legacy non-standard family codes (e.g. `S1612`) are
frozen — retained but never replicated.

## Pipeline

```
external source Excel files (DATA_ROOT)
        │
        ▼
notebooks/data_processing.ipynb ──► data/mold_data.json  (schemaVersion 5.0)
        │                                   │
        │                                   ├──► notebooks/dq_issues_by_family.ipynb
        │                                   │        └─► data/dq_issues_by_family.xlsx
        │                                   │
        │                                   └──► notebooks/json_export.ipynb
        │                                            └─► data/output/{Family}.xlsx
        │                                                 (one workbook per mold family,
        └── mapping logic shared via                       from docs/templates/
            notebooks/mold_v3_mapping.py                  MoldFamily_(Template).xlsx)
```

## Repository layout

| Path | Purpose |
|------|---------|
| `docs/reference/` | **Authoritative standard** (Definition v3.0 + Standard v3.1) |
| `docs/Mold Data – JSON Structure & Template Changes (v5).md` | JSON schema 5.0 + template change log |
| `docs/Mold Management Excel – Final Design Spec.md` | Excel workbook design spec |
| `docs/Mold Management Excel – Owner Setup Guide.md` | Template owner configuration guide |
| `docs/Mold Management Excel – User Instruction Guide.md` | End-user editing guide |
| `docs/templates/MoldFamily_(Template).xlsx` | Per-family workbook template |
| `notebooks/mold_v3_mapping.py` | Shared legacy→v3 mapping module (single source of truth) |
| `notebooks/data_processing.ipynb` | Source Excel → `mold_data.json` (v5.0) |
| `notebooks/dq_issues_by_family.ipynb` | Data-quality + v3 governance report (I1–I19) |
| `notebooks/json_export.ipynb` | JSON → one Excel workbook per family (win32com) |
| `scripts/update_template_v3.py` | One-time template migration to v3 naming (already applied) |
| `data/` | Generated artifacts (not tracked) |

## Setup

Requires Windows with Microsoft Excel (the export and template scripts
drive Excel via COM) and [uv](https://docs.astral.sh/uv/).

```
uv sync
```

Create `.env` with the location of the raw source files (needed only to
regenerate `mold_data.json`):

```
DATA_ROOT=<folder containing "WWW Bottom Mold list..." and "Mold Capacity Management.xlsm">
```

## Running

Run the notebooks in order (Jupyter, VS Code, or headless):

```
uv run --with nbconvert python -m nbconvert --to notebook --execute --inplace notebooks/data_processing.ipynb
uv run --with nbconvert python -m nbconvert --to notebook --execute --inplace notebooks/dq_issues_by_family.ipynb
uv run --with nbconvert python -m nbconvert --to notebook --execute --inplace notebooks/json_export.ipynb
```

`json_export.ipynb` has a `MAX_FAMILIES` setting in its first code cell
for quick smoke tests. Both downstream notebooks refuse to run against
a JSON whose `schemaVersion` ≠ 5.0.

## Data-quality & governance checks

`dq_issues_by_family.ipynb` flags, per family: null vendor IDs (I1),
null daily output (I5), coverage/quantity inconsistencies (I7–I9),
style/component mismatches (I11), vendor-location conflicts (I12),
duplicate assets (I13), orphan families (I14), and the v3 governance
rules — invalid Mold IDs (I15), missing PRI (I16), unpaired blockers
(I17), OT not PRI (I18), and non-standard family codes (I19).

## Notes

- The legacy→v3 component mapping (OS1→OS-PRI, MS2-1→MS-BOT-B, …) lives
  in `notebooks/mold_v3_mapping.py`; see §1.7 of the JSON structure doc.
- `scripts/update_template_v3.py` already migrated the template's
  `_dimMoldHierarchies` table and labels; re-running it is harmless but
  unnecessary. If the table is ever refreshed via Power Query, the
  upstream `master_references.xlsx` must carry the same 8 short Mold IDs.
