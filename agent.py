"""
agent.py

The FitFindr planning loop. Orchestrates the three tools in response to a
natural language user query, passing state between them via a session dict.

Complete tools.py and test each tool in isolation before implementing this file.

Usage (once implemented):
    from agent import run_agent
    from utils.data_loader import get_example_wardrobe

    result = run_agent(
        query="vintage graphic tee under $30, size M",
        wardrobe=get_example_wardrobe(),
    )
    print(result["fit_card"])
    print(result["error"])   # None on success
"""

import re

from tools import search_listings, suggest_outfit, create_fit_card


# ── query parsing ─────────────────────────────────────────────────────────────

def _parse_query(query: str) -> dict:
    """
    Extract description, size, and max_price from a natural language query.

    Uses regex heuristics rather than an LLM call, since the inputs are short
    and the patterns (a dollar price, a "size X" token) are predictable.
    """
    working = query

    # Extract max_price: matches "$30", "under 30", "under $30 dollars"
    max_price = None
    price_match = re.search(r"\$?(\d+(?:\.\d+)?)", query)
    if price_match and (
        "$" in query or "under" in query.lower() or "less than" in query.lower()
    ):
        max_price = float(price_match.group(1))
        working = working.replace(price_match.group(0), "")

    # Extract size: looks for "size X" (e.g. "size M", "size S/M")
    size = None
    size_match = re.search(r"size\s+([A-Za-z0-9/]+)", query, re.IGNORECASE)
    if size_match:
        size = size_match.group(1)
        working = working.replace(size_match.group(0), "")

    # Strip filler words left over from price/size extraction
    working = re.sub(r"\b(under|less than|dollars?)\b", "", working, flags=re.IGNORECASE)
    description = re.sub(r"\s+", " ", working).strip()

    return {"description": description, "size": size, "max_price": max_price}


# ── session state ─────────────────────────────────────────────────────────────

def _new_session(query: str, wardrobe: dict) -> dict:
    """
    Initialize and return a fresh session dict for one user interaction.

    The session dict is the single source of truth for everything that happens
    during a run — it stores the original query, parsed parameters, tool results,
    and any error that caused early termination.

    You may add fields to this dict as needed for your implementation.
    """
    return {
        "query": query,              # original user query
        "parsed": {},                # extracted description / size / max_price
        "search_results": [],        # list of matching listing dicts
        "selected_item": None,       # top result, passed into suggest_outfit
        "wardrobe": wardrobe,        # user's wardrobe dict
        "outfit_suggestion": None,   # string returned by suggest_outfit
        "fit_card": None,            # string returned by create_fit_card
        "error": None,               # set if the interaction ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Main agent entry point. Runs the FitFindr planning loop for a single
    user interaction and returns the completed session dict.
    """
    # Step 1 — Initialize the session
    session = _new_session(query, wardrobe)

    # Step 2 — Parse the query into description / size / max_price
    session["parsed"] = _parse_query(query)

    # Step 3 — Call search_listings(); branch early on no results or load failure
    try:
        session["search_results"] = search_listings(
            description=session["parsed"]["description"],
            size=session["parsed"]["size"],
            max_price=session["parsed"]["max_price"],
        )
    except (FileNotFoundError, ValueError) as e:
        session["error"] = f"Could not load listings data: {e}"
        return session

    if not session["search_results"]:
        session["error"] = (
            f"No listings found matching '{query}'. "
            "Try a broader description, a higher price limit, or a different size."
        )
        return session  # Early return — do NOT call suggest_outfit or create_fit_card

    # Step 4 — Select the top result
    session["selected_item"] = session["search_results"][0]

    # Step 5 — Suggest an outfit using the selected item + wardrobe
    session["outfit_suggestion"] = suggest_outfit(
        new_item=session["selected_item"],
        wardrobe=session["wardrobe"],
    )

    # Step 6 — Generate the shareable fit card caption
    session["fit_card"] = create_fit_card(
        outfit=session["outfit_suggestion"],
        new_item=session["selected_item"],
    )

    # Step 7 — Return the completed session
    return session


# ── CLI test ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe, get_empty_wardrobe

    print("=== Happy path: graphic tee ===\n")
    session = run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    )
    if session["error"]:
        print(f"Error: {session['error']}")
    else:
        print(f"Found: {session['selected_item']['title']}")
        print(f"\nOutfit: {session['outfit_suggestion']}")
        print(f"\nFit card: {session['fit_card']}")

    print("\n\n=== No-results path ===\n")
    session2 = run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    )
    print(f"Error message: {session2['error']}")