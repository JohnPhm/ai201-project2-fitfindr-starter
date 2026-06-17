# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
Search_listings is a tool that searches the listings dataset for any items that matches the description, size, and optional price ceiling that the user includes. 
**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): Keywords that describe the user's intended item, including 
- `size` (str): A string that describes the size of the article of clothing. The string can also be case-insensitive as it only requires a single letter to denote the sizing. None can be used to skip size filtering.
- `max_price` (float): A numerical value that represents the maximum price that the user is willing to pay for the item (price ceiling). None could also be used to skip over the price filtering. 

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
There are two options for the return value of this tool. This tool could return a matching list dictionary that is sorted based on relevance, where the best match comes first. The other return value that is possible would be an empty list, which occurs if there are no matching items according to the description from the user. Either way, the matching list dictionary will contain id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand, and platform if applicable. 

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
The agent will return an empty list if there are no matching items. This will tell the user that there are no items that exist that match their description. 
---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
The tool suggest_outfit will suggest a couple of completed outfits based on the output produced by the search_listings tool and other information provided by the user.
**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): A listing dictionary of items the user intends to purchase. This dictionary will contain strings that denote what the user wants.
- `wardrobe` (dict): A dictionary that contains key value pairs wardrobe items. The key will be the type of items and the value would be the actual name or description of the item. This dictionary may be empty if there are no matching items provided by search_listings.

**What it returns:**
<!-- Describe the return value -->
The tool will return a non-empty string of outfit suggestions for the user.
**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
If the wardrobe is empty, an empty dictionary may be returned and the tool will alert the user of this error. It could suggest the user try to find another item in order to get a new outfit suggestion. 
---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
The create_fit_card tool will return a short, generated caption about the outfit based on the thrifted find. 
**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (): 
- `new_item `(dict): 

**What it returns:**
<!-- Describe the return value -->
There are two possible return values. The first return value is a short caption that can be used on social media to quickly describe the thrifted look. The second possible return value is a descriptive error message if the outfit is empty or missing, alerting the user of the possibility of no outfits being created due to the missing recommended listings. 

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
If the outfit data is incomplete or if it returns nothing, then the agent should prompt the user with an error message, telling the user to either search for another article of clothing within the listings or that it could not create a caption based on the outfit. 
---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->
The agents will decide which tool to call next based on the information that is provided to the agent. The first tool that is always called is the search_listings tool, which searches the listings for any article of clothing that matches the user's input. Search_listings() will take a description, size, and max price as its three arguments and will return either an error message or a matching list dictionary. If the matching list dictionary is successfully returned with key-value pairs, then the user can select one of the items in the dictionary. From here, the next tool called would be suggest_outfit(selected_item, wardrobe). This tool takes the item that the user selected and the wardrobe dictionary provided by the user. If either one of the arguments is empty, an error message will be prompted. Otherwise, the tool will create an outfit suggestion based on the arguments. After suggest_outfit has been ran, the create_fit_card tool can be used. This tool will either create a caption for the user to use or it will provide an error message. If the tool succeeds, everything has ran succesfully. 
---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | |
| suggest_outfit | Wardrobe is empty | |
| create_fit_card | Outfit input is missing or incomplete | |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     ASCII art, a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html), or an embedded
     sketch are all fine. You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->
User Query
     |
     v
Planning Loop -----------------------------------------------------------------------------
     |                                                                                    |
     |--> search_listings(description, size, max_price)  <------------------              |
     |         |                                                           |              |
     |         |--> [Error] "No Listings Found..." --> return and prompt user to search again 
     |         |                                                                          |
     |         | results=[items,...,...]                                                  |
     |         v                                                                          |
     |         Session: selected_item = results[x] (user selects item)                    |
     |         |                                                                          |
     |         v                                                                          |
     |--> suggest_outfit(selected_item, wardrobe) (wardrobe is based on user query) <--   |
     |         |                                                                      | prompt user to change wardrobe
     |         |--> [Error] "Cannot generate suggested outfit" ------------------------   |
     |         |                                                                          |
     |         Session: outfit_suggestion = "..."                                         |
     |         |                                                                          |
     |         |                                                                          |
     |--> create_fit_card(outfit_suggestion, selected_item)                               |
               |                                                                          |
               |--> [Error] "Cannot generate caption"                                     |
               |                                                                          |
               Session: fit_card = "..."                                                  |
               |                                                                          |
               v                                                                          v
               Return session                                                  Error Path Return
---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->
     For this project, I plan to use Claude to help me implement the project. From this planning.md file, I will provide Claude with each section and prompt it to execute and implement each section. I will run checks on the generated code to ensure that it runs and executes the logic that I included in the plan. Furthermore, I will run test queries on each section and test it against my own hand-written logic. This ensures that the generated code is functioning as intended. For example, I will provide Claude the first tool search_listings() along with the appropriate arguments and data (in this case, listings.json). Once the code has been generated, I will run it and examine its output while comparing it with my hand-traced output. Once I have verified that the logic is working as intended, I will continue on with the next tool while using the same testing method. 

**Milestone 3 — Individual tool implementations:**

**Milestone 4 — Planning loop and state management:**

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I am looking for a track jacket under $50 in a size medium. I usually wear jeans and low top sneakers. What are my options out there and how can I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
The first step that the agent would do first would be calling the search_listings tool with the details listed in the example user query. In this example, the tool would be search_listings("track jacket", size="M", max_price=50.0). FitFindr returns one result, which is "90s Track Jacket — Navy/White Stripe, $45, Poshmark, Excellent Condition". 
**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
Once search_listings() returns its results, the suggest_outfit tool can be used to return an outfit based on the user's preference for clothes. The tool suggest_outfit(new_item=<track_jacket>, wardrobe=<user's wardrobe>) could return a suggestion telling the user to pair the track jacket with a pair of jeans and low top canvas sneakers. 
**Step 3:**
<!-- Continue until the full interaction is complete -->
Once both tools have been called and used, the final tool create_fit_card will be called upon to generate a short caption for the thrifted find. 
**Final output to user:**
<!-- What does the user actually see at the end? -->
At the end, the user will actually see a complete wardrobe suggestion if there are items that matches what the user wants. If there isn't any matching items, then the user will receive an error message. 