# SandHybrid Mission Ledger

This file is the release-blocking source of truth for work requested on SandHybrid / Epoch Sim Lab.

## Rules

- Every requested mission remains `OPEN`, `ACTIVE`, `BLOCKED`, or `VERIFIED`.
- A mission is not complete because code exists or a README claims it exists.
- `VERIFIED` requires an automated contract where practical and a runtime acceptance check where behavior or performance is visual.
- Deferred, missed, partially implemented, or avoided work stays in this file and carries into the next release.
- Every release note must list the mission IDs it closes and the evidence used to verify them.
- Canonical cells remain authoritative. Optimization may skip, group, queue, or bulk-move work, but may not invent, delete, duplicate, reconstruct, snap, or silently refill material.

## Current architecture audit

The current hierarchy is partially implemented:

- 8x8 macro movement runs before fine movement.
- 64x64 chunks and 8x8 tiles can sleep and early-out.
- Fine movement still dispatches over the complete 640x360 grid for every phase.
- Chemistry still dispatches over the complete grid before macro movement.
- The full cell buffer is copied before fine movement every simulation tick.
- Debug `TESTS` is a theoretical maximum, not the number of pair tests actually executed.
- Debug `SWAPS` still exists in source and must remain visible in every release.
- Rendering is one fullscreen draw; debug grid cost is fragment-shader work and has not yet been measured with GPU timestamps.
- Runtime CPU concurrency is currently one native event thread plus one Vulkan simulation/render thread. There is no C++23 coroutine task runtime or CPU worker pool.

---

# P0 — Release blockers

## SIM-HIER-001 — True hierarchical work elimination

**Status:** OPEN

Replace full-grid early-out scheduling with a same-frame hierarchical scheduler.

Required pipeline:

1. Classify 64x64 chunks and 8x8 tiles before expensive cell work.
2. Build compact GPU worklists for:
   - sleeping chunks to skip,
   - macro-eligible 8x8 regions,
   - active chemistry tiles,
   - mixed/fine fallback tiles,
   - macro/fine boundary tiles.
3. Dispatch macro movement first from the compact macro worklist.
4. Dispatch fine-cell movement only for mixed, partial, damaged, reacting, half-water, actor-adjacent, and macro-boundary tiles.
5. Run a bounded boundary reconciliation pass in the same simulation tick.
6. Preserve deterministic phase ordering and canonical cell conservation.

Do not alternate entire macro and pixel frames. Do not visibly delay fine edges by one frame unless a measured, optional background-chemistry cadence proves visually identical. Movement boundaries must resolve in the same tick.

**Acceptance:**

- A world containing large uniform sand/water bodies executes substantially fewer fine invocations than the dense baseline.
- Mixed edges still move pixel-by-pixel without seams, gaps, teleportation, duplication, or one-frame holes.
- Macro-eligible regions move using the same density, fall, diagonal, viscosity, and displacement rules as fine cells.
- Debug reports actual queued macro tiles, fine fallback tiles, and boundary tiles.

## SIM-HIER-002 — No artificial block refilling

**Status:** OPEN

Do not move arbitrary pixels merely to make an 8x8 block full again. A region may become macro-eligible only when normal material motion naturally produces a valid uniform region.

Allowed:

- bounded local liquid equalization,
- density displacement,
- physically valid granular settling,
- conservative half-water merging,
- macro/fine boundary exchange.

Forbidden:

- snapping cells into aligned positions,
- synthesizing missing cells,
- deleting edge fragments,
- borrowing distant material to fill a macro-cell,
- reconstructing damaged terrain.

**Acceptance:** per-material and total represented volume remain unchanged except for explicit, audited reactions or world-boundary loss.

## SIM-HIER-003 — Remove full-buffer movement snapshot copy

**Status:** OPEN

Replace the full cell-buffer copy before fine movement with one of:

- a correct immutable neighborhood ping-pong layout,
- per-active-tile snapshot storage,
- compact boundary snapshots,
- another measured design that preserves deterministic neighborhood reads.

**Acceptance:** no full 640x360x16-byte transfer occurs every simulation tick, and movement remains race-free and deterministic.

## DBG-001 — Preserve and expand movement telemetry

**Status:** ACTIVE

The following counters must remain visible in F3 debug mode:

- simulation step,
- actual fine pair tests,
- fine swaps,
- macro pair tests,
- macro tile swaps,
- macro cells moved,
- total moved cells,
- fine fallback tiles,
- macro/fine boundary tiles,
- sleeping and active tiles,
- sleeping, active, and dirty chunks,
- cells genuinely bypassed by indirect scheduling,
- bee, ant, and beetle movement/count counters,
- structural, liquid, gas, selected-material, and FPS counters.

Current `SWAPS` source instrumentation must not be removed. Current `TESTS` must stop using `width * height * phases / 2` and count real shader work instead.

**Acceptance:** a deterministic fixture produces known non-zero fine and macro counts, and the F3 overlay displays the same values read back by the test harness.

## DBG-002 — GPU pass timing and grid-cost measurement

**Status:** OPEN

Add a Vulkan timestamp query pool around:

- tile classification,
- chunk classification,
- active-worklist construction,
- chemistry,
- macro movement,
- fine movement,
- boundary reconciliation,
- actor/factory pass,
- debug-stat collection,
- scene rendering,
- F3 grid/overlay rendering,
- queue wait/present pacing where measurable.

Show microseconds and percentage of GPU frame time in F3. Add independent debug toggles for statistics text and grid/region shading so grid cost can be measured rather than guessed.

**Acceptance:** F3 can show the measured difference between normal render, stats-only, grid-only, and full debug modes.

## GPU-CONC-001 — Async compute/graphics scheduling

**Status:** OPEN

Inspect queue-family capabilities and use the best available path:

- dedicated compute queue when available,
- graphics queue fallback when not,
- dedicated transfer queue for staging/readback when available,
- timeline semaphores for simulation/render dependencies,
- render state N while compute produces state N+1,
- no unsynchronized access to authoritative buffers.

Do not claim concurrency when all work is serialized into one primary command buffer on one queue.

**Acceptance:** debug telemetry reports selected queue topology and measured overlap. The fallback remains correct on single-queue hardware.

## CPU-CONC-001 — C++23 coroutine task runtime

**Status:** OPEN

Add a bounded coroutine/task scheduler for CPU-side work that benefits from concurrency:

- asynchronous scene load/save and PPM encoding,
- staging uploads and readbacks,
- shader reload/validation,
- debug-stat readback,
- release/runtime diagnostics,
- command-buffer preparation where safe,
- cancellation and deterministic shutdown.

Coroutines orchestrate work; GPU cell physics remains in Vulkan compute. Use a fixed worker pool rather than creating transient threads per task.

**Acceptance:** window/input remains responsive during save/load/readback, shutdown joins deterministically, and ThreadSanitizer-capable CPU contracts find no data race in shared task state.

## ATM-001 — Passable conserved atmosphere and liquids

**Status:** OPEN

Gases and liquids are atmospheric/fluid volume, not blocking occupancy tiles for living actors.

- Player, bees, ants, beetles, and plants may coexist spatially with gases.
- Bugs and the player must not be displaced, trapped, duplicated, or deleted by gas placement.
- Liquids may spatially overlap actor occupancy through the actor layer while still causing drowning/non-breathable conditions.
- Sealed structural materials contain gas/liquid volume.
- Displacing fluid into less available volume raises local pressure; it does not delete fluid.
- The closed system must conserve gas/liquid volume except audited reactions and explicit boundary vents.

**Acceptance:** pressure, volume, and per-material conservation tests pass through movement, painting, actor motion, save/load, and macro/fine transitions.

## ATM-002 — Respiration and suffocation

**Status:** OPEN

Every living entity requires breathable oxygen.

- Living entities consume local oxygen and return carbon dioxide.
- They suffocate when conserved breathable oxygen reaches zero locally.
- They also suffocate when completely surrounded by non-breathable gases or liquid with no reachable breathable volume.
- Gas placement itself is passable and cannot pin insects.
- No living entity is globally exempt from oxygen requirements.

**Acceptance:** player, bees, ants, beetles, and plants survive in oxygen, consume it at configured rates, produce CO2, and die predictably in vacuum/non-breathable enclosures.

## ATM-003 — Water aeration and half-water correction

**Status:** OPEN

- Reduce oxygen generated by falling water to a conservative, bounded rate.
- Oxygen creation must consume or transfer represented dissolved/entrained gas rather than create unbounded volume.
- Eliminate isolated one-half-water pockets through local conservative merging/equalization.
- Half-water must never multiply oxygen production or increase total water volume.

**Acceptance:** waterfall stress tests show stable water and oxygen totals, no unbounded GPU load growth, and no persistent isolated half-water specks after settling.

## UI-001 — Input and cursor reliability

**Status:** OPEN

- Cursor size and shape controls remain responsive.
- Buttons must not require hard or repeated presses.
- Eraser remains visible and selectable.
- Element cards and keyboard mappings stay synchronized.
- Mouse zoom and deliberately slow middle-drag pan remain functional.
- Connected fill command remains available.
- F3 debug mode preserves all useful counters, including swaps.

**Acceptance:** automated hit-test contracts plus a manual 10-minute input soak show no lost clicks, stuck state, or control overlap at supported window sizes.

## BEE-001 — Hive and swarm correctness

**Status:** OPEN

- Restore the approved suspended/default hive design from repository history; do not reconstruct it from screenshots.
- Use it as the default and in relevant scenes.
- Bees must move through gases without being blocked.
- Swarm state alternates between the biohazard mask and circular/orbit state.
- Biohazard is the dominant state, currently targeted at roughly two-thirds of the cycle unless superseded by a later explicit ratio.
- Bees must reliably return to biohazard formation.
- Formation changes must not overwrite ecology, foraging, queen, pollen, honey, migration, or suffocation behavior.

**Acceptance:** deterministic swarm timer tests and runtime captures show repeated biohazard -> circle -> biohazard cycles with no permanent stuck state.

## REL-001 — Verified release gate

**Status:** OPEN

No release is published until:

- Windows Release build passes,
- Linux Release build passes,
- shader contracts pass,
- material/conservation contracts pass,
- hierarchy counters pass deterministic fixtures,
- GPU timing queries return valid results,
- UI input soak passes,
- atmosphere/respiration tests pass,
- release assets identify the source commit and version.

---

# P1 — Required follow-up

## GPU-SPARSE-001 — Active chunk indirect dispatch

**Status:** OPEN

Build compact active chunk/tile lists and use indirect dispatch so sleeping space is not launched at all. Preserve dense authoritative storage initially for save compatibility; sparse storage is a later independent migration.

## RENDER-001 — Stable render/simulation decoupling

**Status:** OPEN

Maintain fixed 60 Hz deterministic simulation and up to 120 FPS presentation while rendering an immutable completed simulation state. Rendering must never stall simulation solely to read debug values.

## RENDER-002 — Debug overlay efficiency

**Status:** OPEN

Keep the single fullscreen draw unless measurements justify a split. Reduce repeated fragment work by precomputing debug panel text/counters where useful, and measure all changes with timestamp queries. Never remove useful data merely to improve FPS.

## SCENE-001 — Scene alignment and atmosphere

**Status:** OPEN

- Rebuild authored structures with aligned bricks where structural rules require them.
- Remove accidental one-pixel structural glass/walls.
- Ensure vacuum/eraser test scenes begin with the intended oxygen volume.
- Replace authored lava sources with magma vents where requested, while preserving intentionally simulated lava produced by vents.
- Preserve moddable image save/load paths.

## SCENE-002 — Default scene and material coverage

**Status:** OPEN

Verify default scenes, engineering lab, ecosystem, platformer, volcano, waterworks, demolition, frontier base, and blank/test scenes against their requested contents, atmosphere, actors, machines, hives, and material controls.

## PERF-001 — Performance regression suite

**Status:** OPEN

Add repeatable benchmarks for:

- empty/sleeping world,
- uniform falling sand macro body,
- uniform water basin,
- mixed sand/water boundary,
- active ecology/hive,
- volcano/chemistry stress,
- full F3 debug,
- grid-only debug,
- atmosphere pressure enclosure.

Record GPU pass timings, queue occupancy, macro/fine work counts, frame time, simulation time, and conservation errors.

---

# Carry-forward product missions

These remain open until explicitly verified in the release that claims them:

- Canonical material behavior independent of creation source.
- No silent material deletion or provenance-dependent physics.
- Per-metal melting/vaporization thresholds and preserved damaged mass.
- Plastic thermal/fire/lava behavior.
- Stable flowing water, oil, honey, acid, saltwater, dirty water, and lava.
- Terrain stability without reconstruction; two laser hits per pixel; collapse after more than half is dislodged.
- Near-zero-loss ecology and gas cycle.
- Correct magma vent pressure/eruption behavior.
- Exact Alt-hover inspection card.
- Player movement, mining, shooting, health, oxygen, and tools.
- Material colors/readability and future gas-presentation boundary.
- Debug counters for movement, materials, ecology, hierarchy, conservation, and GPU timings.
- Moddable scene image save/load.
- Windows and Linux release packages.

## Release checklist

Before closing any mission:

1. Link the implementation commit.
2. Link the automated contract or benchmark.
3. Record the runtime reproduction procedure.
4. Record before/after counters or timings.
5. Confirm no open mission was silently removed from this ledger.
