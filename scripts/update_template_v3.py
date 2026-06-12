"""One-time migration of MoldFamily_(Template).xlsx to the v3 standard.

Per docs/reference/ (Bottoming Mold Master Data Standard v3.1):
- _dimMoldHierarchies rows become short Mold IDs ({Type}-{Position}(-B));
  position and stage are encoded in the ID itself, so the table keeps its
  three columns (adding Position/Stage columns would collide with
  _dimMoldCondition at E1).
- Summary labels: "Mold Code:" -> "Mold Family:", "Component Code" -> "Mold ID".
- {Component} sheet labels: rows 2-5 become Mold Family / Mold ID /
  Component Description / Design Compound.

Uses Excel COM (not openpyxl) to preserve array formulas, data
validations, protection, and table metadata.

Run:  uv run python scripts/update_template_v3.py
"""

import sys
from pathlib import Path

import win32com.client as win32

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TEMPLATE = Path(__file__).resolve().parents[1] / "docs" / "templates" / "MoldFamily_(Template).xlsx"

HIERARCHY_ROWS = [
    # Component Code (short Mold ID), Component Name, Sole Type
    ("OS-PRI",   "Outsole Primary",              "Outsole"),
    ("OS-BOT",   "Outsole Bottom Layer",         "Outsole"),
    ("MS-PRI",   "Midsole Primary",              "Midsole"),
    ("MS-PRI-B", "Midsole Primary Blocker",      "Midsole"),
    ("MS-BOT",   "Midsole Bottom Layer",         "Midsole"),
    ("MS-BOT-B", "Midsole Bottom Layer Blocker", "Midsole"),
    ("MS-HEEL",  "Midsole Heel",                 "Midsole"),
    ("OT-PRI",   "Other Component",              "Other"),
]


def main():
    if not TEMPLATE.exists():
        raise SystemExit(f"Template not found: {TEMPLATE}")

    app = win32.DispatchEx("Excel.Application")
    app.Visible = False
    app.DisplayAlerts = False
    try:
        wb = app.Workbooks.Open(str(TEMPLATE))
        try:
            # ── _Master_Ref: _dimMoldHierarchies → 8 short Mold IDs ──────────
            ws_ref = wb.Worksheets("_Master_Ref")
            lo = ws_ref.ListObjects("_dimMoldHierarchies")
            n = len(HIERARCHY_ROWS)
            old_ref = lo.Range.Address
            lo.Resize(ws_ref.Range(f"A1:C{n + 1}"))
            ws_ref.Range(f"A2:C{n + 1}").Value = HIERARCHY_ROWS
            print(f"_dimMoldHierarchies: {old_ref} -> {lo.Range.Address} ({n} rows)")

            # ── Summary labels ───────────────────────────────────────────────
            ws_sum = wb.Worksheets("Summary")
            ws_sum.Range("A1").Value = "Mold Family: "
            ws_sum.Range("A6").Value = "Mold ID"
            print(f"Summary: A1='{ws_sum.Range('A1').Value}', A6='{ws_sum.Range('A6').Value}'")

            # ── {Component} sheet labels ─────────────────────────────────────
            ws_comp = wb.Worksheets("{Component}")
            ws_comp.Range("A2").Value = "Mold Family: "
            ws_comp.Range("A3").Value = "Mold ID:"
            ws_comp.Range("A4").Value = "Component Description:"
            ws_comp.Range("A5").Value = "Design Compound:"
            labels = [ws_comp.Range(f"A{r}").Value for r in range(2, 6)]
            print(f"{{Component}} labels A2:A5 = {labels}")

            # ── Verification dump ────────────────────────────────────────────
            codes = [r[0] for r in ws_ref.Range(f"A2:C{n + 1}").Value]
            print(f"Component codes: {codes}")
            mcl = wb.Names("MoldComponentList").RefersTo
            print(f"MoldComponentList -> {mcl}")

            wb.Save()
            print(f"Saved: {TEMPLATE}")
        finally:
            wb.Close(SaveChanges=False)
    finally:
        app.Quit()


if __name__ == "__main__":
    main()
