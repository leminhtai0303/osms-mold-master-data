# Mold Management Excel – Final Design Spec (v2)

============================================================
1. FILE STRUCTURE (PER FAMILY)
============================================================

Each Excel file = 1 Mold Family (Source of Truth)

Sheets:
1. Summary              ← Primary working interface; includes Styles section
2. {ComponentCode}      ← One sheet per component (e.g. OS1, MS1)
                           Contains both Inventory and Sourcing Rules
3. _Master_Ref          ← Hidden, query-driven master tables

NOTE: Standalone "Sourcing Rule" and "Styles" sheets have been removed.
      Their data is now embedded in the sheets above.

------------------------------------------------------------


============================================================
2. AVAILABLE TABLES & NAMED RANGES (GLOBAL)
============================================================

These MUST exist in TEMPLATE and MUST NOT be modified by Python.

Tables:
  - _Master_Ref._dimMoldHierarchies
  - _Master_Ref._dimVendor          ← MUST include Vendor ID column
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

A1: "Mold Code:"   B1: <FamilyCode>    [Python writes B1]
A2: "Brands:"      B2: <BrandNames>    [Python writes B2]


------------------------------------------------------------
3.2 Mold Summary Table (Left Zone: A4:P31)
------------------------------------------------------------

Row 4  = Section title    A4: "Mold Summary"
Row 5  = Zone banner      A5:G5 → "References"   H5:N5 → "INPUT – EDIT HERE"
Row 6  = Column headers
Rows 7–31 = Data (25 rows max)
Col O  = MissingKeyFlag   [Hidden, formula]
Col P  = DupFlag          [Hidden, formula]


------------------------------------------------------------
3.3 Mold Summary Column Definitions
------------------------------------------------------------

A6  Component Code    [Dropdown → MoldComponentList]
B6  Sole Type         [Lookup: XLOOKUP(A, _dimMoldHierarchies[Component Code], [Sole Type])]
C6  Component Name    [Lookup: XLOOKUP(A, _dimMoldHierarchies[Component Code], [Component Name])]
D6  Vendor Name       [Dropdown → VendorList]
E6  Location          [Lookup: XLOOKUP(D, _dimVendor[Vendor Short Name], [Location])]

F6  Total Mold Qty    [Formula — see 3.5]
G6  Status Check      [Formula — see 3.6]

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

IMPORTANT: Formula references the component sheet by its component code
           directly (no prefix). Sheet name = value in column A.

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

⚠ Previous version used "MoldInv_"&A7 — that prefix has been removed.
  Any existing files built from the old template must have this formula
  updated when the component sheet is renamed.


------------------------------------------------------------
3.6 Status Check Formula
------------------------------------------------------------

=IF(OR(A7<>"", D7<>""),
  IFS(O7, "Missing Keys",
      P7, "Duplicate Keys",
      TRUE, "OK"),
"")

  Missing Keys  → Component Code or Vendor is blank while the other is filled
  Duplicate Keys → Same Sole Type + Vendor combination appears more than once
  OK            → Valid row

Conditional format: row turns RED if Status ≠ "OK"


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


------------------------------------------------------------


============================================================
4. SHEET: {ComponentCode}
============================================================


------------------------------------------------------------
4.1 Purpose
------------------------------------------------------------

One sheet per component in the family (e.g. OS1, MS1, MS2).
Sheet name = Component Code exactly (e.g. "OS1").

Contains two side-by-side sections:
  LEFT   A:G  → Inventory grid (mold sizes × vendors)
  RIGHT  H:M  → Sourcing Rules (factory → vendor allocation)

Both sections share the same row range (rows 9–43).


------------------------------------------------------------
4.2 Header (Rows 1–6)
------------------------------------------------------------

Row 1  A1: "Mold Inventory"    [Section title, static]
Row 2  A2: "Mold Code:"        B2: <FamilyCode>    [Python writes B2]
Row 3  A3: "SoleType:"         B3: <SoleType>      [Python writes B3]
Row 4  A4: "Component Name:"   B4: <DisplayName>   [Python writes B4]
Row 5  A5: "Compound:"         B5: <Compound>      [Python writes B5]
Row 6  [blank]


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
  A8  MoldSize      [Locked, static]
  B8  ShoeSizes     [Header, static]
  C8  Vendor_1      [Dropdown → VendorList]
  D8  Vendor_2      [Dropdown → VendorList]
  E8  Vendor_3      [Dropdown → VendorList]
  F8  Vendor_4      [Dropdown → VendorList]
  G8  TotalQty      [Formula header, static]

SOURCING SIDE
  H8  Factory Name      [Header, static]
  I8  Factory Location  [Header, static — auto-filled by formula]
  J8  Factory Code      [Header, static — auto-filled by formula]
  K8  Vendor Short Name [Header, static]
  L8  Vendor Location   [Header, static — auto-filled by formula]
  M8  Vendor Code       [Header, static — returns Vendor ID (FTY)]


------------------------------------------------------------
4.5 Data Range (Rows 9–43, 35 rows = mold sizes 1.0 → 18.0)
------------------------------------------------------------

INVENTORY SIDE  A9:G43

  A   MoldSize      Fixed: 1, 1.5, 2, … 18  [Locked]
  B   ShoeSizes     Comma-separated shoe sizes [Editable, free text]
  C–F Qty per Vendor  Number ≥ 0, blank allowed [Editable]
  G   TotalQty      Formula: SUM(C:F) for that row [Locked]

  Max 4 vendor columns (C–F). Owner extends template if more needed.

SOURCING SIDE  H9:M43

  H   Factory Name      [Dropdown → FactoryList, user-entered]
  I   Factory Location  [Auto: XLOOKUP(H, _dimFactory[Factory Name], [Factory Country])]
  J   Factory Code      [Auto: XLOOKUP(H, _dimFactory[Factory Name], [Factory Number])]
  K   Vendor Short Name [Dropdown → VendorList, user-entered]
  L   Vendor Location   [Auto: XLOOKUP(K, _dimVendor[Vendor Short Name], [Location])]
  M   Vendor Code       [Auto: XLOOKUP(K, _dimVendor[Vendor Short Name], [Vendor ID])]

  Rows are not tied to mold sizes — a sourcing rule in row 9 is unrelated
  to mold size 1.0 in col A row 9. Users fill from row 9 downward.
  35 rows available; sufficient for all factory-vendor combinations.


------------------------------------------------------------
4.6 Validation
------------------------------------------------------------

  C8:F8   → VendorList   (vendor short name for inventory header)
  C9:F43  → ≥ 0 numeric  (inventory quantities)
  H9:H43  → FactoryList  (factory name dropdown)
  K9:K43  → VendorList   (vendor short name for sourcing)

  I, J, L, M: auto-filled via XLOOKUP — no manual input required


------------------------------------------------------------
4.7 Protection
------------------------------------------------------------

Allow edit:
  B9:B43    ShoeSizes
  C8:F8     Vendor header dropdowns
  C9:F43    Inventory quantities
  H9:H43    Factory Name (sourcing)
  K9:K43    Vendor Short Name (sourcing)

Block:
  All other cells — structure changes, formulas, headers


------------------------------------------------------------
4.8 Python Responsibility
------------------------------------------------------------

Write:
  B2        Family code
  B3        Sole type
  B4        Component display name
  B5        Compound
  B9:B43    Shoe sizes (sizing rules from JSON)
  C8:F8     Vendor short name headers (up to 4)
  C9:F43    Inventory quantities (by vendor column)
  H9:H{9+n-1}   Factory names (sourcing rules)
  K9:K{9+n-1}   Vendor short names (sourcing rules)

Do NOT touch:
  Row 7 instructions, row 8 sourcing headers, I/J/L/M formula columns,
  mold size column A, G TotalQty formulas


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


------------------------------------------------------------
5.3 Tables
------------------------------------------------------------

_dimMoldHierarchies   Component Code, Sole Type, Component Name
_dimVendor            Vendor Short Name, Vendor Full Name, Vendor ID, Location
_dimMoldShop          Mold Shop Name
_dimMoldOwnership     Mold Ownership values
_dimMoldCondition     Mold Condition values
_dimFactory           Factory Name, Factory Number, Factory Country


------------------------------------------------------------
5.4 _dimVendor Requirements
------------------------------------------------------------

MUST include a "Vendor ID" column containing the FTY number.
The {Component} sheet column M formula uses this column:

    XLOOKUP(K9, _dimVendor[Vendor Short Name], _dimVendor[Vendor ID], "")

This returns the stable FTY identifier used in mold_data.json.


------------------------------------------------------------
5.5 Rules
------------------------------------------------------------

- Hidden sheet
- Protected — no user editing
- NEVER modified by Python
- Updated only via Power Query refresh


------------------------------------------------------------


============================================================
6. SYSTEM PRINCIPLES
============================================================

1. Structure controlled by owner
2. Users edit only allowed cells
3. Master data centralized in _Master_Ref (Power Query)
4. All relationships enforced via dropdown + XLOOKUP lookup
5. Errors visible, not hidden
6. Excel acts as controlled UI, not free-form data entry
7. Sourcing Rules are component-specific — stored on each {Component} sheet
8. Styles are family-level — stored on Summary sheet


============================================================
END OF SPEC
============================================================
