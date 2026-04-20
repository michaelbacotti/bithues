# Woodworking Joinery Blocks — Project File

**Status:** Idea / Planning
**Created:** 2026-04-16
**Updated:** 2026-04-16
**Folder:** `projects/joinery-blocks/`

## Concept
Building blocks like LEGO, but blocks connect via traditional woodworking joinery instead of plastic studs. Used as toys or educational tools for learning joinery techniques.

## Joinery Types to Implement

### Priority: Dovetail + Mortise/Tenon
- **Mortise and tenon** — square/rectangular connection; one block has a hole (mortise), the other has a matching peg (tenon)
- **Dovetail** — angled interlocking joint; traditionally used at corners; provides mechanical resistance against pulling apart

### Other Types
- **Finger/box joint** — interlocking rectangular fingers at 90° corners
- **Tongue and groove** — flat panel connections; tongue protrusion locks into groove
- **Dowel and peg** — small round pegs lock aligned holes
- **Biscuit joint** — flat compressed football-shaped wafers

## Dovetail Design Specs

**Standard dovetail angles:**
| Material | Angle | Ratio |
|----------|-------|-------|
| Hardwood (oak, maple) | ~7° | 1:8 |
| Softwood (pine) | ~14° | 1:4 |
| **P1S PLA/PETG** | **~10-15°** | **1:6 recommended** |

**For 3D printed dovetail:**
- Use 10-15° angle (steeper than wood — PLA is more brittle)
- Locking ratio: 1 part dovetail width at widest / 6 parts depth
- Example: 6mm wide dovetail → 10mm lock depth
- Print with 0.2mm layer lines perpendicular to the angle for strength

**Block sizes to design first:**
1. **Basic dovetail block** — 20mm cube with one face having a dovetail socket, another having the matching dovetail tab
2. **Corner dovetail block** — 90° L-shaped block for building frames
3. **Mortise/tenon starter block** — 20mm cube, mortise on one face, tenon on opposite face

## Design Specs
- Block size target: ~20mm base unit (scalable to 40mm)
- Grid increment: 10mm
- Block shapes needed: cubes, corner pieces, flat connectors, frame pieces
- Print tolerance: 0.15-0.2mm gap for PLA/PETG fit

## Software
- **Fusion 360** — primary design tool (precision required for angled dovetail geometry)
- **bambu-studio-ai** — for parametric boxes/brackets, STL export, slicing
- **Tinkercad** — quick concepts only

## Fusion 360 Scripts
See: `~/openclaw/workspace/icloud/Bacotti Bot/3D-Printing/fusion-scripts/`
- `sample_mortise_tenon_block.py` — first test script (two blocks: mortise + tenon)

## Files
| File | Description | Status |
|------|-------------|--------|
| `sample_mortise_tenon_block.py` | Mortise + tenon block pair | Ready to test |
| `dovetail_block.py` | Dovetail interlocking blocks | Not started |
| `finger_joint_block.py` | Finger/box joint blocks | Not started |