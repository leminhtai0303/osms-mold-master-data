# Mold Management Excel – Final Design Spec (v1)

============================================================
1. FILE STRUCTURE (PER FAMILY)
============================================================

Each Excel file = 1 Mold Family (Source of Truth)

Sheets:
1. Summary                     ← Primary working interface
2. MoldInv_{ComponentCode}    ← Inventory management (per component)
3. Sourcing Rule              ← Rare update (controlled rows)
4. Styles                     ← Rare update
5. _Master_Ref                ← Hidden, query-driven master tables


------------------------------------------------------------


============================================================
2. AVAILABLE TABLERS & NAMED RANGES (GLOBAL)
============================================================

These MUST exist in TEMPLATE and MUST NOT be modified by Python.
Tables:
  - _Master_Ref._dimMoldHierarchies
  - _Master_Ref._dimVendor  
  - _Master_Ref._dimMoldOwnership
  - _Master_Ref._dimMoldCondition
  - _Master_Ref._dimFactory

Name Range:
  - VendorList → _Master_Ref._dimVendor[Vendor Short Name]

  - FactoryList → _Master_Ref._dimFactory[Factory Name]

  - MoldComponentList → _Master_Ref._dimMoldHierarchies[Component Code]

  - MoldCondition → _Master_Ref._dimMoldCondition[Mold Condition]

  - MoldOwnership → _Master_Ref._dimMoldOwnership[Mold Ownership]


------------------------------------------------------------


============================================================
3. SHEET: Summary (Mold Summary)
============================================================


------------------------------------------------------------
3.1 Header Section
------------------------------------------------------------

A1: Mold Family  
A2: <FamilyCode>

B1: Brand  
B2: <BrandName>


------------------------------------------------------------
3.2 Table Layout
------------------------------------------------------------

Row 4 = Table Name
A4:N4 → Mold Summary

Row 5 = Banner
A5:G5 → REFERENCE – DO NOT EDIT  
H5:N5 → INPUT – EDIT HERE

Rows 6 = Table Header

------------------------------------------------------------
3.3 Column Definitions
------------------------------------------------------------

A6  Component Code        [Dropdown → MoldComponentList]
B6  Sole Type             [Lookup → _Master_Ref]
C6  Component Name        [Lookup → _Master_Ref]
D6  Vendor Short Name     [Dropdown → VendorList]
E6  Location              [Dropdown → _Master_Ref]

F6  Total Mold Qty        [Formula, whole number]
G6  Status Check          [Formula]

H6  Mold Shop             [Free text]
I6  Mold Ownership        [Dropdown → MoldOwnership]
J6  Mold Condition        [Dropdown → MoldCondition]
K6  Init Season           [Free text]
L6  Daily Output          [Number ≥ 0, blank allowed]
M6  Mold Init Cost        [Number ≥ 0, blank allowed]
N6  Comments              [Free text]


------------------------------------------------------------
3.4 Zone Definition
------------------------------------------------------------

READ-ONLY (A:G)
EDITABLE (H:N)

Users MUST NOT modify structure


------------------------------------------------------------
3.5 Calculation Logic
------------------------------------------------------------

Total Mold Qty:

=IFERROR(
  LET(
    sh,"MoldInv_"&$A7,
    ven,$D7,
    col,MATCH(ven,INDIRECT("'"&sh&"'!8:8"),0),
    SUM(INDEX(INDIRECT("'"&sh&"'!A:ZZ"),0,col))
  ),
"")


------------------------------------------------------------
3.6 Validation
------------------------------------------------------------

Daily Output, Mold Cost:
    ≥ 0, allow blank

Dropdown fields:
    MUST use named ranges


------------------------------------------------------------
3.7 Error Handling
------------------------------------------------------------

Status Check:

    ERR_DUP
    ERR_BADNUM
    OK

Conditional Format:
    Row turns RED if Status != OK


------------------------------------------------------------


============================================================
4. SHEET: MoldInv_{Component}
============================================================


------------------------------------------------------------
4.1 Purpose
------------------------------------------------------------

ONLY place user edits inventory quantities


------------------------------------------------------------
4.2 Layout
------------------------------------------------------------

Row 1–6: Header + instructions

Row 7 = Table Header

Columns:

A   MoldSize       [Locked]
B   ShoeSizes      [Editable]

C   Vendor_1       [Dropdown header]
D   Vendor_2       [Dropdown header]
E   Vendor_3       [Dropdown header]
F   Vendor_4       [Dropdown header]

(Expandable by owner)

G   TotalQty       [Formula optional]


------------------------------------------------------------
4.3 Vendor Header Rules
------------------------------------------------------------

C7:F7:

    Dropdown:
        =VendorList

    Additional allowed:
        NOT_USED


MUST match Summary Vendor Short Name


------------------------------------------------------------
4.4 Freeze Pane
------------------------------------------------------------

Freeze at:

    C8

Keeps:
    MoldSize + ShoeSizes visible


------------------------------------------------------------
4.5 Data Input
------------------------------------------------------------

C8:F rows:

    Number ≥ 0
    Blank allowed

NO text allowed


------------------------------------------------------------
4.6 Mold Size
------------------------------------------------------------

Fixed list:

    1 → 18 (step 0.5)

Users CANNOT add rows


------------------------------------------------------------
4.7 Conditional Formatting
------------------------------------------------------------

Highlight if:
    - invalid number
    - negative value

Optional:
    Qty > 0 and ShoeSizes empty


------------------------------------------------------------
4.8 Protection
------------------------------------------------------------

Allow edit:
    B column, C–F columns (data only)

Block:
    structure changes


------------------------------------------------------------
4.9 Python Responsibility
------------------------------------------------------------

- Set Vendor headers & dropdown
- Populate quantities
- Do NOT modify layout


------------------------------------------------------------


============================================================
5. SHEET: Sourcing Rule
============================================================


------------------------------------------------------------
5.1 Purpose
------------------------------------------------------------

Capture Factory × Component → Vendor relation


------------------------------------------------------------
5.2 Layout
------------------------------------------------------------

Row 1–2: Header + instructions

Row 4: Table header

Columns:

Factory Name        [Dropdown → FactoryList]
Factory Location    [Reference]
Factory Code        [Reference]

Component           [Reference]
Component Code      [Dropdown → MoldComponentList]

Vendor Short Name   [Dropdown → VendorList]
Vendor Location     [Reference]
Vendor Code         [Reference]

Table Max rows: 20

------------------------------------------------------------
5.3 Rules
------------------------------------------------------------

- User can edit ONLY within 20 rows
- Cannot insert rows
- Owner extends template if needed


------------------------------------------------------------
5.4 Python Behavior
------------------------------------------------------------

- Fill max 20 rows
- If exceed:
    truncate + log warning


------------------------------------------------------------


============================================================
6. SHEET: Styles
============================================================


------------------------------------------------------------
6.1 Purpose
------------------------------------------------------------

Track styles using the mold family


------------------------------------------------------------
6.2 Layout
------------------------------------------------------------

Row 1–2: Header + instructions

Row 4: Table header

Column:
StyleName           [Free text]
OutSole             [Check box]
MidSole             [Check box]
------------------------------------------------------------
6.3 Rules
------------------------------------------------------------

- Light editing allowed
- No heavy validation required
------------------------------------------------------------


============================================================
7. SHEET: _Master_Ref
============================================================


------------------------------------------------------------
7.1 Purpose
------------------------------------------------------------

Master data source for validation + lookup


------------------------------------------------------------
7.2 Data Source
------------------------------------------------------------

Loaded via Power Query from:

    master_references.xlsx


------------------------------------------------------------
7.3 Tables
------------------------------------------------------------

_dimMoldHierachies
_dimVendor
_dimMoldShop
_dimMoldOwnership
_dimMoldCondition
_dimFactory


------------------------------------------------------------
7.4 Rules
------------------------------------------------------------

- Hidden
- Protected
- NEVER modified by Python
- Updated only via query refresh


------------------------------------------------------------


============================================================
8. SYSTEM PRINCIPLES
============================================================

1. Structure controlled by owner
2. Users edit only allowed cells
3. Master data centralized in _Master_Ref
4. All relationships enforced via dropdown + lookup
5. Errors visible, not hidden
6. Excel acts as controlled UI, not free-form data


============================================================
END OF SPEC
============================================================