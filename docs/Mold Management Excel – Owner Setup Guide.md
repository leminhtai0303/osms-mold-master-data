# Mold Management Excel — Owner Setup Guide (v5)

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

    ⚠ sh = comp (column A value only — no "MoldInv_" prefix).
      Sheet name must match the Component Code exactly.

- Status Check formula (col G):
    =IF(OR(A7<>"",D7<>""),
      IFS(O7,"Missing Keys", P7,"Duplicate Keys", TRUE,"OK"),
    "")

- Hidden flag columns O, P:
    O → OR(ISBLANK(A7), ISBLANK(D7))
    P → COUNTIFS($B$7:$B$31,$B7,$D$7:$D$31,$D7)>1

- Data validation:
    A7:A31  → MoldComponentList
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
2.2 {ComponentCode} Sheet Template
------------------------------------------------------------

This is the master template sheet that Python copies once per component.
Named "MoldInv_{Component}" in the template file before copying — Python
renames each copy to the component code (e.g. "OS1", "MS1").

Pre-configure:

HEADER (rows 1–5)
- A1: "Mold Inventory"  (static label)
- A2: "Mold Code:"  A3: "SoleType:"  A4: "Component Name:"  A5: "Compound:"
  (B column values written by Python)

INSTRUCTION ROW (row 7)
- A7: inventory editing instruction (static text, locked)
- H7: sourcing editing instruction (static text, locked)

COLUMN HEADER ROW (row 8)
INVENTORY:
- A8: "MoldSize"  B8: "ShoeSizes"  (static, locked)
- C8:F8: vendor header dropdowns → validation = VendorList  (Python writes values)
- G8: "TotalQty"  (static, locked)

SOURCING:
- H8: "Factory Name"
- I8: "Factory Location"
- J8: "Factory Code"
- K8: "Vendor Short Name"
- L8: "Vendor Location"
- M8: "Vendor Code"
  All static text, locked.

DATA ROWS (rows 9–43, mold sizes 1.0 → 18.0)

INVENTORY SIDE A9:G43:
- A9:A43: fixed mold size list 1, 1.5, 2, … 18  (locked)
- B9:B43: ShoeSizes free text  (unlock)
- C9:F43: qty cells, validation ≥ 0  (unlock)
- G9:G43: TotalQty formula =SUM(C9:F9)  (locked)

SOURCING SIDE H9:M43:
- H9:H43: Factory Name  → validation = FactoryList  (unlock)
- I9:I43: XLOOKUP(H9, _dimFactory[Factory Name], _dimFactory[Factory Country], "")  (locked)
- J9:J43: XLOOKUP(H9, _dimFactory[Factory Name], _dimFactory[Factory Number], "")   (locked)
- K9:K43: Vendor Short Name  → validation = VendorList  (unlock)
- L9:L43: XLOOKUP(K9, _dimVendor[Vendor Short Name], _dimVendor[Location], "")      (locked)
- M9:M43: XLOOKUP(K9, _dimVendor[Vendor Short Name], _dimVendor[Vendor ID], "")     (locked)

Conditional formatting:
- C9:F43: highlight red if invalid number or negative
- Optional: highlight if qty > 0 but ShoeSizes (col B) is blank


------------------------------------------------------------
2.3 _Master_Ref Sheet
------------------------------------------------------------

- Power Query connected to master_references.xlsx
- Tables: _dimMoldHierarchies, _dimVendor, _dimMoldShop,
          _dimMoldOwnership, _dimMoldCondition, _dimFactory
- _dimVendor MUST have a "Vendor ID" column (FTY number)
  — required by the M column XLOOKUP on component sheets
- Named ranges defined (see spec section 2)
- Hidden and protected
- DO NOT allow editing


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
  MoldInv_{Component} (template sheet, before copying)
  Each copied component sheet

------------------------------------------------------------
3.4 DATA INJECTION — Summary sheet
------------------------------------------------------------

Write:
  B1   Family code
  B2   Brand name(s)
  A7:A31  Component codes       [col A, unlocked area]
  D7:D31  Vendor short names    [col D, unlocked area]
  H7:N31  Operational data      (Mold Ownership, Condition, Shop,
                                  Init Season, Daily Output, Mold Cost, Comments)

Styles section:
  R7:R{7+n-1}   Style names
  S7:S{7+n-1}   Outsole flags   (1 or None)
  T7:T{7+n-1}   Midsole flags   (1 or None)

Do NOT touch:
  Formulas (B, C, E, F, G), validation, formatting, structure
  Hidden columns O, P

------------------------------------------------------------
3.5 DATA INJECTION — {ComponentCode} sheets
------------------------------------------------------------

For each component in the family:
  1. Copy MoldInv_{Component} template sheet
  2. Rename copy to the component code (e.g. "OS1")
  3. Unlock copied sheet
  4. Write header values: B2 (family), B3 (sole type), B4 (name), B5 (compound)
  5. Write shoe sizes B9:B43 from sizingRules.moldSizeToShoeSizes
  6. Write vendor headers C8:F8 (up to 4 vendor short names)
  7. Write inventory quantities into the matching vendor column × mold size row
  8. Write sourcing rules:
       H9:H{9+m-1}  factory names  (resolve from vendorId → factory lookup)
       K9:K{9+m-1}  vendor short names  (resolve from vendorId reference)
     I, J, L, M columns auto-fill via XLOOKUP — Python does not touch them

Do NOT touch:
  Mold size column A, instruction rows, header row 8 (sourcing side),
  G TotalQty formulas, I/J/L/M XLOOKUP formula columns

------------------------------------------------------------
3.6 Delete template sheet
------------------------------------------------------------

After all component copies are created, delete "MoldInv_{Component}".

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
     the vendor header written by Python to C8:F8 on the component sheet.

2. Summary F formula uses component code (col A) as the sheet name directly.
   → Sheet name MUST equal the Component Code. No prefix.

3. _dimVendor MUST contain a "Vendor ID" column.
   → Component sheet col M XLOOKUP depends on it.


============================================================
5. QA CHECKLIST
============================================================

Owner must verify after each export:

✅ No red rows in Summary
✅ TotalQty populated for all rows
✅ All dropdowns functional
✅ Sourcing rules visible on each component sheet
✅ Styles section populated on Summary
✅ All sheets protected
✅ MoldInv_{Component} template sheet deleted from output files

============================================================
END OF GUIDE
============================================================
