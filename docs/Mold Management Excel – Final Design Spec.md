# Mold Management Excel – Final Design Spec (v3)

Aligned with the Bottoming Mold Master Data Standard v3.0/v3.1
(see `docs/reference/` — source of truth for naming and governance).

Two-layer model: the **Mold ID** identifies what a mold produces
({MoldFamily}-{Type}-{Position}(-B)); the **Physical Asset** is the
actual mold at a vendor (size coverage, mold set, revision, status).
In these workbooks each Summary row = one Mold ID at one vendor
(an asset group); the component sheets hold the per-size detail.

============================================================
1. FILE STRUCTURE (PER FAMILY)
============================================================

Each Excel file = 1 Mold Family (Source of Truth)

Sheets:
1. Summary              ← Primary working interface; includes Styles section
2. {MoldID}             ← One sheet per component, named by SHORT Mold ID
                           (e.g. OS-PRI, MS-PRI, MS-BOT-B)
                           Contains both Inventory and Sourcing Rules
3. Notes                ← Free-form notes
4. _Master_Ref          ← Hidden, query-driven master tables

Sheet names use the SHORT Mold ID (family prefix dropped): the family is
already in the file name and Excel sheet names are limited to 31 chars.
Full Mold ID = {FileFamily}-{SheetName}, e.g. SA-2301.xlsx / MS-PRI-B
→ SA-2301-MS-PRI-B.

------------------------------------------------------------


============================================================
2. AVAILABLE TABLES & NAMED RANGES (GLOBAL)
============================================================

These MUST exist in TEMPLATE and MUST NOT be modified by Python.

Tables:
  - _Master_Ref._dimMoldHierarchies  ← 8 standard short Mold IDs (see 5.3)
  - _Master_Ref._dimVendor           ← MUST include Vendor ID column
  - _Master_Ref._dimMoldOwnership
  - _Master_Ref._dimMoldCondition
  - _Master_Ref._dimFactory

Named Ranges:
  - VendorList         → _Master_Ref._dimVendor[Vendor Short Name]
  - FactoryList        → _Master_Ref._dimFactory[Factory Name]
  - MoldComponentList  → _Master_Ref._dimMoldHierarchies[Component Code]
  - MoldCondition      → _Master_Ref._dimMoldCondition[Mold Condition]
  - MoldOwnership      → _Master_Ref._dimMoldOwnership[Mold Owner Ship]

------------------------------------------------------------


============================================================
3. SHEET: Summary
============================================================


------------------------------------------------------------
3.1 Header Section
------------------------------------------------------------

A1: "Mold Family:"   B1: <FamilyCode>    [Python writes B1]
A2: "Brands:"        B2: <BrandNames>    [Python writes B2]


------------------------------------------------------------
3.2 Mold Summary Table (Left Zone: A4:P31)
------------------------------------------------------------

Row 4  = Section title    A4: "Mold Summary"
Row 5  = Zone banner      A5:G5 → "References"   H5:N5 → "INPUT – EDIT HERE"
Row 6  = Column headers
Rows 7–31 = Data (25 rows max)
Col O  = MissingKeyFlag   [Hidden, formula]
Col P  = DupFlag          [Hidden, formula]

Each row = ONE Mold ID at ONE vendor (one physical-asset group).


------------------------------------------------------------
3.3 Mold Summary Column Definitions
------------------------------------------------------------

A6  Mold ID           [Dropdown → MoldComponentList; short form, e.g. MS-PRI-B]
B6  Sole Type         [Lookup: XLOOKUP(A, _dimMoldHierarchies[Component Code], [Sole Type])]
C6  Component Name    [Lookup: XLOOKUP(A, _dimMoldHierarchies[Component Code], [Component Name])]
D6  Vendor Name       [Dropdown → VendorList]
E6  Location          [Lookup: XLOOKUP(D, _dimVendor[Vendor Short Name], [Location])]

F6  Total Mold Qty    [Formula — see 3.5]
G6  Check             [Formula — see 3.6; data-entry validation flag.
                       NOT the asset Status field from the standard —
                       see 6. Future Extensions]

H6  Mold Ownership    [Dropdown → MoldOwnership]
I6  Mold Condition    [Dropdown → MoldCondition]
J6  Mold Shop         [Free text]
K6  Init Season       [Free text, validated format: S/F + 2 digits]
L6  Daily Output      [Number ≥ 0, blank allowed]
M6  Mold Init Cost    [Number ≥ 0, blank allowed]
N6  Comments          [Free text]


------------------------------------------------------------
3.4 Zone Definition (Mold Summary Table)
------------------------------------------------------------

READ-ONLY  A:G, O:P
EDITABLE   H:N

Users MUST NOT modify structure.


------------------------------------------------------------
3.5 Total Mold Qty Formula
------------------------------------------------------------

IMPORTANT: Formula references the component sheet by the short Mold ID
           in column A directly. Sheet name = value in column A.

=IF(G7="OK",
  LET(
    comp, A7,
    ven,  D7,
    sh,   comp,
    hdrRow, 8,
    col, MATCH(ven, INDIRECT("'"&sh&"'!"&hdrRow&":"&hdrRow), 0),
    SUM(INDEX(INDIRECT("'"&sh&"'!A:ZZ"), 0, col))
  ),
"")

It finds the vendor's column on the component sheet (header row 8) and
sums that column's quantities.


------------------------------------------------------------
3.6 Check Formula
------------------------------------------------------------

=IF(OR(A7<>"", D7<>""),
  IFS(O7, "Missing Keys",
      P7, "Duplicate Keys",
      TRUE, "OK"),
"")

  Missing Keys   → Mold ID or Vendor is blank while the other is filled
  Duplicate Keys → Same Mold ID + Vendor combination appears more than once
  OK             → Valid row

Hidden flag columns:
  O7 → =OR(ISBLANK(A7), ISBLANK(D7))
  P7 → =COUNTIFS($A$7:$A$31,$A7,$D$7:$D$31,$D7)>1

Conditional format: row turns RED if Check ≠ "OK"

NOTE: this is a data-entry validation flag ("Check"), distinct from the
asset lifecycle Status (Active / Inactive / In Repair / Retired) defined
in the standard. Avoid calling this column "Status".


------------------------------------------------------------
3.7 Styles Section (Right Zone: R4:T31)
------------------------------------------------------------

Sits to the right of the Mold Summary table. Users edit here to declare
which styles use this mold family and which components they use.

Row 4  = Section title    R4: "Styles Using This Family"
Row 5  = Banner           R5: "Input Style Name"
Row 6  = Column headers   R6: Style Name   S6: Outsole   T6: Midsole
Rows 7–31 = Input (25 rows max)

S7:T31  Checkbox columns   1 = used   0 = not used


------------------------------------------------------------
3.8 Styles Section Rules
------------------------------------------------------------

- A style may have Outsole only, Midsole only, or both checked
- Python writes style names (R) and checkbox values (S, T)
- Users may light-edit styles; no heavy validation required
- No dropdown validation on R column (free text)

One Style → one Mold Family; one Mold Family → many Styles (Standard §9).

------------------------------------------------------------


============================================================
4. SHEET: {MoldID}  (e.g. OS-PRI, MS-PRI, MS-BOT-B)
============================================================


------------------------------------------------------------
4.1 Purpose
------------------------------------------------------------

One sheet per component (Mold ID) in the family.
Sheet name = SHORT Mold ID exactly (must match Summary col A).

Contains two side-by-side sections:
  LEFT   A:E  → Inventory grid (size patterns × vendors)
  RIGHT  H:M  → Sourcing Rules (factory → vendor allocation)

Both sections share the same row range (rows 9–43).


------------------------------------------------------------
4.2 Header (Rows 1–6)
------------------------------------------------------------

Row 1  A1: "Mold Inventory"           [Section title, static]
Row 2  A2: "Mold Family:"             B2: <FamilyCode>             [Python writes B2]
Row 3  A3: "Mold ID:"                 B3: <Full Mold ID>           [Python writes B3]
Row 4  A4: "Component Description:"   B4: <ComponentDescription>   [Python writes B4]
Row 5  A5: "Design Compound:"         B5: <DesignCompound>         [Python writes B5]
Row 6  [blank]

B3 carries the FULL governed Mold ID (e.g. SA-2301-MS-PRI-B); the sheet
name carries the short form. Sole type, position, and stage are all
encoded in the Mold ID.


------------------------------------------------------------
4.3 Instruction Row (Row 7)
------------------------------------------------------------

A7: "Edit ShoeSizes as comma-separated list (e.g., 3.5, 4).
     Do not Merge, Insert/Delete Column. Leave blank if unknown."

H7: "Select Factory and Vendor from Dropdown List."


------------------------------------------------------------
4.4 Column Header Row (Row 8)
------------------------------------------------------------

INVENTORY SIDE
  A8  Sizes         [Locked, static]
  B8:E8  Vendor headers   [Dropdown → VendorList; Python writes values]

SOURCING SIDE
  H8  Factory Name      [Header, static]
  I8  Factory Location  [Header, static — auto-filled by formula]
  J8  Factory Code      [Header, static — auto-filled by formula]
  K8  Vendor Short Name [Header, static]
  L8  Vendor Location   [Header, static — auto-filled by formula]
  M8  Vendor Code       [Header, static — returns Vendor ID (FTY)]


------------------------------------------------------------
4.5 Data Range (Rows 9–43, 35 rows)
------------------------------------------------------------

INVENTORY SIDE  A9:E43

  A   Sizes        Comma-separated shoe sizes covered by one physical
                   mold size (a size-coverage pattern, e.g. "3.5, 4").
                   One row per distinct pattern. [Editable, free text]
  B–E Qty per Vendor   Number ≥ 0, blank allowed [Editable]

  Max 4 vendor columns (B–E). Owner extends template if more needed.

  The size patterns correspond 1:1 with the sizeCoverage entries on the
  asset records in mold_data.json. Two patterns sharing a base size but
  covering different ranges (e.g. "3.5" vs "3.5, 4, 4.5") are distinct
  physical mold types and occupy separate rows.

SOURCING SIDE  H9:M43

  H   Factory Name      [Dropdown → FactoryList, user-entered]
  I   Factory Location  [Auto: XLOOKUP(H, _dimFactory[Factory Name], [Factory Country])]
  J   Factory Code      [Auto: XLOOKUP(H, _dimFactory[Factory Name], [Factory Number])]
  K   Vendor Short Name [Dropdown → VendorList, user-entered]
  L   Vendor Location   [Auto: XLOOKUP(K, _dimVendor[Vendor Short Name], [Location])]
  M   Vendor Code       [Auto: XLOOKUP(K, _dimVendor[Vendor Short Name], [Vendor ID])]

  Rows are not tied to inventory rows — a sourcing rule in row 9 is
  unrelated to the size pattern in col A row 9. Users fill from row 9
  downward. 35 rows available.


------------------------------------------------------------
4.6 Validation
------------------------------------------------------------

  B8:E8   → VendorList   (vendor short name for inventory header)
  B9:E43  → ≥ 0 numeric  (inventory quantities)
  H9:H43  → FactoryList  (factory name dropdown)
  K9:K43  → VendorList   (vendor short name for sourcing)

  I, J, L, M: auto-filled via XLOOKUP — no manual input required


------------------------------------------------------------
4.7 Protection
------------------------------------------------------------

Allow edit:
  A9:A43    Size patterns
  B8:E8     Vendor header dropdowns
  B9:E43    Inventory quantities
  H9:H43    Factory Name (sourcing)
  K9:K43    Vendor Short Name (sourcing)

Block:
  All other cells — structure changes, formulas, headers


------------------------------------------------------------
4.8 Python Responsibility
------------------------------------------------------------

Write:
  B2        Family code
  B3        Full Mold ID
  B4        Component description
  B5        Design compound
  A9:A43    Size patterns (from assets[*].sizeCoverage)
  B8:E8     Vendor short name headers (up to 4)
  B9:E43    Inventory quantities (by vendor column × pattern row)
  H9:H{9+n-1}   Factory names (sourcing rules)
  K9:K{9+n-1}   Vendor short names (sourcing rules)

Do NOT touch:
  Row 7 instructions, row 8 sourcing headers, I/J/L/M formula columns


------------------------------------------------------------


============================================================
5. SHEET: _Master_Ref
============================================================


------------------------------------------------------------
5.1 Purpose
------------------------------------------------------------

Master data source for all validation and lookups.


------------------------------------------------------------
5.2 Data Source
------------------------------------------------------------

Loaded via Power Query from:

    master_references.xlsx

⚠ The template's _dimMoldHierarchies was migrated in place to the v3
  short Mold IDs (scripts/update_template_v3.py). If the table is
  refreshed from master_references.xlsx, the upstream file must carry
  the same 8 rows or the refresh restores the legacy codes.


------------------------------------------------------------
5.3 Tables
------------------------------------------------------------

_dimMoldHierarchies   Component Code, Component Name, Sole Type
_dimVendor            Vendor ID, Vendor Short Name, Vendor Full Name, Location, ...
_dimMoldOwnership     Mold Ownership values
_dimMoldCondition     Mold Condition values
_dimFactory           Factory Number, Factory Name, Factory Country, ...

_dimMoldHierarchies standard rows (Component Code = short Mold ID):

  OS-PRI     Outsole Primary                Outsole
  OS-BOT     Outsole Bottom Layer           Outsole
  MS-PRI     Midsole Primary                Midsole
  MS-PRI-B   Midsole Primary Blocker        Midsole
  MS-BOT     Midsole Bottom Layer           Midsole
  MS-BOT-B   Midsole Bottom Layer Blocker   Midsole
  MS-HEEL    Midsole Heel                   Midsole
  OT-PRI     Other Component                Other

Position (PRI/BOT/HEEL) and Stage (-B) are encoded in the Component
Code; the table deliberately has no separate Position/Stage columns
(they would collide with _dimMoldCondition at column E).


------------------------------------------------------------
5.4 _dimVendor Requirements
------------------------------------------------------------

MUST include a "Vendor ID" column containing the FTY number.
The {MoldID} sheet column M formula uses this column:

    XLOOKUP(K9, _dimVendor[Vendor Short Name], _dimVendor[Vendor ID], "")

This returns the stable FTY identifier used in mold_data.json.


------------------------------------------------------------
5.5 Rules
------------------------------------------------------------

- Hidden sheet
- Protected — no user editing
- NEVER modified by Python exports
- Updated only via Power Query refresh (or the one-time migration script)


------------------------------------------------------------


============================================================
6. SYSTEM PRINCIPLES & FUTURE EXTENSIONS
============================================================

1. Structure controlled by owner
2. Users edit only allowed cells
3. Master data centralized in _Master_Ref (Power Query)
4. All relationships enforced via dropdown + XLOOKUP lookup
5. Errors visible, not hidden
6. Excel acts as controlled UI, not free-form data entry
7. Sourcing Rules are component-specific — stored on each {MoldID} sheet
8. Styles are family-level — stored on Summary sheet
9. No freeform mold identifiers — Summary col A is restricted to the
   governed short Mold IDs in MoldComponentList (Standard §9.1)

FUTURE EXTENSIONS (deliberately not implemented yet):
  - Mold Set (A/B/C/D), Revision, and asset Status columns on Summary.
    The standard defines them as asset attributes, but the current
    source data carries no values; adding columns now would shift the
    H–N input zone and break formulas/protection for no data. When the
    business starts tracking them, extend the Summary table to the
    right of N and add dimension tables for Status and Mold Set.
============================================================
END OF SPEC
============================================================
