#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
reset = (ROOT / "shaders/reset.comp").read_text(encoding="utf-8")
paint = (ROOT / "shaders/paint.comp").read_text(encoding="utf-8")
swarm = (ROOT / "shaders/bee_swarm.glsl").read_text(encoding="utf-8")
errors: list[str] = []

for token in (
    "Restored from the ecosystem hive immediately before PR #19 replaced it",
    "return defaultHiveMaterial(p, sandboxHiveQueen(), material);",
    "material = defaultHiveMaterial(p, ecosystemHiveQueen(), material);",
    "scene == SCENE_SANDBOX || scene == SCENE_ECOSYSTEM",
    "p.x > queen.x - 38 && p.x < queen.x + 30",
    "p.y > queen.y - 17 && p.y < queen.y - 12",
    "q2 >= 25 && q2 < 92",
    "q.x >= 1 && q.x <= 10 && abs(q.y) <= 1",
    "!defaultHivePerchForScene(scene, p)",
):
    if token not in reset:
        errors.append(f"reset: missing {token}")

for token in (
    "The buildable hive is the same suspended ecosystem prefab",
    "delta.x > -38 && delta.x < 30",
    "delta.y > -17 && delta.y < -12",
    "distanceSquared >= 25 && distanceSquared < 92",
    "delta.x >= 1 && delta.x <= 10",
    "colonySlot = beeFormationSlotFromOffset(delta);",
):
    if token not in paint:
        errors.append(f"paint: missing {token}")

for token in (
    "const uint BEE_SWARM_BIOHAZARD_TICKS = 1800u;",
    "const uint BEE_SWARM_CIRCLE_TICKS = 900u;",
    "BEE_SWARM_BIOHAZARD_TICKS + BEE_SWARM_CIRCLE_TICKS",
    "BEE_BIOHAZARD_PACKED",
    "BEE_SPAWN_PACKED",
    "BEE_SPAWN_SLOT",
    "beeBiohazardTargetOffset",
    "beeCircleTargetOffset",
    "beeSwarmState(step) == 0u",
):
    if token not in swarm:
        errors.append(f"swarm: missing {token}")

for forbidden in (
    "BEE_INITIAL_PACKED",
    "beeCloudTargetOffset",
    "beeHaloTargetOffset",
    "return reverse ? 2u - alternate : 1u + alternate",
):
    if forbidden in swarm:
        errors.append(f"swarm: obsolete third-state contract remains: {forbidden}")


def parse_array(name: str) -> list[int]:
    match = re.search(rf"const uint {name}\[BEE_FORMATION_COUNT\] = uint\[\]\((.*?)\);", swarm, re.S)
    if not match:
        errors.append(f"swarm: unable to parse {name}")
        return []
    return [int(value) for value in re.findall(r"(\d+)u", match.group(1))]


bio = parse_array("BEE_BIOHAZARD_PACKED")
spawn = parse_array("BEE_SPAWN_PACKED")
slots = parse_array("BEE_SPAWN_SLOT")
for name, values in (("biohazard", bio), ("spawn", spawn), ("slot", slots)):
    if len(values) != 200:
        errors.append(f"{name}: expected 200 values, found {len(values)}")
if len(set(bio)) != len(bio):
    errors.append("biohazard mask contains duplicate cells")
if len(set(spawn)) != len(spawn):
    errors.append("spawn mask contains duplicate cells")
if sorted(slots) != list(range(200)):
    errors.append("spawn slot map is not a permutation of all 200 bee identities")
if spawn != sorted(spawn):
    errors.append("spawn keys are not sorted for bounded binary lookup")

for packed in spawn:
    x = (packed & 127) - 64
    y = (packed >> 7) - 64
    if x * x + y * y < 92:
        errors.append(f"spawn cell overlaps hive shell/chamber at {(x, y)}")
    if -38 < x < 30 and -17 < y < -12:
        errors.append(f"spawn cell overlaps restored wooden perch at {(x, y)}")

bio_ticks = re.search(r"BEE_SWARM_BIOHAZARD_TICKS = (\d+)u", swarm)
circle_ticks = re.search(r"BEE_SWARM_CIRCLE_TICKS = (\d+)u", swarm)
if not bio_ticks or not circle_ticks:
    errors.append("unable to parse swarm state durations")
elif int(bio_ticks.group(1)) != 2 * int(circle_ticks.group(1)):
    errors.append("biohazard/circle duration is not exactly 2:1")

if errors:
    raise SystemExit("\n".join(errors))
print("Fix36 audit passed: restored pre-PR19 suspended hives, two live scene colonies, 200 collision-free bee identities, and exact 2:1 biohazard/circle timing.")
