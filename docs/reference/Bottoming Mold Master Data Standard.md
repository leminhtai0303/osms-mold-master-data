# Bottoming Mold Master Data Standard (v3.1)

Version: 3.1  
Date: 2026-06-12  
Author: Tai Le  
Audience: Bottoming Team, Raw Material Management  

---

## 1. Purpose

Define a standardized hierarchy, naming convention, and governance model  
for sole-related mold master data.

Goal: consistent naming, clean tracking, single source of truth.

---

## 2. Scope

Covers all molds used in sole production:
- Outsole (OS)
- Midsole (MS)
- Other components (OT): footbed, insole, shank, plate, etc.

Excludes:
- Upper tooling (KPU, injection PU)
- Lasting, cutting dies, non-mold assets

---

## 3. Core Concept: Two Layers

Mold data is split into two layers:

| Layer | Purpose |
|-------|--------|
| Mold ID | Defines what the mold produces |
| Physical Asset | Defines the actual mold (size, vendor, revision) |

- Mold ID = product definition  
- Asset = physical instance  

---

## 4. Hierarchy

Hierarchy structure:
- Family > Type > Position > Stage

| Level | Values |
|------|--------|
| Type | OS / MS / OT |
| Position | PRI / BOT / HEEL |
| Stage | (none) / -B |

---

## 5. Naming Convention

### Format
{MoldFamily}-{Type}-{Position}(-B)

### Rules
- Type ∈ {OS, MS, OT}
- Position ∈ {PRI, BOT, HEEL}
- PRI is mandatory
- BOT / HEEL require PRI
- OT always uses PRI
- “-B” must have matching non-B

### Examples
- SA-2301-MS-PRI  
- SA-2301-MS-PRI-B  
- SA-2301-MS-BOT  

---

## 6. Mold Family

- Opaque identifier (no embedded meaning)
- Format: Brand prefix + number
- Assigned by development team

### Rules
- Width / gender variants → new Mold Family
- Legacy suffixes (-1, -A, -B) → attributes (Revision, Set)
- Non-standard legacy codes → retained, not reused

---

## 7. Mold Type

| Code | Definition |
|------|------------|
| OS | Outsole (ground-contact) |
| MS | Midsole (cushioning) |
| OT | Other sole components |

---

## 8. Position

- PRI = main component (always exists)  
- BOT = lower layer (dual density)  
- HEEL = heel-only component  

### Construction (derived)
- PRI  
- PRI + BOT  
- PRI + HEEL  
- PRI + BOT + HEEL  

---

## 9. Stage

| Suffix | Meaning |
|--------|--------|
| (none) | Default / compress |
| -B | Blocker (preform stage) |

Rule:
- Every -B must have a matching non-B

---

## 10. Mold ID vs Physical Asset

### Mold ID
- Identifies the component definition
- Does NOT include size, vendor, or revision

Example: SA-2552-MS-PRI = primary midsole for SA-2552

---

### Physical Asset

Each physical mold is an asset record:

**Key fields:**
- Mold ID  
- Size  
- Vendor  
- Mold Set (A/B/C)  
- Revision  
- Status  

### Principle
- Multiple assets can share one Mold ID  
- Each asset = one physical mold  

---

## 11. Governance Rules

1. No freeform Mold IDs  
2. Mold ID = product definition (not asset)  
3. PRI must always exist  
4. BOT / HEEL require PRI  
5. -B must pair with non-B  
6. Revision tracked at asset level (no new Mold ID)  
7. Mold Set distinguishes duplicates (A/B/C)  
8. OT always uses PRI  
9. Style–Family mapping managed separately  
10. Legacy codes retained but not reused  

---

## 12. Appendix (Optional Reference)

- Legacy mappings (suffix → attributes)
- Glossary (materials, processes)
- Extended examples
