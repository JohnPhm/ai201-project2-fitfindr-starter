# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

#Planning Loop
The planning loop starts with the user query, where the user includes the item they are looking for. The first tool that is used is search_listing(), which takes three arguments as its input. This tool either outputs an error or a resulting dictionary. If the error occurs, a message will prompt the user to try again. The user can then select an item from the dictionary to continue. The following tool called would be the suggest_outfit(), where two arguments are dictionaries - the first one being the chosen item from search_listing() and the second dictionary includes the user's wardrobe. Once the outfit suggestion has been completed, the final tool can be called upon. Create_fit_card() takes the suggestion and the selected item to generate a short caption about the outfit.  

#AI Usage
In this project, AI (more specifically Claude) was used to generate portions of code. For instance, the tool search_listings() was generated using Claude. I prompted Claude with the logic of how search_listings() works and asked it to generate the code. Once the code was generated, I wrote the tests to determine if the logic was followed correctly. I wrote a separate test file to determine if the function works and I also wrote simple terminal commands to quickly determine if the function works. The search_listings() function worked correctly the first time but suggest_outfits() function was not working correctly the first time. Once I determined that the function was not functioning correctly, I revised the function using Claude and tested the functon again to determine the function's logic. I also used AI to help debug specific errors during the setup of the project, including the fixing the versions of the required libraries. 

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
