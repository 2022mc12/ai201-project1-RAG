# added .json to end of reddit links to get the .json file for the webpage
# reddit1.json corresponds to the first link in the document list, and so on
# for the rest of the 5 webpages, just downloaded the html of the web page

# all these files are in the intermediate data folder
import json

def extract_text_json(obj):
    texts = []

    
    if isinstance(obj, dict): 
        # Extract text fields only
        for key in ("title", "selftext", "body"):
            value = obj.get(key)

            # makes sure that the text is a non empty string
            if isinstance(value, str) and value.strip(): 
                lower = value.lower() # more standardized

                # light data cleaning
                exclude = [
                    "[deleted]", # deleted posts
                    "[removed]", # removed posts
                    # bot messages 
                    "i am a bot", 
                    "remindmebot",
                    "sneakpeekbot"
                ]
                if not any(phrase in lower for phrase in exclude):
                    texts.append(value)

        # extract all replies for comments
        # replies for a comment is stored as a field in the dictionary for the comment
        for value in obj.values():
            texts.extend(extract_text_json(value))

    elif isinstance(obj, list):
        # extract text from comments or replies
        # comments for a post (and replies for a comment) are stored as a list of dictionaries
        for item in obj:
            texts.extend(extract_text_json(item))

    return texts





reddit_descriptions = ["Incoming Freshman Commuter Post", "Commuter Experience Post", "Commuter Dining Plan Post", "Commuter Financial Aid Post", "Commuter Advice Post"]
for i in range(1,6):
    with open(f"intermediate_data/reddit{i}.json", "r", encoding="utf-8") as f:
        reddit_json = json.load(f)

    # process json file to extract text
    all_text = extract_text_json(reddit_json)

    # Join into one document
    document = "\n\n".join(all_text)

    with open(f"documents/{reddit_descriptions[i-1]}.txt", "w", encoding="utf-8") as f:
        f.write(document)