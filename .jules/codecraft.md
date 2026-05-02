# CodeCraft Journal

## 2025-05-14 - Optimized generator hot loop
**Mode:** Bolt
**Learning:** `Object.keys().sort()` inside a loop that runs thousands of times is extremely expensive in JS. Pre-calculating sorted candidate lists and using `Set` for character set lookups provides a significant speedup.
**Measurement:** 50,000 characters generation time reduced from ~0.93s to ~0.47s (Variety 50) and ~1.3s to ~0.60s (Variety 100), effectively doubling performance under variety pressure.
**Action:** Always pre-calculate data structures and use efficient lookups (Set/Map) for operations inside performance-critical loops.

## 2025-05-15 - Redundant parsing and character mapping alignment
**Mode:** Bolt
**Learning:** Re-parsing and re-building trigram data structures (duplets) on every "Generate" click is redundant and creates a lag spike (~100ms for English corpus). Implementing a granular cache that only invalidates when input data or transformation parameters (case mode, filter) change significantly improves user-perceived responsiveness for repeated generations. Additionally, initializing character mappings by iterating over the source string and using `toUpperCase()` is safer than index-based iteration when source strings might have misaligned characters or different lengths.
**Measurement:** Second and subsequent generations are now near-instant, as the ~100ms parsing overhead is skipped.
**Action:** Encapsulate heavy data processing into update-on-demand methods and use robust transformation logic for international character sets.

## 2026-05-02 - Enhanced Interactive Experience and Caching logic
**Mode:** Palette & Bolt
**Learning:** Adding live-preview (auto-generation on input) significantly improves UX but requires robust debouncing and silent failure modes (no alerts on empty input) to avoid being intrusive. Caching complex objects like kerning tweaks (which involve O(N) loops and Math.pow) is essential when many UI triggers can fire rapidly.
**Action:** Always implement debouncing for live-preview features and ensure dependency tracking for expensive re-computations to maintain 60fps UI responsiveness.
