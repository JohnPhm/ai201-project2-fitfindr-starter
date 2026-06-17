# test_create_fit_card.py
from tools import suggest_outfit, create_fit_card

fake_item = {
    "title": "90s Track Jacket — Navy/White Stripe",
    "price": 45.00,
    "platform": "depop",
    "category": "outerwear",
    "colors": ["navy", "white"],
    "style_tags": ["90s", "vintage", "athletic", "streetwear"],
    "brand": None,
    "condition": "excellent",
}

fake_outfit = "Pair with white graphic tee and black slim chinos for a clean 90s streetwear look."

# Run 3 times on identical input — outputs should differ
for i in range(3):
    print(f"\n=== Run {i+1} ===")
    print(create_fit_card(fake_outfit, fake_item))

# Test the empty outfit guard
print("\n=== EMPTY OUTFIT GUARD ===")
result = create_fit_card("", fake_item)
print(result)
assert "Error" in result, "Should return error string for empty outfit"