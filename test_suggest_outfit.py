# test_suggest_outfit.py
from tools import suggest_outfit

# A minimal fake listing dict (same shape search_listings returns)
fake_item = {
    "title": "Vintage Levi's Denim Jacket",
    "category": "outerwear",
    "colors": ["blue", "white"],
    "style_tags": ["vintage", "casual", "90s"],
    "brand": "Levi's",
    "condition": "good",
}

# ── Test 1: empty wardrobe ────────────────────────────────────────────────────
print("=== EMPTY WARDROBE ===")
result = suggest_outfit(fake_item, {"items": []})
print(result)
assert isinstance(result, str) and len(result) > 0, "Should return non-empty string"

# ── Test 2: wardrobe with items ───────────────────────────────────────────────
print("\n=== WITH WARDROBE ===")
fake_wardrobe = {
    "items": [
        {"title": "White Graphic Tee", "category": "top", "colors": ["white"]},
        {"title": "Black Slim Chinos", "category": "bottoms", "colors": ["black"]},
    ]
}
result = suggest_outfit(fake_item, fake_wardrobe)
print(result)
assert isinstance(result, str) and len(result) > 0, "Should return non-empty string"

# ── Test 3: missing 'items' key entirely ─────────────────────────────────────
print("\n=== MISSING ITEMS KEY ===")
result = suggest_outfit(fake_item, {})
print(result)
assert isinstance(result, str) and len(result) > 0, "Should not crash on missing key"

print("\nAll tests passed.")