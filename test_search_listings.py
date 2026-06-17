"""
test_search_listings.py

Quick smoke test for search_listings. Run with:
    python test_search_listings.py
"""

from tools import search_listings


def show(label: str, results: list[dict]):
    print(f"\n{'─' * 60}")
    print(f"TEST: {label}")
    if not results:
        print("  → No results returned (empty list)")
    else:
        print(f"  → {len(results)} result(s):")
        for r in results:
            print(f"     [{r['id']}] {r['title']} | ${r['price']} | size: {r['size']}")


# ── 1. Keyword only ───────────────────────────────────────────────────────────
# Expects: listings matching "vintage graphic tee" keywords, best matches first
show(
    "keyword only — 'vintage graphic tee'",
    search_listings("vintage graphic tee"),
)

# ── 2. Size filter ────────────────────────────────────────────────────────────
# Expects: "M" should match sizes like "S/M", "M", "M/L" — NOT "XL"
show(
    "size filter — 'y2k top', size='M'",
    search_listings("y2k top", size="M"),
)

# ── 3. Price ceiling ──────────────────────────────────────────────────────────
# Expects: no result priced above $30
show(
    "price ceiling — 'denim', max_price=30.00",
    search_listings("denim", max_price=30.00),
)

# ── 4. All three filters combined ─────────────────────────────────────────────
# Expects: only size-L items, under $25, matching "vintage"
show(
    "all filters — 'vintage', size='L', max_price=25.00",
    search_listings("vintage", size="L", max_price=25.00),
)

# ── 5. No keyword match ───────────────────────────────────────────────────────
# Expects: empty list (nothing in the dataset matches these words)
show(
    "no keyword match — 'skateboard helmet pads'",
    search_listings("skateboard helmet pads"),
)

# ── 6. Price too low for anything ────────────────────────────────────────────
# Expects: empty list (everything costs more than $1)
show(
    "price wipes everything — 'jacket', max_price=1.00",
    search_listings("jacket", max_price=1.00),
)

# ── 7. Size with no matches ───────────────────────────────────────────────────
# Expects: empty list (no listings sized XXS)
show(
    "size wipes everything — 'top', size='XXS'",
    search_listings("top", size="XXS"),
)

print(f"\n{'─' * 60}")
print("Smoke tests complete.")