# Mold Management Excel — User Instruction Guide (v3)

============================================================
1. PURPOSE
============================================================

This file is the Source of Truth for mold management per family.

You will mainly:
- Review mold information on the Summary sheet
- Update operational data (output, cost, condition, comments) on Summary
- Update inventory quantities on each component sheet
- Update sourcing rules on each component sheet
- Update styles using this family on the Summary sheet

You WILL NOT:
- Modify structure, headers, or formulas
- Add or delete rows or columns
- Edit grey / locked cells


============================================================
2. UNDERSTANDING MOLD IDs
============================================================

Every component is identified by a governed Mold ID:

    {MoldFamily}-{Type}-{Position}(-B)

Example: SA-2301-MS-PRI-B reads as

    SA-2301  → Mold Family (the sole design; shown in the file name and B1)
    MS       → Type:      OS = Outsole, MS = Midsole, OT = Other
    PRI      → Position:  PRI = Primary, BOT = Bottom layer, HEEL = Heel insert
    -B       → Blocker (oversized preform stage); absent = normal mold

Inside the workbook the family prefix is dropped — sheet names and the
Summary "Mold ID" column show the SHORT form (MS-PRI-B). The full Mold ID
is shown on each component sheet (cell B3).

A Mold ID identifies WHAT a mold produces, not a specific piece of
metal. The same Mold ID can exist at several vendors and sizes — each
Summary row is one Mold ID at one vendor.

Full definitions: see docs/reference/ (Bottoming Mold Master Data
Definition & Standard).


============================================================
3. SHEET: Summary
============================================================

The Summary sheet has two side-by-side sections.


------------------------------------------------------------
3.1 Header (Rows 1–2)
------------------------------------------------------------

A1 / B1 = Mold Family code  → system-filled, do not edit
A2 / B2 = Brand name        → system-filled, do not edit


------------------------------------------------------------
3.2 LEFT SECTION — Mold Summary Table (Cols A–N)
------------------------------------------------------------

Each row = ONE component (Mold ID) at ONE vendor

Two zones:

LEFT (grey, cols A–G):     System-controlled — DO NOT EDIT
RIGHT (white, cols H–N):   Your input area — EDIT HERE


What you CAN edit (white cells only):

  H  Mold Ownership    → select from dropdown
  I  Mold Condition    → select from dropdown
  J  Mold Shop         → free text
  K  Init Season       → format: S26 or F26 (season letter + 2-digit year)
  L  Daily Output      → number ≥ 0, leave blank if unknown
  M  Mold Init Cost    → number ≥ 0, leave blank if unknown
  N  Comments          → free text notes

What you MUST NOT change:

  A  Mold ID           — system key (short form, e.g. MS-PRI)
  B  Sole Type         — auto-lookup
  C  Component Name    — auto-lookup
  D  Vendor Name       — system-filled, contact owner to change
  E  Location          — auto-lookup
  F  Total Mold Qty    — calculated from component sheet
  G  Check             — error indicator


Check column meanings:

  OK             → Row is valid
  Missing Keys   → Mold ID or Vendor is blank — contact owner
  Duplicate Keys → Same Mold ID + Vendor appears more than once — contact owner

If a row turns RED → check the Check column and follow the steps above.

(The Check column validates data entry. It is not the mold's lifecycle
status — condition is tracked in column I.)


------------------------------------------------------------
3.3 RIGHT SECTION — Styles Using This Family (Cols R–T)
------------------------------------------------------------

Lists which styles use this mold family and which components they use.

  R  Style Name    → type the style name
  S  Outsole       → enter 1 if this style uses the Outsole from this family, else 0 or blank
  T  Midsole       → enter 1 if this style uses the Midsole from this family, else 0 or blank

A style may use Outsole only, Midsole only, or both — enter accordingly.

Max 25 styles (rows 7–31). Contact owner if more rows are needed.

IMPORTANT:
- Do NOT type in the header rows (rows 4–6)
- Do NOT change column structure


------------------------------------------------------------
3.4 Where to Edit Inventory Quantities
------------------------------------------------------------

⚠ Inventory quantities are NOT edited on this sheet.

To update mold quantities:
  → Go to the component sheet (e.g. OS-PRI, MS-PRI)

The Total Mold Qty column (F) updates automatically.


============================================================
4. SHEET: {MoldID}  (e.g. OS-PRI, MS-PRI, MS-BOT-B)
============================================================

One sheet exists per component. The sheet name is the short Mold ID;
the full Mold ID is shown in cell B3. Each sheet has two sections:
LEFT (cols A–E) = Inventory   RIGHT (cols H–M) = Sourcing Rules


------------------------------------------------------------
4.1 LEFT SECTION — Inventory Grid (Cols A–E)
------------------------------------------------------------

Column A  Sizes      Comma-separated shoe sizes covered by one mold size
                     Example: 3.5, 4  (one physical mold covers both)
                     One row per distinct size pattern
Column B–E  Qty      Quantity of molds for each vendor with that pattern
                     Number ≥ 0, blank = none

The vendor names appear in the header row (row 8, cols B–E).
These are system-filled — contact owner to add or change vendors.

What you CAN edit:
  A   Sizes (comma-separated, free text)
  B–E Inventory quantities (numbers only, no text)

What you MUST NOT change:
  Row 8 vendor headers, rows 1–7 header area


------------------------------------------------------------
4.2 RIGHT SECTION — Sourcing Rules (Cols H–M)
------------------------------------------------------------

Records which factory sources this component from which vendor.
Each row = one factory → vendor allocation.

  H  Factory Name      → select from dropdown (FactoryList)
  I  Factory Location  → auto-filled, do not edit
  J  Factory Code      → auto-filled, do not edit
  K  Vendor Short Name → select from dropdown (VendorList)
  L  Vendor Location   → auto-filled, do not edit
  M  Vendor Code       → auto-filled (Vendor ID / FTY number), do not edit

What you CAN edit:
  H   Factory Name (dropdown)
  K   Vendor Short Name (dropdown)

What you MUST NOT change:
  Column headers (row 8), formula columns I, J, L, M

Rules:
  - One factory can only source this component from one vendor
  - If a factory does not appear, it does not use this component
  - Fill rows from top (row 9) downward, leave unused rows blank
  - Max 35 rows available

Sourcing rows are independent of the inventory rows on the left —
row 9 sourcing has nothing to do with row 9 sizes.


------------------------------------------------------------
4.3 General Rules for Component Sheets
------------------------------------------------------------

- Do NOT insert, delete, or reorder rows or columns
- Do NOT merge cells
- Do NOT paste from other sheets into locked areas
- Leave cells blank if data is unknown — do NOT enter 0 unless the quantity is truly 0
- If a new vendor or factory is needed → contact system owner
- Blocker sheets (names ending in -B, e.g. MS-PRI-B) are the oversized
  preform molds; they always pair with a normal sheet of the same name
  without -B. Track their quantities separately on their own sheet.


============================================================
5. GENERAL TIPS
============================================================

- Use dropdowns wherever available — do not type values that should come from a list
- If a cell turns red → there is a data issue; check the Check column or contact owner
- Leave blank rather than guess
- Keep comments short and specific

============================================================
END OF GUIDE
============================================================
