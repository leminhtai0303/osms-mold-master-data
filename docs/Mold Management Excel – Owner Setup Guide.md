# Mold Management Excel — Owner Setup Guide (v6)

Aligned with the Bottoming Mold Master Data Standard v3.0/v3.1
(see `docs/reference/`). Terminology: Mold ID = governed component
identifier {MoldFamily}-{Type}-{Position}(-B); component sheets and
Summary col A use the SHORT form (e.g. MS-PRI-B).

============================================================
1. CORE PRINCIPLE
============================================================

Template is FULLY configured before use:

✔ Formulas
✔ Data validation
✔ Conditional formatting
✔ Sheet protection

Python only performs:

✔ Temporary unlock
✔ Data injection
✔ Re-lock

============================================================
2. TEMPLATE REQUIREMENTS (OWNER MUST SET ONCE)
============================================================

------------------------------------------------------------
2.1 Summary Sheet
------------------------------------------------------------

Pre-configure:

HEADER
- A1: "Mold Family:"   A2: "Brands:"  (B values written by Python)

MOLD SUMMARY TABLE (A:P)

- Lookup formulas:
    B  (Sole Type)    → XLOOKUP(A, _dimMoldHierarchies[Component Code], [Sole Type])
    C  (Comp Name)    → XLOOKUP(A, _dimMoldHierarchies[Component Code], [Component Name])
    E  (Location)     → XLOOKUP(D, _dimVendor[Vendor Short Name], [Location])

- Total Mold Qty formula (col F):
    =IF(G7="OK",
      LET(comp,A7, ven,D7, sh,comp, hdrRow,8,
        col,MATCH(ven,INDIRECT("'"&sh&"'!"&hdrRow&":"&hdrRow),0),
        SUM(INDEX(INDIRECT("'"&sh&"'!A:ZZ"),0,col))),
    "")

    ⚠ sh = comp (column A value only).
      Component sheet name must match the short Mold ID in col A exactly.

- Check formula (col G):
    =IF(OR(A7<>"",D7<>""),
      IFS(O7,"Missing Keys", P7,"Duplicate Keys", TRUE,"OK"),
    "")

    NOTE: column header is "Check" — a data-entry validation flag.
    Do not name it "Status": the standard reserves Status for the
    asset lifecycle (Active / Inactive / In Repair / Retired).

- Hidden flag columns O, P:
    O → =OR(ISBLANK(A7), ISBLANK(D7))
    P → =COUNTIFS($A$7:$A$31,$A7,$D$7:$D$31,$D7)>1

- Data validation:
    A7:A31  → MoldComponentList   (the 8 short Mold IDs — see 2.3)
    D7:D31  → VendorList
    H7:H31  → MoldOwnership
    I7:I31  → MoldCondition
    K7:K31  → Season format (custom: S/F + 2-digit year)
    L7:L31  → ≥ 0 numeric
    M7:M31  → ≥ 0 numeric

- Conditional formatting:
    Row turns RED if col G ≠ "OK"

- Protection:
    Lock A:G, O:P
    Unlock H:N

STYLES SECTION (R:T)

- Row 4: section title "Styles Using This Family"
- Row 5: banner "Input Style Name"
- Row 6: column headers  R6=Style Name  S6=Outsole  T6=Midsole
- Rows 7–31: input range (25 rows)
    S7:T31 → default value 0 (unchecked)

- Protection: unlock R7:T31, lock headers


------------------------------------------------------------
2.2 {Component} Sheet Template
------------------------------------------------------------

This is the master template sheet that Python copies once per component.
It is named "{Component}" in the template file — Python renames each
copy to the component's SHORT Mold ID (e.g. "OS-PRI", "MS-BOT-B") and
deletes the "{Component}" prototype from the output file.

Pre-configure:

HEADER (rows 1–5)
- A1: "Mold Inventory"  (static label)
- A2: "Mold Family:"  A3: "Mold ID:"  A4: "Component Description:"
  A5: "Design Compound:"
  (B column values written by Python; B3 = FULL Mold ID,
   e.g. SA-2301-MS-PRI-B)

INSTRUCTION ROW (row 7)
- A7: inventory editing instruction (static text, locked)
- H7: sourcing editing instruction (static text, locked)

COLUMN HEADER ROW (row 8)
INVENTORY:
- A8: "Sizes"  (static, locked)
- B8:E8: vendor header dropdowns → validation = VendorList  (Python writes values)

SOURCING:
- H8: "Factory Name"
- I8: "Factory Location"
- J8: "Factory Code"
- K8: "Vendor Short Name"
- L8: "Vendor Location"
- M8: "Vendor Code"
  All static text, locked.

DATA ROWS (rows 9–43)

INVENTORY SIDE A9:E43:
- A9:A43: size-coverage patterns, comma-separated shoe sizes
  (e.g. "3.5, 4") — one row per distinct pattern  (unlock; Python writes)
- B9:E43: qty cells, validation ≥ 0  (unlock)

SOURCING SIDE H9:M43:
- H9:H43: Factory Name  → validation = FactoryList  (unlock)
- I9:I43: XLOOKUP(H9, _dimFactory[Factory Name], _dimFactory[Factory Country], "")  (locked)
- J9:J43: XLOOKUP(H9, _dimFactory[Factory Name], _dimFactory[Factory Number], "")   (locked)
- K9:K43: Vendor Short Name  → validation = VendorList  (unlock)
- L9:L43: XLOOKUP(K9, _dimVendor[Vendor Short Name], _dimVendor[Location], "")      (locked)
- M9:M43: XLOOKUP(K9, _dimVendor[Vendor Short Name], _dimVendor[Vendor ID], "")     (locked)

Conditional formatting:
- B9:E43: highlight red if invalid number or negative
- Optional: highlight if qty > 0 but Sizes (col A) is blank


------------------------------------------------------------
2.3 _Master_Ref Sheet
------------------------------------------------------------

- Power Query connected to master_references.xlsx
- Tables: _dimMoldHierarchies, _dimVendor, _dimMoldOwnership,
          _dimMoldCondition, _dimFactory
- _dimVendor MUST have a "Vendor ID" column (FTY number)
  — required by the M column XLOOKUP on component sheets
- Named ranges defined (see spec section 2)
- Hidden and protected
- DO NOT allow editing

_dimMoldHierarchies MUST contain exactly the 8 standard rows
(Component Code = short Mold ID; set once by scripts/update_template_v3.py):

  OS-PRI     Outsole Primary                Outsole
  OS-BOT     Outsole Bottom Layer           Outsole
  MS-PRI     Midsole Primary                Midsole
  MS-PRI-B   Midsole Primary Blocker        Midsole
  MS-BOT     Midsole Bottom Layer           Midsole
  MS-BOT-B   Midsole Bottom Layer Blocker   Midsole
  MS-HEEL    Midsole Heel                   Midsole
  OT-PRI     Other Component                Other

⚠ If this table is fed by Power Query from master_references.xlsx,
  update the upstream file with the same 8 rows — otherwise a refresh
  restores the legacy codes (OS1, MS1, ...) and breaks the Summary
  lookups and dropdown.


============================================================
3. PYTHON EXECUTION MODEL
============================================================

------------------------------------------------------------
3.1 Open template
------------------------------------------------------------

Load template workbook.
Build lookup maps from _Master_Ref:
  - vendor_short_by_id:       Vendor ID → Vendor Short Name
  - factory_name_by_number:   Factory Number → Factory Name
Close template.

------------------------------------------------------------
3.2 Per-family loop
------------------------------------------------------------

Open a fresh copy of the template for each family.

------------------------------------------------------------
3.3 UNLOCK sheets
------------------------------------------------------------

Disable protection on:
  Summary
  {Component} (template sheet, before copying)
  Each copied component sheet

------------------------------------------------------------
3.4 DATA INJECTION — Summary sheet
------------------------------------------------------------

Write:
  B1   Family code
  B2   Brand name(s)
  A7:A31  Short Mold IDs          [col A, must equal component sheet names]
  D7:D31  Vendor short names      [col D]
  H7:N31  Operational data        (Mold Ownership, Condition, Shop,
                                   Init Season, Daily Output, Mold Cost, Comments)

Styles section:
  R7:R{7+n-1}   Style names
  S7:S{7+n-1}   Outsole flags   (1 or None)
  T7:T{7+n-1}   Midsole flags   (1 or None)

Do NOT touch:
  Formulas (B, C, E, F, G), validation, formatting, structure
  Hidden columns O, P

------------------------------------------------------------
3.5 DATA INJECTION — {MoldID} sheets
------------------------------------------------------------

For each component (Mold ID) in the family:
  1. Copy the {Component} template sheet
  2. Rename copy to the SHORT Mold ID (e.g. "MS-PRI-B")
  3. Unlock copied sheet
  4. Write header values: B2 (family), B3 (full Mold ID),
     B4 (component description), B5 (design compound)
  5. Write size patterns A9:A43 from assets[*].sizeCoverage
  6. Write vendor headers B8:E8 (up to 4 vendor short names)
  7. Write inventory quantities into the matching vendor column × pattern row
  8. Write sourcing rules:
       H9:H{9+m-1}  factory names  (resolve from factoryNumber lookup)
       K9:K{9+m-1}  vendor short names  (resolve from vendorId reference)
     I, J, L, M columns auto-fill via XLOOKUP — Python does not touch them

Do NOT touch:
  Instruction rows, header row 8 (sourcing side),
  I/J/L/M XLOOKUP formula columns

------------------------------------------------------------
3.6 Delete template sheet
------------------------------------------------------------

After all component copies are created, delete "{Component}".

------------------------------------------------------------
3.7 RE-LOCK and SAVE
------------------------------------------------------------

Re-enable protection on all sheets.
Save as .xlsx.


============================================================
4. CRITICAL SYSTEM DEPENDENCIES
============================================================

1. Summary TotalQty uses MATCH(vendorShortName, componentSheet!row8)
   → Vendor short name in Summary col D MUST exactly match
     the vendor header written by Python to B8:E8 on the component sheet.

2. Summary F formula uses the short Mold ID (col A) as the sheet name
   directly. → Sheet name MUST equal the col A value. No prefix.

3. _dimVendor MUST contain a "Vendor ID" column.
   → Component sheet col M XLOOKUP depends on it.

4. _dimMoldHierarchies MUST contain the 8 standard short Mold IDs.
   → Summary col A dropdown and B/C lookups depend on it.


============================================================
5. QA CHECKLIST
============================================================

Owner must verify after each export:

✅ No red rows in Summary
✅ TotalQty populated for all rows with a vendor
✅ All dropdowns functional (col A lists OS-PRI … OT-PRI)
✅ Sourcing rules visible on each component sheet
✅ Styles section populated on Summary
✅ Component sheets named by short Mold ID; B3 shows the full Mold ID
✅ All sheets protected
✅ {Component} template sheet deleted from output files

============================================================
END OF GUIDE
============================================================
