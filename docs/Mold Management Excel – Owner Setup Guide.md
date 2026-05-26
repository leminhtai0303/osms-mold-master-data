# Mold Management Excel — Owner Setup Guide (v4 TEMPLATE-LOCK MODEL)

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

For EACH sheet:

------------------------------------------------------------
2.1 Summary
------------------------------------------------------------

Pre-configure:

- Lookup formulas (B, C)
- Total Mold Qty formula (F)
- Status formula (G)
- Hidden validation columns (O, P)

- Data validation:
    Component Code → MoldComponentList
    Vendor → VendorList
    Ownership → MoldOwnership
    Condition → MoldCondition

- Conditional formatting:
    Row red if Status != OK

- Protection:
    Lock A:G, O:P
    Unlock H:N

------------------------------------------------------------
2.2 MoldInv_{Component} TEMPLATE
------------------------------------------------------------

Pre-configure:

- Fixed MoldSize rows (1–18)

- Vendor columns (C:F):
    dropdown → VendorList + NOT_USED/N/A

- Qty cells:
    validation ≥0

- TotalQty formula column

- Freeze pane at C8

- Protection:
    lock header + structure
    unlock qty cells

------------------------------------------------------------
2.3 Sourcing Rule
------------------------------------------------------------

Pre-configure:

- Max 20 rows
- Dropdown:
    Factory → FactoryList
    Component → MoldComponentList
    Vendor → VendorList

- Protection:
    lock structure
    unlock input cells

------------------------------------------------------------
2.4 _Master_Ref
------------------------------------------------------------

- Power Query connected
- Tables created
- Named ranges defined

DO NOT allow editing

------------------------------------------------------------

============================================================
3. PYTHON EXECUTION MODEL
============================================================

For each generated file:

------------------------------------------------------------
3.1 Open file
------------------------------------------------------------

Load workbook

------------------------------------------------------------
3.2 UNLOCK sheets
------------------------------------------------------------

Disable protection:

Summary  
MoldInv_*  
Sourcing Rule  

------------------------------------------------------------
3.3 DATA INGESTION
------------------------------------------------------------

Summary:

- Write ONLY:
    A Component Code
    D Vendor
    E Location
    H Mold Shop (if needed)
    K Init Season (if needed)

MoldInv:

- Set vendor headers (C7:F7)
- Fill quantities

Sourcing Rule:

- Fill up to 20 rows

------------------------------------------------------------
3.4 IMPORTANT RULES
------------------------------------------------------------

Python MUST NOT:

✘ Modify formulas  
✘ Modify validation  
✘ Modify formatting  
✘ Insert/delete rows  

------------------------------------------------------------
3.5 NORMALIZATION
------------------------------------------------------------

Before writing:

value = str(value).strip()

------------------------------------------------------------
3.6 RE-LOCK SHEETS
------------------------------------------------------------

After writing:

- Re-enable protection
- Keep same lock rules

------------------------------------------------------------
3.7 SAVE FILE
------------------------------------------------------------


============================================================
4. CRITICAL SYSTEM DEPENDENCY
============================================================

Summary Vendor = MoldInv header EXACT MATCH

Used in:

MATCH(vendor, headerRow)

Mismatch:
→ TotalQty error
→ Highlighted automatically

============================================================
5. QA CHECK
============================================================

Owner must verify:

✅ No red rows in Summary  
✅ TotalQty populated  
✅ Dropdown works  
✅ Sheets protected  

============================================================
END OF GUIDE
============================================================