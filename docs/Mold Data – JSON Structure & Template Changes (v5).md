# Mold Data — JSON Structure & Template Changes (v5)

Aligned with the Bottoming Mold Master Data Standard v3.0/v3.1
(see `docs/reference/` — the source of truth for naming and governance).

Core concept (Standard §3): mold data is split into two layers —
the **Mold ID** (product definition: what a mold produces) and the
**Physical Asset** (the actual mold: vendor, size coverage, mold set,
revision, status). In the JSON, the component object is the Mold ID
layer and `assets[]` is the physical layer.

============================================================
1. JSON STRUCTURE OVERVIEW  (mold_data.json  schemaVersion 5.0)
============================================================

------------------------------------------------------------
1.1 Top-level shape
------------------------------------------------------------

{
  "schemaVersion": "5.0",
  "lastUpdated":   "YYYY-MM-DD",
  "reference":     { ... },
  "families":      { ... }
}


------------------------------------------------------------
1.2 reference block
------------------------------------------------------------

"reference": {
  "vendors": {
    "<FTY_NUMBER>": {                  ← keyed by Vendor ID, NOT generated code
      "name":      "Full legal name",
      "shortName": "Display name",
      "location":  { "code": "VN", "name": "Vietnam" }
    },
    ...
  },
  "moldShops": {
    "<CODE>": { "name": "Display name" },
    ...
  },
  "moldTypes":     { "OS": "Outsole", "MS": "Midsole", "OT": "Other" },
  "positions":     { "PRI": "Primary", "BOT": "Bottom Layer", "HEEL": "Heel" },
  "stages":        ["Default", "Blocker"],
  "assetStatuses": ["Active", "Inactive", "In Repair", "Retired"],
  "moldSets":      ["A", "B", "C", "D"]
}

Key rules:
  - vendors keyed by vendorId (FTY number) — stable, truly unique identifier
  - location lives on the vendor, not on individual asset entries
    (business rule: one vendor = one location)
  - moldTypes / positions / stages / assetStatuses / moldSets are the
    controlled vocabularies from the standard (replaces allowedSoleTypes)


------------------------------------------------------------
1.3 families block — one entry per Mold Family
------------------------------------------------------------

"families": {
  "<MOLD_FAMILY>": {
    "moldFamily":           "SA-2255",    ← renamed from moldCode
    "designFamily":         "SA-2255",    ← groups related variants; defaults to moldFamily
    "isLegacyCode":         false,        ← true for frozen non-standard codes (S1612, ...)
    "notes":                null,
    "stylesUsingThisFamily": { ... },     ← see 1.4 (unchanged from v4)
    "components": {                       ← see 1.5 — FLAT, keyed by full Mold ID
      "SA-2255-OS-PRI":  { ... },
      "SA-2255-MS-PRI":  { ... }
    }
  }
}

The Mold Family code is an OPAQUE identifier (Standard §6.1). The system
does not parse meaning from it. Width variants (SA-2017-E, SA-2654-4E)
are legitimate separate families. Frozen legacy codes (S1612) are
retained but never replicated.

Removed vs v4:
  - the intermediate "Outsole"/"Midsole" nesting level under components —
    components are now keyed directly by their governed Mold ID;
    the sole type is carried on each component as `soleType`


------------------------------------------------------------
1.4 stylesUsingThisFamily
------------------------------------------------------------

Object keyed by brand. Each value is a list of style objects.

"stylesUsingThisFamily": {
  "SAUCONY": [
    { "styleName": "ECHELON 10", "soleTypes": ["Outsole", "Midsole"] },
    { "styleName": "ECHELON 9",  "soleTypes": ["Outsole"] }
  ]
}

  soleTypes  which components this style sources from THIS family


------------------------------------------------------------
1.5 component block — the Mold ID (product definition) layer
------------------------------------------------------------

Component keys are governed Mold IDs:

    {MoldFamily}-{Type}-{Position}(-B)

    Type     ∈ {OS, MS, OT}
    Position ∈ {PRI, BOT, HEEL}
    -B       = Blocker stage suffix

"components": {
  "SA-2501-MS-BOT-B": {
    "moldId":               "SA-2501-MS-BOT-B",
    "legacyCode":           "MS2-1",          ← original source-data code (back-compat key)
    "type":                 "MS",             ← OS / MS / OT
    "position":             "BOT",            ← PRI / BOT / HEEL
    "stage":                "Blocker",        ← Default / Blocker
    "soleType":             "Midsole",        ← kept: style soleTypes + Excel lookups use it
    "componentDescription": "Midsole Bottom Layer Blocker",   ← generated, supplementary
    "constructionType":     "Vertical Split", ← derived per (family, type) — see below
    "designCompound":       "TPEE",           ← renamed from compound
    "notes":                null,

    "sourcingRules": [                ← unchanged shape; source sheets still
      { "factoryNumber": 61589,         speak legacy codes ("Sole Part" = MS2-1)
        "vendorId": "FTY000594" }
    ],

    "assets": [ ... ]                 ← see 1.6 — the Physical Asset layer
  }
}

constructionType is DERIVED from which positions exist for the same
(family, type), ignoring the -B stage (Standard §6.3):

  {PRI}            → "Single Piece"
  {PRI, BOT}       → "Vertical Split"
  {PRI, HEEL}      → "Main + Heel"
  {PRI, BOT, HEEL} → "3-Way"
  no PRI           → null  (governance gap — flagged by DQ check I16)

Removed vs v4: displayName (reconstructable from legacyCode +
componentDescription).


------------------------------------------------------------
1.6 assets block — the Physical Asset layer
------------------------------------------------------------

One entry per vendor-level asset group. NOTE on granularity: the raw
source data is vendor-row grained, not per-physical-mold, so one entry
represents all physical molds of this Mold ID held at one vendor; the
per-size detail lives in sizeCoverage. No synthetic Asset ID is
generated — records are rebuilt on every pipeline run.

"assets": [
  {
    "vendorId":         "FTY000594",  ← FK into reference.vendors
    "moldShopCode":     "LONGYU",
    "moldSet":          null,         ← standard field (A/B/C/D); not in source data — A implied
    "revision":         null,         ← standard field (integer); not in source data — 0 implied
    "status":           null,         ← Active / Inactive / In Repair / Retired — to be backfilled
    "ownership":        "WWW",
    "condition":        "1. Good",    ← legacy raw condition; NOT mapped onto status
    "conditionNote":    "OK",
    "moldCost":         1465.0,
    "initSeason":       "F22",
    "lastDemandSeason": "F26",
    "capacity": {
      "dailyOutput":  120.0,
      "actualOutput": null
    },
    "totalMoldQty":     18,
    "sizeCoverage": [                 ← renamed from inventory.coverage
      { "shoeSizes": ["3.5", "4"], "qty": 1 },
      ...
    ],
    "sizeGrouping":     "1:2",        ← derived: uniform shoeSizes length n → "1:n", else "mixed"
    "comments":         null
  }
]

vendorId may be null when the vendor has no FTY number yet; in that case
a temporary "vendorName" display field is added (same rule as v4).


------------------------------------------------------------
1.7 Legacy → v3 mapping (applied by data_processing.ipynb)
------------------------------------------------------------

Implemented in notebooks/mold_v3_mapping.py — shared by all notebooks.

Component codes (Standard §8):

  Legacy code   displayName               Mold ID suffix
  ───────────   ───────────────────────   ──────────────
  OS1           OS1 (Top)                 -OS-PRI
  OS2           OS2 (Bottom)              -OS-BOT
  MS1           MS1 (Top)                 -MS-PRI
  MS1-1         MS1 (Top - Blocker)       -MS-PRI-B
  MS2           MS2 (Bottom)              -MS-BOT
  MS2-1         MS2 (Bottom - Blocker)    -MS-BOT-B
  MS3           MS3 (Heel)                -MS-HEEL

  Rule: trailing digit 1→PRI, 2→BOT, 3→HEEL; a "-1" sub-suffix or
  "Blocker" in the display name → -B stage. Unmappable codes are
  quarantined (reason = unmappable_component_code), as are rows whose
  sole type contradicts the parsed type (reason = type_mismatch).

Family codes (Standard §6.1, documented but NOT auto-split — no Saucony
family in the current dataset carries these suffixes):

  -1 / -2 / -3 trailing digits   → Revision attribute on the asset record
  -A / -B / -C trailing letters  → Mold Set attribute on the asset record
  -E / -4E / -M / -W variants    → separate Mold Family (kept as-is)

  DQ check I19 flags candidate codes for review. Family codes are
  whitespace-stripped (fixes the historical 'SA-1517 ' duplicate).


------------------------------------------------------------
1.8 Field changes summary (v4 → v5)
------------------------------------------------------------

RENAMED
  families[*].moldCode                   → moldFamily
  components.*.compound                  → designCompound
  components.*.molds                     → assets
  molds[*].inventory.coverage            → assets[*].sizeCoverage

RESTRUCTURED
  components."Outsole"/"Midsole".<code>  → components.<MoldID>  (flat, governed key)
  molds[*].asset.{...}                   → flattened onto the asset entry
  molds[*].inventory.{...}               → flattened onto the asset entry

ADDED
  families[*].designFamily, isLegacyCode
  components.*: moldId, legacyCode, type, position, stage,
                componentDescription, constructionType
  assets[*]:    moldSet, revision, status, sizeGrouping
  reference:    moldTypes, positions, stages, assetStatuses, moldSets

REMOVED
  components.*.displayName               → use legacyCode / componentDescription
  reference.allowedSoleTypes             → superseded by reference.moldTypes


============================================================
2. EXCEL TEMPLATE CHANGES (v5)
============================================================

------------------------------------------------------------
2.1 _Master_Ref._dimMoldHierarchies
------------------------------------------------------------

Rows replaced with the 8 standard short Mold IDs (was 7 legacy codes):

  Component Code   Component Name                 Sole Type
  ──────────────   ────────────────────────────   ─────────
  OS-PRI           Outsole Primary                Outsole
  OS-BOT           Outsole Bottom Layer           Outsole
  MS-PRI           Midsole Primary                Midsole
  MS-PRI-B         Midsole Primary Blocker        Midsole
  MS-BOT           Midsole Bottom Layer           Midsole
  MS-BOT-B         Midsole Bottom Layer Blocker   Midsole
  MS-HEEL          Midsole Heel                   Midsole
  OT-PRI           Other Component                Other

The table keeps its three columns. Position and Stage are encoded in
the Component Code itself (separate columns would collide with
_dimMoldCondition at E1; deliberately omitted).

⚠ If _dimMoldHierarchies is refreshed via Power Query from
  master_references.xlsx, the upstream file must carry the same 8 rows
  or the refresh will restore the legacy codes.

------------------------------------------------------------
2.2 Label changes
------------------------------------------------------------

Summary sheet
  A1  "Mold Code:"       → "Mold Family:"
  A6  "Component Code"   → "Mold ID"

{Component} sheet
  A2  "Mold Code:"       → "Mold Family:"
  A3  "SoleType:"        → "Mold ID:"               (full governed Mold ID)
  A4  "Component Name:"  → "Component Description:"
  A5  "Compound:"        → "Design Compound:"

No columns were moved or inserted — all formulas, validations, and
protection ranges are unchanged. Mold Set / Revision / Status columns
are deliberately NOT added (all-null in source data; would shift the
H–N input zone). Documented as a future extension in the Design Spec.

------------------------------------------------------------
2.3 Sheet naming
------------------------------------------------------------

Component sheets are named by SHORT Mold ID (family prefix dropped —
sheet names are limited to 31 chars and the family is already in the
file name):

  v4:  "OS1", "MS1", "MS2-1"
  v5:  "OS-PRI", "MS-PRI", "MS-BOT-B"

Summary column A carries the same short Mold ID, so the Total Mold Qty
INDIRECT formula chain (sheet name = col A value) keeps working.

------------------------------------------------------------
2.4 Python (json_export notebook) changes
------------------------------------------------------------

CHANGED
  Component iteration   flat: for mold_id, comp in components.items()
  Sheet / col A name    short Mold ID rebuilt from type/position/stage
  Header cells          B2 family, B3 full Mold ID,
                        B4 componentDescription, B5 designCompound
  Asset fields          read from flattened assets[] / sizeCoverage
  Schema guard          raises unless schemaVersion == "5.0"

============================================================
END OF DOCUMENT
============================================================
