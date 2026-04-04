# CodeCraft Journal

## 2025-05-14 - Optimized generator hot loop
**Mode:** Bolt
**Learning:** `Object.keys().sort()` inside a loop that runs thousands of times is extremely expensive in JS. Pre-calculating sorted candidate lists and using `Set` for character set lookups provides a significant speedup.
**Measurement:** 50,000 characters generation time reduced from ~0.93s to ~0.47s (Variety 50) and ~1.3s to ~0.60s (Variety 100), effectively doubling performance under variety pressure.
**Action:** Always pre-calculate data structures and use efficient lookups (Set/Map) for operations inside performance-critical loops.
