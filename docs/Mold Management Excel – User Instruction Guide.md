# Mold Management Excel – User Instruction Guide (v1)

============================================================
1. PURPOSE
============================================================

This file is the Source of Truth for Mold Management per Family.

You will mainly:
- Review mold information
- Update operational data (output, cost, condition, comments)

You WILL NOT:
- Modify structure
- Add rows
- Edit grey cells


============================================================
2. SHEET: Summary (Primary Working Sheet)
============================================================


------------------------------------------------------------
2.1 Basic Information (Top of Sheet)
------------------------------------------------------------

A2 = Mold Family → already defined  
B2 = Brand → already defined  

No action required.


------------------------------------------------------------
2.2 How to Read the Table
------------------------------------------------------------

Each row represents:

    ONE Component at ONE Vendor


There are 2 zones in the table:

LEFT SIDE (Grey):
- System-controlled (DO NOT EDIT)

RIGHT SIDE (White):
- User input area (YOU EDIT HERE)


------------------------------------------------------------
2.3 What You CAN Edit (White Cells Only)
------------------------------------------------------------

Column H – Mold Shop  
    → Enter mold shop name (free text)

Column I – Init Season  
    → Enter season if known (free text)

Column J – Daily Output  
    → Enter number ≥ 0  
    → Leave blank if unknown

Column K – Mold Cost  
    → Enter number ≥ 0  
    → Leave blank if unknown

Column L – Mold Ownership  
    → Select from dropdown

Column M – Mold Condition  
    → Select from dropdown

Column N – Comment  
    → Optional notes


IMPORTANT RULES:
- Only type in WHITE cells
- Do NOT paste random text into numeric columns
- Leave blank if unsure


------------------------------------------------------------
2.4 What You MUST NOT Change
------------------------------------------------------------

DO NOT touch:
- Grey cells (Columns A–G)
- Column headers
- Sheet structure

DO NOT:
- Insert rows
- Delete rows
- Insert columns
- Merge cells

If new vendor/component is needed:
→ Contact system owner


------------------------------------------------------------
2.5 System Generated Columns (For Reference)
------------------------------------------------------------

Column F – Total Mold Qty
    → Automatically calculated from MoldInv sheet
    → DO NOT EDIT

Column G – Status Check
    → Indicates data issue


Status meaning:

OK        → Data is valid  
ERR_DUP   → Duplicate Component + Vendor  
ERR_BADNUM → Invalid number input  


------------------------------------------------------------
2.6 Error Handling (IMPORTANT)
------------------------------------------------------------

If a row turns RED:
    → There is an issue

Steps to fix:

1. Check Status column (Column G)
2. Fix the issue:

   If ERR_DUP:
       → Duplicate entry exists → inform owner

   If ERR_BADNUM:
       → Fix Daily Output or Mold Cost
       → Must be number ≥ 0 or blank


------------------------------------------------------------
2.7 Data Entry Tips
------------------------------------------------------------

- If you don’t know a value → leave blank
- Do NOT guess numbers
- Use dropdowns whenever available
- Keep comments short and clear


------------------------------------------------------------
2.8 Where to Edit Inventory Data
------------------------------------------------------------

⚠ Inventory quantities are NOT edited in this sheet

To update mold quantity:

    Go to:
    Sheet → MoldInv_{ComponentCode}

This Summary sheet will automatically update.


============================================================
(Next sections will explain other sheets)
============================================================