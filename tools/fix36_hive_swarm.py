#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one replacement, found {count}")
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, replacement: str, label: str) -> str:
    output, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one regex replacement, found {count}")
    return output


BIOHAZARD_PACKED = """const uint BEE_BIOHAZARD_PACKED[BEE_FORMATION_COUNT] = uint[](
    2366u, 2370u, 2489u, 2503u, 2741u, 2763u, 2879u, 2883u, 2993u, 3002u,
    3023u, 3144u, 3254u, 3404u, 3501u, 3539u, 3634u, 3791u, 4011u, 4053u,
    4143u, 4306u, 4521u, 4567u, 4653u, 4926u, 4930u, 4948u, 5160u, 5178u,
    5190u, 5208u, 5292u, 5559u, 5577u, 5588u, 5800u, 5804u, 5848u, 6069u,
    6091u, 6099u, 6205u, 6211u, 6313u, 6359u, 6446u, 6572u, 6577u, 6580u,
    6583u, 6592u, 6601u, 6604u, 6607u, 6612u, 6696u, 6715u, 6725u, 6737u,
    6744u, 6819u, 6877u, 6955u, 6960u, 6997u, 7071u, 7085u, 7091u, 7093u,
    7095u, 7113u, 7115u, 7117u, 7121u, 7125u, 7137u, 7208u, 7217u, 7247u,
    7258u, 7332u, 7342u, 7378u, 7452u, 7518u, 7524u, 7603u, 7604u, 7628u,
    7629u, 7712u, 7727u, 7761u, 7856u, 7888u, 7961u, 8034u, 8039u, 8107u,
    8149u, 8220u, 8243u, 8269u, 8421u, 8471u, 8489u, 8535u, 8553u, 8624u,
    8656u, 8730u, 8884u, 8908u, 9062u, 9109u, 9128u, 9176u, 9195u, 9369u,
    9395u, 9399u, 9417u, 9421u, 9641u, 9687u, 9703u, 9749u, 9787u, 9797u,
    9835u, 9881u, 9911u, 9920u, 9929u, 10046u, 10050u, 10155u, 10197u, 10215u,
    10262u, 10301u, 10307u, 10346u, 10427u, 10432u, 10437u, 10522u, 10542u, 10578u,
    10674u, 10679u, 10684u, 10687u, 10692u, 10697u, 10702u, 10853u, 10903u, 10946u,
    10985u, 11036u, 11197u, 11199u, 11201u, 11362u, 11417u, 11461u, 11495u, 11551u,
    11578u, 11711u, 11713u, 11743u, 11849u, 11933u, 11939u, 11958u, 11995u, 12003u,
    12072u, 12091u, 12101u, 12109u, 12192u, 12204u, 12209u, 12242u, 12246u, 12256u,
    12453u, 12471u, 12489u, 12507u, 12595u, 12621u, 12713u, 12718u, 12754u, 12759u
);"""

SPAWN_PACKED = """const uint BEE_SPAWN_PACKED[BEE_FORMATION_COUNT] = uint[](
    2366u, 2370u, 2489u, 2503u, 2741u, 2763u, 2879u, 2883u, 2993u, 3002u,
    3023u, 3144u, 3254u, 3404u, 3501u, 3539u, 3634u, 3791u, 4011u, 4053u,
    4143u, 4306u, 4521u, 4567u, 4653u, 4926u, 4930u, 4948u, 5160u, 5178u,
    5190u, 5208u, 5292u, 5559u, 5577u, 5588u, 5800u, 5804u, 5848u, 6057u,
    6069u, 6077u, 6083u, 6091u, 6099u, 6103u, 6696u, 6700u, 6702u, 6705u,
    6708u, 6711u, 6715u, 6720u, 6725u, 6729u, 6732u, 6735u, 6737u, 6740u,
    6744u, 6819u, 6877u, 6955u, 6960u, 6997u, 7071u, 7085u, 7091u, 7093u,
    7095u, 7113u, 7115u, 7117u, 7121u, 7125u, 7137u, 7208u, 7217u, 7247u,
    7258u, 7332u, 7342u, 7378u, 7452u, 7518u, 7524u, 7603u, 7604u, 7628u,
    7629u, 7712u, 7727u, 7761u, 7856u, 7888u, 7961u, 8034u, 8039u, 8107u,
    8149u, 8220u, 8243u, 8269u, 8421u, 8471u, 8489u, 8535u, 8553u, 8624u,
    8656u, 8730u, 8884u, 8908u, 9062u, 9109u, 9128u, 9176u, 9195u, 9369u,
    9395u, 9399u, 9417u, 9421u, 9641u, 9687u, 9703u, 9749u, 9787u, 9797u,
    9835u, 9881u, 9911u, 9920u, 9929u, 10046u, 10050u, 10155u, 10197u, 10215u,
    10262u, 10301u, 10307u, 10346u, 10427u, 10432u, 10437u, 10522u, 10542u, 10578u,
    10674u, 10679u, 10684u, 10687u, 10692u, 10697u, 10702u, 10853u, 10903u, 10946u,
    10985u, 11036u, 11197u, 11199u, 11201u, 11362u, 11417u, 11461u, 11495u, 11551u,
    11578u, 11711u, 11713u, 11743u, 11849u, 11933u, 11939u, 11958u, 11995u, 12003u,
    12072u, 12091u, 12101u, 12109u, 12192u, 12204u, 12209u, 12242u, 12246u, 12256u,
    12453u, 12471u, 12489u, 12507u, 12595u, 12621u, 12713u, 12718u, 12754u, 12759u
);"""

SPAWN_SLOTS = """const uint BEE_SPAWN_SLOT[BEE_FORMATION_COUNT] = uint[](
    0u, 1u, 2u, 3u, 4u, 5u, 6u, 7u, 8u, 9u,
    10u, 11u, 12u, 13u, 14u, 15u, 16u, 17u, 18u, 19u,
    20u, 21u, 22u, 23u, 24u, 25u, 26u, 27u, 28u, 29u,
    30u, 31u, 32u, 33u, 34u, 35u, 36u, 37u, 38u, 44u,
    39u, 42u, 43u, 40u, 41u, 45u, 56u, 47u, 46u, 48u,
    49u, 50u, 57u, 51u, 58u, 52u, 53u, 54u, 59u, 55u,
    60u, 61u, 62u, 63u, 64u, 65u, 66u, 67u, 68u, 69u,
    70u, 71u, 72u, 73u, 74u, 75u, 76u, 77u, 78u, 79u,
    80u, 81u, 82u, 83u, 84u, 85u, 86u, 87u, 88u, 89u,
    90u, 91u, 92u, 93u, 94u, 95u, 96u, 97u, 98u, 99u,
    100u, 101u, 102u, 103u, 104u, 105u, 106u, 107u, 108u, 109u,
    110u, 111u, 112u, 113u, 114u, 115u, 116u, 117u, 118u, 119u,
    120u, 121u, 122u, 123u, 124u, 125u, 126u, 127u, 128u, 129u,
    130u, 131u, 132u, 133u, 134u, 135u, 136u, 137u, 138u, 139u,
    140u, 141u, 142u, 143u, 144u, 145u, 146u, 147u, 148u, 149u,
    150u, 151u, 152u, 153u, 154u, 155u, 156u, 157u, 158u, 159u,
    160u, 161u, 162u, 163u, 164u, 165u, 166u, 167u, 168u, 169u,
    170u, 171u, 172u, 173u, 174u, 175u, 176u, 177u, 178u, 179u,
    180u, 181u, 182u, 183u, 184u, 185u, 186u, 187u, 188u, 189u,
    190u, 191u, 192u, 193u, 194u, 195u, 196u, 197u, 198u, 199u
);"""


swarm = read("shaders/bee_swarm.glsl")
header = f"""const uint BEE_SWARM_BIOHAZARD_TICKS = 1800u;
const uint BEE_SWARM_CIRCLE_TICKS = 900u;
// Compatibility name retained for the inherited ecology audit. There is now
// exactly one alternate state: the swarm circle.
const uint BEE_SWARM_ALTERNATE_TICKS = BEE_SWARM_CIRCLE_TICKS;
const uint BEE_SWARM_CYCLE_TICKS = BEE_SWARM_BIOHAZARD_TICKS + BEE_SWARM_CIRCLE_TICKS;

{BIOHAZARD_PACKED}

// Spawn positions preserve all 200 identities without overwriting the restored
// wooden perch or hive shell. Each entry maps back to its biohazard target slot.
{SPAWN_PACKED}

{SPAWN_SLOTS}"""
swarm = sub_once(
    swarm,
    r"const uint BEE_SWARM_BIOHAZARD_TICKS.*?\n\);\n\nuint beeHash32",
    header + "\n\nuint beeHash32",
    "swarm constants and masks",
)
formation_functions = """ivec2 beeFormationOffset(uint slot) {
    uint packedValue = BEE_BIOHAZARD_PACKED[min(slot, BEE_FORMATION_COUNT - 1u)];
    return ivec2(int(packedValue & 127u) - 64, int(packedValue >> 7u) - 64);
}

int beeFormationSlotFromOffset(ivec2 offset) {
    if (offset.x < -64 || offset.x > 63 || offset.y < -64 || offset.y > 63) return -1;
    uint key = (uint(offset.y + 64) << 7u) | uint(offset.x + 64);
    int low = 0;
    int high = int(BEE_FORMATION_COUNT) - 1;
    for (int iteration = 0; iteration < 8 && low <= high; ++iteration) {
        int middle = (low + high) / 2;
        uint middleKey = BEE_SPAWN_PACKED[middle];
        if (key == middleKey) return int(BEE_SPAWN_SLOT[middle]);
        if (key < middleKey) high = middle - 1;
        else low = middle + 1;
    }
    return -1;
}

uint beeFormationSlotFromAux"""
swarm = sub_once(
    swarm,
    r"ivec2 beeFormationOffset\(uint slot\).*?\n\}\n\nuint beeFormationSlotFromAux",
    formation_functions,
    "formation lookup",
)
state_functions = """uint beeSwarmState(uint step) {
    return (step % BEE_SWARM_CYCLE_TICKS) < BEE_SWARM_BIOHAZARD_TICKS ? 0u : 1u;
}

ivec2 beeBiohazardTargetOffset(uint slot, uint step, ivec2 home) {
    const uint increments[8] = uint[8](1u, 3u, 7u, 9u, 11u, 13u, 17u, 19u);
    uint epoch = step / 90u;
    uint increment = increments[beeHash32(uint(home.x) ^ (uint(home.y) << 16u) ^ epoch) & 7u];
    uint targetSlot = (slot + epoch * increment) % BEE_FORMATION_COUNT;
    ivec2 anchor = beeFormationOffset(targetSlot);
    ivec2 flutter = beeRotateOffset(ivec2(1 + int(slot & 1u), 0), step / 3u + slot * 5u);
    return anchor + flutter;
}

ivec2 beeCircleTargetOffset(uint slot, uint step) {
    // A breathing annulus rather than a rigid geometric ring. Bees keep their
    // individual circulation while the colony reads as one round swarm.
    int radius = 37 + int((slot * 13u) % 12u);
    uint phase = step / 9u + slot * 7u;
    return beeRotateOffset(ivec2(radius, 0), phase) +
           beeRotateOffset(ivec2(2 + int(slot & 1u), 0), step / 3u + slot * 11u);
}

ivec2 beeSwarmTarget(uint aux, uint step) {
    uint slot = beeFormationSlotFromAux(aux);
    ivec2 home = beeHomeCenterFromAux(aux);
    ivec2 offset = beeSwarmState(step) == 0u
        ? beeBiohazardTargetOffset(slot, step, home)
        : beeCircleTargetOffset(slot, step);
    return home + offset;
}

ivec2 beeOrbitTarget(uint aux, uint step) { return beeSwarmTarget(aux, step); }
"""
swarm = sub_once(
    swarm,
    r"uint beeSwarmState\(.*?ivec2 beeOrbitTarget\(uint aux, uint step\) \{ return beeSwarmTarget\(aux, step\); \}\n",
    state_functions,
    "two-state swarm cycle",
)
write("shaders/bee_swarm.glsl", swarm)


reset = read("shaders/reset.comp")
brick_stair = """bool brickStair(ivec2 p, ivec2 startBrick, int count, bool risingRight) {
    ivec2 brick = brickCoordinate(p);
    int localX = brick.x - startBrick.x;
    if (localX < 0 || localX >= count) return false;
    int stairY = risingRight ? startBrick.y - localX : startBrick.y + localX;
    return brick.y == stairY;
}
"""
hive_helpers = """
// Restored from the ecosystem hive immediately before PR #19 replaced it.
// Sandbox and Ecosystem deliberately share this one canonical live prefab.
ivec2 sandboxHiveQueen() {
    return ivec2(int(pc.width * 4u / 5u), int(pc.height) - 126);
}

ivec2 ecosystemHiveQueen() {
    return ivec2(int(pc.width * 4u / 5u), int(pc.height) - 128);
}

ivec2 hiveQueenForScene(uint scene) {
    return scene == SCENE_SANDBOX ? sandboxHiveQueen() : ecosystemHiveQueen();
}

bool defaultHivePerch(ivec2 p, ivec2 queen) {
    return p.x > queen.x - 38 && p.x < queen.x + 30 &&
           p.y > queen.y - 17 && p.y < queen.y - 12;
}

uint defaultHiveMaterial(ivec2 p, ivec2 queen, uint material) {
    ivec2 q = p - queen;
    int q2 = q.x * q.x + q.y * q.y;
    if (defaultHivePerch(p, queen)) material = MAT_WOOD;
    if (q2 >= 25 && q2 < 92) material = MAT_BEE_NEST;
    if (q2 == 0) material = MAT_QUEEN_BEE;
    else if (q.x >= 1 && q.x <= 10 && abs(q.y) <= 1) material = MAT_EMPTY;
    else if (q2 < 25) {
        uint chamberPattern = hash32(indexOf(p) ^ pc.seed);
        material = (chamberPattern & 3u) == 0u ? MAT_EMPTY
            : (((chamberPattern >> 2u) & 1u) == 0u ? MAT_HONEY : MAT_POLLEN);
    }
    int formationSlot = beeFormationSlotFromOffset(q);
    if (material == MAT_EMPTY && formationSlot >= 0) material = MAT_BEE;
    return material;
}

bool defaultHivePerchForScene(uint scene, ivec2 p) {
    if (scene != SCENE_SANDBOX && scene != SCENE_ECOSYSTEM) return false;
    return defaultHivePerch(p, hiveQueenForScene(scene));
}
"""
reset = replace_once(reset, brick_stair, brick_stair + hive_helpers, "insert canonical hive helpers")
reset = replace_once(
    reset,
    """    if (d.y >= 0 && d.y < 48 && abs(d.x) < 52 - d.y) material = MAT_SAND;
    return material;
}""",
    """    if (d.y >= 0 && d.y < 48 && abs(d.x) < 52 - d.y) material = MAT_SAND;
    return defaultHiveMaterial(p, sandboxHiveQueen(), material);
}""",
    "sandbox hive",
)
reset = sub_once(
    reset,
    r"ivec2 ecosystemQueen\(\) \{.*?\n\}\n\nuint ecosystemMaterial",
    "uint ecosystemMaterial",
    "remove replaced ecosystem queen helper",
)
reset = sub_once(
    reset,
    r"    // Fix29 compact hive plus a hidden moving swarm mask\..*?    if \(material == MAT_EMPTY && formationSlot >= 0\) material = MAT_BEE;\n",
    "    material = defaultHiveMaterial(p, ecosystemHiveQueen(), material);\n",
    "ecosystem hive",
)
reset = replace_once(
    reset,
    """    return (isBlockCapable(material) || authoredTerrain) &&
           !looseAuthoredCargo(scene, p, material) &&
           !looseAuthoredTerrain(scene, p, material);""",
    """    return (isBlockCapable(material) || authoredTerrain) &&
           !looseAuthoredCargo(scene, p, material) &&
           !looseAuthoredTerrain(scene, p, material) &&
           !defaultHivePerchForScene(scene, p);""",
    "keep hive perch non-structural",
)
reset = replace_once(
    reset,
    """    if (scene == SCENE_ECOSYSTEM && material == MAT_BEE) {
        ivec2 queen = ecosystemQueen();
        int slot = beeFormationSlotFromOffset(p - queen);
        if (slot >= 0) {
            cell.aux |= BEE_AUX_SWARM | BEE_AUX_FED;
            cell.aux = beePackMetadata(cell.aux, queen, uint(slot));
            cell.age = beePackAge(uint((slot * 17) % 900), BEE_TARGET_NONE);
        }
    }""",
    """    if ((scene == SCENE_SANDBOX || scene == SCENE_ECOSYSTEM) && material == MAT_BEE) {
        ivec2 queen = hiveQueenForScene(scene);
        int slot = beeFormationSlotFromOffset(p - queen);
        if (slot >= 0) {
            cell.aux |= BEE_AUX_SWARM | BEE_AUX_FED;
            cell.aux = beePackMetadata(cell.aux, queen, uint(slot));
            cell.age = beePackAge(uint((slot * 17) % 900), BEE_TARGET_NONE);
        }
    }""",
    "initialize both scene colonies",
)
write("shaders/reset.comp", reset)


paint = read("shaders/paint.comp")
paint = sub_once(
    paint,
    r"    Cell cell;\n    int colonySlot = -1;\n    if \(material == MAT_BEE_NEST\) \{.*?    \} else \{\n        cell = makeCell\(material\);\n    \}",
    """    Cell cell;
    int colonySlot = -1;
    if (material == MAT_BEE_NEST) {
        // The buildable hive is the same suspended ecosystem prefab used by
        // Sandbox and Ecosystem, including its queen, chambers and 200 bees.
        uint prefabMaterial = MAT_EMPTY;
        bool prefabCell = false;
        if (delta.x > -38 && delta.x < 30 && delta.y > -17 && delta.y < -12) {
            prefabMaterial = MAT_WOOD;
            prefabCell = true;
        }
        if (distanceSquared >= 25 && distanceSquared < 92) {
            prefabMaterial = MAT_BEE_NEST;
            prefabCell = true;
        }
        if (all(equal(p, center))) {
            prefabMaterial = MAT_QUEEN_BEE;
            prefabCell = true;
        } else if (delta.x >= 1 && delta.x <= 10 && abs(delta.y) <= 1) {
            prefabMaterial = MAT_EMPTY;
            prefabCell = true;
        } else if (distanceSquared < 25) {
            uint chamberPattern = cellHash(p, 0xb33u);
            prefabMaterial = (chamberPattern & 3u) == 0u ? MAT_EMPTY :
                (((chamberPattern >> 2u) & 1u) == 0u ? MAT_HONEY : MAT_POLLEN);
            prefabCell = true;
        }
        if (!prefabCell) {
            colonySlot = beeFormationSlotFromOffset(delta);
            if (colonySlot < 0) return;
            prefabMaterial = MAT_BEE;
        }
        cell = makeCell(prefabMaterial);
    } else {
        cell = makeCell(material);
    }""",
    "buildable canonical hive",
)
write("shaders/paint.comp", paint)

print("Applied Fix36: restored the pre-PR19 suspended hive in both scenes and reduced bees to a 2:1 biohazard/circle cycle.")
