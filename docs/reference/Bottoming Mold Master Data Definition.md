# Bottoming Mold Master Data — Definition & Naming Standard

Version: 3.0 Approved
Date: 2026-06-12
Author: Tai Le
Audience: Bottoming Team, Raw Material Management

---

## 1. Purpose

Standardized hierarchy, naming convention, and controlled vocabulary for
all sole-related mold master data. Goal: eliminate freeform naming, enable
consistent tracking, establish single source of truth for mold assets.

---

## 2. Scope

Covers all molds used in sole unit production:
- Outsole molds
- Midsole molds
- Other molds (footbed, insole, shank, plates, small parts)

Does not cover: upper tooling (KPU, injection PU), lasting equipment,
cutting dies, or non-mold production assets.

---

## 3. Core Concept: Two Layers

Mold data is split into two distinct layers:

| Layer | Purpose | Key |
|-------|---------|-----|
| **Mold ID** (master data) | Identifies what a mold **produces** — the product definition | `{Family}-{Type}-{Position}(-B)` |
| **Physical Asset** (asset data) | Identifies the actual metal sitting in a factory | Mold ID + Size + Vendor + Set + Revision |

Mold ID answers: "What component is this?"
Physical Asset answers: "Which specific mold, where, in what condition?"

---

## 4. Hierarchy

Every mold record sits within a 4-level hierarchy:

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| L1 | Mold Family | Sole design grouping | SA-2301 |
| L2 | Mold Type | Category of sole component | OS / MS / OT |
| L3 | Position | Role in assembly | PRI / BOT / HEEL |
| L4 | Stage | Production stage | -B suffix or none |

### Hierarchy Visual

Mold Family (SA-2301)
├── Outsole
│   ├── SA-2301-OS-PRI          (primary — always present)
│   └── SA-2301-OS-BOT          (bottom layer, e.g. IBR — rare)
├── Midsole
│   ├── SA-2301-MS-PRI          (primary — always present)
│   │   └── SA-2301-MS-PRI-B    (blocker)
│   ├── SA-2301-MS-BOT          (bottom density layer)
│   │   └── SA-2301-MS-BOT-B    (blocker)
│   └── SA-2301-MS-HEEL         (heel insert/plug)
└── Other
└── SA-2301-OT-PRI          (shank, plate, footbed, etc.)

---

## 5. Naming Convention

### Format

{MoldFamily}-{Type}-{Position}(-B)

All segments are dash-separated. The `-{Type}-` segment is the **parsing
boundary**: everything left = family identity, everything right = component.

| Segment | Values | Required |
|---------|--------|----------|
| MoldFamily | Brand prefix + family number | Yes |
| Type | OS / MS / OT | Yes |
| Position | PRI / BOT / HEEL | Yes |
| -B | Blocker suffix | Only if blocker |

### Examples

| Mold ID | Reads As |
|---------|----------|
| SA-2301-OS-PRI | SA-2301, Outsole, primary |
| SA-2301-MS-PRI | SA-2301, Midsole, primary |
| SA-2301-MS-PRI-B | SA-2301, Midsole, primary, Blocker |
| SA-2301-MS-BOT | SA-2301, Midsole, bottom layer |
| SA-2301-MS-BOT-B | SA-2301, Midsole, bottom layer, Blocker |
| SA-2301-MS-HEEL | SA-2301, Midsole, heel insert |
| SA-1920-OS-BOT | SA-1920, Outsole, bottom layer (IBR) |
| MRS-1756-OT-PRI | MRS-1756, Other component |

---

## 6. Definitions

### 6.1 Mold Family

A logical grouping of all molds required to produce the complete sole
unit for a shoe design.

The Mold Family code is an **opaque identifier** — a name, not a data
structure. The system does not parse meaning from it. All structured
information is captured in separate attributes.

#### Brand Prefix

| Brand | Prefix | Example |
|-------|--------|---------|
| Saucony | SA | SA-2301 |
| Merrell | MRS | MRS-1756 |
| Chaco | CHS | CHS-398 |
| CAT | T | T1557 |
| Bates | BA | BA-85 |
| Wolverine | W | W-519 |
| Harley-Davidson | HO | HO-281 |
| Hytest | HY | HY-33 |

#### Family Number

A sequential number assigned when the sole design is created. Managed by
each brand's development team.

Width variants are absorbed into the family number as a separate family:

| Standard | Width Variant | Why Separate |
|----------|--------------|--------------|
| SA-2654 | SA-2654E | Different last, not interchangeable |
| SA-2402 | SA-2402-4E → SA-24024E | Different cavity geometry |

**Rule:** All new Mold Family codes must use the standard brand prefix.

#### Legacy Suffixes Are NOT Separate Families

Legacy codes often contain operational suffixes (-1, -2, -A, -B, -C)
that do not represent different sole designs. These are tracked as
attributes (Revision, Mold Set), not as distinct families.

| Legacy Code | Style | Mold Family | Revision | Mold Set |
|-------------|-------|-------------|----------|----------|
| SA-2301 | Kinvara 14 | SA-2301 | 0 | A (implied) |
| SA-2301-2 | Kinvara 14 | SA-2301 | 2 | A |
| MRS-1873-1 | — | MRS-1873 | 1 | A |
| MRS-1873-1-C | — | MRS-1873 | 1 | C |
| SA-2552-2A | Triumph 23 | SA-2552 | 2 | A |
| SA-2552-2B | Triumph 23 | SA-2552 | 2 | B |

#### Legacy Code Exceptions

Some legacy codes do not follow standard format. Retained as-is, frozen
for backward compatibility.

| Pattern | Examples | Action |
|---------|----------|--------|
| Vendor catalog numbers | 210K, 261K, S1612 | Retain; do not replicate |
| Product names as codes | FLIP, FLOP, Wrapsody | Retain; do not replicate |
| Alternate prefixes | M-461, Q-171 | Retain; do not replicate |

### 6.2 Mold Type

Three fixed categories:

| Code | Name | Definition |
|------|------|------------|
| OS | Outsole | Ground-contact layer. Material: rubber, TPU, TPR, IBR. |
| MS | Midsole | Cushioning layer between outsole and upper. Material: EVA, PU, ETPU, Peba, SCF. |
| OT | Other | All remaining sole-unit parts: footbed, insole, shank, plate, airbag, carbon fiber, TPU shell. |

### 6.3 Position

Three semantic codes identifying a component's **role in assembly**.

| Code | Name | Definition |
|------|------|------------|
| PRI | Primary | The main or only piece. Always present. In single-piece = whole unit. In multi-piece = top layer, main body, or forepart. |
| BOT | Bottom | Secondary layer underneath the primary. Used in dual-density/dual-compound constructions. |
| HEEL | Heel | Heel insert, plug, or top lift. A discrete piece covering the heel zone only. |

**Design principle:** PRI = "the piece you'd keep if you could only keep
one." Always the larger, more complex, higher-cost component.

#### Construction Type (Derived)

Not encoded in the ID. Derived from which positions exist:

| Construction | Positions | Typical Use |
|---|---|---|
| Single piece | PRI only | ~95% of all OS and MS |
| Vertical split | PRI + BOT | Dual-density midsole; rubber-over-IBR outsole |
| Main + heel plug | PRI + HEEL | Main body + separate heel cushion |
| 3-way | PRI + BOT + HEEL | Top + bottom + heel |

#### Position Applicability (from 2,280-record analysis)

| Position | OS | MS | OT |
|---|:---:|:---:|:---:|
| PRI | ✅ 99% | ✅ Every MS | ✅ Always |
| BOT | Rare (~1%) | ~7% | — |
| HEEL | Not observed | ~1.4% | — |
| Blocker (-B) | Not observed | Rare (~0.6%) | Rare |

#### Rules

- PRI must always exist. BOT and HEEL cannot exist without PRI.
- OT type always uses PRI. Different OT components are distinguished
  by Component Description attribute, not position code.

### 6.4 Stage (Blocker vs. Default)

| Suffix | Name | Definition |
|--------|------|------------|
| (none) | Default | Compress mold (final shaping) or single mold. |
| -B | Blocker | Oversized preform, first step of two-step process. |

Rule: If -B exists, the corresponding non-B must also exist. Always a
pair. A -B mold never exists alone.

---

## 7. Mold ID vs. Physical Asset

### 7.1 Mold ID (Master Data)

The Mold ID identifies **what a mold produces** — the product definition.
It is NOT a unique identifier for a physical piece of metal.

`SA-2552-MS-PRI` = "primary midsole component of the SA-2552 sole design."

It says nothing about size, factory, copy, or revision.

### 7.2 Physical Asset Record

Each physical mold is a separate record carrying:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| Asset ID | System-generated | UUID / auto-increment | True primary key |
| Mold ID | Code | SA-2301-MS-PRI-B | Governed identifier from naming convention |
| Mold Family | Code | SA-2301 | Grouping key. Links to Shoe Style(s). |
| Design Family | Code | SA-2301 | Groups related variants (see 6.1) |
| Type | Enum | MS | OS / MS / OT |
| Position | Enum | PRI | PRI / BOT / HEEL |
| Stage | Enum | Blocker | Blocker / Compress / Single |
| Construction Type | Derived | Dual Density | Derived from sibling positions |
| Component Description | Text | Midsole Top Layer | Human-readable. Supplementary. |
| Size Coverage | Text | US7-8 | Which shoe size(s) this physical mold produces |
| Size Grouping | Enum | 1:2 | Sizes per physical mold (1:1, 1:2, 1:3) |
| Design Compound | Text | EVA 55C | Material designed to process |
| Status | Enum | Active | Active / Inactive / In Repair / Retired |
| Revision | Integer | 0 | Incremented when re-cut. 0 = original. |
| Mold Set | Enum | A | A (default/implied) / B / C / D |
| Vendor ID | Text | Factory A | Where stored/used |

### 7.3 Multiple Physical Assets, One Mold ID

| Mold ID | Size | Vendor | Set | Rev |
|---------|------|--------|-----|-----|
| SA-2552-MS-PRI | US7 | GuoSheng | A | 0 |
| SA-2552-MS-PRI | US8 | GuoSheng | A | 0 |
| SA-2552-MS-PRI | US9 | HengMao | B | 0 |
| SA-2552-MS-PRI | US9 | GuoSheng | A | 1 |

All four = same Mold ID. Different physical assets.

---

## 8. Migration from Legacy Data

### Source-to-Target Mapping

Legacy component position numbers map deterministically:

| Position # | Position Code | Logic |
|:---:|---|---|
| 1 (only component) | PRI | Count=1 → PRI |
| 1 (has siblings) | PRI | Position 1 → always PRI |
| 2 | BOT | Position 2 → BOT |
| 3 | HEEL | Position 3 → HEEL |
| Blocker in name | append -B | Explicit label |

### Legacy Suffix Migration

| Legacy Suffix | Target Attribute | Example |
|---|---|---|
| -1, -2, -3 (revision) | Revision attribute | SA-2307-1 → Revision=1 |
| -A, -B, -C (mold set) | Mold Set attribute | MRS-1873-1-C → Set=C |
| -4E, -E (width) | Separate Mold Family | SA-2654E = distinct family |
| -M, -W (gender) | Separate Mold Family | T1153M = distinct family |

### Migration Statistics (2026 dataset, all brands)

| Category | Records | % |
|---|---:|---:|
| Auto-assigned PRI (single piece) | 2,086 | 91.5% |
| Multi-piece (PRI+BOT, PRI+HEEL, 3-way) | 180 | 7.9% |
| Blockers (-B) | 14 | 0.6% |
| **Total** | **2,280** | **100%** |

---

## 9. Governance Rules

1. **No freeform mold IDs.** All identifiers must follow:
   `{MoldFamily}-{Type}-{Position}(-B)`.
2. **Mold ID = product definition.** It identifies what a mold produces,
   not which physical copy. Physical assets are tracked separately.
3. **PRI always exists.** Every Mold Family + Type must have PRI. BOT
   and HEEL cannot exist without PRI.
4. **Blocker-Default integrity.** Every -B must have a paired non-B.
5. **OT is always PRI.** Different OT components are distinguished by
   Component Description attribute.
6. **Revision tracking.** When a mold is re-cut, increment Revision
   attribute on the asset record. Do not create a new Mold ID.
7. **Mold Set tracking.** Capacity duplicates (A/B/C) share the same
   Mold ID. Distinguished by Mold Set attribute.
8. **Component Description is supplementary.** Human-readable (e.g.,
   "SCF Midsole Top Layer Blocker") but the Mold ID is governed.
9. **Style-to-Family mapping maintained separately.** One Style → one
   Mold Family. One Mold Family → many Styles (reuse).
10. **Legacy codes frozen.** All new codes must follow standard format.
    Existing non-standard codes are retained but not replicated.

---

## 10. Glossary

| Term | Definition |
|------|------------|
| Blocker | Oversized preform from first step of two-step molding. |
| BOM | Structured list of components needed for a finished product. |
| Blow Molding | Air injected into hot plastic tube inside a mold. For airbag units. |
| CM EVA | Compression Molded EVA. Most common midsole method. |
| Compression Mold | Heated mold pressing raw material into shape under pressure. |
| Component | A distinct molded part within a sole unit. |
| Construction Type | Derived: Single / Vertical / Main+Heel / 3-Way. Not in the ID. |
| Crash Pad | Lightweight IBR cushion layer under rubber outsole. Mapped as OS-BOT. |
| Design Family | Attribute grouping related Mold Families sharing same base design. |
| Dual Density | Two layers of different hardness bonded vertically. PRI + BOT. |
| Durometer | Material hardness measurement. |
| ETPU | Expanded TPU. Lightweight high-energy-return foam beads. |
| EVA | Ethylene-Vinyl Acetate. Lightweight midsole foam. |
| Footbed | Contoured insert inside shoe. Comfort, arch support. |
| Fore Part | Front outsole section in horizontal split. Industry term. |
| Heel / Top Lift | Rear sole portion. Highest impact zone. |
| IBR | Injection Blown Rubber. Lighter, flexible outsole sub-layer. |
| Injection Molding | Liquid material injected into mold under pressure and cooled. |
| Insole | Flat interior sole layer directly under foot. |
| Last | Foot-shaped form for shoe construction. Drives mold design. |
| Master Data | Standing reference data. Changes infrequently. |
| MDG | Master Data Governance. Policies ensuring data accuracy. |
| Midsole | Cushioning layer between outsole and upper. |
| Mold | Precision cavity (steel/aluminum) shaping raw materials. Capital asset. |
| Mold Family | Logical group of all molds for one sole design. |
| Mold ID | Governed identifier for what a mold produces. Not a physical asset key. |
| Mold Set | Duplicate tooling (A/B/C) for capacity or multi-factory deployment. |
| Outsole | Bottom-most layer contacting ground. Grip, traction, abrasion resistance. |
| Peba (PEBAX) | High-performance elastomer for racing midsoles. |
| Plate | Rigid element (carbon fiber, TPU) for stiffness/propulsion. |
| PLM | Product Lifecycle Management software. |
| PU | Polyurethane. Denser foam for work boots. |
| SCF | Supercritical Foam. Fine cell structure, lightweight cushioning. |
| Shank | Rigid midfoot support. Torsional stability. |
| Sole Unit | Complete assembled bottom: outsole + midsole + other components. |
| TPR | Thermoplastic Rubber. Injection moldable. Lower-cost outsole. |
| TPU | Thermoplastic Polyurethane. Durable, flexible plastic. |

---

## 12. References

1. ITC Infotech, "Sole Mold Management: Driving Footwear Tooling
   Optimization with PLM" (2026)
2. Weston Rubber, "Footwear Soling Components Explained" (2026)
3. Shoemakers Academy, "How to Design Shoe Outsole Tooling"
4. Lems Shoes, "Lems Outsoles Explained" (2026)
5. Running Warehouse AU, "Shoe Components Guide"

---

## 13. Change Log

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-06-11 | Initial standard with numeric positions (1/2/3). |
| 3.0 | 2026-06-12 | Replaced numeric positions with PRI/BOT/HEEL. Split Mold ID (product definition) from Physical Asset (metal in factory). Added Mold Set/Revision/Design Family as attributes. Formalized Mold Family as opaque identifier. Added migration rules. Updated glossary. Removed OT sub-types (OT always PRI). Renamed Compound to Design Compound. Added legacy suffix handling. |