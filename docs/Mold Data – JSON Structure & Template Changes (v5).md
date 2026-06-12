# Mold Data — JSON Structure & Template Changes (v3)

============================================================
1. JSON STRUCTURE OVERVIEW  (mold_data.json  schemaVersion 3.0)
============================================================

------------------------------------------------------------
1.1 Top-level shape
------------------------------------------------------------

{
  "schemaVersion": "3.0",
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
  "allowedSoleTypes": ["Outsole", "Midsole"]
}

Key rules:
  - vendors keyed by vendorId (FTY number) — stable, truly unique identifier
  - vendorCode (generated string) is NOT stored anywhere in v3
  - location lives on the vendor, not on individual mold entries
    (business rule: one vendor = one location)


------------------------------------------------------------
1.3 families block — one entry per mold family
------------------------------------------------------------

"families": {
  "<MOLD_CODE>": {
    "moldCode":             "SA-2255",
    "notes":                null,
    "stylesUsingThisFamily": { ... },   ← see 1.4
    "components": {                     ← see 1.5
      "Outsole": { ... },
      "Midsole": { ... }
    }
  }
}

Removed vs v2:
  - "brands": []  was always empty — removed
  - "sourcingRules": [] at family level — moved inside each component
  - "sizingRulesByComponent": {} at family level — moved inside each component


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
             ["Outsole", "Midsole"]  — uses both components
             ["Outsole"]             — uses only the outsole
             ["Midsole"]             — uses only the midsole

Previously (v2): flat array [{ "brand": "SAUCONY", "styleName": "..." }]
  — brand was duplicated on every row, soleTypes did not exist


------------------------------------------------------------
1.5 component block
------------------------------------------------------------

"components": {
  "Outsole": {
    "OS1": {
      "displayName":  "OS1 (Top)",
      "compound":     "Rubber",
      "notes":        null,

      "sizingRules": {                  ← was sizingRulesByComponent at family level
        "moldSizeToShoeSizes": {
          "3.5": ["3.5", "4"],
          "4.5": ["4.5", "5"],
          ...
          "14": ["14"]
        }
      },

      "sourcingRules": [                ← was sourcingRules at family level
        { "factoryNumber": 61589, "vendorId": "FTY000594" },
        { "factoryNumber": 62430, "vendorId": "FTY000594" }
      ],

      "molds": [                        ← one entry per vendor holding molds
        {
          "vendorId":     "FTY000594",  ← FK into reference.vendors
          "vendorName":   null,         ← only present when vendorId is null (pending FTY)
          "moldShopCode": "LONGYU",
          "initSeason":   "F22",
          "lastDemandSeason": "F26",
          "capacity": {
            "dailyOutput":  120.0,
            "actualOutput": null
          },
          "asset": {
            "moldCost":      1465.0,
            "ownership":     "WWW",
            "condition":     "1. Good",
            "conditionNote": "OK"
          },
          "inventory": {
            "totalMoldQty": 18,
            "qtyByMoldSize": {
              "3.5": 1, "4.5": 1, "5.5": 2, ...
            }
          },
          "comments": null
        }
      ]
    }
  }
}


------------------------------------------------------------
1.6 Null vendorId molds
------------------------------------------------------------

A mold entry is allowed to have vendorId: null when the vendor has not yet
been assigned a Vendor ID (FTY number) in the master reference.

In this case, add vendorName as a temporary display-only field:

  { "vendorId": null, "vendorName": "JIATAI-VN(HONGCHEN)", ... }

Once the FTY is registered:
  - add the vendor to reference.vendors keyed by the new FTY
  - replace vendorId: null + vendorName with the real FTY
  - drop vendorName


------------------------------------------------------------
1.7 Field changes summary (v2 → v3)
------------------------------------------------------------

REMOVED
  reference.vendors key was generated vendorCode  → now vendorId (FTY)
  reference.vendors[*].vendorCode field            → removed
  families[*].brands                               → removed (always empty)
  families[*].sourcingRules (family-level)         → moved into each component
  families[*].sizingRulesByComponent (family-level)→ moved into each component
  molds[*].vendorCode                              → removed (not stable)
  molds[*].vendorName                              → removed (except null-FTY fallback)
  molds[*].vendorShortName                         → removed (resolve from reference)
  molds[*].location                                → removed (resolve from vendor reference)
  molds[*].moldShopName                            → removed (resolve from reference.moldShops)
  molds[*].remark                                  → merged into comments

ADDED
  reference.vendors[*].location                   ← vendor has one location
  families[*].components.*.*. sizingRules          ← was family-level lookup
  families[*].components.*.*. sourcingRules        ← was family-level, included soleType+solePart
  stylesUsingThisFamily keyed by brand             ← was flat array
  stylesUsingThisFamily[brand][*].soleTypes        ← new field

CHANGED
  sourcingRules entries: removed soleType, solePart ← redundant when inside component
  molds[*].vendorId: now the ONLY vendor identifier on a mold entry


============================================================
2. EXCEL TEMPLATE CHANGES
============================================================

------------------------------------------------------------
2.1 Sheet structure
------------------------------------------------------------

VERSION 2 (old)                  VERSION 3 (new)
─────────────────────────────    ──────────────────────────────────────
1. Summary                       1. Summary  (+ Styles section added)
2. MoldInv_{ComponentCode}       2. {ComponentCode}  (renamed; + Sourcing
3. Sourcing Rule  ← removed         Rules section added)
4. Styles         ← removed      3. _Master_Ref  (unchanged)
5. _Master_Ref

Standalone Sourcing Rule and Styles sheets eliminated.
Their data is now embedded in the sheets above.


------------------------------------------------------------
2.2 Summary sheet changes
------------------------------------------------------------

ADDED — Styles section (right of main table)

  R4        Section title: "Styles Using This Family"
  R5        Banner: "Input Style Name"
  R6        Column headers: Style Name | Outsole | Midsole
  R7:T31    Input range (25 rows)
              R = style name (free text)
              S = Outsole flag  (1 = uses this family's outsole, 0 = does not)
              T = Midsole flag  (1 = uses this family's midsole, 0 = does not)

CHANGED — Total Mold Qty formula (col F)

  Old:  sh = "MoldInv_" & A7     ← hardcoded prefix, breaks on rename
  New:  sh = A7                  ← component code is now the sheet name directly

  ⚠ Any files generated from the old template must have this formula
    updated in F7:F31 before use with the new component sheet names.


------------------------------------------------------------
2.3 {ComponentCode} sheet changes
------------------------------------------------------------

RENAMED
  MoldInv_{ComponentCode}  →  {ComponentCode}   (e.g. "OS1", "MS1")
  Sheet name must exactly match the Component Code used in Summary col A.

ADDED — Sourcing Rules section (right of inventory grid)

  Layout: columns H–M, rows 7–43

  H7        Instruction: "Select Factory and Vendor from Dropdown List."
  H8:M8     Column headers (static, locked):
              H8 Factory Name       I8 Factory Location   J8 Factory Code
              K8 Vendor Short Name  L8 Vendor Location    M8 Vendor Code

  H9:H43    Factory Name       [Dropdown → FactoryList, user-entered]
  I9:I43    Factory Location   [Auto: XLOOKUP from _dimFactory[Factory Country]]
  J9:J43    Factory Code       [Auto: XLOOKUP from _dimFactory[Factory Number]]
  K9:K43    Vendor Short Name  [Dropdown → VendorList, user-entered]
  L9:L43    Vendor Location    [Auto: XLOOKUP from _dimVendor[Location]]
  M9:M43    Vendor Code        [Auto: XLOOKUP from _dimVendor[Vendor ID]]
              ↑ "Vendor Code" column returns the Vendor ID (FTY number)

  35 rows available (rows 9–43, shared row range with inventory grid).
  Rows are independent of mold sizes — fill sourcing from row 9 downward.

CLARIFIED — Inventory vendor columns

  Max 4 vendor columns: C, D, E, F  (not 6 as previously stated)
  Vendor header dropdowns:  C8:F8  → VendorList
  Inventory qty validation: C9:F43 → number ≥ 0


------------------------------------------------------------
2.4 _Master_Ref changes
------------------------------------------------------------

_dimVendor table MUST include a "Vendor ID" column containing the FTY number.

This column is required by the Sourcing Rules section on each component sheet:

  M9 = XLOOKUP(K9, _dimVendor[Vendor Short Name], _dimVendor[Vendor ID], "")

The Vendor ID returned here is the stable FK that links back to
reference.vendors in mold_data.json.

All other tables and named ranges unchanged.


------------------------------------------------------------
2.5 Python (json_export notebook) changes
------------------------------------------------------------

CHANGED
  Vendor short name resolution
    Old: mold["vendorShortName"]
    New: reference["vendors"][mold["vendorId"]]["shortName"]
         with fallback to mold["vendorName"] when vendorId is null

  Sizing rules source
    Old: fam["sizingRulesByComponent"][comp_code]
    New: comp["sizingRules"]

  Sourcing rules source
    Old: fam["sourcingRules"]  (family-level, includes soleType/solePart)
    New: flatten comp["sourcingRules"] across all components
         (component context is known from iteration)

  Styles iteration
    Old: for s in fam["stylesUsingThisFamily"]: s["styleName"]
    New: for brand, styles in fam["stylesUsingThisFamily"].items():
             for s in styles: s["styleName"], s["soleTypes"]

  Vendor header write range
    Old: C8:H8  (6 columns)
    New: C8:F8  (4 columns)

  Component sheet name
    Old: "MoldInv_" + comp_code
    New: comp_code  (no prefix)

ADDED
  Write sourcing rules to component sheet
    H9:H{9+n-1}  factory names
    K9:K{9+n-1}  vendor short names
    (I, J, L, M auto-fill via XLOOKUP — Python does not touch them)

  Write styles to Summary sheet
    R7:R{7+n-1}  style names
    S7:S{7+n-1}  outsole flags  (1 or None)
    T7:T{7+n-1}  midsole flags  (1 or None)

REMOVED
  write_sourcing_rules() function  ← logic distributed into write_summary()
                                      and write_component_sheet()


============================================================
END OF DOCUMENT
============================================================
