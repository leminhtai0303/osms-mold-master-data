"""Legacy-to-v3 mold master data mapping helpers.

Single source of truth for the Bottoming Mold Master Data Standard
(docs/reference/, v3.0 Definition + v3.1 Standard). Imported by
data_processing.ipynb, dq_issues_by_family.ipynb, and json_export.ipynb.

Mold ID format: {MoldFamily}-{Type}-{Position}(-B)
  Type     ∈ {OS, MS, OT}
  Position ∈ {PRI, BOT, HEEL}
  -B       = Blocker stage suffix

Family-code suffix rules from the standard (documented here, NOT applied
as splitting logic because no Saucony family in the current dataset
carries them — DQ check I19 flags candidates for future brands):
  -1/-2/-3 trailing digits  -> Revision attribute on the asset record
  -A/-B/-C trailing letters -> Mold Set attribute on the asset record
  -E/-4E width, -M/-W gender -> separate Mold Family (kept as-is)
"""

import re

# ---------------------------------------------------------------------------
# Controlled vocabulary (v3.0 Definition §6, §7.2)
# ---------------------------------------------------------------------------

MOLD_TYPES = {"OS": "Outsole", "MS": "Midsole", "OT": "Other"}
SOLE_TYPE_TO_TYPE = {"Outsole": "OS", "Midsole": "MS", "Other": "OT"}

POSITION_BY_DIGIT = {"1": "PRI", "2": "BOT", "3": "HEEL"}
POSITION_NAMES = {"PRI": "Primary", "BOT": "Bottom Layer", "HEEL": "Heel"}

STAGES = ["Default", "Blocker"]
ASSET_STATUSES = ["Active", "Inactive", "In Repair", "Retired"]
MOLD_SETS = ["A", "B", "C", "D"]

CONSTRUCTION_TYPES = {
    frozenset({"PRI"}): "Single Piece",
    frozenset({"PRI", "BOT"}): "Vertical Split",
    frozenset({"PRI", "HEEL"}): "Main + Heel",
    frozenset({"PRI", "BOT", "HEEL"}): "3-Way",
}

# Legacy component codes observed in source data: OS1, OS2, MS1, MS1-1,
# MS2, MS2-1, MS3. The "-1" sub-suffix marks a Blocker (confirmed by
# "Blocker" in every matching display name).
LEGACY_COMPONENT_RE = re.compile(r"^(OS|MS|OT)(\d)(?:-(\d+))?$")

MOLD_ID_RE = re.compile(
    r"^(?P<family>.+)-(?P<type>OS|MS|OT)-(?P<position>PRI|BOT|HEEL)(?P<blocker>-B)?$"
)

# Standard family code: brand prefix + number, optional width/gender
# variant suffix kept inside the family (e.g. SA-2654E, SA-24024E).
STANDARD_FAMILY_RE = re.compile(r"^(SA|MRS|CHS|BA|HO|HY)-\d+[0-9A-Z]*$|^[TW]-?\d+[0-9A-Z]*$")

# Width variants are legitimate separate families (v3.0 §6.1). Current
# data carries them hyphenated (SA-2017-E, SA-2654-4E) — accepted as-is;
# used by is_legacy_family_code and DQ check I19 to avoid false positives.
WIDTH_VARIANT_RE = re.compile(r"^(SA|MRS|CHS|BA|HO|HY)-\d+-?(4E|E|M|W)$")


# ---------------------------------------------------------------------------
# Legacy -> v3 derivation
# ---------------------------------------------------------------------------

def normalize_family(mold_code):
    """Family codes are opaque identifiers; only whitespace is cleaned."""
    return str(mold_code).strip()


def is_legacy_family_code(family):
    """True for frozen non-standard codes (S1612, FLIP, M-461, ...)."""
    return not (STANDARD_FAMILY_RE.match(family) or WIDTH_VARIANT_RE.match(family))


def derive_component(legacy_code, display_name=None):
    """Map a legacy component code to (type, position, stage).

    Returns None when the code cannot be mapped (caller quarantines).
    """
    m = LEGACY_COMPONENT_RE.match(str(legacy_code).strip().upper())
    if not m:
        return None
    type_, digit, sub = m.groups()
    position = POSITION_BY_DIGIT.get(digit)
    if position is None:
        return None
    if sub is not None and sub != "1":
        return None  # unknown sub-suffix
    is_blocker = sub is not None or "BLOCKER" in str(display_name or "").upper()
    return type_, position, "Blocker" if is_blocker else "Default"


def build_mold_id(family, type_, position, stage="Default"):
    mold_id = f"{family}-{type_}-{position}"
    return mold_id + "-B" if stage == "Blocker" else mold_id


def short_mold_id(type_, position, stage="Default"):
    """Short form without family prefix — used for Excel sheet names."""
    short = f"{type_}-{position}"
    return short + "-B" if stage == "Blocker" else short


def parse_mold_id(mold_id):
    """Parse a governed Mold ID into its segments, or None if invalid."""
    m = MOLD_ID_RE.match(str(mold_id))
    if not m:
        return None
    return {
        "family": m.group("family"),
        "type": m.group("type"),
        "position": m.group("position"),
        "stage": "Blocker" if m.group("blocker") else "Default",
    }


def component_description(type_, position, stage="Default"):
    """Human-readable supplementary description, e.g. 'Midsole Bottom Layer Blocker'."""
    base = f"{MOLD_TYPES[type_]} {POSITION_NAMES[position]}"
    return base + " Blocker" if stage == "Blocker" else base


def derive_construction_type(positions):
    """Construction type from the set of non-blocker positions of one
    (family, type). Returns None when PRI is missing (governance gap)."""
    return CONSTRUCTION_TYPES.get(frozenset(positions))
